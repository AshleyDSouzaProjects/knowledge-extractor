import json
import subprocess
from dataclasses import dataclass
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


def _fetch_info(url: str) -> dict:
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-playlist", url],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp info failed: {result.stderr[:500]}")
    return json.loads(result.stdout)
