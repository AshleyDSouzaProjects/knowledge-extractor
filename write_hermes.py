import os

vault = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
bp_path = os.path.join(vault, "AI/05-my-thinking/hermes-best-practice.md")

with open(bp_path) as f:
    content = f.read()

marker = "## 17 Autonomous Operation Prompts (Mnimiy/@Mnilax, 2026-06-28)"
if marker in content:
    content = content[:content.index(marker)]

section = """## 17 Autonomous Operation Prompts (@Mnilax / Mnimiy, 2026-06-28)

Source: https://x.com/mnilax/status/2063697740526399833 — full content retrieved manually.

### Mental model
A prompt to a chat window is a question. A prompt to a persistent agent is a **job description**: trigger (schedule or event) + body (what to do) + escalation rule (when to bother you). Drop any of the three and the prompt either never fires, does the wrong thing, or buries you in noise.

### Setup (set once)

    hermes config set model anthropic/claude-opus-4.8
    hermes config set terminal.backend daytona

Why: small/local models drop tool calls mid-task on multi-step jobs. Claude holds context. Serverless backend = hibernates when idle = pennies between jobs, not a 24/7 invoice.

### The 17 Prompts

**1. Morning brief (7am)**

    every weekday at 7am, pull my unread GitHub notifications and open PRs, summarize what changed and what's blocking each, send to Telegram as 3-5 bullets

**2. Repo watch (silence-first)**

    watch [org/repo]. stay silent unless CI goes red or a new issue opens with label "bug". then message me the failing job name or the issue body, nothing else

**3. Inbox triage (hourly)**

    every hour, check my connected channels, group by sender and urgency, auto-archive newsletters, only escalate ones mentioning a deadline, a person waiting on me, or money

**4. Research digest (Friday 6pm, deduped)**

    every Friday at 6pm, search new releases and serious discussion in [topic], dedupe against last week, deliver a 5-bullet digest with links to Telegram

**5. Repo cold-start**

    clone [repo url], summarize the architecture in 5 bullets, find the main entrypoint and the single riskiest file, draft a clean PR workflow for contributing

**6. Async research handoff**

    research [question], compare top 3 options on price, limits, lock-in, send the result tonight when done. don't wait on me, make reasonable assumptions and list them at the top

**7. Competitor changelog watch (daily 9am)**

    every day at 9am, check the changelog and pricing pages of [product A], [product B], only message me when something changed: a feature, a price move, a deprecation. quote the diff

**8. Nightly code review (11pm)**

    every night at 11pm, look at today's commits and flag anything risky: a TODO left in, a console.log shipped, a function over 80 lines, a changed path with no test. short list

**9. Stand-up writer (9:55am weekdays)**

    every weekday at 9:55am, assemble my stand-up from my repos and channels: what closed, what's in progress, what's blocked, as three short bullets

**10. Mention radar (daily)**

    once a day, search for new mentions of [my project or handle] across the web and my platforms, ignore praise, escalate bug reports, complaints, and unanswered questions

**11. Talk to bullets**

    take [video or podcast url], pull the transcript, give me the argument in 5 bullets with timestamps for the parts worth watching. skip the intro and sponsor read

**12. Error explainer**

    here's a stack trace: [paste]. search my repo for the cause, explain what's failing in two sentences, draft the smallest patch that fixes it without touching anything else

**13. Inbox-zero reply drafts**

    for routine emails (scheduling, intros, status), draft a reply in my voice and hold it in a queue for my approval. never send on your own. escalate anything needing a real decision

**14. On-call diagnosis**

    when a monitoring alert fires, pull the last 50 lines of the relevant logs, check what deployed recently, and send me a one-paragraph first guess at the cause with the raw alert

**15. Point at Claude (one line)**

    hermes config set model anthropic/claude-opus-4.8

**16. Serverless backend**

    hermes config set terminal.backend daytona

**17. Make it permanent (after any good run)**

    that worked. save it as a reusable skill called "[name]" so you run it the same way next time without me re-explaining

### Install

    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
    hermes setup

### What not to do
- **Vague schedules** — "send updates on my repos" = firehose. Every scheduled prompt needs an explicit escalation rule.
- **No token budget on hourly jobs** — unbounded hourly triage can quietly spend 10x planned cost. Scope cadence and check spend in week 1.
- **Cheap local model** — drops tool calls mid-task. Fails in ways that look like prompt bugs. The model is not the place to economize.

### Which ones to keep
Your week is not everyone's week. 3 prompts tuned to your actual routine beat 17 set up once and never read. Paste all 17, keep the ones that map to work you repeat, delete the rest.
"""

with open(bp_path, "w") as f:
    f.write(content + section)
print("Updated hermes-best-practice.md")

disc = os.path.join(vault, "pending discussions/hermes-agent-17-prompts.md")
if os.path.exists(disc):
    os.remove(disc)
    print("Deleted pending discussion")
else:
    print("Pending discussion already deleted")
