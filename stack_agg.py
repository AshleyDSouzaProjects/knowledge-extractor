"""Aggregate the stack scan into a master tool list with usage counts."""

import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "stack_scan_report.json")))

by_cat = defaultdict(lambda: defaultdict(list))
for p in data:
    for cat, hits in p["mentions"].items():
        for h in hits:
            by_cat[cat][h].append(p["name"])

lines = ["# Master tool index — " + str(len(data)) + " projects scanned", ""]
for cat in sorted(by_cat):
    lines.append("## " + cat)
    items = sorted(by_cat[cat].items(), key=lambda kv: (-len(kv[1]), kv[0]))
    for tool, projs in items:
        lines.append("- **" + tool + "** (" + str(len(projs)) + "): " + ", ".join(sorted(projs)))
    lines.append("")

# env keys across the machine
env = defaultdict(list)
for p in data:
    for k in p["env_keys"]:
        env[k].append(p["name"])
lines.append("## ENV KEY NAMES (names only, no values)")
for k, projs in sorted(env.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    lines.append("- `" + k + "` (" + str(len(projs)) + "): " + ", ".join(sorted(projs)))
lines.append("")

# size / activity table
lines.append("## Projects by size")
for p in sorted(data, key=lambda x: -x["bytes"]):
    lines.append("- " + p["name"] + " — " + str(round(p["bytes"] / 1_000_000, 1))
                 + " MB, " + str(p["files"]) + " files, modified " + str(p["last_modified"])
                 + (", manifests: " + ",".join(p["manifests"]) if p["manifests"] else ", no manifest"))

out = os.path.join(HERE, "stack_master_index.md")
with open(out, "w") as f:
    f.write("\n".join(lines))
print("wrote stack_master_index.md (" + str(len("\n".join(lines))) + " chars)")

tools = sum(len(v) for v in by_cat.values())
print("distinct tools/services matched: " + str(tools))
print("distinct env key names: " + str(len(env)))
