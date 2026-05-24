# First Product Code Block

## Status

Accepted implementation-brief target after `V1-20260524-005734`.

## Intent

This document freezes the first narrow product-code block for `Table Sandbox
0.1`.

It does not introduce new architecture. It translates the accepted planning
canon into one executable implementation target.

## Goal

Build the first narrow `Table Sandbox 0.1` slice:

`tiny canonical fixture module -> initial GameState -> render
board/spaces/piece -> move_piece_requested Action -> permissive validation ->
piece_moved Event -> reducer updates GameState -> event log updates ->
renderer redraws from GameState -> basic save/load snapshot`

The goal is not to build the full product, full game, full authoring workspace,
or full Sword of Rome-like module.

## Technical Shell Decision

Use:

- Vite
- React
- TypeScript
- Phaser

Role split:

- React owns the application/editor shell.
- Phaser owns visual table rendering and pointer input.
- Runtime owns `GameState`, `Action/Event` pipeline, reducer and event log.
- `RulesHooks` answer runtime questions.
- Phaser must not be source of truth.

Renderer input may request actions.
Renderer objects must not directly mutate authoritative `GameState`.

## Prototype Decision

The existing `table-map-editor-canvas-local-fixed` prototype is reference plus
selective donor.

Use it only for ideas such as:

- layers;
- spaces;
- connections;
- curved paths;
- zones;
- inspector behavior;
- validation ideas;
- `map.json` export ideas;
- Russian UI behavior.

Do not copy it wholesale as product architecture.

## Product-Code Starting Boundary

Start a new product-code skeleton clearly separated from old prototypes.

The first implementation block may create the smallest app shell needed for the
slice, but must not migrate the whole prototype.

Keep these responsibilities separate:

- runtime;
- renderer/table surface;
- fixtures;
- persistence;
- validation;
- `RulesHooks` shim;
- event log.

## Tiny Fixture Set

Required fixture files:

- `project.json`
- `module.json`
- `map.json`
- `scenario.basic.json`
- `rules.metadata.json`
- `savegame.empty.json`

Minimum content:

- 1 project;
- 1 module;
- 1 map;
- 2 spaces;
- 1 connection;
- 1 scenario;
- 1 or 2 factions;
- 1 or 2 piece definitions;
- 1 movable piece instance;
- permissive/manual rules metadata.

File role rules:

- `project.json` is workspace index.
- `module.json` is module manifest.
- `map.json` is board topology.
- `scenario.basic.json` is initial setup.
- `rules.metadata.json` is declarative rules capability metadata.
- `savegame.empty.json` is runtime snapshot state, not canonical module content.

## First Action

Type:

`move_piece_requested`

Payload:

- `pieceId`
- `fromLocationId`
- `toLocationId`

Meaning:

The user/system requests moving one piece from one location to another.

## First Event

Type:

`piece_moved`

Payload:

- `pieceId`
- `fromLocationId`
- `toLocationId`

Meaning:

The runtime has accepted and committed the move.

Action = request / intention.
Event = committed fact.

## Runtime Rule

No direct state mutation from renderer, Phaser scene, UI component, or
`RulesHooks`.

Correct flow:

`Phaser/input -> Runtime creates Action -> RulesHooks validate/resolve ->
Runtime commits Event -> Reducer updates GameState -> Event log appends ->
Renderer redraws from GameState`

## Acceptance Checklist

Done only when:

- app starts locally;
- React shell renders;
- Phaser scene/table area renders inside the shell;
- tiny fixture module loads;
- initial `GameState` is created from fixture data;
- spaces render;
- one piece renders at location A;
- user can request moving the piece to location B;
- runtime creates `move_piece_requested`;
- validation allows the action;
- resolution returns `piece_moved`;
- runtime commits the event;
- committed event receives sequence/order;
- event log displays the committed event;
- reducer changes piece location in `GameState`;
- renderer redraws the piece at location B;
- basic save/load preserves `GameState` and event log;
- no Phaser object is authoritative source of truth;
- no Sword of Rome-specific lower-layer logic is introduced.

## Explicit Non-Goals

Do not implement in this block:

- full Sword of Rome rules;
- combat;
- scoring;
- cards/decks;
- strict legality;
- hidden information;
- multiplayer;
- online/server authority;
- AI;
- full module package importer/exporter;
- full Map Editor migration;
- mature asset system;
- full Scenario Editor;
- full Pieces/Factions Editor;
- advanced stack model;
- save migration framework;
- polished final UI.

## Stop Condition

Stop this implementation block when one piece can move from one space to
another through:

`Action -> Event -> GameState -> event log -> render -> save/load`

After that, create a short implementation report before expanding scope.

## Immediate Next Step After This Block

After this block is complete, do not jump to full rules or full editor
migration.

Next candidates are, in this order:

1. harden the same first slice;
2. add one more manual action;
3. improve fixture validation;
4. improve save/load boundaries;
5. only then begin controlled Map Editor integration.
