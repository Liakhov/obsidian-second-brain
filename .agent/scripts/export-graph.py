#!/usr/bin/env python3
"""
export-graph.py — exports the wiki graph to JSON for external visualization.

No external dependencies. Usage:
    python3 .agent/scripts/export-graph.py

Output files (in the repo root):
  - wiki-graph.json — full graph (nodes + edges).
  - wiki-graph-summary.md — text summary.

Obsidian already has a native graph view — this script is useful for external
visualization (D3.js, Graphviz, Cytoscape) or for analytics via jq.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
WIKI = ROOT / "wiki"

WIKILINK_RE = re.compile(r"\[\[([^\[\]|#]+)(?:#[^\[\]|]*)?(?:\|[^\[\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
TYPE_RE = re.compile(r"^type:\s*(\S+)", re.MULTILINE)


def page_type(text: str) -> str:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "unknown"
    t = TYPE_RE.search(m.group(1))
    return t.group(1) if t else "unknown"


def main() -> int:
    if not WIKI.exists():
        print(f"wiki/ not found at {WIKI}", file=sys.stderr)
        return 1

    pages = {p.stem: p for p in WIKI.rglob("*.md") if not p.name.startswith(".")}
    nodes = []
    edges = []
    out_degree: dict[str, int] = defaultdict(int)
    in_degree: dict[str, int] = defaultdict(int)

    for name, path in pages.items():
        text = path.read_text(encoding="utf-8")
        nodes.append({
            "id": name,
            "path": str(path.relative_to(ROOT)),
            "type": page_type(text),
        })
        for match in WIKILINK_RE.finditer(text):
            target = match.group(1).rsplit("/", 1)[-1].strip()
            edges.append({"source": name, "target": target})
            out_degree[name] += 1
            in_degree[target] += 1

    graph = {"nodes": nodes, "edges": edges}
    (ROOT / "wiki-graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Summary
    top_in = sorted(in_degree.items(), key=lambda kv: -kv[1])[:10]
    top_out = sorted(out_degree.items(), key=lambda kv: -kv[1])[:10]
    summary_lines = [
        "# Wiki Graph — Summary",
        "",
        f"- Pages: **{len(nodes)}**",
        f"- Links: **{len(edges)}**",
        "",
        "## Top 10 hubs (inbound links)",
        *[f"- {name}: {count}" for name, count in top_in],
        "",
        "## Top 10 by outbound links",
        *[f"- {name}: {count}" for name, count in top_out],
    ]
    (ROOT / "wiki-graph-summary.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )

    print(f"Exported {len(nodes)} nodes, {len(edges)} links")
    print(f"  → wiki-graph.json")
    print(f"  → wiki-graph-summary.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
