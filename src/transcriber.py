import subprocess
from dataclasses import dataclass
from pathlib import Path

import whisper

WHISPER_LADDER = ["tiny", "base", "small"]
MIN_AVG_LOGPROB = -1.2  # escalate if mean segment confidence is below this


@dataclass
class Transcript:
    text: str
    segments: list
    model_used: str
    language: str
    avg_logprob: float


def transcribe(video_path: Path, starting_model: str = "tiny") -> Transcript:
    audio_path = _extract_audio(video_path)

    try:
        start_idx = WHISPER_LADDER.index(starting_model)
    except ValueError:
        start_idx = 0

    last_result = None
    for model_name in WHISPER_LADDER[start_idx:]:
        model = whisper.load_model(model_name)
        result = model.transcribe(str(audio_path), verbose=None)

        segments = result.get("segments", [])
        avg_lp = (
            sum(s.get("avg_logprob", -1.0) for s in segments) / len(segments)
            if segments
            else -1.0
        )
        last_result = (result, model_name, avg_lp)

        if avg_lp >= MIN_AVG_LOGPROB:
            break  # quality is good enough

    audio_path.unlink(missing_ok=True)
    result, model_name, avg_lp = last_result
    return Transcript(
        text=result["text"].strip(),
        segments=result.get("segments", []),
        model_used=model_name,
        language=result.get("language", "en"),
        avg_logprob=round(avg_lp, 3),
    )


def _extract_audio(video_path: Path) -> Path:
    audio_path = video_path.with_suffix(".wav")
    subprocess.run(
        [
            "ffmpeg", "-i", str(video_path),
            "-ac", "1", "-ar", "16000",
            "-y", str(audio_path),
        ],
        capture_output=True,
        check=True,
    )
    return audio_path
