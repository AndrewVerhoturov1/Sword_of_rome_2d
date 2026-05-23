# Domain Schemas Contract

## Status

Planning artifact. Local working contract for next architecture step.

## Purpose

Зафиксировать human-readable data contract для платформы:

- что считается definition;
- что считается runtime state;
- какие файлы нужны;
- какие сущности считаются canonical;
- какие invariants нельзя нарушать.

Этот документ не заменяет будущие Zod schemas. Он подготавливает их.

## Product Reading

Проект = platform:

- authoring tool;
- runtime sandbox;
- module package system.

Sword of Rome-like модуль = первый test module, не source of truth для universal schema.

## Canonical Split

### Definition Layer

Почти неизменяемые описания:

- `ModuleManifest`
- `MapDefinition`
- `SpaceDefinition`
- `ConnectionDefinition`
- `ZoneDefinition`
- `FactionDefinition`
- `PieceDefinition`
- `ScenarioDefinition`
- `DocumentDefinition`
- later `CardDefinition`

### Runtime Layer

Меняющееся состояние:

- `PieceInstance`
- `ScenarioState`
- `GameState`
- `SaveGameState`
- `TurnState`
- `PhaseState`
- `Action`
- `Event`

### Rules Layer

Module-specific behavior:

- `RulesMetadata`
- `RulesHooksInterface` implementation

Rules layer не владеет canonical state storage. Он отвечает на вопросы runtime.

## Canonical File Set

### `project.json`

Purpose:

- root workspace index.

Stores:

- `projectId`
- `name`
- `schemaVersion`
- `modules[]`
- optional `activeModuleId`
- optional editor-level metadata

Does not store:

- full map graph
- scenario setup
- runtime save state
- executable rules

Owner:

- `Core Infrastructure + Project/Data Model`

### `modules/<moduleId>/module.json`

Purpose:

- module entry manifest.

Stores:

- `moduleId`
- `name`
- `version`
- `engineCompatibility`
- `schemaVersions`
- file pointers to content
- rules metadata pointer
- rules entry pointer
- default scenario/map

Does not store:

- full runtime save state
- action log
- full executable rules code inline

Owner:

- `Module Package`

First-pass note for `Table Sandbox 0.1`:

- if keeping separate `pieces.json` / `factions.json` is too heavy for the first
  thin slice, a small temporary compact layout inside `module.json` is acceptable;
- this is a short-term milestone simplification, not long-term canonical target.

### `modules/<moduleId>/map.json`

Purpose:

- stable board and graph definition.

Stores:

- `mapId`
- `version`
- board asset reference
- spaces
- connections
- off-map boxes/zones
- visual metadata

Does not store:

- current piece positions
- current control
- current phase
- event log

Owner:

- module content, validated by universal schema

### `modules/<moduleId>/scenario.<scenarioId>.json`

Purpose:

- initial setup template over chosen map.

Stores:

- `scenarioId`
- `moduleId`
- `mapId`
- initial `PieceInstance[]`
- starting control/state
- starting turn/phase
- scenario variables

Does not store:

- post-start history
- full play log
- mutable save snapshots across turns

Owner:

- module content + authoring layer

### `modules/<moduleId>/rules.metadata.json`

Purpose:

- declarative rules metadata for runtime/editor integration.

Stores:

- `rulesVersion`
- `hookContractVersion`
- phase ids
- supported action kinds
- automation profile
- visibility capabilities

Does not store:

- executable rules logic
- authoritative runtime state

Owner:

- module rules layer

### `saves/<saveId>.savegame.json`

Purpose:

- concrete play session snapshot.

Stores:

- `saveId`
- referenced module/scenario/map versions
- `GameState`
- event log
- current turn/phase
- mutable piece/control/variable state
- optional RNG state

Does not store:

- canonical map graph definition
- piece definitions
- executable rules

Owner:

- runtime + persistence layer

## Core Entity Glossary

### `ModuleManifest`

Entry point модуля. Говорит runtime, где брать map/scenario/rules/documents/assets.

### `MapDefinition`

Статическая топология поля. Это board geometry и graph, не текущее состояние партии.

### `SpaceDefinition`

Одна именованная точка на карте.

### `ConnectionDefinition`

Связь между двумя spaces.

### `PieceDefinition`

Шаблон фишки. Что это за тип, как выглядит, к какой faction относится по умолчанию.

### `PieceInstance`

Конкретная фишка в сценарии или сейве. Где стоит, в каком status, с какими mutable flags.

### `ScenarioDefinition`

Шаблон старта. Как разложить initial state поверх map.

### `ScenarioState`

Initial mutable state, с которого стартует партия.

### `GameState`

Authoritative runtime truth. То, что реально сейчас существует в партии.

### `SaveGameState`

Serialized snapshot текущей партии.

### `Action`

Намерение или запрос: "хочу сделать X".

### `Event`

Зафиксированный факт: "X произошло".

## Definition Vs Runtime State

### Immutable-ish

- `ModuleManifest`
- `MapDefinition`
- `SpaceDefinition`
- `ConnectionDefinition`
- `FactionDefinition`
- `PieceDefinition`
- `ScenarioDefinition`
- `RulesMetadata`

### Mutable

- `PieceInstance.locationId`
- `PieceInstance.status`
- `GameState`
- `TurnState`
- `PhaseState`
- `controlBySpace`
- `markers`
- `eventLog`
- `SaveGameState`

## ID And Reference Rules

### ID policy

Каждая сущность имеет stable id.

Recommended shape:

- `module:<id>`
- `map:<id>`
- `space:<id>`
- `connection:<id>`
- `pieceDef:<id>`
- `piece:<id>`
- `scenario:<id>`
- `save:<id>`

### Reference integrity

Mandatory:

- connection references existing spaces;
- piece instance references existing piece definition;
- piece instance location references existing space or zone;
- scenario references existing map and module;
- save references compatible module/scenario/map versions.

## Invariants

1. `Phaser` is never source of truth.
2. `map.json` does not contain current runtime state.
3. `scenario.json` does not contain play history.
4. `savegame.json` does not redefine definitions.
5. `Action` and `Event` are different things.
6. `PieceDefinition` and `PieceInstance` are different things.
7. Runtime state changes only through action/event pipeline.
8. All files carry `schemaVersion`.
9. Saves carry module/map/scenario version references or hashes.

## Authoring Vs Runtime Boundary

Safe default for `Table Sandbox 0.1`:

- `authoring` mode changes definitions and setup files;
- `playSandbox` mode changes current runtime state through `Action/Event`.

In practice:

- map edits belong to `map.json`;
- scenario setup edits belong to `scenario.json`;
- current piece movement belongs to `GameState` / `savegame.json`;
- current control changes belong to runtime state, not map definitions.

This boundary must stay explicit. The same visual gesture must not silently
edit definitions in one case and runtime state in another without a clear mode.

## Open Questions To Resolve

### Stack model

Need explicit decision:

- simple derived stacks from shared `locationId`; or
- first-class `Stack` entity; or
- `stackId` + `stackPosition` on `PieceInstance`.

Safe default for `Table Sandbox 0.1`:

- stack is a derived grouping by shared `locationId`;
- `Stack` is not a canonical entity yet;
- `stackId` and `stackPosition` are not required in the first save format;
- the first milestone keeps one-piece move as the primary proof path.

Why this default:

- it preserves the clean `PieceInstance -> locationId` contract;
- it avoids an extra stack lifecycle too early;
- it keeps `savegame.json` simple;
- it leaves advanced stacks for later without blocking the first slice.

### Module dependencies

Need explicit decision:

- can one module depend on another;
- how version compatibility works;
- whether shared assets/definitions are allowed.

### Save compatibility policy

Need explicit decision:

- hard block on version mismatch;
- warning-only mode;
- migration-required flow.

Safe default for `Table Sandbox 0.1`:

- block structural incompatibility;
- allow warning-only for minor safe metadata mismatches;
- defer migration engine.

## Recommended Follow-up

This file should be followed by:

1. `rules_hooks_interface.md`
2. `minimal_canonical_file_schemas.md`
3. future JSON/Zod schema specs
4. milestone-level implementation breakdown
