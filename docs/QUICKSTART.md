# Threading Quickstart

This guide creates a small, user-owned project profile without adding personal material to the reusable core.

## Start through the Agent Dashboard

Open the repository in Codex Agent and say **“Dashboard”**. The Agent will show
the capabilities, ask whether to use Profile mode or a separate project path,
and then run the intake in `docs/AGENT_ONBOARDING.md`. You do not need to paste
your whole project into chat.

## 1. Choose a project space

For the simplest local setup, ask the Agent to create Profile mode. It will run:

```bash
python3 90_scripts_tools/project_profile/init_project.py \
  --slug my-project \
  --title "My project" \
  --pack none
```

This creates `profiles/local/my-project/`, which is ignored by Git. It copies
templates only; it does not import Figma files, desktop folders, PDFs or other
source material.

The optional GSA Pack can be selected explicitly during initialization:

```bash
python3 90_scripts_tools/project_profile/init_project.py \
  --slug my-project \
  --title "My project" \
  --pack gsa
```

`--pack none` is the default. It creates no `packs/gsa/` directory. `--pack gsa`
copies the independent Design Innovation academic pack into the user-owned
profile.

If an existing profile later needs the pack, load it explicitly:

```bash
python3 90_scripts_tools/project_profile/load_pack.py \
  --profile profiles/local/my-project \
  --pack gsa
```

Use `--update` only after reviewing local edits to an already copied pack. For a
profile outside this repository, add `--allow-external-profile`.

You can also choose a separate project directory or repository. Confirm the
exact destination before creating it, and keep that project evidence separate
from the reusable Threading core.

## 2. Copy the profile template manually (if needed)

Copy `profiles/_template/` to a new local project folder, for example:

```text
profiles/local/my-project/
```

The `profiles/local/` path is ignored by Git by default. If a profile will be shared, review it as a separate public artefact first.

## 3. Write the project context

Start with:

- the question or brief;
- the relevant people, systems or setting, using neutral labels where possible;
- what is known, assumed and still missing;
- evidence boundaries, consent requirements and exclusions;
- the intended output and current status.

Do not begin with a polished claim. Begin with what the project can actually support.

## 4. Select a method

If the GSA Pack is loaded, read the relevant entry in:

- `packs/gsa/methods/semester1-method-catalog.md`;
- `packs/gsa/methods/semester2-method-catalog.md`;
- `packs/gsa/methods/provotyping-for-participatory-innovation.md`;
- `packs/gsa/reflection-document/video-analysis-method.md`;
- `packs/gsa/assessment/stage3-assessment-guide.md`.

Use the assessment guide as an operational audit scaffold only; verify current
requirements against the authorised official assessment form.

Use `20_skill_library/skills/apply-taught-methods/SKILL.md` to record why the method fits, what inputs it uses, what it produces and what it cannot establish.

## 5. Keep the chain visible

For each meaningful decision, update the evidence and decision records:

```text
source → note → interpretation → claim → criterion → concept → test → iteration
```

Use `[EVIDENCE NEEDED]`, `[SOURCE TO VERIFY]` or `[DECISION PENDING]` when a link is missing.

## 6. Run a privacy check before sharing

Check for names, email addresses, schedules, private correspondence, raw recordings, identifiable images, consent records, absolute paths and institution-restricted files. Remove or anonymise them before moving anything from `profiles/local/` into a shared repository.

## 7. Remember the boundary

Threading is a reasoning and traceability scaffold. It does not provide ethics approval, legal advice, institutional policy or evidence that a proposed intervention works.
