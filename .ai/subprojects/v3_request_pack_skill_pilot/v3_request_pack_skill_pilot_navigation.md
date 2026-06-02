# V3 Request Pack Skill Pilot Navigation

Слаг: `v3_request_pack_skill_pilot`  
Владелец: `Orc`  
Статус: `draft / pending review`  
Дата обновления: `2026-06-02`

## Назначение

Этот файл — карта документов подпроекта.

Он показывает:

- какие документы уже существуют;
- какие документы сейчас canonical;
- что читать человеку;
- что читать `Orc`;
- чего пока нет;
- какие файлы не надо трактовать как active source.

## Current lifecycle stage

```text
Stage 5 pilot
```

Gate state:

```text
pending human review of battle plan
```

Stage warning:

```text
Do not claim next stage started unless human gate is closed.
```

## Active route

```text
Planner -> Orc
```

## Start here

### Human-first route

Человеку обычно читать так:

1. `v3_request_pack_skill_pilot_readme.md`
2. `v3_request_pack_skill_pilot_navigation.md`
3. `v3_request_pack_skill_pilot_decisions.md`
4. `v3_request_pack_skill_pilot_journal.md`
5. `v3_request_pack_skill_pilot_plan_full.md`

### Orc route

`Orc` обычно читать так:

1. `v3_request_pack_skill_pilot_navigation.md`
2. `v3_request_pack_skill_pilot_plan_index.md`
3. `v3_request_pack_skill_pilot_plan_full.md`
4. `v3_request_pack_skill_pilot_decisions.md`
5. latest `v3_request_pack_skill_pilot_journal.md`

## Canonical file list

Сейчас canonical документами подпроекта являются только реально существующие файлы:

- `v3_request_pack_skill_pilot_plan_full.md`
- `v3_request_pack_skill_pilot_battle_plan.md`
- `v3_request_pack_skill_pilot_readme.md`
- `v3_request_pack_skill_pilot_decisions.md`
- `v3_request_pack_skill_pilot_plan_index.md`
- `v3_request_pack_skill_pilot_journal.md`
- `v3_request_pack_skill_pilot_navigation.md`

## Existing documents

### Planner-owned documents

| File | Purpose | Audience |
|---|---|---|
| `v3_request_pack_skill_pilot_plan_full.md` | Стратегическая база пилота | human + agents |
| `v3_request_pack_skill_pilot_battle_plan.md` | Сжатый operational-конспект remaining path | human + agents |

### Orc-owned documents

| File | Purpose | Audience |
|---|---|---|
| `v3_request_pack_skill_pilot_readme.md` | Human-first вход | human-first |
| `v3_request_pack_skill_pilot_decisions.md` | Долгоживущие решения и границы | human + agents |
| `v3_request_pack_skill_pilot_plan_index.md` | Agent-oriented retrieval map по `plan_full` | agents |
| `v3_request_pack_skill_pilot_journal.md` | Фактический стартовый журнал | human + agents |
| `v3_request_pack_skill_pilot_navigation.md` | Карта документов подпроекта | human + agents |

## Planned or not created yet

Эти файлы и артефакты сейчас не созданы и не должны трактоваться как existing:

| File or artifact | State | Notes |
|---|---|---|
| `v3_request_pack_skill_pilot_status.md` | `not created` | не входит в current minimal set |
| skill files | `not created` | global skill materialization закрыт отдельным human gate |
| request files | `not created` | `V3 request` не готовится на этом шаге |
| proof artifacts | `not created` | proof не запущен |
| scripts | `not created` | automation пока не открыт, кроме возможного узкого helper по отдельному решению |
| repo-level docs | `not created` | repo-level promotion не открыт |

## Non-canonical / do not use as active source

- `v3_request_pack_skill_pilot_plan_full_draft.md` — draft, не использовать вместо accepted `plan_full`.
- Любые legacy route docs — не возвращать как active route.

## Reading routes by need

| Need | Route |
|---|---|
| Понять подпроект как человек | `readme -> navigation -> decisions -> journal -> plan_full` |
| Продолжить работу как `Orc` | `navigation -> battle_plan -> plan_index -> plan_full -> decisions -> latest journal` |
| Проверить стратегию | `plan_full -> plan_index` |
| Проверить фактический старт | `journal` |

## Maintenance rule

- Добавлять файл в canonical list только после его реального создания.
- Не записывать `battle_plan` или `status` как обязательные стартовые документы.
- Не объявлять `Stage 6` открытым.
- Не возрождать legacy route.
