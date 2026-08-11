# Legacy Project Profiles

`profiles/` is retained for v0.1 compatibility and non-destructive migration.
New complete workspaces belong in `projects/local/<slug>/`.

- `profiles/_template/` is the legacy lightweight scaffold.
- `profiles/local/` is ignored by Git and is intended for private project work.
- A profile intended for sharing must pass its own evidence, privacy, provenance and licensing review before it is moved out of `profiles/local/`.

Do not place raw participant material, private correspondence, schedules, contact details or consent records in the reusable core.

Use `90_scripts_tools/project_workspace/migrate_legacy_profile.py` to create a
v0.2 Managed Workspace while leaving the original profile unchanged.
