"""KUA Step 4e — drop investment / company-performance notes for TANSTAAFL.

BOUNDARY (set by Ashley 2026-09-14, "Option B")
KUA is a general collector. For tanstaafl it writes two things into
~/tanstaafl/data/inbox/kua/ and stops:
  1. the vault note, copied verbatim
  2. one row in that folder's _meta.csv
It does not run tanstaafl-ingest. It does not touch QUEUE.md. It writes nowhere else in
tanstaafl. The VA ops job `tanstaafl-ingest-kua` (tanstaafl tenant, 08:30 IST) ingests the
drops and appends the QUEUE.md triage rows.

History: 2026-09-03 research/vault-inbox mirror (retired 2026-09-07). 2026-09-07 this helper
also ran the ingest and wrote QUEUE.md (retired 2026-09-14).

Usage:
    python3 kua_route_tanstaafl.py "<vault-relative note path>" [--ticker SYMBOL]

--ticker   NSE symbol. Pass it only when the note is about ONE listed company and the symbol
           is certain. It is checked against tanstaafl's data/reference/nse-listed-universe.csv.
           An unknown or delisted symbol is dropped with a warning, because a wrong match is
           worse than no match (doctrine 40 §5).

published_at is always the note's capture date. The note body holds replies and analysis
written at capture time, so an earlier date would leak that knowledge into point-in-time
readers (tanstaafl rule 1).

Metadata is fixed at first ingest. The manifest key is (sha256, source, url), so editing a
_meta.csv row after the job has ingested the note changes nothing in the corpus.
"""
import argparse
import csv
import datetime
import os
import re

VAULT = "/Users/ashleydsouza/Library/Mobile Documents/iCloud~md~obsidian/Documents/ai-knowledge-vault"
TANS = "/Users/ashleydsouza/tanstaafl"
INBOX = os.path.join(TANS, "data", "inbox", "kua")
META = os.path.join(INBOX, "_meta.csv")
UNIVERSE = os.path.join(TANS, "data", "reference", "nse-listed-universe.csv")
META_HEADER = ["filename", "company", "doc_type", "published_at", "url"]


def slugify(name):
    s = os.path.splitext(os.path.basename(name))[0].lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def note_date(body, fallback):
    m = re.search(r"^date:\s*\"?(\d{4}-\d{2}-\d{2})", body, re.MULTILINE)
    return m.group(1) if m else fallback


def valid_ticker(symbol):
    """Return the upper-cased symbol if it is a currently listed NSE symbol, else None."""
    if not symbol:
        return None
    sym = symbol.strip().upper()
    try:
        with open(UNIVERSE, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if (row.get("symbol") or "").strip().upper() != sym:
                    continue
                removed = (row.get("removed_on") or "").strip()
                if removed:
                    print("WARNING: %s left the listed universe on %s; company left blank" % (sym, removed))
                    return None
                return sym
    except OSError:
        print("WARNING: cannot read %s; company left blank" % UNIVERSE)
        return None
    print("WARNING: %s is not in nse-listed-universe.csv; company left blank" % sym)
    return None


def meta_has(filename):
    if not os.path.exists(META):
        return False
    with open(META, newline="", encoding="utf-8") as fh:
        return any((row.get("filename") or "") == filename for row in csv.DictReader(fh))


def route(rel, ticker=None):
    src = os.path.join(VAULT, rel)
    if not os.path.exists(src):
        print("SKIP - not found in vault:", rel)
        return None

    with open(src, errors="ignore") as fh:
        body = fh.read()
    captured = note_date(body, datetime.date.today().isoformat())

    dest_name = captured + "-" + slugify(rel) + ".md"
    dest = os.path.join(INBOX, dest_name)
    os.makedirs(INBOX, exist_ok=True)

    if os.path.exists(dest):
        print("Note already in inbox, left untouched:", dest_name)
    else:
        with open(dest, "w") as fh:
            fh.write(body)  # verbatim: no banner, no rewriting
        print("Wrote note:", dest_name)

    company = valid_ticker(ticker)

    if meta_has(dest_name):
        print("_meta.csv already has a row for this note; unchanged")
    else:
        is_new = not os.path.exists(META)
        with open(META, "a", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            if is_new:
                writer.writerow(META_HEADER)
            writer.writerow([dest_name, company or "", "kua_note", captured, "obsidian-vault://" + rel])
        print("_meta.csv row added: company=%s published_at=%s" % (company or "-", captured))

    print("Dropped. VA ops job tanstaafl-ingest-kua will ingest it at 08:30 IST.")
    return dest_name


def main():
    parser = argparse.ArgumentParser(description="Drop a vault note into tanstaafl's KUA inbox.")
    parser.add_argument("rel", help="vault-relative note path")
    parser.add_argument("--ticker", default=None, help="NSE symbol, only when certain")
    args, extra = parser.parse_known_args()
    if extra:
        print("NOTE: ignoring legacy arguments (entity/claim/counter are no longer used):", extra)
    route(args.rel, args.ticker)


if __name__ == "__main__":
    main()
