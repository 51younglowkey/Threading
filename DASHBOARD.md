# Threading Dashboard

Threading is an Agent-native, evidence-led project workflow for Research and
Design. It can start a project, accompany its full lifecycle or join an
already-developed project. The local Managed Workspace holds the project's
working knowledge and history.

## Welcome view

Use this when no Managed Workspace is selected or the user asks what Threading
can do:

```text
THREADING / WELCOME
────────────────────────────────────────────────────────────────
I can help you:
  1. start a Research and Design project from a question or brief
  2. accompany the project through evidence, decisions, prototypes and testing
  3. join an already-developed project and preserve its history
  4. identify and confirm its Current State
  5. organise derived knowledge from Figma, files and chat history
  6. use the optional GSA Pack for methods and Stage 3 work
  7. show one evidence-supported next move

Start with: “帮我新建一个项目空间”, “帮我接管这个现有项目” or “继续推进这个项目”
────────────────────────────────────────────────────────────────
```

## Natural-language routes

- `Dashboard`, `status`, `overview`: render the selected project's current view.
- `帮我新建一个项目空间`, `start a new project`: create or select a Managed
  Workspace and begin with a question, intended outcome and uncertainty.
- `帮我接管这个现有项目`, `adopt project`: create or select a Managed Workspace,
  register source pointers, orient bounded sources and propose Current State.
- `继续推进这个项目`, `continue this project`: read the selected workspace,
  show its Current State and propose the next evidence-led move.
- `整理已经导入的聊天记录`, `reconcile chat archive`: register the selected
  Markdown archive, extract candidates and ask before promotion.
- `帮我整理 Figma 的演变`, `map Figma`: record file/page/frame evolution and
  propose a current candidate for user confirmation.
- `加载 GSA Pack`, `load pack gsa`: enable the linked pack and show its methods,
  Provotyping, Reflection Document and Stage 3 capabilities.
- `Update Threading`, `升级 Threading，并接续我已有的项目`: check tracked
  changes and remote state, then preview compatibility repairs and legacy-trace
  connections before applying them.
- `帮我找出 evidence gaps`, `find the evidence gaps`: report unsupported claims,
  missing source pointers and pending confirmations in bounded project records.
- `Threading doctor`: verify core, skill, privacy ignore, project schema and pack.

## Project view

Read the selected `projects/local/<slug>/CURRENT.md`, `packs.md` and bounded
records. Do not infer current state from file modification time alone.

```text
THREADING / PROJECT DASHBOARD
────────────────────────────────────────────────────────────────
Project          <title>
Workspace        projects/local/<slug>/
Phase            <phase>
Last confirmed   <date or [DATE TO CONFIRM]>
Current status   <confirmed | needs confirmation>
Current question <confirmed question or [DECISION PENDING]>
Current direction <confirmed direction or [DECISION PENDING]>

KNOWLEDGE
  Sources        <registered count>
  Evidence       <record count>
  Decisions      <record count>
  Chat review    <candidate count>

GSA PACK         <enabled/disabled> / <version>
NEXT MOVE        <one concrete action or [DECISION PENDING]>
────────────────────────────────────────────────────────────────
```

## Current-state rule

Root `NOW.md` describes Threading itself. A local project's `CURRENT.md`
describes what that school/research/design project currently accepts as active.
The Agent may propose changes from newer Figma or chat material, but only the
user can confirm promotion to Current State. Preserve earlier states in decision
and iteration history.

## Source boundary

Raw Figma files, desktop folders and complete chat archives may stay in their
original locations. Bounded derived text may live in the local Managed Workspace
when it records source ID, pointer, inspected scope, date and status. A pointer
is not inspection permission.
