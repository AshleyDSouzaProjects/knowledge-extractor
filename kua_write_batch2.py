"""KUA Batch 2 — Write remaining concepts + AI/02-tools/ + AI/04-companies/ notes"""
import os

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
concepts = os.path.join(vault, "AI/01-concepts")
tools = os.path.join(vault, "AI/02-tools")
companies = os.path.join(vault, "AI/04-companies")
resources = os.path.join(vault, "AI/06-resources")
for d in [concepts, tools, companies, resources]:
    os.makedirs(d, exist_ok=True)

notes = {}

# ==================== AI/01-concepts ====================

notes[os.path.join(concepts, "post-agent-companies.md")] = """---
tags: [agentic-ai, future-of-work, ai-strategy, business-model, ai-jumpstart]
source: https://x.com/jrwoodbridge/status/2067985204958880038
authors: [Justin (@jrwoodbridge), Yoni Rechtman (@yrechtman), Michael Bloch (@michaelxbloch)]
date: 2026-06-28
confidence: extracted
---

# Post-Agent Companies

## Summary
A co-authored piece by Justin Woodbridge and Yoni Rechtman examining what companies look like in a world where AI agents can execute most cognitive work. Widely shared; multiple perspectives captured below.

## Core Thesis (Michael Bloch framing)
"The mid-game is selling AI labor at human-labor prices. The end-game is using that labor to build the network, context, and trust that become the real company."

AI labor monetization is an intermediate strategy — the real competitive moat comes from relationships, contextual understanding, and trust built while deploying that labor.

## Key Observation
"Everything feels astroturfed. Last week we were token-maxxing. Now we are token-minning." — The AI landscape shifts rapidly; durable companies need to build something beyond the current model moment.

## Implications
- Companies that survive the agentic transition will be those that used AI labor to build network effects, not just to cut costs
- The current window of selling AI labor at human prices is temporary — prices will compress
- What matters long-term: the proprietary context, relationships, and trust accumulated during this window

## Relevance to AI Jumpstart
Add to AI Jumpstart project — directly relevant to positioning and strategy.
"""

notes[os.path.join(concepts, "local-llm-b2b-strategy.md")] = """---
tags: [local-llm, ai-infrastructure, b2b, cost-optimization, ai-hardware]
source: https://x.com/jordan_ross_8f/status/2067864896050430288
author: Jordan Ross (@jordan_ross_8F)
date: 2026-06-28
confidence: extracted
---

# Local LLM B2B Strategy — Preparing for Token Price Surge

## Thesis
Token prices are going to increase sharply. Running local LLMs for a B2B business will be a massive price advantage when the change happens.

## Why Local LLMs Will Matter
- API costs from frontier models create compressed margins for AI apps
- Companies relying on external APIs become exposed to price increases
- Local deployment removes the per-token cost entirely

## Practical Toolkit
Jordan Ross published a 17-page how-to guide covering:
- What hardware to buy
- What technology to run
- 8 steps to begin getting agents running locally

Targeted at non-technical founders wanting to get started.

## Connection
See also: [[asus-nuc-16-pro-local-ai-cluster]], [[local-ai-devices-vs-subscriptions]], [[local-ai-on-mac-performance-comparison]]

## Related Insight
The infrastructure decision made now determines margin structure later. Founding teams and investors need fluency across the full stack.
"""

notes[os.path.join(concepts, "llm-wiki-second-brain-karpathy.md")] = """---
tags: [second-brain, knowledge-management, obsidian, llm, karpathy, self-improving-systems]
source: https://x.com/0xobssnnn/status/2070683754025177238
author: Andrej Karpathy (via obssnnn/@0xObssnnn)
date: 2026-06-28
confidence: extracted
---

# LLM Wiki Second Brain — Karpathy's 9 Rules for Self-Maintaining Knowledge Base

## Summary
Andrej Karpathy published 9 rules for a self-maintaining knowledge base using Claude and Obsidian, organized in 3 layers with distinct ownership. Contrasts with traditional RAG.

## Core Architecture
**3 layers with distinct ownership:**
- **Raw layer** — Unedited by the user; raw captures stay authentic
- **Wiki layer** — Managed by the model; compiled, interconnected pages
- **Schema file** — Single file governing both layers

## Key Distinction: LLM Wiki vs RAG
- **RAG**: Re-derives answers per query from raw sources
- **LLM Wiki**: Compiles sources once into interconnected pages that compound over time

Starting with 10 sources allows for neighbor updates across the knowledge graph.

## The Compounding Effect
The system transforms a basic folder into an augmented thinking tool. Knowledge compounds as the wiki layer grows — unlike RAG which starts fresh each query.

## Highly Relevant to Ashley's System
This vault IS an implementation of this concept. Key questions:
- Is the "wiki layer" (compiled knowledge in AI/ folders) being maintained separately from raw captures?
- Is the schema consistent across all notes?

## Action Items
- Research the original paper/post mentioned
- Consider creating a project for LLM Wiki Second Brain
- Cross-reference with existing second brain notes in this vault
"""

notes[os.path.join(concepts, "langchain-4-loop-framework.md")] = """---
tags: [ai-agents, loops, prompt-engineering, langchain, automation]
source: https://x.com/dunik_7/status/2069079047510864322
author: dunik (@dunik_7)
date: 2026-06-28
confidence: extracted
---

# LangChain 4-Loop Framework — Moving Beyond Manual Prompt Engineering

## Summary
Article: "The 4 loops that quietly killed prompt engineering." LangChain introduced a 4-loop playbook for optimization. Most people still use manual prompt entry methods.

## Core Insight
1% better every night compounds to 37x better in a year (1.01^365 = 37.8).

The shift is from manually crafting individual prompts to building loops that continuously improve agent performance.

## Why Prompt Engineering Is Dying
- Manual prompt iteration is slow and doesn't scale
- Loops automate the improvement cycle
- The delta compounds dramatically over time

## Connection
Pairs with: [[loop-engineering-prompter-to-loop-designer]], [[ai-agent-self-improvement-loops]]
"""

notes[os.path.join(concepts, "retail-agentic-ai-architecture.md")] = """---
tags: [ai-architecture, retail-ai, enterprise-ai, agentic-ai, multi-agent]
source: https://www.linkedin.com/posts/arghya-mukherjee-11b34543_agenticai-retailai-enterpriseai-share-7475600026149249024-vHBr/
author: Arghya Mukherjee
date: 2026-06-28
confidence: extracted
---

# Agentic AI Architecture for Enterprise Retail

## Core Thesis
Agentic AI in retail is not "an LLM + RAG chatbot" but a governed operating system converting retail signals into controlled business actions.

## Key Architectural Components

1. **API & Identity Layer** — Authentication, tenant isolation, access controls, audit trails
2. **Agent Control Plane** — Coordinates LLM gateway, policy engine, orchestrator, memory, task scheduling
3. **Specialist Retail Agents** — Domain-specific agents for inventory, replenishment, pricing, promotions, supplier management, finance, store operations
4. **Tool & Data Gateway** — Controlled access to ERP, POS, WMS, CRM systems and forecasting models
5. **Model-Serving** — Routing, autoscaling, caching, latency, cost optimization
6. **Guardrails & Observability** — Applied across prompts, tool calls, recommendations, and business actions

## Practical Example: Stockout Prediction
Agents coordinate to recommend 840-unit replenishment with evidence-backed reasoning and pending approval mechanisms.

## Critical Design Questions
- Centralized vs event-driven orchestration
- Policy enforcement placement (planning, tool-calls, action stages)
- Memory architecture (domain-owned vs shared semantic layer)
- Risk stratification (autonomous vs human-approved actions)
- Journey-first vs platform-primitives-first implementation
"""

notes[os.path.join(concepts, "pepsico-promoai-pricingai-ml-optimization.md")] = """---
tags: [enterprise-ml, optimization, pepsico, pricing, promotions, operations-research]
source: https://arxiv.org/html/2606.17941
authors: [Aleix Llenas, Eduardo Salazar-Treviño, Francisco Leskovar et al.]
journal: INFORMS Journal on Applied Analytics
date: 2026-06-28
confidence: extracted
instructions: focus on the what not who or why — all relevant facts and salient info gathered
---

# PepsiCo PromoAI + PricingAI — Enterprise ML Optimization at Scale

## Summary
Two large-scale optimization systems developed at PepsiCo for revenue management: PromoAI (promotional calendar optimization) and PricingAI (base pricing strategy). Demonstrates feasibility of advanced optimization in enterprise environments at $90B+ annual revenue scale.

## PromoAI — Promotional Calendar Optimization

**Problem**: Constructing optimal promotional calendars subject to operational constraints.
- Retailers have limited promotional capacity (slotting constraints)
- Must determine optimal timing, depth, and mechanics for hundreds of Product Promotion Groups (PPGs)
- Must respect exclusivity rules, minimum spacing requirements, seasonal alignment

**Method**: ML-based promotional forecasts + Mixed-Integer Linear Programming (MILP)
- ML forecasts predict sales uplift for different promotional scenarios
- MILP optimizes calendar construction across trade channels
- Integrated with planner workflows for human oversight

## PricingAI — Base Pricing Strategy

**Problem**: Setting base prices across product portfolios and geographies

**Method**: Bayesian hierarchical models for elasticity estimation + Nonlinear Programming (NLP)
- Bayesian hierarchical models estimate price elasticities with appropriate uncertainty
- Nonlinear programming optimizes prices subject to business constraints
- Cross-product cannibalization effects modeled

## Key Technical Components
- **ML Forecasting**: Promotional uplift prediction
- **MILP**: Mixed-integer linear programming for calendar optimization
- **Bayesian Hierarchical Models**: Price elasticity estimation across SKUs and markets
- **NLP**: Nonlinear programming for price optimization

## Scale
PepsiCo operates across numerous geographies and retail channels. Annual revenues exceeding $90 billion.

## Significance
Demonstrates that enterprise-scale revenue management can be automated using ML + mathematical programming while maintaining human planner oversight. Published in INFORMS Journal on Applied Analytics (peer-reviewed).
"""

# ==================== AI/02-tools ====================

notes[os.path.join(tools, "mineru-document-processing-tool.md")] = """---
tags: [tools, ocr, pdf, document-processing, open-source, local-ai]
source: https://x.com/heynavtoor/status/2069773963413340297
author: Nav Toor (@heynavtoor)
date: 2026-06-28
confidence: extracted
---

# MinerU — Free Open Source Document Processing Tool

## Summary
MinerU reads any PDF, Word doc, PowerPoint, Excel sheet, or scanned image. Extracts text in reading order, converts tables to HTML, recognizes equations as LaTeX, handles scanned documents with OCR in 109 languages.

## Three Usage Methods
1. **CLI** — One command per document
2. **Python SDK** — Five lines of code integration
3. **Web app** — mineru.net (no installation required)

## What It Does
- Extracts text preserving reading order
- Converts tables to structured HTML
- Recognizes math equations as LaTeX
- OCR for scanned documents (109 languages)
- Handles PDFs, Word, PowerPoint, Excel, images

## Integrations
Works with: Claude Desktop, Cursor, Windsurf, LangChain, LlamaIndex, and other platforms.

## License
Free for personal and commercial use — Apache 2.0-based (MinerU Open Source License). Runs locally, keeps documents on your machine.

## Performance Comparison
- Contract processing: 4 minutes vs one week manually
- Invoice processing: 12 minutes vs four days manually
- Research papers: an afternoon vs two weeks manually

## Web App
mineru.net — upload, process, download (no installation required)

## Action Item
Install and test MinerU; evaluate which current projects it could supersede (particularly pdf2md).
"""

notes[os.path.join(tools, "fluid-voice-local-dictation-mac.md")] = """---
tags: [tools, voice-dictation, local-ai, mac, productivity]
source: https://x.com/sdhilip/status/2069140867466797200
author: Dhilip Subramanian (@sdhilip)
date: 2026-06-28
confidence: extracted
---

# FluidVoice — Local Voice Dictation on Mac (vs Wispr Flow)

## Summary
After 6 months and 44,414 words with Wispr Flow (top 0.1% of users, 161 wpm), Dhilip switched to FluidVoice — an open source local Mac app.

## FluidVoice Key Features
- Open source
- Runs local on Mac — no API key needed
- Corrects as you speak
- Handles slang better than expected
- Free vs Wispr Flow's paid subscription

## Get It
altic.dev/fluid

## Verdict
Cancelled Wispr Flow paid plan after finding FluidVoice. Recommended for Mac users.
"""

notes[os.path.join(tools, "claude-code-hooks-enforcement.md")] = """---
tags: [claude-code, hooks, best-practice, tools, ai-coding]
source: https://x.com/sairahul1/status/2069710540654645550
author: Rahul (@sairahul1)
date: 2026-06-28
confidence: extracted
---

# Claude Code Hooks — Making CLAUDE.md Instructions Actually Stick

## Summary
CLAUDE.md tells Claude how to behave. Hooks make Claude actually follow those instructions. Most people use only CLAUDE.md and miss hooks entirely.

## The Gap
- Writing "do not modify prod.env" in CLAUDE.md is not enough
- Claude might follow it sometimes but not always
- Hooks are the enforcement mechanism

## How Hooks Work
Hooks are shell commands that execute in response to tool call events:
- PreToolUse hooks: run before a tool is called
- PostToolUse hooks: run after a tool is called
- Can block, modify, or log tool calls

## Article Referenced
"Claude Code Hooks: The Most Powerful Feature Nobody Uses"

## Takeaway
If you have a rule in CLAUDE.md, implement a corresponding hook to enforce it. Instructions without enforcement are suggestions.

## Connection to This Vault
Directly relevant to Claude Code setup — hooks are already configured in this project's settings.json. Review current hooks to ensure coverage of all CLAUDE.md rules.
"""

notes[os.path.join(tools, "claude-code-setup-official-plugin.md")] = """---
tags: [claude-code, plugins, tools, setup, hooks, skills, mcp]
source: https://x.com/sairahul1/status/2069774978019422537
author: Rahul (@sairahul1)
date: 2026-06-28
confidence: extracted
---

# claude-code-setup — Official Anthropic Plugin

## Summary
Anthropic quietly released an official plugin called claude-code-setup that turns Claude Code from "pretty good" into an actual AI dev environment. Scans your project and recommends + sets up: hooks, skills, MCP servers, subagents, automations.

## Installation
/plugin install claude-code-setup@claude-plugins-official

## What It Does
1. Scans your project
2. Recommends: hooks, skills, MCP servers, subagents, automations
3. Sets everything up step-by-step automatically

## Why It Matters
Most people use Claude Code completely vanilla — no hooks, no skills, no MCP. The real power comes from the ecosystem around Claude Code, not the base tool.

## Action Item
Install claude-code-setup on projects that haven't been set up — particularly new projects that start without this infrastructure.
"""

notes[os.path.join(tools, "hermes-agent-17-prompts.md")] = """---
tags: [hermes-agent, nous-research, local-ai, autonomous-agents, tools]
source: https://x.com/mnilax/status/2063697740526399833
author: Mnimiy (@Mnilax)
date: 2026-06-28
confidence: extracted
---

# Hermes Agent — 17 Prompts for Autonomous Operation

## Summary
Nous Research released Hermes Agent (February 2026) — an open-source, self-hosted agent that doesn't live inside an IDE and doesn't forget when the tab closes. Runs as a daemon on your own machine.

## Key Differentiators vs IDE-Bound Agents
- Runs as a daemon (persistent background process)
- Not dependent on keeping a browser tab open
- Self-hosted — your data stays local
- Open source — inspectable and modifiable

## The 17 Prompts
The tweet promotes 17 copy-paste prompts for leveraging this agent autonomously while you sleep. (Full prompt list not available in extraction — visit original tweet for prompts.)

## Connection
Compare to [[claude-code-setup-official-plugin]] — Hermes represents the open-source alternative stack to Anthropic's hosted approach.
"""

notes[os.path.join(tools, "local-ai-on-mac-performance-comparison.md")] = """---
tags: [local-ai, mac, performance, mlx, ollama, llama-cpp, hardware]
source: https://x.com/rewind02/status/2070500974335087067
author: rewind (@rewind02)
date: 2026-06-28
confidence: extracted
tweet-thread: true
---

# Local AI on Mac — MLX vs Ollama vs llama.cpp Performance

## Summary
Why Mac Studio performance for running AI models underperforms relative to published benchmarks: it's not the hardware, it's three software layers stacked on top.

## Key Finding
"Performance isn't about the hardware — it's about three software layers stacked on top of it"

## Framework Comparison
- **MLX** — Apple's native framework; fastest on Mac
- **Ollama** — Slower than alternatives despite popularity
- **llama.cpp** — Competitive alternative
- **vllm-mlx** — Also tested

## Critical Insight: Prefill Time
"Prefill" time (latency before first token generation) is an overlooked bottleneck. Most people measure tokens/second but ignore time-to-first-token.

## Recommendations
- **Quantization**: 4-bit is optimal speed-to-quality balance on Mac
- Use MLX for best performance on Apple Silicon
- Don't use Ollama as primary inference engine if speed matters

## Mac Advantages
Unified memory gives Macs an advantage vs Nvidia GPUs for models that fit in memory — no PCIe bandwidth bottleneck for memory transfers.

## Action Item
Compare to current setup: what framework is this system using for local models? Optimize if using Ollama.
"""

notes[os.path.join(tools, "local-ai-devices-vs-subscriptions.md")] = """---
tags: [local-ai, cost-optimization, hardware, subscriptions, tools]
source: https://x.com/noisyb0y1/status/2067866069037973631
author: Noisy (@noisyb0y1)
date: 2026-06-28
confidence: extracted
---

# Local AI Devices vs Subscriptions — $3/Month Alternative

## Summary
Most people pay $20-200/month for AI access (ChatGPT Plus, Claude Pro, Cursor). Local AI devices can provide comparable functionality for approximately $3/month.

## The Business Case
- ChatGPT Plus: $20/month
- Claude Pro: $20/month
- Cursor: varies
- Local alternative: ~$3/month in electricity

## Referenced Article
"Stop paying for AI subscriptions. These local devices do the same for $3/month."

## Connection
See also: [[asus-nuc-16-pro-local-ai-cluster]], [[local-ai-on-mac-performance-comparison]], [[local-llm-b2b-strategy]]
"""

notes[os.path.join(tools, "asus-nuc-16-pro-local-ai-cluster.md")] = """---
tags: [local-ai, hardware, ai-hardware, home-lab, cluster, tools]
source: https://x.com/lagerskoy/status/2071005662746743233
author: lagerskoy
date: 2026-06-28
confidence: extracted
---

# ASUS NUC 16 Pro — Local AI Cluster for Personal Use

## Summary
Video by Alex Ziskind (@digitalix) demonstrating three ASUS NUC 16 Pro boxes configured as a cluster for running local AI models like Llama 3.3 70B.

## Hardware
Three ASUS NUC 16 Pro boxes combined into a working cluster.

## Tests Covered
- CPU performance
- GPU performance
- NPU performance
- Cluster configuration for running Llama 3.3 70B

## Key Topics Addressed
- Hardware pricing
- Prompt processing speeds
- Memory limitations
- Networking challenges

## Why This Matters
"AI computation is transitioning from data centers into compact, purchasable systems that individuals can experiment with and scale."

Represents the hardware end of the local AI movement — alongside software frameworks in [[local-ai-on-mac-performance-comparison]].

## Reference
Video by Alex Ziskind @digitalix — practical, realistic desk setup demonstration.
"""

notes[os.path.join(tools, "claude-skills-gtm-outbound-motion.md")] = """---
tags: [claude-code, skills, gtm, sales, outbound, automation, tools]
source: https://x.com/yanndine/status/2069847546499887181
author: Yann (@yanndine)
date: 2026-06-28
confidence: extracted
---

# AI-Run GTM Motion with Claude Code Skills

## Summary
Claude Skills has transformed outbound operations. 215 Claude Code skills spanning the entire sales pipeline — operated from a single project folder and unified brief.

## What's Included (215 skills)
- **40 outreach skills** — ICP definition through pipeline review
- **131 plugin skills** — Supporting infrastructure
- **31 SDR-specific skills** — Sales development representative workflows

## Capabilities
- Persona mapping
- Trigger identification
- Copywriting by seniority level (VP, Director, IC)
- LinkedIn sequencing
- Deal risk flagging

## What You Need
- Laptop
- Claude Max subscription
- An afternoon to implement

## Key Advantage
Eliminates session-to-session inconsistencies and manual prompt rebuilding. One unified brief drives the entire sales cycle.

## Weekly Operations
- Outbound cycles
- Content generation
- Deal reviews

All within one session.
"""

notes[os.path.join(tools, "7-github-repos-enhance-claude-code.md")] = """---
tags: [claude-code, github, tools, enhancement, best-practice]
source: https://x.com/vaibhavsisinty/status/2068212256769466608
author: Vaibhav Sisinty (@VaibhavSisinty)
date: 2026-06-28
confidence: partial
retrieval: Full thread with 7 repos not captured — only opening tweet visible via Jina. Visit original URL for complete list.
---

# 7 GitHub Repos to Enhance Claude Code

## Opening Tweet
"7 GitHub repos that make Claude Code mass-destructively better. All free. Most people haven't installed a single one. Each one solves a specific gap that Claude Code doesn't fix on its own."

## Status: Partial Capture
The thread promised 7 specific GitHub repositories with descriptions of what each solves. The full thread content was not available via Jina extraction. The 7 repos are in the thread replies.

## Action Item
- Visit the original URL for the full list of 7 repos
- Add to project kaizen and /plan to evaluate and incorporate
- Add findings to Claude code best practice notes
"""

# ==================== AI/04-companies ====================

notes[os.path.join(companies, "google-5-day-ai-agents-curriculum.md")] = """---
tags: [google, ai-agents, learning, curriculum, resources]
source: https://www.linkedin.com/posts/lfrodrigues_google-released-huge-learning-resources-for-share-7473698603270807552-M1Hj/
author: Luís Rodrigues
date: 2026-06-28
confidence: extracted
---

# Google 5-Day AI Agents Learning Curriculum

## Summary
Google released comprehensive learning materials for AI agents — "an exceptional resource for anyone starting with AI Agents." Five-day structured curriculum progressing from foundation to production deployment.

## Five-Day Structure

**Day 1: Introduction to AI Agents**
- Distinguishing agents from chatbots
- Reasoning and autonomous action capabilities

**Day 2: Tools and MCP**
- Extending agents beyond conversation
- Integrating with external APIs
- Mastering Model Context Protocol

**Day 3: Context Engineering & Memory**
- Building persistent memory systems
- Agents retaining knowledge across interactions

**Day 4: Evaluation & Observability**
- Using logs and metrics to identify agent failures
- Implementing feedback loops

**Day 5: Production-Ready Deployment**
- Moving from test scripts to Vertex AI
- Multi-agent collaboration
- Safety mechanisms and infrastructure for reliability

## Key Resources
- Multiple whitepapers
- 10+ code samples and hands-on projects

## Central Theme
Real agents require complete systems with infrastructure — not just clever prompts. Success depends on evaluation, observability, and knowing when agents should refuse action.
"""

# ==================== AI/06-resources ====================

notes[os.path.join(resources, "postman-passport-secure-agent-api-access.md")] = """---
tags: [api-security, postman, credentials, non-human-identity, tools, ai-agents]
source: https://www.linkedin.com/posts/abhinavasthana_we-are-in-the-agentic-era-of-ai-and-agents-ugcPost-7475263464656142336-8Yqm/
author: Abhinav Asthana (CEO, Postman)
date: 2026-06-28
confidence: extracted
---

# Postman Passport — Secure API Credential Management for AI Agents

## Context
AI agents will consume APIs at 1000x the current rate. API keys stored in .env files and bash profiles get copy-pasted into Slack and Google Docs — creating exponential security risk as agent volume scales.

## The Problem
- API keys distributed in dotfiles on local machines
- Credentials shared across communication platforms
- Current access mechanisms (bearer tokens, OAuth) require API key distribution
- As agent volume scales, this risk grows exponentially

## Solution: Postman Passport
Instead of handing out real API keys, gives humans, machines, and agents a credential reference bound to its holder — useless to anyone else.

**Key mechanism**: Credential reference resolves to the real key inside the organization's network. "Actual keys never leave your vault."

## Architecture Principles
- Better developer experience prevents security problems upstream
- Credential binding to specific holders
- Server-side secret storage with runtime injection
- Governance, trust, identity, and observability as architectural requirements

## Limitation
(From commenter Edgar Kussberg): Passport protects credentials in transit but does NOT govern sensitive data flowing back in API responses at agent scale. This is a separate problem.

## Connection
Directly relevant to [[klue-hack-non-human-identity-attack-surface]] — same attack surface, complementary solution.
"""

for fpath, content in notes.items():
    with open(fpath, "w") as f:
        f.write(content)
    fname = os.path.basename(fpath)
    folder = os.path.basename(os.path.dirname(fpath))
    print(f"Written: AI/{folder}/{fname}")

print(f"\nTotal: {len(notes)} notes written")
