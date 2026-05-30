---
status: accepted
date: 2026-05-30
tags:
  - workflow
  - ingest
  - web-clipper
---

# ADR-0004: raw/ is flat — Web Clipper writes there directly

## Context

`raw/` holds immutable source material. It is never browsed manually
— access is via backlinks from `wiki/` and full-text search. Topic
classification is already the job of `wiki/<topic>/`. §3.1 makes
`raw/` immutable.

## Decision

`raw/` is flat. Files: `raw/YYYY-MM-DD-<source-slug>.md`. Topic
classification happens in `wiki/<topic>/` at INGEST time.

`raw/assets/` is the only permitted subfolder, reserved for binary
image attachments. No other subfolders.

Web Clipper config:
- Note location: `raw`
- File name: `{{date}}-{{title|safe_name}}`

## Consequences

- `raw/` is genuinely immutable — no exceptions to §3.1.
- INGEST determines topic from source content, not file path.
- At scale, shard by date (`raw/2026/`) if browsing hurts.
  Mechanical, not semantic.
