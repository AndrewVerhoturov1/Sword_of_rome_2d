# {Subproject Title} Status

Slug: `{subproject_slug}`  
Owner: `Orc`  
Status updated: `YYYY-MM-DD`  
Status kind: `live snapshot, not journal`

## Current lifecycle stage

```text
<stage name>
```

## Current owner role

```text
<Planner / Orc / Human / external draft pending local review>
```

## Current gate

```text
<gate name>: <open / closed / blocked / pending>
```

## Last completed action

```text
<last factual completed action>
```

Do not include long history. Put long history in journal.

## Current active document or route

```text
<active doc / active route / package / handoff>
```

## Next allowed step

```text
<one next allowed step>
```

Do not list future stages as already allowed.

## Blockers

- `<blocker 1>`
- `<blocker 2>`

If no blockers:

```text
none known
```

## Human action needed

Simple instructions for the human.

Example:

```text
Open readme/status/navigation. If the route is clear, say: `<approval phrase>`.
```

## Verification state

| Check | State |
|---|---|
| File existence | `<not run / passed / pending>` |
| Path scope | `<not run / passed / pending>` |
| Diff check | `<not run / passed / pending>` |
| Automated tests | `<not needed / not run / passed>` |
| Human check | `<pending / accepted / failed>` |

## Resume instruction

If context is lost:

1. Read this status.
2. Read the latest journal entry.
3. Read decisions.
4. Check whether human gate is closed.
5. Continue only from `Next allowed step`.
