#!/usr/bin/env python3
"""Report Threading core, skill, project and linked-pack health."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED_WORKSPACE_PATHS = (
    "AGENTS.md",
    "CURRENT.md",
    "project.md",
    "packs.md",
    "threading.json",
    "sources/source_registry.md",
    "sources/chats/chat_inventory.md",
    "sources/chats/candidate_records.md",
    "sources/figma/evolution_map.md",
    "sources/local-files/README.md",
    "evidence/evidence_log.md",
    "decisions/decision_log.md",
    "iterations/iteration_log.md",
    "outputs/README.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Threading installation and project health.")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--home", type=Path, default=Path.home())
    return parser.parse_args()


def check(label: str, ok: bool, detail: str) -> bool:
    print(f"{'PASS' if ok else 'FAIL'}  {label}: {detail}")
    return ok


def git_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", path], cwd=ROOT, check=False
    )
    return result.returncode == 0


def main() -> int:
    args = parse_args()
    results: list[bool] = []
    version_path = ROOT / "VERSION"
    results.append(check("core", version_path.is_file(), str(ROOT)))
    version = version_path.read_text(encoding="utf-8").strip() if version_path.exists() else "missing"
    results.append(check("version", version != "missing", version))
    results.append(check("local privacy", git_ignored("projects/local/example"), "projects/local is ignored"))

    home = args.home.expanduser().resolve()
    skill_locations = (
        ("Codex skill", home / ".agents" / "skills" / "threading"),
        ("Claude Code skill", home / ".claude" / "skills" / "threading"),
    )
    for label, skill in skill_locations:
        installed = skill.exists() or skill.is_symlink()
        if installed and skill.is_symlink():
            detail = f"symlink -> {skill.resolve()}"
        elif installed:
            detail = "copied installation"
        else:
            detail = "not registered; run install_skill.py"
        results.append(check(label, installed, detail))

    if args.project:
        project = args.project.expanduser().resolve()
        results.append(check("project", project.is_dir(), str(project)))
        current = project / "CURRENT.md"
        state_path = project / "threading.json"
        results.append(check("Current State", current.is_file(), str(current)))
        results.append(check("project state", state_path.is_file(), str(state_path)))
        missing = [relative for relative in REQUIRED_WORKSPACE_PATHS if not (project / relative).is_file()]
        results.append(
            check(
                "workspace structure",
                not missing,
                "complete" if not missing else "missing: " + ", ".join(missing),
            )
        )
        if state_path.is_file():
            try:
                state = json.loads(state_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                results.append(check("project JSON", False, str(error)))
            else:
                results.append(
                    check("schema", state.get("schema_version") == 2, str(state.get("schema_version")))
                )
                pack = state.get("gsa_pack", {})
                if pack.get("enabled"):
                    pack_version = (ROOT / "packs" / "gsa" / "VERSION").read_text(encoding="utf-8").strip()
                    results.append(
                        check(
                            "GSA Pack",
                            pack.get("mode") == "linked-read-only" and pack.get("version") == pack_version,
                            f"project={pack.get('version')} core={pack_version}",
                        )
                    )

    passed = sum(results)
    print(f"Summary: {passed}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
