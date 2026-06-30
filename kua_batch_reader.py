import os, re

folder = '/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault/00-inbox/pending URLs'

pending_files = sorted([f for f in os.listdir(folder) if f.endswith('.md')])

results = []

for filename in pending_files:
    filepath = os.path.join(folder, filename)
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

        is_twitter = url and ('x.com' in url or 'twitter.com' in url) if url else False
        has_thread_marker = 'tweet thread' in content.lower()
        is_thread = is_twitter and has_thread_marker

        results.append({
            'filename': filename,
            'url': url,
            'is_twitter': is_twitter,
            'has_thread_marker': has_thread_marker,
            'is_thread': is_thread,
        })
    except Exception as e:
        results.append({
            'filename': filename,
            'url': None,
            'error': str(e),
        })

for r in results:
    if r.get('error'):
        print(f"ERROR: {r['filename']} — {r['error']}")
    else:
        marker = '[THREAD]' if r['is_thread'] else '[TWITTER]' if r['is_twitter'] else '[OTHER]'
        url_short = (r['url'][:60] + '...') if r['url'] and len(r['url']) > 60 else r['url']
        print(f"{marker} {r['filename'][:50]:<50} {url_short if url_short else 'NO URL'}")
