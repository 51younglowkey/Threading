#!/usr/bin/env python3
"""Create a user-owned Threading project profile without importing source material."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "profiles" / "_template"
DEFAULT_OUTPUT_ROOT = ROOT / "profiles" / "local"
GSA_PACK = ROOT / "packs" / "gsa"
SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an ignored, user-owned Threading project profile."
    )
    parser.add_argument("--slug", required=True, help="lowercase project slug, e.g. community-repair-lab")
    parser.add_argument("--title", default="Untitled project", help="project title written to context.md")
    parser.add_argument(
        "--pack",
        choices=("none", "gsa"),
        default="none",
        help="optional pack to load into the new profile (default: none)",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="profile root; defaults to profiles/local",
    )
    parser.add_argument(
        "--allow-external-root",
        action="store_true",
        help="allow an explicitly chosen profile root outside this Threading workspace",
    )
    return parser.parse_args()


def resolve_output_root(raw: Path, allow_external: bool) -> Path:
    root = raw.expanduser() if raw.is_absolute() else ROOT / raw
    root = root.resolve()
    if root == ROOT or ROOT in root.parents:
        return root
    if not allow_external:
        raise ValueError("Refusing an output root outside this Threading workspace.")
    if root in {Path("/").resolve(), Path.home().resolve()}:
        raise ValueError("Refusing a filesystem root or home directory as an output root.")
    return root


def write_context(profile: Path, slug: str, title: str) -> None:
    context_path = profile / "context.md"
    content = context_path.read_text(encoding="utf-8")
    content = content.replace("Status: draft / active / maintenance / archived", "Status: draft")
    content = content.replace("Project or module:\n", f"Project or module: {title}\nProject slug: {slug}\n")
    context_path.write_text(content, encoding="utf-8")


def write_status(profile: Path) -> None:
    status_path = profile / "status.md"
    if not status_path.exists():
        status_path.write_text(
            "# Project Dashboard State\n\n"
            "Status: draft\n"
            "Current phase: framing\n"
            "Last updated: [DATE TO CONFIRM]\n"
            "Next action: [DECISION PENDING]\n"
            "Privacy review: not started\n",
            encoding="utf-8",
        )


def write_packs(profile: Path, selected: str) -> None:
    packs_path = profile / "packs.md"
    if selected == "none":
        packs_path.write_text(
            "# Loaded Packs\n\n"
            "Core: Threading\n"
            "Optional packs: none\n"
            "Pack source: none selected\n\n"
            "No optional pack was copied into this profile.\n",
            encoding="utf-8",
        )
        return

    if selected == "gsa":
        if not GSA_PACK.is_dir():
            raise SystemExit(f"Missing optional pack directory: {GSA_PACK}")
        destination = profile / "packs" / "gsa"
        shutil.copytree(GSA_PACK, destination)
        packs_path.write_text(
            "# Loaded Packs\n\n"
            "Core: Threading\n"
            "Optional packs: gsa\n"
            "Pack source: packs/gsa/PACK.md\n\n"
            "The GSA pack was selected during project initialization.\n",
            encoding="utf-8",
        )
        return

    raise SystemExit(f"Unsupported pack: {selected}")


def main() -> int:
    args = parse_args()
    slug = args.slug.strip()
    if not SLUG_PATTERN.fullmatch(slug):
        raise SystemExit("Invalid --slug. Use lowercase letters, numbers and hyphens only.")
    if not args.title.strip():
        raise SystemExit("--title cannot be empty.")
    if not TEMPLATE.is_dir():
        raise SystemExit(f"Missing template directory: {TEMPLATE}")

    try:
        output_root = resolve_output_root(args.output_root, args.allow_external_root)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    profile = output_root / slug
    if profile.exists():
        raise SystemExit(f"Refusing to overwrite existing profile: {profile}")

    output_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, profile)
    write_context(profile, slug, args.title.strip())
    write_status(profile)
    write_packs(profile, args.pack)

    try:
        display_path = str(profile.relative_to(ROOT))
    except ValueError:
        display_path = str(profile)
    print(f"Created user-owned profile: {display_path}")
    print(f"Optional pack: {args.pack}")
    print("Next: fill context.md, source_map.md and status.md through the Agent intake.")
    print("No source files were imported.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
