#!/usr/bin/env python3
"""Fix sharpen.py: swap to Groq-first, Gemini optional."""
import py_compile, sys

path = '/home/derek/vault/MaeveGenesis/ventures/sharpen.py'
with open(path) as f:
    lines = f.readlines()

out = []
i = 0
while i < len(lines):
    if '# Get Gemini analysis' in lines[i]:
        # Inject Groq-first block
        out += [
            "    # Groq first (hourly reset, reliable)\n",
            "    groq_analysis = None\n",
            "    if groq_key:\n",
            "        log(f'{product}: Calling Groq...')\n",
            "        try:\n",
            "            groq_analysis = call_groq(groq_key, prompt)\n",
            "            log(f'{product}: Groq done ({len(groq_analysis)} chars)')\n",
            "        except Exception as e:\n",
            "            log(f'{product}: Groq failed - {e}')\n",
            "\n",
            "    time.sleep(10)\n",
            "\n",
            "    # Gemini optional - daily quota may be exhausted\n",
            "    gemini_analysis = None\n",
            "    try:\n",
            "        log(f'{product}: Calling Gemini (optional)...')\n",
            "        gemini_analysis = call_gemini(gemini_key, prompt, retries=2)\n",
            "        log(f'{product}: Gemini done ({len(gemini_analysis)} chars)')\n",
            "    except Exception as e:\n",
            "        log(f'{product}: Gemini skipped - {e}')\n",
            "\n",
            "    if not groq_analysis and not gemini_analysis:\n",
            "        raise RuntimeError('Both AI partners failed')\n",
        ]
        # Skip original lines until appendix write
        while i < len(lines) and '# Write AI analysis appendix' not in lines[i]:
            i += 1
        # Inject corrected appendix block
        out += [
            "    # Write AI analysis appendix\n",
            "    appendix_path = doc_path.replace('BUSINESS_CASE.md', 'AI_PARTNER_ANALYSIS.md')\n",
            "    with open(appendix_path, 'w') as f:\n",
            "        f.write(f'# {product} - AI Partner Analysis\\n')\n",
            "        f.write(f'*Generated: {datetime.now().isoformat()}*\\n\\n')\n",
            "        f.write('---\\n\\n')\n",
            "        if groq_analysis:\n",
            "            f.write('## Groq (Llama 3.3 70B) Analysis\\n\\n')\n",
            "            f.write(groq_analysis)\n",
            "        if gemini_analysis:\n",
            "            f.write('\\n\\n---\\n\\n## Gemini Analysis\\n\\n')\n",
            "            f.write(gemini_analysis)\n",
        ]
        # Skip original appendix block until analysis written log line
        while i < len(lines) and "Analysis written to" not in lines[i]:
            i += 1
    else:
        out.append(lines[i])
    i += 1

with open(path, 'w') as f:
    f.writelines(out)

try:
    py_compile.compile(path, doraise=True)
    print('PATCHED + SYNTAX OK')
except py_compile.PyCompileError as e:
    print(f'SYNTAX ERROR: {e}')
    sys.exit(1)
