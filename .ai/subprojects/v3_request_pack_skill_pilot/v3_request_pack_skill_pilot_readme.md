# V3 Request Pack Skill Pilot Readme

Slug: `v3_request_pack_skill_pilot`  
Owner: `Orc`  
Audience: human first  
Status: `draft`  
Lifecycle stage: `Stage 5 pilot`  
Active route: `Planner -> Orc`

## Что это

`v3_request_pack_skill_pilot` — это docs-only подпроект для первого `Stage 5` pilot по теме `V3 request pack` preparation skill.

Этот подпроект не запускает skill execution и не открывает следующий stage. Он держит локальный набор документов, чтобы зафиксировать границы пилота, точки human gate и безопасный стартовый контекст для дальнейшей работы.

## Зачем он существует

Подпроект нужен, чтобы не смешивать:

- планирование пилота;
- materialization skill;
- подготовку `V3 request`;
- получение внешнего package;
- import;
- accepted result.

Практическая цель простая: сначала держать пилот как понятный docs-only слой, а не разворачивать раньше времени skill files, proof artifacts, scripts или repo-level promotion.

## Текущий статус простыми словами

Сейчас мы на этапе `Stage 5 pilot`. Уже есть принятый стратегический `plan_full` и создан минимальный стартовый docs set для маршрута `Planner -> Orc`.

Уже принято для этого подпроекта:

- active route `Planner -> Orc`;
- подпроект остаётся docs-only;
- `request != package != import != accepted result`;
- `Stage 6` не открыт;
- repo-level promotion не открыт;
- global skill materialization не разрешён без отдельного human gate;
- automation допустим только как узкий `request-pack preflight helper` по отдельному human decision;
- human approval ничем не подменяется.

Ещё не начато:

- `status`;
- skill execution;
- подготовка `V3 request`;
- proof run;
- import;
- открытие `Stage 6`;
- repo-level promotion.

## Что читать сначала

| Ситуация | Читать |
|---|---|
| Хочу быстро понять подпроект | этот `readme`, потом `v3_request_pack_skill_pilot_navigation.md` |
| Хочу увидеть принятые границы | `v3_request_pack_skill_pilot_decisions.md` |
| Хочу увидеть фактический стартовый шаг | `v3_request_pack_skill_pilot_journal.md` |
| Хочу проверить стратегическую базу | `v3_request_pack_skill_pilot_plan_full.md` |
| Я агент и хочу быстро найти нужный блок в плане | `v3_request_pack_skill_pilot_plan_index.md` |

## Какие документы уже существуют

Сейчас в canonical стартовый набор входят:

- `v3_request_pack_skill_pilot_plan_full.md` — стратегическая база подпроекта.
- `v3_request_pack_skill_pilot_battle_plan.md` — сжатый operational-конспект remaining path в текущих границах.
- `v3_request_pack_skill_pilot_readme.md` — human-first вход.
- `v3_request_pack_skill_pilot_decisions.md` — долгоживущие решения и границы.
- `v3_request_pack_skill_pilot_plan_index.md` — agent-oriented retrieval map по `plan_full`.
- `v3_request_pack_skill_pilot_journal.md` — фактический журнал стартовых действий.
- `v3_request_pack_skill_pilot_navigation.md` — карта документов подпроекта.

## Чего ещё пока нет

Сейчас специально не созданы:

- `v3_request_pack_skill_pilot_status.md`;
- skill files;
- request files;
- proof artifacts;
- handoff files;
- scripts;
- новые repo-level docs.

## Current safe next step

Безопасный следующий шаг: человеку открыть `battle_plan`, `navigation`, `decisions` и подтвердить, что battle plan остаётся внутри docs-only границ и не открывает proof, import или `Stage 6`.

## Role warning

- `Planner` владеет стратегией.
- `Orc` ведёт execution evidence и operational docs.
- Human закрывает gates.
- Agent recommendation не равен human approval.

## Non-canonical files

- `v3_request_pack_skill_pilot_plan_full_draft.md` — draft-слой, не использовать как active source вместо accepted `plan_full`.

## Human check

1. Откройте [v3_request_pack_skill_pilot_battle_plan.md](D:\Codex+Kilocode\projects\sword-of-rome-web\.ai\subprojects\v3_request_pack_skill_pilot\v3_request_pack_skill_pilot_battle_plan.md).
2. Проверьте, что там нет запуска skill, proof, import, `V3 request` или `Stage 6`, а следующий шаг — только ваш verdict.
3. Если всё верно, ответьте: `battle_plan принят`.
4. Если что-то не так, напишите простыми словами, какой блок нужно исправить.
