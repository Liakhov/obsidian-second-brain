---
status: accepted
date: 2026-05-27
tags:
  - workflow
  - tasks
---

# ADR-0003: Centralize tasks in markdown files

## Context

Two patterns for tracking tasks in a markdown vault:
1. **Centralized** — `tasks.md` at root plus one per project.
2. **Inline** — `- [ ]` checkboxes scattered across notes,
   aggregated by the Obsidian Tasks community plugin.

Inline feels natural ("I think about X — record it — add a
task next to the thought"). But it scatters tasks across the
vault and requires a plugin.

## Decision

Centralized. `tasks.md` at the vault root for global tasks.
`projects/<slug>/tasks.md` for project-scoped tasks. Each file
is a plain markdown checkbox list.

## Consequences

- Easy to scan "what to do today" in one place.
- No plugin dependency — works in any markdown viewer.
- Trade-off: tasks are sometimes divorced from the note where
  the thought emerged. Acceptable cost.
- If multi-line tasks with metadata (due dates, priorities) are
  needed later, can adopt inline tasks selectively without
  abandoning the centralized files.

## Alternatives

- **Inline + Obsidian Tasks plugin.** Rejected — community plugin
  dependency. Tasks scattered. Requires plugin sync between
  devices.
- **Hybrid (both patterns).** Rejected at start — ambiguity about
  where a task lives is worse than slight inconvenience of one
  pattern.
- **Tasks in `inbox/` only.** Rejected — inbox is for thoughts,
  not commitments.
