import os, sys

file_path = sys.argv[1]

if not os.path.exists(file_path):
    print("FAILED:file_not_created")
    sys.exit(0)

with open(file_path, "r", errors="ignore") as f:
    content = f.read()

if len(content.strip()) < 50:
    print("FAILED:file_too_small")
    sys.exit(0)

failure_patterns = [
    "[tweet content unavailable without api]",
    "[content unavailable without api]",
    "unable to synthesize",
    "no video found",
    "http 402",
    "payment required",
]

content_lower = content.lower()
for pattern in failure_patterns:
    if pattern in content_lower:
        print("FAILED:api_paywall_or_error")
        sys.exit(0)

success_patterns = ["## Summary", "---", "tags:", "source:"]
has_content = any(m in content for m in success_patterns)

if has_content and len(content.strip()) > 100:
    print("SUCCESS:valid_content")
else:
    print("FAILED:no_valid_content")
