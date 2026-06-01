# Ork Planner Readme

Slug: `ork_planner`  
Owner: `Orc`  
Audience: human first  
Status: `draft-pending-local-review`  
Lifecycle stage: `Stage 4 — Remaining local docs system`  
Active route: `Planner -> Orc`

## Что это

`ork_planner` — локальный pilot-подпроект для проверки workflow `Planner -> Orc`.

Он нужен, чтобы доказать, что большой план, навигация, журнал, статус, decisions, battle plan и reusable templates помогают продолжать работу без потери контекста и без смешивания ролей.

## Зачем он существует

Практический смысл:

1. `Planner` создаёт и держит стратегический `plan_full`.
2. Человек принимает gates.
3. `Orc` исполняет принятый план, выбирает route, ведёт live evidence и не переписывает стратегию без разрешения.
4. Документы отвечают человеку и агентам: что сделано, что pending, какой следующий безопасный шаг.

## Текущий статус простыми словами

Сейчас идёт `Stage 4`.

Эта Stage 4 docs slice подготовлена как внешний `V3` artifact package. Это ещё не local import, не Kilo Notebook V3 и не human acceptance. Нельзя считать Stage 4 принятой, пока человек явно это не подтвердит.

## Что читать сначала

| Ситуация | Читать |
|---|---|
| Человеку понять состояние | этот `ork_planner_readme.md`, потом `ork_planner_status.md` |
| Агенту продолжить работу | `ork_planner_navigation.md`, потом `ork_planner_status.md` |
| Агенту читать большой план | `ork_planner_plan_index.md`, потом `ork_planner_plan_full.md` |
| Понять execution history | `ork_planner_journal.md` |
| Понять Orc execution decisions | `ork_planner_decisions.md` |
| Понять Planner decisions | `ork_planner_plan_decisions.md` |
| Использовать шаблоны | `.ai/subprojects/templates/subproject_templates_guide.md` |

## Какие документы уже существуют после импорта Stage 4

Planner-owned:

- `ork_planner_plan_full.md` — canonical strategy.
- `ork_planner_plan_decisions.md` — Planner decision memory.
- `ork_planner_planner_request_ideas.md` — Planner support artifact, если есть в repo.

Orc-owned:

- `ork_planner_plan_index.md` — agent-oriented index; не human README.
- `ork_planner_navigation.md` — общая карта подпроекта.
- `ork_planner_journal.md` — factual execution log.
- `ork_planner_battle_plan.md` — сжатый исполнительный конспект оставшихся шагов из `ork_planner_plan_full.md`.
- `ork_planner_readme.md` — этот human-first вход.
- `ork_planner_status.md` — live snapshot.
- `ork_planner_decisions.md` — Orc-owned execution decisions.

Reusable template layer:

- `.ai/subprojects/templates/subproject_plan_full_template.md`
- `.ai/subprojects/templates/subproject_plan_index_template.md`
- `.ai/subprojects/templates/subproject_navigation_template.md`
- `.ai/subprojects/templates/subproject_journal_template.md`
- `.ai/subprojects/templates/subproject_battle_plan_template.md`
- `.ai/subprojects/templates/subproject_readme_template.md`
- `.ai/subprojects/templates/subproject_status_template.md`
- `.ai/subprojects/templates/subproject_decisions_template.md`
- `.ai/subprojects/templates/subproject_templates_guide.md`

## Чего ещё нет

- Нет human acceptance для Stage 4 docs.
- Нет нового tiny docs-only подпроекта для `Stage 5`.
- Нет repo-level alignment wave для `Stage 6`.
- Нет права считать legacy `Boss / B1 / Junior Orchestrator` active route.
- Нет разрешения переписывать `ork_planner_plan_full.md`, `ork_planner_battle_plan.md` или `ork_planner_plan_index.md` в этом package.

## Current safe next step

```text
Локально проверить/import package только по allowed paths.
Потом человек читает readme/status/navigation/journal/decisions/templates guide и решает: Stage 4 accepted или нужны правки.
```

Нельзя начинать `Stage 5`, пока человек не примет Stage 4.

## Role warning

- `Planner` отвечает за strategy and `plan_full`.
- `Orc` отвечает за execution route, journal, status, decisions, navigation и evidence.
- Агент может рекомендовать route, но не утверждает спорный route за человека.
- Human approval нельзя подменять словами агента.
- Legacy `Boss / B1 / Junior Orchestrator` — history only, не active route.

## Non-canonical files

Не использовать как active docs:

- `ork_planner_plan_navigation.md`
- `ork_planner_plan_active_1.md`
- `.ai/subprojects/ork_planner/reviews/`
- старые drafts/scaffolds без explicit human decision

## Human check

1. Открой `ork_planner_status.md`.
2. Убедись, что Stage 4 acceptance = `pending`.
3. Открой `ork_planner_navigation.md`.
4. Убедись, что `readme` = human-first, а `plan_index` = agent-oriented.
5. Открой `.ai/subprojects/templates/subproject_templates_guide.md`.
6. Проверь, понятно ли, как пользоваться шаблонами.
7. Верни одно из двух:
   - `Stage 4 local docs accepted`
   - `Stage 4 needs fixes: ...`
