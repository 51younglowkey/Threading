#!/usr/bin/env python3
"""Render a conservative text dashboard from a user-owned Threading profile."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROFILE_ROOT = ROOT / "profiles" / "local"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a text dashboard for a Threading project profile.")
    parser.add_argument("--profile", type=Path, help="profile directory, relative to the workspace")
    parser.add_argument(
        "--allow-external-profile",
        action="store_true",
        help="allow an explicitly chosen profile outside this workspace",
    )
    return parser.parse_args()


def value(text: str, label: str, fallback: str) -> str:
    match = re.search(rf"^{re.escape(label)}:[ \t]*(.*)$", text, flags=re.MULTILINE)
    if not match:
        return fallback
    found = match.group(1).strip()
    return found or fallback


def meaningful_field(text: str, label: str) -> bool:
    found = value(text, label, "")
    return bool(found) and not found.startswith("[")


def bullet_value(text: str, label: str, fallback: str) -> str:
    match = re.search(rf"^-\s+{re.escape(label)}:[ \t]*(.*)$", text, flags=re.MULTILINE)
    if not match:
        return fallback
    found = match.group(1).strip()
    return found or fallback


def profile_dirs() -> list[Path]:
    if not PROFILE_ROOT.is_dir():
        return []
    return sorted(path for path in PROFILE_ROOT.iterdir() if path.is_dir() and not path.name.startswith("."))


def readiness(profile: Path) -> dict[str, str]:
    context = (profile / "context.md").read_text(encoding="utf-8") if (profile / "context.md").exists() else ""
    source_map = (profile / "source_map.md").read_text(encoding="utf-8") if (profile / "source_map.md").exists() else ""
    evidence = (profile / "evidence_log.md").read_text(encoding="utf-8") if (profile / "evidence_log.md").exists() else ""
    decisions = (profile / "decision_log.md").read_text(encoding="utf-8") if (profile / "decision_log.md").exists() else ""
    iteration = (profile / "iteration_log.md").read_text(encoding="utf-8") if (profile / "iteration_log.md").exists() else ""
    status = (profile / "status.md").read_text(encoding="utf-8") if (profile / "status.md").exists() else ""

    return {
        "Brief": "ready" if meaningful_field(context, "Working question") else "needs input",
        "Sources": "mapped" if "[SOURCE TO VERIFY]" not in source_map and "| S-" in source_map else "not started",
        "Evidence": "in progress" if "| E-001 | [SOURCE TO VERIFY]" not in evidence else "not started",
        "Decisions": "visible" if "[DATE TO CONFIRM]" not in decisions else "not started",
        "Prototype": "recorded" if "| v0.1 |" not in iteration else "not started",
        "Testing": bullet_value(status, "Testing", "not started"),
        "Writing": bullet_value(status, "Writing", "not started"),
        "Privacy": value(status, "Privacy review", "not started"),
    }


def render_first_run() -> None:
    print("THREADING / FIRST RUN")
    print("────────────────────────────────────────────────────────────────")
    print("Workspace       Threading")
    print("Mode            Reusable core + user-owned local project profile")
    print("Packs           none loaded by default")
    print("Project         Not started")
    print("Next move       Start a short project intake")
    print("Privacy         Project files stay in the user's chosen local space")
    print("────────────────────────────────────────────────────────────────")
    print("Say: start project / load pack gsa")


def render_profile(profile: Path) -> None:
    context = (profile / "context.md").read_text(encoding="utf-8") if (profile / "context.md").exists() else ""
    status = (profile / "status.md").read_text(encoding="utf-8") if (profile / "status.md").exists() else ""
    packs = (profile / "packs.md").read_text(encoding="utf-8") if (profile / "packs.md").exists() else ""
    title = value(context, "Project or module", profile.name)
    lifecycle = value(status, "Status", value(context, "Status", "draft"))
    phase = value(status, "Current phase", "framing")
    updated = value(status, "Last updated", "[DATE TO CONFIRM]")
    next_action = value(status, "Next action", "[DECISION PENDING]")
    loaded_packs = value(packs, "Optional packs", "none")
    states = readiness(profile)

    print("THREADING / PROJECT DASHBOARD")
    print("────────────────────────────────────────────────────────────────")
    print(f"Project         {title}")
    if ROOT in profile.parents:
        profile_display = f"{profile.relative_to(ROOT)}/"
    else:
        profile_display = f"<external profile>/{profile.name}/"
    print(f"Profile         {profile_display}")
    print(f"Packs           {loaded_packs}")
    print(f"Status          {lifecycle}")
    print(f"Phase           {phase}")
    print(f"Last update     {updated}")
    print()
    print("READINESS")
    for label, state in states.items():
        print(f"  {label:<14}{state}")
    print()
    print(f"NEXT MOVE       {next_action}")
    print("────────────────────────────────────────────────────────────────")
    print("Say: update dashboard / map my sources / review privacy")


def main() -> int:
    args = parse_args()
    if args.profile is None:
        profiles = profile_dirs()
        if not profiles:
            render_first_run()
            return 0
        if len(profiles) > 1:
            print("THREADING / SELECT A PROJECT")
            for profile in profiles:
                print(f"- {profile.name}")
            print("The Agent must ask which profile to display.")
            return 0
        profile = profiles[0]
    else:
        profile = (args.profile if args.profile.is_absolute() else ROOT / args.profile).resolve()
        if ROOT not in profile.parents:
            if not args.allow_external_profile:
                raise SystemExit(
                    "Refusing to render a profile outside this workspace. "
                    "Use --allow-external-profile only after confirming the exact profile path."
                )
            if profile in {Path("/").resolve(), Path.home().resolve()}:
                raise SystemExit("Refusing to render a filesystem root or home directory as a profile.")
        if not profile.is_dir():
            raise SystemExit(f"Profile not found: {profile}")
    render_profile(profile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
