import json
import re
import subprocess
import urllib.request
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Optional


@dataclass
class VideoMeta:
    url: str
    title: str
    platform: str
    duration: int  # seconds
    video_path: Path
    uploader: Optional[str] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None


def download_video(url: str, output_dir: Path) -> VideoMeta:
    output_dir.mkdir(parents=True, exist_ok=True)

    info = _fetch_info(url)
    title = info.get("title", "untitled")
    platform = info.get("extractor_key", "unknown").lower()
    duration = int(info.get("duration") or 0)
    uploader = info.get("uploader")
    upload_date = info.get("upload_date")
    description = (info.get("description") or "")[:1000]

    output_template = str(output_dir / "video.%(ext)s")
    # Run without capturing output so yt-dlp progress prints live to terminal
    result = subprocess.run(
        [
            "yt-dlp",
            "-f", "bestvideo[height<=1080]+bestaudio/best",
            "--merge-output-format", "mp4",
            "-o", output_template,
            "--no-playlist",
            "--newline",  # one progress line per update, easier to read
            url,
        ],
        timeout=1800,  # 30 min ceiling for large videos
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp download failed (exit code {result.returncode})")

    video_files = list(output_dir.glob("video.*"))
    if not video_files:
        raise RuntimeError("Download completed but no video file found")

    return VideoMeta(
        url=url,
        title=title,
        platform=platform,
        duration=duration,
        video_path=video_files[0],
        uploader=uploader,
        upload_date=upload_date,
        description=description,
    )


def fetch_tweet_text(url: str) -> str:
    """Fetch tweet text via the public oEmbed API (no auth required)."""
    try:
        api_url = f"https://publish.twitter.com/oembed?url={url}"
        with urllib.request.urlopen(api_url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        html = data.get("html", "")
        match = re.search(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
        if not match:
            return ""
        text = match.group(1)
        text = re.sub(r"<a[^>]*>(.*?)</a>", r"\1", text)  # links → link text
        text = re.sub(r"<[^>]+>", "", text)                # strip remaining tags
        text = unescape(text).strip()
        # Discard if the only content is a URL (bare link tweet with no text)
        if re.match(r"^https?://\S+$", text):
            return ""
        return text
    except Exception:
        return ""


def fetch_page_text(url: str) -> str:
    """Render the page in a headless browser and extract visible text."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ""

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="load", timeout=30000)
            page.wait_for_timeout(3000)  # allow JS to render content

            # Try specific content selectors first
            for selector in ["[data-testid='tweetText']", "article", "main"]:
                els = page.query_selector_all(selector)
                if els:
                    text = "\n\n".join(el.inner_text() for el in els).strip()
                    if len(text) > 100:
                        browser.close()
                        return text

            # Generic fallback: full body text
            text = page.inner_text("body").strip()
            browser.close()
            return text if len(text) > 100 else ""
    except Exception:
        return ""


def _fetch_info(url: str) -> dict:
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-playlist", url],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp info failed: {result.stderr[:500]}")
    # stdout may contain one JSON object per line (multi-video threads/carousels)
    return json.loads(result.stdout.splitlines()[0])
