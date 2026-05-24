# Project State

## Дата обновления

`2026-05-24`

## Текущий этап

`Table Sandbox 0.1: first move slice accepted baseline`

## Что уже принято

- Проектовый canon: это browser-based authoring tool / tabletop sandbox для 2D counter-based варгеймов.
- `Sword of Rome-like` модуль здесь = первый тестовый модуль, не весь продукт.
- Первый product-code путь уже прошёл через:
  - `0008` — technical bootstrap shell;
  - `0009` — canonical fixture seed;
  - `0010` — runtime/data bootstrap from fixtures;
  - `0011` — first narrow Action/Event move slice;
  - `0012` — permissive RulesHooks shim.

## Что уже работает в product code

- Отдельный `table-sandbox/` shell на `Vite + React + TypeScript + Phaser`.
- Authoritative `GameState` живёт вне Phaser.
- Tiny fixtures грузятся из `table-sandbox/src/fixtures/tiny-module/`.
- Runtime знает:
  - `tiny-project`
  - `tiny-module`
  - `tiny-map`
  - `basic`
  - 2 spaces
  - 1 connection
  - 1 piece instance
- Первый узкий move pipeline уже доказан:
  - `move_piece_requested`
  - `piece_moved`
  - reducer updates `GameState`
  - event log grows
  - renderer redraws piece from updated runtime state
- Rules boundary уже выделен:
  - runtime asks `validateAction`
  - runtime asks `resolveAction`
  - rules shim answers permissively
  - runtime commits returned events itself

## Что зафиксировано в workflow

- Repo-level policy layer добавлен:
  - language policy
  - human review policy
  - bug tracking policy
- Эти политики уже вшиты не только в repo docs, но и в Kilo process layer:
  - handoff creation
  - Kilo rules
  - report templates
  - review prompts

## Текущие ограничения

- Нет save/load slice.
- Нет broad rules engine.
- Нет drag/drop system.
- Нет authoring surfaces product-level breadth.
- Нет mature module package loading beyond tiny local fixture slice.

## Ближайший practical next step

Следующий шаг должен оставаться узким и идти поверх уже принятого move slice.

Рабочее направление:

- следующий runtime step после `0011`, без перепридумывания архитектуры;
- не возвращаться назад к bootstrap;
- не расползаться сразу в save/load, broad rules или editor breadth.

## Текущие риски

- Легко расползти следующий handoff в несколько систем сразу: runtime, rules, persistence и UI.
- Легко начать чинить “на будущее” вместо следующего узкого slice.
- Bundle warning от Phaser/Vite остаётся, но пока не blocker.
