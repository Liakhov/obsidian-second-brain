# Wiki log

Append-only journal of wiki-scoped operations. Project-scoped
operations log to `projects/<slug>/log.md` instead.

Each entry starts with `## [YYYY-MM-DD]` so the log is parseable
with simple tools:

```bash
grep "^## \[" wiki/log.md | tail -10    # last 10 entries
```

## Operation types

- **ingest** — a `raw/` source compiled into wiki pages.
- **query** — non-trivial query (most queries are not logged;
  only the ones that produced archive pages).
- **lint** — health-check pass.
- **adr** — ADR created (vault or project — both logged here for
  vault-level visibility; project ADRs also log to project log).
- **conflict** — conflict between sources recorded.
- **supersede** — old claim explicitly replaced.

## Entries

## [2026-05-27] init | vault created

Initial vault structure following Karpathy LLM Wiki pattern
extended with PARA-style projects and procedural memory.

- `AGENTS.md` + `CLAUDE.md` (symlink) — single schema source.
- `wiki/` — index, log, history, meta with starter ADRs.
- `.agent/` — operations, references, scripts.
- `raw/`, `projects/`, `archive/`, `inbox/` — empty content roots.

Starter ADRs documenting initial design decisions:
- ADR-0001 — AGENTS.md as single source.
- ADR-0002 — history.md as procedural memory.
- ADR-0003 — tasks centralized in markdown files.
- ADR-0004 — Web Clipper to raw/ directly.
