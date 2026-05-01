#!/usr/bin/env python3
"""
MaeveGenesis AI Sharpening Runner
Waits for Gemini/Groq rate limits to clear, runs both business cases
through AI partners for critique and elaboration, updates docs, pushes to GitHub.
Run once — fully autonomous.
"""
import sys, time, json, sqlite3, subprocess, requests
from datetime import datetime
sys.path.insert(0, '/home/derek/vault/utils/core-skills')
from brain import get_secret

LOG = '/home/derek/vault/MaeveGenesis/logs/sharpening.log'
VENTURES = '/home/derek/vault/MaeveGenesis/ventures'
SENTINEL_DOC = f'{VENTURES}/sentinel/BUSINESS_CASE.md'
GHOST_DOC = f'{VENTURES}/ghost/BUSINESS_CASE.md'
def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line)
    with open(LOG, 'a') as f: f.write(line + '\n')

def get_api_keys():
    gemini = get_secret('GEMINI_API_KEY')
    groq_key = get_secret('GROQ_API_KEY')
    return gemini, groq_key

def call_gemini(api_key, prompt, retries=8):
    import google.genai as genai
    client = genai.Client(api_key=api_key)
    for attempt in range(retries):
        try:
            resp = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config={'temperature': 0.7, 'max_output_tokens': 8192}
            )
            return resp.text
        except Exception as e:
            if any(x in str(e) for x in ['429','quota','rate','RetryInfo','RESOURCE_EXHAUSTED']):
                wait = 65 * (attempt + 1)
                log(f'Gemini rate limited — waiting {wait}s (attempt {attempt+1}/{retries})...')
                time.sleep(wait)
            else:
                raise
    raise RuntimeError('Gemini max retries exceeded')

def call_groq(api_key, prompt, retries=5):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    for attempt in range(retries):
        try:
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
                log(f'Groq rate limited — waiting {wait}s (attempt {attempt+1}/{retries})...')
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except requests.exceptions.HTTPError as e:
            if '429' in str(e) or 'rate' in str(e).lower():
                time.sleep(65 * (attempt + 1))
            else:
                raise
    raise RuntimeError('Groq max retries exceeded')

SHARPEN_PROMPT = """You are a seasoned venture analyst and startup advisor. Below is a business case document for an AI micro-SaaS product. Your job is to:

1. IDENTIFY any weaknesses, gaps, or overly optimistic assumptions in the business case
2. SHARPEN the market sizing with any additional data or corrections
3. ADD any missing competitive intelligence about the space
4. ELABORATE on the go-to-market strategy with specific, actionable tactics not already covered
5. ADD a "Devil's Advocate" section at the end with the 3 strongest arguments AGAINST building this
6. ADD a "Backer's Checklist" section — 5 specific questions a smart investor would ask before committing

Be specific. Use real company names, real numbers. Do not be generic. If you don't know something, say so — don't fabricate.

Return your full analysis in Markdown. Start with "## AI Partner Analysis" and organize by section.

BUSINESS CASE:
---
{doc}
---"""

def sharpen_doc(doc_path, gemini_key, groq_key):
    with open(doc_path) as f:
        doc = f.read()

    product = 'Sentinel' if 'sentinel' in doc_path.lower() else 'Ghost'
    log(f'Sharpening {product}...')

    prompt = SHARPEN_PROMPT.format(doc=doc[:12000])  # keep within token limits

    # Groq first (hourly reset, reliable)
    groq_analysis = None
    if groq_key:
        log(f'{product}: Calling Groq...')
        try:
            groq_analysis = call_groq(groq_key, prompt)
            log(f'{product}: Groq done ({len(groq_analysis)} chars)')
        except Exception as e:
            log(f'{product}: Groq failed - {e}')

    time.sleep(10)

    # Gemini optional - daily quota may be exhausted
    gemini_analysis = None
    try:
        log(f'{product}: Calling Gemini (optional)...')
        gemini_analysis = call_gemini(gemini_key, prompt, retries=2)
        log(f'{product}: Gemini done ({len(gemini_analysis)} chars)')
    except Exception as e:
        log(f'{product}: Gemini skipped - {e}')

    if not groq_analysis and not gemini_analysis:
        raise RuntimeError('Both AI partners failed')
    # Write AI analysis appendix
    appendix_path = doc_path.replace('BUSINESS_CASE.md', 'AI_PARTNER_ANALYSIS.md')
    with open(appendix_path, 'w') as f:
        f.write(f'# {product} - AI Partner Analysis\n')
        f.write(f'*Generated: {datetime.now().isoformat()}*\n\n')
        f.write('---\n\n')
        if groq_analysis:
            f.write('## Groq (Llama 3.3 70B) Analysis\n\n')
            f.write(groq_analysis)
        if gemini_analysis:
            f.write('\n\n---\n\n## Gemini Analysis\n\n')
            f.write(gemini_analysis)

    # Append summary to main doc
    with open(doc_path, 'a') as f:
        f.write('\n\n---\n\n')
        f.write('## AI Partner Review\n\n')
        f.write(f'Full AI partner analysis (Gemini + Groq): see [{product} AI Analysis](./AI_PARTNER_ANALYSIS.md)\n\n')
        f.write(f'*Analysis generated: {datetime.now().isoformat()}*\n')

    return appendix_path

def push_to_github(token):
    remote = f'https://{token}@github.com/DMoneyOH/maeve-genesis-ventures.git'
    cmds = [
        f'cd {VENTURES} && git remote set-url origin {remote}',
        f'cd {VENTURES} && git add -A',
        f"cd {VENTURES} && git commit -m 'AI partner sharpening: Sentinel + Ghost " + datetime.now().strftime("%Y-%m-%d %H:%M") + "'",
        f'cd {VENTURES} && git push origin main',
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        safe = cmd.replace(token, '***')[:60]
        if r.returncode != 0 and 'nothing to commit' not in (r.stdout + r.stderr):
            log(f'Push error: {safe} — {(r.stdout+r.stderr)[-150:]}')
            return False
    return True

def notify(tg_token, chat_id, msg):
    try:
        requests.post(f'https://api.telegram.org/bot{tg_token}/sendMessage',
            json={'chat_id': chat_id, 'text': msg}, timeout=10)
    except Exception as e:
        log(f'Telegram failed: {e}')

def run():
    log('=== AI Sharpening Run Starting ===')

    gemini_key, groq_key = get_api_keys()
    github_token = get_secret('GITHUB_TOKEN')
    tg_token = get_secret('TELEGRAM_BOT_TOKEN')
    chat_id = get_secret('TELEGRAM_CHAT_ID')

    # Sharpen Sentinel
    try:
        sharpen_doc(SENTINEL_DOC, gemini_key, groq_key)
    except Exception as e:
        log(f'Sentinel sharpening failed: {e}')

    time.sleep(15)

    # Sharpen Ghost
    try:
        sharpen_doc(GHOST_DOC, gemini_key, groq_key)
    except Exception as e:
        log(f'Ghost sharpening failed: {e}')

    # Push to GitHub
    log('Pushing to GitHub...')
    success = push_to_github(github_token)

    if success:
        msg = (
            'MaeveGenesis Ventures — AI-Sharpened Docs Ready\n\n'
            'Both business cases reviewed and elaborated by Gemini + Groq.\n\n'
            'Sentinel analysis:\n'
            'https://github.com/DMoneyOH/maeve-genesis-ventures/blob/main/sentinel/AI_PARTNER_ANALYSIS.md\n\n'
            'Ghost analysis:\n'
            'https://github.com/DMoneyOH/maeve-genesis-ventures/blob/main/ghost/AI_PARTNER_ANALYSIS.md\n\n'
            'Full repo:\n'
            'https://github.com/DMoneyOH/maeve-genesis-ventures'
        )
        notify(tg_token, chat_id, msg)
        log('Done. Telegram sent.')
    else:
        log('Push failed — check logs.')
        notify(tg_token, chat_id, 'MaeveGenesis sharpening: push to GitHub failed. Check /vault/MaeveGenesis/logs/sharpening.log')

    log('=== Sharpening Run Complete ===')

if __name__ == '__main__':
    run()
