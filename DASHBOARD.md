# Threading Dashboard

This is the Agent-facing text dashboard for Threading. Read it when a user asks for the dashboard, status, overview, or next step, and when a new user starts without a project profile.

Threading is a local-first reasoning workspace. It helps a project move from a brief to traceable evidence, decisions, prototypes and writing. It does not upload a project, invent evidence or replace academic judgement.

## First-run view

```text
THREADING / FIRST RUN
────────────────────────────────────────────────────────────────
Workspace       Threading
Mode            Reusable core + user-owned local project profile
Packs           none loaded by default
Project         Not started
Next move       Start a short project intake
Privacy         Project files stay in the user's chosen local space
                 unless the user explicitly asks the Agent to inspect them
────────────────────────────────────────────────────────────────
```

If `profiles/local/` contains a project profile, replace the first-run view with the project view below. If more than one profile exists, ask which one to show; do not silently choose.

## Capability map

```text
BRIEF → SOURCES → EVIDENCE → INTERPRETATION → DECISION → PROTOTYPE → TEST → ITERATION
```

- **Frame** — turn an initial brief into a working question, intended output and constraints.
- **Locate** — record where the project already lives: Figma, a local folder, another repository or a mixed setup.
- **Trace** — keep source material, notes, interpretations, claims and limitations distinct.
- **Choose** — make decisions visible, including alternatives, reasons and what remains uncertain.
- **Apply** — select a method from the generic core or an explicitly loaded pack because it answers a named analytical need.
- **Build and test** — connect prototype versions to learning questions, observations and iteration decisions.
- **Reflect** — prepare a retrospective or submission review without turning a framework into proof.

## Project view template

When a profile exists, render a compact view like this. Use only information found in the profile files; never infer progress from the existence of a file.

```text
THREADING / PROJECT DASHBOARD
────────────────────────────────────────────────────────────────
Project         <title>
Profile         profiles/local/<slug>/
Packs           <none | gsa>
Status          <draft | active | maintenance | archived>
Phase           <framing | evidence | synthesis | prototype | testing | writing>
Last update     <date or [DATE TO CONFIRM]>

READINESS
  Brief         <ready | needs input | blocked | not started>
  Sources       <mapped | needs input | not started>
  Evidence      <traceable | needs input | not started>
  Decisions     <visible | needs input | not started>
  Prototype     <recorded | needs input | not started>
  Privacy       <checked | needs review | not started>

NEXT MOVE       <one concrete action, or [DECISION PENDING]>
────────────────────────────────────────────────────────────────
Say “start project”, “update dashboard”, “map my sources”, or “review privacy” to continue.
```

## Dashboard commands

These are natural-language routes, not shell commands:

- **“Dashboard” / “status”** — inspect the selected profile and render the project view.
- **“Start project”** — run the intake in `docs/AGENT_ONBOARDING.md` one question at a time.
- **“Map my sources”** — record pointers to Figma, local folders, repositories or other sources; ask permission before inspecting any location.
- **“Orient my project”** — after permission, make a bounded top-level pass over the named Figma/file/repository source and separate observed facts from inference and unknowns.
- **“Update dashboard”** — re-read the profile files and update only supported statuses.
- **“Review privacy”** — check for personal material, raw participant data, private correspondence, absolute paths, secrets and institution-restricted sources.
- **“Choose a method”** — route through `20_skill_library/skills/apply-taught-methods/` after the brief and analytical need are clear.
- **“Load pack gsa”** — read `packs/gsa/PACK.md` and make the independent Design Innovation academic pack available for this project; ask before changing an existing profile's pack selection.
- **External profile** — if the user has explicitly chosen a profile outside this
  repository, use the bounded renderer with `--allow-external-profile`; never
  infer or scan an external path from a pointer alone.

## What the Agent must not do

- Do not copy a user's Figma files, desktop folders, recordings, calendars or correspondence into the reusable core.
- Do not inspect a local folder or repository merely because its path was mentioned; ask for explicit permission to read it.
- Do not treat a file name, method, diagram or hypothesis as evidence of a project finding.
- Do not mark a step ready when the profile contains a placeholder or missing support.
- Do not commit `profiles/local/` unless the user explicitly reviews it as a separate shareable artefact.
- Do not load or copy an optional pack merely because its name appears in a project source; require an explicit selection.
