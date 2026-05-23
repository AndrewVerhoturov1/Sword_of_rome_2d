# Module Authoring Workflow

## Status

Planning artifact. Practical workflow for the authoring side of the platform.

## Purpose

Зафиксировать, как designer/developer работает с модулем на практике:

- что редактируется в одном workspace;
- что остаётся отдельными editor surfaces;
- как из authoring собирается module package;
- где проходит граница между authoring mode и play sandbox mode.

Это не новый уровень архитектуры. Это operational guide поверх уже принятого
`4-layer` split.

## Recommended Safe Default

Лучший вариант для этого проекта:

```text
one Module Authoring Workspace
+ several specialized editor surfaces inside it
+ explicit Play Sandbox Preview
```

Не нужен ни один огромный редактор, ни полностью разрозненные редакторы.
Нужен один общий рабочий центр модуля, внутри которого дизайнер переключается
между узкими surface-ами.

## Workspace Vs Surfaces

### One shared workspace

Единым должен быть:

- active module context;
- active scenario context;
- id registry;
- validation status;
- file graph;
- package save/export;
- preview/play launch;
- switching between surfaces.

### Specialized surfaces

Отдельными surfaces должны быть:

- `Module Settings / Manifest`;
- `Map Editor`;
- `Pieces / Factions Editor`;
- `Scenario Editor`;
- `Rules Metadata Surface`;
- `Play Sandbox Preview`;
- later `Cards Editor`;
- later `Documents Editor`.

## Practical Workflow

Типичный день работы дизайнера:

1. Open Module Authoring Workspace.
2. Create or select module.
3. Edit module settings and manifest.
4. Build map spaces, connections, zones.
5. Define factions and piece types.
6. Build scenario setup.
7. Adjust rules metadata.
8. Validate references.
9. Preview in Play Sandbox.
10. Move pieces, check runtime loop, inspect event log.
11. Save module package or save play snapshot.
12. Return to a surface that needs correction.

## How Module Package Is Assembled

Authoring workflow should produce a valid module package from canonical files:

```text
project.json
modules/<moduleId>/module.json
modules/<moduleId>/map.json
modules/<moduleId>/scenario.<scenarioId>.json
modules/<moduleId>/rules.metadata.json
```

For `Table Sandbox 0.1`, `module.json` may temporarily keep small
`PieceDefinition[]` and `FactionDefinition[]` inline as compact layout.

Play Sandbox then loads the package and creates `GameState` through the
`Action -> Event -> GameState` pipeline.

## Mode Boundary

### Authoring Mode

Changes:

- definitions;
- scenario setup;
- module metadata;
- rules metadata.

Writes:

- `project.json`;
- `module.json`;
- `map.json`;
- `scenario.<scenarioId>.json`;
- `rules.metadata.json`.

### Play Sandbox Mode

Changes:

- current runtime state;
- event log;
- save snapshot.

Writes:

- `GameState`;
- `eventLog[]`;
- `savegame.json`.

The same visual gesture must not silently switch meaning between these modes.

## Boundary Rules

- authoring changes create or edit the module package;
- runtime changes happen only through `Action/Event`;
- runtime must not silently rewrite definitions;
- authoring surfaces must not silently rewrite current save state;
- Play Sandbox Preview is for runtime proof, not for editing definitions.

## Table Sandbox 0.1 Scope

For `0.1`, keep this minimal:

- one Module Authoring Workspace;
- one Map surface;
- one Pieces/Factions surface;
- one Scenario surface;
- one Module Settings / Rules metadata surface;
- one Play Sandbox Preview;
- basic validation summary.

Can defer:

- cards editor;
- documents editor;
- assets manager;
- scenario variants;
- publishing tools;
- advanced package import/export;
- collaboration;
- migration tooling.

## Later Extension

Later the workspace can gain:

- cards/decks editor;
- documents / player-aid editor;
- assets library;
- validation / migration tools;
- package export/import manager;
- playtest session manager;
- server-authoritative preview;
- hidden-info tooling.

## Still Open

Still open on purpose:

- whether authoring gets its own transaction log;
- whether authoring undo/redo is separate from play undo;
- exact UI navigation between surfaces;
- when `PieceDefinition[]` and `FactionDefinition[]` should move out of `module.json`;
- whether scenario-fork-from-save becomes a first-class tool later.

## Relation To Module Package Model

This workflow is the practical authoring side for the package model.

The mature package shape is documented in `module_package_model.md`.

How to read both docs together:

- this file says how a designer works day to day;
- `module_package_model.md` says how the package should evolve as a product
  bundle;
- `module.json` stays a manifest in the long run, even if `0.1` keeps compact
  inline `pieces/factions`.

## Relation To Product UX Model

This file is not the full UX model of the product.

Use `module_product_ux_model.md` for:

- the full user loop across authoring, playtest, and runtime/save flows;
- explicit mode transitions;
- package lifecycle in the user's mental model.

Use this file for the narrower question:

- how the authoring side itself should work inside that larger UX model.

## External Prototype Input

The external `table-map-editor-canvas-local-fixed` prototype is most relevant to
the future Map Editor surface inside this workflow.

Use it as:

- a reference for map editing interaction;
- a donor of inspector/layout ideas;
- a source of candidate canvas behaviors;
- not a direct product architecture.
