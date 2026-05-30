# ADR-CREATE

> If you are executing this operation, read this file fully before any
> action. Do not rely on summaries from elsewhere.

Create an Architecture Decision Record at the right level
(vault or project) with proper numbering and logging.

## Required plan fields

Before writing, show plan with:

- **Level** — `vault` or `project:<slug>`
- **Path** — `wiki/meta/NNNN-<slug>.md` or
  `projects/<X>/decisions/NNNN-<slug>.md`
- **Number** — next available NNNN (4-digit zero-padded)
- **Title** — short imperative
- **Status** — `proposed` or `accepted`
- **Supersedes** — link to old ADR if applicable, else "none"
- **Log entry preview** — line for the appropriate log

Then: "Proceed?"

## Steps after confirmation

### 1. Determine level

- User explicitly says "vault ADR" / "global decision" → vault.
- User says "ADR for project X" → project.
- If unclear, ask one question:
  "Is this about the vault itself, or about project <X>?"

Tie-breaker rule (use silently when context makes it obvious):
- Concerns naming conventions, file structure, workflow rules,
  agent behavior → **vault ADR**.
- Concerns project's tech stack, scope, architecture, product
  decisions → **project ADR**.

### 2. Find next number

Scan target directory for existing `NNNN-...md` files. Take max
number + 1, pad to 4 digits.

- `wiki/meta/0001-...md` ... `0042-...md` → next is `0043`.
- New directory with no ADRs yet → start at `0001`.

### 3. Build slug

From decision title, kebab-case, max 50 chars. Strip articles.
- "Use PostgreSQL instead of MongoDB" → `postgres-over-mongo`.
- "Centralize tasks in a single file" → `tasks-centralized`.

If slug already exists in target dir (rare), append `-2`.

### 4. Read template

Read `.agent/references/adr-template.md`.

### 5. Gather ADR content

Ask user the four standard ADR questions in one combined prompt
(not four separate):

```
ADR-NNNN: <title>

Fill in each (or "—" to skip — I'll mark as TODO):
  • Context (what's the situation, what's the tradeoff?):
  • Decision (what we chose, imperative):
  • Consequences (what becomes easier / harder?):
  • Alternatives (what we considered and rejected, briefly):
```

For "—" fields, leave a placeholder: `<!-- TODO: fill in -->`.

### 6. Set frontmatter

- `status` — `proposed` if user weighing an idea; `accepted` if
  documenting a made decision. **Default: `accepted`.**
- `date: YYYY-MM-DD` — today.
- `tags: [...]` — derived from context. Ask only if unclear.
- `supersedes: [[NNNN-<old-slug>]]` — only if applicable.

### 7. Write file at target path

### 8. Cross-link if supersedes

If this ADR supersedes an existing one:
- Ask which old ADR (if not already clear).
- Update old ADR's frontmatter:
  `status: superseded by [[NNNN-<new-slug>]]`.
- **Do NOT delete the old ADR.** Supersession is explicit history.

### 9. Append to appropriate log

**Vault ADR** → `wiki/log.md`:

```
## [YYYY-MM-DD] adr | vault | NNNN-<slug> — <title>
```

**Project ADR** → `projects/<slug>/log.md`:

```
## [YYYY-MM-DD] adr | NNNN-<slug> — <title>
```

If `projects/<slug>/log.md` doesn't exist, create it with header
`# Log — <project name>` first.

## Edge cases

**Description too vague** ("ADR about how we organize stuff").
Ask for a concrete decision statement before creating.

**It's a question, not a decision** ("ADR: should we use Postgres?").
Suggest: "This sounds like an open question. Create as
`status: proposed` (we're still weighing it), or wait until decided?"

**Multiple decisions bundled in one ADR.** Suggest splitting:
one decision per ADR makes superseding cleaner later.

**User wants to update an existing ADR.** Ask:
"Updating an ADR usually means superseding it. Create a new one
that supersedes <old>, or amend the existing in place?"
Default behavior: supersede.

**Slug collision in target dir.** Append `-2` (or `-3`, etc.).
Don't ask — this is mechanical.

**User asks for ADR but project doesn't exist yet.** Ask:
"No `projects/<slug>/` found. Create the project first, or
make this a vault-level ADR?"

## Post-checklist

- [ ] Did I read this spec at the start?
- [ ] Does the plan include all required fields?
- [ ] Is the number correctly the next available?
- [ ] Is the file at the right path (vault vs project)?
- [ ] If superseding, did I update the old ADR's status?
- [ ] Did I log to the right log file (`wiki/log.md` or project log)?

## Files

**Reads:** target directory for numbering,
`.agent/references/adr-template.md`, optionally old ADR being
superseded.

**Writes:** new ADR file, optionally updated old ADR (status),
`wiki/log.md` (vault) or `projects/<slug>/log.md` (project).