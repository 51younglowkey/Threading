# Compatibility Upgrade / 兼容升级

This workflow updates Threading without discarding project knowledge created by
an earlier version.

After an older Core fast-forwards to a version containing this workflow, start
a new Agent task in the Threading folder once. The new project instructions run
the compatibility check automatically and show any required plan.

## Natural-language command / 自然语言入口

```text
升级 Threading，并接续我已有的项目
Update Threading and reconnect my existing projects
```

## Check first / 先检查

```bash
python3 90_scripts_tools/project_workspace/upgrade_workspaces.py
```

Check mode reports:

- recognised Managed Workspaces under `projects/local/`;
- missing files required by the current schema;
- stored and current Threading versions;
- linked GSA Pack metadata changes;
- legacy profiles that can be migrated or attached for review;
- blocked workspaces requiring manual attention.

No files change in check mode.

## Apply after review / 审查后应用

```bash
python3 90_scripts_tools/project_workspace/upgrade_workspaces.py --apply
```

When following the integrated Core update route, the equivalent reviewed step
is:

```bash
python3 90_scripts_tools/threading/update_threading.py --apply-workspaces
```

Apply mode may:

1. add scaffold files that are missing from an existing Managed Workspace;
2. update `threading.json` schema, Core version and linked-pack metadata;
3. migrate a Legacy Profile into a new Managed Workspace;
4. attach a review-only Legacy Profile copy when the destination already exists;
5. write project-local history under `history/upgrades/`;
6. write a summary under `outputs/threading-upgrades/`.

## Preservation rules / 保留规则

- Existing `CURRENT.md`, project context, evidence, decisions, iterations and
  outputs are never overwritten.
- Legacy source profiles remain unchanged.
- External Figma files, folders and complete chat exports remain in place.
- Legacy and model-generated statements remain candidates until the project
  owner confirms them.
- A workspace using a newer, unsupported schema is blocked rather than changed.
- A malformed `threading.json` is reported for manual repair.

## Chat and external traces

The upgrader does not scan a home directory or guess which external files belong
to a project. After upgrading, use `整理已经导入的聊天记录` for a selected chat
archive and provide any earlier Agent analysis as a secondary note.
