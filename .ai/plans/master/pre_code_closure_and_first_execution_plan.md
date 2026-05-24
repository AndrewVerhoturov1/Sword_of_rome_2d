# Pre-Code Closure And First Execution Plan

## Status

Accepted planning synthesis from `V1-20260524-003946`.

## Purpose

This artifact closes the gap between the accepted planning canon and the first
real product-code implementation block.

It does not replace the broader post-`0.1` roadmap. It defines the short,
practical bridge from:

- accepted architecture and planning canon;
- to a narrow, safe first coding phase.

## Current Position

The project already has enough architectural and planning structure to stop
broad exploratory planning.

What is still missing is not another large design pass, but a short execution
closure that freezes:

- the first product-code target;
- the technical shell;
- the tiny canonical fixture seed;
- the first action/event pair;
- the acceptance threshold for the first slice.

## Nearest Step

The nearest step is to create and accept a tiny first product-code brief for
the narrowest `Table Sandbox 0.1` slice.

That brief should lock:

- runtime shell direction;
- the tiny fixture set;
- `move_piece_requested -> piece_moved` as the first action/event pair;
- the first observable acceptance checklist.

## Phase 0 - Pre-Code Closure

Goal:
Freeze the narrowest safe implementation target before writing broad product
code.

Expected output:

- first product-code brief;
- technical shell decision;
- tiny canonical fixture set;
- fixed first action/event pair;
- acceptance checklist;
- frozen prototype role.

Why now:
Without this closure, implementation can drift into broad product-building or
accidental prototype carryover.

Dependencies:

- accepted `Table Sandbox 0.1` milestone;
- accepted first vertical slice target;
- accepted prototype integration decision.

Done condition:
All six items above are explicit and no longer treated as open planning topics.

## Phase 1 - Technical Bootstrap

Goal:
Stand up the smallest real product shell for the first slice.

Expected output:

- Vite host app;
- React shell;
- TypeScript baseline;
- Phaser integration boundary;
- explicit rule that canonical runtime state lives outside Phaser.

Why now:
The first coding slice needs a stable host before loading fixtures and driving
the runtime loop.

Dependencies:

- completed Phase 0.

Done condition:
The app boots cleanly and has a clear boundary between host shell, runtime
state, and rendering layer.

## Phase 2 - Canonical Fixture Seed

Goal:
Introduce the smallest canonical data set that can drive the first real slice.

Expected output:

- tiny `project/module/map/scenario/rules/save` fixtures;
- two spaces;
- one movable piece;
- one scenario setup;
- one minimal runtime snapshot path.

Why now:
The first slice must prove the canonical data path, not a hardcoded demo-only
runtime.

Dependencies:

- completed Phase 1;
- accepted canonical file model.

Done condition:
The fixture set is small, readable, and sufficient to drive one end-to-end
piece move.

## Phase 3 - Runtime/Data Bootstrap

Goal:
Load canonical fixture data into a minimal `GameState` bootstrap.

Expected output:

- load path from fixtures into runtime state;
- minimal `GameState` shape for the first slice;
- explicit runtime ownership outside Phaser.

Why now:
The project must prove data-first runtime flow before it proves richer UI or
authoring features.

Dependencies:

- completed Phase 2.

Done condition:
The app can initialize a minimal runtime state from canonical fixture inputs.

## Phase 4 - Action/Event Spine

Goal:
Prove the first real `Action -> Event -> GameState -> log` loop.

Expected output:

- `move_piece_requested`;
- validation for the tiny slice;
- `piece_moved`;
- runtime state update;
- event log entry.

Why now:
This is the smallest meaningful proof that the platform runtime loop actually
works as designed.

Dependencies:

- completed Phase 3;
- accepted action/event contract.

Done condition:
One intentional action causes one validated event and one visible runtime state
change with log output.

## Phase 5 - First Vertical Slice

Goal:
Prove the first thin vertical slice from load to render.

Expected output:

- load canonical fixtures;
- build initial runtime state;
- trigger one piece move;
- update state;
- record log;
- render the result.

Why now:
This is the first point where the project stops being planning-only and becomes
a real executable product slice.

Dependencies:

- completed Phase 4.

Done condition:
The full narrow loop is visible and repeatable:

`load -> GameState -> Action -> Event -> log -> render`

## Immediate Post-First-Slice Phases

After the first slice is proven, the next work should stay narrow:

1. harden the same slice with clearer acceptance checks;
2. add one more manual action without broadening the architecture;
3. improve fixture validation and save/load boundaries;
4. only then expand toward controlled authoring-side surfaces.

## What Must Wait

The following should wait until after the first slice is proven:

- broad authoring workspace implementation;
- rich package management flows;
- complex playtest session management;
- deeper prototype extraction work;
- advanced rules automation;
- richer optional content groups.

## Stop-Planning Start-Coding Threshold

Planning should stop and implementation should begin when all of the following
are explicit:

- the technical shell is fixed;
- the fixture seed is fixed;
- the first action/event pair is fixed;
- the acceptance checklist is fixed;
- the prototype role is frozen as reference-only input.

At that point, more broad planning is lower-value than implementation.

## Anti-Overplanning Guardrail

Do not open new broad planning branches before the first slice exists in code.

Allowed planning after this point should be only:

- short execution notes directly supporting the first slice;
- tiny clarifications needed to unblock implementation;
- verification of whether the first slice matches the already accepted canon.
