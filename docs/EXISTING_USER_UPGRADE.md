# Upgrade Existing Threading Users to v0.2

Use this once for an existing clone. Do not re-clone and do not delete the old
profile, chat archive or source folder.

## 1. Update the public core

```bash
cd /path/to/Threading
git pull --ff-only origin main
```

## 2. Install the natural-language skill

```bash
python3 90_scripts_tools/threading/install_skill.py
```

The default symlink installation follows future Git updates.

## 3. Create or migrate local project knowledge

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

## 4. Reconcile the already imported chats

```text
整理已经导入的聊天记录
```

Select the existing Markdown and any earlier Codex analysis notes.

## 5. Enable and verify the linked GSA Pack

```text
加载 GSA Pack，并告诉我现在多了哪些能力
```

## 6. Verify

```bash
python3 90_scripts_tools/threading/doctor.py \
  --project projects/local/<slug>
```

Start a new Codex task and say `Threading Dashboard`.
