# Figma Evolution Workflow

Use this route when a project has many Figma files, pages or frames across time.

1. Record the authorised Figma file/page/frame scope.
2. Inspect top-level structure and metadata before deep content.
3. Store bounded extracted text under the local project's
   `sources/figma/derived/` with source pointer, scope and date.
4. Classify each relevant item as `current-candidate`, `candidate`, `historical`,
   `reference` or `unknown`.
5. Record what insight, opportunity or direction it represents and whether it
   supersedes an earlier item.
6. Let the Agent propose the most recent coherent working set.
7. Require user confirmation before marking it `current` or changing
   `CURRENT.md`.

Recent modification time is evidence of recency, not evidence that the item is
the accepted current direction.
