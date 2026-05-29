import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.claude_utils import MODELS, call_with_escalation, load_tier, save_tier

SKILL_DIR = Path(__file__).parent
EXAMPLES_FILE = SKILL_DIR / "examples.jsonl"
METRICS_FILE = SKILL_DIR / "metrics.jsonl"
PATTERNS_FILE = SKILL_DIR / "patterns.json"

TASK = "url_finder"
MIN_CONFIDENCE = 0.6


@dataclass
class FindResult:
    url: Optional[str]
    source_type: Optional[str]
    method: str  # "regex" | "claude" | "failed"
    confidence: float


class URLFinderSkill:
    def __init__(self):
        self.patterns = json.loads(PATTERNS_FILE.read_text())
        EXAMPLES_FILE.touch()
        METRICS_FILE.touch()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def find(self, raw_text: str) -> FindResult:
        url, source_type = self._try_regex(raw_text)
        if url:
            return FindResult(url=url, source_type=source_type, method="regex", confidence=1.0)
        return self._try_claude(raw_text)

    def record_success(self, raw_text: str, url: str, source_type: Optional[str], method: str):
        self._log_metric(auto_found=True, source_type=source_type or "unknown", url=url)
        if method == "claude":
            self._add_example(raw_text, url, source_type or "unknown", kind="auto")

    def record_intervention(self, raw_text: str, corrected_url: str, source_type: str):
        self._log_metric(auto_found=False, source_type=source_type, url=corrected_url)
        self._add_example(raw_text, corrected_url, source_type, kind="correction")

    def get_metrics(self) -> dict:
        if not METRICS_FILE.exists() or METRICS_FILE.stat().st_size == 0:
            return {"total": 0, "auto_found": 0, "interventions": 0, "success_rate": 0.0, "by_source": {}}

        records = [json.loads(l) for l in METRICS_FILE.read_text().strip().splitlines() if l]
        total = len(records)
        auto = sum(1 for r in records if r["auto_found"])
        by_source: dict = {}
        for r in records:
            st = r.get("source_type", "unknown")
            bucket = by_source.setdefault(st, {"total": 0, "auto": 0})
            bucket["total"] += 1
            if r["auto_found"]:
                bucket["auto"] += 1

        return {
            "total": total,
            "auto_found": auto,
            "interventions": total - auto,
            "success_rate": round(auto / total * 100, 1) if total else 0.0,
            "by_source": by_source,
        }

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _try_regex(self, text: str) -> tuple[Optional[str], Optional[str]]:
        for source_type, pattern_list in self.patterns.items():
            for pattern in pattern_list:
                m = re.search(pattern, text, re.IGNORECASE)
                if m:
                    return m.group(0), source_type
        return None, None

    def _try_claude(self, text: str) -> FindResult:
        examples = self._load_examples(limit=6)
        few_shot = ""
        if examples:
            lines = []
            for ex in examples:
                lines.append(f'Input snippet: "{ex["input_snippet"][:200]}"')
                lines.append(f'Extracted URL: {ex["url"]} (type: {ex["source_type"]})\n')
            few_shot = "Prior successful extractions for context:\n" + "\n".join(lines) + "\n"

        system = (
            "You are a video URL extractor. Given text from social media, email, or web content, "
            "find the primary video URL. Return ONLY valid JSON:\n"
            '{"url": "<url or null>", "source_type": "<youtube|twitter|linkedin|vimeo|loom|other|null>", "confidence": 0.0-1.0}\n'
            "If no video URL is present, return: "
            '{"url": null, "source_type": null, "confidence": 0.0}'
        )
        user_msg = f"{few_shot}Input text:\n{text[:2000]}"

        def make_request(client, model):
            return client.messages.create(
                model=model,
                max_tokens=200,
                system=system,
                messages=[{"role": "user", "content": user_msg}],
            )

        def validate(response):
            raw = response.content[0].text.strip()
            data = json.loads(raw)
            url = data.get("url")
            confidence = float(data.get("confidence", 0.0))
            if not url or confidence < MIN_CONFIDENCE:
                raise ValueError(f"low confidence: {confidence}")
            return data

        try:
            data = call_with_escalation(TASK, make_request, validate)
            return FindResult(
                url=data["url"],
                source_type=data.get("source_type"),
                method="claude",
                confidence=float(data.get("confidence", 0.8)),
            )
        except Exception:
            return FindResult(url=None, source_type=None, method="failed", confidence=0.0)

    def _load_examples(self, limit: int = 6) -> list:
        if not EXAMPLES_FILE.exists() or EXAMPLES_FILE.stat().st_size == 0:
            return []
        records = [json.loads(l) for l in EXAMPLES_FILE.read_text().strip().splitlines() if l]
        corrections = [r for r in records if r.get("kind") == "correction"]
        autos = [r for r in records if r.get("kind") == "auto"]
        # Corrections are more valuable — always include the latest ones first
        combined = corrections[-3:] + autos[-(max(limit - 3, 1)):]
        return combined[-limit:]

    def _add_example(self, raw_text: str, url: str, source_type: str, kind: str):
        entry = {
            "input_snippet": raw_text[:500],
            "url": url,
            "source_type": source_type,
            "kind": kind,
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        with EXAMPLES_FILE.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def _log_metric(self, auto_found: bool, source_type: str, url: str):
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "auto_found": auto_found,
            "source_type": source_type,
            "url": url,
        }
        with METRICS_FILE.open("a") as f:
            f.write(json.dumps(entry) + "\n")
