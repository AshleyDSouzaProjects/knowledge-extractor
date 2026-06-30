"""KUA Image Batch — Write notes from 4 image files + PDF incomplete-capture + cleanup"""
import os, shutil

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
concepts = os.path.join(vault, "AI/01-concepts")
tools = os.path.join(vault, "AI/02-tools")
thinking = os.path.join(vault, "AI/05-my-thinking")
pending_urls = os.path.join(vault, "00-inbox/pending URLs")
pending_disc = os.path.join(vault, "pending discussions")
today = "2026-06-28"

notes = {}

# ============================================================
# IMG_4565.jpeg — AI SLDC.md
# Traditional Iterative SDLC vs AI-Driven SDLC diagram
# ============================================================
notes[os.path.join(concepts, "ai-driven-sdlc-vs-traditional.md")] = """---
tags: [ai-sdlc, software-development, ai-architecture, agentic-ai, enterprise-ai]
source: image/IMG_4565.jpeg
date: 2026-06-28
confidence: raw
---

# AI-Driven SDLC vs Traditional Iterative SDLC

## Diagram Overview
Side-by-side comparison of Traditional Iterative SDLC and AI-Driven SDLC. Same phases, different bottlenecks, different proportions.

## Traditional Iterative SDLC
**Phases and durations:**
1. Requirements — 2-3 days
2. Design — 1-2 days
3. Implementation — 1-3 weeks
4. Testing — 3-5 days
5. Review & Deploy — 2-3 days
6. Maintenance — Ongoing

**Iteration cycle: weeks (Sprint-based)**

Bottleneck: Implementation (1-3 weeks) dominates the cycle.

## AI-Driven SDLC
**Phases:**
1. Requirements — Specification quality is the new bottleneck
2. Design — Architecture decisions amplified at scale; Specs become eval criteria (feedback loop back to requirements)
3. [AI Agent icon] — Minutes to hours; Agent self-corrects (feedback loop)
4. Evaluation:
   - Output Eval — Verify what it built
   - Trajectory Eval — AND how it got there
5. Review & Deploy
6. Maintenance — Continuous automation

**Iteration cycle: minutes to hours**

## Key Shifts in AI-Driven SDLC

**New bottleneck: Specification quality**
Where traditional SDLC bottlenecked on implementation time (weeks), AI-Driven SDLC bottlenecks on how well requirements are specified. Better specs = better agent output.

**Architecture decisions are amplified at scale**
Design phase decisions have larger downstream impact when an AI agent is executing implementation.

**Dual evaluation: Output + Trajectory**
Not just "did it build the right thing" (Output Eval) but "did it get there the right way" (Trajectory Eval). This matters for safety, reproducibility, and debugging agent behavior.

**Continuous feedback loops**
- Specs feed back as eval criteria
- Agent self-corrects during implementation
- Continuous automation in maintenance phase

## Implication
In AI-Driven SDLC, human leverage shifts from implementation to specification and evaluation. The ability to write precise requirements and evaluate agent trajectories becomes the core engineering skill.
"""

# ============================================================
# IMG_4603.jpg — Add to project Jumpstart.md
# Agentic AI Data Layers by Rahul Agarwal
# ============================================================
notes[os.path.join(concepts, "agentic-ai-data-layers.md")] = """---
tags: [ai-architecture, data-architecture, agentic-ai, enterprise-ai, data-engineering, ai-jumpstart]
source: image/IMG_4603.jpg
author: Rahul Agarwal
date: 2026-06-28
confidence: raw
relevant-for-project: AI Jumpstart
---

# Agentic AI Data Layers

Source: Rahul Agarwal infographic

## The 9 Data Layer Stack for Agentic AI

### 1. DATA INGESTION
Data sources → Gather data → Store in raw layer → Normalize formats

### 2. ETL / ELT PIPELINES
Raw data → Transform data → Load to warehouse → Do validation

### 3. DATA VERSIONING
Update dataset → Create new version → Monitor changes → Recreate outcomes

### 4. VECTOR PIPELINES
Input data → Split into chunks → Create embeddings → Vector DB → RAG

### 5. METADATA MANAGEMENT
Dataset created → Record schema → Support discovery → Monitor ownership

### 6. DATA GOVERNANCE
Set policies → Implement access control → Ensure compliance → Review usage

### 7. DATA QUALITY CHECKS
Incoming data → Apply validation rules → Identify anomalies → Notify/stop pipeline

### 8. DATA LINEAGE
Origin → Transform steps → Final tables → End consumers

### 9. STREAMING DATA
Events produced → Ingest streams → Process in real time → Trigger agents

### DATA WAREHOUSES / LAKES
Refined data → Central repository → Power analytics → Agent queries

## Key Insight
Each layer feeds into agent capabilities. Vector pipelines and RAG are the bridge between raw data and agent reasoning. Streaming data is what triggers agents in real time. Data governance and quality checks are non-negotiable for production agentic systems.

## Connection
Complements: [[contextual-semantic-layers-agentic-ai]], [[context-lake-orchestration-layer-for-ai-agents]]
"""

# ============================================================
# IMG_4551.jpg — Open source models.md
# 12 Open-Source LLM Models (ByteByteGo)
# ============================================================
notes[os.path.join(tools, "12-open-source-llm-models-reference.md")] = """---
tags: [open-source, llm, models, reference, ai-jumpstart]
source: image/IMG_4551.jpg
author: ByteByteGo
date: 2026-06-28
confidence: raw
relevant-for-project: AI Jumpstart
---

# 12 Open-Source LLM Models — Reference Guide (ByteByteGo)

## The 12 Models

| # | Model | Provider | Key Characteristic |
|---|-------|----------|--------------------|
| 1 | **Llama 4 Scout** | Meta | Text, documents, and images in one open-weight model |
| 2 | **DeepSeek V4** | DeepSeek | Frontier-level performance, MIT license, million-token context |
| 3 | **Qwen3** | Qwen (Alibaba) | Multilingual flagship with switchable thinking modes, Apache 2.0 |
| 4 | **Gemma 4** | Google | Google's open model running from smartphones to enterprise servers |
| 5 | **Phi 4** | Microsoft | Compact model, strong math reasoning, runs on a single GPU |
| 6 | **Mistral Small 3.1** | Mistral | Vision support and long context on consumer hardware |
| 7 | **Nemotron 3 Super** | NVIDIA | Million-token context with fully open weights and training recipes |
| 8 | **GLM 5.1** | Zhipu AI | Top of SWE-Bench Pro, MIT license, no commercial restrictions |
| 9 | **Kimi K2.6** | Moonshot AI | Competitive coding performance at significantly lower cost |
| 10 | **StarCoder2** | BigCode | Fully open: weights, data, and training pipeline all public |
| 11 | **OLMo 2** | Allen AI | Weights, data, code, and recipes all under Apache 2.0 |
| 12 | **Falcon 3** | Technology Innovation Institute | Lightweight open-weight models for single-GPU deployment |

## Groupings

### Frontier Performance
- DeepSeek V4 (MIT, million-token)
- GLM 5.1 (top SWE-Bench Pro)
- Kimi K2.6 (competitive coding at lower cost)

### Fully Open (weights + training data + code)
- StarCoder2 (weights, data, training pipeline all public)
- OLMo 2 (full Apache 2.0 stack)
- Nemotron 3 Super (fully open weights + training recipes)

### Multimodal
- Llama 4 Scout (text + docs + images)
- Mistral Small 3.1 (vision support)

### Compact / Edge-Friendly
- Phi 4 (single GPU, strong math)
- Gemma 4 (smartphone to enterprise)
- Falcon 3 (lightweight, single-GPU)

### Multilingual
- Qwen3 (multilingual flagship)
"""

# ============================================================
# IMG_4566.jpeg — Types of AI options.md
# 6 AI Deployment Patterns (Brij Kishore Pandey)
# ============================================================
notes[os.path.join(concepts, "6-ai-deployment-patterns-2026.md")] = """---
tags: [ai-deployment, cloud-ai, edge-ai, local-ai, private-ai, hybrid-ai, on-device-ai, infrastructure, ai-jumpstart]
source: image/IMG_4566.jpeg
author: Brij Kishore Pandey
date: 2026-06-28
confidence: raw
relevant-for-project: AI Jumpstart
---

# 6 AI Deployment Patterns Powering Modern AI in 2026

Source: Brij Kishore Pandey

Choose based on: **latency, privacy, cost, scale, governance, and connectivity**

---

## 1. Cloud AI — Hyperscale Intelligence

**Flow:** User Request → Send to Cloud → Large Model Runs → Uses Cloud Tools/Data → Returns Response

**Key features:** Elastic compute, large foundation models, managed services

**Pros:**
- Best for scale
- Access to the largest models
- Managed infrastructure

**Cons:**
- Higher latency
- Internet dependency
- Data residency concerns

**When to use:** Large-scale apps and foundation model access

---

## 2. Edge AI — Near the Source

**Flow:** Sensor/Input → Route to Edge Node → Local Inference → Immediate Action → Cloud Sync Optional

**Key features:** Low latency decisions, bandwidth savings, near-real-time processing

**Pros:**
- Fast local decisions
- Reduces bandwidth usage
- Works close to devices

**Cons:**
- Limited compute
- Harder fleet management
- Hardware fragmentation

**When to use:** Real-time field decisions

---

## 3. Local AI — On Your Machine

**Flow:** Prompt/Input → Load Local Model → Use Local GPU/CPU → Access Local Files → Generate Answer

**Key features:** Full control, offline capable, customizable setup

**Pros:**
- Strong privacy
- Works offline
- Full environment control

**Cons:**
- Hardware cost
- Setup and maintenance burden
- Limited scale vs cloud

**When to use:** Personal/private workstation use

---

## 4. On-Device AI — AI in Your Pocket

**Flow:** User Input → Device NPU Activates → Compact Model Runs → Instant Inference → Personal Response

**Key features:** Battery optimized, instant UX, data stays on device

**Pros:**
- Very low latency
- Better privacy
- Great mobile experiences

**Cons:**
- Smaller models only
- Limited memory
- Mostly inference-focused

**When to use:** Mobile and embedded experiences

---

## 5. Private AI — Enterprise-Controlled

**Flow:** Employee Request → Enterprise Gateway → Private Model/Data → Policy Check → Approved Output

**Key features:** VPC or on-prem, policy controls, sensitive data protected

**Pros:**
- Strong compliance
- Better security posture
- Good for sensitive workloads

**Cons:**
- Higher setup cost
- Operational overhead
- Slower to evolve

**When to use:** Regulated enterprise workloads

---

## 6. Hybrid AI — Best of Both Worlds

**Flow:** Request Arrives → Policy/Router Decides → Send to Best Environment → Combine Results/Data → Deliver Best Response

**Key features:** Smart routing, cost-performance balance, flexible deployment

**Pros:**
- Flexible architecture
- Balances privacy and scale
- Optimizes cost and latency

**Cons:**
- More complex architecture
- Governance is harder
- Requires strong observability

**When to use:** Mixed privacy + scale scenarios

---

## Decision Framework
Choose based on:
- **Latency** needs → Edge or On-Device
- **Privacy** requirements → Local, Private, or On-Device
- **Cost** sensitivity → Local or On-Device
- **Scale** requirements → Cloud or Hybrid
- **Governance** requirements → Private or Hybrid
- **Connectivity** constraints → Local or Edge (offline capable)
"""

# ============================================================
# PDF incomplete-capture
# ============================================================
pdf_note = os.path.join(pending_disc, "fable-5-fallout-pdf-pending.md")
with open(pdf_note, "w") as f:
    f.write("""---
tags: [incomplete-capture, pending-discussion, open-source, fable-5, pdf]
source: image/Fable_5_Fallout-1781587336137.pdf
date: 2026-06-28
status: incomplete-capture
---

# INCOMPLETE CAPTURE — Fable 5 Fallout PDF

**Reason:** PDF requires poppler-utils to render. Not installed (pdftotext not found).
**Original file:** Open source detailed pending discussion.md
**File:** Fable_5_Fallout-1781587336137.pdf (in vault root)

## Ashley Notes
Marked as "Open source detailed pending discussion" — this PDF appears to be about the fallout/impact of Claude Fable 5 on open source models or the AI ecosystem.

## Action Required
1. Run: `brew install poppler` to enable PDF reading
2. Then re-run: `python3 /path/to/pdf2md skills` on the PDF
3. OR use MinerU (mineru.net) — uploads and processes PDFs without local install

The PDF is currently at:
/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault/Fable_5_Fallout-1781587336137.pdf

---
*Filed by KUA on 2026-06-28*
""")
print("Created: fable-5-fallout-pdf-pending.md")

# ============================================================
# Write all notes
# ============================================================
for fpath, content in notes.items():
    with open(fpath, "w") as f:
        f.write(content)
    fname = os.path.basename(fpath)
    folder = os.path.basename(os.path.dirname(fpath))
    print(f"Written: AI/{folder}/{fname}")

# ============================================================
# Delete pending URL files for image captures
# ============================================================
image_pending_files = [
    "AI SLDC.md",
    "Add to project Jumpstart.md",
    "Open source models.md",
    "Types of AI options.md",
    "Open source detailed pending discussion.md",
]
for fname in image_pending_files:
    fpath = os.path.join(pending_urls, fname)
    if os.path.exists(fpath):
        os.remove(fpath)
        print(f"Deleted pending URL: {fname}")
    else:
        print(f"Not found: {fname}")

# ============================================================
# Delete image files from vault root (after filing notes)
# ============================================================
image_files = [
    "IMG_4565.jpeg",
    "IMG_4603.jpg",
    "IMG_4551.jpg",
    "IMG_4566.jpeg",
]
for img in image_files:
    img_path = os.path.join(vault, img)
    if os.path.exists(img_path):
        os.remove(img_path)
        print(f"Deleted image: {img}")
    else:
        print(f"Image not found: {img}")

# Keep the PDF — needed for future processing
print("Kept: Fable_5_Fallout-1781587336137.pdf (needs manual processing)")

# ============================================================
# Copy image-derived notes with project references to pending discussions
# ============================================================
disc_copies = [
    (os.path.join(concepts, "agentic-ai-data-layers.md"),
     "Add to project Jumpstart. Also has 'relevant-for-project: AI Jumpstart'."),
    (os.path.join(tools, "12-open-source-llm-models-reference.md"),
     "Add to project AI Jumpstart."),
    (os.path.join(concepts, "6-ai-deployment-patterns-2026.md"),
     "Relevant for AI Jumpstart — types of AI options and infrastructure decisions."),
]

import shutil
for src, note in disc_copies:
    if os.path.exists(src):
        dst = os.path.join(pending_disc, os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"Copied to pending discussions: {os.path.basename(src)}")

print("\n=== IMAGE BATCH COMPLETE ===")
remaining = [f for f in os.listdir(pending_urls) if f.endswith(".md")]
print(f"Remaining pending URL files: {len(remaining)}")
for f in sorted(remaining):
    print(f"  {f}")
