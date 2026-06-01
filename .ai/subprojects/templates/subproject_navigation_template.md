# {Subproject Title} Navigation

Слаг: `{subproject_slug}`  
Владелец: `Orc`  
Статус: `draft / active / pending review`  
Дата обновления: `YYYY-MM-DD`

## Назначение

Этот файл — карта подпроекта.

Он показывает:

- какие документы существуют;
- где они лежат;
- что читать человеку;
- что читать агенту;
- какие файлы являются canonical;
- какие файлы deprecated/non-canonical;
- какой lifecycle stage сейчас активен.

Navigation не должен становиться:

- human README;
- journal;
- status;
- decisions;
- full plan;
- battle plan;
- rewrite стратегии.

## Current lifecycle stage

```text
<Stage name>
```

Gate state:

```text
<pending / accepted / blocked / needs human decision>
```

Stage warning:

```text
Do not claim next stage started unless human gate is closed.
```

## Active route

```text
Planner -> Orc
```

Если подпроект использует другой route, он должен быть явно утверждён человеком и отражён в decisions/status.

## Start here

### Human-first route

Человеку обычно читать так:

1. `{subproject_slug}_readme.md`
2. `{subproject_slug}_status.md`
3. `{subproject_slug}_navigation.md`
4. `{subproject_slug}_decisions.md`, если нужно понять принятые решения
5. `{subproject_slug}_journal.md`, если нужно понять историю действий
6. `{subproject_slug}_plan_full.md`, если нужно проверить стратегию

### Agent route

Агенту обычно читать так:

1. `{subproject_slug}_navigation.md`
2. `{subproject_slug}_status.md`
3. `{subproject_slug}_plan_index.md`
4. `{subproject_slug}_plan_full.md`
5. `{subproject_slug}_battle_plan.md`
6. `{subproject_slug}_decisions.md`
7. последние записи `{subproject_slug}_journal.md`

### Planner route

Planner читает:

1. `{subproject_slug}_plan_full.md`
2. `{subproject_slug}_plan_decisions.md`, если есть
3. source docs / repo rules
4. review feedback от человека

Planner не должен вести journal как будто он Orc.

## Existing documents

### Planner-owned documents

| File | Purpose | Audience |
|---|---|---|
| `{subproject_slug}_plan_full.md` | Большая strategy/lifecycle база | human + agents |
| `{subproject_slug}_plan_decisions.md` | Planner-owned decisions, если используется | Planner + reviewers |

### Orc-owned documents

| File | Purpose | Audience |
|---|---|---|
| `{subproject_slug}_plan_index.md` | Agent-oriented index по большому плану | agents |
| `{subproject_slug}_navigation.md` | Карта подпроекта | human + agents |
| `{subproject_slug}_journal.md` | Фактический журнал действий | human + agents |
| `{subproject_slug}_battle_plan.md` | Сжатый исполнительный конспект оставшихся шагов из `plan_full` | human + Orc |
| `{subproject_slug}_readme.md` | Human-first вход | human-first |
| `{subproject_slug}_status.md` | Самый свежий live snapshot | human + agents |
| `{subproject_slug}_decisions.md` | Важные решения подпроекта | human + agents |

## Planned documents not created yet

Не записывать planned files как existing.

| File | Planned stage | Notes |
|---|---|---|
| `<path>` | `<stage>` | `<why not created yet>` |

## Reusable template layer

Если подпроект использует общий template layer, перечислить его здесь.

Template path:

```text
.ai/subprojects/templates/
```

Templates:

- `subproject_plan_full_template.md`
- `subproject_plan_index_template.md`
- `subproject_navigation_template.md`
- `subproject_journal_template.md`
- `subproject_battle_plan_template.md`
- `subproject_readme_template.md`
- `subproject_status_template.md`
- `subproject_decisions_template.md`
- `subproject_templates_guide.md`

Rule:

```text
Templates are reusable. Do not overfit them to one subproject.
```

## Non-canonical / deprecated files

List files that should not be used as active source.

Examples:

- `{subproject_slug}_plan_active_1.md`
- `{subproject_slug}_plan_navigation.md`
- old drafts
- rejected imports
- legacy route docs

For each non-canonical file, explain:

```text
why not canonical / what replaced it / safe action
```

## Reading routes by need

| Need | Route |
|---|---|
| Понять подпроект как человек | `readme` -> `status` -> `navigation` |
| Продолжить выполнение | `status` -> `battle_plan` -> `decisions` -> latest `journal` |
| Проверить стратегию | `plan_full` -> `plan_index` -> `plan_decisions` |
| Проверить решения | `decisions` + отдельно `plan_decisions` |
| Проверить историю действий | `journal` |
| Проверить reusable templates | `subproject_templates_guide.md` -> individual templates |

## Maintenance rule

- Обновлять lifecycle stage только по факту.
- Добавлять файл в existing documents только после его создания.
- Не объявлять human acceptance без explicit verdict.
- Не превращать navigation в readme или journal.
- Не удалять non-canonical warnings без причины.
- Если route или gate изменился, обновить также `status` и при необходимости `decisions`.
