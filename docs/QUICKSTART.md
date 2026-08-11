# Threading Quickstart / 快速开始

Quickstart is the short first-use route. The complete bilingual operating guide is
in [`docs/AGENT_ONBOARDING.md`](AGENT_ONBOARDING.md).

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

## 3. Choose an entry point / 选择入口

Start from scratch:

```text
帮我新建一个项目空间
```

Start early and continue the full workflow:

```text
帮我从这个 brief 开始建立一个 Research and Design 项目
```

Join an already-developed project:

Say:

```text
帮我接管这个现有项目
```

Threading asks for the project title, phase, intended outcome and where material
lives. It creates `projects/local/<slug>/`, which is Git-ignored. It registers
pointers before inspection and asks permission before reading named sources.

Equivalent deterministic command:

```bash
python3 90_scripts_tools/project_workspace/adopt_project.py \
  --slug my-project \
  --title "My project" \
  --pack none
```

Add `--pack gsa` only when the independent linked GSA Pack is relevant.

## 4. Orient sources / 整理来源

Grant explicit permission for named Figma files/pages, a specific local project
folder or a selected Markdown chat archive. Threading separates observed,
inferred, candidate and unknown information.

For chat history already imported, say:

```text
整理已经导入的聊天记录
```

## 5. Confirm Current State / 确认当前状态

The Agent proposes the current question, direction, working set and next move.
The user must confirm them before `CURRENT.md` changes. Older directions remain
in decision and iteration history.

## 6. Use the Dashboard / 查看 Dashboard

```text
Threading Dashboard
```

The Dashboard shows Current State, registered knowledge, chat review queue,
linked GSA Pack status and one next move.

## 7. Update later / 后续更新

```text
Update Threading
```

Or use `90_scripts_tools/threading/update_threading.py`. See `docs/UPDATING.md`.
