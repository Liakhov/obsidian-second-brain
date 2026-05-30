---
status: accepted
date: 2026-05-27
tags:
  - architecture
  - agents
---

# ADR-0001: AGENTS.md as single source, CLAUDE.md as symlink

## Context

Claude Code reads `CLAUDE.md` by default. Codex, Cursor, opencode
and others read `AGENTS.md`. Maintaining two full files means
manual sync — they will drift, and the drift will be silent until
it causes a bug.

## Decision

`AGENTS.md` is the single source of rules. `CLAUDE.md` is a Git
symlink to `AGENTS.md`. One file, two visible names.

## Consequences

- One place to edit rules. No drift.
- Every compatible agent sees the same behavior.
- On Windows, symlinks need either WSL or developer mode enabled.
  If a team is Windows-only, fall back to a pre-commit hook that
  copies `AGENTS.md` to `CLAUDE.md` on every commit. Not our
  current concern — revisit if it becomes one.
- If Anthropic or OpenAI introduce incompatible directives in
  their respective files later, this ADR will be superseded.

## Alternatives

- **Two real files, sync manually.** Rejected — drift is
  inevitable.
- **One file + symlink in the other direction (CLAUDE.md is real,
  AGENTS.md is symlink).** Semantically equivalent. Chose
  `AGENTS.md` because it's the broader cross-tool standard.
- **Script-generated from a template.** Extra moving parts at the
  start.
