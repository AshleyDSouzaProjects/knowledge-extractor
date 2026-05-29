#!/usr/bin/env python3
import sys
import warnings
from pathlib import Path
import tempfile

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
warnings.filterwarnings("ignore", message="pin_memory")

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

load_dotenv()

from skills.url_finder import URLFinderSkill
from src.downloader import download_video
from src.transcriber import transcribe
from src.screen_extractor import extract_screen_content
from src.summarizer import summarize
from src.note_writer import write_knowledge_entry, write_obsidian_note
from src.setup_wizard import needs_setup, run_setup

console = Console()


@click.command()
@click.argument("input_text", required=False)
@click.option(
    "--whisper-model",
    default="tiny",
    type=click.Choice(["tiny", "base", "small", "medium"]),
    help="Starting Whisper model (auto-escalates on low confidence).",
    show_default=True,
)
@click.option("--skip-slides", is_flag=True, help="Skip visual slide extraction (faster).")
@click.option("--metrics", is_flag=True, help="Show URL finder skill metrics and exit.")
@click.option("--setup", "run_setup_flag", is_flag=True, help="Re-run the notes destination setup wizard.")
def main(input_text, whisper_model, skip_slides, metrics, run_setup_flag):
    """Extract knowledge from a video.

    INPUT_TEXT can be a URL, tweet/email/LinkedIn text, a file path, or - to read stdin.
    """
    if run_setup_flag or needs_setup():
        run_setup()
        if run_setup_flag:
            return

    finder = URLFinderSkill()

    if metrics:
        _print_metrics(finder)
        return

    # Resolve input
    if not input_text or input_text == "-":
        console.print("[dim]Paste your content (URL, tweet, email…) then Ctrl+D:[/dim]")
        input_text = sys.stdin.read().strip()
    elif Path(input_text).exists():
        input_text = Path(input_text).read_text().strip()

    if not input_text:
        console.print("[red]No input provided.[/red]")
        raise SystemExit(1)

    console.print(Panel("[bold]Knowledge Extractor[/bold]", expand=False))

    # ── Step 1: Find video URL ────────────────────────────────────────
    with _spinner("Finding video URL…"):
        result = finder.find(input_text)

    if result.url:
        console.print(
            f"[green]✓[/green] URL found via [cyan]{result.method}[/cyan] "
            f"({result.source_type}): {result.url}"
        )
        finder.record_success(input_text, result.url, result.source_type, result.method)
    else:
        console.print("[yellow]Could not find a video URL automatically.[/yellow]")
        result.url = click.prompt("Paste the video URL")
        result.source_type = click.prompt(
            "Source type",
            default="other",
            type=click.Choice(["youtube", "twitter", "linkedin", "vimeo", "loom", "other"]),
        )
        finder.record_intervention(input_text, result.url, result.source_type)

    # Text from the original post/tweet/email, stripped of the URL
    source_text = _extract_source_text(input_text, result.url)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # ── Step 2: Download (optional — falls back to text-only) ─────
        console.print("[dim]Downloading video…[/dim]")
        meta = None
        try:
            meta = download_video(result.url, tmp)
            console.print(
                f"[green]✓[/green] Downloaded: [bold]{meta.title}[/bold] "
                f"({meta.duration // 60}m {meta.duration % 60}s)"
            )
        except Exception as e:
            console.print(f"[yellow]⚠ No video found — extracting from text only:[/yellow] {e}")

        # ── Step 3: Transcribe ────────────────────────────────────────
        transcript_text = ""
        if meta:
            est_mins = max(1, meta.duration // 600)
            console.print(
                f"[dim]Transcribing with whisper/{whisper_model} "
                f"(~{est_mins}min on CPU for a {meta.duration // 60}min video)…[/dim]"
            )
            try:
                transcript = transcribe(meta.video_path, starting_model=whisper_model)
                transcript_text = transcript.text
                console.print(
                    f"[green]✓[/green] Transcribed with whisper/{transcript.model_used} "
                    f"— {transcript.language}, avg_logprob={transcript.avg_logprob}"
                )
            except Exception as e:
                console.print(f"[yellow]⚠ Transcription failed (continuing without):[/yellow] {e}")

        # ── Step 4: Screen content ────────────────────────────────────
        slides = []
        if meta and not skip_slides:
            console.print("[dim]Scanning video frames for slide content…[/dim]")
            try:
                slides = extract_screen_content(meta.video_path)
            except Exception as e:
                console.print(f"[yellow]⚠ Slide scan failed (continuing without):[/yellow] {e}")
            label = f"{len(slides)} slide(s) detected" if slides else "no slides detected"
            console.print(f"[green]✓[/green] Screen scan: {label}")

        if not transcript_text and not source_text:
            console.print("[red]✗ No content to summarise (no video and no source text).[/red]")
            raise SystemExit(1)

        # ── Step 5: Summarise ─────────────────────────────────────────
        slide_text = "\n\n".join(s.text for s in slides)
        title = meta.title if meta else (source_text[:60].strip() or "untitled")
        platform = meta.platform if meta else result.source_type
        duration = meta.duration if meta else 0
        uploader = meta.uploader if meta else None
        upload_date = meta.upload_date if meta else None

        console.print("[dim]Summarising with Claude…[/dim]")
        try:
            summary = summarize(
                transcript=transcript_text,
                slide_text=slide_text,
                title=title,
                url=result.url,
                platform=platform,
                source_text=source_text,
            )
        except Exception as e:
            console.print(f"[red]✗ Summarisation failed:[/red] {e}")
            raise SystemExit(1)
        console.print(f"[green]✓[/green] Summarised: [bold]{summary['title']}[/bold]")

        # ── Step 6: Write outputs ─────────────────────────────────────
        try:
            entry_dir = write_knowledge_entry(
                url=result.url,
                platform=platform,
                title=title,
                duration=duration,
                transcript_text=transcript_text or source_text,
                slides=slides,
                summary=summary,
                uploader=uploader,
                upload_date=upload_date,
            )
            note_path = write_obsidian_note(
                url=result.url,
                platform=platform,
                title=title,
                duration=duration,
                summary=summary,
                entry_dir=entry_dir,
            )
        except Exception as e:
            console.print(f"[red]✗ Failed to write outputs:[/red] {e}")
            raise SystemExit(1)

    console.print()
    console.print(Panel(
        f"[bold green]Done![/bold green]\n\n"
        f"Knowledge base : {entry_dir}\n"
        f"Note           : {note_path}",
        title="Extraction complete",
        expand=False,
    ))

    console.print()
    _print_metrics(finder)


def _print_metrics(finder: URLFinderSkill):
    m = finder.get_metrics()
    if m["total"] == 0:
        return

    table = Table(title="URL Finder Skill Performance", show_header=True, header_style="bold cyan")
    table.add_column("Source", style="dim")
    table.add_column("Auto-found / Total", justify="right")
    table.add_column("Success rate", justify="right")

    table.add_row(
        "[bold]ALL[/bold]",
        f"[bold]{m['auto_found']}/{m['total']}[/bold]",
        f"[bold]{m['success_rate']}%[/bold]",
    )
    if m["by_source"]:
        table.add_section()
        for src, counts in sorted(m["by_source"].items()):
            pct = round(counts["auto"] / counts["total"] * 100, 1) if counts["total"] else 0
            table.add_row(f"  {src}", f"{counts['auto']}/{counts['total']}", f"{pct}%")

    console.print(table)


def _extract_source_text(input_text: str, url: str) -> str:
    """Return the input with URLs stripped — the surrounding post/tweet/email text."""
    import re as _re
    text = input_text.replace(url, "")
    text = _re.sub(r"https?://\S+", "", text).strip()
    return text


def _spinner(label: str):
    return Progress(SpinnerColumn(), TextColumn(label), console=console, transient=True)


if __name__ == "__main__":
    main()
