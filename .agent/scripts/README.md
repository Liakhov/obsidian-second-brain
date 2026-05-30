# scripts/

Optional utilities for vault maintenance. No external dependencies — Python 3 only.

## lint-wiki.py

Sanity-check for `wiki/`. Finds broken links, orphan pages, stale pages, pages without sources.

```bash
python3 .agent/scripts/lint-wiki.py          # staleness threshold: 90 days
python3 .agent/scripts/lint-wiki.py 30       # 30 days — for fast-moving topics
```

Exit code: `0` if clean, `2` if there are findings. Convenient for cron / pre-commit hook.

## export-graph.py

Exports the wiki graph to JSON. Not a replacement for Obsidian's graph view — useful for external visualization (D3, Graphviz) and analytics (`jq '.nodes | length' wiki-graph.json`).

```bash
python3 .agent/scripts/export-graph.py
```

Outputs: `wiki-graph.json`, `wiki-graph-summary.md` in the repo root (both are in `.gitignore`).

## When adding your own scripts

Keep them:
- Without external dependencies if possible (`stdlib` is enough).
- With a short docstring at the top.
- With exit codes that make sense.
- Without modifying `raw/`. Ever.