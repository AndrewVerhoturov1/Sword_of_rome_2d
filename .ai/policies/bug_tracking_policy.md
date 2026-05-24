# Bug Tracking Policy

## Main rule

Every implementation, QA, Kilo, or Codex report must include a section:

`Баги и сложности`

This section must explicitly say one of:

- `Багов и сложностей не обнаружено.`
- `Были проблемы, они исправлены.`
- `Есть нерешённые проблемы.`
- `Нужна проверка человеком.`

Agents must not silently ignore problems that appeared during work.

## What must be reported

Agents must report:

- build errors;
- typecheck errors;
- runtime errors;
- browser console errors if observed;
- visual/layout problems;
- Phaser/canvas visibility problems;
- click/drag/input problems;
- JSON/schema/reference problems;
- failed assumptions;
- confusing file locations;
- repeated mistakes;
- workaround used;
- anything that required more than one attempt to fix.

## Check the bug journal first

Before debugging a bug or investigating a repeated difficulty, inspect `.ai/logs/bug_journal.md` for similar symptoms.

This is especially important for:

- Phaser/React integration;
- layout and visibility issues;
- build/typecheck problems;
- fixture/JSON consistency;
- workflow/tooling misunderstandings.

## Bug journal

Important or repeatable problems must be recorded in:

`.ai/logs/bug_journal.md`

Use the bug journal when:

- the bug may happen again;
- the fix is not obvious;
- the same issue appeared more than once;
- a human had to verify the fix;
- the problem was caused by project workflow, tooling, Phaser/React integration, layout, JSON shape, or agent misunderstanding.

Do not fill the journal with tiny one-off typos unless they caused real confusion.

Human review alone does not automatically require a bug journal entry. Add or update the journal when the issue is important, repeated, non-obvious, workaround-driven, or useful for future debugging.

When adding a new entry, inspect existing IDs for the same date and use the next available `NNN`. Never renumber older entries.

## Required report format

Every task report must include:

```markdown
### Баги и сложности

Status: none / fixed / open / pending human check

Summary:
[простое описание]

Details:
[что произошло]

Fix:
[как исправлено, если исправлено]

Verification:
[чем проверено: exact commands, tests, browser/manual check, human confirmation, or explicit `not run / not verified`]

Journal:
[not needed / added BUG-YYYYMMDD-NNN / related to BUG-YYYYMMDD-NNN]
```

## Bug journal entry format

Use this format in `.ai/logs/bug_journal.md`:

```markdown
### BUG-YYYYMMDD-NNN — Short title

Status: open / fixed / workaround / pending human check

Area:
[например: table-sandbox, Phaser, layout, fixtures, JSON, docs, workflow]

Symptoms:
[что было видно простыми словами]

Cause:
[почему это произошло, если известно]

Fix:
[что помогло]

Verification:
[как проверили]

Human check:
[not needed / required / completed]

Related files:
- [список файлов]

Notes for future agents:
[коротко: что помнить, чтобы не повторить]
```

## Simple Russian requirement

Bug reports for the user must be written in simple Russian.

Bad:

`Renderer lifecycle regression due to stale container dimensions.`

Good:

`Phaser-поле не было видно, потому что блок для него получил неправильный размер.`

## Open bug rule

If a bug is not fixed, the agent must not mark the task as fully done.

It must write:

- what remains broken;
- how to reproduce it;
- what was already tried;
- what the next agent should check.

If a human check fails, treat that as a bug/difficulty result, not as a silent note. Mark the report as `open`, `fixed`, or `pending human check` by the real state, explain what failed, and update the journal when the issue is repeatable or useful for future debugging.

## Boundary with Human Check

`Human Check` says whether human validation is needed.

`Баги и сложности` says whether real problems or difficulties happened during the task.

These sections are related, but they are not the same thing.

## Human review connection

If the bug affects visible UI, browser behavior, click/drag, layout, or user-facing text, follow:

`.ai/policies/human_review_policy.md`

Mark the result as `pending human check` when human confirmation is still needed.
