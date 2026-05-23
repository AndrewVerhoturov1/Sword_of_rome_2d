# First Vertical Slice Spec

## Status

Planning artifact. One end-to-end proof slice for `Table Sandbox 0.1`.

## Slice Definition

One piece moves from one space to another through the full canonical pipeline.

## Preconditions

- sample module exists;
- sample scenario exists;
- runtime can load definitions and state into `GameState`;
- permissive rules shim is present;
- action/event log is wired.

## Input

User drags one piece from `space A` to `space B`.

## Expected Pipeline

### 1. Request

Runtime emits `move_piece_requested`.

### 2. Validation

Rules answer permissively.

- valid shaped action: allow;
- broken refs or malformed payload: block.

### 3. Resolution

Rules return `piece_moved` as proposed event.

### 4. Commit

Runtime commits the event, assigns sequence, and appends to log.

### 5. State Apply

Reducer updates authoritative `GameState`.

### 6. Render

View redraws from committed state, not from raw input.

## Expected Result

- piece appears in `space B`;
- event log shows the move;
- no hidden mutation path exists outside committed event handling;
- `GameState` stays the sole source of truth;
- module rules remain permissive and do not own state mutation.

## Acceptance Criteria

This slice is valid only if all of the following are true:

- the move uses the canonical `Action -> Event -> GameState` pipeline;
- validation, resolution, commit, reducer, log, and render all happen visibly;
- the same slice can be replayed from canonical data;
- the test module does not require special-case lower-layer logic.

## What This Slice Proves

- canonical data load works;
- runtime bootstrap works;
- `RulesHooksInterface` boundary works;
- `Action/Event` separation works;
- runtime ownership of state works;
- renderer is a view only.

## Out Of Slice

Do not pull these into the first slice:

- combat;
- cards;
- hidden info;
- multi-step phases;
- reaction windows;
- save migration;
- online sync;
- strict legality;
- polished UI.

## Next Steps After Slice

If this slice works, the next sensible expansion is:

1. remaining manual actions;
2. save/load hardening;
3. validation hardening;
4. tiny test module pass.
