#!/usr/bin/env python3
"""Register Threading as a user-level Codex and Claude Code skill."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "skills" / "threading"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Register the Threading skill for Codex and Claude Code."
    )
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument(
        "--platform",
        choices=("all", "codex", "claude"),
        default="all",
        help="register for both supported Agents by default",
    )
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink")
    parser.add_argument(
        "--update",
        action="store_true",
        help="replace an existing installation after moving it to a timestamped backup",
    )
    return parser.parse_args()


def skill_destinations(home: Path, platform: str) -> list[tuple[str, Path]]:
    destinations: list[tuple[str, Path]] = []
    if platform in {"all", "codex"}:
        destinations.append(("Codex", home / ".agents" / "skills" / "threading"))
    if platform in {"all", "claude"}:
        destinations.append(("Claude Code", home / ".claude" / "skills" / "threading"))
    return destinations


def backup_existing(destination: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = destination.with_name(f"threading.backup-{stamp}")
    suffix = 1
    while backup.exists() or backup.is_symlink():
        backup = destination.with_name(f"threading.backup-{stamp}-{suffix}")
        suffix += 1
    destination.rename(backup)
    return backup


def main() -> int:
    args = parse_args()
    home = args.home.expanduser().resolve()
    if home == Path("/").resolve():
        raise SystemExit("Refusing to use a filesystem root as the user home.")
    if not SOURCE.is_dir():
        raise SystemExit(f"Missing skill source: {SOURCE}")

    destinations = skill_destinations(home, args.platform)

    # Validate every target before changing any of them. An unrelated existing
    # skill is never overwritten unless the user explicitly requests --update.
    for _, destination in destinations:
        if not (destination.exists() or destination.is_symlink()):
            continue
        already_linked = (
            destination.is_symlink()
            and destination.resolve() == SOURCE.resolve()
            and args.mode == "symlink"
        )
        if not already_linked and not args.update:
            raise SystemExit(
                f"Skill destination already exists: {destination}. "
                "It was not changed. Inspect it, then use --update only if replacement is intended."
            )

    for agent_name, destination in destinations:
        if (
            destination.is_symlink()
            and destination.resolve() == SOURCE.resolve()
            and args.mode == "symlink"
        ):
            print(f"{agent_name}: Threading skill already linked: {destination}")
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        backup: Path | None = None
        if destination.exists() or destination.is_symlink():
            backup = backup_existing(destination)

        if args.mode == "symlink":
            destination.symlink_to(SOURCE.resolve(), target_is_directory=True)
        else:
            shutil.copytree(SOURCE, destination)
            (destination / "references" / "core-path.txt").write_text(
                str(ROOT.resolve()) + "\n", encoding="utf-8"
            )

        print(f"{agent_name}: registered Threading skill ({args.mode}): {destination}")
        if backup:
            print(f"{agent_name}: previous installation preserved at: {backup}")

    # v0.2 used ~/.codex/skills. Remove only the obsolete symlink when it
    # points to this exact clone; preserve any copied or unrelated installation.
    if args.platform in {"all", "codex"}:
        legacy = home / ".codex" / "skills" / "threading"
        if legacy.is_symlink() and legacy.resolve() == SOURCE.resolve():
            legacy.unlink()
            print(f"Codex: removed obsolete Threading symlink: {legacy}")
        elif legacy.exists() or legacy.is_symlink():
            print(f"Codex: preserved legacy installation for manual review: {legacy}")

    print("Threading Skill registration is ready. If it is not visible, restart the Agent once.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
