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

## Page types

- **`wiki/sources/`** — one file per ingested source. A short summary
  of what it claims, with examples and the key takeaway. Created
  once, rarely edited.
- **`wiki/topics/`** — your synthesized position on a subject. Grows
  as new sources touch it; never splits until it has to.
- **`wiki/patterns/`** — emergent insights that recur across 3+
  sources. Rare — typically under ten in the whole vault.

## Structure

```
.
├── AGENTS.md          agent rules (single source of truth)
├── CLAUDE.md          symlink → AGENTS.md
├── README.md          human onboarding
├── tasks.md           global TODO
├── raw/               immutable source material (Web Clipper sink)
│   └── assets/        local image attachments
├── wiki/
│   ├── index.md       map of content (MOC)
│   ├── history.md     user corrections that change agent behavior
│   ├── sources/       one file per ingested source
│   ├── topics/        evolving knowledge pages
│   └── patterns/      emergent insights from 3+ sources
├── projects/          project docs (code lives in its own repo)
│   ├── index.md       catalog of all projects
│   └── <slug>/        README, tasks, notes/, data/, assets/
└── skills/
    └── second-brain/  cross-repo bridge skill (symlinked to agents)
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

## Projects + the cross-repo skill

Projects are documented under `projects/<slug>/` (purpose, what's done,
backlog, notes). Their source code lives in its own repo elsewhere — the
vault holds only the documentation. See `AGENTS.md` for the page schema.

To read and update that documentation from **inside a project's own
repo** (where the vault isn't otherwise visible), install the
`second-brain` skill. It lives in `skills/second-brain/` and is shared
with both Claude Code and Codex via symlinks — one canonical file,
versioned with the vault.

One-time setup per machine, run from the vault root:

```bash
VAULT="$(pwd)"
mkdir -p ~/.claude/skills ~/.agents/skills
ln -sfn "$VAULT/skills/second-brain" ~/.claude/skills/second-brain   # Claude Code
ln -sfn "$VAULT/skills/second-brain" ~/.agents/skills/second-brain   # Codex
```

The skill resolves the vault path from the symlink at run time, so no
absolute path is hard-coded. Editing `skills/second-brain/SKILL.md`
updates both agents at once. On a new machine: clone the vault, re-run
the commands above.

Writing into the vault from another repo triggers a one-time permission
prompt (path outside the working directory) — allowlist the vault path
in each agent's user settings once.

## Optional: local images

Web Clipper stores image URLs by default. To make images local so the
agent can read them:

- Obsidian → Settings → Files and links → Attachment folder:
  `raw/assets/`.
- Settings → Hotkeys → bind "Download attachments for current file"
  (e.g. `Ctrl+Shift+D`).
- After clipping, press the hotkey.

## License

MIT — see [LICENSE](LICENSE).
