#!/usr/bin/env python3
"""
Groq-only adversarial analysis for all 5 MaeveGenesis ventures.
No Gemini — runs clean. Gemini supplement scheduled for midnight PT reset.
"""
import sys, time, json, subprocess, requests
from datetime import datetime

sys.path.insert(0, '/home/derek/vault/utils/core-skills')
from brain import get_secret

LOG      = '/home/derek/vault/MaeveGenesis/logs/sharpening.log'
VENTURES = '/home/derek/vault/MaeveGenesis/ventures'
CREDS    = '/home/derek/vault/utils/.claude-mcp-servers/multi-ai-collab/credentials.json'

DOCS = {
    'Sentinel': f'{VENTURES}/sentinel/BUSINESS_CASE.md',
    'Ghost':    f'{VENTURES}/ghost/BUSINESS_CASE.md',
    'Pulse':    f'{VENTURES}/pulse/BUSINESS_CASE.md',
    'Prism':    f'{VENTURES}/prism/BUSINESS_CASE.md',
    'Forge':    f'{VENTURES}/forge/BUSINESS_CASE.md',
}

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

def call_groq(api_key, prompt, retries=6):
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    for attempt in range(retries):
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
            wait = 65 * (attempt + 1)
            log(f'Groq rate limit — waiting {wait}s...')
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']
    raise RuntimeError('Groq max retries exceeded')

PROMPT = """You are a seasoned venture analyst reviewing a business case for an AI micro-SaaS product.

Provide a rigorous adversarial analysis. Be specific — use real company names and numbers. Do not repeat content from the case; challenge and add to it.

## 1. WEAKNESSES
Gaps, overly optimistic assumptions, or missing considerations.

## 2. MARKET SIZING REVIEW
Validate or correct TAM/SAM/SOM. Flag inflated or unsourced numbers.

## 3. MISSING COMPETITIVE INTELLIGENCE
Specific competitors or substitutes not in the document.

## 4. GO-TO-MARKET GAPS
What acquisition tactics are missing, underspecified, or likely to underperform?

## 5. DEVIL'S ADVOCATE
The 3 strongest arguments AGAINST building this. Be brutal.

## 6. BACKER'S CHECKLIST
5 specific questions a smart investor would demand answers to before committing.

BUSINESS CASE:
---
{doc}
---"""

def run_one(product, doc_path, groq_key):
    log(f'--- {product} ---')
    with open(doc_path) as f:
        doc = f.read()
    prompt = PROMPT.format(doc=doc[:14000])
    log(f'{product}: Calling Groq...')
    result = call_groq(groq_key, prompt)
    log(f'{product}: {len(result)} chars received')

    out_path = doc_path.replace('BUSINESS_CASE.md', 'AI_PARTNER_ANALYSIS.md')
    with open(out_path, 'w') as f:
        f.write(f'# {product} — AI Adversarial Analysis\n')
        f.write(f'*Model: Groq Llama 3.3 70B | {datetime.now().isoformat()}*\n')
        f.write(f'*Note: Gemini supplement scheduled for midnight PT quota reset.*\n\n')
        f.write('---\n\n')
        f.write(result)

    with open(doc_path) as f:
        main = f.read()
    if 'AI Partner Review' not in main:
        with open(doc_path, 'a') as f:
            f.write('\n\n---\n\n## AI Partner Review\n\n')
            f.write(f'[Full adversarial analysis →](./AI_PARTNER_ANALYSIS.md)  \n')
            f.write(f'*{datetime.now().isoformat()}*\n')
    log(f'{product}: Done')

def push(token):
    remote = f'https://{token}@github.com/DMoneyOH/maeve-genesis-ventures.git'
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    for cmd in [
        f'cd {VENTURES} && git remote set-url origin {remote}',
        f'cd {VENTURES} && git add -A',
        f"cd {VENTURES} && git commit -m 'Adversarial analysis all 5 ventures (Groq) {ts}'",
        f'cd {VENTURES} && git push origin main',
    ]:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        safe = cmd.replace(token,'***')[:65]
        if r.returncode != 0 and 'nothing to commit' not in out:
            log(f'Git error: {safe} — {out[-150:]}')
            return False
        log(f'OK: {safe}')
    return True

def run():
    log('=== Groq-Only Adversarial Run: All 5 Ventures ===')
    groq_key = get_groq_key()
    gh_token = get_secret('GITHUB_TOKEN')
    tg_token = get_secret('TELEGRAM_BOT_TOKEN')
    chat_id  = get_secret('TELEGRAM_CHAT_ID')

    results = {}
    for product, doc_path in DOCS.items():
        try:
            run_one(product, doc_path, groq_key)
            results[product] = 'OK'
        except Exception as e:
            log(f'{product} FAILED: {e}')
            results[product] = f'FAILED: {e}'
        time.sleep(10)

    ok = push(gh_token)
    status = '\n'.join(f'{k}: {v}' for k, v in results.items())
    n_ok = sum(1 for v in results.values() if v == 'OK')

    if ok:
        links = '\n'.join(
            f'  {p}: github.com/DMoneyOH/maeve-genesis-ventures/blob/main/{p.lower()}/AI_PARTNER_ANALYSIS.md'
            for p in DOCS if results.get(p) == 'OK'
        )
        msg = (
            f'MaeveGenesis — All 5 Venture Analyses Complete ({n_ok}/5)\n\n'
            f'{status}\n\n'
            f'Analyses:\n{links}\n\n'
            f'Repo: github.com/DMoneyOH/maeve-genesis-ventures\n\n'
            f'(Gemini supplement: scheduled midnight PT)'
        )
    else:
        msg = f'MaeveGenesis: analysis done but GitHub push failed.\n{status}'

    requests.post(f'https://api.telegram.org/bot{tg_token}/sendMessage',
        json={'chat_id': chat_id, 'text': msg}, timeout=10)
    log(f'Done. {n_ok}/5 complete. Telegram sent.')

if __name__ == '__main__':
    run()
