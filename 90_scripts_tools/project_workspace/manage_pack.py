#!/usr/bin/env python3
"""Enable or disable Threading's linked, read-only GSA Pack for a local project."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import core_version, gsa_version, read_state, resolve_project, write_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage linked Threading packs.")
    parser.add_argument("--project", type=Path, required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--enable-gsa", action="store_true")
    action.add_argument("--disable-gsa", action="store_true")
    parser.add_argument("--allow-external-project", action="store_true")
    return parser.parse_args()


def write_pack_state(project: Path, enabled: bool) -> None:
    version = gsa_version() if enabled else None
    legacy = project / "packs" / "gsa"
    note = ""
    if legacy.is_dir():
        note = (
            "\nLegacy copied pack detected at `packs/gsa/`. It was left unchanged; "
            "the active pack is the linked core version.\n"
        )
    content = (
        "# Linked Packs\n\n"
        f"Threading core version: {core_version()}\n"
        f"GSA Pack: {'enabled' if enabled else 'disabled'}\n"
        f"GSA Pack version: {version or 'none'}\n"
        "Mode: linked-read-only\n\n"
        "Project analysis belongs in this workspace. Do not modify the pack source.\n"
        f"{note}"
    )
    (project / "packs.md").write_text(content, encoding="utf-8")
    state = read_state(project)
    state.setdefault("schema_version", 2)
    state.setdefault("workspace_type", "managed")
    state["threading_version"] = core_version()
    state["gsa_pack"] = {
        "enabled": enabled,
        "mode": "linked-read-only",
        "version": version,
    }
    write_state(project, state)


def main() -> int:
    args = parse_args()
    try:
        project = resolve_project(args.project, args.allow_external_project)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    if not (project / "CURRENT.md").exists():
        raise SystemExit("Selected directory is not a Managed Workspace: missing CURRENT.md")

    enabled = bool(args.enable_gsa)
    write_pack_state(project, enabled)
    if enabled:
        print(f"GSA Pack enabled (linked, read-only), version {gsa_version()}")
        print("Available: taught methods, Provotyping, Reflection Document analysis, Stage 3 audit.")
    else:
        print("GSA Pack disabled for this project. Core Threading remains available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
