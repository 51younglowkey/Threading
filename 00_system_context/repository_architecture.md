# Threading Repository Architecture

Updated: 2026-08-10

## Core and profiles

Threading is the reusable system layer: rules, methods, templates, bounded tools, an Agent-facing text Dashboard and documentation about how to keep academic work traceable.

Each user may add a separate project profile containing their own context, evidence, decisions, prototypes and outputs. A profile should be clearly marked as user-owned and should not silently become part of the reusable core.

The first-run route is Agent-native: `DASHBOARD.md` explains the capability map,
`docs/AGENT_ONBOARDING.md` collects a minimum brief, and a profile is created
only after the user confirms its local destination. Figma files, desktop folders
and other repositories are source pointers until the user explicitly permits
inspection.

```text
Threading
├── reusable rules, methods, templates and tools
├── optional packs selected at project initialization
└── optional user-owned project profiles (local or separately controlled)
```

## Versioning

- Use ordinary commits for meaningful, reviewable changes.
- Use a version number in a document when an artefact reaches a named iteration.
- Use a Git tag only for a stable milestone that may need to be reconstructed or cited.
- Keep version records distinct from project names and profile names.
- Explain why a change happened in an iteration record; a commit alone is not a research rationale.

## Privacy boundary

The public edition must exclude personal correspondence, schedules, participant identities, consent records, raw recordings, identifiable images, private academic administration, local absolute paths, caches, dependencies and generated exports. A clean working tree is not enough: inspect historical commits and archived refs before publishing.

## Lifecycle

The reusable core may evolve continuously. A user-owned profile can be active, in maintenance or archived. Archiving preserves its historical record and does not authorise deletion or silent modernisation.
