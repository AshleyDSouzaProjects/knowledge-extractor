"""KUA Cleanup — delete processed pending files, create incomplete-captures, copy to pending discussions"""
import os, shutil, datetime

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
pending_urls = os.path.join(vault, "00-inbox/pending URLs")
pending_disc = os.path.join(vault, "pending discussions")
ai_concepts = os.path.join(vault, "AI/01-concepts")
ai_tools = os.path.join(vault, "AI/02-tools")
ai_thinking = os.path.join(vault, "AI/05-my-thinking")
ai_resources = os.path.join(vault, "AI/06-resources")
ai_companies = os.path.join(vault, "AI/04-companies")
os.makedirs(pending_disc, exist_ok=True)

ts = datetime.datetime.now().isoformat()
today = datetime.date.today().isoformat()

# ============================================================
# 1. Files to DELETE (successfully processed)
# ============================================================
to_delete = [
    "1 Introduction.md",
    "5 of n.md",
    "Agentic enterprise.md",
    "Creating a future-proof enterprise agentic platform architecture.md",
    "Context lake The orchestration layer for AI agents 1.md",
    "Context lake The orchestration layer for AI agents.md",
    "Context Lake.md",
    "Semantic Layers Evolving with Agentic AI.md",
    "Ai resource by google.md",
    "Attack surface for AI security.md",
    "Attack surface of AI agentic.md",
    "Interesting concept.. relevant for AI Jimpstart project.md",
    "Secure api access for agents.md",
    "Tech architecture for enterprise AI.md",
    "Alex (@de1lymoon) 47 likes · 9 replies.md",
    "Codez (@0xCodez) 5K likes · 89 replies.md",
    "DAN KOE (@thedankoe) 311K likes · 9K replies.md",
    "Mnimiy (@Mnilax) 1K likes · 27 replies.md",
    "Mnimiy (@Mnilax) 359 likes · 15 replies.md",
    "Derek Nee (@DerekNee) 381 likes · 26 replies.md",
    "Dhilip Subramanian (@sdhilip) 2K likes · 121 replies.md",
    "Aakash Gupta (@aakashgupta) 32 likes · 7 replies.md",
    "rewind (@rewind02) 739 likes · 41 replies.md",
    "Corey Ganim (@coreyganim) 100 likes · 11 replies.md",
    "darkzodchi (@zodchiii) 921 likes · 43 replies.md",
    "Jordan Ross (@jordan_ross_8F) 10 likes · 16 replies.md",
    "Justin (@jrwoodbridge) 61 likes · 4 replies.md",
    "Post ageng companies.md",
    "Rahul (@sairahul1) 120 likes · 11 replies.md",
    "Rahul (@sairahul1) 226 likes · 14 replies.md",
    "obssnnn (@0xObssnnn) 342 likes · 10 replies.md",
    "yoni rechtman (@yrechtman) 50 likes · 2 replies.md",
    "Skills needed for AI org success.md",
    "Nav Toor (@heynavtoor) 1K likes · 35 replies.md",
    "dunik (@dunik_7) 142 likes · 3 replies.md",
    "VİSA Free World (@visafreeworld) 18 likes · 1 replies.md",
    "Yann (@yanndine) 56 likes · 81 replies.md",
    "Untitled.md",
    "Setting up local AI.md",
    "Noisy (@noisyb0y1) 48 likes · 7 replies.md",
    "Noisy (@noisyb0y1) 48 likes · 7 replies 1.md",
    "Superior (@andreysuperior) 199 likes · 13 replies.md",
    "Tanner Mullen | Biz Ops (@tannerdripjobs) 420 likes · 13 replies.md",
    "Idea for 1 person business ...md",
    "Claude code best practice.md",
    "Open source.md",
    "Ai governance.md",
]

deleted = []
not_found = []
for fname in to_delete:
    fpath = os.path.join(pending_urls, fname)
    if os.path.exists(fpath):
        os.remove(fpath)
        deleted.append(fname)
    else:
        not_found.append(fname)

print(f"Deleted {len(deleted)} pending URL files")
if not_found:
    print(f"Not found (already gone or typo): {not_found}")

# ============================================================
# 2. Incomplete-capture notes for 404 / unextractable files
# ============================================================
incomplete = [
    {
        "pending_file": "Claude code projects.md",
        "note_name": "claude-code-projects-links-pending.md",
        "folder": pending_disc,
        "tags": ["incomplete-capture", "pending-discussion", "claude-code", "linkedin"],
        "source": "https://www.linkedin.com/posts/rubendominguezibar_bookma-ugcPost-7474948898065899520-WFLB/",
        "reason": "LinkedIn post 404 — post deleted or private",
        "instructions": "Pending discussion: Claude - create a project using /research to go through all these links, get the info and file for discussion once ready.",
        "action": "Re-check URL; if unavailable, search LinkedIn for Ruben Dominguez Ibar Claude Code bookmarks post.",
    },
    {
        "pending_file": "Tools for claude.md",
        "note_name": "tools-for-claude-pending.md",
        "folder": pending_disc,
        "tags": ["incomplete-capture", "pending-discussion", "claude-code", "tools", "linkedin"],
        "source": "https://www.linkedin.com/posts/rubendominguezibar_youre-using-claude-at-maybe-10-of-what-share-7476617688673611",
        "reason": "LinkedIn post 404 — post deleted or private",
        "instructions": "Pending discussion: Check how many of these tools we do and make a plan for the rest.",
        "action": "Search LinkedIn for Ruben Dominguez Ibar Claude Code tools post. Key question: which Claude capabilities are we using vs missing?",
    },
    {
        "pending_file": "the-enterprise-in-2030-report.md",
        "note_name": "ibm-enterprise-2030-report-pending.md",
        "folder": pending_disc,
        "tags": ["incomplete-capture", "pending-discussion", "ibm", "enterprise-ai", "report", "ai-jumpstart"],
        "source": "https://www-api.ibm.com/adobe/assets/urn:aaid:aem:9b35d27c-6a4d-4dcd-a804-550ea0d80cd0/original/as/the-enterprise-in-2030-report.pdf",
        "reason": "PDF binary — 5.3MB, cannot extract text via WebFetch",
        "instructions": "Claude: Download, analyse and create a detailed note. Add points to AI jump start.",
        "action": "Download PDF manually and run through pdf2md skill, or use MinerU. Then file to AI/01-concepts/ and add key points to AI Jumpstart project.",
    },
]

for item in incomplete:
    content_lines = [
        "---",
        "tags: [" + ", ".join(item["tags"]) + "]",
        "source: " + item["source"],
        "date: " + today,
        "status: incomplete-capture",
        "---",
        "",
        "# INCOMPLETE CAPTURE — " + item["note_name"].replace(".md", "").replace("-", " ").title(),
        "",
        "**Reason:** " + item["reason"],
        "**Original file:** " + item["pending_file"],
        "**Source URL:** " + item["source"],
        "",
        "## Ashley's Instructions",
        item["instructions"],
        "",
        "## Action Required",
        item["action"],
        "",
        "---",
        "*Filed by KUA on " + today + "*",
    ]
    note_path = os.path.join(item["folder"], item["note_name"])
    with open(note_path, "w") as f:
        f.write("\n".join(content_lines))
    print(f"Created incomplete-capture: {item['note_name']}")

    # Also delete the pending URL file
    pending_path = os.path.join(pending_urls, item["pending_file"])
    if os.path.exists(pending_path):
        os.remove(pending_path)
        print(f"  + Deleted pending URL file: {item['pending_file']}")

# ============================================================
# 3. Copy filed notes to pending discussions (discussion triggers)
# ============================================================
discussion_copies = [
    (os.path.join(ai_concepts, "company-skills-in-version-control.md"),
     "Aakash Gupta: check all notes related to AI Jumpstart project and create a section-wise summary."),
    (os.path.join(ai_thinking, "corey-ganim-ai-agent-niches.md"),
     "Replace c1 agent with 3 others; change project SH to focus on 2 niches. Items 1, 2, 4 worth exploring."),
    (os.path.join(ai_concepts, "local-llm-b2b-strategy.md"),
     "Pending discussion: Important to /research more. Jordan Ross local LLM guide."),
    (os.path.join(ai_tools, "hermes-agent-17-prompts.md"),
     "Pending discussion: 1 of n Hermes Agent series."),
    (os.path.join(ai_tools, "claude-code-setup-official-plugin.md"),
     "Pending discussion: 1 of m. Claude: install and evaluate claude-code-setup plugin."),
    (os.path.join(ai_thinking, "ai-agents-vs-workforce-cost-comparison.md"),
     "Pending discussion: Research the paper mentioned; add content; use to update AI Jumpstart project."),
    (os.path.join(ai_tools, "local-ai-on-mac-performance-comparison.md"),
     "Tweet thread. Compare rewind local AI setup to current system. Which framework are we using?"),
    (os.path.join(ai_concepts, "llm-wiki-second-brain-karpathy.md"),
     "Find the original Karpathy paper/post; read thoroughly; add to second brain notes; create/update LLM wiki second brain project."),
    (os.path.join(ai_resources, "postman-passport-secure-agent-api-access.md"),
     "Add to AI Jumpstart project. Pending discussion: how does this affect our agent security posture?"),
    (os.path.join(ai_concepts, "matrix-os-agent-operating-system.md"),
     "Derek Nee: Add to other pending discussions on same topic. Add to AI Jumpstart project."),
    (os.path.join(ai_tools, "mineru-document-processing-tool.md"),
     "Claude: install MinerU and understand which current projects it supersedes (particularly pdf2md)."),
    (os.path.join(ai_concepts, "pepsico-promoai-pricingai-ml-optimization.md"),
     "Instructions: go through this and create a detailed extract, focus on the what not who/why."),
]

copied = []
for src, note in discussion_copies:
    if os.path.exists(src):
        fname = os.path.basename(src)
        dst = os.path.join(pending_disc, fname)
        shutil.copy2(src, dst)
        copied.append((fname, note))
        print(f"Copied to pending discussions: {fname}")
    else:
        print(f"NOT FOUND (skipping): {src}")

print(f"\nTotal discussion copies: {len(copied)}")

# ============================================================
# Summary
# ============================================================
print("\n=== CLEANUP SUMMARY ===")
print(f"Deleted: {len(deleted)} pending URL files")
print(f"Incomplete-captures created: {len(incomplete)}")
print(f"Pending discussion copies: {len(copied)}")
remaining = os.listdir(pending_urls)
remaining_md = [f for f in remaining if f.endswith(".md")]
print(f"Remaining in pending URLs: {len(remaining_md)} files")
for f in sorted(remaining_md):
    print(f"  {f}")
