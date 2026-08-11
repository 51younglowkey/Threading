# Threading Quickstart

## 1. Clone once

```bash
git clone https://github.com/51younglowkey/Threading.git
cd Threading
```

## 2. Install the optional natural-language skill

```bash
python3 90_scripts_tools/threading/install_skill.py
```

Start a new Codex task after installation.

## 3. Adopt the existing project

Say:

```text
帮我接管这个现有项目
```

Threading asks for the project title, slug and where material lives. It creates
`projects/local/<slug>/`, which is Git-ignored. It registers pointers before
inspection and never imports raw sources automatically.

Equivalent deterministic command:

```bash
python3 90_scripts_tools/project_workspace/adopt_project.py \
  --slug my-project \
  --title "My project" \
  --pack none
```

Add `--pack gsa` only when the independent linked GSA Pack is relevant.

## 4. Orient sources

Grant explicit permission for named Figma files/pages, a specific local project
folder or a selected Markdown chat archive. Threading separates observed,
inferred, candidate and unknown information.

For chat history already imported, say:

```text
整理已经导入的聊天记录
```

## 5. Confirm Current State

The Agent proposes the current question, direction, working set and next move.
The user must confirm them before `CURRENT.md` changes. Older directions remain
in decision and iteration history.

## 6. Use the Dashboard

```text
Threading Dashboard
```

The Dashboard shows Current State, registered knowledge, chat review queue,
linked GSA Pack status and one next move.

## 7. Update later

```text
Update Threading
```

Or use `90_scripts_tools/threading/update_threading.py`. See `docs/UPDATING.md`.
