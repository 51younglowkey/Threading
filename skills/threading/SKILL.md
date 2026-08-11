---
name: threading
description: Organise an existing or new local research, design or academic project with Threading. Use for natural-language requests such as Dashboard, 接管项目, what can you do, find the current direction, map Figma evolution, 整理已经导入的聊天记录, load or use the GSA Pack, review evidence and decisions, migrate an old Threading profile, diagnose Threading, or update Threading.
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
- `接管项目`, `adopt project`, `orient this project`: follow
  `references/routes.md#existing-project-adoption`.
- `整理已经导入的聊天记录`, `reconcile chat archive`: follow
  `references/routes.md#chat-reconciliation`.
- `map Figma`, `current Figma`, `which design is current`: follow
  `references/routes.md#figma-evolution`.
- `load pack gsa`, `use GSA Pack`: enable the linked pack for the selected
  workspace, then show its capabilities and version.
- `update Threading`: run the safe check first; apply only after reporting local
  tracked changes and the proposed update.
- `what can you do`, `help`: render the concise capability view in
  `references/routes.md#capability-view`.

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
