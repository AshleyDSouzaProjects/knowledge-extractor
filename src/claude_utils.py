import json
from pathlib import Path
import anthropic

MODELS = ["claude-haiku-4-5-20251001", "claude-sonnet-4-6"]
TIERS_FILE = Path(__file__).parent.parent / "skills" / "model_tiers.json"


def load_tier(task: str) -> int:
    try:
        return json.loads(TIERS_FILE.read_text()).get(task, 0)
    except Exception:
        return 0


def save_tier(task: str, tier_index: int):
    try:
        data = {}
        if TIERS_FILE.exists():
            data = json.loads(TIERS_FILE.read_text())
        data[task] = tier_index
        TIERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        TIERS_FILE.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


def call_with_escalation(task: str, make_request, validate_response):
    """Call Claude starting from the persisted tier for this task.

    make_request(client, model) -> raw API response
    validate_response(response) -> parsed result, or raise on bad quality
    """
    client = anthropic.Anthropic()
    tier = load_tier(task)

    last_exc = None
    for i, model in enumerate(MODELS[tier:], start=tier):
        try:
            response = make_request(client, model)
            result = validate_response(response)
            save_tier(task, i)
            return result
        except Exception as exc:
            last_exc = exc
            continue

    raise RuntimeError(f"All models failed for task '{task}'") from last_exc
