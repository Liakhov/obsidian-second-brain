# Second brain — Obsidian + Claude Code

Local LLM-powered knowledge base. You curate sources and ask
questions; the agent (Claude Code, Codex, Cursor, or any other
that reads `AGENTS.md`) does the bookkeeping — distilling sources
into wiki pages, cross-linking them, tracking decisions, and
learning your corrections.

Built on [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f),
extended with PARA-style projects, ADRs, and procedural memory.

## Philosophy

> "The LLM writes and maintains the wiki; the human reads and
> asks questions." — Karpathy

The wiki compounds over time. Each new source enriches it,
adds cross-references, and flags conflicts. LLMs do the
bookkeeping that humans abandon.

## Structure

```
.
├── AGENTS.md          single source of agent rules
├── CLAUDE.md          symlink → AGENTS.md
├── tasks.md           global TODO
├── inbox/             quick captures (future skill: Telegram, voice)
├── projects/          active projects (PARA-style)
├── raw/               immutable source material (Web Clipper sink)
├── wiki/              distilled knowledge (agent writes, you read)
│   ├── index.md       map
│   ├── log.md         operations log
│   ├── history.md     agent's procedural memory
│   └── meta/          ADRs about the vault itself
├── archive/           completed projects, stale content
├── .agent/            machinery
│   ├── operations/    per-operation specs (lazy-loaded by agent)
│   ├── references/    page templates
│   └── scripts/       optional Python utilities (lint, graph)
└── .obsidian/         Obsidian config
```

Full map of "what goes where" is in `AGENTS.md` §2.

## Quick start

### 1. Install tools

- [Obsidian](https://obsidian.md/) — desktop app.
- [Obsidian Web Clipper](https://obsidian.md/help/web-clipper) — browser extension.
- An agent that reads `AGENTS.md`/`CLAUDE.md`:
    - [Claude Code](https://claude.com/claude-code)
    - or Codex, Cursor, opencode, etc.

### 2. Clone and open

```bash
git clone <this-repo> my-vault
cd my-vault
```

Open the folder in Obsidian (Open folder as vault).

### 3. Configure Web Clipper

- Destination: this vault.
- Folder: `raw/<topic>/`. Web Clipper writes directly here
  (see [ADR-0004](wiki/meta/0004-web-clipper-to-raw-directly.md)).
- Frontmatter template (minimum):
  ```
  title, source, author, published, created, tags: [clippings]
  ```

### 4. Start the agent

From the repo root:

```bash
claude        # or: codex / cursor / opencode
```

The agent reads `AGENTS.md` on session start and discovers the
operations table. First useful commands:

- `"Ingest raw/<topic>/<file>"` — distill a source into wiki pages.
- `"What do I know about X?"` — query with citations.
- `"Lint vault"` — run health check.
- `"Document this decision as an ADR"` — record a vault or
  project-level decision.

## Day-to-day workflow

| When | What | How |
|---|---|---|
| Reading something interesting | Clip it | Web Clipper → `raw/<topic>/` |
| Once a day or week | Ingest new sources | "ingest all new sources" |
| Anytime | Ask the wiki | "what do I know about X" |
| Once a month | Vault health | "lint vault" |
| When making a non-trivial decision | Record it | "create ADR for X" |
| When you correct the agent twice | Lesson learned | "remember this as a lesson" |

## Operations the agent does

5 operations, fully specified in `.agent/operations/`:

- **INGEST** — compile a `raw/` source into wiki pages.
- **QUERY** — search wiki, answer with citations, optionally
  archive synthesis answers.
- **LINT** — Python-script-based deterministic checks plus
  agent-judgment heuristic checks.
- **ADR-CREATE** — record a decision at vault or project level
  with proper numbering and supersession links.
- **HISTORY-LOG** — append corrections to procedural memory.

## Optional: download images locally for clipped pages

By default, Web Clipper stores images as remote URLs. To make
images available offline (and for the agent to read them
directly):

- Settings → Files and links → Attachment folder path:
  `raw/assets/`.
- Settings → Hotkeys → bind "Download attachments for current file"
  (e.g. `Ctrl+Shift+D`).
- After clipping an article, press the hotkey → images saved
  locally → agent can read them.

## Credits and inspiration

- [Andrej Karpathy — LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Astro-Han — karpathy-llm-wiki Agent Skill](https://github.com/Astro-Han/karpathy-llm-wiki)
- [Tiago Forte — The PARA Method](https://fortelabs.com/blog/para/)

## License

MIT — see [LICENSE](LICENSE).