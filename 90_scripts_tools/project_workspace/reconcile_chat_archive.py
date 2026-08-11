#!/usr/bin/env python3
"""Register an existing Markdown chat archive and create a bounded review scaffold."""

from __future__ import annotations

import argparse
import hashlib
import re
from datetime import date
from pathlib import Path

from common import markdown_escape, resolve_project


HEADING_PATTERN = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
TITLE_PATTERN = re.compile(r"^(?:Title|Conversation|Chat title):\s*(.+?)\s*$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Register a Markdown chat archive for user-confirmed reconciliation."
    )
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--label", help="neutral archive label")
    parser.add_argument("--analysis-note", type=Path, action="append", default=[])
    parser.add_argument("--max-headings", type=int, default=200)
    parser.add_argument("--allow-external-project", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observed_headings(text: str, limit: int) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    seen: set[str] = set()
    for number, line in enumerate(text.splitlines(), start=1):
        match = HEADING_PATTERN.match(line) or TITLE_PATTERN.match(line)
        if not match:
            continue
        value = match.group(match.lastindex or 1).strip()
        key = value.casefold()
        if not value or key in seen:
            continue
        seen.add(key)
        headings.append((number, value))
        if len(headings) >= limit:
            break
    return headings


def append_inventory(
    inventory: Path,
    archive_id: str,
    label: str,
    pointer: str,
    digest: str,
    heading_count: int,
    notes: list[Path],
) -> None:
    text = inventory.read_text(encoding="utf-8")
    if digest in text:
        raise SystemExit("This chat archive hash is already registered in the selected project.")
    note_labels = ", ".join(markdown_escape(str(path)) for path in notes) or "none"
    row = (
        f"| {archive_id} | {markdown_escape(label)} — {markdown_escape(pointer)} | "
        f"{digest} | {heading_count} | {note_labels} | pending review |\n"
    )
    inventory.write_text(text.rstrip() + "\n" + row, encoding="utf-8")


def write_reconciliation(
    destination: Path,
    archive_id: str,
    label: str,
    archive: Path,
    digest: str,
    headings: list[tuple[int, str]],
    notes: list[Path],
) -> None:
    heading_lines = "\n".join(
        f"- Line {number}: {value}" for number, value in headings
    ) or "- No Markdown conversation headings detected; manual segmentation is required."
    note_lines = "\n".join(f"- {path}" for path in notes) or "- none"
    content = f"""# Chat Reconciliation — {archive_id}

Status: pending review
Archive label: {label}
Archive pointer: {archive}
SHA-256: {digest}
Registered: {date.today().isoformat()}

## Earlier analysis notes

{note_lines}

## Observed headings

{heading_lines}

## Review protocol

1. Select a bounded group of relevant conversations.
2. Separate observed user statements from model-generated prose.
3. Record candidate insight, decision, rejected direction, open question,
   source pointer or unsupported model claim.
4. Compare candidates with confirmed Figma/local sources and `CURRENT.md`.
5. Ask the project owner to confirm, reject or supersede each material item.
6. Promote only confirmed items into project records. Leave the archive unchanged.

## Candidate review

| ID | Conversation / line locator | Type | Candidate statement | Supporting source | Review status | Destination |
|---|---|---|---|---|---|---|
"""
    destination.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.max_headings < 1:
        raise SystemExit("--max-headings must be positive.")
    try:
        project = resolve_project(args.project, args.allow_external_project)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    archive = args.archive.expanduser().resolve()
    if not archive.is_file():
        raise SystemExit(f"Chat archive not found: {archive}")
    if archive.suffix.lower() not in {".md", ".markdown", ".txt"}:
        raise SystemExit("First release supports Markdown or plain-text chat archives only.")
    notes = [path.expanduser().resolve() for path in args.analysis_note]
    missing_notes = [path for path in notes if not path.is_file()]
    if missing_notes:
        raise SystemExit(f"Analysis note not found: {missing_notes[0]}")

    text = archive.read_text(encoding="utf-8", errors="replace")
    digest = sha256(archive)
    archive_id = f"CH-{date.today().strftime('%Y%m%d')}-{digest[:8]}"
    label = args.label.strip() if args.label else archive.stem
    headings = observed_headings(text, args.max_headings)
    inventory = project / "sources" / "chats" / "chat_inventory.md"
    if not inventory.exists():
        raise SystemExit("Selected project is missing sources/chats/chat_inventory.md")
    append_inventory(inventory, archive_id, label, str(archive), digest, len(headings), notes)

    review_dir = project / "sources" / "chats" / "reconciliation"
    review_dir.mkdir(parents=True, exist_ok=True)
    review_path = review_dir / f"{archive_id}.md"
    write_reconciliation(review_path, archive_id, label, archive, digest, headings, notes)
    print(f"Registered chat archive: {archive_id}")
    print(f"Observed headings: {len(headings)}")
    print(f"Review scaffold: {review_path}")
    print("No candidate was promoted and the source archive was not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
