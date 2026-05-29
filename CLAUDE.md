# Knowledge Extractor — Claude Context

## What this project does
CLI tool that takes a URL, tweet, email body, or LinkedIn post → finds the video link → downloads, transcribes, extracts slide content, summarises with Claude → writes a structured knowledge base entry and an Obsidian note.

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
skills/
  url_finder/
    extractor.py            ← self-improving URL finder skill
    patterns.json           ← regex patterns (grows automatically)
    examples.jsonl          ← few-shot examples (corrections weighted higher)
    metrics.jsonl           ← per-run log → success rate metric
  model_tiers.json          ← persisted model tier per task (written at runtime)
src/
  claude_utils.py           ← shared model ladder: Haiku → Sonnet on failure
  downloader.py             ← yt-dlp wrapper (live progress, 30min timeout)
  transcriber.py            ← Whisper tiny→base→small (auto-escalates on logprob)
  screen_extractor.py       ← scene-change detection + EasyOCR slide extraction
  summarizer.py             ← Claude summarisation
  note_writer.py            ← writes knowledge-base/ entry + Obsidian note
knowledge-base/             ← one subfolder per video (gitignored, stays local)
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

### Slide detection
- OpenCV scene-change detection (frame diff > 15% threshold)
- EasyOCR on changed frames
- Frames with < 10 words skipped (talking heads, empty screens)
- Near-duplicate OCR text deduplicated by hash

## Output locations
- Knowledge base: `<project>/knowledge-base/<slug>/` with `transcript.md`, `slides.md`, `summary.md`, `metadata.json`
- Notes: written to path configured by setup wizard (`NOTES_OUTPUT_PATH` in `.env`); Obsidian mode uses a `knowledge-extractor/` subfolder
- file:// links in notes use URL-encoded paths (spaces → %20) — required for Obsidian on macOS

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
