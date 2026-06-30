"""KUA Email Filing + Project Routing"""
import os, shutil, datetime

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
thinking = os.path.join(vault, "AI/05-my-thinking")
emails_folder = os.path.join(vault, "Emails")
today = "2026-06-28"

# ============================================================
# File the Kieran Flanagan email
# ============================================================
email_note = os.path.join(thinking, "audience-building-with-ai-kieran-flanagan.md")
content = """---
tags: [content-strategy, audience-building, ai-content, personal-brand, substack, newsletter]
source: email
author: Kieran Flanagan (The AI Marketing Generalist)
date: 2026-06-26
filed: 2026-06-28
confidence: extracted
---

# Building an Audience From Zero With AI — 8 Principles (Kieran Flanagan)

Source: Substack newsletter "The AI Marketing Generalist" — June 26, 2026

## Context
Kieran Flanagan has built an audience across Substack, YouTube, and LinkedIn. These are principles learned through years of iteration, with AI system implementations for each.

---

## CRAFT — What You Create

### Principle 1: Say Something
Authenticity is overrated. You can be authentic and create incredibly boring content. You need:
- A genuinely useful lesson
- A real point of view with great clarity
- Something with an opinion (not sitting on the fence)

"I used to feel like I failed if people argued about my ideas online, but now I know it's a sign that something I wrote was interesting."

**AI Implementation:** Post-enrichment skill — takes a draft, pattern-matches against audience, finds authoritative quotes, stories, case studies to enrich the post and bring the point to life.

### Principle 2: Be Worth Sharing
Your audience grows when OTHER people talk about your ideas, not when you talk about yourself. The goal of every piece of content: hand someone else a thought worth passing on.
- LinkedIn: repost
- Substack: restack
- YouTube: share

**AI Implementation:** AI reviewer that reads drafts from the audience's perspective. Evaluates against sharing triggers: Does this make someone look smart? Does it say what they have been thinking? Does it give a framework they can forward? Does it spark a debate worth having? Flags "portable" moments — lines someone would screenshot and send to a colleague.

### Principle 3: Use AI to Think Better, Not Write Faster
Most people use AI to create more content. Wrong instinct. Real value: understanding more.

The first thing to build is an **audience profile** (NOT a writing tool):
- Map readers pain points, motivations, language they use
- What triggers engagement vs makes them scroll past
- From that profile: build a content queue of ideas designed around what the audience cares about

"Everything starts with the reader. AI makes it easier to understand the audience and create an entire content queue for that audience."

---

## STRATEGY — How You Grow

### Principle 4: Master One Platform
What works on LinkedIn does NOT work on Substack. What works on Substack does NOT work on YouTube. Formats, hooks, structures are all diverging. Much better to master one than aimlessly cross-post.

**AI Implementation:** Build a "winning content profile" per platform:
1. Feed in top-performing posts from one platform
2. AI extracts patterns: what hooks worked, what structures drove engagement, optimal length and format
3. Use this profile as a guide when creating content for that platform
4. When ready to expand to a second platform, build a new profile for it

### Principle 5: Quality Over Quantity
A personal brand is NOT a follower count. It is an audience that cares about what you say. A small list that trusts you beats a huge feed that scrolls past you.

### Principle 6: Be Remembered, Not Viral
Stop trying to go viral. Work to be remembered. Getting obsessed with the algorithm makes you create content you do not enjoy making. Focus on memorable content you enjoy creating.

---

## MINDSET — How You Sustain It

### Principle 7: It's Hard. Accept It.
Every channel is full of content. It is hard to find repeatable motions that work. As soon as you nail a content type/format/subject, it becomes old news. There is no shortcut.

### Principle 8: Love the Grind
You have to love creating content because it is a super duper grind. You will feel like giving up. The only way through: grind, learn, grind, learn some more. One successful creator took 10 years until his YouTube channel took off. He just out-ground everyone else.

---

## Key Takeaways
1. Opinion beats authenticity — say something that can be argued with
2. Shareability is the quality metric — would someone screenshot this?
3. Audience understanding first, content second — AI helps build the profile
4. One platform mastery beats cross-posting — build per-platform winning profiles
5. Trust beats reach — small engaged list > large disengaged feed
6. Memorable beats viral — algorithm chasing destroys the fun
"""

with open(email_note, "w") as f:
    f.write(content)
print(f"Filed: AI/05-my-thinking/audience-building-with-ai-kieran-flanagan.md")

# Move the source email file to archive (keep in Emails/ — it is already in Emails/)
# The email is already in its correct location in Emails/, no move needed
# The extracted note is now in AI/05-my-thinking/

# ============================================================
# Project Routing — check for AI Jumpstart project
# ============================================================
print("\n=== PROJECT ROUTING CHECK ===")
roots = [
    "/Users/ashleydsouza/Documents/Coding_projects",
    "/Users/ashleydsouza/Documents/Coding_projects/new projects"
]
found_projects = []
for root in roots:
    if not os.path.isdir(root):
        continue
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name)
        if os.path.isdir(p) and not name.startswith("."):
            name_lower = name.lower()
            if any(kw in name_lower for kw in ["jump", "jumpstart", "jimpstart"]):
                print(f"FOUND AI Jumpstart match: {p}")
                found_projects.append(p)
            found_projects.append(p)

# Check if AI Jumpstart project exists anywhere
jumpstart_dirs = [p for p in found_projects if any(
    kw in os.path.basename(p).lower() for kw in ["jump", "jumpstart"]
)]
if jumpstart_dirs:
    print(f"AI Jumpstart project dir found: {jumpstart_dirs}")
else:
    print("AI Jumpstart project NOT FOUND in known project directories.")
    print("Notes with 'Add to project AI Jumpstart' flag:")
    flagged = [
        "AI/01-concepts/company-skills-in-version-control.md",
        "AI/01-concepts/matrix-os-agent-operating-system.md",
        "AI/02-tools/claude-skills-gtm-outbound-motion.md",
        "AI/05-my-thinking/ai-app-margins-token-awareness.md",
        "AI/06-resources/postman-passport-secure-agent-api-access.md",
        "AI/05-my-thinking/ai-organization-success-emotional-clarity.md",
        "AI/01-concepts/agentic-ai-data-layers.md",
        "AI/02-tools/12-open-source-llm-models-reference.md",
        "AI/01-concepts/6-ai-deployment-patterns-2026.md",
        "AI/01-concepts/post-agent-companies.md",
        "AI/02-tools/mineru-document-processing-tool.md",
        "pending discussions/ibm-enterprise-2030-report-pending.md",
    ]
    for f in flagged:
        print(f"  ? {f}")
    print("=> Needs clarification: which directory is 'AI Jumpstart project'?")
