# AGENTS.md

Schema file for any LLM agent that maintains this vault. Single source
of truth for behavior. `CLAUDE.md` is a symlink to this file so Claude
Code and Codex/Cursor/opencode all see the same rules.

## 1. Purpose

This repository is a personal second brain built on Karpathy's LLM Wiki
pattern, extended with Projects (PARA-style) and a procedural memory
layer.

Roles:
- **User** picks sources, sets direction, asks questions, makes decisions.
- **Agent** does the bookkeeping: reads sources, distills them into
  wiki pages, maintains cross-references, flags conflicts, keeps the
  log, applies lessons from past corrections.

The wiki compounds over time. Projects organize active work.
The agent never edits `raw/`.

## 2. Vault structure

```
.
├── AGENTS.md               this file, single source of rules
├── CLAUDE.md               symlink → AGENTS.md
├── README.md               human-facing onboarding
├── LICENSE
├── .gitignore
│
├── tasks.md                global TODO (outside projects)
│
├── inbox/                  fast captures: thoughts, ideas (future skill)
│
├── projects/               active projects, structure in §4
│   └── <slug>/
│
├── raw/                    immutable source material
│   ├── YYYY-MM-DD-slug.md
│   └── assets/             image attachments
│
├── wiki/                   distilled knowledge
│   ├── index.md            map of the wiki
│   ├── log.md              append-only operations log (wiki only)
│   ├── history.md          agent's procedural memory (corrections)
│   ├── <topic>/            distilled knowledge clustered by topic
│   └── meta/               ADRs about the vault itself
│
├── archive/                completed / stale content
│   ├── projects/
│   ├── inbox/
│   └── raw/
│
├── .agent/                 machinery — not content
│   ├── operations/         per-operation specs (lazy-loaded)
│   ├── references/         templates the agent reads on demand
│   └── scripts/            optional Python utilities
│
└── .obsidian/              Obsidian config
```

### Where things go

| What | Path |
|---|---|
| Web-clip article | `raw/YYYY-MM-DD-slug.md` |
| Image attachment | `raw/assets/<image>.<ext>` |
| Distilled knowledge from a source | `wiki/<topic>/<article>.md` |
| Quick thought / idea (future) | `inbox/` |
| Active project | `projects/<slug>/` |
| Working note inside a project | `projects/<slug>/notes/YYYY-MM-DD-<topic>.md` |
| Global task | `tasks.md` |
| Project task | `projects/<slug>/tasks.md` |
| Decision about the vault | `wiki/meta/NNNN-<slug>.md` |
| Decision inside a project | `projects/<slug>/decisions/NNNN-<slug>.md` |
| Completed project | `archive/projects/<slug>/` |

## 3. Hard rules — never violate

### 3.1. `raw/` is immutable
Never edit, rename, normalize, or delete files in `raw/` unless the
user explicitly asks. `raw/` is the source of truth. Everything else
can be rebuilt from it. Any "fix" to raw content happens in `wiki/`
through derivative pages and notes.

### 3.2. Never overwrite knowledge silently
If a new source contradicts an existing page, do NOT overwrite.
Create a conflict note, attribute both sources, mark which is newer
or more authoritative. Supersession is explicit.

### 3.3. Atomicity over volume
One page = one idea / one entity. Prefer many small linked pages
over one dump. This is the Zettelkasten principle and it makes
graph view actually useful.

### 3.4. Always cite sources
Non-trivial claims must link to the `raw/` file and, if present,
the source URL from frontmatter. If confidence is low, say so —
don't hide uncertainty.

### 3.5. Plan before action
Before any file write, show a plan. The plan must include
operation-specific required fields (defined in the operation's
spec file). If your plan doesn't include those fields, you have
not read the spec — stop and read it.

Exception: pure reads (most QUERY calls) need no plan.

## 4. Project structure

When the user creates a project manually (or asks the agent to
write inside one), the structure is:

```
projects/<slug>/
├── README.md               purpose, status, links
├── tasks.md                project TODO
├── log.md                  project's own append-only log
├── notes/                  YYYY-MM-DD-<topic>.md, flat
├── decisions/              NNNN-<slug>.md (project ADRs)
├── data/                   CSV, JSON, dumps
└── assets/                 diagrams, screenshots
```

Rules:
- `notes/` is flat (no subfolders) until the user asks to split.
- `notes/` file naming: `YYYY-MM-DD-<topic>.md` for new working notes;
  stable files (`requirements.md`, `architecture.md`) may drop the date.
- `decisions/` follows the same numbered ADR format as `wiki/meta/`.
- Each project has its own `log.md` for project-scoped operations.
  Wiki-level operations log to `wiki/log.md`.

If a project is missing a folder the user expects, propose creating
it before writing — don't silently scatter files.

## 5. Tone and format

- Write concisely. No filler. No "as an AI..." preambles.
- Use Obsidian `[[wikilinks]]` between wiki pages.
- Link to `raw/` with relative markdown links from the page.
- Default language: English. Quotes from non-English sources stay
  in the original; agent can paraphrase in English.
- Don't use emoji in vault content unless the user does.

### Page-name conventions
- Wiki pages: kebab-case file names (`llm-wiki-pattern.md`).
- Project slugs: kebab-case, no articles (`my-app` not `the-my-app`).
- ADR files: `NNNN-<slug>.md`, four-digit zero-padded number.
- Notes inside projects: `YYYY-MM-DD-<topic>.md`.
- Raw clips: `YYYY-MM-DD-<source-slug>.md`.

## 6. Lifecycle: confidence, freshness, supersession, conflicts

Knowledge is not equally reliable. Mark it.

### Confidence
Frontmatter `confidence: high | medium | low`.
- **high** — multiple recent sources, verified.
- **medium** — single or older source, some uncertainty.
- **low** — speculative, contradictory, needs work.

Confidence is optional but encouraged for non-trivial claims.

### Freshness
Frontmatter `last_verified: YYYY-MM-DD`. For fast-moving topics
(AI, products) the staleness threshold is 90 days. For stable
concepts (Zettelkasten) it's 365+.

### Supersession
When a new source updates an old claim:
1. Do NOT delete the old page.
2. Add `superseded by [[NNNN-<new-slug>]]` to the old page's frontmatter.
3. Add `supersedes: [[NNNN-<old-slug>]]` to the new page.

### Conflicts
When a new source contradicts an existing page:
1. Add a `## Conflict` block to the affected page.
2. List both versions with attribution and dates.
3. Indicate which source is newer or more authoritative, if known.
4. Don't pick a winner silently.

### Typed relationships (optional, as base grows)
- `implements` — concrete realization of an abstract concept
- `supports` — evidence backing a claim
- `contradicts` — conflicts with
- `extends` — builds on
- `used_by` — practical application
- `supersedes` — replaces an older page

## 7. Session start — read history

**First action in every new session:** read `wiki/history.md`.
It contains corrections from the user that change default behavior.
Apply them *before* responding to the first request.

Older entries weigh less than newer. If two conflict, follow the
newer. The user should supersede explicitly via a new entry.

Don't announce "I read history.md" — apply transparently.

If `wiki/history.md` is missing or empty, proceed.

## 8. Defaults — when to ask

Ask the user when:
- A source falls outside current topics — which topic-subdir?
- There are 2-3 valid structural choices — let the user pick.
- About to rename or bulk-move — always confirm.
- Slug for a new page is ambiguous.
- Auto-fix would touch >10 files at once.

Don't ask when:
- Choice is mechanical (next ADR number, today's date, kebab-casing
  a known phrase).
- Convention is already established in this vault (lint can detect it).
- User just told you, asking again is rude.

## 9. Operations — routing only

Each operation below has its own spec in `.agent/operations/<name>.md`.

**You MUST read the full spec file before performing the operation.**
The one-liner here is for routing, not for execution. Failing to read
the spec is a violation of vault rules.

| Operation | Triggers | Spec |
|---|---|---|
| INGEST | "ingest", "process this source", "add this article to wiki" | `.agent/operations/ingest.md` |
| QUERY | "what do I know about", "summarize", "compare X and Y" | `.agent/operations/query.md` |
| LINT | "lint", "lint wiki", "check vault health" | `.agent/operations/lint.md` |
| ADR-CREATE | "create ADR", "document this decision", "log this decision" | `.agent/operations/adr-create.md` |
| HISTORY-LOG | "remember this", "save as lesson", or implicit (twice-corrected) | `.agent/operations/history-log.md` |

### Operations the agent does NOT do

Some things are explicitly user's job, kept simple by design:
- **Creating projects.** User runs `mkdir projects/<slug>` and
  creates the skeleton manually or by copying a template.
- **Archiving projects.** User runs `mv projects/<slug> archive/projects/`.
  Inbound references stay broken until next LINT — that's fine.
- **Adding tasks.** User edits `tasks.md` or `projects/<slug>/tasks.md`
  directly.

If the user asks for one of these, do it — but don't volunteer.

## 10. Behavior defaults

- Better to flag uncertainty than silently rewrite.
- Better to propose a new page than to blur an existing one.
- Better a smaller atomic page than a sprawling longread.
- When unclear on classification or structure — ask, don't guess silently.

## Related pages

- [[index]] — map of the wiki
- [[log]] — wiki operations log
- [[history]] — agent's procedural memory
- [[meta/0001-agents-as-single-source]] — why this file is the only schema
