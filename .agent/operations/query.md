# QUERY

> If you are executing this operation, read this file fully before any
> action. Do not rely on summaries from elsewhere.

Search the wiki and answer a question. Optionally archive the answer
back as a new wiki page.

## Required plan fields

**Mode 1 (read-only query):** no plan needed. Reading doesn't change
state. Just answer.

**Mode 2 (archive sub-operation):** plan must include:
- **Archive path** — `wiki/<topic>/<derived-name>.md`
- **Page type** — `synthesis`
- **Sources cited** — list of wiki pages
- **Index update note** — entry with `[Archived]` prefix
- **Log entry preview** — line for `wiki/log.md`

Then: "Archive? (yes / no / rename it)"

## Mode 1: Simple query

### Steps
1. Read `wiki/index.md` to locate relevant articles.
2. Read those articles.
3. Synthesize an answer. **Prefer wiki content over training knowledge.**
4. Cite sources with markdown links:
   `[Article Title](wiki/<topic>/<article>.md)` (project-root-relative
   paths in conversation output).
5. Output the answer in chat. Do NOT write files.

### After answering — decide whether to propose archive

Propose archive when the answer contains a **durable synthesis** that
didn't exist before. Heuristics:

| Propose archive | Don't propose |
|---|---|
| Multi-source comparison ("Obsidian vs Notion") | Simple factual lookup ("who wrote X") |
| Derived insight ("what pattern across these 4 sources?") | Definitional question ("what is Y") |
| Cross-topic synthesis | Status question ("latest source I ingested") |

If unsure, don't propose. Better under-archive than spam.

When proposing, jump to Mode 2.

## Mode 2: Archive sub-operation

Triggered by user saying "archive", "save this", "yes" after Mode 1
proposal, or explicit "archive this answer" command.

### Steps
1. Read `.agent/references/archive-template.md`.

2. Compose the new wiki page:
    - **File name** reflects the query topic, not the question text.
      "Compare LLM Wiki and RAG" → `llm-wiki-vs-rag.md`.
    - **Path** — `wiki/<topic>/<derived-name>.md` in the most
      relevant topic subdir.
    - **Page type** — `synthesis` (in frontmatter).
    - **Sources field** — markdown links to wiki articles cited.
    - **No Raw field** — this content doesn't come from `raw/`.
    - Convert conversation-style paths
      (`wiki/topic/article.md`) to file-relative paths
      (`../topic/article.md` or `article.md` for same dir).

3. **Always create a new page.** Never merge into existing articles —
   archive content is synthesized, not raw material.

4. Update `wiki/index.md`. Prefix the `Summary` with `[Archived]`
   so the entry is visually distinct from ingested articles.

5. Append to `wiki/log.md`:

   ```
   ## [YYYY-MM-DD] query | Archived: <page title>
   ```

## Edge cases

**No relevant articles in wiki.** Tell the user: "No wiki pages on
this topic. Check `raw/` directly, or ingest a source first?"
Don't fabricate from training knowledge.

**Index disagrees with files** (page in index but file missing, or
vice versa). Note the inconsistency in the answer; suggest running
LINT.

**Question requires `raw/` access** ("what's the exact quote from X?").
Read the specific raw file. Cite both wiki page and raw file.

**Question is ambiguous** ("tell me about machine learning"). If a
hub article or topic index exists, start there. Otherwise list
available articles and ask user to narrow.

**Archive proposed but user declines.** That's fine. Don't insist.
Don't re-propose later in the same conversation.

**User asks to archive a Mode 1 answer that's already simple/factual.**
Confirm: "This is a short factual answer, not a synthesis. Archive
anyway?"

## Post-checklist (Mode 2 only)

- [ ] Did I read this spec at the start?
- [ ] Does the plan have all required fields?
- [ ] Is the archive page using the archive template?
- [ ] Does `wiki/index.md` entry have `[Archived]` prefix?
- [ ] Is `wiki/log.md` updated?

## Files

**Reads (Mode 1):** `wiki/index.md`, relevant wiki articles,
optionally `raw/` files.

**Reads (Mode 2):** above, plus `.agent/references/archive-template.md`.

**Writes (Mode 1):** nothing.

**Writes (Mode 2):** one new wiki page, `wiki/index.md`, `wiki/log.md`.