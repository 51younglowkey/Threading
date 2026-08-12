#!/usr/bin/env python3
"""Check or apply a safe fast-forward update to the Threading public core."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_UPGRADER = ROOT / "90_scripts_tools" / "project_workspace" / "upgrade_workspaces.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely update the Threading core.")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--apply", action="store_true", help="apply a verified fast-forward update")
    action.add_argument(
        "--apply-workspaces",
        action="store_true",
        help="apply the reviewed compatibility plan after the core is current",
    )
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


def run_workspace_upgrade(apply: bool) -> None:
    if not WORKSPACE_UPGRADER.is_file():
        print("Compatibility upgrader is not available in this Threading version.")
        return
    command = [sys.executable, str(WORKSPACE_UPGRADER)]
    if apply:
        command.append("--apply")
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        message = result.stderr.strip() or "Compatibility upgrade requires review."
        raise SystemExit(message)


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
        run_workspace_upgrade(apply=args.apply_workspaces)
        if not args.apply_workspaces:
            print("After reviewing the compatibility plan, re-run with --apply-workspaces.")
        return 0
    if args.apply_workspaces:
        raise SystemExit(
            "A core update is still available. Apply it first, then review the new compatibility plan."
        )
    if not args.apply:
        print("Update available. Re-run with --apply after reviewing this result.")
        print("Managed Workspace compatibility will be checked again after the core update.")
        return 0

    before = version()
    git("merge", "--ff-only", remote_ref)
    print(f"Updated Threading: {before} -> {version()}")
    print("The Git update did not overwrite Managed Workspaces under projects/local/.")
    run_workspace_upgrade(apply=False)
    print("Review this compatibility plan, then run update_threading.py --apply-workspaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
