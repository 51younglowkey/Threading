# Managed Workspace Schema

```text
projects/local/<slug>/
├── AGENTS.md
├── CURRENT.md
├── project.md
├── packs.md
├── threading.json
├── sources/
│   ├── source_registry.md
│   ├── figma/evolution_map.md
│   ├── figma/derived/
│   ├── chats/chat_inventory.md
│   ├── chats/candidate_records.md
│   └── local-files/README.md
├── evidence/evidence_log.md
├── decisions/decision_log.md
├── iterations/iteration_log.md
├── history/upgrades/ (created when needed)
├── sources/legacy/ (review-only copies created when needed)
└── outputs/README.md
```

`CURRENT.md` is the confirmed snapshot for the school project. Root `NOW.md`
describes Threading itself. Logs preserve history; `CURRENT.md` never replaces
the evidence, decision or iteration record.

Project states use `candidate`, `confirmed`, `rejected`, `superseded` and
`unknown`. Only user-confirmed material may become current. The Agent may propose
changes but must preserve provenance and ask before promotion.

Compatibility upgrades may add missing scaffold files and update
`threading.json` metadata. They never overwrite existing project records.
Legacy material attached under `sources/legacy/` remains `candidate` until the
project owner reviews and promotes specific items.
