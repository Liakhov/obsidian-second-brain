---
name: second-brain
description: Use when working on a project and you need its recorded context
  (what's done, backlog, past decisions) or want to record progress,
  improvements, notes, or new ideas into the second-brain vault — especially
  from inside the project's own repo, where the vault is not otherwise
  visible.
---

# Second Brain bridge

Connects any repo session to the second-brain vault. The vault documents
projects under `projects/<slug>/` and distilled knowledge under `wiki/`. The
project's own source code lives in its repo; the vault holds only its
documentation.

## Find the vault

This skill is symlinked into the runtime skills directory from inside the
vault. Resolve the symlink to its real location:

```bash
readlink -f ~/.claude/skills/second-brain   # Claude Code
readlink -f ~/.agents/skills/second-brain   # Codex (use whichever exists)
```

That prints `<vault>/skills/second-brain`. The vault root is two levels up —
drop the trailing `/skills/second-brain`. Use that path as `<vault>` below.
(Keeping each command simple and substitution-free avoids permission
prompts.)

## Use it

1. Read `$VAULT/AGENTS.md` — the full, authoritative schema and rules. This
   skill deliberately does not restate them.
2. Identify the project `<slug>` (the current repo's name usually matches; if
   unsure, read `$VAULT/projects/index.md`). Read `$VAULT/projects/<slug>/`
   (`README.md`, `tasks.md`, `notes/`) for recorded context.
3. To record work, edit those files following AGENTS.md:
   - `README.md` — purpose, status, what's done, repo + `[[wiki]]` topic links
   - `tasks.md` — improvements / backlog
   - `notes/YYYY-MM-DD-<topic>.md` — a decision or learning
   - bump `updated:` frontmatter where present
4. If the project is new (no folder yet), propose creating
   `$VAULT/projects/<slug>/` and a row in `$VAULT/projects/index.md`, then ask
   before writing — same as the vault's INGEST flow.

## Hard rule

Never edit, rename, or delete anything under `$VAULT/raw/` — it is immutable
source material.