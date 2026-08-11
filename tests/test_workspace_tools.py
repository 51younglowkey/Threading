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
        codex_home = self.root / "codex-home"
        run(
            THREADING_TOOLS / "install_skill.py",
            "--codex-home",
            str(codex_home),
        )
        installed = codex_home / "skills" / "threading"
        self.assertTrue(installed.is_symlink())
        result = run(
            THREADING_TOOLS / "doctor.py",
            "--codex-home",
            str(codex_home),
            "--project",
            str(project),
        )
        self.assertIn("Summary:", result.stdout)
        self.assertNotIn("FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
