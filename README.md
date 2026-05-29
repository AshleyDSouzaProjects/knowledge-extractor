# Knowledge Extractor

Paste a URL, tweet, email, or LinkedIn post — extracts knowledge from videos (download + transcribe + OCR slides) or text-only content (tweets, articles, X Notes). Summarises with Claude and writes a structured note to your Obsidian vault or a local folder.

## Prerequisites

- Python 3.12+
- [ffmpeg](https://ffmpeg.org/) — `brew install ffmpeg` on Mac
- An [Anthropic API key](https://console.anthropic.com/)

> **Note:** First install pulls in `torch`, `whisper`, and `easyocr` — expect ~2–3 GB and several minutes. Transcription runs on CPU by default (~1 min per 10 min of video).

## Setup

```bash
git clone <repo-url>
cd knowledge-extractor

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium    # headless browser for text-only pages (~300MB)

cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

On the first run, a setup wizard will ask where to save notes — either your Obsidian vault or any local folder. The choice is saved to `.env` and remembered for all future runs.

## Usage

```bash
python extract.py "https://..."              # URL or tweet
python extract.py -                          # paste multi-line text, Ctrl+D to end
python extract.py path/to/file.txt           # text file containing a URL

python extract.py "..." --skip-slides        # skip OCR (faster, audio only)
python extract.py --metrics                  # show URL-finder success rate
python extract.py --setup                    # change notes destination
```

## Output

For each video, two things are written:

**Local knowledge base** (`knowledge-base/<slug>/`):
- `transcript.md` — full transcript
- `slides.md` — OCR'd slide content with timestamps
- `summary.md` — overview, key points, next steps, tags
- `metadata.json` — source metadata

**Note** (Obsidian vault or folder you chose at setup):
- A single `.md` file with frontmatter, summary, key points, and what-to-do-next steps, linked back to the local knowledge base.

## Re-run setup

```bash
python extract.py --setup
```
