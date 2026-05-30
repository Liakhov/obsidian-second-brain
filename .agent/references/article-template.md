# Wiki article template

Format for files in `wiki/<topic>/<article>.md`. Use this for every
new wiki page created by INGEST or by direct user request.

## File naming

`<concept-or-entity-name>.md`, kebab-case.

- Name reflects the **concept**, not the source. "Karpathy's gist
  on LLM Wiki" → article name is `llm-wiki-pattern.md` (the
  concept), not `karpathy-gist.md` (the source).
- One concept per file. If multiple concepts emerge from one
  source, create multiple files.

## Frontmatter

```yaml
---
title: "<article title>"
type: concept | entity | synthesis | source-note
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
confidence: high | medium | low
tags:
  - <tag1>
  - <tag2>
sources:
  - "<Author or org> (YYYY-MM-DD)"
raw:
  - "[<source-filename>](../../raw/<file>.md)"
relationships:
  implements: []
  supports: []
  contradicts: []
  extends: []
  used_by: []
  supersedes: []
---
```

Field semantics:

- **type** —
  - `concept`: an idea, principle, pattern.
  - `entity`: a person, product, project, tool, organization.
  - `synthesis`: cross-source analysis, comparison, derived insight.
  - `source-note`: rare; a summary that's mostly about one source.
- **created** — date the article was first written. Never changes.
- **updated** — date the knowledge content last changed. Refreshed
  on every meaningful edit. Not filesystem mtime.
- **last_verified** — date the claims here were checked against
  current state of the world. Stale after threshold (90 days for
  fast-moving topics, 365+ for stable concepts).
- **confidence** — `high` (multiple recent sources, verified),
  `medium` (single or older sources), `low` (speculative).
- **sources** — human-readable list. Format: "Author or org (date)".
  One per line.
- **raw** — markdown links to `raw/` files. Relative from the
  article's location: `../../raw/<file>.md` if article is at
  `wiki/<topic>/`. One per yaml list item.
- **relationships** — optional typed links. Can be omitted on
  early articles; add as the base grows.

## Body sections

```markdown
# <Article title>

One sentence — the article's thesis or definition (TL;DR).

## Context / definition

Explanation in your own words. Not a copy-paste from source.
Atomic: one idea. Length proportional to depth of the concept.

## Key points

- Point 1 (with [[wikilink]] if connects to another article)
- Point 2

## See also

- [[other-article-1]] — short note on the connection
- [[other-article-2]] — short note on the connection

## Conflict
<!-- Optional. Include only if sources disagree. -->

Source A says X (link). Source B says Y (link). Source B is newer,
so the article's current claim follows B; A is preserved here for
provenance.

## Sources

- [<source-filename>](../../raw/<file>.md) — what this source contributed
- [<another-file>](../../raw/<file2>.md) — what this source contributed
```

## Rules

- **Atomicity.** One concept per page. If a page grows past ~400
  lines and covers multiple concepts, split.
- **Cite for non-trivial claims.** Link to `raw/` or another wiki
  page. Bare assertions without source = low signal.
- **Use `[[wikilinks]]` liberally.** They're the connective tissue.
- **Update `updated` on meaningful edits.** Typo fix doesn't count.
- **Don't rewrite — refactor.** When updating, preserve the
  paragraphs that still hold; rewrite only what changed.

## Anti-patterns

- ❌ Title that copies the source ("Notes from Karpathy's gist").
  Use the concept name.
- ❌ Inline quotes longer than 2-3 sentences. Paraphrase, then
  link to the raw file.
- ❌ Frontmatter with `tags: [everything-i-can-think-of]`.
  3-5 tags max.
- ❌ Confidence `high` with one source older than 6 months.
- ❌ Two pages on the same concept under slightly different names.
  Merge.
