# Threading Dashboard Compatibility Route

The primary installable route is `skills/threading/SKILL.md`. Use this file only
when an older Threading checkout routes here directly.

1. Read root `DASHBOARD.md`.
2. Prefer `projects/local/<slug>/` Managed Workspaces; treat `profiles/local/`
   as a legacy migration source.
3. Read the selected project's nested `AGENTS.md` and `CURRENT.md` first.
4. Use `90_scripts_tools/project_workspace/render_dashboard.py` for the
   deterministic text view.
5. For existing projects, use the adoption route rather than a blank intake.
6. For GSA, use linked read-only activation through `manage_pack.py` and show
   the available capabilities immediately.
7. Never promote Figma or chat-derived candidates to Current State without user
   confirmation.
