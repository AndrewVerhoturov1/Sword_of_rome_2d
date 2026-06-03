# V3 Request Pack Skill Pilot Navigation

Slug: `v3_request_pack_skill_pilot`  
Owner: `Orc`  
Status: `draft / pending external run`  
Date: `2026-06-02`

## Назначение

Это карта документов подпроекта и связанных request artifacts.

## Current lifecycle stage

```text
Stage 5 pilot
```

Gate state:

```text
V3 request draft prepared; pending human send to external chat
```

## Active route

```text
Planner -> Orc
```

## Human-first route

1. `v3_request_pack_skill_pilot_readme.md`
2. `v3_request_pack_skill_pilot_navigation.md`
3. `v3_request_pack_skill_pilot_decisions.md`
4. `v3_request_pack_skill_pilot_journal.md`
5. `v3_request_pack_skill_pilot_plan_full.md`

## Orc route

1. `v3_request_pack_skill_pilot_navigation.md`
2. `v3_request_pack_skill_pilot_battle_plan.md`
3. `v3_request_pack_skill_pilot_plan_index.md`
4. `v3_request_pack_skill_pilot_plan_full.md`
5. `v3_request_pack_skill_pilot_decisions.md`
6. latest `v3_request_pack_skill_pilot_journal.md`

## Canonical subproject docs

- `v3_request_pack_skill_pilot_plan_full.md`
- `v3_request_pack_skill_pilot_battle_plan.md`
- `v3_request_pack_skill_pilot_readme.md`
- `v3_request_pack_skill_pilot_decisions.md`
- `v3_request_pack_skill_pilot_plan_index.md`
- `v3_request_pack_skill_pilot_journal.md`
- `v3_request_pack_skill_pilot_navigation.md`

## Linked V3 request artifacts

Эти файлы уже существуют, но не входят в canonical subproject docs list, потому что лежат в `.ai/v3/requests/`:

- `V3-20260602-114035-v3-request-pack-skill-draft_request.md`
- `V3-20260602-114035-v3-request-pack-skill-draft_prompt.md`
- `V3-20260602-114035-v3-request-pack-skill-draft_send_note.md`

## What exists already

| File | Purpose | Audience |
|---|---|---|
| `v3_request_pack_skill_pilot_plan_full.md` | стратегическая база | human + agents |
| `v3_request_pack_skill_pilot_battle_plan.md` | сжатый operational summary | human + agents |
| `v3_request_pack_skill_pilot_readme.md` | human-first вход | human |
| `v3_request_pack_skill_pilot_decisions.md` | долгоживущие решения | human + agents |
| `v3_request_pack_skill_pilot_plan_index.md` | retrieval map по `plan_full` | agents |
| `v3_request_pack_skill_pilot_journal.md` | factual log | human + agents |
| `v3_request_pack_skill_pilot_navigation.md` | эта карта | human + agents |

## What does not exist yet

| File or artifact | State | Notes |
|---|---|---|
| `v3_request_pack_skill_pilot_status.md` | `not created` | не входит в текущий набор |
| returned package | `not created` | внешний чат ещё не запускался |
| import artifacts | `not created` | import-stage не открыт |
| global skill files | `not created` | materialization требует отдельного human gate |
| scripts | `not created` | broad automation не открыта |
| repo-level docs | `not created` | repo-level promotion не открыт |

## Non-canonical / do not use as active source

- любые legacy route docs;
- любой draft, который пытается подменить accepted `plan_full`;
- любой package, который ещё не прошёл package-only review.

## Reading routes by need

| Need | Route |
|---|---|
| Понять подпроект как человек | `readme -> navigation -> decisions -> journal -> plan_full` |
| Продолжить работу как `Orc` | `navigation -> battle_plan -> plan_index -> plan_full -> decisions -> latest journal` |
| Отправить готовый V3 request | `navigation -> linked V3 request artifacts -> prompt -> external chat` |
| Проверить фактические действия | `journal` |

## Maintenance rule

- Не добавлять файл в canonical subproject docs, пока он реально не создан в подпроектной папке.
- Не объявлять `Stage 6` открытым.
- Не смешивать request, package, import и accepted result.
- Не возрождать legacy route.
