import os, datetime

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
today = datetime.date.today().isoformat()

routes = [
    ("/Users/ashleydsouza/Documents/Coding_projects/iSwarm", "AI/02-tools/linkedin-lyzr-shadowlm-computeragent-opengap-enterprise-ai-ownership-20260620.md", "Lyzr AI: ShadowLM, ComputerAgent, OpenGAP", "build-vs-buy / data-ownership argument relevant to iswarm GTM thesis; Ashley flagged for evaluate-and-include"),
    ("/Users/ashleydsouza/Documents/Coding_projects/iSwarm", "knowledge-extractor/twitter-imran-lmrankhan-article-before-it-was-obvious-your-20260620.md", "Before It Was Obvious: Learning from Startup Success Stories", "Ashley asked for a section in iswarm GTM about finding specific problems iswarm tools can solve -- needs follow-up, flagged to pending discussions"),
]

for proj_dir, note_rel, title, why in routes:
    vn_path = os.path.join(proj_dir, "VAULT_NOTES.md")
    note_abs = os.path.join(vault, note_rel)

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
        print("Already linked: " + title + " -> " + os.path.basename(proj_dir))
        continue

    line = "- **" + title + "** — `" + note_abs + "` — " + why + " — added " + today + "\n"
    with open(vn_path, "a") as f:
        f.write(line)
    print("Routed: " + title + " -> " + os.path.basename(proj_dir))

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
