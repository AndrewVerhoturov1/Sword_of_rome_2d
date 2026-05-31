# Ork Planner Navigation

Slug: `ork_planner`  
Last updated: 2026-05-31

## Start Here

1. `ork_planner_status.md` - где мы сейчас.
2. `ork_planner_plan_active_1.md` - текущий setup-план.
3. `ork_planner_plan_index.md` - быстрое оглавление полного плана.
4. `ork_planner_decisions.md` - важные решения.

## Core Documents

| File | Purpose | When to read |
|---|---|---|
| `ork_planner_readme.md` | Входная дверь подпроекта | В начале |
| `ork_planner_navigation.md` | Карта документов и контекста | При навигации |
| `ork_planner_plan_full.md` | Полный подробный план | Для глубокого понимания |
| `ork_planner_plan_index.md` | Оглавление полного плана | Для быстрого поиска |
| `ork_planner_plan_active_1.md` | Setup-план | Для текущего шага |
| `ork_planner_journal.md` | Журнал выполнения | Чтобы понять историю |
| `ork_planner_status.md` | Ближайшее состояние | После compaction |
| `ork_planner_decisions.md` | Принятые решения | При спорных вопросах |

## Active Plans

- `ork_planner_plan_active_1.md` - стартовый setup-план подпроекта.

## Required Repo Context

- `AGENTS.md` - repo-level workflow contract.
- `.ai/repo_navigation.md` - global navigation проекта.
- `.ai/project_state.md` - project-wide current state.
- `.ai/rules/codex_role_planner.md` - Planner role boundary for `Planner -> Orc`.
- `ideas/subproject_single_execution_chat_documentation_system_v2.md` - source of truth для active структуры подпроекта.

## V1 / V2 / V3 / Kilo Materials

| Type | ID / File | Purpose | Status |
|---|---|---|---|
| V1 | none yet | external second opinion при необходимости | not used |
| V2 | none | not needed for this setup | not used |
| V3 | `V3-20260531-091439-ork-planner-doc-critique` | external critique package for 8 core docs | imported |
| Kilo | none | not needed for this setup | not used |

## Review Materials

These files are critique artifacts only. They do not overwrite source docs and should be read before Orc starts if findings are still unresolved.

- `reviews/V3-ork_planner_readme.md`
- `reviews/V3-ork_planner_navigation.md`
- `reviews/V3-ork_planner_plan_full.md`
- `reviews/V3-ork_planner_plan_index.md`
- `reviews/V3-ork_planner_plan_active_1.md`
- `reviews/V3-ork_planner_journal.md`
- `reviews/V3-ork_planner_status.md`
- `reviews/V3-ork_planner_decisions.md`

## Deprecated / Do Not Use

- `Boss / B1 / Junior Orchestrator` как active route.
- любые block-style подпапки внутри `ork_planner`.
- `blocks/`
- `B1-*`
- `BOSS_*`
- `TASK_CONTROL_PACK*`
- `SUBPROJECT_STATE.md`
- `PLANNER_HANDOFF.md`
- `ORC_EXECUTION_LOG.md`
- `CHECKPOINTS.md`
- `CONTEXT_INDEX.md`

## Reading Routes

### Resume after context compaction

1. Read `ork_planner_status.md`.
2. Read `ork_planner_decisions.md`.
3. Open active plan from status.
4. If critique findings are unresolved, read `reviews/`.
5. Continue from resume instruction.

### Review this subproject after V3 critique import

1. Read `ork_planner_status.md`.
2. Read `ork_planner_decisions.md`.
3. Read imported `reviews/V3-*.md` files.
4. Decide whether to revise source docs before Orc.

### Understand the whole subproject

1. Read `ork_planner_readme.md`.
2. Read `ork_planner_plan_index.md`.
3. Open relevant anchors in `ork_planner_plan_full.md`.
4. Read `ork_planner_decisions.md`.

### Continue setup work

1. Read `ork_planner_status.md`.
2. Read `ork_planner_plan_active_1.md`.
3. Append result to `ork_planner_journal.md`.

## Navigation Maintenance Rule

Update this file when:

- a new active plan appears;
- a review package is imported;
- a new external response or Kilo report becomes part of subproject context;
- accepted decisions change;
- deprecated or forbidden files become relevant again.
