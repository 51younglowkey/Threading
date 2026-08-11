#!/usr/bin/env python3
"""Search a page-anchored course-PDF OCR index without loading whole PDFs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX = ROOT / ".academic_cache" / "pdf_index" / "week_pdf" / "page_index.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser(description="Search a local PDF/image OCR index.")
    parser.add_argument("query", help="Case-insensitive text or regular expression.")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--regex", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if args.limit <= 0:
        parser.error("--limit must be a positive integer")
    index_path = args.index.expanduser().resolve()
    if not index_path.is_file():
        print(
            f"Index not found: {index_path}\n"
            "Build an index first with build_week_pdf_index.py, or pass --index PATH.",
            file=sys.stderr,
        )
        return 2

    pattern_text = args.query if args.regex else re.escape(args.query)
    try:
        pattern = re.compile(pattern_text, re.IGNORECASE)
    except re.error as exc:
        print(f"Invalid regular expression: {exc}", file=sys.stderr)
        return 2
    matches = []
    with index_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            record = json.loads(raw_line)
            text = record.get("search_text", "")
            hits = list(pattern.finditer(text))
            if hits:
                first = hits[0]
                start = max(0, first.start() - 180)
                end = min(len(text), first.end() + 260)
                snippet = re.sub(r"\s+", " ", text[start:end]).strip()
                matches.append((len(hits), record, snippet))

    matches.sort(key=lambda item: (-item[0], item[1]["file_name"].casefold(), item[1]["page_number"]))
    for count, record, snippet in matches[: args.limit]:
        confidence = record.get("mean_confidence")
        confidence_text = "n/a" if confidence is None else f"{confidence:.3f}"
        print(
            f"{record['source_label']} p.{record['page_number']} | "
            f"hits={count} | mean_confidence={confidence_text}"
        )
        print(f"  {snippet}")
    print(f"matches={len(matches)} shown={min(len(matches), args.limit)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
