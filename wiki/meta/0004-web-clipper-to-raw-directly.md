---
status: accepted
date: 2026-05-27
tags:
  - workflow
  - ingest
  - web-clipper
---

# ADR-0004: Web Clipper writes to raw/ directly

## Context

Earlier design considered a staging area: Web Clipper → `raw/inbox/`,
then agent's INGEST would move processed files from `raw/inbox/`
to `raw/`. The idea was to visually distinguish "unprocessed"
from "ingested" via the file system.

This added complexity:
- A second inbox concept on top of the top-level `inbox/`.
- Special-case rule that "raw/ is immutable, except raw/inbox/".
- Path drift: any wiki link to a raw file would break when the
  source moved.

## Decision

Web Clipper writes to `raw/<topic>/YYYY-MM-DD-slug.md` directly.
No `raw/inbox/`. Whether a source has been ingested is tracked
in `wiki/log.md` (ingest entries) and `wiki/index.md` (referenced
by wiki articles).

The top-level `inbox/` exists for a future, distinct purpose:
quick thoughts, voice notes, Telegram captures — content that's
not a "source" yet.

## Consequences

- `raw/` is genuinely immutable. Cleaner hard rule.
- "What's not ingested yet" requires looking at the log, not the
  file system. Acceptable: LINT can surface unreferenced raw files.
- `inbox/` retains a single clear purpose — short-form captures —
  rather than conflating with source staging.

## Alternatives

- **raw/inbox/ as buffer.** Rejected — complexity not justified
  by visibility benefit.
- **Tag-based status (`status: pending` in frontmatter).**
  Rejected — invisible on the file system; log already serves
  this role.
