# {Subproject Title} Readme

Slug: `{subproject_slug}`  
Owner: `Orc`  
Audience: human first  
Status: `draft`  
Lifecycle stage: `<stage>`  
Active route: `Planner -> Orc`

## Что это

Коротко объяснить человеку, что это за подпроект.

Форма:

```text
{subproject_slug} — это подпроект для <цель>.
```

## Зачем он существует

Объяснить практическую пользу:

- какую проблему решает;
- почему это отдельный subproject;
- чем поможет человеку и агентам.

## Текущий статус простыми словами

Написать без jargon:

```text
Сейчас мы на этапе <stage>. Уже сделано <...>. Ещё не принято <...>. Следующий безопасный шаг <...>.
```

Не объявлять acceptance, если человек его не дал.

## Что читать сначала

| Ситуация | Читать |
|---|---|
| Я человек и хочу понять статус | этот readme, потом `{subproject_slug}_status.md` |
| Я агент и продолжаю работу | `{subproject_slug}_navigation.md` |
| Нужно понять большой план | `{subproject_slug}_plan_full.md` |
| Нужно найти anchors | `{subproject_slug}_plan_index.md` |
| Нужно увидеть execution history | `{subproject_slug}_journal.md` |
| Нужно увидеть важные решения подпроекта | `{subproject_slug}_decisions.md` |

## Какие документы уже существуют

List only files that exist.

- `{subproject_slug}_plan_full.md` — Planner-owned full plan.
- `{subproject_slug}_plan_index.md` — agent-oriented index.
- `{subproject_slug}_navigation.md` — map.
- `{subproject_slug}_journal.md` — factual log.
- `{subproject_slug}_battle_plan.md` — сжатый исполнительный конспект оставшихся шагов из `plan_full`.
- `{subproject_slug}_readme.md` — this human entry.
- `{subproject_slug}_status.md` — live snapshot.
- `{subproject_slug}_decisions.md` — Orc execution decisions.

## Чего ещё нет

List missing/pending items:

- no human acceptance yet;
- no next stage started;
- no repo-level alignment;
- no tests run;
- no Kilo run, if true.

## Current safe next step

Write one safe next step.

```text
<open file / review / approve / request fixes / run local import / stop>
```

Do not list future stages as already allowed.

## Role warning

- `Planner` owns strategy.
- `Orc` owns execution evidence.
- Human approves gates.
- Agent recommendation is not human approval.
- Do not mix role boundaries.

## Non-canonical files

List files that should not be used as active source:

- old drafts;
- old `plan_active_*`;
- deprecated navigation;
- legacy route docs.

## Human check

1. Open `<file>`.
2. Confirm `<what should be visible>`.
3. If correct, say `<approval phrase>`.
4. If not correct, say what needs fixing.
