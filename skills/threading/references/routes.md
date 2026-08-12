# Threading Routes

## Capability view

Explain in plain language that Threading can:

1. start a Research and Design project from a question, brief or goal;
2. accompany the project through framing, evidence, decisions, prototypes,
   testing, iteration and outcome;
3. join an existing complex project and preserve its history;
4. identify and confirm its current working state;
5. organise derived knowledge from Figma, local files and chat archives;
6. trace evidence, decisions, prototypes, tests and iterations;
7. use an explicitly enabled GSA Pack for methods, Provotyping, Reflection
   Document analysis and Stage 3 audit;
8. show one evidence-supported next move.

End with one useful prompt chosen from the situation: `帮我新建一个项目空间`,
`帮我接管这个现有项目` or `继续推进这个项目`.

## New-project start

1. Confirm the project title, slug, type and intended outcome.
2. Ask for the minimum working question and current uncertainty; do not demand
   a polished brief.
3. Ask whether the project is Research, Service Design, Product Design or another
   Research and Design context.
4. Create or select a Managed Workspace under `projects/local/`.
5. Start a source map and evidence plan without requiring source files yet.
6. Propose the first Current State and one next move.
7. Ask for confirmation before writing the proposal as the authoritative
   `CURRENT.md`.

## Existing-project adoption

1. Ask whether to create a Managed Workspace under `projects/local/` or use an
   explicitly chosen existing workspace.
2. Confirm project title and slug.
3. Record Figma, local-folder and chat-archive pointers without inspection.
4. Ask permission for a bounded orientation pass over named sources.
5. Separate `observed`, `inferred`, `candidate` and `unknown`.
6. Propose a current question, direction, working set and next action.
7. Ask the user to confirm or correct the proposal.
8. Only then update `CURRENT.md`. Preserve competing or older directions in
   the decision and iteration records as active, rejected or superseded.

Use `90_scripts_tools/project_workspace/adopt_project.py` for deterministic
workspace creation. It creates structure and pointers only; it does not inspect
or copy raw sources.

## Continue a project

1. Read the selected workspace's nested `AGENTS.md`, `CURRENT.md`, `packs.md`
   and bounded records.
2. Render the Dashboard and state what is confirmed, candidate, superseded or
   missing.
3. Ask which workstream to continue: evidence, decisions, prototype, testing,
   writing or project handover.
4. Propose one next move with its source or confirmation requirement.

## Figma evolution

1. Confirm the Figma files/pages/frames the user permits the Agent to inspect.
2. Begin with metadata and named top-level areas, not a whole-file dump.
3. Record observations in `sources/figma/evolution_map.md` with roles:
   `current-candidate`, `candidate`, `historical`, `reference` or `unknown`.
4. Store bounded extracted text in `sources/figma/derived/`, with the Figma
   pointer, inspected scope and date.
5. Propose the most recent coherent working set and explain the evidence.
6. Require user confirmation before marking anything `current` or changing
   `CURRENT.md`.
7. Record supersession instead of deleting earlier directions.

## Chat reconciliation

1. Ask the user to select the existing Markdown archive and grant inspection
   permission.
2. Run `reconcile_chat_archive.py` to register its hash, pointer and observed
   conversation headings. Include any earlier Codex analysis files as secondary
   notes when the user selects them.
3. Work through the generated reconciliation file in bounded batches.
4. Extract only candidate insights, decisions, rejected directions, open
   questions, source pointers and unsupported model claims.
5. Preserve the conversation/date locator. Do not treat model prose as evidence.
6. Compare candidates with confirmed Figma/local sources and `CURRENT.md`.
7. Ask the user to confirm promotion, rejection or supersession.
8. Promote confirmed items into the appropriate records; leave the raw archive
   unchanged.

## GSA Pack

Enable the pack through `manage_pack.py`. Show that it adds:

- Semester 1 and Semester 2 taught-method catalogues;
- Provotyping guidance;
- Reflection Document guidance-video analysis protocol;
- Stage 3 ILO, rubric and audit scaffolds.

Verify consequential wording against the authorised official source. Never
describe the pack as official or endorsed by GSA.

## Update and repair

Run `update_threading.py` without `--apply` first. Refuse an automatic update
when tracked core files are dirty, the branch has diverged or a fast-forward is
not possible. The Git update must not modify ignored local Managed Workspaces.

After the core update, run `upgrade_workspaces.py` in check mode and show the
compatibility plan. Do not apply workspace changes in the same unreviewed step
as a newly downloaded Core schema. With owner approval, apply it to:

- preserve every existing `CURRENT.md`, evidence, decision and iteration record;
- add only schema files that are missing;
- refresh `threading.json` and linked-pack version metadata;
- migrate a legacy profile into a new Managed Workspace when no destination exists;
- attach a review-only legacy copy when a matching Managed Workspace already exists;
- write an upgrade report and project-local upgrade history.

Never scan broad external folders, overwrite project knowledge or promote
legacy/chat content into Current State automatically.

Use `migrate_legacy_profile.py` for old `profiles/local/` projects. It copies
known records into a new Managed Workspace and leaves the legacy profile intact.
Use `doctor.py` after installation, migration or update.
