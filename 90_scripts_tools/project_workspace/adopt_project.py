#!/usr/bin/env python3
"""Create a complete local Threading Managed Workspace without importing raw sources."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from common import (
    PROJECTS_ROOT,
    TEMPLATE,
    core_version,
    gsa_version,
    markdown_escape,
    read_state,
    replace_template_tokens,
    resolve_output_root,
    validate_slug,
    write_state,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Adopt an existing project into a private Threading Managed Workspace."
    )
    parser.add_argument("--slug", required=True, help="lowercase project slug")
    parser.add_argument("--title", required=True, help="project title")
    parser.add_argument("--pack", choices=("none", "gsa"), default="none")
    parser.add_argument("--local-source", action="append", default=[], help="local source pointer")
    parser.add_argument("--figma-source", action="append", default=[], help="Figma file/page pointer")
    parser.add_argument("--chat-source", action="append", default=[], help="chat Markdown pointer")
    parser.add_argument("--output-root", type=Path, default=PROJECTS_ROOT)
    parser.add_argument("--allow-external-root", action="store_true")
    return parser.parse_args()


def display_pointer(raw: str) -> str:
    path = Path(raw).expanduser()
    if path.exists():
        return str(path.resolve())
    return raw.strip()


def source_rows(args: argparse.Namespace) -> list[str]:
    rows: list[str] = []
    counter = 1
    groups = (
        ("local-folder", args.local_source),
        ("figma", args.figma_source),
        ("chat-markdown", args.chat_source),
    )
    for source_type, values in groups:
        for raw in values:
            pointer = markdown_escape(display_pointer(raw))
            rows.append(
                f"| S-{counter:03d} | {source_type} | {pointer} | not requested |  | unknown |"
            )
            counter += 1
    if not rows:
        rows.append(
            "| S-001 | [SOURCE TO VERIFY] | [SOURCE TO VERIFY] | not requested |  | unknown |"
        )
    return rows


def write_sources(project: Path, args: argparse.Namespace) -> None:
    path = project / "sources" / "source_registry.md"
    text = path.read_text(encoding="utf-8")
    placeholder = (
        "| S-001 | [SOURCE TO VERIFY] | [SOURCE TO VERIFY] | not requested |  | unknown |"
    )
    path.write_text(text.replace(placeholder, "\n".join(source_rows(args))), encoding="utf-8")


def configure_pack(project: Path, selected: str) -> None:
    enabled = selected == "gsa"
    version = gsa_version() if enabled else None
    packs = (
        "# Linked Packs\n\n"
        f"Threading core version: {core_version()}\n"
        f"GSA Pack: {'enabled' if enabled else 'disabled'}\n"
        f"GSA Pack version: {version or 'none'}\n"
        "Mode: linked-read-only\n\n"
        "Project analysis belongs in this workspace. Do not modify the pack source.\n"
    )
    (project / "packs.md").write_text(packs, encoding="utf-8")
    state = read_state(project)
    state["gsa_pack"] = {
        "enabled": enabled,
        "mode": "linked-read-only",
        "version": version,
    }
    write_state(project, state)


def main() -> int:
    args = parse_args()
    try:
        slug = validate_slug(args.slug)
        output_root = resolve_output_root(args.output_root, args.allow_external_root)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    title = args.title.strip()
    if not title:
        raise SystemExit("--title cannot be empty.")
    if not TEMPLATE.is_dir():
        raise SystemExit(f"Missing Managed Workspace template: {TEMPLATE}")

    project = output_root / slug
    if project.exists():
        raise SystemExit(f"Refusing to overwrite existing workspace: {project}")
    output_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, project)
    replace_template_tokens(project, title, slug)
    write_sources(project, args)
    configure_pack(project, args.pack)

    print(f"Created Managed Workspace: {project}")
    print(f"Threading core: {core_version()}")
    print(f"GSA Pack: {'linked and enabled' if args.pack == 'gsa' else 'disabled'}")
    print("Registered source pointers only; no raw source was inspected or copied.")
    print("Next: ask the Agent to orient the named sources and propose a Current State.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
