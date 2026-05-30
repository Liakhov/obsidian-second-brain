# Raw source template

This is the exact format for files in `raw/`. Used when manually saving a source or
when Web Clipper drops a file.

## File naming

`YYYY-MM-DD-<source-slug>.md`

- `YYYY-MM-DD` — date the source was collected (today), not the
  source's publication date.
- `<source-slug>` — kebab-case from source title, max 60 chars,
  no articles.
- If publication date is unknown and the slug is unique enough,
  the date prefix may be dropped (e.g., `descriptive-slug.md`),
  but the `Published` frontmatter field must still be present
  (set to `Unknown`).
- If the name collides, append `-2`, `-3`, etc.

## Frontmatter (required)

```yaml
---
title: "<source title>"
source: "<URL or 'manual entry'>"
author:
  - "<name>"
published: YYYY-MM-DD | Unknown
collected: YYYY-MM-DD
tags:
  - clippings
---
```

## Body

After frontmatter, preserve the original source content. Clean up
formatting noise (broken whitespace, nav menus from web pages,
ads) but **do not** rewrite, paraphrase, or summarize opinions.
This is the source of truth.

If the source is non-English, keep it in the original language.
Translation happens at the wiki layer, not here.

## What NOT to do

- Don't add commentary in the raw file.
- Don't link to other wiki pages from inside the raw file.
- Don't modify the body after first save — even to fix typos.
  This file is immutable. Mistakes are documented separately
  in the wiki layer if needed.
- Don't add to the frontmatter beyond the required fields above
  (the agent uses these specifically; extra fields are ignored).

## Why this matters

The raw file is the audit trail. When a wiki claim is challenged,
agent (or user) traces back to `raw/` and sees the original
source unchanged. If raw drifts from the original, the system's
trust breaks down.
