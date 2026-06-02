# Временный bridge для первого Stage 5 pilot

Слаг источника: `ork_planner`  
Назначение: дать новому planner-чату короткий вход в текущую систему документации перед стартом первого `Stage 5` pilot.

## Что это

Это временный bridge-документ.

Он нужен, потому что текущая система подпроектной документации уже собрана локально, но ещё не поднята как repo-level global canon.

Этот файл:

- показывает, где сейчас лежит рабочая правда;
- даёт короткий порядок чтения;
- объясняет, что не надо придумывать новую систему с нуля;
- не заменяет существующие документы `ork_planner`.

Этот файл не является:

- repo-level standard;
- полным планом;
- battle plan;
- разрешением пропускать human gates.

## Где сейчас лежит source of truth

Сначала читать документы `ork_planner`:

1. [ork_planner_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_readme.md)
2. [ork_planner_status.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_status.md)
3. [ork_planner_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_navigation.md)
4. [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md)
5. [ork_planner_battle_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_battle_plan.md)
6. [ork_planner_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_decisions.md)
7. [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
8. [subproject_templates_guide.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/templates/subproject_templates_guide.md)

## Как это читать

- `readme` = человеческий вход.
- `status` = самый короткий живой снимок.
- `navigation` = карта ссылок и путей.
- `plan_full` = полный канон и lifecycle.
- `battle_plan` = короткий operational-конспект оставшегося пути.
- `decisions` = важные долгоживущие решения.
- `journal` = фактическая история действий.
- `templates_guide` = как устроен reusable docs-set для новых подпроектов.

## Что важно помнить новому planner-чату

- Active route: `Planner -> Orc`.
- Не надо перепридумывать docs system с нуля.
- Не надо заранее расписывать весь execution path за Orc.
- Не надо подменять human approval.
- Из `journal` и planner-memory брать прежде всего универсальные process rules, а не всю локальную историю подряд.
- Если нужен новый подпроект, его надо проектировать поверх уже существующего template-layer.

## Что является текущей стартовой идеей пилота

Текущий pilot нужен не для ещё одного docs-only подпроекта сам по себе.

Стартовая идея такая:

- новый planner должен спланировать пилот, в котором будет создан skill для Codex;
- задача skill: помогать готовить `V3` request pack для внешнего чата;
- детали реализации заранее не даны намеренно;
- нужно проверить, как planner сам разложит задачу.

## Stop rule

Если после чтения документов всё ещё неясно:

- какой именно scope у пилота;
- какие файлы нужны для нового подпроекта;
- где заканчивается planning и начинается execution;

нужно остановиться и вернуть человеку короткий список вопросов, а не домысливать скрытые детали.
