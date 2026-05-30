# INGEST

> If you are executing this operation, read this file fully before any
> action. Do not rely on summaries from elsewhere.

Compile a source from `raw/` into wiki pages.

## Required plan fields

Before writing any file, show a plan that includes:

- **Source path** — exact `raw/<file>.md`
- **New pages** — list of paths to be created (or "none")
- **Updated pages** — list of paths to be modified (or "none")
- **Cross-reference count** — N new `[[wikilinks]]`
- **Index update note** — what changes in `wiki/index.md`
- **Source Notes entry preview** — the entry going into `wiki/Source Notes.md` (status, confidence, derived pages)
- **Log entry preview** — the line going into `wiki/log.md`

Then: "Proceed?"

If any field is missing from your plan, you skipped this spec.
Stop and re-read.

## Steps after confirmation

### 1. Read source
Open the file at `raw/<file>.md`. Parse frontmatter (title,
source URL, author, published date). If frontmatter is missing or
incomplete, use file name as title and note the gap; don't fail.

### 2. Determine topic
All raw files live at `raw/` root. Determine
the topic from the source's content: frontmatter `tags`, title, and
body. Cross-check against existing `wiki/<topic>/` subdirs to prefer
an existing topic over a new one.

- If one topic is obvious and matches an existing `wiki/<topic>/` —
  use it; no need to ask.
- If the source spans 2-3 topics — propose primary + secondary, ask
  user to confirm primary placement.
- If a brand-new topic would be created — propose name and confirm
  before creating `wiki/<topic>/`.

### 3. Read article template
Read `.agent/references/article-template.md` to know the exact
article format. Use that format for any new pages.

### 4. Read current state
- `wiki/index.md` — to know what already exists.
- Last 10 entries of `wiki/log.md` — for recent activity context.
- If `wiki/<topic>/` exists, list its articles.

### 5. Extract key concepts
From the source, extract 3-15 key ideas / entities / facts. More
than ~15 makes pages unfocused. Fewer than 3 means the source
isn't worth a wiki page yet — still add it to `wiki/Source Notes.md`
(step 11), but skip steps 6–9.

### 6. Decide page placement per concept

For each concept:

- **Same thesis as existing article** → merge into it. Add the
  new source to `Sources` and `Raw` fields. Update affected
  sections.
- **New concept** → create new article at
  `wiki/<topic>/<concept-name>.md`. Name reflects the concept,
  not the source file.
- **Spans multiple topics** → place in the most relevant subdir.
  Add `See Also` cross-references to related articles elsewhere.

These are not exclusive. One source can merge into one article
AND create another for a distinct concept it introduces.

### 7. Check for conflicts
For each merge, compare new claims against existing ones:
- If new contradicts old, do NOT overwrite.
- Add a `## Conflict` block listing both versions with attribution
  and dates.
- If the conflict spans two pages, note it in both and cross-link.

### 8. Cascade updates
After the primary article:
- Scan articles in the same topic-subdir for content affected by
  the new source.
- Scan `wiki/index.md` entries in other topics for related concepts.
- Update every article whose content is materially affected.
- Refresh `Updated` frontmatter date on each touched article.
- **Archive pages are never cascade-updated** — they are
  point-in-time snapshots.

### 9. Update index
Update `wiki/index.md`:
- Add or modify entries for every touched article.
- When adding a new topic section, include a one-line description.
- `Updated` date reflects when knowledge content last changed —
  not filesystem mtime.

### 10. Append to log
Append to `wiki/log.md`:

```
## [YYYY-MM-DD] ingest | <primary article title>
- Source: raw/<file>.md
- Created: <new article paths or omit line>
- Updated: <updated article paths or omit line>
```

### 11. Update Source Notes
Append an entry to `wiki/Source Notes.md` under `## Entries`,
using the template documented at the top of that file. Required
fields: File link to `raw/`, URL (if present), Author, Published,
Ingested (today), Status (`active`), Confidence, Key terms,
3–5 line summary, Derived pages (links to the articles created
or updated in steps 6–9; "none" if step 5 produced too few concepts).

Re-ingest of an existing source: update the existing entry in place
(refresh `Ingested` date, add new derived pages, bump status if
needed). Do not create a duplicate entry.

## Edge cases

**Source already ingested.** If `wiki/log.md` already has an
ingest entry for this source, ask: "This was ingested on <date>.
Re-process? May cause conflicts with current wiki content."

**Topic subdir doesn't exist in `wiki/`.** Create it. Don't ask.

**No clear primary article emerges** (source is a disparate list).
Ask: "This source touches 6 unrelated concepts. Create 6 small
articles, or merge into a single source-summary page?"

**Frontmatter missing required fields** (no title, no URL).
Use file name as title, leave URL empty, log a warning in chat.
Don't ask, don't fail.

**Source is non-English.** Wiki page can be in English with quotes
preserved in original. Ask user only if unclear.

**Batch ingest** (user says "ingest all new sources").
- Scan `raw/` for files not appearing in `wiki/log.md` ingest entries.
- Show combined plan: list all sources, summary of expected pages.
- Process one at a time to preserve quality of cross-references.
- One log entry per source, not one combined entry.

## Post-checklist (verify before declaring done)

- [ ] Did I read this spec file at the start of this operation?
- [ ] Does my plan include all required fields above?
- [ ] Are all new/updated files actually written?
- [ ] Is `wiki/index.md` updated?
- [ ] Is `wiki/log.md` updated with the standard format?
- [ ] Is `wiki/Source Notes.md` updated with an entry for this source?
- [ ] Did cascade updates touch every materially affected page?

## Files

**Reads:** source file in `raw/`, `wiki/index.md`, last entries
of `wiki/log.md`, `wiki/Source Notes.md` (to check for existing
entry), target wiki articles, `.agent/references/article-template.md`.

**Writes:** new/updated `wiki/<topic>/*.md`, `wiki/index.md`,
`wiki/log.md`, `wiki/Source Notes.md`.