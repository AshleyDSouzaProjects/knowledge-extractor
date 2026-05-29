import json

from .claude_utils import call_with_escalation

TASK = "summarizer"

SYSTEM = """You extract structured knowledge from video content. Return ONLY valid JSON:
{
  "title": "clean concise title",
  "summary": "2-3 paragraph summary of the core content and argument",
  "key_points": ["point 1", "point 2", "point 3"],
  "next_steps": ["step 1", "step 2", "step 3"],
  "tags": ["tag1", "tag2"],
  "category": "ai|tech|business|science|health|finance|education|other",
  "source_quality": "low|medium|high"
}

key_points: core insights and takeaways from the content.
next_steps: 3-7 concrete, ordered steps the viewer can take to apply or implement what was covered. If the content is purely informational with no actionable output, return an empty array.
tags: 5-10 specific, searchable terms (topics, tools, people, concepts mentioned).
Do not wrap in markdown code fences."""

REQUIRED_KEYS = {"title", "summary", "key_points", "tags"}


def summarize(
    transcript: str,
    slide_text: str,
    title: str,
    url: str,
    platform: str,
) -> dict:
    parts = [f"VIDEO TITLE: {title}", f"PLATFORM: {platform}", f"URL: {url}"]
    if transcript:
        parts.append(f"\nTRANSCRIPT:\n{transcript[:8000]}")
    if slide_text:
        parts.append(f"\nSLIDE / SCREEN CONTENT:\n{slide_text[:3000]}")

    user_msg = "Summarise this video content into structured knowledge:\n\n" + "\n".join(parts)

    def make_request(client, model):
        return client.messages.create(
            model=model,
            max_tokens=1024,
            system=SYSTEM,
            messages=[{"role": "user", "content": user_msg}],
        )

    def validate(response):
        raw = response.content[0].text.strip()
        # Strip accidental markdown fences
        if raw.startswith("```"):
            lines = raw.splitlines()
            raw = "\n".join(lines[1:])
            if raw.rstrip().endswith("```"):
                raw = raw.rstrip()[:-3].rstrip()
        data = json.loads(raw)
        missing = REQUIRED_KEYS - data.keys()
        if missing:
            raise ValueError(f"Missing keys: {missing}")
        return data

    return call_with_escalation(TASK, make_request, validate)
