#!/usr/bin/env python3
"""Copy a legacy Threading profile into a v0.2 Managed Workspace."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from common import (
    PROJECTS_ROOT,
    TEMPLATE,
    core_version,
    field,
    gsa_version,
    replace_template_tokens,
    resolve_output_root,
    validate_slug,
    write_state,
)


ROOT = Path(__file__).resolve().parents[2]
LEGACY_ROOT = ROOT / "profiles" / "local"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy a legacy profile into a Managed Workspace.")
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--slug")
    parser.add_argument("--title")
    parser.add_argument("--output-root", type=Path, default=PROJECTS_ROOT)
    parser.add_argument("--allow-external-profile", action="store_true")
    parser.add_argument("--allow-external-root", action="store_true")
    return parser.parse_args()


def resolve_legacy(raw: Path, allow_external: bool) -> Path:
    profile = raw.expanduser() if raw.is_absolute() else ROOT / raw
    profile = profile.resolve()
    if LEGACY_ROOT not in profile.parents and profile != LEGACY_ROOT:
        if not allow_external:
            raise ValueError(
                "Refusing a legacy profile outside profiles/local. Use "
                "--allow-external-profile only after confirming the path."
            )
        if profile in {Path("/").resolve(), Path.home().resolve()}:
            raise ValueError("Refusing a filesystem root or home directory as a profile.")
    if not profile.is_dir():
        raise ValueError(f"Legacy profile not found: {profile}")
    return profile


def legacy_text(profile: Path, name: str) -> str:
    path = profile / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def current_from_legacy(title: str, context: str, status: str) -> str:
    question = field(context, "Working question", "[DECISION PENDING]")
    direction = field(context, "Current hypothesis or design proposition", "[DECISION PENDING]")
    phase = field(status, "Current phase", "orientation")
    next_move = field(status, "Next action", "[DECISION PENDING]")
    return f"""# Current Project State

Project: {title}
Status: active
Current phase: {phase}
Last confirmed: [DATE TO CONFIRM]
Confirmation status: needs confirmation

## Current question

{question}

## Current direction

{direction}

## Current insight or opportunity

[EVIDENCE NEEDED]

## Current working set

| Source ID | File / page / frame / material | Why current | Confirmation |
|---|---|---|---|
| [SOURCE TO VERIFY] |  | Migrated profile requires review | needs confirmation |

## Current prototype or draft

[DECISION PENDING]

## Open contradiction or uncertainty

Legacy material has not yet been reconciled with current Figma, local files or chat history.

## Next move

{next_move}

These values were copied as candidates from a legacy profile. Confirm them before use.
"""


def write_known_records(source: Path, destination: Path) -> None:
    mapping = {
        "context.md": "project.md",
        "source_map.md": "sources/source_registry.md",
        "evidence_log.md": "evidence/evidence_log.md",
        "decision_log.md": "decisions/decision_log.md",
        "iteration_log.md": "iterations/iteration_log.md",
    }
    for old_name, new_name in mapping.items():
        old = source / old_name
        if not old.exists():
            continue
        new = destination / new_name
        content = old.read_text(encoding="utf-8")
        banner = (
            "> Migrated from a legacy Threading profile. Review status and structure before promotion.\n\n"
        )
        new.write_text(banner + content, encoding="utf-8")

    snapshot = destination / "legacy_snapshot"
    snapshot.mkdir(parents=True, exist_ok=True)
    for name in ("README.md", "context.md", "status.md", "source_map.md", "packs.md"):
        old = source / name
        if old.is_file():
            shutil.copy2(old, snapshot / name)


def main() -> int:
    args = parse_args()
    try:
        profile = resolve_legacy(args.profile, args.allow_external_profile)
        slug = validate_slug(args.slug or profile.name)
        output_root = resolve_output_root(args.output_root, args.allow_external_root)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    context = legacy_text(profile, "context.md")
    status = legacy_text(profile, "status.md")
    packs = legacy_text(profile, "packs.md")
    title = (args.title or field(context, "Project or module", profile.name)).strip()
    destination = output_root / slug
    if destination.exists():
        raise SystemExit(f"Refusing to overwrite existing Managed Workspace: {destination}")

    output_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, destination)
    replace_template_tokens(destination, title, slug)
    write_known_records(profile, destination)
    (destination / "CURRENT.md").write_text(
        current_from_legacy(title, context, status), encoding="utf-8"
    )

    gsa_enabled = bool(re.search(r"^Optional packs:\s*gsa\s*$", packs, flags=re.MULTILINE))
    gsa_pack = {
        "enabled": gsa_enabled,
        "mode": "linked-read-only",
        "version": gsa_version() if gsa_enabled else None,
    }
    write_state(
        destination,
        {
            "schema_version": 2,
            "workspace_type": "managed",
            "threading_version": core_version(),
            "project_slug": slug,
            "migrated_from": str(profile),
            "gsa_pack": gsa_pack,
        },
    )
    (destination / "packs.md").write_text(
        "# Linked Packs\n\n"
        f"Threading core version: {core_version()}\n"
        f"GSA Pack: {'enabled' if gsa_enabled else 'disabled'}\n"
        f"GSA Pack version: {gsa_version() if gsa_enabled else 'none'}\n"
        "Mode: linked-read-only\n\n"
        "The legacy profile and any copied pack were left unchanged.\n",
        encoding="utf-8",
    )

    print(f"Migrated copy created: {destination}")
    print(f"Legacy profile preserved unchanged: {profile}")
    print("Current State requires user confirmation before it becomes authoritative.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
