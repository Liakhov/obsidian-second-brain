# LINT

> If you are executing this operation, read this file fully before any
> action. Do not rely on summaries from elsewhere.

Vault health check. Hybrid: Python script for deterministic checks,
agent judgment for heuristic ones.

## Required plan fields

Before action, show plan with:

- **Script availability** — confirm `.agent/scripts/lint-wiki.py` exists
- **Phase 1 (auto-fix)** — list categories that will be fixed without ask
- **Phase 2 (report)** — list heuristic categories
- **Bulk fix gate** — confirm with user if auto-fixes would touch >10 files
- **Log entry preview** — line for `wiki/log.md`

Then: "Proceed?"

## Phase 1 — Deterministic (Python script)

### Steps
1. Run `python3 .agent/scripts/lint-wiki.py`. Capture output.

2. Parse the output. Findings categories:
    - Broken `[[wikilinks]]`
    - Broken `raw/` refs
    - Missing index entries (article exists but not in `wiki/index.md`)
    - Index entries pointing to nonexistent files
    - Stale pages (`last_verified` older than threshold)
    - Pages without sources
    - Orphan pages (no inbound links — except in `IGNORE_PAGES` list)

3. **Auto-fix where safe.** For each finding:

   **Auto-fix (no ask):**
    - Missing index entry → add with placeholder summary `(no summary)`
      if article lacks `## Summary` section.
    - Index entry pointing to nonexistent file → mark as `[MISSING]`
      in index (do NOT delete).
    - Broken `[[wikilink]]` where exactly one alternative file has the
      same name elsewhere in `wiki/` → fix the path.
    - Broken `raw/` link where exactly one alternative raw file has
      the same name → fix the path.

   **Report, don't fix:**
    - Broken `[[wikilink]]` with zero matches → report.
    - Broken `[[wikilink]]` with multiple matches → list candidates,
      ask user.
    - Stale pages → report. Don't auto-update `last_verified`.
    - Pages without sources → report.

4. **Bulk fix gate.** If Phase 1 would auto-fix more than 10 files,
   stop and show user the list before proceeding. Bulk movement
   often indicates a directory rename — needs human review.

5. Update `wiki/index.md` if any auto-fixes affected it.

## Phase 2 — Heuristic (agent judgment)

### Steps
6. **Orphans review.** For each orphan from script:
    - Skip if file is in `IGNORE_PAGES`:
      `index`, `log`, `history`, `Source Notes`, `_template`.
    - Read the page. Decide:
        - Hub-page that should have inbound links but doesn't →
          report as actionable.
        - Leaf-page naturally isolated (one-off synthesis) →
          acceptable, skip.

7. **Contradictions scan.** Read the latest 5-10 ingested articles
   (from `wiki/log.md` ingest entries). For each, check whether
   claims conflict with claims in other recently-updated articles.
    - If a contradiction is detected, do NOT auto-fix.
    - Propose a conflict-note: which articles, which claims,
      which sources, which is newer/more authoritative.
    - Ask user to resolve.

8. **Stale claims (semantic).** For pages with `confidence: low`
   or `last_verified` > 180 days on fast-moving topics
   (AI, products, tools), read the page, check sources, decide
   if it may be obsolete. Report findings. Don't auto-update.

9. **Concept-without-page.** Scan articles for `[[wikilinks]]` to
   pages that don't exist (already caught by deterministic check).
   Among them, find concepts referenced 3+ times across different
   articles. These earned their own page but don't have one.
   Report as suggestions.

## Phase 3 — Report and log

10. **Summary to user.** Structured output:

    ```
    Lint results:
      ✓ Auto-fixed: N
        • <category>: <count>
      ⚠ Needs attention: M
        • <category>: <count, with file links>
      ℹ Suggestions: K
        • <category>: <items>
    ```

11. **Append to `wiki/log.md`:**

    ```
    ## [YYYY-MM-DD] lint | <N> findings, <M> auto-fixed
    - Auto-fixed: <brief list>
    - Reported: <brief list>
    ```

## Edge cases

**Script fails to run** (Python missing, syntax error).
Fall back to agent-only manual scan. Tell user: "script unavailable,
doing manual lint (slower)." Skip categories that require systematic
scanning (orphans, all-page indexes) and focus on recently-touched
articles.

**Script returns suspicious finding count** (e.g., 100+ broken links).
Likely a moved directory. Show count first, ask: "this looks like
bulk movement, proceed with auto-fix or pause to investigate?"

**Heuristic check finds nothing.** Don't fabricate findings. Say
"no heuristic issues detected" and move on.

**LINT triggered on a vault with <10 wiki pages.** Skip orphan
detection and concept-without-page checks — too noisy at small
scale. Run only broken-link and stale-page checks.

## Post-checklist

- [ ] Did I read this spec at the start?
- [ ] Was the Python script actually run?
- [ ] Were auto-fixes applied only to the safe categories?
- [ ] Did I respect the >10 file bulk gate?
- [ ] Is the summary structured (auto-fixed / needs attention / suggestions)?
- [ ] Is `wiki/log.md` updated?

## Files

**Reads:** all `wiki/**/*.md`, all `raw/**/*.md` (for ref validation),
`wiki/log.md`.

**Writes:** auto-fixes in affected wiki files, `wiki/index.md`
(if entries fixed), `wiki/log.md`.