# Second brain — Obsidian + Claude Code

Personal LLM-powered knowledge base. You curate sources and ask
questions; the agent (Claude Code, Codex, Cursor, or any that reads
`AGENTS.md`) does the bookkeeping — distilling sources into wiki pages,
cross-linking them, learning your corrections.

Inspired by [Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
and [McFarland's content wiki](https://alexmcfarland.substack.com/p/how-claude-maintains-my-content-wiki).

## Philosophy

> The LLM writes and maintains the wiki; the human reads and asks
> questions.

Topic pages grow over time. New sources add paragraphs, not new files.
Three page types — that's the whole framework.

## Structure

```
.
├── AGENTS.md          agent rules (single source of truth)
├── CLAUDE.md          symlink → AGENTS.md
├── tasks.md           global TODO
├── raw/               immutable source material (Web Clipper sink)
├── wiki/
│   ├── index.md       map of content
│   ├── history.md     user corrections that change agent behavior
│   ├── sources/       one file per ingested source
│   ├── topics/        evolving knowledge pages
│   └── patterns/      emergent insights from 3+ sources
├── projects/          active projects (PARA-style)
└── archive/           completed / stale content
```

Full schema in `AGENTS.md`.

## Quick start

1. Install [Obsidian](https://obsidian.md/) and the
   [Web Clipper](https://obsidian.md/help/web-clipper) extension.
2. Configure Web Clipper:
   - **Destination:** this vault.
   - **Note location:** `raw`.
   - **File name:** `{{date}}-{{title|safe_name}}`.
   - **Frontmatter:** `title, source, author, published, tags`.
3. Open the folder in Obsidian (Open folder as vault).
4. Run an agent that reads `AGENTS.md`:
   - [Claude Code](https://claude.com/claude-code)
   - or Codex, Cursor, opencode, etc.

First useful commands:

- `ingest raw/<file>` — distill a source into wiki pages.
- `what do I know about X?` — query the wiki with citations.
- `remember this as a correction` — append to `wiki/history.md`.
- `check vault health` — ad-hoc lint pass.

## Day-to-day

| When | What |
|---|---|
| Reading something interesting | Web Clipper → `raw/` |
| Once a day or week | "ingest new sources" |
| Anytime | "what do I know about X" |
| When the agent makes the same mistake twice | "remember this as a correction" |
| Once a month | "check vault health" |

## Optional: local images

Web Clipper stores image URLs by default. To make images local so the
agent can read them:

- Obsidian → Settings → Files and links → Attachment folder:
  `raw/assets/`.
- Settings → Hotkeys → bind "Download attachments for current file"
  (e.g. `Ctrl+Shift+D`).
- After clipping, press the hotkey.

## Credits

- [Andrej Karpathy — LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Alex McFarland — How Claude maintains my content wiki](https://alexmcfarland.substack.com/p/how-claude-maintains-my-content-wiki)
- [Tiago Forte — PARA Method](https://fortelabs.com/blog/para/)

## License

MIT — see [LICENSE](LICENSE).
