# History

Append-only log of corrections from the user. The agent reads this
file at the start of every session and applies the lessons before
responding to the first request.

> Format and rules: `.agent/references/history-entry-format.md`.
> Operation spec: `.agent/operations/history-log.md`.
> Rationale: [[meta/0002-history-md-procedural-memory]].

Cap: latest 20 entries. When the cap is hit, the oldest entry
moves to `wiki/history-archive.md` automatically.

## Entries

*(empty — will be populated as the user corrects agent behavior)*
