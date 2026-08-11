# Threading Repository Architecture

Updated: 2026-08-11
Schema: 2

## Four layers

```text
Public Threading core
  rules, templates, scripts, linked packs and update source
            │
            ├── installable Threading skill
            │     natural-language routing in Codex
            │
            └── projects/local/<slug>/
                  private Managed Workspace for one school/research/design project
                         │
                         └── external raw sources
                              Figma / local folders / chat archives
```

The complete product is the Threading project workflow, implemented through the
repository core plus a user-owned Managed Workspace. The standalone skill is an
access and routing layer, while the local workspace holds the project instance.

## Current and history

Root `NOW.md` describes the Threading product. Each local `CURRENT.md` contains
the user-confirmed present state of one project. Evidence, decision and iteration
records preserve history, including rejected and superseded directions.

## Local knowledge boundary

`projects/local/` is Git-ignored. It may contain bounded derived text and
analysis from explicitly authorised sources when every record preserves a source
pointer, inspected scope, date and status. Raw sources may remain in their
original controlled locations and are not imported automatically.

## Packs

Optional packs use linked, read-only activation. A project records the enabled
pack and version in `packs.md` and `threading.json`; project-specific analysis
never modifies the public pack source.

## Compatibility

`profiles/local/` is the v0.1 compatibility layer. Migration creates a new
Managed Workspace and preserves the legacy profile unchanged.

## Versioning

- `VERSION` identifies the Threading core release.
- `docs/CHANGELOG.md` records public capability changes.
- `threading.json` records project schema and linked-pack state.
- Git tags identify stable reconstructable releases.
- Project iteration versions remain separate from Threading versions.
