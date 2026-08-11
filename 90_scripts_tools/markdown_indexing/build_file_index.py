#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "00_system_context" / "file_index.md"

IGNORED_PARTS = {
    ".academic_cache",
    ".git",
    ".next",
    ".venv",
    ".vinext",
    ".wrangler",
    "__pycache__",
    "backups",
    "dist",
    "node_modules",
    "outputs",
    "tmp",
}


def likely_role(path: Path) -> str:
    name = path.name.lower()
    parts = [p.lower() for p in path.parts]
    if "template" in name:
        return "Template"
    if name.endswith(".ics"):
        return "Calendar import file"
    if name.endswith(".csv"):
        return "Structured tracker"
    if "evidence" in name or "evidence" in parts:
        return "Evidence chain record"
    if "brief" in name or "context" in parts:
        return "Project context"
    if "schedule" in name or "calendar" in parts:
        return "Schedule / deadline record"
    if "checklist" in name:
        return "Checklist"
    if "quote" in name:
        return "Quote bank"
    if "log" in name:
        return "Log"
    return "Working file"


def project_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if str(rel).startswith("02_templates/"):
        return "Template library"
    if str(rel).startswith("00_system_context/"):
        return "System context"
    if str(rel).startswith("90_scripts_tools/"):
        return "Scripts / tools"
    return "Threading"


def file_type(path: Path) -> str:
    suffix = path.suffix.lower()
    return suffix[1:] if suffix else "directory/no extension"


def main() -> None:
    ignored_result = subprocess.run(
        ["git", "ls-files", "--others", "--ignored", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    git_ignored = {
        Path(item.decode("utf-8", errors="surrogateescape"))
        for item in ignored_result.stdout.split(b"\0")
        if item
    }

    rows = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_dir():
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.name == ".DS_Store" or path.suffix in {".bak", ".pyc"}:
            continue
        rel = path.relative_to(ROOT)
        if rel in git_ignored:
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        rows.append((rel, file_type(path), likely_role(path), project_for(path), modified))

    lines = [
        "# Threading File Index",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| File path | File type | Likely role | Project / sub-project | Last modified |",
        "|---|---|---|---|---|",
    ]
    for rel, kind, role, project, modified in rows:
        lines.append(f"| `{rel}` | {kind} | {role} | {project} | {modified} |")

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(rows)} files.")


if __name__ == "__main__":
    main()
