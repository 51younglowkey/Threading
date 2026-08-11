#!/usr/bin/env python3
"""Check or apply a safe fast-forward update to the Threading public core."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely update the Threading core.")
    parser.add_argument("--apply", action="store_true", help="apply a verified fast-forward update")
    parser.add_argument("--no-fetch", action="store_true", help="inspect existing refs without network access")
    return parser.parse_args()


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise SystemExit(f"git {' '.join(args)} failed: {message}")
    return result.stdout.strip()


def version() -> str:
    path = ROOT / "VERSION"
    return path.read_text(encoding="utf-8").strip() if path.exists() else "pre-versioned"


def main() -> int:
    args = parse_args()
    if git("rev-parse", "--is-inside-work-tree") != "true":
        raise SystemExit("Threading core is not inside a Git working tree.")
    branch = git("branch", "--show-current")
    if branch != "main":
        raise SystemExit(f"Refusing automatic update from branch {branch!r}; switch to main first.")
    dirty = git("status", "--porcelain")
    if dirty:
        print("Threading core has local tracked or untracked changes:")
        print(dirty)
        raise SystemExit("Commit, stash or resolve tracked changes before updating.")

    if not args.no_fetch:
        git("fetch", "origin", "main")
    remote_ref = "origin/main"
    git("rev-parse", "--verify", remote_ref)
    counts = git("rev-list", "--left-right", "--count", f"HEAD...{remote_ref}").split()
    if len(counts) != 2:
        raise SystemExit("Could not determine local/remote divergence.")
    ahead, behind = (int(value) for value in counts)
    print(f"Threading version: {version()}")
    print(f"Branch: {branch}; ahead: {ahead}; behind: {behind}")

    if ahead and behind:
        raise SystemExit("Local and origin/main have diverged; manual review is required.")
    if ahead:
        raise SystemExit("Local main contains unpublished commits; automatic update is disabled.")
    if behind == 0:
        print("Threading core is already up to date.")
        return 0
    if not args.apply:
        print("Update available. Re-run with --apply after reviewing this result.")
        return 0

    before = version()
    git("merge", "--ff-only", remote_ref)
    print(f"Updated Threading: {before} -> {version()}")
    print("Managed Workspaces under projects/local/ were not touched.")
    print("Run doctor.py, then start a new Codex task to refresh instructions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
