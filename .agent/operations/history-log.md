# HISTORY-LOG

> If you are executing this operation, read this file fully before any
> action. Do not rely on summaries from elsewhere.

Append a correction or lesson to the agent's procedural memory at
`wiki/history.md`.

## Triggers

**Explicit:**
- "remember this", "save as lesson"
- "next time, do X instead of Y"
- "log this correction"

**Implicit:**
- User corrected the same kind of thing **twice in the same
  conversation** → agent proposes: "Want me to log this as a
  recurring correction?"

**NOT triggered by:**
- A single one-off fix.
- A typo correction.
- A specific content edit ("change line 3").

## Required plan fields

Before writing, show the entry preview:

```
I'll append to wiki/history.md:

  ## [YYYY-MM-DD HH:MM] correction
  - Context: <one line>
  - Correction: <one or two lines>
  - Lesson: <one line, imperative>

Proceed?
```

For implicit triggers (agent-detected pattern), show the full
proposed text and **let user edit before commit**.

## Steps after confirmation

### 1. Read history file
Read current `wiki/history.md`. Count entries (count `## [` lines).

### 2. Archive oldest if at limit
If count >= 20:
- Move the oldest entry to `wiki/history-archive.md`.
- Create archive file if missing, with header `# History Archive`.
- Result: latest 19 in `history.md` + new entry = 20.
- This is automatic, no ask.

### 3. Format the entry
Read `.agent/references/history-entry-format.md` if uncertain about
format. Template:

```
## [YYYY-MM-DD HH:MM] correction
- Context: <what I was doing>
- Correction: <what the user fixed or asked differently>
- Lesson: <what I should do differently next time>
```

All three fields required. Don't write entries with empty fields.

### 4. Append to `wiki/history.md`
Don't overwrite existing entries. Append at the end of the file,
preserving chronological order (oldest first, newest last).

### 5. Confirm to user
Show appended entry and current count:
"Logged. history.md now at 14/20."

## What counts as a lesson

| Yes (write to history) | No (don't write) |
|---|---|
| "Stop using bullet lists for short status updates" | "Fix typo in line 3" |
| "When I say 'meeting note', use the template" | "Re-do this answer shorter" |
| "I write file names in lowercase-kebab, never CamelCase" | "Use British spelling here" (one piece of content) |
| "Don't write ADRs for one-line decisions" | "Move this paragraph above the next" |

Rule of thumb:
- **Lesson** = a rule that changes future behavior.
- **Correction** = a fix for now.

Only lessons go to history.md.

## Session start behavior (related, not an operation)

This isn't triggered — it's a passive read described here because
it's tied to history.md.

- On every new conversation start, agent reads `wiki/history.md`.
- Treats entries as standing instructions modifying default behavior.
- Older entries weigh less. Newer override older if they conflict.
- Agent does **not** announce "I read history.md" — apply silently.

If `wiki/history.md` is missing or empty, proceed without it.

## Edge cases

**"Remember this" with ambiguous referent.**
Ask: "What's the lesson — that I should X, or that I should Y?"

**Lesson contradicts an existing entry.**
Show the conflicting old entry. Ask: "This contradicts <old entry
from <date>>. Supersede it (mark old as outdated) or keep both?"
Default: supersede.

**Lesson is project-specific, not vault-wide.**
Suggest: "This sounds project-specific. Want it in
`projects/<X>/notes/` as a guideline, instead of global history?"

**20-entry limit hit, oldest entry is itself important.**
Still archive (it's preserved in `history-archive.md`). The cap
is on the live file only.

**User edits the proposed entry before confirming.**
Use the user's edited text verbatim. Don't second-guess.

## Post-checklist

- [ ] Did I read this spec at the start?
- [ ] Does the entry have all three fields filled?
- [ ] Did I check the 20-entry cap before appending?
- [ ] Is the entry actually appended, not overwriting?
- [ ] Did I show user the appended entry and current count?

## Files

**Reads:** `wiki/history.md`,
`.agent/references/history-entry-format.md`, optionally
`wiki/history-archive.md` (when archiving).

**Writes:** `wiki/history.md`, optionally `wiki/history-archive.md`.

Never logs to `wiki/log.md` — history is private agent memory,
not a public operation record.