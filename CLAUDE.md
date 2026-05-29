---
## New Project Synergies — 2026-05-29
> Full analysis: `/Users/ashleydsouza/Documents/Coding_projects/NEW_PROJECTS_SYNERGY.md`

**Relevant new projects for knowledge extractor:**
- **autoresearch** — ~~Apply self-improving loop to the summarisation prompt.~~ **Decision: not proceeding.** The URL finder works because success is binary (found/not found). Summarisation quality is subjective — Haiku-as-judge optimises for a proxy metric, not actual usefulness. Risks: Goodhart's Law (prompt games the judge), verbosity creep (automated loops reward thoroughness over concision), overfitting to a 7-video test set that skews AI/tech/Twitter, and tag drift toward generic terms. The one real gap identified (missing `next_steps`) was fixed with a single targeted prompt edit in minutes — a better return than building a test harness. Prefer deliberate prompt tweaks when a specific failure is observed.
- **gtm-orchestrator** — `notion-session-log` hook; Slack stop-event notification for long extraction runs. (Not yet activated.)

---

# Knowledge Extractor — Claude Context

## What this project does
CLI tool that extracts structured knowledge from any content: video (download → transcribe → OCR slides) or text (tweets, X articles, email bodies). Handles both in the same run — combines source text + transcript + slides into a single Claude summarisation → writes a knowledge base entry and a note to Obsidian or a local folder.

## How to run
```bash
source .venv/bin/activate
python extract.py "https://..." 
python extract.py -                  # paste multi-line text, Ctrl+D to end
python extract.py path/to/file.txt
python extract.py --metrics          # show URL finder success rate
python extract.py "..." --skip-slides  # skip OCR (faster, audio-only)
python extract.py --setup            # re-run notes destination wizard
```

## Environment
- Python 3.12 via `uv`, venv at `.venv/`
- System deps: `ffmpeg` (installed via brew)
- API key: `ANTHROPIC_API_KEY` in `.env`
- All Python deps in `requirements.txt`

## Architecture

```
extract.py                  ← CLI entry point (click + rich)
resummary.py                ← re-run summariser on existing KB entries (no re-download)
skills/
  url_finder/
    extractor.py            ← self-improving URL finder skill
    patterns.json           ← regex patterns (grows automatically)
    examples.jsonl          ← few-shot examples (corrections weighted higher, gitignored)
    metrics.jsonl           ← per-run log → success rate metric (gitignored)
  model_tiers.json          ← persisted model tier per task (written at runtime, gitignored)
src/
  claude_utils.py           ← shared model ladder: Haiku → Sonnet on failure
  downloader.py             ← yt-dlp + oEmbed + Playwright fallback chain; text extraction
  transcriber.py            ← Whisper tiny→base→small (auto-escalates on logprob)
  screen_extractor.py       ← scene-change detection + EasyOCR slide extraction
  summarizer.py             ← Claude summarisation (transcript + slides + source_text)
  note_writer.py            ← writes knowledge-base/ entry + configured note destination
  setup_wizard.py           ← first-run wizard: Obsidian vault or local folder
knowledge-base/             ← one subfolder per entry (gitignored, stays local)
```

## Key design decisions

### Model ladder (cost-first)
All Claude calls start with `claude-haiku-4-5-20251001`. Escalates to `claude-sonnet-4-6` only if output fails quality check (bad JSON, missing keys, low confidence). Tier is persisted per task in `skills/model_tiers.json` so it remembers which tier worked last time.

### Whisper ladder (quality-first)
Starts at `tiny` (or `--whisper-model` override). Escalates to `base` → `small` if `avg_logprob < -1.2`. Most content is clear-speaker video so tiny is almost always sufficient.

### Self-improving URL finder
- Regex patterns tried first (fast, free)
- Claude (Haiku) used as fallback with growing few-shot examples
- When user has to manually provide a URL → logged as `intervention`, correction saved as high-priority few-shot example
- Success metric: `auto_found / total` shown after every run
- Source: `skills/url_finder/`

### Content extraction waterfall
For any URL that doesn't have a video, extraction falls through three layers:
1. **oEmbed API** (`publish.twitter.com/oembed`) — fast, no auth, returns tweet text. Result discarded if it's only a URL (bare-link tweets).
2. **Playwright headless browser** — renders JS, waits 3s for React to settle, tries `[data-testid="tweetText"]` → `article` → `main` → body. Handles X articles and any JS-rendered page. Uses `wait_until="load"` — NOT `networkidle` (X never reaches it).
3. **Fail with clear message** — tells user to use `python extract.py -` and paste content manually.

### Note destination (setup wizard)
On first run, wizard asks: Obsidian vault or local folder. Saves `NOTES_OUTPUT_TYPE` and `NOTES_OUTPUT_PATH` to `.env`. Re-run anytime with `--setup`. Obsidian mode writes to `<vault>/knowledge-extractor/<slug>.md`; folder mode writes directly to chosen folder.

### Summariser inputs
`summarize()` accepts `source_text` (original post/tweet/email text, stripped of URL), `transcript` (Whisper output), and `slide_text` (OCR). All three are optional — Claude works with whatever is available.

### Slide detection
- OpenCV scene-change detection (frame diff > 15% threshold)
- EasyOCR on changed frames
- Frames with < 10 words skipped (talking heads, empty screens)
- Near-duplicate OCR text deduplicated by hash

### Summary output fields
`title`, `summary` (2-3 paragraphs), `key_points` (insights), `next_steps` (3-7 ordered actionable steps — omitted if purely informational), `tags` (5-10 searchable terms), `category`, `source_quality`

## Output locations
- Knowledge base: `<project>/knowledge-base/<slug>/` — `transcript.md`, `slides.md`, `summary.md`, `metadata.json`
- Notes: written to path configured by setup wizard (`NOTES_OUTPUT_PATH` in `.env`); Obsidian mode uses a `knowledge-extractor/` subfolder
- Slug: ASCII-only, non-ASCII chars stripped; format `{platform}-{title-slug}-{YYYYMMDD}`
- file:// links in notes use URL-encoded paths (spaces → %20) — required for Obsidian on macOS

## GitHub
Public repo: `https://github.com/AshleyDSouzaProjects/knowledge-extractor`
- `skills/url_finder/examples.jsonl`, `metrics.jsonl`, `model_tiers.json` are gitignored (personal state)
- `knowledge-base/` is gitignored (local only)

## Logging behaviour
- `dim` info line before each slow step (what's happening + time estimate)
- `✓` on success, `✗` on hard failure, `⚠` on soft failure (slide scan — continues without)
- yt-dlp download progress shown live (not captured)
- Whisper runs silently (`verbose=None`) — no frame-by-frame progress bar
- FP16 and pin_memory warnings suppressed at startup

## What NOT to change without asking
- The `capture_output` removal on yt-dlp download — user needs to see download progress
- `verbose=None` on Whisper — the progress bar flood was explicitly removed
- URL-encoding in `note_writer.py` — required for Obsidian file:// links to work on macOS
- Playwright `wait_until="load"` + 3s wait — `networkidle` times out on X (never reaches idle)
