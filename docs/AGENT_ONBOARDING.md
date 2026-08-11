# Agent-native Project Onboarding

This is the first-run route for a person using Threading through Codex Agent or another repository-aware assistant. It is a conversation and a small set of local files, not a web form.

## Outcome

At the end of onboarding, the user should have:

1. a one-sentence working brief;
2. a named, user-owned project profile;
3. a map of where existing work lives (Figma, local folder, another repository or a mixed setup);
4. an explicit current phase and next action;
5. an explicit optional-pack choice (`none` by default, or a selected pack);
6. a clear boundary around what the Agent may inspect and what must stay outside the workspace.

The Agent should not demand a polished proposal. The first useful result is a truthful starting point with visible unknowns.

## Conversation protocol

Ask one question at a time and reflect the answer back in plain language before moving on. Use neutral labels for people and settings unless the user explicitly wants a name recorded in their private profile.

### 0. Set the boundary

Explain:

> Threading is the reusable reasoning layer. Your project profile is yours. We can record pointers to Figma, a local folder or another repository without copying those files into the reusable core. I will not inspect a location or upload anything unless you explicitly ask me to.

Ask whether the user wants:

- **Profile mode** — a local profile inside `profiles/local/<slug>/`, ignored by Git;
- **Separate project mode** — a new project directory or repository at a path the user explicitly chooses.

Do not create a broad directory, initialise a repository or move files before the user confirms the target path.

### 1. Name the work

Ask for a short project title and a lowercase slug. The slug should be stable, descriptive and free of personal names where possible.

Example: `community-repair-lab`.

After the title and slug, ask whether to load an optional method pack. Explain
that `none` is the default and keeps the profile generic; `gsa` adds the
independent Design Innovation academic pack. Do not infer this choice from the
project title or source paths.

### 2. Frame the brief

Ask:

- What are you trying to understand, change or make?
- Who or what is the relevant setting, described neutrally?
- What would a useful output look like?

Write the answer to `context.md`. Keep uncertainty visible with `[EVIDENCE NEEDED]` or `[DECISION PENDING]`.

### 3. Locate existing work

Ask where the project currently lives:

- Figma file or FigJam board;
- local desktop folder;
- another Git repository;
- a mixture of these;
- nowhere yet.

Record pointers in `source_map.md`. A pointer is not permission to inspect. Ask separately before reading a Figma file, local folder, repository, recording, correspondence or participant material.

### 3a. Orient without importing

Once the user grants permission, begin with a bounded orientation pass: inspect
only the top-level structure, named frames/pages or file list needed to identify
the project shape. Return a short summary with `observed`, `inferred` and
`unknown` separated. Ask before opening raw notes, recordings, participant
material or a large collection of files. Record the resulting source IDs and
limits, not a copied source dump.

### 4. Place the project in a phase

Use the user's own description to choose one current phase:

`framing` → `evidence` → `synthesis` → `prototype` → `testing` → `writing`.

If the phase is unclear, write `framing` and mark the decision as `[DECISION PENDING]`; do not pretend the project is further along.

### 5. Record boundaries

Ask only what is needed to work safely:

- Are there participant, consent, safeguarding or institutional restrictions?
- Which materials must stay outside the project profile?
- Is the Agent allowed to inspect the named sources now, or only record them?

Never ask the user to paste raw recordings, signed consent, private correspondence or sensitive identifiers into the reusable core.

## Bootstrap the profile

For Profile mode, use the bounded standard-library tool:

```bash
python3 90_scripts_tools/project_profile/init_project.py \
  --slug <project-slug> \
  --title "<project title>" \
  --pack none
```

The tool copies `profiles/_template/` to `profiles/local/<slug>/` and refuses to overwrite an existing profile. It does not import source material.

If the user explicitly selects the GSA Pack, use `--pack gsa` instead. The tool
copies only that pack into the user-owned profile; it never copies course PDFs or
the user's source files. Record the selection in `packs.md`.

If an existing profile later needs the GSA Pack, ask for explicit confirmation of
that profile and run the bounded loader:

```bash
python3 90_scripts_tools/project_profile/load_pack.py \
  --profile profiles/local/<project-slug> \
  --pack gsa
```

For an explicitly chosen profile outside the Threading workspace, add
`--allow-external-profile`. Use `--update` only after reviewing any local edits
inside the existing pack; it updates copied pack files in place.

For Separate project mode, confirm the exact destination first. If a profile-only
scaffold is useful outside the Threading clone, the bounded tool can be used with
an explicit external-root opt-in:

```bash
python3 90_scripts_tools/project_profile/init_project.py \
  --slug <project-slug> \
  --title "<project title>" \
  --output-root "/explicit/path/for/the/project" \
  --allow-external-root
```

The tool still refuses to overwrite an existing profile and never initialises a
Git repository or imports source files. If the user wants a separate Git
repository, confirm the exact folder and the repository action as a second,
explicit decision. Keep the Threading core and the user's project evidence
separate unless the user explicitly chooses another arrangement.

For a deterministic Dashboard view of an external profile, use:

```bash
python3 90_scripts_tools/project_profile/render_dashboard.py \
  --profile "/explicit/path/for/the/project" \
  --allow-external-profile
```

After bootstrapping, fill only the profile files:

- `context.md` — brief, setting, output and boundaries;
- `source_map.md` — pointers and inspection permissions;
- `status.md` — current phase, readiness and next action;
- `evidence_log.md` — source/evidence identifiers, not raw material;
- `decision_log.md` — reasons, alternatives and consequences;
- `iteration_log.md` — prototype/draft learning and next tests.

## First dashboard response

After the first intake, render `DASHBOARD.md` in the compact project format. Show one concrete next action, not a list of everything Threading can do. If a field is blank, show `needs input`; if support is missing, show `[EVIDENCE NEEDED]` rather than filling it in.

## Safety and handoff

- The local profile is user-owned and ignored by default.
- Do not commit `profiles/local/` without a separate privacy and provenance review.
- Do not copy Figma exports, desktop folders, PDFs, recordings, calendars or correspondence into the core.
- If the user wants to share the project with classmates, recommend a separate review of the profile and its Git history before publication.
- Threading provides workflow scaffolding; it does not provide ethics approval, legal advice or evidence that a design works.
