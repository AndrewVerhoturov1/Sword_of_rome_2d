# Project State

## Дата обновления

`2026-05-25`

## Текущий этап

`Table Sandbox 0.1: Smart Drag Move accepted baseline`

## Что уже принято

- Проектовый canon: это browser-based authoring tool / tabletop sandbox для 2D counter-based варгеймов.
- `Sword of Rome-like` модуль здесь = первый тестовый модуль, не весь продукт.
- Первый product-code путь уже прошёл через:
  - `0008` — technical bootstrap shell;
  - `0009` — canonical fixture seed;
  - `0010` — runtime/data bootstrap from fixtures;
  - `0011` — first narrow Action/Event move slice;
  - `0012` — permissive RulesHooks shim;
  - direct graph-aware hardening for `move_piece_requested`;
  - `0014` — minimal runtime snapshot save/load;
  - `0015` — Manual Sandbox Action Pack 1;
  - `0016` — Manual Sandbox Interaction Pack 1 / Smart Drag Move.

## Что уже работает в product code

- Отдельный `table-sandbox/` shell на `Vite + React + TypeScript + Phaser`.
- Authoritative `GameState` живёт вне Phaser.
- Tiny fixtures грузятся из `table-sandbox/src/fixtures/tiny-module/`.
- Runtime знает:
  - `tiny-project`
  - `tiny-module`
  - `tiny-map`
  - `basic`
  - около 6 spaces
  - простой connected graph
  - multiple piece instances
- Первый узкий move pipeline уже доказан:
  - `move_piece_requested`
  - `piece_moved`
  - reducer updates `GameState`
  - event log grows
  - renderer redraws piece from updated runtime state
- Первый минимальный persistence loop уже доказан:
  - `Сохранить` пишет runtime snapshot в `localStorage`
  - `Загрузить` восстанавливает `GameState`
  - `Загрузить` восстанавливает `eventLog`
  - renderer redraw идёт из restored runtime state
- Первый ручной sandbox action pack уже доказан:
  - можно создать фишку через `create_piece_requested -> piece_created`
  - можно удалить фишку через `delete_piece_requested -> piece_deleted`
  - можно менять контроль точки через `change_control_requested -> control_changed`
  - selected object panel показывает выбранную точку/фишку
  - save/load переживает новые runtime-изменения, включая `controlState`
- Первый interaction-oriented move pack уже доказан:
  - existing piece можно тянуть левой кнопкой
  - во время drag виден source tail/line
  - ближайший target space подсвечивается
  - release идёт через existing `move_piece_requested -> piece_moved`
  - invalid drop не мутирует `GameState` и даёт понятное русское сообщение
  - save/load переживает committed drag move
- Rules boundary уже выделен:
  - runtime asks `validateAction`
  - runtime asks `resolveAction`
  - rules shim answers permissively
  - runtime commits returned events itself
- Move validation уже усилена:
  - проверка существования `pieceId`
  - проверка `fromLocationId`
  - проверка `toLocationId`
  - проверка bidirectional connection между space
- Runtime now also carries:
  - `controlState` for per-space ownership
  - human-readable Russian validation messages for sandbox actions
- Runtime/bootstrap now also honors:
  - fixture-driven initial `controlBySpace`

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

- Нет mature save system beyond one narrow local snapshot.
- Нет broad rules engine.
- Нет authoring surfaces product-level breadth.
- Нет mature module package loading beyond tiny local fixture slice.

## Ближайший practical next step

Следующий шаг пока не зафиксирован локально окончательно.

Рабочая рамка:

- идти поверх уже принятого move + rules + snapshot baseline;
- идти поверх уже принятого move + rules + snapshot + manual sandbox actions baseline;
- не возвращаться назад к bootstrap;
- не расползаться сразу в broad rules, save architecture или editor breadth;
- сначала взять grounded second opinion через `/v1` по следующему узкому шагу.

## Текущие риски

- Легко расползти следующий handoff в несколько систем сразу: runtime, rules, persistence и UI.
- Легко начать строить “большую систему сохранений”, хотя сейчас принят только один narrow `localStorage` snapshot.
- Легко начать чинить “на будущее” вместо следующего узкого slice.
- Bundle warning от Phaser/Vite остаётся, но пока не blocker.
