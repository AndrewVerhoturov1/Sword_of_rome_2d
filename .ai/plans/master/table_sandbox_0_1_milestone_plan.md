# Table Sandbox 0.1 Milestone Plan

## Status

Planning artifact. Operational milestone plan for the first sandbox loop.

## Goal

Собрать `Table Sandbox 0.1` как минимальный universal tabletop sandbox:

- canonical files can load and save;
- runtime owns authoritative `GameState`;
- actions become events through a visible pipeline;
- rules stay permissive and module-agnostic enough for the first test module;
- one tiny end-to-end slice proves the architecture.

Read this plan together with `minimal_canonical_file_schemas.md`. Use one
vocabulary everywhere:

- `project.json` = workspace index;
- `module.json` = module manifest;
- `map.json` = board topology;
- `scenario.json` = initial setup;
- `rules.metadata.json` = rules capabilities metadata;
- `savegame.json` = mutable runtime snapshot.

## Non-Goals

Пока не входит:

- full Sword of Rome rules;
- combat resolver;
- strict legality;
- hidden information;
- online/server sync;
- AI/opponent automation;
- advanced stack model;
- module dependency system;
- migration engine.

## Step Order

### 1. Minimal canonical data seed

Create the smallest sample module package that can round-trip:

- `project.json`;
- `module.json`;
- `map.json`;
- `scenario.<scenarioId>.json`;
- `rules.metadata.json`;
- `savegame.json`.

Follow `minimal_canonical_file_schemas.md` for the first-pass field contract.

Dependency:
- nothing else can be stable until IDs, references, and file ownership exist.

### 2. Runtime state bootstrap

Load module and scenario into initial `GameState`.

Dependency:
- requires canonical sample files;
- must preserve separation between definitions, scenario state, and save state.

### 3. Action/Event backbone

Make the request-to-commit pipeline explicit:

- input/request;
- `Action`;
- validation;
- `resolveAction`;
- committed `Event`;
- reducer;
- append-only event log;
- render refresh.

Dependency:
- depends on runtime state bootstrap;
- must exist before real drag/drop or editor mutation paths.

### 4. Permissive RulesHooks shim

Add minimal module rules that answer, not own, the runtime:

- `getAllowedActions`;
- `validateAction`;
- `resolveAction`;
- `checkWinCondition`;
- `getPhaseActions` and `onPhaseStart` may stay stubbed.

Dependency:
- sits on top of Action/Event backbone;
- must remain permissive for `0.1`.

### 5. First thin vertical slice

Prove one full loop:

- load sample module;
- load sample scenario;
- show board, spaces, and one or more pieces;
- drag one piece from one space to another;
- emit `move_piece_requested`;
- validate permissively;
- resolve to `piece_moved`;
- commit event;
- update `GameState`;
- append event log;
- redraw from `GameState`.

Dependency:
- requires steps 1 through 4.

### 6. Remaining manual table actions

After the first slice works, add the rest of the first-set manual actions:

- create piece;
- delete piece;
- change control;
- create space;
- update space;
- create connection;
- save snapshot;
- load save.

Dependency:
- should not start before the first slice proves the loop.

### 7. Basic authoring surfaces

Add minimal authoring controls that still write through the same canonical pipeline.

Dependency:
- must not invent a second data model;
- should not bypass runtime authority.

### 8. Save/load hardening

Make save/load round-trip the runtime state and event log without redefining content.

Dependency:
- useful once several event types exist.

### 9. Validation hardening

Add checks for:

- id uniqueness;
- reference integrity;
- known action/event types;
- valid piece locations;
- schema version compatibility.

Dependency:
- follows the first working pipeline;
- should remain runtime safety, not strict game rules.

### 10. Tiny test module pass

Only after the universal loop works, add a tiny Sword of Rome-like test layer:

- a few named spaces;
- a few faction/piece definitions;
- one scenario.

Dependency:
- must not reshape universal layers.

## Dependency Graph

```text
canonical sample files
→ GameState bootstrap
→ Action/Event backbone
→ permissive RulesHooks
→ first thin vertical slice
→ remaining manual actions
→ save/load hardening
→ validation hardening
→ tiny test module
```

## Acceptance Checks

`Table Sandbox 0.1` is acceptable when:

- a small sample module loads;
- one piece can move between two spaces through the full pipeline;
- runtime commits events and owns `GameState`;
- event log is visible and append-only;
- save/load round-trips the canonical state;
- rules stay permissive and do not hardcode the first test module into lower layers.
- the file roles match `minimal_canonical_file_schemas.md` exactly.

## Deferred Features

Explicitly after `0.1`:

- strict legality;
- full combat and scoring;
- card/deck subsystem;
- hidden info;
- reaction windows;
- online sync;
- AI;
- sophisticated stack model;
- module dependency framework;
- migration framework.

## Anti-Scope-Creep Rule

If a feature only makes the Sword of Rome-like test module more accurate, but does not
strengthen the universal sandbox loop, defer it.

## Next Artifact

After this plan, the natural follow-up is `first_vertical_slice_spec.md`.
