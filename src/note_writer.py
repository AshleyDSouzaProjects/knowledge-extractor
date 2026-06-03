import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import quote

KNOWLEDGE_BASE = Path(__file__).parent.parent / "knowledge-base"


def _notes_dir(slug: str) -> Path:
    output_type = os.environ.get("NOTES_OUTPUT_TYPE", "folder")
    base = Path(os.environ.get("NOTES_OUTPUT_PATH", str(Path.home() / "knowledge-extractor-notes")))
    if output_type == "obsidian":
        return base / "knowledge-extractor"
    return base


_PLATFORM_CONFIDENCE = {
    "twitter": "claimed",
    "linkedin": "claimed",
    "youtube": "claimed",
    "substack": "claimed",
    "instagram": "claimed",
    "tiktok": "claimed",
    "facebook": "claimed",
    "reddit": "claimed",
}

def _confidence_from_platform(platform: str) -> str:
    return _PLATFORM_CONFIDENCE.get(platform.lower(), "raw")


_LANG_NAMES = {
    "af": "Afrikaans", "ar": "Arabic", "zh": "Chinese", "cs": "Czech",
    "da": "Danish", "nl": "Dutch", "fi": "Finnish", "fr": "French",
    "de": "German", "el": "Greek", "hi": "Hindi", "hu": "Hungarian",
    "id": "Indonesian", "it": "Italian", "ja": "Japanese", "ko": "Korean",
    "ms": "Malay", "no": "Norwegian", "fa": "Persian", "pl": "Polish",
    "pt": "Portuguese", "ro": "Romanian", "ru": "Russian", "es": "Spanish",
    "sv": "Swedish", "ta": "Tamil", "te": "Telugu", "th": "Thai",
    "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu", "vi": "Vietnamese",
}


def _translation_note(language: Optional[str]) -> str:
    if not language or language == "en":
        return ""
    name = _LANG_NAMES.get(language, language.upper())
    return f"> *Translated from {name} to English*\n\n"


def write_knowledge_entry(
    url: str,
    platform: str,
    title: str,
    duration: int,
    transcript_text: str,
    slides: list,
    summary: dict,
    uploader: Optional[str] = None,
    upload_date: Optional[str] = None,
    source_language: Optional[str] = None,
) -> Path:
    slug = _make_slug(platform, title)
    entry_dir = KNOWLEDGE_BASE / slug
    entry_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "url": url,
        "platform": platform,
        "title": title,
        "duration_seconds": duration,
        "uploader": uploader,
        "upload_date": upload_date,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "tags": summary.get("tags", []),
        "category": summary.get("category", "other"),
        "source_quality": summary.get("source_quality", "medium"),
        "slug": slug,
    }
    (entry_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

    if transcript_text:
        heading = "Transcript" if duration > 0 else "Source Text"
        (entry_dir / "transcript.md").write_text(
            f"# {heading}: {title}\n\n> Source: {url}\n\n{transcript_text}\n"
        )
    else:
        (entry_dir / "transcript.md").write_text("# Transcript\n\n_No transcript available._\n")

    if slides:
        parts = [f"# Slide Content: {title}\n\n> Source: {url}\n"]
        for s in slides:
            m, sec = divmod(int(s.timestamp), 60)
            parts.append(f"## [{m:02d}:{sec:02d}]\n\n{s.text}\n")
        (entry_dir / "slides.md").write_text("\n".join(parts))
    else:
        (entry_dir / "slides.md").write_text("# Slides\n\n_No slide content detected._\n")

    kp_lines = "".join(f"- {p}\n" for p in summary.get("key_points", []))
    ns_lines = "".join(f"{i}. {s}\n" for i, s in enumerate(summary.get("next_steps", []), 1))
    tag_line = " ".join(f"#{t.replace(' ', '-')}" for t in summary.get("tags", []))
    next_steps_section = f"## What To Do Next\n\n{ns_lines}\n" if ns_lines else ""
    (entry_dir / "summary.md").write_text(
        f"# Summary: {title}\n\n"
        f"> Source: {url}\n"
        f"> Platform: {platform} | Duration: {f'{duration // 60}m {duration % 60}s' if duration else 'text only'}\n\n"
        f"{_translation_note(source_language)}"
        f"## Overview\n\n{summary.get('summary', '')}\n\n"
        f"## Key Points\n\n{kp_lines}\n"
        f"{next_steps_section}"
        f"## Tags\n\n{tag_line}\n"
    )

    return entry_dir


def write_obsidian_note(
    url: str,
    platform: str,
    title: str,
    duration: int,
    summary: dict,
    entry_dir: Path,
    source_language: Optional[str] = None,
) -> Path:
    notes_dir = _notes_dir(entry_dir.name)
    notes_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    tags_yaml = "\n".join(
        f"  - {t.replace(' ', '-')}" for t in summary.get("tags", [])
    )
    category = summary.get("category", "other")
    kb_path = entry_dir.resolve()
    kb_uri = "file://" + quote(str(kb_path), safe="/:")
    kp_lines = "".join(f"- {p}\n" for p in summary.get("key_points", []))
    ns_lines = "".join(f"{i}. {s}\n" for i, s in enumerate(summary.get("next_steps", []), 1))
    next_steps_section = f"## What To Do Next\n\n{ns_lines}\n" if ns_lines else ""

    confidence = _confidence_from_platform(platform)
    note = (
        f"---\n"
        f"tags:\n"
        f"  - knowledge-extractor\n"
        f"  - {category}\n"
        f"{tags_yaml}\n"
        f"source: \"{url}\"\n"
        f"platform: \"{platform}\"\n"
        f"date: \"{date_str}\"\n"
        f"duration: \"{f'{duration // 60}m {duration % 60}s' if duration else 'text only'}\"\n"
        f"confidence: \"{confidence}\"\n"
        f"---\n\n"
        f"# {summary.get('title', title)}\n\n"
        f"{_translation_note(source_language)}"
        f"## Summary\n\n{summary.get('summary', '')}\n\n"
        f"## Key Points\n\n{kp_lines}\n"
        f"{next_steps_section}"
        f"## Source\n\n"
        f"[Original Source]({url})\n\n"
        f"## Full Knowledge Base\n\n"
        f"- [Transcript]({kb_uri}/transcript.md)\n"
        f"- [Slides]({kb_uri}/slides.md)\n"
        f"- [Raw Summary]({kb_uri}/summary.md)\n"
        f"- [Metadata]({kb_uri}/metadata.json)\n"
    )

    note_path = notes_dir / f"{entry_dir.name}.md"
    note_path.write_text(note)
    return note_path


def _make_slug(platform: str, title: str) -> str:
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    ascii_title = title.encode("ascii", "ignore").decode("ascii")
    clean = re.sub(r"https?://\S+", "", ascii_title)   # strip embedded URLs
    clean = re.sub(r"[^\w\s-]", "", clean.lower().strip())
    clean = re.sub(r"[\s_-]+", "-", clean)[:50].strip("-")
    return f"{platform}-{clean}-{date_str}"
