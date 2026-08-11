# Threading Dashboard and Project Onboarding

Use this skill when the user asks for a Dashboard, status, overview, next step, project start, project setup, source mapping or a local project space.

Optional packs are opt-in. The generic Threading core is always available; do
not read a pack's methods until the user selects it. For the GSA Pack, route the
user to `packs/gsa/PACK.md` and initialize with `--pack gsa` when requested.

## Route

1. Read `DASHBOARD.md`.
2. Check whether `profiles/local/` contains zero, one or multiple user-owned profiles.
3. If there is no selected profile, follow `docs/AGENT_ONBOARDING.md` one question at a time.
4. If a profile is selected, read `status.md`, `context.md`, `source_map.md`, `evidence_log.md`, `decision_log.md` and `iteration_log.md` as needed.
5. Render the compact project dashboard. Use only supported information.

## Output contract

The dashboard must show:

- project title and profile path;
- lifecycle status and current phase;
- readiness for brief, sources, evidence, decisions, prototype/testing and privacy;
- one concrete next action;
- a reminder of what remains outside the profile.

Use `not started`, `needs input`, `needs review`, `blocked` or a supported positive status. Do not turn an empty template into progress.

## Source handling

The user may keep the project in Figma, a desktop folder, another repository or a mixed setup. Record a pointer in `source_map.md` first. Ask for explicit permission before inspecting any source, and never copy raw project material into the reusable core automatically.

After permission, prefer a bounded orientation pass over a full import: inspect
top-level files, frames or pages; report `observed`, `inferred` and `unknown`
separately; then ask whether to go deeper.

## Bounded tool

For a deterministic local text view, run:

```bash
python3 90_scripts_tools/project_profile/render_dashboard.py \
  --profile profiles/local/<project-slug>
```

For a new local profile, run `init_project.py` from the same directory after the user has confirmed Profile mode and the slug. For a separate path, require the explicit `--allow-external-root` flag and confirm repository initialisation separately.

For an existing profile that the user explicitly selects for GSA loading, use
`load_pack.py --pack gsa`; add `--allow-external-profile` for a profile outside
the Threading workspace. Do not update an already copied pack without explicit
confirmation.
