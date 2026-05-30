# Editor Play Visual Continuity Route

## Status

Accepted route baseline after external answer `V1-20260527-003610`.

This document is a public planning artifact.

It does not start implementation by itself.

It fixes the accepted route, boundaries, and priority order for the next phase.

## Source

- Primary source:
  - `.ai/external_chats/notebook/2026-05-27_V1-20260527-003610_practical-route-to-dual-goal-editor-parity-with.md`
- Current repo maturity:
  - `.ai/project_state.md`
- Important design boundaries:
  - `.ai/plans/master/prototype_integration_mapping.md`
  - `.ai/plans/master/module_authoring_workflow.md`

## Intent

Move from current `Map Authoring 0.1 + 0020 checkpointed editor-growth state`
toward:

1. real `editor -> play/test` continuity;
2. later prototype parity for map editor UX;
3. later scenario authoring.

Priority is explicit:

`continuity first -> parity second -> scenario later`

## Accepted Problem Framing

Current main blocker is not "editor too weak".

Current main blocker is that editor and play/test do not share one explicit
visual/render contract.

Today:

- editor already has useful authoring surface:
  - underlay;
  - transform controls;
  - opacity / visibility / lock;
  - grid / snap;
  - undo / redo;
  - spaces / connections;
  - inspector / object list / validation;
  - preview;
- play/test already has useful runtime surface:
  - `GameState`;
  - Action/Event pipeline;
  - piece drag;
  - create/delete piece;
  - change control;
  - reset;
  - save/load snapshot.

But preview bridge is still too narrow:

- `draftToGameState()` carries graph/runtime data;
- authored map visual is not a first-class runtime render contract;
- play/test still feels like old fixed sandbox instead of authored map preview.

## Accepted Boundaries

- Current old `map-plane / rotate / underlay geometry` tail is not the main
  next topic anymore.
- Prototype `table-map-editor-canvas-local-fixed` stays reference/selective
  donor, not product-code foundation.
- Do not do wholesale prototype migration.
- Do not mix authoring draft with authoritative runtime `GameState`.
- Do not move underlay image directly into `GameState` as source of truth.
- Phaser remains renderer/input layer, not source of truth.

## Accepted Route

### 1. Editor -> Play Visual Continuity Bridge 0.1

Introduce separate shared display contract between editor and play/test.

Target shape:

- `MapRenderModel` or `MapVisualState`
- contains:
  - `mapId`
  - `coordinateSystem.width`
  - `coordinateSystem.height`
  - underlay `src`
  - underlay natural size
  - underlay offset / scale / rotation
  - visible / opacity
  - optional display-only grid metadata if truly needed

Preview should produce two artifacts side by side:

1. runtime `GameState` from spaces/connections
2. `mapVisual` from coordinate system + underlay

### 2. Phaser Viewport / Map-Size Support

After `mapVisual` exists:

- world bounds come from authored map;
- initial camera = fit-to-map;
- zoom in/out exists;
- reset/fit camera exists;
- pan exists;
- existing piece drag remains intact.

### 3. Runtime Underlay Rendering

Play/test renderer must draw authored underlay behind:

`underlay -> connections -> spaces -> pieces -> selection/drag visuals`

### 4. Test Pieces For Preview

Before Scenario Authoring, play/test needs a narrow test affordance:

- add one test piece in play/test;
- place it on selected/first space;
- move it through existing runtime pipeline;
- do not silently convert this into authored scenario data.

### 5. Runtime/Editor Validation Bridge

Add only narrow bridge checks, for example:

- map has spaces;
- connections reference existing spaces;
- map visual can render;
- play/test can fit authored bounds;
- if no pieces exist, UI tells how to add a test piece.

### 6. Editor UI Parity Pack 1

After continuity works, improve:

- object tree / object list;
- inspector grouping;
- context menu polish;
- visibility / lock affordances;
- validation panel polish.

### 7. Editor Connection Parity Pack

After continuity and basic UI polish:

- easier connection selection;
- clearer selected connection state;
- inspector/context actions;
- connection metadata;
- later curve points / bends.

### 8. Editor Map Surface Polish Pack

Later parity polish:

- hover / selection polish;
- grid / snap polish;
- editor map pan / zoom controls;
- underlay inspector polish;
- better Russian UI text;
- object state indicators.

### 9. Map Save / Export / Import Hardening

Clarify boundaries:

- canonical map data;
- editor-only UI state;
- runtime-only playtest state.

### 10. Scenario Authoring 0.1

Only after map continuity works:

- start pieces;
- start positions;
- start control;
- scenario validation;
- preview loop.

## Best Next Step Candidate

Best current bounded candidate:

`Editor -> Play Visual Continuity Bridge 0.1`

Expected first-step core:

1. create separate `MapRenderModel` / `MapVisualState`;
2. derive it from current editor draft during preview;
3. pass it into `PhaserStage`;
4. stop assuming authored map lives inside old fixed `800x500` world;
5. render authored underlay in play/test;
6. add fit-to-map and zoom without breaking current drag/action pipeline.

## What This Document Does Not Freeze Yet

This document fixes the route, but not yet the exact first implementation cut.

Still intentionally open:

- exact file-by-file first patch set;
- exact minimal type shape for `MapRenderModel`;
- whether grid display metadata belongs in first cut or later;
- exact acceptance checklist for the first implementation slice.

These points should be refined through the next bounded `/v1`.

## Non-Goals Right Now

- no wholesale prototype migration;
- no broad redesign of all editor/runtime layers;
- no full layer system;
- no zones pack;
- no curved connections pack in the first step;
- no full scenario editor;
- no full package export/import system;
- no underlay-as-`GameState` source of truth;
- no return to old rotate/map-plane bug as the main next topic.
