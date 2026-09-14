"""KUA Step 0a — find unprocessed attachments anywhere in the vault.

Written 2026-09-03 after discovering that Step 0a only ever scanned 00-inbox/,
while Obsidian was dropping every shared image at the vault root. 68 files sat
unprocessed from 10 June to 2 September.
"""
import os, re, sys

VAULT = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"

SKIP_DIRS = {".git", ".obsidian", ".trash", "Twitter Bookmarks", "Paintings"}
EXTS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".pdf", ".docx")

# Files that are part of the toolchain rather than captures
IGNORE_NAMES = {"screenshot.png"}


def walk_vault():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            yield root, f


def main():
    attachments = []
    notes = []
    for root, f in walk_vault():
        path = os.path.join(root, f)
        if f.lower().endswith(EXTS):
            attachments.append(path)
        elif f.lower().endswith(".md"):
            notes.append(path)

    # Build the set of filenames referenced by any note.
    #
    # An embed (![[name]] / ![](name)) is the obvious case, but notes filed by
    # earlier KUA runs cite their image in a frontmatter `source:` line instead,
    # e.g.  source: "image/IMG_4651.png (LinkedIn - The Unicorn Magazine)".
    # Treating only embeds as references over-counts the backlog and would cause
    # already-processed images to be re-read and re-filed as duplicates.
    # So: any bare mention of the filename anywhere in a note counts.
    referenced = set()
    embed_re = re.compile(r"!\[\[([^\]|#]+)")
    md_re = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    all_text = []
    for n in notes:
        try:
            with open(n, errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        all_text.append(text.lower())
        for m in embed_re.findall(text) + md_re.findall(text):
            referenced.add(os.path.basename(m.strip()).lower())
    corpus = "\n".join(all_text)

    unref, ref = [], []
    for a in attachments:
        base = os.path.basename(a)
        if base.lower() in IGNORE_NAMES:
            continue
        cited = base.lower() in referenced or base.lower() in corpus
        (ref if cited else unref).append(a)

    def rel(p):
        return p.replace(VAULT + "/", "")

    unref.sort(key=lambda p: os.path.getmtime(p), reverse=True)

    print("=== UNREFERENCED ATTACHMENTS (" + str(len(unref)) + ") — awaiting processing ===")
    for p in unref:
        import datetime
        ts = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d")
        mb = os.path.getsize(p) / 1048576.0
        print("  %s  %6.1fMB  %s" % (ts, mb, rel(p)))

    print()
    print("=== REFERENCED BY A NOTE (" + str(len(ref)) + ") — leave alone ===")
    for p in ref[:20]:
        print("  " + rel(p))
    if len(ref) > 20:
        print("  ... and " + str(len(ref) - 20) + " more")

    total_mb = sum(os.path.getsize(p) for p in unref) / 1048576.0
    print()
    print("Backlog: %d files, %.0f MB" % (len(unref), total_mb))


if __name__ == "__main__":
    main()
