"""Re-summarise existing knowledge base entries using updated summarizer."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from src.summarizer import summarize
from src.note_writer import KNOWLEDGE_BASE, write_obsidian_note
from datetime import datetime, timezone
from urllib.parse import quote

def resummary_entry(entry_dir: Path):
    meta = json.loads((entry_dir / "metadata.json").read_text())
    transcript_raw = (entry_dir / "transcript.md").read_text()
    slides_raw = (entry_dir / "slides.md").read_text()

    # Strip headers added by note_writer
    transcript_text = "\n".join(transcript_raw.splitlines()[3:]).strip()
    slide_text = "\n".join(slides_raw.splitlines()[3:]).strip()

    print(f"Re-summarising: {entry_dir.name}")
    summary = summarize(
        transcript=transcript_text,
        slide_text=slide_text,
        title=meta["title"],
        url=meta["url"],
        platform=meta["platform"],
    )

    # Rewrite summary.md
    duration = meta["duration_seconds"]
    kp_lines = "".join(f"- {p}\n" for p in summary.get("key_points", []))
    ns_lines = "".join(f"{i}. {s}\n" for i, s in enumerate(summary.get("next_steps", []), 1))
    tag_line = " ".join(f"#{t.replace(' ', '-')}" for t in summary.get("tags", []))
    next_steps_section = f"## What To Do Next\n\n{ns_lines}\n" if ns_lines else ""
    (entry_dir / "summary.md").write_text(
        f"# Summary: {meta['title']}\n\n"
        f"> Source: {meta['url']}\n"
        f"> Platform: {meta['platform']} | Duration: {duration // 60}m {duration % 60}s\n\n"
        f"## Overview\n\n{summary.get('summary', '')}\n\n"
        f"## Key Points\n\n{kp_lines}\n"
        f"{next_steps_section}"
        f"## Tags\n\n{tag_line}\n"
    )

    # Update metadata tags/category/source_quality
    meta["tags"] = summary.get("tags", meta["tags"])
    meta["category"] = summary.get("category", meta.get("category", "other"))
    meta["source_quality"] = summary.get("source_quality", meta.get("source_quality", "medium"))
    (entry_dir / "metadata.json").write_text(json.dumps(meta, indent=2))

    # Rewrite Obsidian note
    write_obsidian_note(
        url=meta["url"],
        platform=meta["platform"],
        title=meta["title"],
        duration=duration,
        summary=summary,
        entry_dir=entry_dir,
    )

    print(f"  ✓ Done — {len(summary.get('next_steps', []))} next steps written")


if __name__ == "__main__":
    entries = sorted(KNOWLEDGE_BASE.iterdir()) if len(sys.argv) == 1 else [KNOWLEDGE_BASE / sys.argv[1]]
    for entry in entries:
        if entry.is_dir():
            resummary_entry(entry)
