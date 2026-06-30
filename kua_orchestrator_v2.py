#!/usr/bin/env python3
import os, re, subprocess, sys, json, time
from datetime import datetime

vault = '/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault'
pending_folder = os.path.join(vault, '00-inbox/pending URLs')
extractor_path = '/Users/ashleydsouza/Documents/Coding_projects/knowledge extractor'
validator_script = os.path.join(extractor_path, 'kua_validate.py')
ke_folder = os.path.join(vault, 'knowledge-extractor')

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
            print(f'[{idx}/{len(pending_files)}] SKIP: {filename[:60]} — no URL found', flush=True)
            skipped.append((filename, 'no_url'))
            continue

        print(f'[{idx}/{len(pending_files)}] {filename[:50]}... ', end='', flush=True)

        before_files = set(os.listdir(ke_folder))

        cmd = [
            'bash', '-c',
            f'cd "{extractor_path}" && . .venv/bin/activate && python extract.py "{url}"'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)

        if result.returncode != 0 and 'Done!' not in result.stdout:
            print(f'ERROR', flush=True)
            failed.append((filename, url, 'extraction_failed'))
            continue

        after_files = set(os.listdir(ke_folder))
        new_files = after_files - before_files

        if not new_files:
            print(f'FAIL (no file created)', flush=True)
            failed.append((filename, url, 'no_output_file'))
            continue

        extracted_file = os.path.join(ke_folder, list(new_files)[0])

        validation_result = subprocess.run(
            ['python3', validator_script, extracted_file],
            capture_output=True, text=True, timeout=10
        )

        if 'SUCCESS' not in validation_result.stdout:
            print(f'INVALID', flush=True)
            reason = validation_result.stdout.split(':')[-1].strip() if ':' in validation_result.stdout else 'unknown'
            failed.append((filename, url, reason))
            continue

        os.remove(filepath)
        title = list(new_files)[0].replace('.md', '')
        succeeded.append((filename, title))
        print(f'OK', flush=True)

    except subprocess.TimeoutExpired:
        print(f'TIMEOUT', flush=True)
        failed.append((filename, url if 'url' in locals() else 'unknown', 'timeout'))
    except Exception as e:
        print(f'ERROR: {str(e)[:40]}', flush=True)
        failed.append((filename, url if 'url' in locals() else 'unknown', str(e)[:40]))

print(f'\n=== SUMMARY ===')
print(f'Succeeded: {len(succeeded)}')
print(f'Failed: {len(failed)}')
print(f'Skipped: {len(skipped)}')
print(f'\nFiles successfully processed:')
for fname, title in succeeded:
    print(f'  ✓ {title}')
if failed:
    print(f'\nFailed extractions:')
    for fname, url, reason in failed[:10]:
        print(f'  ✗ {fname[:50]} — {reason}')
    if len(failed) > 10:
        print(f'  ... and {len(failed)-10} more')
if skipped:
    print(f'\nSkipped (no URL):')
    for fname, reason in skipped:
        print(f'  → {fname[:50]}')
