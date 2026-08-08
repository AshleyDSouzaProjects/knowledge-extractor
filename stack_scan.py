"""Full-machine stack scan.

Walks every project root and harvests, per project:
  - declared dependencies (package.json, requirements*.txt, pyproject.toml, Gemfile, go.mod)
  - .env / .env.example KEY NAMES ONLY  (values are never read or stored)
  - SaaS / service / model / tool mentions matched against a controlled vocabulary
  - languages present, repo size, last-modified

SECURITY: .env handling splits on the first '=' and keeps only the left side. No secret
value is ever read into memory, printed, or written to the report.

Output: stack_scan_report.json + a compact per-project markdown digest.
"""

import json
import os
import re
from datetime import datetime, timezone

ROOTS = [
    "/Users/ashleydsouza/Documents/Coding_projects",
    "/Users/ashleydsouza/Documents/Personal",
]

SKIP_DIRS = {
    "node_modules", ".venv", "venv", ".git", "__pycache__", ".next", "dist",
    "build", ".pytest_cache", ".mypy_cache", "site-packages", ".turbo",
    "coverage", ".cache", "target", ".ruff_cache", "vendor", ".idea",
}

TEXT_EXT = {".md", ".txt", ".json", ".py", ".js", ".ts", ".tsx", ".jsx", ".sh",
            ".yml", ".yaml", ".toml", ".cfg", ".ini", ".html", ".env", ".sql",
            ".mjs", ".cjs"}

MAX_FILE_BYTES = 400_000

# ---------------------------------------------------------------- vocabulary

VOCAB = {
    "AI models / providers": [
        "claude-opus", "claude-sonnet", "claude-haiku", "claude-3-5-sonnet",
        "gpt-5.5", "gpt-5.4", "gpt-5", "gpt-4o", "gpt-4.1", "o3-mini",
        "gemini-2.5", "gemini-2.0", "gemini-1.5", "gemini-embedding",
        "qwen2.5-coder", "qwen3", "qwen", "deepseek", "llama-3.3", "llama3",
        "mistral", "mixtral", "nomic-embed", "whisper", "stable-diffusion",
        "text-embedding-3", "voyage", "cohere", "grok", "kimi", "glm-",
    ],
    "AI infra / runtime": [
        "ollama", "mlx", "llama.cpp", "llama-server", "vllm", "transformers",
        "sentence-transformers", "torch", "onnx", "openrouter", "groq",
        "together.ai", "replicate", "huggingface", "modal.com", "runpod",
        "bedrock", "vertex ai", "azure openai",
    ],
    "Agent frameworks / SDKs": [
        "anthropic", "openai", "google-generativeai", "google-genai",
        "langchain", "langgraph", "crewai", "autogen", "llamaindex",
        "@anthropic-ai/sdk", "agent sdk", "managed agents", "mcp",
        "claude code", "codex", "smolagents", "pydantic-ai", "dspy",
    ],
    "Databases / storage": [
        "postgres", "postgresql", "pgvector", "pglite", "sqlite",
        "better-sqlite3", "supabase", "lancedb", "pinecone", "weaviate",
        "chroma", "qdrant", "neo4j", "redis", "mongodb", "duckdb",
        "airtable", "notion", "firebase", "dynamodb", "s3", "r2",
    ],
    "Hosting / infra": [
        "vercel", "cloudflare", "netlify", "railway", "render.com", "fly.io",
        "oracle cloud", "aws", "gcp", "azure", "digitalocean", "heroku",
        "docker", "kubernetes", "launchd", "crontab", "cron", "pm2",
        "systemd", "nginx", "caddy", "argo cd", "terraform",
    ],
    "Comms / messaging": [
        "twilio", "vapi", "brevo", "resend", "sendgrid", "mailgun", "postmark",
        "slack", "telegram", "whatsapp", "baileys", "elevenlabs", "deepgram",
        "livekit", "retell", "discord", "intercom",
    ],
    "Payments / billing": [
        "stripe", "razorpay", "paddle", "lemonsqueezy", "chargebee",
    ],
    "Scraping / browser": [
        "playwright", "patchright", "puppeteer", "selenium", "apify",
        "firecrawl", "jina", "beautifulsoup", "scrapy", "yt-dlp", "gosom",
        "browserbase", "crawl4ai", "requests", "httpx", "cheerio",
    ],
    "Docs / media": [
        "pymupdf", "fitz", "tesseract", "easyocr", "opencv", "pandoc",
        "python-pptx", "libreoffice", "docling", "pdfplumber", "sharp",
        "ffmpeg", "pillow", "markitdown", "unstructured",
    ],
    "Web / app frameworks": [
        "next.js", "nextjs", "react", "vue", "svelte", "vite", "fastapi",
        "flask", "django", "express", "hono", "astro", "tailwind",
        "livewire", "laravel", "jinja2", "uvicorn", "streamlit", "gradio",
    ],
    "Dev tooling / QA": [
        "pytest", "vitest", "jest", "playwright test", "eslint", "ruff",
        "black", "mypy", "prettier", "husky", "github actions", "wrangler",
        "turbo", "nx", "uv", "poetry", "pnpm", "bun",
    ],
    "Monitoring / ops": [
        "sentry", "uptimerobot", "betterstack", "healthcheck", "datadog",
        "grafana", "prometheus", "amplitude", "posthog", "alertmanager",
    ],
    "GTM / CRM / sales": [
        "apollo.io", "apollo", "attio", "hubspot", "salesforce", "clay.com",
        "instantly", "smartlead", "linkedin api", "phantombuster",
    ],
    "Knowledge / personal": [
        "obsidian", "readwise", "raindrop", "zotero", "anki",
    ],
}

ENVKEY_HINT = re.compile(r"^[A-Z][A-Z0-9_]{2,}$")


def is_skippable(path):
    parts = set(path.split(os.sep))
    return bool(parts & SKIP_DIRS)


def read_text(path):
    try:
        if os.path.getsize(path) > MAX_FILE_BYTES:
            return ""
        with open(path, errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def env_key_names(path):
    """KEY NAMES ONLY. Values are discarded before they enter any variable."""
    keys = []
    for raw in read_text(path).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key = line.split("=", 1)[0].strip().lstrip("export ").strip()
        if ENVKEY_HINT.match(key):
            keys.append(key)
    return sorted(set(keys))


def deps_from_package_json(path):
    out = []
    try:
        data = json.loads(read_text(path) or "{}")
    except Exception:
        return out
    for field in ("dependencies", "devDependencies", "peerDependencies"):
        for name, ver in (data.get(field) or {}).items():
            out.append(name + "@" + str(ver))
    return out


def deps_from_requirements(path):
    out = []
    for raw in read_text(path).splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        out.append(line)
    return out


def deps_from_pyproject(path):
    out = []
    text = read_text(path)
    block = re.search(r"dependencies\s*=\s*\[(.*?)\]", text, re.S)
    if block:
        for m in re.finditer(r'["\']([^"\']+)["\']', block.group(1)):
            out.append(m.group(1))
    for m in re.finditer(r"^([A-Za-z0-9_.\-]+)\s*=\s*[\"^~><=]", text, re.M):
        out.append(m.group(1))
    return out


def scan_project(root, name):
    proj = os.path.join(root, name)
    info = {
        "name": name,
        "root": root,
        "path": proj,
        "deps": [],
        "env_keys": [],
        "mentions": {},
        "files": 0,
        "bytes": 0,
        "langs": {},
        "has_readme": False,
        "has_claude_md": False,
        "last_modified": None,
        "manifests": [],
    }

    newest = 0
    corpus = []

    for dirpath, dirnames, filenames in os.walk(proj):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if is_skippable(dirpath):
            continue
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            try:
                st = os.stat(fp)
            except Exception:
                continue
            info["files"] += 1
            info["bytes"] += st.st_size
            newest = max(newest, st.st_mtime)
            if ext:
                info["langs"][ext] = info["langs"].get(ext, 0) + 1

            low = fn.lower()
            if low == "readme.md":
                info["has_readme"] = True
            if low == "claude.md":
                info["has_claude_md"] = True

            if low == "package.json" and "node_modules" not in fp:
                info["deps"] += deps_from_package_json(fp)
                info["manifests"].append("package.json")
            elif low.startswith("requirements") and ext == ".txt":
                info["deps"] += deps_from_requirements(fp)
                info["manifests"].append(fn)
            elif low == "pyproject.toml":
                info["deps"] += deps_from_pyproject(fp)
                info["manifests"].append("pyproject.toml")
            elif low == "go.mod":
                info["manifests"].append("go.mod")
            elif low == "gemfile":
                info["manifests"].append("Gemfile")
            elif low == "composer.json":
                info["manifests"].append("composer.json")

            if low.startswith(".env") or low == "env.example":
                info["env_keys"] += env_key_names(fp)

            if ext in TEXT_EXT and st.st_size <= MAX_FILE_BYTES:
                corpus.append(read_text(fp).lower())

    info["env_keys"] = sorted(set(info["env_keys"]))
    info["deps"] = sorted(set(info["deps"]))
    info["manifests"] = sorted(set(info["manifests"]))
    info["last_modified"] = (datetime.fromtimestamp(newest, timezone.utc).date().isoformat()
                             if newest else None)

    blob = "\n".join(corpus)
    for category, terms in VOCAB.items():
        hits = []
        for t in terms:
            if t in blob:
                hits.append(t)
        if hits:
            info["mentions"][category] = sorted(hits)

    return info


def main():
    projects = []
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            full = os.path.join(root, name)
            if not os.path.isdir(full) or name.startswith("."):
                continue
            projects.append(scan_project(root, name))

    out_json = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "stack_scan_report.json")
    with open(out_json, "w") as f:
        json.dump(projects, f, indent=2)

    lines = ["# Stack scan — " + datetime.now().date().isoformat(),
             "",
             "Projects scanned: " + str(len(projects)), ""]
    for p in projects:
        lines.append("## " + p["name"] + "  (" + os.path.basename(p["root"]) + ")")
        lines.append("- files: " + str(p["files"]) + " · "
                     + str(round(p["bytes"] / 1_000_000, 1)) + " MB · last modified "
                     + str(p["last_modified"]))
        if p["manifests"]:
            lines.append("- manifests: " + ", ".join(p["manifests"]))
        top_ext = sorted(p["langs"].items(), key=lambda kv: -kv[1])[:6]
        if top_ext:
            lines.append("- files by type: " + ", ".join(k + " x" + str(v) for k, v in top_ext))
        if p["env_keys"]:
            lines.append("- ENV KEY NAMES: " + ", ".join(p["env_keys"]))
        for cat, hits in p["mentions"].items():
            lines.append("- " + cat + ": " + ", ".join(hits))
        if p["deps"]:
            shown = p["deps"][:40]
            lines.append("- declared deps (" + str(len(p["deps"])) + "): " + ", ".join(shown)
                         + (" …" if len(p["deps"]) > 40 else ""))
        lines.append("")

    out_md = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "stack_scan_digest.md")
    with open(out_md, "w") as f:
        f.write("\n".join(lines))

    print("scanned " + str(len(projects)) + " projects")
    print("→ stack_scan_report.json")
    print("→ stack_scan_digest.md  (" + str(len("\n".join(lines))) + " chars)")


if __name__ == "__main__":
    main()
