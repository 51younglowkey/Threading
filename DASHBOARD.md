# Threading Dashboard

Threading is a complete local reasoning workspace with an optional installable
skill. It organises derived project knowledge without pretending that imported
history is current or that a framework is evidence.

## Welcome view

Use this when no Managed Workspace is selected or the user asks what Threading
can do:

```text
THREADING / WELCOME
────────────────────────────────────────────────────────────────
I can help you:
  1. adopt an existing complex project
  2. identify and confirm its Current State
  3. organise derived knowledge from Figma, files and chat history
  4. trace evidence → decision → prototype → test → iteration
  5. use the optional GSA Pack for methods and Stage 3 work
  6. show one evidence-supported next move

Start with: “帮我接管这个现有项目”
────────────────────────────────────────────────────────────────
```

## Natural-language routes

- `Dashboard`, `status`, `overview`: render the selected project's current view.
- `帮我接管这个现有项目`, `adopt project`: create or select a Managed Workspace,
  register source pointers, orient bounded sources and propose Current State.
- `整理已经导入的聊天记录`, `reconcile chat archive`: register the selected
  Markdown archive, extract candidates and ask before promotion.
- `帮我整理 Figma 的演变`, `map Figma`: record file/page/frame evolution and
  propose a current candidate for user confirmation.
- `加载 GSA Pack`, `load pack gsa`: enable the linked pack and show its methods,
  Provotyping, Reflection Document and Stage 3 capabilities.
- `Update Threading`: check tracked changes and remote state before a safe
  fast-forward update.
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
