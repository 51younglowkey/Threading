#!/usr/bin/env python3
"""Render Threading's project-aware text Dashboard."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import PROJECTS_ROOT, ROOT, field, resolve_project


LEGACY_ROOT = ROOT / "profiles" / "local"
PLACEHOLDER_PREFIXES = ("[", "| [")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a Threading Managed Workspace Dashboard.")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--allow-external-project", action="store_true")
    return parser.parse_args()


def local_projects() -> list[Path]:
    if not PROJECTS_ROOT.is_dir():
        return []
    return sorted(path for path in PROJECTS_ROOT.iterdir() if path.is_dir())


def first_section_value(text: str, heading: str, fallback: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return fallback
    for line in match.group(1).splitlines():
        value = line.strip()
        if not value or value.startswith("|") or value.startswith(PLACEHOLDER_PREFIXES):
            continue
        return value
    return fallback


def table_data_rows(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(
        1
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("|")
        and not line.startswith("|---")
        and "| ID |" not in line
        and "[SOURCE TO VERIFY]" not in line
    )


def render_welcome() -> None:
    print("THREADING / WELCOME")
    print("────────────────────────────────────────────────────────────────")
    print("Workspace       Complete local research and design workspace")
    print("Project         No Managed Workspace selected")
    print("Core abilities  Adopt project / Current State / Figma evolution")
    print("                Chat reconciliation / evidence / decisions / outputs")
    print("GSA Pack        available, not enabled by default")
    print("Next move       Say: 帮我接管这个现有项目")
    print("────────────────────────────────────────────────────────────────")


def render_project(project: Path) -> None:
    current = (project / "CURRENT.md").read_text(encoding="utf-8")
    packs = (project / "packs.md").read_text(encoding="utf-8") if (project / "packs.md").exists() else ""
    title = field(current, "Project", project.name)
    phase = field(current, "Current phase", "orientation")
    confirmed = field(current, "Last confirmed", "[DATE TO CONFIRM]")
    confirmation = field(current, "Confirmation status", "needs confirmation")
    question = first_section_value(current, "Current question", "[DECISION PENDING]")
    direction = first_section_value(current, "Current direction", "[DECISION PENDING]")
    next_move = first_section_value(current, "Next move", "[DECISION PENDING]")
    gsa = field(packs, "GSA Pack", "disabled")
    gsa_version = field(packs, "GSA Pack version", "none")
    sources = table_data_rows(project / "sources" / "source_registry.md")
    evidence = table_data_rows(project / "evidence" / "evidence_log.md")
    decisions = table_data_rows(project / "decisions" / "decision_log.md")
    chat_candidates = table_data_rows(project / "sources" / "chats" / "candidate_records.md")

    print("THREADING / PROJECT DASHBOARD")
    print("────────────────────────────────────────────────────────────────")
    print(f"Project         {title}")
    try:
        display = f"{project.relative_to(ROOT)}/"
    except ValueError:
        display = f"<external project>/{project.name}/"
    print(f"Workspace       {display}")
    print(f"Phase           {phase}")
    print(f"Last confirmed  {confirmed}")
    print(f"Current status  {confirmation}")
    print(f"Current question {question}")
    print(f"Current direction {direction}")
    print()
    print("KNOWLEDGE")
    print(f"  Sources       {sources} registered")
    print(f"  Evidence      {evidence} records")
    print(f"  Decisions     {decisions} records")
    print(f"  Chat review   {chat_candidates} candidates")
    print()
    print(f"GSA PACK        {gsa} / version {gsa_version}")
    if gsa == "enabled":
        print("  Methods / Provotyping / Reflection Document / Stage 3 audit")
    print()
    print(f"NEXT MOVE       {next_move}")
    print("────────────────────────────────────────────────────────────────")
    print("Say: orient my project / reconcile chat archive / map Figma / review current state")


def main() -> int:
    args = parse_args()
    if args.project:
        try:
            project = resolve_project(args.project, args.allow_external_project)
        except ValueError as error:
            raise SystemExit(str(error)) from error
        render_project(project)
        return 0

    projects = local_projects()
    if not projects:
        render_welcome()
        if LEGACY_ROOT.is_dir() and any(path.is_dir() for path in LEGACY_ROOT.iterdir()):
            print("Legacy profiles detected. Say: migrate my old Threading profile")
        return 0
    if len(projects) > 1:
        print("THREADING / SELECT A PROJECT")
        for project in projects:
            print(f"- {project.name}")
        print("Ask the user which project to open; do not choose silently.")
        return 0
    render_project(projects[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
