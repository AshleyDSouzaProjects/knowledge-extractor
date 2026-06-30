# MinerU Evaluation — Knowledge Extractor Integration
*Evaluated 2026-06-29*

## Installation Status

**Partially installed.** `magic-pdf 1.3.0` (Python 3.9) and `magic-pdf 1.3.12` (Python 3.11) both installed via pip.

**Blocker:** MinerU requires Python 3.10+ (uses `|` union type syntax). System Python is 3.9. Python 3.11 (Homebrew) works for import but CLI fails due to a cascade of missing ML dependencies:
- `ultralytics` — installed
- `doclayout-yolo` — installed  
- `rapid_table` — missing (not yet installed)
- Likely further: model weight downloads (YOLO layout model, OCR models, etc.) — several GB

**Bottom line:** Full MinerU requires ~5 additional pip installs + model weight downloads. Not a quick setup.

---

## Quality Comparison (what we know)

| Feature | pdftotext (poppler) | MinerU |
|---|---|---|
| Text extraction | Good — preserves reading order | Better — layout-aware |
| Tables | Flat text only | Structured HTML |
| Equations | Raw text (garbled) | LaTeX |
| Scanned PDFs | Fails (no OCR) | OCR in 109 languages |
| Images | Skipped | Can extract |
| Setup | One brew install, instant | 5+ pip installs + GB of models |
| Speed | Fast | Slow (ML inference per page) |
| Python version | Any | 3.10+ required |

**Test PDF** (`IT_leaders_V2.pdf`): pdftotext produced 35,675 chars of clean readable text in <1s. MinerU could not complete due to missing deps.

---

## Recommendation

**Do NOT replace pdftotext with MinerU in the KUA pipeline.**

Reason: KUA processes text-heavy content (tweets, articles, LinkedIn posts, newsletters). For these, pdftotext is fast, reliable, and sufficient. MinerU's advantages (table HTML, LaTeX equations, OCR) are irrelevant for KUA's typical inputs.

**MinerU IS worth using for:**
- Academic papers with equations
- Financial reports with complex tables
- Scanned documents (anything where pdftotext returns garbage)
- One-off structured PDF extraction where layout matters

**Suggested workflow:**
1. KUA continues using pdftotext as primary PDF extractor
2. MinerU installed as optional fallback, invoked manually for complex structured PDFs
3. To complete MinerU setup when needed: `pip3.11 install rapid_table` then run — expect additional missing deps and model downloads on first run

---

## Integration Steps (if you want to add MinerU as optional path)

```python
# In extract.py, add a --mineru flag:
# /opt/homebrew/bin/python3.11 -m magic_pdf.tools.cli -p <pdf_path> -o <out_dir> -m auto
# Output: <out_dir>/<pdf_name>/auto/<pdf_name>.md
```

Full setup first requires:
1. `pip3.11 install rapid_table` (and likely 2-3 more missing deps)
2. First run downloads model weights (~1-3GB)
3. Config at `~/magic-pdf.json` already created
