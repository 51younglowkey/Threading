#!/usr/bin/env python3
"""Safely connect older Threading traces to the current Managed Workspace schema."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

from common import (
    PROJECTS_ROOT,
    ROOT,
    TEMPLATE,
    core_version,
    field,
    gsa_version,
    resolve_output_root,
    resolve_project,
    validate_slug,
    write_state,
)


CURRENT_SCHEMA = 2
LEGACY_ROOT = ROOT / "profiles" / "local"
MIGRATOR = Path(__file__).with_name("migrate_legacy_profile.py")
KNOWN_LEGACY_FILES = (
    "README.md",
    "context.md",
    "status.md",
    "source_map.md",
    "evidence_log.md",
    "decision_log.md",
    "iteration_log.md",
    "packs.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check or apply non-destructive compatibility upgrades for Threading "
            "Managed Workspaces and legacy profiles."
        )
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--project", type=Path, action="append", default=[])
    parser.add_argument("--legacy-profile", type=Path, action="append", default=[])
    parser.add_argument("--output-root", type=Path, default=PROJECTS_ROOT)
    parser.add_argument("--legacy-root", type=Path, default=LEGACY_ROOT)
    parser.add_argument("--allow-external-project", action="store_true")
    parser.add_argument("--allow-external-root", action="store_true")
    parser.add_argument("--allow-external-legacy", action="store_true")
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def resolve_legacy_profile(raw: Path, allow_external: bool) -> Path:
    profile = raw.expanduser() if raw.is_absolute() else ROOT / raw
    profile = profile.resolve()
    if LEGACY_ROOT not in profile.parents and profile != LEGACY_ROOT:
        if not allow_external:
            raise ValueError(
                "Refusing a legacy profile outside profiles/local. Use "
                "--allow-external-legacy only after confirming the exact path."
            )
        if profile in {Path("/").resolve(), Path.home().resolve()}:
            raise ValueError("Refusing a filesystem root or home directory as a legacy profile.")
    if not profile.is_dir():
        raise ValueError(f"Legacy profile not found: {profile}")
    return profile


def discover_projects(output_root: Path) -> list[Path]:
    if not output_root.is_dir():
        return []
    return sorted(
        path for path in output_root.iterdir() if path.is_dir() and not path.name.startswith(".")
    )


def discover_legacy(legacy_root: Path) -> list[Path]:
    if not legacy_root.is_dir():
        return []
    return sorted(
        path for path in legacy_root.iterdir() if path.is_dir() and not path.name.startswith(".")
    )


def load_state(project: Path) -> tuple[dict, str | None]:
    path = project / "threading.json"
    if not path.exists():
        return {}, None
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as error:
        return {}, f"invalid threading.json: {error}"


def project_title(project: Path, state: dict) -> str:
    current = project / "CURRENT.md"
    if current.is_file():
        value = field(current.read_text(encoding="utf-8"), "Project", "")
        if value:
            return value
    context = project / "project.md"
    if context.is_file():
        value = field(context.read_text(encoding="utf-8"), "Project", "")
        if value:
            return value
    return str(state.get("project_title") or project.name)


def pack_enabled(project: Path, state: dict) -> bool:
    pack = state.get("gsa_pack")
    if isinstance(pack, dict) and isinstance(pack.get("enabled"), bool):
        return bool(pack["enabled"])
    packs = project / "packs.md"
    if packs.is_file():
        return field(packs.read_text(encoding="utf-8"), "GSA Pack", "disabled") == "enabled"
    return False


def template_files() -> list[Path]:
    return sorted(path for path in TEMPLATE.rglob("*") if path.is_file())


def plan_project(project: Path) -> dict:
    state, error = load_state(project)
    plan = {
        "kind": "managed",
        "path": project,
        "slug": project.name,
        "state": state,
        "error": error,
        "blocked": False,
        "missing": [],
        "schema_before": state.get("schema_version"),
        "version_before": state.get("threading_version"),
        "title": project_title(project, state),
        "gsa_enabled": pack_enabled(project, state),
        "changes": [],
    }
    if error:
        plan["blocked"] = True
        return plan
    if not (project / "CURRENT.md").is_file() and not (project / "project.md").is_file():
        plan["blocked"] = True
        plan["error"] = "not recognised as a Managed Workspace"
        return plan
    schema = state.get("schema_version")
    if isinstance(schema, int) and schema > CURRENT_SCHEMA:
        plan["blocked"] = True
        plan["error"] = f"workspace schema {schema} is newer than supported schema {CURRENT_SCHEMA}"
        return plan
    try:
        validate_slug(project.name)
    except ValueError as error_value:
        plan["blocked"] = True
        plan["error"] = str(error_value)
        return plan

    missing = [
        path.relative_to(TEMPLATE)
        for path in template_files()
        if not (project / path.relative_to(TEMPLATE)).exists()
    ]
    plan["missing"] = missing
    if missing:
        plan["changes"].append(f"add {len(missing)} missing schema files")
    if schema != CURRENT_SCHEMA:
        plan["changes"].append(f"schema {schema or 'unknown'} -> {CURRENT_SCHEMA}")
    if state.get("threading_version") != core_version():
        plan["changes"].append(
            f"Threading {state.get('threading_version') or 'unknown'} -> {core_version()}"
        )
    pack = state.get("gsa_pack") if isinstance(state.get("gsa_pack"), dict) else {}
    expected_pack_version = gsa_version() if plan["gsa_enabled"] else None
    if (
        pack.get("enabled") != plan["gsa_enabled"]
        or pack.get("mode") != "linked-read-only"
        or pack.get("version") != expected_pack_version
    ):
        plan["changes"].append("refresh linked GSA Pack metadata")
    return plan


def render_template(path: Path, title: str, slug: str) -> str:
    content = path.read_text(encoding="utf-8")
    replacements = {
        "[PROJECT TITLE]": title,
        "[PROJECT SLUG]": slug,
        "[THREADING VERSION]": core_version(),
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content


def replace_label(text: str, label: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(label)}:.*$", flags=re.MULTILINE)
    replacement = f"{label}: {value}"
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return text.rstrip() + f"\n{replacement}\n"


def unique_history_path(project: Path, stamp: str) -> Path:
    folder = project / "history" / "upgrades"
    candidate = folder / f"{stamp}.md"
    index = 1
    while candidate.exists():
        candidate = folder / f"{stamp}-{index}.md"
        index += 1
    return candidate


def apply_project(plan: dict, stamp: str) -> list[str]:
    project = plan["path"]
    changes: list[str] = []
    for relative in plan["missing"]:
        if relative in {Path("threading.json"), Path("packs.md")}:
            continue
        source = TEMPLATE / relative
        destination = project / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            render_template(source, plan["title"], plan["slug"]), encoding="utf-8"
        )
        changes.append(f"created {relative}")

    state = dict(plan["state"])
    state["schema_version"] = CURRENT_SCHEMA
    state.setdefault("workspace_type", "managed")
    state["threading_version"] = core_version()
    state.setdefault("project_slug", plan["slug"])
    state["gsa_pack"] = {
        "enabled": plan["gsa_enabled"],
        "mode": "linked-read-only",
        "version": gsa_version() if plan["gsa_enabled"] else None,
    }
    history = state.get("upgrade_history")
    if not isinstance(history, list):
        history = []
        state["upgrade_history"] = history
    event = {
        "date": date.today().isoformat(),
        "from_schema": plan["schema_before"],
        "to_schema": CURRENT_SCHEMA,
        "from_threading_version": plan["version_before"],
        "to_threading_version": core_version(),
        "added_files": [str(path) for path in plan["missing"]],
    }
    if event not in history:
        history.append(event)
    write_state(project, state)
    changes.append("updated threading.json metadata")

    packs = project / "packs.md"
    if packs.exists():
        pack_text = packs.read_text(encoding="utf-8")
    else:
        pack_text = render_template(TEMPLATE / "packs.md", plan["title"], plan["slug"])
    pack_text = replace_label(pack_text, "Threading core version", core_version())
    pack_text = replace_label(
        pack_text, "GSA Pack", "enabled" if plan["gsa_enabled"] else "disabled"
    )
    pack_text = replace_label(
        pack_text,
        "GSA Pack version",
        gsa_version() if plan["gsa_enabled"] else "none",
    )
    pack_text = replace_label(pack_text, "Mode", "linked-read-only")
    packs.write_text(pack_text, encoding="utf-8")
    changes.append("refreshed packs.md metadata")

    history_path = unique_history_path(project, stamp)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(
        "# Threading Compatibility Upgrade\n\n"
        f"Date: {date.today().isoformat()}\n"
        f"Project: {plan['title']}\n"
        f"Schema: {plan['schema_before'] or 'unknown'} -> {CURRENT_SCHEMA}\n"
        f"Threading: {plan['version_before'] or 'unknown'} -> {core_version()}\n\n"
        "## Applied changes\n\n"
        + "\n".join(f"- {item}" for item in changes)
        + "\n\nExisting project content was preserved. Current State still requires project-owner confirmation.\n",
        encoding="utf-8",
    )
    changes.append(f"wrote {history_path.relative_to(project)}")
    return changes


def legacy_plan(profile: Path, output_root: Path) -> dict:
    if not any((profile / name).is_file() for name in KNOWN_LEGACY_FILES):
        return {
            "kind": "legacy",
            "path": profile,
            "blocked": True,
            "error": "no recognised legacy Threading files found",
            "action": "blocked",
        }
    try:
        slug = validate_slug(profile.name)
    except ValueError as error:
        return {
            "kind": "legacy",
            "path": profile,
            "blocked": True,
            "error": str(error),
            "action": "blocked",
        }
    destination = output_root / slug
    if not destination.exists():
        action = "create-managed-workspace"
    else:
        if not (destination / "CURRENT.md").is_file() and not (destination / "project.md").is_file():
            return {
                "kind": "legacy",
                "path": profile,
                "slug": slug,
                "destination": destination,
                "blocked": True,
                "error": "matching destination is not a recognised Managed Workspace",
                "action": "blocked",
            }
        state, _ = load_state(destination)
        legacy_sources = state.get("legacy_sources", [])
        attached = str(profile) in legacy_sources or state.get("migrated_from") == str(profile)
        snapshot = destination / "sources" / "legacy" / profile.name
        action = "already-connected" if attached or snapshot.exists() else "attach-review-copy"
    return {
        "kind": "legacy",
        "path": profile,
        "slug": slug,
        "destination": destination,
        "blocked": False,
        "error": None,
        "action": action,
    }


def append_legacy_source(project: Path, profile: Path, destination: Path) -> None:
    registry = project / "sources" / "source_registry.md"
    if not registry.exists():
        return
    text = registry.read_text(encoding="utf-8")
    pointer = str(profile)
    if pointer in text:
        return
    source_id = "L-" + hashlib.sha256(pointer.encode("utf-8")).hexdigest()[:8].upper()
    row = (
        f"| {source_id} | legacy-profile | {pointer} | migration authorised | "
        f"{destination.relative_to(project)} | historical |"
    )
    lines = text.splitlines()
    table_rows = [index for index, line in enumerate(lines) if line.startswith("|")]
    insert_at = (table_rows[-1] + 1) if table_rows else len(lines)
    lines.insert(insert_at, row)
    registry.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def attach_legacy(plan: dict, stamp: str) -> list[str]:
    profile = plan["path"]
    project = plan["destination"]
    destination = project / "sources" / "legacy" / profile.name
    destination.mkdir(parents=True, exist_ok=False)
    copied: list[str] = []
    for name in KNOWN_LEGACY_FILES:
        source = profile / name
        if source.is_file():
            shutil.copy2(source, destination / name)
            copied.append(name)
    (destination / "MIGRATION_REVIEW.md").write_text(
        "# Legacy Profile Review\n\n"
        f"Source profile: {profile}\n"
        f"Attached: {date.today().isoformat()}\n"
        "Status: candidate — project-owner review required\n\n"
        "The source profile was preserved unchanged. Review these records before promoting them:\n\n"
        "- `context.md` -> `project.md` and `CURRENT.md` candidates\n"
        "- `source_map.md` -> `sources/source_registry.md` candidates\n"
        "- `evidence_log.md` -> `evidence/evidence_log.md` candidates\n"
        "- `decision_log.md` -> `decisions/decision_log.md` candidates\n"
        "- `iteration_log.md` -> `iterations/iteration_log.md` candidates\n",
        encoding="utf-8",
    )
    append_legacy_source(project, profile, destination)
    state, error = load_state(project)
    if error:
        raise RuntimeError(error)
    sources = state.setdefault("legacy_sources", [])
    if str(profile) not in sources:
        sources.append(str(profile))
    state["threading_version"] = core_version()
    write_state(project, state)
    history_path = unique_history_path(project, stamp)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(
        "# Legacy Profile Attachment\n\n"
        f"Date: {date.today().isoformat()}\n"
        f"Source: {profile}\n"
        f"Review copy: {destination.relative_to(project)}\n"
        f"Copied files: {', '.join(copied) or 'none'}\n\n"
        "No legacy statement was promoted into Current State automatically.\n",
        encoding="utf-8",
    )
    return [
        f"attached legacy review copy at {destination.relative_to(project)}",
        f"copied {len(copied)} known legacy files",
        "preserved the source profile unchanged",
    ]


def create_from_legacy(plan: dict, output_root: Path) -> list[str]:
    command = [
        sys.executable,
        str(MIGRATOR),
        "--profile",
        str(plan["path"]),
        "--slug",
        plan["slug"],
        "--output-root",
        str(output_root),
    ]
    if LEGACY_ROOT not in plan["path"].parents:
        command.append("--allow-external-profile")
    if ROOT not in output_root.parents and output_root != ROOT:
        command.append("--allow-external-root")
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return [
        f"created Managed Workspace at {plan['destination']}",
        "copied known legacy records with candidate warnings",
        "preserved the source profile unchanged",
    ]


def write_report(path: Path, stamp: str, managed: list[dict], legacy: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Threading Upgrade Report",
        "",
        f"Generated: {stamp}",
        f"Threading core: {core_version()}",
        f"Managed Workspace schema: {CURRENT_SCHEMA}",
        "",
        "## Managed Workspaces",
        "",
    ]
    if not managed:
        lines.append("- None found.")
    for item in managed:
        status = "BLOCKED" if item.get("blocked") else (
            "updated" if item.get("applied") else "already-compatible"
        )
        details = item.get("applied") or item.get("changes") or ["already compatible"]
        lines.append(f"- `{item['path']}` — {status}")
        lines.extend(f"  - {detail}" for detail in details)
        if item.get("error"):
            lines.append(f"  - {item['error']}")
    lines.extend(["", "## Legacy Profiles", ""])
    if not legacy:
        lines.append("- None found.")
    for item in legacy:
        status = "BLOCKED" if item.get("blocked") else item.get("action")
        lines.append(f"- `{item['path']}` — {status}")
        lines.extend(f"  - {detail}" for detail in item.get("applied", []))
        if item.get("error"):
            lines.append(f"  - {item['error']}")
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "- Existing evidence, decisions, iterations and Current State were not overwritten.",
            "- External source files and complete chat archives remained in place.",
            "- Legacy content attached to an existing project remains candidate material until owner review.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        output_root = resolve_output_root(args.output_root, args.allow_external_root)
        if args.project:
            projects = [
                resolve_project(path, args.allow_external_project) for path in args.project
            ]
        else:
            projects = discover_projects(output_root)
        if args.legacy_profile:
            legacy_profiles = [
                resolve_legacy_profile(path, args.allow_external_legacy)
                for path in args.legacy_profile
            ]
        else:
            legacy_root = args.legacy_root.expanduser().resolve()
            if legacy_root != LEGACY_ROOT and not args.allow_external_legacy:
                raise ValueError("Use --allow-external-legacy for an external legacy root.")
            legacy_profiles = discover_legacy(legacy_root)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    managed_plans = [plan_project(project) for project in projects]
    legacy_plans = [legacy_plan(profile, output_root) for profile in legacy_profiles]
    blocked = [item for item in managed_plans + legacy_plans if item.get("blocked")]

    print("THREADING COMPATIBILITY UPGRADE")
    print(f"Core: {core_version()} / Managed Workspace schema: {CURRENT_SCHEMA}")
    print(f"Mode: {'APPLY' if args.apply else 'CHECK'}")
    print()
    print("Managed Workspaces")
    if not managed_plans:
        print("- none found")
    for item in managed_plans:
        if item["blocked"]:
            print(f"- {item['path'].name}: BLOCKED — {item['error']}")
        elif item["changes"]:
            print(f"- {item['path'].name}: " + "; ".join(item["changes"]))
        else:
            print(f"- {item['path'].name}: already compatible")
    print()
    print("Legacy Profiles")
    if not legacy_plans:
        print("- none found")
    for item in legacy_plans:
        if item["blocked"]:
            print(f"- {item['path'].name}: BLOCKED — {item['error']}")
        else:
            print(f"- {item['path'].name}: {item['action']}")

    if not args.apply:
        print("\nNo files changed. Re-run with --apply after reviewing this plan.")
        return 1 if blocked else 0

    stamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    for item in managed_plans:
        if item["blocked"] or not item["changes"]:
            continue
        item["applied"] = apply_project(item, stamp)

    for item in legacy_plans:
        if item["blocked"] or item["action"] == "already-connected":
            continue
        try:
            if item["action"] == "create-managed-workspace":
                item["applied"] = create_from_legacy(item, output_root)
            else:
                item["applied"] = attach_legacy(item, stamp)
        except RuntimeError as error:
            item["blocked"] = True
            item["error"] = str(error)
            blocked.append(item)

    report = args.report.expanduser().resolve() if args.report else (
        ROOT / "outputs" / "threading-upgrades" / f"{stamp}.md"
    )
    write_report(report, stamp, managed_plans, legacy_plans)
    print(f"\nUpgrade report: {report}")
    print("Existing project content was preserved; review candidates before promotion.")
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
