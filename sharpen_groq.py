#!/usr/bin/env python3
"""
MaeveGenesis AI Sharpening — Groq-only run.
Gemini daily quota exhausted. This runs Groq on both docs, pushes to GitHub, notifies via Telegram.
"""
import sys, time, json, subprocess, requests
from datetime import datetime

sys.path.insert(0, '/home/derek/vault/utils/core-skills')
from brain import get_secret

LOG      = '/home/derek/vault/MaeveGenesis/logs/sharpening.log'
VENTURES = '/home/derek/vault/MaeveGenesis/ventures'
DOCS     = {
    'Sentinel': f'{VENTURES}/sentinel/BUSINESS_CASE.md',
    'Ghost':    f'{VENTURES}/ghost/BUSINESS_CASE.md',
}
CREDS = '/home/derek/vault/utils/.claude-mcp-servers/multi-ai-collab/credentials.json'

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line)
    with open(LOG, 'a') as f:
        f.write(line + '\n')

def get_groq_key():
    with open(CREDS) as f:
        d = json.load(f)
    groq = d.get('groq', {})
    return groq['api_key'] if isinstance(groq, dict) else groq

def call_groq(api_key, prompt):
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    for attempt in range(5):
        r = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json={
                'model': 'llama-3.3-70b-versatile',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 4096,
                'temperature': 0.7
            },
            timeout=120
        )
        if r.status_code == 429:
            wait = 60 * (attempt + 1)
            log(f'Groq rate limited — waiting {wait}s...')
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']
    raise RuntimeError('Groq: max retries exceeded')

PROMPT = """You are a seasoned venture analyst and startup advisor reviewing a business case for an AI micro-SaaS product.

Your analysis must cover six sections:

1. WEAKNESSES — gaps, overly optimistic assumptions, missing considerations
2. MARKET SIZING REVIEW — validate or correct the TAM/SAM/SOM with any additional data
3. COMPETITIVE INTELLIGENCE — any competitors or analogues not mentioned in the doc
4. GO-TO-MARKET ELABORATION — specific actionable tactics beyond what is already outlined
5. DEVIL'S ADVOCATE — the 3 strongest arguments AGAINST building this product
6. BACKER'S CHECKLIST — 5 specific questions a smart investor would demand answers to before committing

Rules: Be specific. Use real company names and real numbers where possible. Do not be generic or repeat content from the business case verbatim. If uncertain, say so.

Format: Return clean Markdown. Start each section with a ## header.

BUSINESS CASE:
---
{doc}
---"""

def sharpen(product, doc_path, groq_key):
    log(f'--- Sharpening {product} ---')
    with open(doc_path) as f:
        doc = f.read()

    prompt = PROMPT.format(doc=doc[:14000])
    log(f'{product}: Calling Groq (Llama 3.3 70B)...')
    analysis = call_groq(groq_key, prompt)
    log(f'{product}: Got {len(analysis)} chars')

    # Write analysis file
    out_path = doc_path.replace('BUSINESS_CASE.md', 'AI_PARTNER_ANALYSIS.md')
    with open(out_path, 'w') as f:
        f.write(f'# {product} — AI Partner Analysis\n')
        f.write(f'*Model: Groq Llama 3.3 70B | Generated: {datetime.now().isoformat()}*\n')
        f.write(f'*Note: Gemini daily quota exhausted — Groq-only run. Gemini supplement scheduled for next reset.*\n\n')
        f.write('---\n\n')
        f.write(analysis)
    log(f'{product}: Written to {out_path}')

    # Append reference to main doc (avoid duplicates)
    with open(doc_path) as f:
        existing = f.read()
    if 'AI Partner Review' not in existing:
        with open(doc_path, 'a') as f:
            f.write('\n\n---\n\n')
            f.write('## AI Partner Review\n\n')
            f.write(f'[Full AI analysis →](./{product}_AI_PARTNER_ANALYSIS.md)  \n')
            f.write(f'*Analysis generated: {datetime.now().isoformat()}*\n')
    return out_path

def push(token):
    remote = f'https://{token}@github.com/DMoneyOH/maeve-genesis-ventures.git'
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    cmds = [
        f'cd {VENTURES} && git remote set-url origin {remote}',
        f'cd {VENTURES} && git add -A',
        f"cd {VENTURES} && git commit -m 'AI sharpening (Groq): Sentinel + Ghost {ts}'",
        f'cd {VENTURES} && git push origin main',
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        safe = cmd.replace(token, '***')[:65]
        out = (r.stdout + r.stderr).strip()
        if r.returncode != 0 and 'nothing to commit' not in out:
            log(f'Git error [{r.returncode}]: {safe}')
            log(f'  {out[-200:]}')
            return False
        log(f'OK: {safe}')
    return True

def run():
    log('=== Groq-Only Sharpening Start ===')
    groq_key  = get_groq_key()
    gh_token  = get_secret('GITHUB_TOKEN')
    tg_token  = get_secret('TELEGRAM_BOT_TOKEN')
    chat_id   = get_secret('TELEGRAM_CHAT_ID')

    results = {}
    for product, doc_path in DOCS.items():
        try:
            sharpen(product, doc_path, groq_key)
            results[product] = 'OK'
        except Exception as e:
            log(f'{product} failed: {e}')
            results[product] = f'FAILED: {e}'
        time.sleep(8)

    log('Pushing to GitHub...')
    ok = push(gh_token)

    status_lines = '\n'.join(f'{k}: {v}' for k, v in results.items())
    if ok:
        msg = (
            'MaeveGenesis Ventures — AI Analysis Ready\n\n'
            f'{status_lines}\n\n'
            'Sentinel:\nhttps://github.com/DMoneyOH/maeve-genesis-ventures/blob/main/sentinel/AI_PARTNER_ANALYSIS.md\n\n'
            'Ghost:\nhttps://github.com/DMoneyOH/maeve-genesis-ventures/blob/main/ghost/AI_PARTNER_ANALYSIS.md\n\n'
            'Repo:\nhttps://github.com/DMoneyOH/maeve-genesis-ventures\n\n'
            '(Gemini supplement will run at next daily reset ~midnight PT)'
        )
    else:
        msg = f'MaeveGenesis sharpening: GitHub push failed.\n{status_lines}\nCheck sharpening.log'

    requests.post(f'https://api.telegram.org/bot{tg_token}/sendMessage',
        json={'chat_id': chat_id, 'text': msg}, timeout=10)
    log('Telegram sent.')
    log('=== Done ===')

if __name__ == '__main__':
    run()
