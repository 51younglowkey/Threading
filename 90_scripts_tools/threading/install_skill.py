#!/usr/bin/env python3
"""Install Threading's standalone skill by symlink or recoverable copy."""

from __future__ import annotations

import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "skills" / "threading"


def default_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the Threading skill for Codex.")
    parser.add_argument("--codex-home", type=Path, default=default_codex_home())
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink")
    parser.add_argument(
        "--update",
        action="store_true",
        help="replace an existing installation after moving it to a timestamped backup",
    )
    return parser.parse_args()


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
    codex_home = args.codex_home.expanduser().resolve()
    if codex_home in {Path("/").resolve(), Path.home().resolve()}:
        raise SystemExit("Refusing to use a filesystem root or home directory as CODEX_HOME.")
    if not SOURCE.is_dir():
        raise SystemExit(f"Missing skill source: {SOURCE}")
    destination = codex_home / "skills" / "threading"
    destination.parent.mkdir(parents=True, exist_ok=True)

    backup: Path | None = None
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() and destination.resolve() == SOURCE.resolve() and args.mode == "symlink":
            print(f"Threading skill already linked: {destination}")
            return 0
        if not args.update:
            raise SystemExit(
                f"Skill destination already exists: {destination}. Use --update for a recoverable replacement."
            )
        backup = backup_existing(destination)

    if args.mode == "symlink":
        destination.symlink_to(SOURCE, target_is_directory=True)
    else:
        shutil.copytree(SOURCE, destination)
        (destination / "references" / "core-path.txt").write_text(
            str(ROOT.resolve()) + "\n", encoding="utf-8"
        )

    print(f"Installed Threading skill ({args.mode}): {destination}")
    if backup:
        print(f"Previous installation preserved at: {backup}")
    print("Start a new Codex task, then say: Threading Dashboard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
