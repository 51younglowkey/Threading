# Updating Threading

Clone once; update the same clone afterward.

## Check first

```bash
python3 90_scripts_tools/threading/update_threading.py
```

The check fetches `origin/main`, reports ahead/behind state and refuses automatic
updates when tracked core files are dirty or history has diverged.

## Apply a verified fast-forward

```bash
python3 90_scripts_tools/threading/update_threading.py --apply
python3 90_scripts_tools/threading/doctor.py
```

`projects/local/` and `profiles/local/` are Git-ignored and are not changed by
the Git update. A symlink-installed skill sees the updated core immediately;
start a new Codex task to refresh loaded instructions. A copied skill must be
reinstalled with `install_skill.py --mode copy --update`.

## Natural-language route

Say `Update Threading`. The Agent must run check mode and report the result
before using `--apply`.
