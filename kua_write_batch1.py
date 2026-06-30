"""KUA Batch 1 — Write AI/01-concepts/ vault notes"""
import os

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
concepts = os.path.join(vault, "AI/01-concepts")
os.makedirs(concepts, exist_ok=True)

notes = {}

notes["enterprise-agentic-platform-architecture-mckinsey.md"] = """---
tags: [ai-architecture, enterprise-ai, mckinsey, agentic-ai, strategy]
source: https://medium.com/quantumblack/creating-a-future-proof-enterprise-agentic-platform-architecture-c21fc48406a5
via: https://www.linkedin.com/posts/areganti_really-raw-and-no-bs-article-from-mckinsey-share-7472836203365638144-p6mk/
date: 2026-06-28
confidence: extracted
---

# Enterprise Agentic Platform Architecture (McKinsey QuantumBlack)

## Summary
McKinsey QuantumBlack framework for building future-proof enterprise agentic systems. Argues that horizontal solutions (copilots, chatbots) lack transformative power — vertical, workflow-embedded agents deliver genuine value. Addresses the "gen AI paradox": widespread adoption with limited measurable business impact.

## The Central Problem
- Build vs buy decisions
- Short-term gains vs long-term technical debt
- Balancing speed with security and observability in non-deterministic systems
- Avoiding vendor lock-in while maintaining flexibility

## Architecture Framework
A "composable and compostable" platform connecting:
- In-house systems and data repositories
- External agentic applications (MS Copilot, ServiceNow, AgentForce)
- Custom-built capabilities for differentiation
- Shared services (evaluation, orchestration, security)

## Three Design Principles

**1. Protocol-First Interoperability**
Emerging standards like Agent2Agent Protocol (A2A) and Model Context Protocol (MCP) to enable multi-vendor workflows and prevent lock-in.

**2. Production-Ready from Day One**
Four foundational capabilities required immediately:
- Agentic evaluation frameworks for reliability
- Marketplaces for tool/agent discovery and reuse
- Memory management systems
- Continuous feedback mechanisms

**3. Continuous Innovation & Exploration**
Dedicating R&D to track market evolution, simplify architecture as solutions mature, integrate GraphRAG and workflow engines.

## Build/Partner/Buy Decision Framework
- **Buy**: Clear market solutions requiring minimal customization
- **Partner**: Emerging categories lacking viable options; reduces future technical debt
- **Build**: Selective focus on true competitive differentiation

## Case Studies (Financial Sector)
1. European bank automating credit application workflows
2. Financial services firm: AI agents for developer productivity (50% acceleration)
3. Global bank reinventing SDLC with automated agent workflows and "night shift" automation

## Key Emerging Technologies
- **GraphRAG**: Combines agents with knowledge graphs for contextual precision and auditability
- **Workflow Engines**: Constrain agent autonomy within deterministic processes — explicit steps, validations, audit logs

## Key Insight
"The value migrates from individual agents to the integrated platform enabling them."
"""

notes["context-lake-orchestration-layer-for-ai-agents.md"] = """---
tags: [context-lake, ai-architecture, agentic-ai, orchestration, enterprise-ai, mcp]
source: https://www.port.io/glossary/context-lake
via: https://www.linkedin.com/posts/pavan-belagatti_you-need-a-contextual-semantic-layercontext-share-7473976634266529792-2MSm/
series: context-lake-series
date: 2026-06-28
confidence: extracted
---

# Context Lake — Orchestration Layer for AI Agents

## Summary
A context lake is "an aggregated, structured repository where all the information an AI agent needs to operate is stored, correlated, and governed." Evolution of data lakes — from raw analytics data to actionable, domain-specific knowledge accessible to both humans and AI agents.

## Four Core Data Layers
1. **Domain Knowledge** — APIs, services, dependencies, architectural blueprints (GitHub repos, docs)
2. **Operational State** — Real-time metrics, logs, incidents, in-progress changes (PagerDuty, Kubernetes)
3. **Engineering Metadata** — Ownership, policies, access controls, quality signals, observability data
4. **Actions and Tools** — Self-service workflows and available automations; gives agents autonomy while preventing unwanted actions

## How It Works
Context lake functions as an orchestration layer between AI agents and organizational systems. When paired with MCP server:
- Exposes tools and actions to agents
- Acts as an interface similar to a UI for humans
- Provides agents with structured, labeled data for pattern recognition
- Embeds governance and policy enforcement directly into metadata

## Benefits
**1. Higher-Quality Agent Inputs**
Structured, labeled data with metadata like ownership and compliance tags transforms raw data into "reusable learning inputs." Agents can move beyond "What's this API?" to "What's this PCI-compliant API owned by Team A with three downstream dependencies?"

**2. Responsible Governance**
- Embedded policies and controls in the metadata layer
- Guardrails similar to "golden paths" in platform engineering
- Access controls based on data classification (PII restrictions)

**3. Scalable Agent Orchestration**
Multiple AI agents can coordinate as an "intelligent swarm," chaining actions into autonomous workflows while maintaining compliance and human oversight.

## Use Case: Self-Healing Incident Response
An incident-response agent detects failures, queries the context lake for ownership, opens tickets, triggers remediation agents, and logs changes for audit compliance — all autonomously.

## Key Distinction: Data Lake vs Context Lake
Data lakes hold raw data for analytics; context lakes hold actionable, domain-integrated knowledge for immediate operational use.

## Without Context Lake
Agents given unstructured data hallucinate, duplicate work, and make unsafe changes — contributing to "agentic chaos."

## Key Insight
As teams scale from single agents to coordinated multi-agent systems, the context lake becomes critical infrastructure — the shared source of truth enabling agents to collaborate effectively with humans and each other.
"""

notes["contextual-semantic-layers-agentic-ai.md"] = """---
tags: [semantic-layer, agentic-ai, data-architecture, knowledge-graph, rag, ai-architecture]
source: https://www.tellius.com/resources/blog/from-metrics-to-meaning-the-evolution-of-the-semantic-layer-in-the-age-of-agentic-ai
series: context-lake-series
date: 2026-06-28
confidence: extracted
---

# Contextual Semantic Layers — Evolution for Agentic AI (Tellius)

## Summary
Traditional semantic layers designed for dashboards must evolve into contextual semantic layers combining governed metrics, ontology, knowledge graphs, memory systems, and LLM orchestration. Enables AI agents to plan appropriate workflows, show reasoning, and maintain governance guardrails at scale.

Key evidence: LLMs struggle with extended context unless memory is structured; querying knowledge graphs improved accuracy from 16% to 54% in enterprise benchmarks.

## Problem with Legacy Semantic Layers
- Static and passive — built for dashboards, not LLMs
- Unable to capture nuance or combine structured with unstructured data
- Lacked memory for multi-turn conversation
- Could not plan multi-step analysis for "why" questions

## Contextual Semantic Layer Architecture (5 Layers)
1. **Data warehouse** — Snowflake/BigQuery/Redshift as source of truth
2. **Physical data model** — Tables, keys, partitions
3. **Semantic stack** (the innovation):
   - Metrics layer: Versioned KPI definitions
   - Ontology layer: Formal entities and relationships
   - Context & memory: Conversational state, prior filters, user feedback
   - Knowledge graph: Connects structured with unstructured evidence
4. **LLM layer** — Interprets natural language, drafts plans, stays grounded
5. **User interface/agent** — Chat/voice surface with governed answers

## Five Question Types, Five Plans
- **What** — Metric lookup with trend and lineage
- **Why** — Root-cause analysis decomposing change across dimensions
- **How to improve** — Recommendations based on RCA drivers
- **Compare** — Cohort/segment comparison with significance checks
- **Forecast/simulate** — Predictive models with backtest error disclosure

## Eight Stages Every Question Follows
1. Intent & routing — Classify question type, produce plan
2. Metrics resolver — Bind terms to governed definitions, generate SQL
3. Knowledge-graph traversal — Walk allowed edges
4. Hybrid retrieval (RAG) — Pull entity-linked unstructured evidence
5. Evidence packer — Normalize, remove duplicates, rank contributors
6. Guardrails — Security/policy checks before retrieval and composition
7. LLM composer — Draft narrative, add citations, record model version
8. Governed output — Return answer with chart and clickable sources

## Evaluation SLO Thresholds (Realistic Production)
- Lookups: exactness >= 99%, faithfulness 100%, <= 3s P95
- RCA/Compare: coverage >= 60-80%, faithfulness 100%, <= 10s P95
- Forecast: disclose backtest error; <= 15s P95

## Common Production Pitfalls
- Exploding joins → whitelist safe join paths
- Historical correctness → teach "as-of date" semantics
- Units/currency drift → normalize in metrics layer
- Stale embeddings → re-embed on schedule
- Prompt injection → constrain tool use, sanitize retrieved content

## ROI Formula
- Time saved: (analyst hours saved/week) × (fully-loaded rate) × 52
- Decision speed: (days reduced) × (value/day)
- Error reduction: (pre→post error rate) × (cost/error)

## Key Insight
"Business meaning travels with the question" — intent, definitions, entities, evidence, and governed output must chain together with session memory preserved throughout.
"""

notes["genai-governance-10-point-framework.md"] = """---
tags: [ai-governance, data-governance, enterprise-ai, rag, compliance]
source: https://www.linkedin.com/posts/prem-natarajan-ai_generative-ai-does-not-fail-only-because-share-7472625266033623042-pxBT/
author: Prem Natarajan
series: prem-natarajan-ai-series
date: 2026-06-28
confidence: extracted
---

# GenAI Governance — 10-Point Framework (Prem Natarajan)

## Core Thesis
"Generative AI does not fail only because of the model. It often fails because the data behind it was never governed properly."

When enterprise data enters AI workflows through training, fine-tuning, RAG, prompts, or evaluation pipelines, every governance weakness becomes a business risk.

## 10-Point GenAI Data Governance Framework

1. **Classify** — Classify data by sensitivity, risk, and approved AI usage
2. **Approve sources** — Approve trusted sources before AI workflows
3. **Restrict access** — Restrict access using roles, purpose, and context
4. **Minimize** — Minimize sensitive data before processing
5. **Track lineage** — Track lineage across sources, transformations, outputs
6. **Monitor quality** — Monitor quality, completeness, and freshness continuously
7. **Govern RAG** — Govern RAG documents, chunks, metadata, permissions
8. **Define retention** — Define retention rules for prompts, logs, embeddings
9. **Monitor usage** — Monitor usage, leakage, policy violations
10. **Record consent** — Record consent and enforce approved purposes

## Key Insight
"The strongest GenAI systems are not built on the largest datasets. They are built on the right data, used for the right purpose, with clear ownership and controls."

## Application
Organizations should prioritize governance infrastructure BEFORE scaling AI adoption.
"""

notes["klue-hack-non-human-identity-attack-surface.md"] = """---
tags: [ai-security, api-security, non-human-identity, oauth, attack-surface, enterprise-ai]
source: https://www.linkedin.com/posts/siddhanttrivedi_1000-api-queries-in-15-minutes-hundreds-share-7475098733186113537-3Gvs/
author: Sid Trivedi (Foundation Capital)
date: 2026-06-28
confidence: extracted
---

# Klue Hack — Non-Human Identity Attack Surface

## The Incident
~1,000 API queries in 15 minutes. Hundreds of companies breached. Not a single password cracked.

Klue (competitive intelligence platform) was breached via a legacy credential created years ago for an integration test that was never decommissioned. Attackers stole the OAuth tokens Klue uses to connect to customers' Salesforce accounts.

## Affected Companies
Huntress, HackerOne, Snyk, Tanium, Recorded Future, Insurity, Sprout Social

## Attack Mechanism
1. Legacy test credential still active — never shut off
2. Attackers stole OAuth tokens Klue held for customer Salesforce connections
3. To Salesforce, those tokens = Klue (legitimate connection)
4. No password, no MFA, no phished employee — just a trusted connection turned into a master key
5. Automated scripts silently drained CRM data for ~24 hours
6. One company's environment saw ~1,000 API queries in 15 minutes without triggering a single alarm

## Pattern: Third Occurrence in Under a Year
1. Salesloft Drift — August 2025
2. Gainsight — November 2025
3. Klue — June 2026

## Core Insight
"The new attack surface isn't the employee. It's the integration."

Every SaaS tool wired into CRM/sales stack creates a non-human identity with standing access to sensitive data — almost nobody watches those connections the way they watch human accounts.

## Key Vulnerabilities
- **OAuth Token Compromise** — Stolen OAuth tokens provide authenticated access without credential theft
- **Non-Human Identity Risks** — Service accounts, API keys, OAuth tokens largely unmonitored
- **Legacy Credential Neglect** — Old test credentials never decommissioned
- **Detection Gaps** — Automated scripts can drain data without triggering security alarms

## Critical Implication for AI Agents
As AI agents proliferate and each creates new integrations and API connections, the non-human identity attack surface expands exponentially. Organizations need the same security discipline for agent credentials as for human accounts.

## Business Opportunity (for Founders)
Managing third-party vendor risk and monitoring OAuth tokens, API keys, AI agents, and service accounts (non-human identities) across every company.
"""

notes["ai-agent-memory-write-consolidate-recall-apply.md"] = """---
tags: [ai-agents, memory, claude-code, anthropic, best-practice]
source: https://x.com/zodchiii/status/2069744750496772379
author: darkzodchi (@zodchiii)
date: 2026-06-28
confidence: extracted
---

# AI Agent Memory — Write, Consolidate, Recall, Apply Framework

## Summary
A senior Anthropic engineer published a 15-page blueprint for giving AI agents real memory. This four-step framework is now standard in Claude Code agent loops.

## The Four-Step Memory Framework

1. **Write** — Record attempts and outcomes
2. **Consolidate** — Distill into reusable lessons
3. **Recall** — Review lessons before tasks
4. **Apply** — Avoid previous dead ends

## Key Insight
This is described as "the clearest blueprint" for agent memory — moving beyond stateless operation where agents repeat the same mistakes.

## Connection to Claude Code
The approach is now standard in Claude Code agent loops, making this directly applicable to Claude-based development workflows.

## Application
- Agents should write down what they tried and what happened
- Periodic consolidation turns trial-and-error into reusable knowledge
- Recalling lessons before starting a task prevents repetition of dead ends
- Active application of lessons closes the feedback loop
"""

notes["company-skills-in-version-control.md"] = """---
tags: [ai-operations, process-management, skills, agentic-ai, future-of-work]
source: https://x.com/aakashgupta/status/2070960866162557238
author: Aakash Gupta (@aakashgupta)
date: 2026-06-28
confidence: extracted
---

# Company Skills in Version Control — Process Management Innovation

## Summary
What it looks like when a company puts every job in the building into version control. Every function gets a folder; inside are the activities; inside those are skill files encoding how the best person at the company does that task.

## The Problem It Solves
Most companies run on tribal knowledge:
- One CSM knows how to save a churning account
- One PM knows how to write the brief that moves engineering
- That knowledge walks out the door when they quit
- Never reaches the person sitting three feet away

## The Model
- Every function (customer success, sales, finance, engineering) gets a folder
- Inside: the actual activities (renewal, upsell, onboarding, escalation)
- Inside those: skill files spelling out exactly how the best person does that task
- Onboarding becomes `git clone` — new hire pulls the repo and operates on day one the way your best person operates after four years

## Second-Order Effect
"Once the process lives in a file, the human moves from holding the process to editing it."
- A PM ships front-end and back-end features to production by calling skills, not by memorizing the codebase
- A CPO runs product with 5 PMs and 4 designers, down from hundreds, because coordination cost collapses when everyone reads from the same committed playbook

## The Implicit Organizational Decision
Reading each folder name is a map of which tasks stay human and which become a skill file. This call used to be implicit. Now it has a commit history.

## Key Contrast
- Companies moving slowest: treat process as something absorbed by sitting in the room for three years
- Companies moving fastest: treat process as something you pull in thirty seconds

## Relevance to AI Jumpstart
Directly applicable to how AI-native organizations structure themselves. The "skill file" model aligns with Claude Code skills and agent-based workflows.
"""

notes["google-54-page-ai-agents-framework.md"] = """---
tags: [ai-agents, google, framework, multi-agent, architecture]
source: https://x.com/de1lymoon/status/2070954316719120848
author: Alex (@de1lymoon)
date: 2026-06-28
confidence: extracted
---

# Google 54-Page AI Agents Framework — 5 Levels

## Summary
Google released a 54-page framework for constructing AI agents with planning, action, collaboration, and self-improvement capabilities. Outlines progression from single reasoning model to multi-agent systems.

## Core Loop
Mission → Think → Act → Observe → Adapt

## Five Agentic System Levels
- **Level 0** — Model reasons without external interaction
- **Level 1** — Tools enable access to search, APIs, databases, real actions
- **Level 2** — Planning and memory support multi-step goal completion
- **Level 3** — Specialized agents collaborate via MCP and A2A
- **Level 4** — System learns from feedback, simulations, production failures

## Three Essential Components
1. **Model** (the brain)
2. **Tools** (the hands)
3. **Orchestration** (the nervous system)

## Production Infrastructure Required
Beyond the core three components, production needs:
- Agent operations
- Tracing
- Evaluations
- Human oversight
- Identity management
- Security protocols

## Key Insight
"Developers stop writing every rule like bricklayers. They become directors who define the goal, tools, constraints and quality bar."

## Companion Resource
Related article: "From prompter to loop designer: the 10-step roadmap" — evolution from interactive tool usage to autonomous system design.
"""

notes["loop-engineering-prompter-to-loop-designer.md"] = """---
tags: [ai-agents, loop-engineering, claude-code, automation, agentic-ai]
source: https://x.com/0xcodez/status/2064374643729773029
author: Codez (@0xCodez)
date: 2026-06-28
confidence: extracted
---

# Loop Engineering — Prompter to Loop Designer

## Summary
Article about "Loop engineering: the 14-step roadmap from prompter to loop designer." 6.6M views. Addresses the gap between developers who still prompt coding agents by hand and those who build autonomous loops.

## Core Insight
"Most developers still prompt their coding agents by hand. They type, they wait, they read the diff, they type again."

Only 9 out of 10 builders have never written a single loop that prompts the agent — they're stuck in manual interaction mode.

## What Loop Engineering Represents
The progression from:
- Typing prompts manually → waiting → reviewing → typing again
to:
- Defining loops that prompt the agent, observe outputs, and iterate autonomously

## Connection
Pairs with: [[google-54-page-ai-agents-framework]] (Level 4: system learns from feedback)
Also connects to: [[langchain-4-loop-framework]]
"""

notes["ai-agent-self-improvement-loops.md"] = """---
tags: [ai-agents, self-improvement, loops, agentic-ai, research]
source: https://x.com/mnilax/status/2069771486450024898
author: Mnimiy (@Mnilax)
date: 2026-06-28
confidence: extracted
---

# AI Agent Self-Improvement Loops — Research Insights

## Summary
Google and Stanford engineers released a 39-page research paper examining AI agent self-improvement through the feedback loop model: input → output → feedback → update → repeat.

## Critical Finding
Only **9% of agents actually run autonomous loops**. The other 91% rely on manual human prompts.

## Three Critical Components for Functional Self-Improvement Loops
1. **Starting artifact** — The initial input that kicks off the loop
2. **Credit horizon** — How far back to attribute credit for outcomes
3. **Experience batching** — How to group experiences for learning

## Why Most Self-Improvement Loops Fail
The three components above are overlooked in most implementations.

## Key Implication
Most "AI agent" systems are not truly agentic — they're just sophisticated chatbots with human operators triggering each step. True autonomy requires properly designed feedback loops.
"""

notes["matrix-os-agent-operating-system.md"] = """---
tags: [ai-agents, architecture, multi-agent, orchestration, enterprise-ai]
source: https://x.com/dereknee/status/2070065136442933407
author: Derek Nee (@DerekNee)
date: 2026-06-28
confidence: extracted
---

# Matrix OS — Agent Operating System Architecture

## Core Thesis
"You cannot run a company on one giant agent with every tool, every file, and no accountability. That's not autonomy. That's a fog machine."

Building scalable autonomous systems requires architectural discipline, not monolithic agent design.

## Matrix Framework Components

- **Workspace Brain** — Consolidated company knowledge: documentation, codebase, goals, operating rules
- **Runtime Orchestrator** — Manages permissions, dispatch, and verification
- **Department Structure** — Long-running agents with defined scope, identity, and accountability (not chat threads)
- **Scoped Workers** — Specialized agents handling specific tasks with clear success criteria
- **Proof Loop** — Verification that output represents actual progress

## Key Insight
Effectiveness comes from "the right agent with the right context inside the right boundary using the right tools" — not from expanding a single agent's capabilities.

## Improvement Mechanism
Organizational improvement happens through "proof compounding through the system," not individual agent self-modification.

## Practical Implication
- Every agent needs defined scope, identity, and accountability
- Department-level agents (like department heads) provide coherent context
- Scoped workers operate within those boundaries
- The proof loop ensures outputs actually advance goals

## Connection to AI Jumpstart
Directly relevant to designing multi-agent architectures for the AI Jumpstart project.
"""

for fname, content in notes.items():
    fpath = os.path.join(concepts, fname)
    with open(fpath, "w") as f:
        f.write(content)
    print(f"Written: AI/01-concepts/{fname}")

print(f"\nTotal: {len(notes)} notes written to AI/01-concepts/")
