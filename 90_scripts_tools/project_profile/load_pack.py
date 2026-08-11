#!/usr/bin/env python3
"""Enable a linked optional Threading pack for a legacy user-owned profile."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GSA_PACK = ROOT / "packs" / "gsa"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load an optional Threading pack into an existing legacy project profile."
    )
    parser.add_argument(
        "--profile",
        type=Path,
        required=True,
        help="Existing legacy project profile, relative to the workspace or an absolute path.",
    )
    parser.add_argument(
        "--pack",
        choices=("gsa",),
        required=True,
        help="Pack to load.",
    )
    parser.add_argument(
        "--allow-external-profile",
        action="store_true",
        help="Allow an explicitly chosen profile outside this Threading workspace.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="deprecated compatibility flag; linked packs update with the core",
    )
    return parser.parse_args()


def resolve_profile(raw: Path, allow_external: bool) -> Path:
    profile = raw.expanduser() if raw.is_absolute() else ROOT / raw
    profile = profile.resolve()
    if ROOT in profile.parents:
        return profile
    if not allow_external:
        raise ValueError(
            "Refusing a profile outside this workspace. Use --allow-external-profile "
            "only after confirming the exact profile path."
        )
    if profile in {Path("/").resolve(), Path.home().resolve()}:
        raise ValueError("Refusing a filesystem root or home directory as a profile.")
    return profile


def update_packs_file(profile: Path, selected: str) -> None:
    packs_path = profile / "packs.md"
    if packs_path.exists():
        content = packs_path.read_text(encoding="utf-8")
    else:
        content = "# Loaded Packs\n\nCore: Threading\n"
    if re.search(r"^Optional packs:", content, flags=re.MULTILINE):
        content = re.sub(
            r"^Optional packs:.*$",
            f"Optional packs: {selected}",
            content,
            flags=re.MULTILINE,
        )
    else:
        content += f"Optional packs: {selected}\n"
    if re.search(r"^Pack source:", content, flags=re.MULTILINE):
        content = re.sub(
            r"^Pack source:.*$",
            f"Pack source: core packs/{selected}/PACK.md",
            content,
            flags=re.MULTILINE,
        )
    else:
        content += f"Pack source: core packs/{selected}/PACK.md\n"
    pack_version = (GSA_PACK / "VERSION").read_text(encoding="utf-8").strip()
    if re.search(r"^Pack mode:", content, flags=re.MULTILINE):
        content = re.sub(r"^Pack mode:.*$", "Pack mode: linked-read-only", content, flags=re.MULTILINE)
    else:
        content += "Pack mode: linked-read-only\n"
    if re.search(r"^Pack version:", content, flags=re.MULTILINE):
        content = re.sub(r"^Pack version:.*$", f"Pack version: {pack_version}", content, flags=re.MULTILINE)
    else:
        content += f"Pack version: {pack_version}\n"
    content = content.rstrip() + "\n\nThe pack is linked from the Threading core by explicit user selection.\n"
    packs_path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        profile = resolve_profile(args.profile, args.allow_external_profile)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    if not profile.is_dir():
        raise SystemExit(f"Profile not found: {profile}")

    if args.pack == "gsa":
        if not GSA_PACK.is_dir():
            raise SystemExit(f"Missing optional pack directory: {GSA_PACK}")
        destination = profile / "packs" / "gsa"
        if destination.exists():
            print(f"Legacy copied pack preserved unchanged: {destination}")
        update_packs_file(profile, "gsa")
        print(f"Enabled linked pack: gsa for {profile}")
        if args.update:
            print("--update is no longer required; linked packs update with the Threading core.")
        print("No project source files or pack copies were imported.")
        return 0

    raise SystemExit(f"Unsupported pack: {args.pack}")


if __name__ == "__main__":
    raise SystemExit(main())
