#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKUP_DIR = ROOT / "backups"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: backup_file.py <path-relative-to-workspace-or-absolute-path>")
        return 2

    target = Path(sys.argv[1])
    if not target.is_absolute():
        target = ROOT / target
    target = target.resolve()

    if not target.exists() or not target.is_file():
        print(f"File not found: {target}")
        return 1

    if ROOT not in target.parents and target != ROOT:
        print("Refusing to back up files outside this workspace.")
        return 1

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rel = target.relative_to(ROOT)
    safe_name = "__".join(rel.parts)
    backup_path = BACKUP_DIR / f"{timestamp}__{safe_name}"
    BACKUP_DIR.mkdir(exist_ok=True)
    shutil.copy2(target, backup_path)
    print(backup_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
