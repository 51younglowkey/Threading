from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
WORKSPACE_TOOLS = ROOT / "90_scripts_tools" / "project_workspace"
THREADING_TOOLS = ROOT / "90_scripts_tools" / "threading"
UPGRADE_TOOL = WORKSPACE_TOOLS / "upgrade_workspaces.py"


def run(script: Path, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [PYTHON, str(script), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != expect:
        raise AssertionError(
            f"{script.name} returned {result.returncode}, expected {expect}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class WorkspaceToolsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="threading-v02-test-")
        self.root = Path(self.temp.name)
        self.projects = self.root / "projects"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def adopt(self, slug: str = "test-project", pack: str = "gsa") -> Path:
        source = self.root / "source-folder"
        source.mkdir(exist_ok=True)
        run(
            WORKSPACE_TOOLS / "adopt_project.py",
            "--slug",
            slug,
            "--title",
            "Test Project",
            "--pack",
            pack,
            "--local-source",
            str(source),
            "--figma-source",
            "Figma file / Current page",
            "--output-root",
            str(self.projects),
            "--allow-external-root",
        )
        return self.projects / slug

    def test_adopt_dashboard_and_linked_pack(self) -> None:
        project = self.adopt()
        self.assertTrue((project / "CURRENT.md").is_file())
        state = json.loads((project / "threading.json").read_text(encoding="utf-8"))
        self.assertEqual(state["schema_version"], 2)
        self.assertTrue(state["gsa_pack"]["enabled"])
        self.assertEqual(state["gsa_pack"]["mode"], "linked-read-only")
        self.assertFalse((project / "packs" / "gsa").exists())

        rendered = run(
            WORKSPACE_TOOLS / "render_dashboard.py",
            "--project",
            str(project),
            "--allow-external-project",
        )
        self.assertIn("Test Project", rendered.stdout)
        self.assertIn("GSA PACK        enabled", rendered.stdout)

        run(
            WORKSPACE_TOOLS / "manage_pack.py",
            "--project",
            str(project),
            "--disable-gsa",
            "--allow-external-project",
        )
        state = json.loads((project / "threading.json").read_text(encoding="utf-8"))
        self.assertFalse(state["gsa_pack"]["enabled"])

    def test_register_existing_chat_without_promotion(self) -> None:
        project = self.adopt(pack="none")
        archive = self.root / "chat-export.md"
        archive.write_text(
            "# Export\n\n## Early direction\nUser: Maybe option A.\n\n"
            "## Later direction\nUser: We are now exploring option B.\n",
            encoding="utf-8",
        )
        result = run(
            WORKSPACE_TOOLS / "reconcile_chat_archive.py",
            "--project",
            str(project),
            "--allow-external-project",
            "--archive",
            str(archive),
        )
        self.assertIn("No candidate was promoted", result.stdout)
        inventory = (project / "sources" / "chats" / "chat_inventory.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("chat-export", inventory)
        reviews = list((project / "sources" / "chats" / "reconciliation").glob("CH-*.md"))
        self.assertEqual(len(reviews), 1)
        self.assertIn("Early direction", reviews[0].read_text(encoding="utf-8"))

        duplicate = subprocess.run(
            [
                PYTHON,
                str(WORKSPACE_TOOLS / "reconcile_chat_archive.py"),
                "--project",
                str(project),
                "--allow-external-project",
                "--archive",
                str(archive),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn("already registered", duplicate.stderr)

    def test_legacy_migration_preserves_source(self) -> None:
        legacy = self.root / "legacy-profile"
        legacy.mkdir()
        (legacy / "context.md").write_text(
            "# Project Context\n\nProject or module: Legacy Project\n"
            "Working question: What is current?\n"
            "Current hypothesis or design proposition: Candidate direction\n",
            encoding="utf-8",
        )
        (legacy / "status.md").write_text(
            "Current phase: synthesis\nNext action: Confirm the working set\n",
            encoding="utf-8",
        )
        (legacy / "packs.md").write_text("Optional packs: gsa\n", encoding="utf-8")
        original = (legacy / "context.md").read_text(encoding="utf-8")

        run(
            WORKSPACE_TOOLS / "migrate_legacy_profile.py",
            "--profile",
            str(legacy),
            "--allow-external-profile",
            "--slug",
            "legacy-project",
            "--output-root",
            str(self.projects),
            "--allow-external-root",
        )
        migrated = self.projects / "legacy-project"
        self.assertTrue((migrated / "CURRENT.md").is_file())
        self.assertIn("needs confirmation", (migrated / "CURRENT.md").read_text(encoding="utf-8"))
        self.assertEqual(original, (legacy / "context.md").read_text(encoding="utf-8"))
        state = json.loads((migrated / "threading.json").read_text(encoding="utf-8"))
        self.assertTrue(state["gsa_pack"]["enabled"])

    def test_skill_symlink_install_and_doctor(self) -> None:
        project = self.adopt(pack="gsa")
        user_home = self.root / "user-home"
        legacy = user_home / ".codex" / "skills" / "threading"
        legacy.parent.mkdir(parents=True)
        legacy.symlink_to(ROOT / "skills" / "threading", target_is_directory=True)
        run(
            THREADING_TOOLS / "install_skill.py",
            "--home",
            str(user_home),
        )
        codex_skill = user_home / ".agents" / "skills" / "threading"
        claude_skill = user_home / ".claude" / "skills" / "threading"
        self.assertTrue(codex_skill.is_symlink())
        self.assertTrue(claude_skill.is_symlink())
        self.assertFalse(legacy.exists() or legacy.is_symlink())
        repeated = run(
            THREADING_TOOLS / "install_skill.py",
            "--home",
            str(user_home),
        )
        self.assertEqual(repeated.stdout.count("already linked"), 2)
        result = run(
            THREADING_TOOLS / "doctor.py",
            "--home",
            str(user_home),
            "--project",
            str(project),
        )
        self.assertIn("Summary:", result.stdout)
        self.assertNotIn("FAIL", result.stdout)

    def test_skill_registration_preserves_conflicting_installation(self) -> None:
        user_home = self.root / "conflict-home"
        existing = user_home / ".agents" / "skills" / "threading"
        existing.mkdir(parents=True)
        marker = existing / "SKILL.md"
        marker.write_text("existing skill\n", encoding="utf-8")

        result = run(
            THREADING_TOOLS / "install_skill.py",
            "--home",
            str(user_home),
            expect=1,
        )

        self.assertIn("It was not changed", result.stderr)
        self.assertEqual(marker.read_text(encoding="utf-8"), "existing skill\n")
        self.assertFalse((user_home / ".claude" / "skills" / "threading").exists())

    def test_compatibility_upgrade_repairs_without_overwriting(self) -> None:
        project = self.adopt(pack="gsa")
        current_path = project / "CURRENT.md"
        evidence_path = project / "evidence" / "evidence_log.md"
        current_before = current_path.read_text(encoding="utf-8")
        evidence_path.write_text(
            evidence_path.read_text(encoding="utf-8") + "\nOWNER RECORD — preserve exactly\n",
            encoding="utf-8",
        )
        missing = project / "sources" / "chats" / "candidate_records.md"
        missing.unlink()
        state_path = project / "threading.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["schema_version"] = 1
        state["threading_version"] = "0.1.0"
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        report = self.root / "upgrade-report.md"

        check = run(
            UPGRADE_TOOL,
            "--project",
            str(project),
            "--allow-external-project",
            "--report",
            str(report),
        )
        self.assertIn("Mode: CHECK", check.stdout)
        self.assertFalse(missing.exists())
        self.assertFalse(report.exists())

        run(
            UPGRADE_TOOL,
            "--project",
            str(project),
            "--allow-external-project",
            "--apply",
            "--report",
            str(report),
        )
        self.assertTrue(missing.is_file())
        self.assertEqual(current_before, current_path.read_text(encoding="utf-8"))
        self.assertIn("OWNER RECORD — preserve exactly", evidence_path.read_text(encoding="utf-8"))
        upgraded = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(upgraded["schema_version"], 2)
        self.assertEqual(upgraded["threading_version"], (ROOT / "VERSION").read_text().strip())
        self.assertTrue(upgraded["upgrade_history"])
        self.assertTrue(report.is_file())
        self.assertTrue(any((project / "history" / "upgrades").glob("*.md")))

    def test_compatibility_upgrade_attaches_legacy_for_review(self) -> None:
        project = self.adopt(slug="legacy-project", pack="none")
        legacy = self.root / "legacy-project"
        legacy.mkdir()
        source_context = "# Legacy Context\n\nWorking question: What changed?\n"
        (legacy / "context.md").write_text(source_context, encoding="utf-8")
        report = self.root / "legacy-upgrade-report.md"

        run(
            UPGRADE_TOOL,
            "--project",
            str(project),
            "--legacy-profile",
            str(legacy),
            "--output-root",
            str(self.projects),
            "--allow-external-project",
            "--allow-external-root",
            "--allow-external-legacy",
            "--apply",
            "--report",
            str(report),
        )

        review = project / "sources" / "legacy" / "legacy-project"
        self.assertEqual(source_context, (legacy / "context.md").read_text(encoding="utf-8"))
        self.assertEqual(source_context, (review / "context.md").read_text(encoding="utf-8"))
        self.assertTrue((review / "MIGRATION_REVIEW.md").is_file())
        self.assertIn(
            str(legacy),
            (project / "sources" / "source_registry.md").read_text(encoding="utf-8"),
        )
        state = json.loads((project / "threading.json").read_text(encoding="utf-8"))
        self.assertIn(str(legacy.resolve()), state["legacy_sources"])

    def test_compatibility_upgrade_creates_workspace_from_legacy(self) -> None:
        legacy_root = self.root / "legacy-root"
        legacy = legacy_root / "new-legacy-project"
        legacy.mkdir(parents=True)
        (legacy / "context.md").write_text(
            "# Project Context\n\nProject or module: New Legacy Project\n",
            encoding="utf-8",
        )
        report = self.root / "new-legacy-report.md"

        run(
            UPGRADE_TOOL,
            "--legacy-profile",
            str(legacy),
            "--output-root",
            str(self.projects),
            "--allow-external-root",
            "--allow-external-legacy",
            "--apply",
            "--report",
            str(report),
        )

        project = self.projects / "new-legacy-project"
        self.assertTrue((project / "CURRENT.md").is_file())
        self.assertTrue((project / "legacy_snapshot" / "context.md").is_file())
        self.assertIn(
            "needs confirmation", (project / "CURRENT.md").read_text(encoding="utf-8")
        )
        self.assertTrue((legacy / "context.md").is_file())
        self.assertTrue(report.is_file())

    def test_compatibility_upgrade_blocks_newer_schema(self) -> None:
        project = self.adopt(slug="future-project", pack="none")
        state_path = project / "threading.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["schema_version"] = 99
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

        result = run(
            UPGRADE_TOOL,
            "--project",
            str(project),
            "--allow-external-project",
            expect=1,
        )
        self.assertIn("BLOCKED", result.stdout)
        unchanged = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(unchanged["schema_version"], 99)


if __name__ == "__main__":
    unittest.main()
