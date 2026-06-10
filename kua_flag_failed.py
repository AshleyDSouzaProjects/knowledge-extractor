import os, sys, datetime

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
pending_discussions = os.path.join(vault, "pending discussions")
os.makedirs(pending_discussions, exist_ok=True)

pending_url_file = sys.argv[1]
reason = sys.argv[2]
pending_filename = sys.argv[3]

with open(pending_url_file, "r", errors="ignore") as f:
    original_content = f.read()

timestamp = datetime.datetime.now().isoformat()

lines = [
    "---",
    "tags: [kua-failure, extraction-failed, " + reason + "]",
    "date: " + timestamp,
    "status: pending-extraction",
    "---",
    "",
    "KUA EXTRACTION FAILED -- " + pending_filename,
    "",
    "**Reason:** " + reason,
    "**Date:** " + timestamp,
    "",
    "WHAT HAPPENED",
    "",
    "Extraction completed but produced no usable content.",
    "",
    "Reason codes:",
    "- api_paywall_or_error -- API paywall, HTTP 402, or similar access issue",
    "- no_valid_content -- File created but lacks valid content markers",
    "- file_too_small -- Content too minimal (< 50 chars)",
    "- file_not_created -- Extractor did not create output file",
    "",
    "NEXT STEPS",
    "",
    "1. Check if API credentials are needed (Twitter/X, LinkedIn, etc.)",
    "2. Verify URL is still accessible",
    "3. Re-run KUA once issue is resolved",
    "",
    "ORIGINAL CONTENT FROM PENDING URL",
    original_content,
    "",
    "---",
    "**Status:** Pending extraction. Original pending URL file left in place for retry.",
]

note = "\n".join(lines)
note_filename = "kua-failed-" + reason + "-" + pending_filename
note_path = os.path.join(pending_discussions, note_filename)

with open(note_path, "w") as f:
    f.write(note)

print("Flagged to pending discussions: " + note_filename)
