#!/usr/bin/env python3
"""Adversarial analysis - Claude Haiku primary, Groq fallback."""
import sys, time, json, subprocess, requests
from datetime import datetime
sys.path.insert(0, '/home/derek/vault/utils/core-skills')
from brain import get_secret

LOG      = '/home/derek/vault/MaeveGenesis/logs/sharpening.log'
VENTURES = '/home/derek/vault/MaeveGenesis/ventures'
CREDS    = '/home/derek/vault/utils/.claude-mcp-servers/multi-ai-collab/credentials.json'
DOCS = {
    'Pulse':    f'{VENTURES}/pulse/BUSINESS_CASE.md',
    'Prism':    f'{VENTURES}/prism/BUSINESS_CASE.md',
    'Forge':    f'{VENTURES}/forge/BUSINESS_CASE.md',
    'Sentinel': f'{VENTURES}/sentinel/BUSINESS_CASE.md',
    'Ghost':    f'{VENTURES}/ghost/BUSINESS_CASE.md',
}
GROQ_MODELS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile']

def log(msg):
    line = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}'
    print(line)
    open(LOG, 'a').write(line + '\n')

def get_keys():
    anthropic = get_secret('ANTHROPIC_API_KEY')
    d = json.load(open(CREDS))
    groq = d.get('groq', {})
    return anthropic, (groq['api_key'] if isinstance(groq, dict) else groq)

def call_claude(key, prompt):
    r = requests.post('https://api.anthropic.com/v1/messages',
        headers={'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'},
        json={'model': 'claude-haiku-4-5-20251001', 'max_tokens': 3000,
              'messages': [{'role': 'user', 'content': prompt}]}, timeout=120)
    if r.status_code in (429, 529):
        raise RuntimeError(f'Claude {r.status_code}')
    r.raise_for_status()
    t = r.json()['content'][0]['text']
    log(f'  claude-haiku OK {len(t)}c')
    return 'claude-haiku-4-5', t

def call_groq(key, prompt):
    h = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    for model in GROQ_MODELS:
        for attempt in range(3):
            r = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=h,
                json={'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 2500},
                timeout=120)
            if r.status_code == 429:
                w = 45 * (attempt + 1)
                log(f'  {model} 429 wait {w}s')
                time.sleep(w)
                continue
            if r.status_code in (400, 404):
                log(f'  {model} {r.status_code} skip')
                break
            r.raise_for_status()
            t = r.json()['choices'][0]['message']['content']
            log(f'  groq/{model} OK {len(t)}c')
            return model, t
        time.sleep(3)
    raise RuntimeError('Groq exhausted')

PROMPT = """Senior venture analyst: adversarial review of this AI micro-SaaS business case.
Specific, rigorous. Real names and numbers. Do not repeat content from the case.

## 1. WEAKNESSES
Critical gaps and overly optimistic assumptions.

## 2. MARKET SIZING REVIEW
Validate or correct TAM/SAM/SOM. Call out anything inflated or unsourced.

## 3. MISSING COMPETITORS
Specific competitors or substitutes not in the document.

## 4. GO-TO-MARKET GAPS
What acquisition strategies are missing or will actually be harder than described?

## 5. DEVIL'S ADVOCATE
The 3 strongest arguments AGAINST building this. Be brutal and specific.

## 6. BACKER'S CHECKLIST
5 specific questions a smart investor demands answered before committing.

BUSINESS CASE:
---
{doc}
---"""

def analyze(product, path, claude_key, groq_key):
    log(f'=== {product} ===')
    doc = open(path).read()
    pr = PROMPT.format(doc=doc[:12000])
    pm, pt = None, None
    sm, st = None, None
    try:
        log('  Primary: Claude Haiku')
        pm, pt = call_claude(claude_key, pr)
    except Exception as e:
        log(f'  Claude failed: {e} - trying Groq')
        try:
            pm, pt = call_groq(groq_key, pr)
        except Exception as e2:
            log(f'  Groq fallback failed: {e2}')
    time.sleep(5)
    if pt:
        try:
            log('  Secondary: Groq second opinion')
            sm, st = call_groq(groq_key, pr)
        except Exception as e:
            log(f'  Secondary skipped: {e}')
    if not pt:
        raise RuntimeError('All models failed')
    out = path.replace('BUSINESS_CASE.md', 'AI_PARTNER_ANALYSIS.md')
    models = [m for m in [pm, sm] if m]
    with open(out, 'w') as f:
        f.write(f'# {product} - AI Adversarial Analysis\n')
        f.write(f'*{datetime.now().isoformat()}*\n')
        f.write(f'*Models: {", ".join(models)}*\n\n---\n\n')
        if pt:
            f.write(f'## {pm} Analysis\n\n{pt}\n')
        if st:
            f.write(f'\n\n---\n\n## {sm} Second Opinion\n\n{st}\n')
    main = open(path).read()
    if 'AI Partner Review' not in main:
        open(path, 'a').write(
            f'\n\n---\n\n## AI Partner Review\n'
            f'[Analysis](./AI_PARTNER_ANALYSIS.md) | '
            f'{", ".join(models)} | {datetime.now().isoformat()}\n'
        )
    log(f'  Done: {models}')

def push(token):
    remote = f'https://{token}@github.com/DMoneyOH/maeve-genesis-ventures.git'
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    for cmd in [
        f'cd {VENTURES} && git remote set-url origin {remote}',
        f'cd {VENTURES} && git add -A',
        f"cd {VENTURES} && git commit -m 'Adversarial all 5 {ts}'",
        f'cd {VENTURES} && git push origin main',
    ]:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if r.returncode != 0 and 'nothing to commit' not in out:
            log(f'git err: {out[-100:]}')
            return False
    return True

def run():
    log('=== Claude-Primary Adversarial: All 5 Ventures ===')
    claude_key, groq_key = get_keys()
    gh = get_secret('GITHUB_TOKEN')
    tg = get_secret('TELEGRAM_BOT_TOKEN')
    cid = get_secret('TELEGRAM_CHAT_ID')
    log(f'Claude key: {claude_key[:15] if claude_key else "NOT FOUND"}')
    results = {}
    for product, path in DOCS.items():
        try:
            analyze(product, path, claude_key, groq_key)
            results[product] = 'OK'
        except Exception as e:
            log(f'{product} FAILED: {e}')
            results[product] = 'FAILED'
        time.sleep(5)
    ok = push(gh)
    n = sum(1 for v in results.values() if v == 'OK')
    status = '\n'.join(f'{k}: {v}' for k, v in results.items())
    links = '\n'.join(
        f'  {p}: github.com/DMoneyOH/maeve-genesis-ventures/blob/main/{p.lower()}/AI_PARTNER_ANALYSIS.md'
        for p in DOCS if results.get(p) == 'OK'
    )
    msg = (
        f'MaeveGenesis Adversarial Analysis ({n}/5)\n\n{status}\n\n'
        f'Analyses:\n{links}\n\ngithub.com/DMoneyOH/maeve-genesis-ventures'
    ) if ok else f'Done but push failed.\n{status}'
    requests.post(f'https://api.telegram.org/bot{tg}/sendMessage',
        json={'chat_id': cid, 'text': msg}, timeout=10)
    log(f'Complete {n}/5. Telegram sent.')

if __name__ == '__main__':
    run()
