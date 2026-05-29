"""Extract and integrate a multi-part thread into a single knowledge base entry."""
import sys
import tempfile
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
warnings.filterwarnings("ignore", message="pin_memory")

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()

from src.downloader import download_video
from src.transcriber import transcribe
from src.screen_extractor import extract_screen_content
from src.summarizer import summarize
from src.note_writer import write_knowledge_entry, write_obsidian_note

console = Console()


@click.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--whisper-model", default="tiny",
              type=click.Choice(["tiny", "base", "small", "medium"]),
              show_default=True)
@click.option("--skip-slides", is_flag=True)
def main(urls, whisper_model, skip_slides):
    """Download, transcribe and integrate multiple URLs into one knowledge entry.

    Useful for tweet threads split across multiple posts.
    """
    console.print(Panel(f"[bold]Thread Extractor[/bold] — {len(urls)} parts", expand=False))

    all_transcripts = []
    all_slides = []
    primary_meta = None
    primary_url = urls[0]
    source_language = None

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        for i, url in enumerate(urls, 1):
            console.print(f"\n[bold cyan]Part {i}/{len(urls)}:[/bold cyan] {url}")
            part_dir = tmp / f"part{i}"
            part_dir.mkdir()

            # Download
            console.print("[dim]Downloading…[/dim]")
            try:
                meta = download_video(url, part_dir)
                console.print(f"[green]✓[/green] {meta.title} ({meta.duration // 60}m {meta.duration % 60}s)")
                if primary_meta is None:
                    primary_meta = meta
            except Exception as e:
                console.print(f"[yellow]⚠ Download failed (skipping part {i}):[/yellow] {e}")
                continue

            # Transcribe
            est = max(1, meta.duration // 600)
            console.print(f"[dim]Transcribing (~{est}min)…[/dim]")
            try:
                transcript = transcribe(meta.video_path, starting_model=whisper_model)
                all_transcripts.append(f"[Part {i}]\n{transcript.text}")
                if source_language is None:
                    source_language = transcript.language
                console.print(f"[green]✓[/green] {transcript.language}, avg_logprob={transcript.avg_logprob}")
            except Exception as e:
                console.print(f"[yellow]⚠ Transcription failed:[/yellow] {e}")

            # Slides
            if not skip_slides:
                console.print("[dim]Scanning slides…[/dim]")
                try:
                    slides = extract_screen_content(meta.video_path)
                    if slides:
                        all_slides.extend(slides)
                        console.print(f"[green]✓[/green] {len(slides)} slide(s)")
                    else:
                        console.print("[green]✓[/green] no slides")
                except Exception as e:
                    console.print(f"[yellow]⚠ Slide scan failed:[/yellow] {e}")

        if not all_transcripts and not all_slides:
            console.print("[red]✗ No content extracted from any part.[/red]")
            raise SystemExit(1)

        # Combine and summarise
        combined_transcript = "\n\n---\n\n".join(all_transcripts)
        slide_text = "\n\n".join(s.text for s in all_slides)
        title = primary_meta.title if primary_meta else "Thread"
        platform = primary_meta.platform if primary_meta else "twitter"
        duration = sum(0 for _ in urls)  # placeholder

        console.print("\n[dim]Summarising combined content…[/dim]")
        try:
            summary = summarize(
                transcript=combined_transcript,
                slide_text=slide_text,
                title=title,
                url=primary_url,
                platform=platform,
                source_text=f"Multi-part thread ({len(urls)} parts): " + ", ".join(urls),
            )
        except Exception as e:
            console.print(f"[red]✗ Summarisation failed:[/red] {e}")
            raise SystemExit(1)
        console.print(f"[green]✓[/green] Summarised: [bold]{summary['title']}[/bold]")

        # Write outputs
        total_duration = primary_meta.duration if primary_meta else 0
        try:
            entry_dir = write_knowledge_entry(
                url=primary_url,
                platform=platform,
                title=title,
                duration=total_duration,
                transcript_text=combined_transcript,
                slides=all_slides,
                summary=summary,
                uploader=primary_meta.uploader if primary_meta else None,
                upload_date=primary_meta.upload_date if primary_meta else None,
                source_language=source_language,
            )
            note_path = write_obsidian_note(
                url=primary_url,
                platform=platform,
                title=title,
                duration=total_duration,
                summary=summary,
                entry_dir=entry_dir,
                source_language=source_language,
            )
        except Exception as e:
            console.print(f"[red]✗ Failed to write outputs:[/red] {e}")
            raise SystemExit(1)

    console.print()
    console.print(Panel(
        f"[bold green]Done![/bold green]\n\n"
        f"Parts processed : {len(all_transcripts)}/{len(urls)}\n"
        f"Knowledge base  : {entry_dir}\n"
        f"Note            : {note_path}",
        title="Thread extraction complete",
        expand=False,
    ))


if __name__ == "__main__":
    main()
