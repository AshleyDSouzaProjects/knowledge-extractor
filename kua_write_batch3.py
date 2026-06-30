"""KUA Batch 3 — Write AI/05-my-thinking/ + Travel/ notes"""
import os

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
thinking = os.path.join(vault, "AI/05-my-thinking")
travel = os.path.join(vault, "Travel")
tools = os.path.join(vault, "AI/02-tools")
for d in [thinking, travel, tools]:
    os.makedirs(d, exist_ok=True)

notes = {}

notes[os.path.join(thinking, "ai-app-margins-token-awareness.md")] = """---
tags: [ai-strategy, margins, token-economics, infrastructure, ai-jumpstart, relevant-for-project]
source: https://www.linkedin.com/posts/dthakker_battery-ventures-dirt-to-tokens-series-why-share-7473793868359041024-ET2w/
author: Dharmesh Thakker (Battery Ventures)
date: 2026-06-28
confidence: extracted
relevant-for-project: AI Jumpstart
---

# AI App Margins — Token Awareness and Infrastructure Choices

## Core Argument
Being token-aware is key to driving margins. Unlike previous SaaS leaders (Salesforce, Workday) that maintained 70-80% margins on cloud, today's AI apps face inverted economics from API costs.

## The Margin Problem
API costs from frontier models (like Opus), AWS hosting, and Nvidia infrastructure create compressed margins that undermine profitability at scale.

## Strategic Paths to Better Margins
Companies with credible migration strategies toward these will maintain healthier margins:
- Open-weight models
- Smaller language models
- Self-hosted inference infrastructure
- Alternative chips (TPUs, SambaNova)

## Competing Examples
- **Cursor**: Using open-weight foundations → healthier margin model
- **Claude Code**: End-to-end closed platform → different margin structure

## Required Expertise
"Founders and investors will need fluency across the full stack to succeed in this era."

## Discussion Insight
Token efficiency requires optimizing workflow design, data quality, and multi-agent architecture — not just sourcing cheaper tokens.

## Relevance to AI Jumpstart
Directly relevant — infrastructure decisions made now determine long-term margin structure. Consider token awareness as a first-class design constraint.
"""

notes[os.path.join(thinking, "corey-ganim-ai-agent-niches.md")] = """---
tags: [ai-agents, business-model, niches, one-person-business, pending-discussion, ai-jumpstart]
source: https://x.com/coreyganim/status/2068090194662699234
author: Corey Ganim (@coreyganim)
date: 2026-06-28
confidence: extracted
status: pending-discussion
---

# AI Agent Niche Specialization — 5 Business Examples (Corey Ganim)

## Core Strategy
"I install one AI worker into one workflow that is currently costing you money."

Successful AI agent vendors target one specific workflow problem within a single niche. Not multiple agents, not broad platforms — one workflow, one niche.

## 5 Industry Examples with Revenue Models

1. **Roofers** — Missed-call management and lead intake automation
   - Revenue: $3K setup + monthly maintenance

2. **Med Spas** — Consultation qualification and follow-up reminders
   - Revenue: setup + monthly

3. **Agencies** — Automated weekly client reporting
   - Revenue: per-client or retainer

4. **Ecommerce** — Support ticket triage and response drafting
   - Revenue: volume-based or retainer

5. **Realtors** — Lead research with personalized follow-up
   - Revenue: per-lead or monthly

## Business Model
- Solve one existing pain point causing financial loss
- Charge setup fee + ongoing maintenance
- Continuously improve the single solution
- Replicate across similar clients in the same niche

## Ashley's Notes on This
1, 2, 4 are worth exploring. Consider: replace c1 agent with 3 others and change project SH to focus on these 2 niches.

## Status
Pending discussion with Claude. See Claude code projects.md for related discussion.
"""

notes[os.path.join(thinking, "claude-agents-as-a-service-20k-month.md")] = """---
tags: [ai-agents, business-model, saas, one-person-business, new-project-idea]
source: https://x.com/andreysuperior/status/2059992370414796888
author: Superior (@andreysuperior)
date: 2026-06-28
confidence: extracted
status: potential-new-project
---

# Claude Agents as a Service — $20K/Month Business Model

## The Model
Managed Claude agents offered as a service to small businesses at $20,000/month. Automates operations that currently cost more in headcount.

## Case Study
A marketing agency in Austin:
- Previous: 6-person operations team ($28,000/month)
- Functions: lead qualification, customer support, invoicing, reporting, competitor monitoring
- After: Claude agents service at $20,000/month
- Client savings: $8,000/month while the service provider keeps the difference

## Economics
- Provider cost: mainly Claude API + setup time + oversight
- Client value: replaces headcount at lower cost with better consistency
- Margin: potentially very high once the agent system is built

## Action Item
Add to potential new projects list. Evaluate fit with existing skills and current project roster.
"""

notes[os.path.join(thinking, "hormozi-principles-content-business.md")] = """---
tags: [business, content, marketing, hormozi, one-person-business]
source: https://x.com/tannerdripjobs/status/2070539541501399464
via: Tanner Mullen (@tannerdripjobs) summarizing Alex Hormozi
date: 2026-06-28
confidence: extracted
---

# Alex Hormozi — 10 Business Principles (Tanner Mullen Summary)

## Source
Tanner Mullen's 3-hour Hormozi session takeaways.

## 10 Principles

1. **Hooks are everything** — Spend 80% of energy on hooks. The hook determines whether anyone sees the rest.

2. **Remind, don't teach** — People need to be reminded more than taught new things. Repackage best content repeatedly — more effective than constant novelty.

3. **More → Better → New** (Sequencing)
   - When starting: volume is almost always the answer
   - People ahead of you aren't doing 2-3x your volume — often 100x
   - "Volume negates luck"
   - Only optimize for Better once you have flow
   - Try New only when nothing is working

4. **LTV:CAC is the only metric** — Lifetime gross profit (not revenue) divided by all-in acquisition cost. Minimum 3:1. Biggest money comes from 30:1 to 200:1 ratios. When you find one, dump in as much cash as possible.

5. **Only 4 ways to advertise** — Warm outreach, cold outreach, content, paid ads (1-to-1 or 1-to-many × known or stranger). Most owners spend zero hours/day on these. Spend first ~4 hours promoting.

6. **Track everything** — If you don't track, you don't care. Measurement itself improves results. Track outcomes to substantiate claims.

7. **Say/show what only you can** — "Do epic stuff, then talk about what you did." How-I, not how-to.

8. **Give away secrets, sell implementation** — Free content quality builds reputation. Revenue comes from helping execute.

9. **All advertising works** — It is about efficiency, not channel.

10. **State facts, tell truth** — Substantiated claims outperform unsubstantiated assertions.
"""

notes[os.path.join(thinking, "fitness-content-supplier-business-model.md")] = """---
tags: [one-person-business, content-business, ai-content, fitness, business-model, new-project-idea]
source: https://x.com/rrichprmr/status/2070508630785335763
author: Rich (@RrichPRMR)
date: 2026-06-28
confidence: extracted
---

# 1-Person Fitness Content Business — $21K/Month Model

## The Concept
Become a content SUPPLIER, not an influencer. Film workout videos, sell the raw content to fitness brands. AI handles all production.

## How It Works
1. Film authentic workout footage using phone + bench
2. Sell raw footage to multiple brands (activewear, supplement companies)
3. AI repurposes footage: editing into 20+ reels, captions in brand voice, scheduling, reports
4. Each brand gets exclusive content rights for their category

## Economics
- Provider cost: ~$40/month (phone + equipment already owned)
- Revenue: ~$4,200 per brand × 5 brands = $21,000/month
- Works regardless of personal follower count

## Why It Works
- Brands need authentic content that feels real, not polished ads
- AI handles the production work brands would otherwise pay editors for
- Supplier model scales (add more brands, same filming effort)

## Add to List
Add this to the list of 1-person business models. See also: [[corey-ganim-ai-agent-niches]], [[claude-agents-as-a-service-20k-month]]
"""

notes[os.path.join(thinking, "ai-agents-vs-workforce-cost-comparison.md")] = """---
tags: [ai-agents, workforce, cost-comparison, future-of-work]
source: https://x.com/noisyb0y1/status/2070889751192985690
author: Noisy (@noisyb0y1)
date: 2026-06-28
confidence: extracted
note: claim that Anthropic reduced workforce by 40% is likely misinformation/clickbait — do not repeat
---

# AI Agents vs Human Workforce — Cost Comparison Claim

## The Claim (verify before sharing)
"Instead of paying four employees $24,000 every month, I now have a single AI agent doing the entire job for just $20."

Note: The tweet also claims "Anthropic reportedly reduced its workforce by 40%" — this appears to be inaccurate/clickbait. Do not cite this statistic.

## The Pattern Being Described
Companies no longer scale by hiring more people. They scale by deploying AI agents that work 24/7.

AI is not just a tool — it is becoming an entire workforce. The future is not one AI assistant; it is a complete digital organization.

## What Changed For This Person
The post claims a personal workflow transformation after reading a specific document (not named, just called "one document").

## Takeaway
The specific dollar comparison ($24,000 employees → $20 AI) is a rhetorical claim, not a verified case study. The directional point (AI agents dramatically reduce operational costs) aligns with other content in this vault.

## Context
This was captured as "1 of q" and "2 of q" — both files reference the same tweet URL.
"""

notes[os.path.join(thinking, "ai-organization-success-emotional-clarity.md")] = """---
tags: [ai-strategy, future-of-work, emotional-intelligence, ai-org, leadership]
source: https://x.com/lennysan/status/2069467946540580921
author: Lenny Rachitsky sharing Joe Hudson
date: 2026-06-28
confidence: extracted
---

# AI Organization Success — Emotional Clarity Over Knowledge

## Context
Joe Hudson coaches research teams at OpenAI, alongside leadership from Apple and Google.

Shared by Lenny Rachitsky (@lennysan).

## Core Insight
The key differentiator in AI-forward environments is "emotional clarity" — not greater knowledge or increased effort, since AI excels at both.

## What Emotional Clarity Means
- Remaining engaged during difficult conversations
- Avoiding self-blame and blame toward others during challenges
- Persisting through setbacks

## Why It Matters More Now
Traditional advantages (more knowledge, more effort) are less relevant because AI handles those. The humans who succeed are those who can navigate the psychological complexity of working with and through AI systems.

## The Wisdom Stack
A framework Hudson calls a competitive advantage — the organizational capability to process and move through fear as a team ("Fear Metabolism").

## Implication for Teams Building AI Products
Technical skill and prompt engineering are necessary but not sufficient. The teams that win will be those with better psychological infrastructure.

## Relevance to AI Jumpstart
Add to AI Jumpstart project — relevant to team design and organizational culture.
"""

# Travel
notes[os.path.join(travel, "switzerland-budget-travel-guide.md")] = """---
tags: [travel, switzerland, budget-travel, alps]
source: https://x.com/visafreeworld/status/2070967648033116221
author: VİSA Free World (@visafreeworld)
date: 2026-06-28
confidence: partial
retrieval: Full guide is in a video (8:28) — only text preview captured. Visit original URL for complete blueprint.
---

# Switzerland Budget Travel — Alpine Adventure Without Breaking the Bank

## Claim
"Switzerland is only for the rich" is one of the biggest myths on the internet.

## What the Guide Covers
An 8-minute video guide titled "the ultimate, comprehensive blueprint to exploring the Alps on a budget."

## Status: Partial Capture
The specific tips and strategies are in the linked video, not the tweet text. Visit the original URL for the full blueprint.

## Source
x.com/visafreeworld — @visafreeworld travel account
"""

# Dan Koe note (philosophy/thinking)
notes_philosophy = {}
philosophy = os.path.join(vault, "AI/05-my-thinking")

notes_philosophy[os.path.join(philosophy, "fix-your-life-in-1-day-dan-koe.md")] = """---
tags: [productivity, mindset, life-design, dan-koe]
source: https://x.com/thedankoe/status/2010751592346030461
author: DAN KOE (@thedankoe)
date: 2026-06-28
confidence: partial
retrieval: Full article at linked URL. Tweet preview only captured.
engagement: 204.5M views, 8.9K replies, 50K retweets, 320K likes, 834K bookmarks
---

# How to Fix Your Entire Life in 1 Day — Dan Koe

## Premise
Most people go about changing their lives in the completely wrong way, particularly with New Year's resolutions.

## Status: Partial Capture
The full article is at the linked URL. Only the introduction was captured via tweet preview.

The massive engagement (204M views, 320K likes) suggests this is one of Koe's most resonant pieces.

## Action Item
Read the full article. Instructions say to make the note extensive once full content is available.
"""

all_notes = {**notes, **notes_philosophy}

for fpath, content in all_notes.items():
    with open(fpath, "w") as f:
        f.write(content)
    fname = os.path.basename(fpath)
    folder = os.path.basename(os.path.dirname(fpath))
    print(f"Written: {folder}/{fname}")

print(f"\nTotal: {len(all_notes)} notes written")
