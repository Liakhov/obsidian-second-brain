---
status: accepted
date: 2026-05-27
tags:
  - workflow
  - agent-behavior
---

# ADR-0002: history.md as lightweight procedural memory

## Context

The agent starts each session from scratch. It doesn't remember
that the user renamed its file from PascalCase to kebab-case last
week, or that the user prefers single-line summaries instead of
bullet lists. Same corrections repeat — wasted effort for both.

agentmemory v2 proposes a full consolidation pipeline (working →
episodic → semantic → procedural memory). That's overkill for a
single user.

## Decision

One file: `wiki/history.md`. Append-only log of corrections.
Capped at 20 latest entries; older entries move to
`wiki/history-archive.md` automatically. Agent reads
`wiki/history.md` at the start of every session and applies
lessons before responding to the first message.

## Consequences

- Near-zero implementation cost — one markdown file, one read
  at session start.
- Transparent: user can read and edit history directly.
- Compatible with any agent that reads AGENTS.md.
- Doesn't scale past ~100 entries even with archiving — at that
  point we'd need tag-based grouping or topic clustering. Out of
  scope for now; revisit as a new ADR when it hurts.
- Relies on the agent honoring "read history at session start".
  If the agent skips this step, the system silently degrades.
  Acceptable risk for a low-stakes feature.

## Alternatives

- **Full consolidation pipeline (agentmemory v2 style).**
  Rejected — operational overhead too high for one user.
- **Direct rules in `AGENTS.md`.** Rejected — turns the schema
  file into a dumping ground for specific past cases.
- **Per-session memory file (`history-YYYY-MM.md`).** Rejected —
  splitting by time defeats the cross-session purpose.
