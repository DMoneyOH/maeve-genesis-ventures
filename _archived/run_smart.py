#!/usr/bin/env python3
"""Smart-routed adversarial analysis: tries qwen-qwq-32b, then llama-3.1-8b-instant, then gemini-2.5-flash."""
import sys, time, json, subprocess, requests
from datetime import datetime
sys.path.insert(0, '/home/derek/vault/utils/core-skills')
from brain import get_secret

LOG = '/home/derek/vault/MaeveGenesis/logs/sharpening.log'
VENTURES = '/home/derek/vault/MaeveGenesis/ventures'
CREDS = '/home/derek/vault/utils/.claude-mcp-servers/multi-ai-collab/credentials.json'
DOCS = {
    'Sentinel': f'{VENTURES}/sentinel/BUSINESS_CASE.md',
    'Ghost':    f'{VENTURES}/ghost/BUSINESS_CASE.md',
    'Pulse':    f'{VENTURES}/pulse/BUSINESS_CASE.md',
    'Prism':    f'{VENTURES}/prism/BUSINESS_CASE.md',
    'Forge':    f'{VENTURES}/forge/BUSINESS_CASE.md',
}
GROQ_MODELS = ['qwen-qwq-32b', 'llama-3.1-8b-instant', 'llama-3.3-70b-versatile']

def log(msg):
    line = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}'
    print(line)
    open(LOG, 'a').write(line + '\n')

def get_keys():
    d = json.load(open(CREDS))
    g = d['gemini']['api_key'] if isinstance(d['gemini'], dict) else d['gemini']
    q = d.get('groq', {})
    return g, (q['api_key'] if isinstance(q, dict) else q)

def groq_call(key, prompt):
    h = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    for m in GROQ_MODELS:
        log(f'  groq/{m}')
        for attempt in range(3):
            r = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=h,
                json={'model': m, 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 2500}, timeout=120)
            if r.status_code == 429:
                w = 50 * (attempt + 1)
                log(f'  429 wait {w}s')
                time.sleep(w)
                continue
            if r.status_code in (400, 404, 422):
                log(f'  {m} {r.status_code} skip')
                break
            r.raise_for_status()
            t = r.json()['choices'][0]['message']['content']
            log(f'  {m} OK {len(t)}c')
            return m, t
        time.sleep(3)
    raise RuntimeError('All Groq models failed')

def gemini_call(key, prompt):
    import google.genai as genai
    c = genai.Client(api_key=key)
    for m in ['gemini-2.5-flash', 'gemini-2.0-flash']:
        try:
            log(f'  gemini/{m}')
            r = c.models.generate_content(model=m, contents=prompt, config={'max_output_tokens': 2500})
            log(f'  {m} OK {len(r.text)}c')
            return m, r.text
        except Exception as e:
            log(f'  {m} skip: {str(e)[:60]}')
            time.sleep(3)
    return None, None

PROMPT = """Venture analyst: give adversarial analysis of this AI micro-SaaS business case.
Be specific, use real names/numbers, do not repeat the case content.

## 1. WEAKNESSES
## 2. MARKET SIZING REVIEW
## 3. MISSING COMPETITORS
## 4. GO-TO-MARKET GAPS
## 5. DEVIL'S ADVOCATE (3 strongest arguments against)
## 6. BACKER'S CHECKLIST (5 investor questions)

BUSINESS CASE:
---
{doc}
---"""

def analyze(product, path, groq_key, gem_key):
    log(f'=== {product} ===')
    doc = open(path).read()
    pr = PROMPT.format(doc=doc[:11000])
    gm, gr = None, None
    emm, emr = None, None
    try:
        gm, gr = groq_call(groq_key, pr)
    except Exception as e:
        log(f'  groq failed: {e}')
    time.sleep(5)
    try:
        emm, emr = gemini_call(gem_key, pr)
    except Exception as e:
        log(f'  gemini failed: {e}')
    if not gr and not emr:
        raise RuntimeError('all partners failed')
    out = path.replace('BUSINESS_CASE.md', 'AI_PARTNER_ANALYSIS.md')
    models = []
    with open(out, 'w') as f:
        f.write(f'# {product} - AI Adversarial Analysis\n*{datetime.now().isoformat()}*\n\n---\n\n')
        if gr:
            models.append(gm)
            f.write(f'## Groq: {gm}\n\n{gr}\n')
        if emr:
            models.append(emm)
            f.write(f'\n\n---\n\n## Gemini: {emm}\n\n{emr}\n')
    main = open(path).read()
    if 'AI Partner Review' not in main:
        open(path, 'a').write(f'\n\n---\n\n## AI Partner Review\n[Analysis](./AI_PARTNER_ANALYSIS.md) | {", ".join(models)} | {datetime.now().isoformat()}\n')
    log(f'  done: {models}')

def push(token):
    remote = f'https://{token}@github.com/DMoneyOH/maeve-genesis-ventures.git'
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    for cmd in [
        f'cd {VENTURES} && git remote set-url origin {remote}',
        f'cd {VENTURES} && git add -A',
        f"cd {VENTURES} && git commit -m 'adversarial all 5 {ts}'",
        f'cd {VENTURES} && git push origin main',
    ]:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if r.returncode != 0 and 'nothing to commit' not in out:
            log(f'git error: {out[-100:]}')
            return False
    return True

def run():
    log('=== Smart Adversarial Run ===')
    gem_key, groq_key = get_keys()
    gh = get_secret('GITHUB_TOKEN')
    tg = get_secret('TELEGRAM_BOT_TOKEN')
    cid = get_secret('TELEGRAM_CHAT_ID')
    results = {}
    for p, path in DOCS.items():
        try:
            analyze(p, path, groq_key, gem_key)
            results[p] = 'OK'
        except Exception as e:
            log(f'{p} FAILED: {e}')
            results[p] = f'FAILED'
        time.sleep(8)
    ok = push(gh)
    n = sum(1 for v in results.values() if v == 'OK')
    status = '\n'.join(f'{k}: {v}' for k,v in results.items())
    links = '\n'.join(f'  {p}: github.com/DMoneyOH/maeve-genesis-ventures/blob/main/{p.lower()}/AI_PARTNER_ANALYSIS.md' for p in DOCS if results.get(p)=='OK')
    msg = f'MaeveGenesis Adversarial Analysis ({n}/5)\n\n{status}\n\n{links}\n\ngithub.com/DMoneyOH/maeve-genesis-ventures' if ok else f'Done but push failed.\n{status}'
    requests.post(f'https://api.telegram.org/bot{tg}/sendMessage', json={'chat_id': cid, 'text': msg}, timeout=10)
    log(f'complete {n}/5')

if __name__ == '__main__':
    run()
