#!/usr/bin/env python3
import sys, subprocess, requests, sqlite3
sys.path.insert(0,'/home/derek/vault/utils/core-skills')
from brain import get_secret

token = get_secret('GITHUB_TOKEN')
tg_token = get_secret('TELEGRAM_BOT_TOKEN')
chat_id = get_secret('TELEGRAM_CHAT_ID')

VENTURES = '/home/derek/vault/MaeveGenesis/ventures'
REPO = 'DMoneyOH/maeve-genesis-ventures'
remote = f'https://{token}@github.com/{REPO}.git'

cmds = [
    f'cd {VENTURES} && git init -b main',
    f'cd {VENTURES} && git config user.email derekepperson@gmail.com',
    f'cd {VENTURES} && git config user.name "Maeve"',
    f'cd {VENTURES} && git remote remove origin 2>/dev/null; git remote add origin {remote}',
    f'cd {VENTURES} && git add -A',
    f'cd {VENTURES} && git commit -m "MaeveGenesis ventures: Sentinel + Ghost business cases 2026-04-28"',
    f'cd {VENTURES} && git push origin main --force',
]

for cmd in cmds:
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    safe = cmd.replace(token,'***')[:65]
    if r.returncode != 0 and 'nothing to commit' not in (r.stdout+r.stderr):
        print(f'FAIL [{r.returncode}] {safe}')
        print((r.stdout+r.stderr)[-200:])
        sys.exit(1)
    else:
        print(f'OK: {safe}')

print('PUSH COMPLETE')

msg = (
    "MaeveGenesis Ventures — Documentation Ready\n\n"
    "Two business cases prepared for your review:\n\n"
    "1. SENTINEL — Intelligent change monitoring\n"
    "   $12-35/mo subscriptions | Target: $1,600 MRR by day 90\n\n"
    "2. GHOST — Autonomous LinkedIn ghostwriting\n"
    "   $149-299/mo retainers | Target: $2,985 MRR by day 90\n\n"
    "ProfEdgeAI: Archived\n\n"
    "Full documentation:\n"
    "https://github.com/DMoneyOH/maeve-genesis-ventures\n\n"
    "Sentinel: https://github.com/DMoneyOH/maeve-genesis-ventures/blob/main/sentinel/BUSINESS_CASE.md\n\n"
    "Ghost: https://github.com/DMoneyOH/maeve-genesis-ventures/blob/main/ghost/BUSINESS_CASE.md\n\n"
    "Ready to build on your go-ahead."
)
r = requests.post(f'https://api.telegram.org/bot{tg_token}/sendMessage',
    json={'chat_id': chat_id, 'text': msg}, timeout=10)
print(f'Telegram: {r.status_code}')
