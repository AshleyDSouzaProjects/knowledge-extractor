import os, datetime

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
proj_dir = "/Users/ashleydsouza/Documents/Coding_projects/codex/AI jumpstart"
today = datetime.date.today().isoformat()

note_abs = os.path.join(vault, "AI/01-concepts/ai-transformation-7p-model-and-enterprise-ai-coe-20260620.md")
title = "AI Transformation 7P Model + Enterprise AI CoE"
why = "two enterprise-AI-adoption framework infographics, explicitly flagged relevant for AI jumpstart"

vn_path = os.path.join(proj_dir, "VAULT_NOTES.md")

if not os.path.exists(vn_path):
    header = [
        "# Vault Notes — relevant captures for " + os.path.basename(proj_dir),
        "",
        "Auto-maintained by `/kua`. Pointers to notes in the Obsidian vault relevant to this project.",
        "The notes live in the vault (single source of truth); these are links, not copies.",
        "",
    ]
    with open(vn_path, "w") as f:
        f.write("\n".join(header))

with open(vn_path, "r", errors="ignore") as f:
    existing = f.read()

if note_abs in existing:
    print("Already linked")
else:
    line = "- **" + title + "** — `" + note_abs + "` — " + why + " — added " + today + "\n"
    with open(vn_path, "a") as f:
        f.write(line)
    print("Routed: " + title)

claude_md = os.path.join(proj_dir, "CLAUDE.md")
ref_line = "> Relevant captured notes from the Obsidian vault: see [VAULT_NOTES.md](VAULT_NOTES.md)."
if os.path.exists(claude_md):
    with open(claude_md, "r", errors="ignore") as f:
        cm = f.read()
    if "VAULT_NOTES.md" not in cm:
        with open(claude_md, "a") as f:
            f.write("\n\n" + ref_line + "\n")
        print("  + added CLAUDE.md ref")
else:
    with open(claude_md, "w") as f:
        f.write(ref_line + "\n")
    print("  + created CLAUDE.md with ref")
