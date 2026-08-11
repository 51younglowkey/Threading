#!/usr/bin/env python3
"""Shared boundaries for Threading Managed Workspace tools."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECTS_ROOT = ROOT / "projects" / "local"
TEMPLATE = ROOT / "projects" / "_template"
SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def core_version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def gsa_version() -> str:
    return (ROOT / "packs" / "gsa" / "VERSION").read_text(encoding="utf-8").strip()


def validate_slug(slug: str) -> str:
    cleaned = slug.strip()
    if not SLUG_PATTERN.fullmatch(cleaned):
        raise ValueError("Invalid slug. Use lowercase letters, numbers and hyphens only.")
    return cleaned


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


def resolve_project(raw: Path, allow_external: bool, must_exist: bool = True) -> Path:
    project = raw.expanduser() if raw.is_absolute() else ROOT / raw
    project = project.resolve()
    if ROOT not in project.parents:
        if not allow_external:
            raise ValueError(
                "Refusing a project outside Threading. Use --allow-external-project "
                "only after confirming the exact path."
            )
        if project in {Path("/").resolve(), Path.home().resolve()}:
            raise ValueError("Refusing a filesystem root or home directory as a project.")
    if must_exist and not project.is_dir():
        raise ValueError(f"Project not found: {project}")
    return project


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def field(text: str, label: str, fallback: str = "") -> str:
    match = re.search(rf"^{re.escape(label)}:[ \t]*(.*)$", text, flags=re.MULTILINE)
    if not match:
        return fallback
    value = match.group(1).strip()
    return value or fallback


def read_state(project: Path) -> dict:
    path = project / "threading.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_state(project: Path, state: dict) -> None:
    (project / "threading.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def replace_template_tokens(project: Path, title: str, slug: str) -> None:
    replacements = {
        "[PROJECT TITLE]": title,
        "[PROJECT SLUG]": slug,
        "[THREADING VERSION]": core_version(),
    }
    for path in project.rglob("*"):
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            content = content.replace(old, new)
        path.write_text(content, encoding="utf-8")
