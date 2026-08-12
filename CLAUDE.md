# Threading — Claude Code Instructions

Threading is an Agent-native, evidence-led Research and Design project workflow.

Use this file as the parallel Claude Code routing layer for the reusable Threading workspace. `AGENTS.md` is the primary Codex route; keep the two files conceptually aligned. The optional GSA Pack is loaded only when selected by the user.

## Start here

1. Read `NOW.md`.
2. Read `core/system_context/workflow_rules.md` before framework changes.
3. Read `core/skill_library/skill_index.md` when routing a method, template or skill request.
4. Read only the files needed for the current task.

Before Dashboard or onboarding work on the first interaction in this clone, run
`python3 90_scripts_tools/threading/install_skill.py` from the repository root.
Then run `python3 90_scripts_tools/project_workspace/upgrade_workspaces.py` in
check mode. Show and confirm any compatibility plan before applying it; if
nothing needs attention, continue normally.
This required, idempotent setup links the Threading Skill into the supported
user-level Codex and Claude Code Skill locations so it remains available from
other workspaces. Never overwrite a different existing installation
automatically; report the conflict and continue with the repository instructions.
If user-level writes require permission, request that one bounded approval.

For `Update Threading` or `升级 Threading，并接续我已有的项目`, check the core
update first. After applying the Core update, show the resulting Compatibility
Plan and require a second confirmation before applying workspace changes.
Preserve existing project records, add only missing schema files and show the
generated Upgrade Report.

For a first-run or `Dashboard` request, read `DASHBOARD.md` and follow
`docs/AGENT_ONBOARDING.md`. Keep complete local project knowledge in
`projects/local/<slug>/`; retain `profiles/local/` only for legacy migration.
Ask permission before inspecting Figma files, desktop folders or chat archives.
Read a selected project's nested `AGENTS.md` and `CURRENT.md` first.

For GSA-specific taught-method routing, read `packs/gsa/PACK.md` only after the
user enables the linked, read-only pack. Show its available capabilities and
version after activation. The pack is an independent academic resource for
Design Innovation-related workflows, not an official GSA product.

## Behaviour

- Do not invent evidence, sources, quotations, dates, test results or decisions.
- Keep raw evidence, interpretation, claims and outputs distinct.
- Treat personal, participant-specific and institution-restricted information as sensitive.
- Keep the reusable core separate from any user-owned Managed Workspace.
- Treat taught methods as analytical frameworks, not proof of a project claim.
- Mark missing support with `[EVIDENCE NEEDED]`, `[SOURCE TO VERIFY]`, `[DECISION PENDING]` or `[DATE TO CONFIRM]`.
- Before adding future material or releases, repeat the privacy, provenance and Git-history review.
- Public users should use read/clone access; do not add collaborators merely for ordinary Threading use. Keep the optional PDF/image index local and source-authorised.
