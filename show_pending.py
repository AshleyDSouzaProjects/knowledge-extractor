import os

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
pending_dir = os.path.join(vault, "pending discussions")

print("=== Pending Discussions ===\n")

files = sorted(os.listdir(pending_dir)) if os.path.exists(pending_dir) else []
md_files = [f for f in files if f.endswith(".md")]

if not md_files:
    print("No pending discussions found.")
else:
    for i, fname in enumerate(md_files, 1):
        path = os.path.join(pending_dir, fname)
        try:
            with open(path, "r", errors="ignore") as fh:
                content = fh.read()
            lines = content.strip().split("\n")
            title = fname.replace(".md", "")
            for line in lines:
                if line.startswith("title:"):
                    title = line.replace("title:", "").strip().strip('"')
                    break
            print(f"{i}. {title}")
            print(f"   File: {fname}")
        except Exception as e:
            print(f"{i}. {fname} (error: {e})")
        print()

    print(f"Total: {len(md_files)} items")
