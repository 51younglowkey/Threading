---
name: threading
description: Run a local Research and Design project workflow with Threading from a new project, an existing project or any continuing stage. Use for natural-language requests such as Dashboard, 新建项目, 接管项目, 继续推进项目, what can you do, find the current direction, map Figma evolution, 整理已经导入的聊天记录, find evidence gaps, load or use the GSA Pack, review evidence and decisions, migrate an old Threading profile, diagnose Threading, or update Threading.
---

# Threading

Use Threading as the operating layer for a user-owned local project. Keep the
public core, local project knowledge and raw sources separate.

## Resolve the core

1. If this skill is symlinked from a Threading clone, resolve the skill path and
   use the repository containing `VERSION`, `DASHBOARD.md` and `packs/gsa/`.
2. For a copied installation, read `references/core-path.txt` when it exists.
3. If no core can be located, ask for the Threading clone path; do not scan a
   home directory or broad disk location.

## Route the request

- `Dashboard`, `status`, `overview`, `next step`: read the selected project's
  `CURRENT.md`, `packs.md` and bounded records; use the core Dashboard contract.
- `新建项目`, `start a new project`, `set up a project`: follow the new-project
  route in `references/routes.md`, create or select a Managed Workspace and begin
  with the working question, intended outcome and uncertainty.
- `接管项目`, `adopt project`, `orient this project`: follow
  `references/routes.md#existing-project-adoption`.
- `继续推进项目`, `continue this project`, `keep working`: read the selected
  Managed Workspace and follow the current-state / next-move route.
- `整理已经导入的聊天记录`, `reconcile chat archive`: follow
  `references/routes.md#chat-reconciliation`.
- `map Figma`, `current Figma`, `which design is current`: follow
  `references/routes.md#figma-evolution`.
- `load pack gsa`, `use GSA Pack`: enable the linked pack for the selected
  workspace, then show its capabilities and version.
- `update Threading`, `升级 Threading，并接续我已有的项目`: run the safe core
  update check first. After approval, apply the Core update and show the
  resulting compatibility plan. Apply workspaces only after the user has seen
  that plan; report Managed Workspace repairs and legacy migrations.
- `what can you do`, `help`: render the concise capability view in
  `references/routes.md#capability-view`.
- `evidence gaps`, `find the evidence gaps`, `找出证据缺口`: inspect bounded
  project records and report unsupported claims, missing source pointers and
  pending confirmations without inventing support.

## Non-negotiable behaviour

- Require a selected Managed Workspace before writing project knowledge.
- Ask before inspecting a local path, Figma source or chat archive.
- Preserve raw sources; store derived local knowledge with source pointer,
  extraction date, scope and status.
- Treat imported or model-generated material as `candidate` until the user
  confirms it.
- Let the Agent propose a current Figma file/page/frame; require user
  confirmation before changing `CURRENT.md`.
- Never delete or silently rewrite superseded decisions. Record the new state
  and retain the earlier state in history.
- Keep `projects/local/` private and Git-ignored.
- Treat the linked GSA Pack as read-only. Write project analysis into the local
  workspace, never into `packs/gsa/`.

Read `references/workspace-schema.md` when creating, migrating or repairing a
Managed Workspace. Read only the route needed for the current request.
