from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

MIN_WORDS_FOR_SLIDE = 10
SCENE_DIFF_THRESHOLD = 0.15  # fraction of pixels that changed
SAMPLE_EVERY_SECONDS = 2

_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(["en"], verbose=False)
    return _reader


@dataclass
class SlideContent:
    timestamp: float
    text: str
    word_count: int


def extract_screen_content(video_path: Path) -> list[SlideContent]:
    try:
        _get_reader()
    except Exception:
        return []

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_step = max(1, int(fps * SAMPLE_EVERY_SECONDS))

    slides: list[SlideContent] = []
    prev_gray = None
    prev_text_hash = None
    frame_idx = 0

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = frame_idx / fps
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is None:
            scene_changed = True
        else:
            diff = cv2.absdiff(prev_gray, gray)
            changed_ratio = np.count_nonzero(diff > 30) / diff.size
            scene_changed = changed_ratio > SCENE_DIFF_THRESHOLD

        if scene_changed:
            reader = _get_reader()
            ocr_results = reader.readtext(frame, detail=0, paragraph=True)
            text = " ".join(ocr_results).strip()
            word_count = len(text.split())

            if word_count >= MIN_WORDS_FOR_SLIDE:
                text_hash = hash(text[:120])
                if text_hash != prev_text_hash:
                    slides.append(SlideContent(
                        timestamp=round(timestamp, 1),
                        text=text,
                        word_count=word_count,
                    ))
                    prev_text_hash = text_hash

        prev_gray = gray
        frame_idx += frame_step

    cap.release()
    return slides
