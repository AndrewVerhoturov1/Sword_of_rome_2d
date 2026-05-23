# Minimal Canonical File Schemas

## Status

Planning artifact. First-pass schema contract for `Table Sandbox 0.1`.

## Purpose

Зафиксировать простую и практичную первую версию того, что должно лежать в
каждом canonical файле первого milestone.

Этот документ:

- не заменяет `domain_schemas_contract.md`;
- не задаёт TypeScript/Zod implementation;
- не открывает новую архитектуру;
- уточняет минимальный data contract для `Table Sandbox 0.1`.

## Core Rule

Нельзя смешивать роли файлов:

- `project.json` = индекс workspace;
- `module.json` = manifest модуля;
- `map.json` = карта и topology;
- `scenario.json` = стартовая раскладка;
- `rules.metadata.json` = declarative rules capabilities;
- `savegame.json` = текущее mutable состояние партии.

## First-Pass File Roles

### `project.json`

Должен хранить:

- `schemaVersion`
- `projectId`
- `name`
- `modules[]`
- `activeModuleId`

Не должен хранить:

- карту;
- стартовую раскладку;
- runtime state;
- event log;
- rules logic.

### `modules/<moduleId>/module.json`

Должен хранить:

- `schemaVersion`
- `moduleId`
- `name`
- `version`
- `engineCompatibility`
- `defaultMapId`
- `defaultScenarioId`
- `files`
- `rules`

Минимальный safe default для `0.1`:

- `files.map`
- `files.scenarios[]`
- `files.rulesMetadata`
- `rules.hookContractVersion`
- `rules.automationLevel`

Не должен хранить:

- current save state;
- event log;
- inline executable rules;
- full map graph;
- scenario instance state.

### `modules/<moduleId>/map.json`

Должен хранить:

- `schemaVersion`
- `mapId`
- `moduleId`
- `version`
- `name`
- `coordinateSystem`
- `spaces[]`
- `connections[]`
- `zones[]`

Не должен хранить:

- текущие позиции фишек;
- текущий control;
- phase state;
- event log;
- save state.

### `modules/<moduleId>/scenario.<scenarioId>.json`

Должен хранить:

- `schemaVersion`
- `scenarioId`
- `moduleId`
- `mapId`
- `name`
- `setup`

Минимальный `setup`:

- `turnState`
- `pieces[]`
- `controlBySpace`
- `variables`

Не должен хранить:

- post-start history;
- committed event sequence;
- save snapshots;
- full map graph;
- rules implementation.

### `modules/<moduleId>/rules.metadata.json`

Должен хранить:

- `schemaVersion`
- `rulesVersion`
- `hookContractVersion`
- `automationLevel`
- `supportedActionTypes[]`
- `supportedEventTypes[]`
- `phases[]`

Не должен хранить:

- executable rules code;
- actual hook functions;
- current `GameState`;
- event log;
- hidden mutable state.

### `saves/<saveId>.savegame.json`

Должен хранить:

- `schemaVersion`
- `saveId`
- `engineVersion`
- `moduleId`
- `moduleVersion`
- `mapId`
- `mapVersion`
- `scenarioId`
- `scenarioVersion`
- `gameState`
- `eventLog[]`

Не должен хранить:

- full `MapDefinition`;
- full `PieceDefinition[]`;
- module manifest copy;
- executable rules;
- renderer state как source of truth.

Stack note for `0.1`:

- save format stores `PieceInstance.locationId`, not a separate stack entity;
- stack is derived from grouping pieces by `locationId`;
- `stackId` and `stackPosition` stay out of the first save contract.

Compatibility note for `0.1`:

- structurally incompatible save files must be blocked;
- minor safe metadata mismatches may be warning-only;
- automatic migration is out of scope for `0.1`.

## Minimal File Dependency Order

```text
project.json
→ module.json
→ map.json + scenario.json + rules.metadata.json
→ initial GameState
→ Action/Event pipeline
→ savegame.json
```

## Minimal Integrity Rules

- `activeModuleId` должен существовать в `project.modules[]`.
- `module.defaultMapId` должен совпадать с `map.mapId`.
- `module.defaultScenarioId` должен существовать в `module.files.scenarios[]`.
- `scenario.mapId` должен ссылаться на существующий `mapId`.
- `connections[].fromSpaceId` и `toSpaceId` должны ссылаться на существующие spaces.
- `piece.locationId` должен ссылаться на существующий `spaceId` или `zoneId`.
- `savegame` не должен молча загружаться при несовместимых версиях module/map/scenario.
- `eventLog[].seq` должен быть монотонным.
- runtime state меняется только через committed events.

## Save Compatibility Policy For 0.1

Safe default:

- compatible save -> load normally;
- minor safe mismatch -> warn, then allow;
- structural incompatibility -> block load;
- migration-required case -> block load.

Block when:

- `schemaVersion` is incompatible;
- `moduleId`, `mapId`, or `scenarioId` is missing or unknown;
- required version references clearly mismatch without a compatibility rule;
- `pieceDefId` or `locationId` in saved state points to missing definitions;
- event log contains unknown event types that cannot be safely ignored.

Warning-only is acceptable when:

- only human-readable names or non-canonical metadata changed;
- optional fields are missing but have safe defaults;
- version metadata differs in a way that does not break required references.

## First Slice Constraint

Первый vertical slice должен работать с минимальным набором:

- `move_piece_requested`
- `piece_moved`

Смысл:

- доказать путь `Action -> validation -> resolveAction -> Event -> GameState -> log -> render`;
- не тащить раньше времени лишнюю сложность в schema layer.
- stack display for the slice can be derived from shared `locationId`; no canonical `Stack` entity is required.

## Safe Default For 0.1

Самое спорное место первого прохода:

- где держать `FactionDefinition`;
- где держать `PieceDefinition`.

Safe default:

- для `Table Sandbox 0.1` можно временно держать маленькие `factions[]` и
  `pieceDefinitions[]` прямо в `module.json`;
- это temporary compact layout;
- это не final canonical direction;
- позже их лучше вынести в отдельные files вроде `factions.json` и `pieces.json`.

Extraction trigger:

- if `module.json` stops reading like a manifest and starts reading like a content dump,
  definitions should move out;
- if piece/faction counts grow meaningfully, or dedicated editor surfaces appear,
  move to separate files.

## Later Extension

После `0.1` можно выносить отдельно:

- `pieces.json`
- `factions.json`
- `cards.json`
- `documents.json`
- `assets.json`

Также позже можно добавлять:

- content hashes;
- migration policy;
- visibility model;
- response windows;
- advanced stack model;
- full action history besides event log.

## Still Open

Пока не закрыто:

- точная save compatibility policy;
- точная stack model;
- нужен ли отдельный `rulesEntry` уже в early runtime;
- нужен ли action history помимо event log.

Open items here mean later expansion, not a blocker for `0.1`. For `0.1`,
stack is derived from `locationId`, while `FactionDefinition` and
`PieceDefinition` stay in the temporary compact `module.json` layout if needed.

## Relation To Mature Package Model

This file is the compact `0.1` schema contract.

The mature target shape of `module package` lives in
`module_package_model.md`.

Rule of use:

- use this file for first-pass compact layout;
- use `module_package_model.md` for later package splitting and richer content
  zones;
- do not treat compact `0.1` layout as final package shape.
