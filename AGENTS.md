# AGENTS.md

Schema for any LLM agent that maintains this vault. Single source of
truth. `CLAUDE.md` is a symlink → `AGENTS.md`.

## Purpose

Personal second brain on Karpathy's LLM Wiki pattern, simplified to the
3-page model from McFarland's content wiki. User curates sources; agent
distills them into wiki pages, cross-links, and remembers corrections.

The wiki compounds. Topic pages grow over time — new sources add
paragraphs, not new files. Agent never edits `raw/`.

## Vault structure

```
.
├── AGENTS.md           rules (this file)
├── CLAUDE.md           symlink → AGENTS.md
├── README.md           human onboarding
├── tasks.md            global TODO
│
├── raw/                immutable source material (Web Clipper sink, flat)
│   └── assets/
│
├── wiki/
│   ├── index.md        MOC: topics, patterns, link to sources/
│   ├── history.md      user corrections that change agent behavior
│   ├── sources/        one file per ingested source
│   ├── topics/         evolving knowledge pages, grow over time
│   └── patterns/       emergent insights from 3+ sources
│
└── projects/           project docs
    ├── index.md        catalog of all projects
    └── <slug>/         README, tasks, notes/, data/, assets/
```

## Page types

### `wiki/sources/<date>-<slug>.md`

What one source says. Created once, rarely edited.

- File name: `YYYY-MM-DD-<short-slug>.md`, kebab-case. Date is
  publication date if known, else clip date.
- Sections: `## Argument`, `## Examples`, `## Key takeaway`.
- 10-25 lines typical. Anything longer probably belongs in a topic.
- Links back to the `raw/` file in the header.

### `wiki/topics/<slug>.md`

Your synthesized position on a subject. Grows over time as new sources
touch it.

- File name reflects the concept (e.g. `llm-wiki-pattern.md`), not the source.
- TL;DR sentence at the top.
- Sections accrete with new sources — chronological
  (`## Karpathy's original (2026-04)`) or thematic (`## Pros`,
  `## Pitfalls`, `## My take`).
- Update the `updated:` frontmatter on every meaningful edit.
- Split only when a page passes ~500 lines AND clearly contains two
  independent sub-topics. Default: keep growing.

### `wiki/patterns/<slug>.md`

Insights observed across 3+ sources. Rare. Typically <10 in the whole
vault.

- Created only when a pattern truly recurs across multiple sources.
- Structure: thesis + evidence list (links to source files) +
  implications.
- Do NOT create a pattern from a single source.

## Frontmatter

All three page types use the same minimal block:

```yaml
---
title: <title>
updated: YYYY-MM-DD
tags: [tag1, tag2]
---
```

Optional, add only when useful: `url`, `author`, `created`.

Do NOT add: `type`, `confidence`, `last_verified`, `sources`, `raw`,
`relationships`. These were process noise.

## INGEST flow

When the user says "ingest raw/X" or "process this source":

1. Read the raw file.
2. Identify the topics it touches (typically 1-3).
3. Propose, in plain English:
   - Create `wiki/sources/<date>-<slug>.md`.
   - Update or create topic pages (list them by name).
   - Update `wiki/index.md` if a new topic page is added.

   Then ask: "Proceed?"
4. On confirm: write the source page, update topics, update index.

No 7-field plan. No `Source Notes.md` entry. No `log.md` entry. No
cascade-update of unrelated pages. No `confidence` / `last_verified`
bookkeeping.

## QUERY

When the user asks "what do I know about X":

1. Read `wiki/index.md`, find relevant topic page(s).
2. Read those topics. Prefer wiki content over training knowledge.
3. Answer with citations as plain markdown links to topic and source
   files.
4. Do NOT write files. If the answer is worth keeping, the user will
   ask to add it to the relevant topic page.

## Ad-hoc lint

When the user asks "check vault health":

- Scan for broken `[[wikilinks]]`, orphan pages, topic pages with stale
  `updated` dates.
- Fix only what's mechanical and obvious (e.g. a wikilink with exactly
  one matching alternative).
- Report the rest; let the user decide.

No Python scripts. No formal phases. No bulk-fix gate.

## Hard rules

1. **`raw/` is immutable.** Never edit, rename, or delete files there
   unless the user explicitly asks.
2. **Cite sources.** Non-trivial claims on a topic page link to the
   source file they came from.
3. **Don't overwrite silently.** If a new source contradicts an existing
   topic page, add a caveat paragraph naming both sources — don't pick
   a winner without saying so.
4. **Prefer growing a topic page over creating a new file.** Splits
   happen only when a page passes ~500 lines AND contains two
   independent sub-topics.
5. **Plan before write.** Short plain-English plan, then "Proceed?".

## Session start

Read `wiki/history.md` first. Treat its entries as standing instructions
that modify default behavior. Apply silently before responding to the
first request. Newer entries override older if they conflict. If the
file is missing or empty, proceed.

Do not announce "I read history.md" — apply transparently. When
appending a new correction, use the format below.

## `wiki/history.md` format

```markdown
## [YYYY-MM-DD] correction
One short paragraph: what changed and why.
```

The user refactors and prunes this file manually over time.

## When to ask vs decide

Ask when:
- A source clearly spans multiple new topics — confirm primary placement.
- About to rename or move >5 files.
- Slug for a new page is ambiguous.

Don't ask when:
- The choice is mechanical (today's date, kebab-casing).
- Convention is already established.

## Tone

- Concise. No filler. No "as an AI..." preambles.
- Use `[[wikilinks]]` between wiki pages.
- Link to `raw/` files with relative markdown links from the page.
- Default language: English. Quotes from non-English sources stay in
  the original; agent can paraphrase in English.
- Don't use emoji in vault content unless the user does.

## Projects

Projects document work whose **code lives in its own repo elsewhere**;
the vault holds only the documentation, never the source.

`projects/index.md` is the catalog — a MOC listing every project with
status, one-line description, and repo link. Keep it in sync when you
create or meaningfully change a project.

`projects/<slug>/` structure:

```
projects/<slug>/
├── README.md       purpose, status, what's done, repo + [[topic]] links
├── tasks.md        improvements / backlog
├── notes/          flat, YYYY-MM-DD-<topic>.md (decisions, learnings)
├── data/           CSV, JSON, dumps
└── assets/         diagrams, screenshots
```

`README.md` sections: `## Status`, `## Done`, `## Notes`. Frontmatter may
add `status` and `repo`. The improvements/backlog lives in `tasks.md` (a
checkbox list), not in README. Decision history lives in `notes/` — no
separate ADR system, no project log file.

**Bidirectional links.** A project README links the topics it applies
(`Applies [[loop-engineering]]`); a topic may carry an `## Applied in`
section linking back to projects. This makes the knowledge base
actionable — "what do I know about X, and where did I use it?".

**Statistics** (commits, activity, LOC) are deliberately out of scope
for now. When wanted, they arrive via an MCP server, not by scraping.

Creating and archiving projects is the user's job (`mkdir`, `mv`). Agent
does not volunteer to scaffold projects unless asked.

### Editing projects from another repo

Project documentation is reachable from inside a project's own repo via
the `second-brain` skill (`skills/second-brain/`), symlinked into
`~/.claude/skills` and `~/.agents/skills`. That skill points back to this
file for the schema — it does not restate the rules. When an agent in a
foreign repo records project progress, it follows the schema above.
