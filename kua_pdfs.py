"""Write vault notes for Fable 5 Fallout + IBM Enterprise 2030 PDFs, clean up pending discussions."""
import os, shutil

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
tools = os.path.join(vault, "AI/02-tools")
concepts = os.path.join(vault, "AI/01-concepts")
pending_disc = os.path.join(vault, "pending discussions")
today = "2026-06-29"

# ============================================================
# 1. Fable 5 Fallout — filed to AI/02-tools/ (local AI setup guide)
# ============================================================
fable_note = os.path.join(tools, "fable-5-fallout-local-ai-resilience-guide.md")
fable_content = """---
tags: [local-ai, resilience, agency, ai-infrastructure, ollama, lm-studio, hermes-agent, open-source, fable-5]
source: pdf/Fable_5_Fallout-1781587336137.pdf
author: Jordan Ross (8 Figure Agency)
date: 2026-06-29
confidence: extracted
---

# Fable 5 Fallout — Why You Need a Local Model (Jordan Ross)

Source: "The Handbook for Marketing Agency Owners" — 8figureagency.co

## Context: What Happened

On June 13, 2026, the US Commerce Department issued an export-control directive over foreign-national access to Fable 5 and Mythos 5. Anthropic had to disable both models for every customer worldwide overnight. The best model on the planet vanished between Friday and Saturday.

**The Lesson**: You don't own cloud models. You rent them. Rented access gets revoked — by a government, a policy change, a price hike, a company decision.

"The Bleeding Line": every business has one dependency that, if cut, you bleed out. For most agencies right now, it is a frontier API they don't own.

---

## Why Local AI: 3 Things Cloud Never Gives You

1. **Privacy** — model runs on your machine; client data never leaves the building; no logs on someone else's server
2. **Zero marginal cost** — after hardware, every query is free; 24/7 agents cost only electricity
3. **Nobody can turn it off** — works offline, in a blackout, on a plane; no government can revoke it

**Honest trade-off**: local models sit roughly 6-12 months behind the frontier. For 70-80% of routine high-volume work, they already clear the bar.

---

## What It Looks Like in Practice

**SEO shop**: keyword clustering across 10,000 terms overnight; first-draft content for 200 programmatic pages; internal linking maps; title/H1 variations — all free

**Paid ads shop**: 60+ creative variations per night; every winning ad rewritten into 15 fresh tests; bulk first-pass copy for every client

**SMMA/social shop**: caption and hook drafts for every client daily; DM triage; monthly reporting from raw client data — privately

**The framing**: "AI stops being a line item you pay per use and becomes an employee that works for free, around the clock, and can't be shut off."

---

## The Architecture: Cloud Brain, Local Muscles

Don't replace cloud — own a layer of it.

- **Cloud model** (brain): decisions, planning, hard reasoning, flagship work
- **Local models** (muscles): volume work — writing, scraping, coding, research — at zero cost

Example: coding agent on local model writes software 24/7; second local model scans the web and pings via Telegram when it finds opportunities. Both running on a box on your desk. Neither costing a token.

**The decision engine — 4 routing lanes:**
1. Private, sensitive, or high-volume background work → cheap local model
2. Needs giant context window → long-context model
3. Hard reasoning → frontier brain
4. Client-facing flagship → best model for that specific job

**Rule**: build model-agnostic. Wire your stack to route to the best tool per task so you can swap models without rebuilding.

---

## 8 Steps to Set It Up

**Step 1 — Download the runtime first** (not the model)
- Non-technical: LM Studio (lmstudio.ai) — real interface, click and run
- Developer: Ollama (ollama.com) — command line, one command to run

**Step 2 — Match model size to hardware**
- 4B → runs on almost anything (8GB laptop, some phones)
- 12B → sweet spot for 16GB machine
- 27-35B → strong Mac 32GB+ or dedicated GPU
- 70B+ → Mac Studio maxed, or NVIDIA DGX Spark (128GB unified memory)
- Leave headroom: don't load a 20GB model into 20GB RAM

**Step 3 — Pick model families worth knowing**
- **Qwen 3/3.5/3.6** — best all-around; strong coding + multilingual; clean commercial license; learn this family first
- **DeepSeek V4** — hard reasoning and coding; best price-to-performance; reasoning versions think 10-30s before answering (normal)
- **Gemma 4** (Google) — runs remarkably small; 16GB version; reads images; clean writer
- **GPT-OSS 20B** — best small reasoner; good tool-calling; modest hardware
- **Llama** (Meta) — biggest community; most fine-tunes; always a Llama for your setup

**Step 4 — Quantization (the cheat code)**
Raw model = uncompressed photo. Quantized = high-quality JPEG. Q4 roughly halves memory with minimal quality loss. Learn this one concept and your hardware does twice as much.

**Step 5 — Wire into your agent**
- **Hermes**: point a Hermes profile at local model → agent runs free, offline, persistent, pings over Telegram
- **Claude Code via Ollama**: `ollama launch claude --model qwen3` → wires Claude Code to local Ollama; requires 64K+ context and tool calling enabled

**Step 6 — Respect the context window**
Local charges you in RAM for context size. Keep sessions tight, clear often, work one task at a time.

**Step 7 — Give it tools**
"A small local model with web search, file access, and the ability to run code beats a giant model with none." Tools > bigger model.

**Step 8 — Fine-tune when ready** (not day one)
Train on your own data: your offers, your voice, your client niches. Generic model = floor. What you train on top = moat. Process-specific training builds something competitors can't clone.

---

## Key Quotes

"The model everyone can download is the floor. What you train on top of it is the moat."

"A model you chat with is a novelty. A model wired into an agent that works while you sleep is a business asset."

"Privacy as a sales weapon: the second you can say your data never leaves the building, you can sell to healthcare, legal, and finance accounts your competitors legally cannot touch."

## Connection
See also: [[local-ai-on-mac-performance-comparison]], [[local-ai-devices-vs-subscriptions]], [[asus-nuc-16-pro-local-ai-cluster]], [[local-llm-b2b-strategy]], [[hermes-agent-17-prompts]]
"""

with open(fable_note, "w") as f:
    f.write(fable_content)
print("Filed: AI/02-tools/fable-5-fallout-local-ai-resilience-guide.md")

# ============================================================
# 2. IBM Enterprise 2030 — filed to AI/01-concepts/
# ============================================================
ibm_note = os.path.join(concepts, "ibm-enterprise-2030-five-predictions.md")
ibm_content = """---
tags: [enterprise-ai, future-of-work, ai-strategy, ibm, 2030, quantum, productivity, ai-jumpstart]
source: https://www-api.ibm.com/adobe/assets/urn:aaid:aem:9b35d27c-6a4d-4dcd-a804-550ea0d80cd0/original/as/the-enterprise-in-2030-report.pdf
authors: [Andy Baldwin, Neil Dhar, Ritika Gunnar, Rahul Kalia, James Kavanaugh, Salima Lin, Joanne Wright — IBM Institute for Business Value]
survey: 2,000 executives, 33 geographies, 23 industries (Q3/Q4 2025, with Oxford Economics)
date: 2026-06-29
confidence: extracted
relevant-for-project: AI Jumpstart
---

# IBM Enterprise in 2030 — 5 Predictions for the AI-First Enterprise

Source: IBM Institute for Business Value — "The Enterprise in 2030: Engineered for Perpetual Innovation"

## Core Thesis

"AI isn't just enhancing the business model. By 2030, it will be the business model."

The enterprise of the future won't win by fine-tuning today's operations. Success flows from lightning-fast decision-making and real-time course-correction. This requires rewiring the enterprise to be less monolithic, more modular — less like hardware, more like software.

**The Smarter Enterprise**: embeds transformation into its operational DNA. Uses every interaction, transaction, and outcome to continuously become smarter, faster, and more responsive.

---

## Key Stats (2,000 executives surveyed)

- 79% say AI will significantly contribute to revenue by 2030 (up from 40% today)
- Only 24% can clearly see where that revenue will come from
- 67% expect AI to eliminate resource and skills constraints holding them back
- 64% say competitive advantage will come from innovation, not resource optimization
- AI investment will surge ~150% between 2025 and 2030
- 57% say competitive advantage in 2030 will come primarily from sophistication of AI models
- 25% of enterprise boards expected to have an AI advisor or co-decision maker by 2030

---

## Prediction 1: Competitive Pressure Will Make Big Bets Non-Negotiable

In 2030, success = how much an enterprise disrupts its industry quarter by quarter. The biggest risk won't be making wrong bets — it's making bets that are too small.

**The AI Paradox**: when used to full potential, AI provides differentiated value. When used as a crutch, it fuels homogenization. Two-thirds of executives are concerned AI is creating conformity — organizations making the same decisions from the same data.

**Speed over perfection**: 55% say competitive advantage will depend more on speed of execution than making perfect decisions.

**AI-first organizations vs peers by 2030:**
- 70% greater productivity improvement
- 74% greater reduction in process cycle times
- 67% greater improvement in project delivery times

**What to do**: bet big on unconventional ideas tangential to your core business today. Use AI-powered market scanning. Stress-test through rapid experimentation with MVPs. Foster a culture where failures = learning opportunities.

---

## Prediction 2: Today's Productivity Gains Will Fund Tomorrow's Industry Transformation

A two-phase revolution:
- **Phase 1** (underway): eliminate waste, accelerate processes, amplify human capability within existing business models
- **Phase 2**: reinvest freed-up resources to reimagine entire industry verticals

**The numbers:**
- AI expected to increase productivity by 42% by 2030
- Organizations integrating AI into products + services + using more sophisticated models → 54% productivity gain
- 70% of executives plan to use value from AI to fund investment and growth (not bank it as profit)

**The flywheel**: AI implementation → productivity → investment in innovation → transformation → more growth

**IT services wake-up call**: an industry selling hours when AI can deliver outcomes in a fraction of the time faces existential threat. 81% of IT services executives are using AI savings to fund reinvention. Outcome-based billing replacing time-based billing.

**Auto industry precedent**: digital/software revenue = 15% of total automotive revenue today, expected to reach 51% by 2035.

**Consumer note**: 56% of consumers say they're excited enough about AI-enabled services they'd accept flaws. But two-thirds would switch brands if a company concealed AI's involvement.

**What to do**: set a 2030 productivity moonshot goal. Launch quarterly "efficiency sprints" — cross-functional teams find one workflow that can be 50% faster. Create a "productivity-to-opportunity map" connecting efficiency gains to revenue capabilities.

---

## Prediction 3: The Best AI Will Be One-of-a-Kind. Your Kind.

Competitive advantage won't come from using the largest models. It will come from using AI in a way no one else has.

When everyone has access to the same foundation models, the differentiator is:
- How models are combined and customized
- How unique proprietary data is incorporated
- Fine-tuning for specific business objectives

**Framework: LLM vs SLM**
- **LLMs**: general reasoning, versatile, high compute — for complex tasks and problem-solving
- **SLMs**: compact, fast, domain-specific — for real-time apps (chatbots, mobile, IoT) where speed > raw capability
- Match the right tool to the right job, then layer proprietary data on top

By 2030, 82% of executives expect their AI portfolio to include multiple specialized models (partial stat — report continues beyond extracted section).

---

## Prediction 4: AI Won't Do All Your Thinking for You

Human judgment remains essential — but the nature of what humans are responsible for shifts dramatically.

Key tension: AI handles analysis and pattern recognition at scale, but humans must set direction, ask the right questions, and make the strategic calls. The quality of human judgment becomes more — not less — important as AI handles execution.

"We'll need more problem solvers who understand both the business and the models — people who can marry technical capability with business insight. That's the future of every company." — Umang Dharmik, SVP IT, Mercedes-Benz Research Development India

---

## Prediction 5: Quantum Will Cause the Next Seismic Shift

Quantum computing is the next layer of disruption beyond AI. IBM positions quantum as the capability organizations need to prepare for now, even though mainstream enterprise quantum is still ahead.

---

## C-Suite Priority Shifts: 2025 vs 2026-2030

| 2025 Priority | 2026-2030 Priority |
|---|---|
| Productivity/efficiency | Product & service innovation |
| Product & service innovation | Productivity/efficiency |
| Speed of execution | Cybersecurity and data privacy |
| Customer experience | Customer experience |
| AI and tech modernization | Talent recruiting and retention |

Notable shifts: product/service innovation moves to #1. Cybersecurity drops in ranking (becoming table stakes). Ecosystems and partnerships also drop (also table stakes).

---

## Cybersecurity in the Smarter Enterprise

AI is becoming the intelligent backbone of security operations, not just a defensive tool:
- AI augmentation in security operations expected to increase 50% over next 3 years
- Generative AI security capabilities will grow 63%
- 30% of organizations already have an AI-first security foundation that is self-regulating, self-correcting, and self-healing

**Three levels:**
- **Self-regulating**: automatically adjusts security policies and access controls based on real-time risk
- **Self-correcting**: identifies and fixes vulnerabilities as they occur
- **Self-healing**: orchestrates recovery — isolates compromised systems, restores services, rebuilds infrastructure

Result: security evolves from cost center → strategic capability that enables rapid, safe innovation.

---

## Key Quotes

"By 2030, insight will be everywhere. Interfaces will be radically different, and AI will act as the business intelligence system, decision engine, and a participant in operations." — Chad Gates, Pronto Software

"AI neutralizes the classic advantage of the incumbent. A startup can now operate at the same scale as a large enterprise, but move at a much faster speed." — Aaron Levie, CEO Box

"The concept of resource optimization is already outdated." — Akiyuki Ui, Mizuho Bank

"The quality of data, not the quantity, will be the biggest source of competitive advantage." — Junta Tsujinaga, President & CEO, OMRON

"If you fast forward to 2030, the majority of governance work may not actually be done by humans due to its scale and complexity." — Kristie Chon Flynn, DPO, Google

## Connection
[[enterprise-agentic-platform-architecture-mckinsey]], [[matrix-os-agent-operating-system]], [[post-agent-companies]], [[ai-organization-success-emotional-clarity]]
"""

with open(ibm_note, "w") as f:
    f.write(ibm_content)
print("Filed: AI/01-concepts/ibm-enterprise-2030-five-predictions.md")

# ============================================================
# 3. Copy IBM note to pending discussions (per Ashley's instructions)
# ============================================================
ibm_disc = os.path.join(pending_disc, "ibm-enterprise-2030-five-predictions.md")
shutil.copy2(ibm_note, ibm_disc)
print("Copied to pending discussions: ibm-enterprise-2030-five-predictions.md")

# ============================================================
# 4. Copy Fable 5 note to pending discussions (open source discussion)
# ============================================================
fable_disc = os.path.join(pending_disc, "fable-5-fallout-local-ai-resilience-guide.md")
shutil.copy2(fable_note, fable_disc)
print("Copied to pending discussions: fable-5-fallout-local-ai-resilience-guide.md")

# ============================================================
# 5. Remove the incomplete-capture placeholder notes
# ============================================================
to_remove = [
    os.path.join(pending_disc, "ibm-enterprise-2030-report-pending.md"),
    os.path.join(pending_disc, "fable-5-fallout-pdf-pending.md"),
]
for p in to_remove:
    if os.path.exists(p):
        os.remove(p)
        print(f"Removed placeholder: {os.path.basename(p)}")

# ============================================================
# 6. Delete PDF from vault root (no longer needed there)
# ============================================================
pdf_in_vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault/Fable_5_Fallout-1781587336137.pdf"
if os.path.exists(pdf_in_vault):
    os.remove(pdf_in_vault)
    print("Deleted: Fable_5_Fallout-1781587336137.pdf from vault root")

print("\nDone.")
