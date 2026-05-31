# Ork Planner Readme

Slug: `ork_planner`  
Status: planning  
Owner model: `Planner -> Orc`

## Purpose

Подпроект нужен для аккуратного старта новой planning/documentation сущности в active workflow проекта.

## Main Goal

Подготовить минимальный active documentation set для `ork_planner`, не переходя к исполнению задач внутри подпроекта.

## Execution Model

- Planning Chat отдельно.
- Execution Chat один и появится позже.
- Субагенты не используются как основной механизм.
- V1/V2/V3/Kilo вызываются только как внешние инструменты при необходимости.
- Документация является внешней памятью будущего execution chat.

## Scope

Что входит в подпроект сейчас:

- создать папку подпроекта;
- создать 8 стартовых документов;
- зафиксировать active route `Planner -> Orc`;
- зафиксировать stop-point после bootstrap.

## Out of Scope

Что не входит:

- запуск Orc-mode;
- product-work;
- legacy B1/BOS иерархия;
- изменение global workflow docs.

## Main Documents

- `ork_planner_navigation.md` — карта подпроекта.
- `ork_planner_plan_full.md` — полный подробный план.
- `ork_planner_plan_index.md` — оглавление полного плана.
- `ork_planner_plan_active_1.md` — текущий setup-план.
- `ork_planner_journal.md` — журнал выполнения.
- `ork_planner_status.md` — ближайшее состояние.
- `ork_planner_decisions.md` — принятые решения.

## Current Status

Смотри `ork_planner_status.md`.
