# Updating Threading

Clone once; update the same clone afterward.

## Check first

```bash
python3 90_scripts_tools/threading/update_threading.py
```

The check fetches `origin/main`, reports ahead/behind state and refuses automatic
updates when tracked core files are dirty or history has diverged. When the core
is current, it also previews Managed Workspace compatibility changes.

## Apply a verified fast-forward

```bash
python3 90_scripts_tools/threading/update_threading.py --apply
python3 90_scripts_tools/threading/update_threading.py --apply-workspaces
python3 90_scripts_tools/threading/doctor.py
```

`projects/local/` and `profiles/local/` are Git-ignored and are not changed by
the Git fast-forward. Afterward, Threading shows the compatibility plan. The
separate `--apply-workspaces` step adds only missing schema files, refreshes
machine-readable version metadata, connects legacy profiles and writes an
upgrade report. Existing Current State, evidence, decisions, iterations and
outputs are preserved.

A symlink-registered Skill sees the updated core immediately; start a new Agent
task once after upgrading from v0.2 so the new project instructions load. That
first interaction automatically runs the compatibility check. A copied Skill
must be registered again with `install_skill.py --mode copy --update`.

## Natural-language route

Say `Update Threading` or `升级 Threading，并接续我已有的项目`. The Agent must
run check mode and report both the core update and compatibility plan before
using `--apply`.

See [Compatibility upgrade](COMPATIBILITY_UPGRADE.md) for the exact preservation
and migration rules.
