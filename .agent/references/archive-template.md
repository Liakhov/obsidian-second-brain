# Archive page template

Format for archived QUERY answers — synthesis pages created when
the user asks to save a derived answer back to the wiki.

## File naming

`<query-topic>.md`, kebab-case.

- Name reflects the topic of the synthesis, not the question text.
  "Compare LLM Wiki and RAG" → `llm-wiki-vs-rag.md`.
- "How does Zettelkasten fit with PARA?" →
  `zettelkasten-para-relationship.md`.

## Frontmatter

```yaml
---
title: "<archive title>"
type: synthesis
created: YYYY-MM-DD
archived_from_query: YYYY-MM-DD
confidence: high | medium | low
tags:
  - <tag1>
sources:
  - "[[other-article-1]]"
  - "[[other-article-2]]"
---
```

Differences from regular article template:

- **No `raw` field.** Archive content is synthesized from existing
  wiki pages, not directly from sources. The cited wiki pages
  trace back to raw on their own.
- **No `relationships` field.** Archives are usually leaf
  synthesis; relationships are inherited from the cited pages.
- **`archived_from_query`** date — when the user-question
  conversation produced this synthesis.
- **`type: synthesis`** is required (never `concept` or `entity`
  for archive pages).

## Body sections

```markdown
# <Archive title>

## Question

The question that produced this synthesis (1-2 sentences).

## Answer

The synthesized answer. Multi-paragraph if needed. Uses
`[[wikilinks]]` to cited articles, not raw links.

## Key points

- Point 1
- Point 2

## Sources cited

- [[article-1]] — what it contributed
- [[article-2]] — what it contributed
```

## Index entry

When archived, `wiki/index.md` gets a new entry with `[Archived]`
prefix in the summary:

```
- [llm-wiki-vs-rag](wiki/llm-wiki/llm-wiki-vs-rag.md) —
  [Archived] Side-by-side of LLM Wiki pattern vs RAG.
  Updated: YYYY-MM-DD
```

This visually distinguishes archives from ingested articles in
the index.

## Rules

- **Always a new file.** Never merge a QUERY archive into an
  existing article. Archive content is synthesized in a moment;
  ingested articles compound over time. They serve different
  purposes.
- **Cite wiki pages, not raw.** If your answer needed to go to
  raw for a quote, cite the wiki page that owns that quote first,
  and reference the raw file via that page's `raw` field.
- **One question = one archive.** Don't bundle multiple synthesis
  answers into one archive page. Atomicity applies here too.
