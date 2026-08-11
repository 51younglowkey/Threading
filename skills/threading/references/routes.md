# Threading Routes

## Capability view

Explain in plain language that Threading can:

1. adopt an existing complex project;
2. identify and confirm its current working state;
3. organise derived knowledge from Figma, local files and chat archives;
4. trace evidence, decisions, prototypes, tests and iterations;
5. use an explicitly enabled GSA Pack for methods, Provotyping, Reflection
   Document analysis and Stage 3 audit;
6. show one evidence-supported next move.

End with one useful prompt: `帮我接管这个现有项目`.

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
not possible. Local Managed Workspaces are ignored and must not be modified by
the Git update.

Use `migrate_legacy_profile.py` for old `profiles/local/` projects. It copies
known records into a new Managed Workspace and leaves the legacy profile intact.
Use `doctor.py` after installation, migration or update.
