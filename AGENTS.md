# Threading Instructions

Threading is a reusable academic and design-research workspace. The generic core is available to every project; an independent GSA Pack provides an optional situated academic context for Design Innovation-related workflows. Each person's project context, evidence and decisions remain their own.

Reply in Chinese by default when the user writes in Chinese. Preserve useful English academic, research and design terms where translation would reduce precision.

## Start and routing

1. Read `NOW.md` for the compact route.
2. Read `00_system_context/workflow_rules.md` before substantive framework changes.
3. Read the closest `AGENTS.md` for any nested project added later.
4. Read only the current files needed for the task; do not scan every source, export or generated file by default.
5. Use `20_skill_library/skill_index.md` to route method and framework requests.
6. Treat `CLAUDE.md` as the parallel Claude Code routing layer.

### Optional packs

- Load the generic Threading core by default; do not load an optional pack unless the user selects it.
- When the user selects the GSA Pack, or says “load pack gsa”, read `packs/gsa/PACK.md` before using its methods, reflection-document tool or assessment guide.
- During profile initialization, `--pack none` is the default and creates no `packs/gsa/` directory; `--pack gsa` copies the pack into the user-owned profile.
- Describe the GSA Pack as an independent academic pack for Design Innovation-related workflows. Never imply that it is official, endorsed or institutionally owned by GSA.

### Agent dashboard and first run

- On a first interaction, or whenever the user asks for `Dashboard`, `status`, `overview` or `next step`, read `DASHBOARD.md` and render its compact text view.
- If no project profile is selected, follow `docs/AGENT_ONBOARDING.md` one question at a time. Do not invent a project brief or silently choose between multiple profiles.
- User-owned project context belongs in `profiles/local/<slug>/` (ignored by Git) or in a separately controlled project repository. Keep it out of the reusable core.
- Record pointers to Figma files, desktop folders and other repositories in `source_map.md`; a pointer is not permission to inspect the source.
- Ask for explicit permission before reading a named local or connected source. Never import raw project material automatically.
- Use `90_scripts_tools/project_profile/init_project.py` only after the user confirms the profile location and slug. Use `render_dashboard.py` when a deterministic text status is useful.
- For an existing profile, use `90_scripts_tools/project_profile/load_pack.py` only after the user explicitly selects the pack and target profile; use `--allow-external-profile` for an external profile.
- The PDF/image OCR index is an optional local tool. Read its README and require an explicitly authorised source directory before using it; its OCR output is a locator, not automatic project evidence.

## Non-negotiable rules

- Never invent sources, quotations, participant data, citations, page numbers, feedback, test results, dates, findings or design decisions.
- Keep raw evidence separate from cleaned notes, interpretation, synthesis and final outputs.
- Preserve the distinction between evidence, quotation, observation, interpretation, insight, criterion, decision, claim and limitation.
- Preserve traceability for design research: `evidence -> insight -> opportunity -> criteria -> concept -> prototype -> testing -> iteration -> claimed impact`.
- Preserve traceability for academic writing: `source -> note -> interpretation -> claim -> evidence -> counterpoint/limitation -> section -> final argument`.
- Mark missing support explicitly with `[EVIDENCE NEEDED]`, `[SOURCE TO VERIFY]`, `[DECISION PENDING]` or `[DATE TO CONFIRM]`.
- Treat names, contact details, consent records and identifiable raw material as sensitive.
- Do not publish personal, participant-specific, institution-restricted or project-specific material in a reusable edition.
- Read an important file before editing it. Do not overwrite evidence or historical decisions without an explicit reason.
- A method or framework is analytical machinery, not empirical proof. Do not turn a diagram or hypothesis into a validated claim without matching evidence.

## Workspace boundaries

- The reusable core contains rules, methods, templates and tools.
- A user-owned project profile may contain context, evidence, decisions and outputs, but it should not be mixed into the reusable core.
- Calendar, timetable, deadline and personal-administration records are not part of this edition.
- A future public profile must use neutral examples or user-supplied project data and must document its provenance.

## Repository and generated files

- Keep one repository for this edition unless a later profile genuinely requires independent access control.
- Do not add raw participant material, personal correspondence, private academic administration, local caches, dependencies or generated exports to the public repository.
- Change source files rather than generated output when a source exists.
- Review the complete working tree and Git history before any external publication.

## Lifecycle

Reusable rules and methods may evolve. Historical evidence and user-owned project records should remain dated and should not be silently modernised. If a future profile is archived, preserve its record and mark the lifecycle explicitly.
