# GSA Pack — Design Innovation Academic Pack

ID: `gsa`
Status: optional; linked and read-only; not enabled by default
Dependency: Threading core for Dashboard, profile, evidence-chain and generic skill routing
Scope: academic methods, reflection-document analysis and Stage 3 assessment guidance useful for Design Innovation-related study and project work
Initial audience: the current target GSA Stage 3 cohort; verify the authorised source version locally before reuse with another cohort

This is an independent academic pack for Design Innovation-related workflows. It
is a situated, course-derived supplement to the generic Threading core; it is
not required for the core dashboard, profile or evidence-chain workflow.

## Contents

- `methods/semester1-method-catalog.md` — 19 Semester 1 method entries;
- `methods/semester2-method-catalog.md` — 15 Semester 2 method entries;
- `methods/provotyping-for-participatory-innovation.md` — independently authored
  operational method note based on a cited public paper;
- `reflection-document/video-analysis-method.md` — reusable protocol for
  analysing programme guidance videos without importing restricted recordings;
- `assessment/stage3-assessment-guide.md` — ILO, rubric, grade-band and audit
  guide derived from the current official assessment forms.

## Activation behaviour

Select it when creating a Managed Workspace:

```bash
python3 90_scripts_tools/project_workspace/adopt_project.py \
  --slug my-project \
  --title "My project" \
  --pack gsa
```

The Agent should enable this pack only when the user selects it or says “load
pack gsa”. Activation records `enabled`, `linked-read-only` and the pack version
inside the local project. It does not copy the pack into the project. Threading
updates change the linked core; local project analysis remains separate.

## Provenance and boundary

The method catalogues and reflection protocol are paraphrased guidance and source
locators. Course PDFs, slides, assessment material, guidance videos and other
restricted originals are not bundled. A course anchor is provenance, not a
runtime dependency or permission to redistribute the source material.

The assessment guide is an operational paraphrase and audit scaffold. The
current official assessment form remains the authority for exact wording,
current requirements and consequential grading decisions.

This pack is not produced, approved, sponsored or endorsed by Glasgow School of
Art (GSA). “GSA” identifies the academic context of this optional pack; it does
not indicate institutional ownership, affiliation or policy authority.

Before sharing or adapting the pack, read the core repository's `NOTICE.md`,
`THIRD_PARTY_NOTICES.md` and `docs/PROVENANCE_AND_LICENSING.md`.
