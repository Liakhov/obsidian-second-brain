# ADR template

Used by ADR-CREATE for both vault ADRs (`wiki/meta/`) and project
ADRs (`projects/<X>/decisions/`). Format is identical at both levels.

## File naming

`NNNN-<slug>.md`

- `NNNN` — four-digit zero-padded sequential number. `0001`, `0042`.
- `<slug>` — kebab-case from decision title, max 50 chars, no articles.
- Numbering is per-directory: vault ADRs and project ADRs have
  separate counters. `wiki/meta/0001-...` and
  `projects/my-app/decisions/0001-...` can coexist.

## Frontmatter

```yaml
---
status: proposed | accepted | superseded by [[NNNN-<new-slug>]] | deprecated
date: YYYY-MM-DD
tags:
  - <tag1>
supersedes: [[NNNN-<old-slug>]]   # only if this ADR supersedes another
---
```

Status values:
- **proposed** — being weighed, not yet decided.
- **accepted** — current active decision.
- **superseded by [[NNNN-<x>]]** — replaced by a newer ADR. Old
  one is preserved with this status; never deleted.
- **deprecated** — no longer relevant but not directly superseded
  (rare; usually use supersession).

## Body

```markdown
# ADR-NNNN: <short imperative title>

## Context

What's the situation? What tradeoff or problem prompted this?
2-5 sentences. No fluff.

## Decision

What we chose. One or two short sentences. Imperative voice.

## Consequences

- What becomes easier.
- What becomes harder.
- Which doors close, which open.

## Alternatives

What we considered and rejected. One line per alternative with
the rejection reason.

- **<alternative A>.** Rejected because <reason>.
- **<alternative B>.** Rejected because <reason>.
```

Sections are required. If a section is genuinely empty (e.g., no
alternatives considered), say so explicitly: "No alternatives
considered — decision was forced by <constraint>." Don't omit
the section.

## Rules

- **Atomicity.** One ADR = one decision. If a "decision" has 3
  parts, that's 3 ADRs.
- **Imperative titles.** "Use PostgreSQL" not "Use of PostgreSQL"
  or "Why we chose PostgreSQL".
- **Past decisions are immutable.** When something changes,
  create a new ADR that supersedes the old one. Don't edit the
  old ADR's body.
- **Status is the only field that may change post-creation** —
  and only when superseding or deprecating.

## When to write an ADR

| Yes | No |
|---|---|
| Picked one of multiple valid options | Chose obvious default |
| Decision you'll forget the reasoning for in 3 months | Trivial implementation detail |
| Affects how future contributors / future-you works | Will be undone in a week |
| Cross-cutting (touches multiple parts of system) | Local to one file |

## Vault vs project — which level?

- **Vault ADR (`wiki/meta/`)**: about how the vault itself works.
  Naming conventions, structure, workflow rules, agent behavior.
- **Project ADR (`projects/<X>/decisions/`)**: about a specific
  project. Tech stack, scope, product decisions, architecture.

If unsure: vault-level ADRs apply across all projects; project
ADRs would only matter for one project.
