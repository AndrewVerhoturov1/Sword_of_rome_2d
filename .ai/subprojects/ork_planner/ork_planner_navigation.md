# Ork Planner Navigation

Slug: `ork_planner`  
Owner: `Orc`  
Status: `active-draft-pending-local-review`  
Last updated: `2026-06-02`

## Назначение

Карта подпроекта `ork_planner`.

Здесь держим:

- ссылки на существующие документы;
- пути к canonical-файлам;
- порядок чтения для человека и агента;
- текущий lifecycle stage;
- reusable template layer;
- non-canonical файлы, которые нельзя возвращать как active route.

Navigation не заменяет:

- `readme`;
- `status`;
- `journal`;
- `decisions`;
- `plan_full`;
- `battle_plan`.

## Current lifecycle stage

Stage:

```text
Stage 4 — local docs system + reusable templates
```

Gate state:

```text
Stage 4 files are laid out locally. Human review/acceptance still pending.
```

Boundary:

```text
Stage 5 has not started.
Stage 6 has not started.
```

## Active route

```text
Planner -> Orc
```

Legacy `Boss / B1 / Junior Orchestrator` не является active route.

## Start here

### Human-first route

1. [ork_planner_readme.md](ork_planner_readme.md)
2. [ork_planner_status.md](ork_planner_status.md)
3. [ork_planner_navigation.md](ork_planner_navigation.md)
4. [ork_planner_decisions.md](ork_planner_decisions.md)
5. [ork_planner_journal.md](ork_planner_journal.md)
6. [subproject_templates_guide.md](../templates/subproject_templates_guide.md)

### Agent route

1. [ork_planner_navigation.md](ork_planner_navigation.md)
2. [ork_planner_status.md](ork_planner_status.md)
3. [ork_planner_plan_index.md](ork_planner_plan_index.md)
4. [ork_planner_plan_full.md](ork_planner_plan_full.md)
5. [ork_planner_battle_plan.md](ork_planner_battle_plan.md)
6. [ork_planner_decisions.md](ork_planner_decisions.md)
7. latest entries in [ork_planner_journal.md](ork_planner_journal.md)

### Planner route

1. [ork_planner_plan_full.md](ork_planner_plan_full.md)
2. [ork_planner_plan_decisions.md](ork_planner_plan_decisions.md)
3. [ork_planner_planner_request_ideas.md](ork_planner_planner_request_ideas.md), if explicitly needed
4. [ork_planner_navigation.md](ork_planner_navigation.md)

## Existing documents

### Planner-owned documents

| Документ | Путь | Назначение |
|---|---|---|
| [ork_planner_plan_full.md](ork_planner_plan_full.md) | `.ai/subprojects/ork_planner/ork_planner_plan_full.md` | Canonical Planner-owned strategic base. |
| [ork_planner_plan_decisions.md](ork_planner_plan_decisions.md) | `.ai/subprojects/ork_planner/ork_planner_plan_decisions.md` | Planner-owned planning decision memory. |
| [ork_planner_planner_request_ideas.md](ork_planner_planner_request_ideas.md) | `.ai/subprojects/ork_planner/ork_planner_planner_request_ideas.md` | Support artifact only; not Orc evidence. |

### Orc-owned documents

| Документ | Путь | Назначение |
|---|---|---|
| [ork_planner_plan_index.md](ork_planner_plan_index.md) | `.ai/subprojects/ork_planner/ork_planner_plan_index.md` | Agent-oriented index for `plan_full`. |
| [ork_planner_navigation.md](ork_planner_navigation.md) | `.ai/subprojects/ork_planner/ork_planner_navigation.md` | This subproject map. |
| [ork_planner_journal.md](ork_planner_journal.md) | `.ai/subprojects/ork_planner/ork_planner_journal.md` | Factual execution log. |
| [ork_planner_battle_plan.md](ork_planner_battle_plan.md) | `.ai/subprojects/ork_planner/ork_planner_battle_plan.md` | Short operational summary of remaining Stage 4-6 route. |
| [ork_planner_readme.md](ork_planner_readme.md) | `.ai/subprojects/ork_planner/ork_planner_readme.md` | Human-first entry door. |
| [ork_planner_status.md](ork_planner_status.md) | `.ai/subprojects/ork_planner/ork_planner_status.md` | Short live state snapshot. |
| [ork_planner_decisions.md](ork_planner_decisions.md) | `.ai/subprojects/ork_planner/ork_planner_decisions.md` | Important subproject decisions and approvals. |

## Reusable template layer

Template root:

- [templates/](../templates/)
- path: `.ai/subprojects/templates/`

| Шаблон | Путь | Назначение |
|---|---|---|
| [subproject_plan_full_template.md](../templates/subproject_plan_full_template.md) | `.ai/subprojects/templates/subproject_plan_full_template.md` | Full Planner-owned plan for future subproject. |
| [subproject_plan_index_template.md](../templates/subproject_plan_index_template.md) | `.ai/subprojects/templates/subproject_plan_index_template.md` | Agent-oriented index for future `plan_full`. |
| [subproject_navigation_template.md](../templates/subproject_navigation_template.md) | `.ai/subprojects/templates/subproject_navigation_template.md` | Subproject-wide navigation map. |
| [subproject_journal_template.md](../templates/subproject_journal_template.md) | `.ai/subprojects/templates/subproject_journal_template.md` | Factual execution log template. |
| [subproject_battle_plan_template.md](../templates/subproject_battle_plan_template.md) | `.ai/subprojects/templates/subproject_battle_plan_template.md` | Short operational summary template for Orc. |
| [subproject_readme_template.md](../templates/subproject_readme_template.md) | `.ai/subprojects/templates/subproject_readme_template.md` | Human-first entry template. |
| [subproject_status_template.md](../templates/subproject_status_template.md) | `.ai/subprojects/templates/subproject_status_template.md` | Live status snapshot template. |
| [subproject_decisions_template.md](../templates/subproject_decisions_template.md) | `.ai/subprojects/templates/subproject_decisions_template.md` | Important decisions template. |
| [subproject_templates_guide.md](../templates/subproject_templates_guide.md) | `.ai/subprojects/templates/subproject_templates_guide.md` | Human/agent guide for whole template set. |

Template layer status:

```text
draft-pending-local-review-and-human-acceptance
```

Rule:

```text
Template layer is reusable for future subprojects and must not be overfitted to ork_planner.
```

## Planned future work not started

| Stage | Статус | Суть |
|---|---|---|
| `Stage 5` | `not started` | Fresh tiny docs-only pilot subproject from scratch. |
| `Stage 6` | `not started` | Repo-level alignment wave after accepted Stage 5. |

Fixed Stage 6 scope later:

- [.ai/rules/codex_role_planner.md](../../rules/codex_role_planner.md)
- [.ai/rules/codex_role_orc.md](../../rules/codex_role_orc.md)
- [.ai/rules/codex_orchestrator.md](../../rules/codex_orchestrator.md)
- [.ai/repo_navigation.md](../../repo_navigation.md)
- [AGENTS.md](../../../AGENTS.md)

## Non-canonical files

Do not use as active route:

| Файл/путь | Почему не canonical |
|---|---|
| `ork_planner_plan_navigation.md` | Replaced by [ork_planner_navigation.md](ork_planner_navigation.md). |
| `ork_planner_plan_active_1.md` | Old active-plan artifact; not current route. |
| `.ai/subprojects/ork_planner/reviews/` | Review layer only; not source of truth. |
| `Boss / B1 / Junior Orchestrator` | Legacy route; not active workflow. |

## Reading routes by need

| Need | Route |
|---|---|
| Understand current state | [ork_planner_readme.md](ork_planner_readme.md) -> [ork_planner_status.md](ork_planner_status.md) -> [ork_planner_navigation.md](ork_planner_navigation.md) |
| Continue execution safely | [ork_planner_status.md](ork_planner_status.md) -> [ork_planner_battle_plan.md](ork_planner_battle_plan.md) -> [ork_planner_decisions.md](ork_planner_decisions.md) -> latest [ork_planner_journal.md](ork_planner_journal.md) |
| Check role boundaries | [ork_planner_plan_full.md](ork_planner_plan_full.md) -> [ork_planner_plan_index.md](ork_planner_plan_index.md) -> [ork_planner_decisions.md](ork_planner_decisions.md) |
| Check important decisions | [ork_planner_decisions.md](ork_planner_decisions.md) -> [ork_planner_journal.md](ork_planner_journal.md) -> [ork_planner_plan_decisions.md](ork_planner_plan_decisions.md), if needed |
| Check factual history | [ork_planner_journal.md](ork_planner_journal.md) |
| Create future subproject docs | [subproject_templates_guide.md](../templates/subproject_templates_guide.md) -> relevant template files |
| Check whether Stage 5 can start | [ork_planner_status.md](ork_planner_status.md) -> [ork_planner_journal.md](ork_planner_journal.md) -> human approval evidence |

## Tool/external material references

Current Stage 4 route:

```text
external V3 draft package -> local manual layout -> local review -> human acceptance
```

Important distinction:

```text
This is not /v3 import-entry.
This is not Kilo Notebook V3.
This is not direct external package authority without local review.
```

## Maintenance rule

- Keep this file factual and link-first.
- Add file to existing-docs tables only after local file exists.
- Reflect draft/pending states honestly.
- Do not turn navigation into journal, status, or README.
- Do not mark Stage 5 or Stage 6 started before human gate closes.
- If file responsibility changes by human decision, update routes and tables here.
