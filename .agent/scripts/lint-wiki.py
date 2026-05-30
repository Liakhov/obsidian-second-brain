#!/usr/bin/env python3
"""
lint-wiki.py — a simple health-check for the Obsidian LLM Wiki.

No external dependencies (stdlib only). Usage:
    python3 .agent/scripts/lint-wiki.py

Checks in wiki/:
  1. Broken [[wikilinks]] — links to pages that do not exist.
  2. Orphan pages — pages with no inbound links.
  3. Stale pages — last_verified > 90 days (threshold is configurable).
  4. Pages without sources — empty sources in frontmatter / no sources block.
  5. Broken links to raw/ — markdown links to files missing from raw/.

This is a hint, not an auto-fix. Fixing is the agent's/human's job.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
STALE_DAYS_DEFAULT = 90

WIKILINK_RE = re.compile(r"\[\[([^\[\]|#]+)(?:#[^\[\]|]*)?(?:\|[^\[\]]*)?\]\]")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
LAST_VERIFIED_RE = re.compile(r"^last_verified:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
SOURCES_FM_RE = re.compile(r"^sources:\s*\n((?:\s+-\s+.+\n)*)", re.MULTILINE)


def collect_wiki_pages() -> dict[str, Path]:
    """Map page name (without .md) → path."""
    pages: dict[str, Path] = {}
    for path in WIKI.rglob("*.md"):
        if path.name.startswith("."):
            continue
        pages[path.stem] = path
    return pages


def parse_frontmatter(text: str) -> str:
    m = FRONTMATTER_RE.match(text)
    return m.group(1) if m else ""


def find_broken_wikilinks(pages: dict[str, Path]) -> list[tuple[Path, str]]:
    broken = []
    page_names = set(pages.keys())
    for page_name, page_path in pages.items():
        text = page_path.read_text(encoding="utf-8")
        for match in WIKILINK_RE.finditer(text):
            target = match.group(1).strip()
            # Strip path/subfolder if present: [[concepts/Zettelkasten]] → "Zettelkasten"
            target_name = target.rsplit("/", 1)[-1]
            if target_name not in page_names:
                broken.append((page_path, target))
    return broken


def find_orphan_pages(pages: dict[str, Path]) -> list[Path]:
    """Pages with no inbound [[wikilinks]]. index.md and log.md are ignored."""
    inbound: dict[str, int] = defaultdict(int)
    for page_path in pages.values():
        text = page_path.read_text(encoding="utf-8")
        for match in WIKILINK_RE.finditer(text):
            target_name = match.group(1).rsplit("/", 1)[-1].strip()
            inbound[target_name] += 1
    ignore = {"index", "log", "Source Notes"}
    return [p for name, p in pages.items() if name not in ignore and inbound[name] == 0]


def find_stale_pages(pages: dict[str, Path], stale_days: int) -> list[tuple[Path, int]]:
    threshold = date.today() - timedelta(days=stale_days)
    stale = []
    for page_path in pages.values():
        text = page_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        m = LAST_VERIFIED_RE.search(fm)
        if not m:
            continue
        try:
            verified = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        if verified < threshold:
            stale.append((page_path, (date.today() - verified).days))
    return stale


def find_pages_without_sources(pages: dict[str, Path]) -> list[Path]:
    ignore = {"index", "log", "Source Notes"}
    without = []
    for name, page_path in pages.items():
        if name in ignore:
            continue
        text = page_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        has_fm_sources = bool(SOURCES_FM_RE.search(fm))
        has_sources_section = "## Sources" in text
        if not (has_fm_sources or has_sources_section):
            without.append(page_path)
    return without


def find_broken_raw_links(pages: dict[str, Path]) -> list[tuple[Path, str]]:
    broken = []
    for page_path in pages.values():
        text = page_path.read_text(encoding="utf-8")
        for match in MD_LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Resolve relative to the page
            resolved = (page_path.parent / target).resolve()
            # Only care about links into raw/
            try:
                resolved.relative_to(RAW)
            except ValueError:
                continue
            if not resolved.exists():
                broken.append((page_path, target))
    return broken


def report_section(title: str, items: list, formatter) -> None:
    print(f"\n=== {title} ({len(items)}) ===")
    if not items:
        print("  ✓ nothing found")
        return
    for item in items:
        print(f"  • {formatter(item)}")


def main() -> int:
    if not WIKI.exists():
        print(f"wiki/ not found at {WIKI}", file=sys.stderr)
        return 1

    stale_days = STALE_DAYS_DEFAULT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        stale_days = int(sys.argv[1])

    pages = collect_wiki_pages()
    print(f"Scanning {len(pages)} pages in {WIKI}")

    broken_links = find_broken_wikilinks(pages)
    orphans = find_orphan_pages(pages)
    stale = find_stale_pages(pages, stale_days)
    no_sources = find_pages_without_sources(pages)
    broken_raw = find_broken_raw_links(pages)

    rel = lambda p: p.relative_to(ROOT)
    report_section("Broken [[wikilinks]]", broken_links,
                   lambda t: f"{rel(t[0])} → [[{t[1]}]]")
    report_section("Orphan pages (no inbound links)", orphans, rel)
    report_section(f"Stale pages (last_verified > {stale_days} days)", stale,
                   lambda t: f"{rel(t[0])} ({t[1]} days)")
    report_section("Pages without sources", no_sources, rel)
    report_section("Broken links to raw/", broken_raw,
                   lambda t: f"{rel(t[0])} → {t[1]}")

    total = len(broken_links) + len(orphans) + len(stale) + len(no_sources) + len(broken_raw)
    print(f"\nTotal findings: {total}")
    return 0 if total == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
