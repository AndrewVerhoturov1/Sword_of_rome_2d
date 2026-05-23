# Архитектура

## Product Framing

Проект = не "цифровой Sword of Rome", а `browser-based 2D authoring tool / editor / tabletop sandbox` для counter-based варгеймов.

Sword of Rome-like модуль = первый тестовый `module package`, через который проверяется, что универсальные capabilities реально собирают сложную point-to-point, card-driven, counter-based игру.

Главный принцип остаётся тем же:

1. Сначала строим универсальные capabilities и архитектурные швы.
2. Потом через них собираем конкретный Sword of Rome-like test module.
3. Не даём test module превратить платформу в hardcoded "одну игру".

## Repo Layers Vs Product Layers

В repo уже есть три разных плоскости, и их нельзя смешивать:

- `Project context layer` — канон, референсы, workflow и решения в `canon/`, `references/`, `docs/`, `.ai/`.
- `Product architecture layer` — будущий product code для authoring/runtime platform.
- `Prototype layer` — локальные эксперименты в `arena-prototype-launcher/`, `_local/` и `output/Arena tests/`.

Ниже зафиксирована именно `product architecture layer`.

## 4-Layer Product Architecture

Для product code принята `4-layer` модель.

```text
Layer 4: Module Package
  - module content
  - module rules/hooks

Layer 3: Universal Runtime / Play Sandbox
  - GameState execution
  - action/event pipeline
  - play-mode shell

Layer 2: Universal Authoring / Editor Capabilities
  - map/piece/scenario/deck authoring
  - designer tools

Layer 1: Core Infrastructure + Project/Data Model
  - render/input/event/persistence core
  - schemas, ids, versioning, JSON formats
```

Эта модель синтезирует два внешних `/v1` second opinion:

- нужен явный `runtime/play` слой между editor и module-specific rules;
- нужен отдельный `project/data model`, чтобы editor не сохранял хаотичные структуры;
- нужен явный шов между universal runtime и module-specific rules.

## Layer Responsibilities

### Layer 1 — Core Infrastructure + Project/Data Model

Responsibility:

- дать технический фундамент платформы;
- зафиксировать единый язык данных для всех верхних слоёв;
- держать сериализуемое source of truth вне Phaser objects.

Входит:

- `RenderEngine` — Phaser/React integration, lifecycle, camera shell;
- `InputPipeline` — pointer input, drag/drop, select, pan/zoom, snap primitives;
- `EventBus` — внутренняя типизированная шина событий;
- `PersistenceModule` — import/export, validation, version markers;
- `Project/Data Schema` — `Project`, `ModuleManifest`, `MapDefinition`, `Space`, `Connection`, `PieceDefinition`, `ScenarioDefinition`, `SaveGame`;
- разделение `map.json`, `scenario.json`, `savegame.json`;
- ID policy, schema versioning, Zod validation.

Не входит:

- конкретные правила Sword of Rome-like;
- editor UI;
- play legality;
- конкретные ассеты модуля.

### Layer 2 — Universal Authoring / Editor Capabilities

Responsibility:

- создавать и редактировать reusable building blocks варгейма;
- собирать валидные project/module data поверх Layer 1.

Входит:

- map authoring;
- spaces authoring;
- connections authoring;
- piece/counter authoring;
- scenario authoring;
- deck/card authoring later;
- inspector panels;
- designer tools;
- developer map mode;
- authoring undo/redo.

Не входит:

- полная правилами ограниченная play-логика;
- конкретные victory conditions;
- hardcoded модульные знания.

### Layer 3 — Universal Runtime / Play Sandbox

Responsibility:

- запускать любой собранный module package как digital tabletop;
- исполнять универсальный цикл `Action -> Event -> GameState -> Render`;
- давать shell для будущего `Play Mode`, не вшивая rules конкретной игры.

Входит:

- `GameStateModule`;
- `RuntimeTable`;
- `ActionModule`;
- `Action/Event Log`;
- stack interaction;
- selection/context menu;
- Designer Mode shell;
- Play Mode shell;
- phase framework;
- future server-ready action signatures.

Не входит:

- конкретные movement restrictions конкретной игры;
- конкретные card effects;
- конкретные combat/scoring procedures.

### Layer 4 — Module Package

Responsibility:

- содержать конкретную игру/модуль, собранный поверх universal platform.

Внутри слоя две части:

- `Module Content` — карта, spaces, counters, factions, cards, scenarios, aids, texts, assets;
- `Module Rules/Hooks` — allowed actions, phases, restrictions, scoring, win checks, card effects, special procedures.

Sword of Rome-like модуль должен жить здесь, а не просачиваться в lower layers.

## Main Module Breakdown

### Universal Modules

1. `RenderEngine`
   Purpose: Phaser/React board shell.
   Owns: scene lifecycle, camera shell, render loop integration.

2. `InputPipeline`
   Purpose: pointer interaction primitives.
   Owns: drag/drop, select, multi-select, pan/zoom, snap primitives.

3. `EventBus`
   Purpose: typed internal communication between modules.
   Owns: internal event contracts.

4. `PersistenceModule`
   Purpose: save/load/import/export/validation/versioning.
   Owns: JSON IO, Zod validation, schema versions.

5. `ProjectDataSchema`
   Purpose: unified data language for project and module files.
   Owns: `ModuleManifest`, `MapDefinition`, `ScenarioDefinition`, `SaveGame`, IDs.

6. `AssetBoardModule`
   Purpose: board asset metadata and table layout.
   Owns: map image references, board bounds, coordinate system, off-map boxes.

7. `MapGraphModule`
   Purpose: point-to-point map model.
   Owns: spaces, coordinates, connection graph, labels, space kinds.

8. `PiecesStacksModule`
   Purpose: piece definitions, instances, locations, stack behavior.
   Owns: piece types, piece instances, stack grouping, selection relation to location.

9. `AuthoringToolsModule`
   Purpose: universal editor capabilities.
   Owns: map editor, piece editor, scenario editor, draft state, inspector state.

10. `RuntimeTableModule`
    Purpose: universal tabletop runtime shell.
    Owns: runtime board state, camera state, selected objects, transient UI state.

11. `ActionEventModule`
    Purpose: event-sourced spine for runtime.
    Owns: action requests, events, action log, replay/undo basis.

12. `DocumentsModule`
    Purpose: rules/pinned aids/reference windows.
    Owns: document registry, pinned state, local layout state.

13. `CardsDecksModule`
    Purpose: generic card/deck framework.
    Owns: card definitions, deck definitions, pile state.
    Status: later than Table Sandbox 0.1.

14. `OnlineRoomSyncModule`
    Purpose: future server-authoritative multiplayer layer.
    Owns: room/session contracts, player views, action request bridge.
    Status: later than Table Sandbox 0.1.

### Module-Specific Modules

15. `[ModuleName]Content`
    Purpose: concrete module data.
    Owns: map/scenario/piece/card/faction content, labels, texts, aids, assets.

16. `[ModuleName]Rules`
    Purpose: concrete module behavior.
    Owns: phases, legality, scoring, victory checks, card effects, special-case rules.

## Boundary Rules

### Phaser Is Not Source Of Truth

Истина живёт в `GameState`, JSON и событиях. Phaser objects только отображают состояние и прокидывают input в action/event pipeline.

### Content And Rules Stay Separate

Нельзя смешивать:

- `module content` как данные;
- `module rules` как поведение.

Иначе любой модуль быстро станет hardcoded branch платформы.

### Map / Scenario / Savegame Stay Separate

- `map.json` — постоянная структура карты и пространств;
- `scenario.json` — стартовая раскладка и стартовое состояние;
- `savegame.json` — конкретная партия.

### Designer Mode And Play Mode Stay Separate

`Designer Mode` = свободное authoring/manipulation пространство.
`Play Mode` = rules-ready runtime shell с ограничением действий через rule hooks later.

Нельзя размывать границу через хаотичные `if (isPlayMode)` в editor инструментах.

### Rules Hook Boundary Is Mandatory

Между Layer 3 и Layer 4 нужен явный интерфейс:

`RulesHooksInterface`

Минимальные responsibility points:

- `getAllowedActions(...)`
- `validateAction(...)`
- `getPhaseActions(...)`
- `onPhaseStart(...)`
- `checkWinCondition(...)`

Ниже интерфейса = universal platform.
Реализация интерфейса = module-specific behavior.

## Table Sandbox 0.1 Scope

В первый product milestone входят:

- `RenderEngine`
- `InputPipeline`
- `PersistenceModule`
- `ProjectDataSchema`
- `AssetBoardModule`
- `MapGraphModule`
- `PiecesStacksModule`
- `AuthoringToolsModule`
- `RuntimeTableModule`
- `ActionEventModule`
- `DocumentsModule` placeholder

Пока не входят:

- full `CardsDecksModule`
- full `[ModuleName]Rules`
- combat resolver
- full phase automation
- server-authoritative online
- AI

## Next Planning Steps

1. Зафиксировать glossary верхнеуровневых сущностей.
2. Описать `ModuleManifest` для любого module package.
3. Описать минимальные schemas для `map.json`, `scenario.json`, `savegame.json`.
4. Задокументировать `RulesHooksInterface` отдельным planning-артефактом.
5. Зафиксировать module-level scope для `Table Sandbox 0.1`.
6. После этого планировать первый product-code skeleton под слои и модули выше.

## Architectural Rules

- Не хардкодить проект как "одна игра"; держать фокус на reusable authoring tool.
- Не смешивать public context layer с local-only prototype layer.
- Не смешивать universal runtime с module-specific rules.
- Не смешивать module content с module behavior.
- Не выдавать planned architecture за уже реализованный product code.
