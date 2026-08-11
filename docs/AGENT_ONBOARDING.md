# Agent-native Project Adoption and Onboarding

Threading supports two starts:

1. **Adopt existing project** — default for a project already spread across
   Figma, local folders or chat history.
2. **Start new project** — a light scaffold when little work exists yet.

Both create a private Managed Workspace under `projects/local/<slug>/` unless
the user explicitly chooses an external destination.

## First explanation

Tell the user:

> Threading will create a local project knowledge workspace. Your raw Figma,
> desktop and chat sources may stay where they are. I will register pointers
> first, ask before inspection, and store only bounded derived knowledge with
> provenance. Imported material remains candidate until you confirm it.

Ask one question at a time.

## Adopt an existing project

1. Confirm project title and lowercase slug.
2. Ask where current material lives: local folder, Figma, Markdown chat archive
   or a mixture.
3. Ask whether to enable the linked GSA Pack.
4. Create the workspace with `adopt_project.py`. Register pointers only.
5. Ask permission for a bounded orientation pass over the named sources.
6. Separate `observed`, `inferred`, `candidate` and `unknown`.
7. For Figma, propose the most recent coherent current file/page/frame and ask
   the user to confirm it.
8. For existing chat Markdown, register it with `reconcile_chat_archive.py` and
   review selected conversations in batches.
9. Propose Current State: question, direction, insight/opportunity, working set,
   prototype/draft, uncertainty and one next move.
10. Only after confirmation, update `CURRENT.md` and matching logs.

Example creation command:

```bash
python3 90_scripts_tools/project_workspace/adopt_project.py \
  --slug my-project \
  --title "My project" \
  --pack gsa \
  --local-source "/explicit/project/source/folder" \
  --figma-source "explicit Figma file or page pointer" \
  --chat-source "/explicit/chat-export.md"
```

The command does not inspect or copy those sources.

## Start a new project

Use the same Managed Workspace scaffold with no source pointers. Ask for a
minimum working question, intended output and current uncertainty; do not demand
a polished brief.

## Existing v0.1 profile

Use `migrate_legacy_profile.py`. It creates a new Managed Workspace, copies known
records as candidates and preserves the legacy profile unchanged. Current State
requires user confirmation after migration.

## Completion

Render the project Dashboard. Show the enabled pack and one next move. Do not
mark sources, evidence or decisions ready merely because template files exist.
