#!/usr/bin/env python3
import os, re, subprocess, sys, json, time
from datetime import datetime

vault = '/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault'
pending_folder = os.path.join(vault, '00-inbox/pending URLs')
extractor_path = '/Users/ashleydsouza/Documents/Coding_projects/knowledge extractor'
validator_script = os.path.join(extractor_path, 'kua_validate.py')

succeeded = []
failed = []
skipped = []

pending_files = sorted([f for f in os.listdir(pending_folder) if f.endswith('.md')])

print(f'\n=== KUA Run: {datetime.now().isoformat()} ===')
print(f'Total pending files: {len(pending_files)}\n')

for idx, filename in enumerate(pending_files, 1):
    filepath = os.path.join(pending_folder, filename)

    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read()

        url = None
        if '[' in content and '](' in content:
            match = re.search(r'\]\((https?://[^\)]+)\)', content)
            if match:
                url = match.group(1)
        if not url:
            match = re.search(r'(https?://\S+)', content)
            if match:
                url = match.group(1).strip()

        if not url:
            print(f'[{idx}/{len(pending_files)}] SKIP: {filename[:60]} — no URL found')
            skipped.append((filename, 'no_url'))
            continue

        print(f'[{idx}/{len(pending_files)}] Processing: {filename[:60]}...', end='', flush=True)

        cmd = [
            'bash', '-c',
            f'cd "{extractor_path}" && . .venv/bin/activate && python extract.py "{url}"'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)

        if result.returncode != 0:
            print(f' ERROR')
            failed.append((filename, url, 'extraction_failed'))
            continue

        if 'Done!' not in result.stdout:
            print(f' FAILED')
            failed.append((filename, url, 'no_done_status'))
            continue

        extracted_file = None
        for line in result.stdout.split('\n'):
            if 'Note           :' in line:
                extracted_file = line.split(':')[-1].strip()
                break

        if not extracted_file or not os.path.exists(extracted_file):
            print(f' FAILED (no output file)')
            failed.append((filename, url, 'no_output_file'))
            continue

        validation_result = subprocess.run(
            ['python3', validator_script, extracted_file],
            capture_output=True, text=True, timeout=10
        )

        if 'SUCCESS' not in validation_result.stdout:
            print(f' INVALID')
            reason = validation_result.stdout.split(':')[-1].strip() if ':' in validation_result.stdout else 'unknown'
            failed.append((filename, url, reason))
            continue

        os.remove(filepath)
        title = extracted_file.split('/')[-1].replace('.md', '')
        succeeded.append((filename, title))
        print(f' OK')

    except subprocess.TimeoutExpired:
        print(f' TIMEOUT')
        failed.append((filename, url if 'url' in locals() else 'unknown', 'timeout'))
    except Exception as e:
        print(f' ERROR: {str(e)[:50]}')
        failed.append((filename, url if 'url' in locals() else 'unknown', str(e)[:50]))

print(f'\n=== Summary ===')
print(f'Succeeded: {len(succeeded)}')
print(f'Failed: {len(failed)}')
print(f'Skipped: {len(skipped)}')
print(f'\nSucceeded files:')
for fname, title in succeeded:
    print(f'  ✓ {fname[:50]}')
print(f'\nFailed files:')
for fname, url, reason in failed:
    print(f'  ✗ {fname[:50]} — {reason}')
if skipped:
    print(f'\nSkipped files:')
    for fname, reason in skipped:
        print(f'  → {fname[:50]} — {reason}')
