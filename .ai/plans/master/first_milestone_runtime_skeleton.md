# First Milestone Runtime Skeleton

## Status

Planning artifact. Next-step working skeleton for `Table Sandbox 0.1`.

## Purpose

Собрать следующий уровень планирования после уже принятого канона:

- 4-layer product architecture;
- canonical `definitions / runtime state / module rules` split;
- canonical file set;
- `RulesHooksInterface` boundary;
- `Action / Event` backbone.

Этот документ не вводит новый канон. Он раскладывает уже принятый канон в
последовательность работ для первого product milestone.

## Milestone Reading

`Table Sandbox 0.1` = минимальный universal runtime skeleton + data model
foundation + authoring shell, достаточные чтобы:

- хранить and load canonical project/module/map/scenario/save files;
- represent actions and committed events explicitly;
- run a universal tabletop shell without hardcoded module rules;
- оставить место для первого test module, не делая его центром платформы.

External sequencing input уточняет milestone дальше:

- сначала нужен минимальный canonical data seed;
- потом bootstrap `GameState` из module/scenario;
- потом `Action/Event` dispatcher;
- потом permissive `RulesHooks` shim;
- потом первый thin vertical slice;
- first slice = move one piece between two spaces through full pipeline.

## Non-Goals

Пока не входит:

- full game-specific rules engine;
- combat/scoring resolver;
- strict legality automation;
- online/server-authoritative sync;
- decks/cards as full subsystem;
- hidden-info model;
- first-class response windows.

## Planning Principle

Правильная очередь работ для первого milestone:

1. сначала закрепить data and persistence backbone;
2. затем action/event runtime spine;
3. потом universal runtime shell;
4. потом authoring surfaces, которые пишут в тот же canonical data model;
5. только потом module package seam для первого test module.

## Recommended Build Order

### Step 1 — Lock Core Data And Persistence

Goal:

- make canonical file set executable in planning terms;
- ensure data structures can round-trip cleanly.

Focus:

- `project.json`;
- `module.json`;
- `map.json`;
- `scenario.<scenarioId>.json`;
- `savegame.json`;
- version markers and reference integrity.

Decision gate:

- if a file cannot be loaded, validated, and re-saved deterministically,
  it is not ready for later layers.

### Step 2 — Implement Action/Event Backbone

Goal:

- make runtime mutation explicit and replayable.

Focus:

- `Action` envelope;
- `Event` envelope;
- validation result shape;
- resolve result shape;
- reducer principle;
- append-only event log.

Decision gate:

- no state mutation outside committed events;
- no hidden mutation paths in renderer or rules hooks.

### Step 3 — Build Universal Runtime Shell

Goal:

- run a play sandbox that is module-agnostic.

Focus:

- `GameState` owner;
- runtime state reducer;
- phase/turn scaffolding;
- render refresh from committed state;
- action request routing.

Decision gate:

- runtime remains single authority for committed state transitions;
- renderer is only a view;
- module rules answer, runtime commits.

### Step 4 — Add Universal Authoring Surfaces

Goal:

- let editor capabilities write the same canonical structures.

Focus:

- map authoring;
- space/connection authoring;
- piece definition / instance authoring separation;
- scenario authoring;
- inspector state;
- local undo/redo for authoring actions.

Decision gate:

- authoring tools must not invent a second data model;
- editor state stays separate from persisted content.

### Step 5 — Wire Module Package Seam

Goal:

- reserve a clean slot for the first test module.

Focus:

- `ModuleManifest`;
- `RulesMetadata`;
- rules hook entry wiring;
- content vs rules boundary;
- module package loading into universal runtime.

Decision gate:

- module content stays data;
- module rules stay behavior;
- module-specific logic does not leak into Layer 1-3.

## Suggested First Slice Sequence

If we need a more concrete execution order inside the milestone, use this:

1. `ProjectDataSchema`
2. `PersistenceModule`
3. `ActionEventModule`
4. `RuntimeTableModule`
5. `AuthoringToolsModule`
6. `MapGraphModule`
7. `PiecesStacksModule`
8. `DocumentsModule` placeholder
9. `ModuleManifest` / rules seam wiring

Reason:

- this sequence minimizes rework from schema churn;
- it makes save/load and event logging stable before UI breadth expands;
- it keeps the first test module from shaping core abstractions too early.

## Deferred Questions

These remain open on purpose and should not be silently collapsed during
planning:

- exact stack model;
- module dependency model;
- save compatibility policy;
- final event derivation split between runtime and rules hooks.

For `Table Sandbox 0.1`, stack safe default is derived grouping by
`locationId`, not a separate canonical `Stack` entity.

## Useful Output Of This Artifact

After this doc is accepted, next planning step can be one of:

1. a narrower schema spec for the first canonical files;
2. a more concrete module-by-module implementation roadmap for `Table Sandbox 0.1`;
3. a `/v1` question focused only on milestone ordering if external validation is still desired.

For the schema track, the next artifact should be `minimal_canonical_file_schemas.md`.

## External Sequencing Knowledge

This milestone should not be planned as a broad game build. The useful external
signal is strictly sequencing:

- build the smallest canonical sample set first;
- use it to prove runtime loading and state bootstrap;
- wire the action/event backbone before expanding tool breadth;
- keep rules permissive until the sandbox loop exists;
- use one piece-move slice as the first end-to-end proof.

This knowledge belongs here because it refines the already accepted canon without
changing layer boundaries or data contracts.

## Execution Bridge

This artifact no longer acts as the final planning stop before coding.

The practical bridge from accepted planning canon to the first implementation
block is now defined in `pre_code_closure_and_first_execution_plan.md`.

The next real step is a short pre-code closure that freezes:

- the first product-code brief;
- the technical shell;
- the tiny canonical fixture set;
- the first action/event pair;
- the first acceptance checklist.

The concrete artifact for that closure is
`../implementation/first_product_code_block.md`.

After that short closure, implementation should begin through the narrow
`Table Sandbox 0.1` slice instead of another broad planning pass.
