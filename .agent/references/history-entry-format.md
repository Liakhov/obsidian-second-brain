# History entry format

Format for entries in `wiki/history.md`.

## Entry template

```
## [YYYY-MM-DD HH:MM] correction
- Context: <one line — what the agent was doing>
- Correction: <one or two lines — what the user fixed or asked differently>
- Lesson: <one line, imperative — what to do next time>
```

All three fields required. Don't write entries with empty fields.

## Examples

### Good

```
## [2026-05-27 14:23] correction
- Context: Was about to write a 200-word ADR for a one-line decision.
- Correction: User said ADRs are for non-trivial decisions only.
- Lesson: Don't write ADRs for one-line decisions; suggest inline note instead.
```

```
## [2026-06-01 09:15] correction
- Context: Suggested archiving a simple factual answer as a wiki page.
- Correction: User pointed out it was a lookup, not a synthesis.
- Lesson: Don't propose archive for definitional or status questions.
```

```
## [2026-06-10 18:40] correction
- Context: Created file `MyAppNotes.md` in PascalCase.
- Correction: User renamed to `my-app-notes.md` and asked to always use kebab-case.
- Lesson: All file names are lowercase kebab-case. No CamelCase, no PascalCase.
```

### Bad — don't write entries like these

```
## [2026-05-27 14:23] correction
- Context: Was writing.
- Correction: User changed it.
- Lesson: Do better.
```
(Fields are filler, not informative.)

```
## [2026-05-27 14:23] correction
- Context: Made a typo.
- Correction: User fixed typo.
- Lesson: Don't make typos.
```
(One-off, not a behavioral pattern.)

## Length guidance

- Whole entry: 4-7 lines.
- Each field: one or two short lines, never a paragraph.
- If the lesson needs more context, that's a sign it should be an
  ADR (in `wiki/meta/`), not a history entry.

## What makes a good lesson

The `Lesson` line should be:
- **Imperative.** "Don't X" or "Do Y when Z".
- **Specific.** Not "be careful" or "ask the user".
- **Generalizable.** Should apply to future similar situations,
  not just the one that triggered it.
- **Single-action.** One rule per entry. Don't bundle.

If you can't write a generalizable single-action imperative,
the situation probably isn't a lesson — it's just a correction
for the current task. Don't log it.
