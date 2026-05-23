# Rules Hooks Interface

## Status

Planning artifact. Local working contract for module-specific rules boundary.

## Purpose

Зафиксировать шов между:

- `Universal Runtime / Play Sandbox`
- `Module Rules/Hooks`

Core rule:

runtime asks;
module rules answer;
runtime applies and logs.

## Boundary Principle

Universal runtime must not hardcode Sword of Rome-like logic.

Module rules must not:

- mutate Phaser directly;
- own save files directly;
- silently mutate authoritative state outside runtime pipeline.

Rules layer receives structured input and returns structured output.

## Minimal Runtime Pipeline

```text
player/system input
-> Action request
-> runtime asks rules: allowed? valid?
-> rules returns validation/result payload
-> runtime derives/applies committed events
-> GameState updates
-> event log appends
-> renderer redraws
```

## Recommended Contract Shape

### Mandatory Hooks

#### `getAllowedActions(context)`

Purpose:

- tell runtime what actions are currently available.

Input:

- read-only `GameState`
- actor context
- module content references
- phase/turn context

Output:

- list of allowed action descriptors
- optional UI hints

#### `validateAction(context, action)`

Purpose:

- answer whether requested action is legal.

Input:

- read-only `GameState`
- action payload
- actor context

Output:

- `valid: true/false`
- reason codes when invalid
- optional normalized action payload

#### `getPhaseActions(context)`

Purpose:

- expose phase-specific possible actions.

Input:

- current `PhaseState`
- actor context
- read-only `GameState`

Output:

- action descriptors for current phase

#### `onPhaseStart(context)`

Purpose:

- emit phase-start consequences or prompts.

Input:

- new phase context
- read-only `GameState`

Output:

- proposed events
- prompts/required decisions
- no direct mutation

#### `checkWinCondition(context)`

Purpose:

- answer whether scenario/module has reached terminal victory state.

Input:

- read-only `GameState`
- module content references

Output:

- `winner` or `no winner`
- optional reason codes

### Recommended Near-Term Hook

#### `resolveAction(context, action)`

Purpose:

- transform validated action into proposed event list.

Why useful:

- keeps state mutation centralized in runtime;
- keeps rules logic modular;
- prevents event generation from leaking into UI layer.

Output:

- ordered event list
- optional follow-up prompts

## Hook Input Contract

Rules hooks may read:

- read-only `GameState`
- read-only module content
- read-only rules metadata
- actor reference
- phase/turn context
- optional RNG service abstraction later

Rules hooks may not read/write:

- Phaser scene objects as truth
- DOM state
- files directly
- git/shell/runtime side channels

## Hook Output Contract

Hook outputs should be:

- deterministic for same input
- JSON-serializable or easily serializable
- explicit, never implicit

Allowed output kinds:

- validation result
- allowed action descriptors
- proposed event list
- win result
- phase prompt metadata

## Ownership Rules

### Runtime owns

- authoritative `GameState`
- applying events
- appending event log
- persistence
- save/load
- UI refresh

### Module rules own

- legality knowledge
- module-specific phase logic
- module-specific restrictions
- victory checks
- module-specific consequence logic

## Automation Profiles

Recommended `automationLevel` values:

### `manual`

Runtime mostly permissive. Rules hooks provide hints, not strict enforcement.

### `assisted`

Rules hooks validate many actions and derive common consequences, but some outcomes remain human-confirmed.

### `strict`

Rules hooks validate and resolve almost all legal play paths.

For early `Table Sandbox 0.1`, default target:

- `manual` to `assisted`

Do not optimize for `strict` too early.

## Invariants

1. Hooks do not mutate authoritative state in place.
2. Hooks do not bypass action/event pipeline.
3. Hooks do not embed renderer logic.
4. Hooks do not serialize executable code into JSON metadata.
5. Runtime remains single authority for committed state transitions.

## Open Questions

### Event derivation boundary

Need final decision:

- does runtime derive generic events after validation; or
- does `resolveAction(...)` return all events from rules layer.

Recommended direction:

- rules returns proposed events;
- runtime commits them.

### Visibility and hidden information

Need later extension for:

- player-specific views;
- secret hands/decks;
- fog-of-war style restrictions if any appear.

### Interrupt windows

Need later decision for:

- response windows;
- reactions;
- nested prompts.

## Recommended Follow-up

After this file:

1. convert this contract into explicit schema/examples;
2. define action envelope and event envelope;
3. define first milestone hook subset for `Table Sandbox 0.1`.
