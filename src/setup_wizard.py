"""First-run setup wizard: configure where notes are written."""
import os
import re
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()

ENV_FILE = Path(__file__).parent.parent / ".env"
_OBSIDIAN_ICLOUD = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents"


def needs_setup() -> bool:
    return not os.environ.get("NOTES_OUTPUT_PATH")


def run_setup():
    console.print()
    console.print(Panel(
        "[bold]First-time setup[/bold]\n\n"
        "Where should extracted notes be saved?",
        expand=False,
    ))
    console.print()

    output_type = click.prompt(
        "Notes destination",
        type=click.Choice(["obsidian", "folder"], case_sensitive=False),
        default="obsidian",
        show_choices=True,
    )

    if output_type == "obsidian":
        default_vault = _detect_obsidian_vault()
        if default_vault:
            console.print(f"[dim]Detected Obsidian vault at: {default_vault}[/dim]")
        vault_path = click.prompt(
            "Obsidian vault path",
            default=str(default_vault) if default_vault else "",
        )
        notes_path = Path(vault_path).expanduser().resolve()
    else:
        default_folder = Path.home() / "knowledge-extractor-notes"
        notes_path_str = click.prompt(
            "Folder path for notes",
            default=str(default_folder),
        )
        notes_path = Path(notes_path_str).expanduser().resolve()

    if not notes_path.exists():
        if click.confirm(f"  {notes_path} does not exist. Create it?", default=True):
            notes_path.mkdir(parents=True)
            console.print(f"[green]✓[/green] Created {notes_path}")
        else:
            console.print("[red]Setup cancelled.[/red]")
            raise SystemExit(1)

    _save_to_env("NOTES_OUTPUT_TYPE", output_type)
    _save_to_env("NOTES_OUTPUT_PATH", str(notes_path))

    # Update os.environ so the rest of this run picks it up immediately
    os.environ["NOTES_OUTPUT_TYPE"] = output_type
    os.environ["NOTES_OUTPUT_PATH"] = str(notes_path)

    console.print()
    console.print(f"[green]✓[/green] Saved to .env — notes will go to [bold]{notes_path}[/bold]")
    console.print(Rule(style="dim"))
    console.print()


def _detect_obsidian_vault() -> Path | None:
    if _OBSIDIAN_ICLOUD.exists():
        vaults = [p for p in _OBSIDIAN_ICLOUD.iterdir() if p.is_dir() and not p.name.startswith(".")]
        if len(vaults) == 1:
            return vaults[0]
        if vaults:
            return _OBSIDIAN_ICLOUD  # multiple vaults — return parent, let user specify
    return None


def _save_to_env(key: str, value: str):
    if ENV_FILE.exists():
        text = ENV_FILE.read_text()
    else:
        text = ""

    pattern = re.compile(rf"^{re.escape(key)}\s*=.*$", re.MULTILINE)
    line = f'{key}="{value}"'
    if pattern.search(text):
        text = pattern.sub(line, text)
    else:
        text = text.rstrip("\n") + ("\n" if text else "") + line + "\n"

    ENV_FILE.write_text(text)
