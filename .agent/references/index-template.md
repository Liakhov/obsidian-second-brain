# Index template

Format for `wiki/index.md`. This is the wiki's map and entry point.

## Structure

```markdown
# Knowledge base index

> Entry point. Browse by topic, or use Obsidian search.

## <Topic 1>

One-line description of what this topic covers.

- [[<topic-1>/article-a]] — one-line summary.   Updated: YYYY-MM-DD
- [[<topic-1>/article-b]] — one-line summary.   Updated: YYYY-MM-DD
- [[<topic-1>/article-c]] — [Archived] one-line summary.  Updated: YYYY-MM-DD

## <Topic 2>

One-line description.

- [[<topic-2>/article-x]] — one-line summary.   Updated: YYYY-MM-DD

## Meta

Decisions about the vault itself.

- [[meta/0001-agents-as-single-source]] — why one schema file.   Updated: YYYY-MM-DD
- [[meta/0002-tasks-centralized]] — why tasks in a single file.   Updated: YYYY-MM-DD
```

## Rules

- **One entry per article.** Don't list the same article under
  multiple topics. If an article spans topics, place it in the
  most relevant one and use `See also` cross-references in the
  article itself.
- **One-line summary.** Not a paragraph. If the article needs
  more, that's what the article body is for.
- **Updated date** is the article's `updated` frontmatter date,
  not filesystem mtime, not today.
- **Archived entries** get `[Archived]` prefix in the summary —
  visually distinguishes synthesis archives from ingested
  articles.
- **`[MISSING]` prefix** marks entries whose file is gone (caught
  by LINT). Don't delete the entry; let user decide.
- **Topic order** — alphabetical by default. Pin a "Start here"
  or "Meta" section at top/bottom if useful.

## When to add a topic

A topic-subdir in `wiki/` deserves an index section once it has
2+ articles. One-article topics can be listed under a generic
"Misc" section until they grow.

## Anti-patterns

- ❌ Index entries with two-line summaries.
- ❌ Topics that don't match actual `wiki/` subdirectories.
- ❌ Listing log.md / history.md / Source Notes as articles.
- ❌ Including `meta/` ADRs as a "section" mixed with content
  topics — keep ADRs in their own section.
