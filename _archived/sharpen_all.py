#!/usr/bin/env python3
"""
MaeveGenesis Full Adversarial Analysis
Runs all 5 venture business cases through Groq (Llama 3.3 70B) + Gemini (if available).
Pushes results to GitHub and notifies via Telegram.
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

def get_keys():
    with open(CREDS) as f:
        d = json.load(f)
    gemini = d['gemini']['api_key'] if isinstance(d['gemini'], dict) else d['gemini']
    groq = d.get('groq', {})
    groq_key = groq['api_key'] if isinstance(groq, dict) else groq
    return gemini, groq_key

def call_groq(api_key, prompt, retries=5):
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
            log(f'Groq rate limited — waiting {wait}s (attempt {attempt+1})...')
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']
    raise RuntimeError('Groq max retries exceeded')

def call_gemini(api_key, prompt, retries=2):
    import google.genai as genai
    client = genai.Client(api_key=api_key)
    for attempt in range(retries):
        try:
            resp = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config={'temperature': 0.7, 'max_output_tokens': 4096}
            )
            return resp.text
        except Exception as e:
            if any(x in str(e) for x in ['429','quota','rate','RetryInfo','RESOURCE_EXHAUSTED']):
                wait = 70 * (attempt + 1)
                log(f'Gemini rate limited — waiting {wait}s...')
                time.sleep(wait)
            else:
                raise
    raise RuntimeError('Gemini quota exhausted')

PROMPT = """You are a seasoned venture analyst and startup advisor reviewing a business case for an AI micro-SaaS product.

Provide a rigorous adversarial analysis covering all six sections below. Be specific, use real company names and numbers where possible. Do not repeat content from the business case — add to it or challenge it.

## 1. WEAKNESSES
Identify gaps, overly optimistic assumptions, or missing considerations in the business case.

## 2. MARKET SIZING REVIEW
Validate or correct the TAM/SAM/SOM. Flag any numbers that seem inflated or sourced incorrectly.

## 3. MISSING COMPETITIVE INTELLIGENCE
Name specific competitors, analogues, or substitutes not mentioned in the document.

## 4. GO-TO-MARKET GAPS
What acquisition strategies are missing, underspecified, or likely to underperform? Add specific tactics.

## 5. DEVIL'S ADVOCATE
The 3 strongest arguments AGAINST building this product. Be brutal — these should be arguments that could kill the venture.

## 6. BACKER'S CHECKLIST
5 specific questions a smart investor would demand answers to before committing capital. These should expose the key unknowns.

BUSINESS CASE:
---
{doc}
---"""

def already_analyzed(doc_path):
    out = doc_path.replace('BUSINESS_CASE.md', 'AI_PARTNER_ANALYSIS.md')
    try:
        content = open(out).read()
        return len(content) > 500
    except:
        return False

def sharpen(product, doc_path, groq_key, gemini_key):
    if already_analyzed(doc_path):
        log(f'{product}: Analysis already exists — re-running to refresh.')

    log(f'--- {product} ---')
    with open(doc_path) as f:
        doc = f.read()

    prompt = PROMPT.format(doc=doc[:14000])

    # Groq primary
    groq_result = None
    log(f'{product}: Calling Groq...')
    try:
        groq_result = call_groq(groq_key, prompt)
        log(f'{product}: Groq done ({len(groq_result)} chars)')
    except Exception as e:
        log(f'{product}: Groq failed — {e}')

    time.sleep(8)

    # Gemini optional
    gemini_result = None
    try:
        log(f'{product}: Calling Gemini (optional)...')
        gemini_result = call_gemini(gemini_key, prompt)
        log(f'{product}: Gemini done ({len(gemini_result)} chars)')
    except Exception as e:
        log(f'{product}: Gemini skipped — {e}')

    if not groq_result and not gemini_result:
        raise RuntimeError(f'{product}: Both AI partners failed')

    # Write analysis
    out_path = doc_path.replace('BUSINESS_CASE.md', 'AI_PARTNER_ANALYSIS.md')
    with open(out_path, 'w') as f:
        f.write(f'# {product} — AI Partner Adversarial Analysis\n')
        f.write(f'*Generated: {datetime.now().isoformat()}*\n')
        models = []
        if groq_result: models.append('Groq Llama 3.3 70B')
        if gemini_result: models.append('Gemini 2.0 Flash')
        f.write(f'*Models: {", ".join(models)}*\n\n')
        f.write('---\n\n')
        if groq_result:
            f.write('## Groq (Llama 3.3 70B) Analysis\n\n')
            f.write(groq_result)
        if gemini_result:
            f.write('\n\n---\n\n')
            f.write('## Gemini 2.0 Flash Analysis\n\n')
            f.write(gemini_result)

    log(f'{product}: Written to {out_path}')

    # Update main doc with reference (avoid duplicates)
    with open(doc_path) as f:
        main = f.read()
    if 'AI Partner Review' not in main:
        with open(doc_path, 'a') as f:
            f.write('\n\n---\n\n')
            f.write('## AI Partner Review\n\n')
            f.write(f'[Full adversarial analysis →](./AI_PARTNER_ANALYSIS.md)  \n')
            f.write(f'*Analysis generated: {datetime.now().isoformat()}*\n')

    return out_path

def push(token):
    remote = f'https://{token}@github.com/DMoneyOH/maeve-genesis-ventures.git'
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    cmds = [
        f'cd {VENTURES} && git remote set-url origin {remote}',
        f'cd {VENTURES} && git add -A',
        f"cd {VENTURES} && git commit -m 'Full adversarial analysis: all 5 ventures {ts}'",
        f'cd {VENTURES} && git push origin main',
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        safe = cmd.replace(token, '***')[:65]
        if r.returncode != 0 and 'nothing to commit' not in out:
            log(f'Git error: {safe} — {out[-200:]}')
            return False
        log(f'OK: {safe}')
    return True

def notify(tg_token, chat_id, msg):
    requests.post(f'https://api.telegram.org/bot{tg_token}/sendMessage',
        json={'chat_id': chat_id, 'text': msg}, timeout=10)

def run():
    log('=== Full Adversarial Analysis — All 5 Ventures ===')
    gemini_key, groq_key = get_keys()
    gh_token = get_secret('GITHUB_TOKEN')
    tg_token = get_secret('TELEGRAM_BOT_TOKEN')
    chat_id  = get_secret('TELEGRAM_CHAT_ID')

    results = {}
    for product, doc_path in DOCS.items():
        try:
            sharpen(product, doc_path, groq_key, gemini_key)
            results[product] = 'OK'
        except Exception as e:
            log(f'{product} FAILED: {e}')
            results[product] = f'FAILED: {e}'
        time.sleep(10)

    log('Pushing to GitHub...')
    ok = push(gh_token)

    status = '\n'.join(f'{k}: {v}' for k, v in results.items())
    success_count = sum(1 for v in results.values() if v == 'OK')

    if ok:
        links = '\n'.join(
            f'{p}: https://github.com/DMoneyOH/maeve-genesis-ventures/blob/main/{p.lower()}/AI_PARTNER_ANALYSIS.md'
            for p in DOCS if results.get(p) == 'OK'
        )
        msg = (
            f'MaeveGenesis — All 5 Venture Analyses Complete\n\n'
            f'{success_count}/5 succeeded\n\n'
            f'{status}\n\n'
            f'Analysis links:\n{links}\n\n'
            f'Repo: https://github.com/DMoneyOH/maeve-genesis-ventures'
        )
    else:
        msg = f'MaeveGenesis adversarial analysis: GitHub push failed.\n{status}'

    notify(tg_token, chat_id, msg)
    log(f'Telegram sent. {success_count}/5 completed.')
    log('=== Done ===')

if __name__ == '__main__':
    run()
