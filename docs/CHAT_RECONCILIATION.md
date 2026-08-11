# Existing Chat Archive Reconciliation

This workflow handles Markdown chat exports that are already present and may
already have been partially analysed by Codex.

## Natural-language command

```text
整理已经导入的聊天记录
Reconcile existing chat archive
把现有聊天记录纳入项目知识
```

## Process

1. Select the archive and explicitly permit inspection.
2. Register its pointer and SHA-256; leave the raw archive unchanged.
3. Include any earlier Codex analysis files as secondary notes.
4. Build a conversation/heading inventory.
5. Review only relevant conversations in bounded batches.
6. Extract candidate insight, decision, rejected direction, open question,
   source pointer and unsupported model claim.
7. Compare candidates with confirmed Figma/local evidence and Current State.
8. Ask the owner to confirm, reject or supersede material items.
9. Promote confirmed material into the appropriate records.

Run the deterministic registration step with:

```bash
python3 90_scripts_tools/project_workspace/reconcile_chat_archive.py \
  --project projects/local/my-project \
  --archive "/explicit/existing-chat-export.md" \
  --analysis-note "/explicit/earlier-codex-summary.md"
```

The script does not automatically promote chat content into project truth.
