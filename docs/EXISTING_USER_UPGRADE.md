# Upgrade Existing Threading Users to v0.2

Use this once for an existing clone. Do not re-clone and do not delete the old
profile, chat archive or source folder.

## 1. Update the public core

```bash
cd /path/to/Threading
git pull --ff-only origin main
```

## 2. Register the natural-language Skill

Open the updated clone in Codex or Claude Code. The Agent registers the Skill
automatically on the first interaction. To complete the registration directly,
run:

```bash
python3 90_scripts_tools/threading/install_skill.py
```

The default symlink registration covers both supported Agents, follows future
Git updates and migrates an obsolete v0.2 symlink when it points to this clone.

## 3. Check and connect existing project knowledge

After the Core update, preview every recognised Managed Workspace and Legacy
Profile:

```bash
python3 90_scripts_tools/project_workspace/upgrade_workspaces.py
```

After reviewing the plan:

```bash
python3 90_scripts_tools/project_workspace/upgrade_workspaces.py --apply
```

This preserves existing project records, adds missing schema files and writes
an Upgrade Report.

## 4. Create or migrate local project knowledge manually

For an old `profiles/local/<slug>/` profile:

```bash
python3 90_scripts_tools/project_workspace/migrate_legacy_profile.py \
  --profile profiles/local/<slug>
```

For a project that was loaded without a profile:

```text
帮我接管这个现有项目
```

Point Threading to the existing local folder, Figma and chat Markdown. The
sources remain in place; derived knowledge enters `projects/local/<slug>/`.

## 5. Reconcile the already imported chats

```text
整理已经导入的聊天记录
```

Select the existing Markdown and any earlier Codex analysis notes.

## 6. Enable and verify the linked GSA Pack

```text
加载 GSA Pack，并告诉我现在多了哪些能力
```

## 7. Verify

```bash
python3 90_scripts_tools/threading/doctor.py \
  --project projects/local/<slug>
```

Start a new Codex task and say `Threading Dashboard`.
