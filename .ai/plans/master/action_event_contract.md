# Action Event Contract

## Status

Planning artifact. Local working contract for runtime backbone.

## Purpose

Зафиксировать минимальный, но устойчивый backbone для:

- input -> action
- validation
- resolution
- committed events
- `GameState` mutation
- log
- save/load

Этот документ не задаёт code signatures. Он задаёт смысл и boundaries.

## Core Principle

Нужно жёстко разделять:

- `Action` = запрос / намерение
- `Event` = подтверждённый факт

Простая формула:

```text
player/system asks -> Action
rules interpret -> proposed Event[]
runtime commits -> Event[]
runtime mutates -> GameState
runtime logs -> event log
renderer shows -> updated state
```

## Why This Exists

Без этого разделения быстро ломаются:

- replay
- undo
- debugging
- online sync later
- save compatibility
- boundary between universal runtime and module-specific rules

## Canonical Runtime Flow

### Step 1 — Input

User or system initiates something:

- drag piece
- create piece
- delete piece
- change control
- create space
- create connection

### Step 2 — Action

Runtime converts input into `Action`.

Meaning:

- "I want to do this"

At this point nothing has happened yet.

### Step 3 — Validation

Runtime asks rules layer:

- allowed?
- blocked?
- warning only?

Validation result does not mutate canonical state.

### Step 4 — Resolution

Rules layer returns `proposed events`.

Meaning:

- "if this action is accepted, these facts should happen"

### Step 5 — Commit

Runtime checks event shape and invariants, then commits events.

Only runtime may:

- append committed events
- mutate authoritative `GameState`
- persist save state
- trigger render from committed state

### Step 6 — State Apply

Runtime reducer applies committed events to `GameState`.

### Step 7 — Post-Commit

Runtime may then:

- check win condition
- refresh allowed actions
- save snapshot
- redraw UI

## Action Envelope

Minimum planning contract:

- `actionId`
- `type`
- `actorId`
- `payload`

Recommended later fields:

- `timestamp`
- `correlationId`
- `source`
- `mode`
- `targetRefs`

### Meaning Of Fields

#### `actionId`

Stable id of one request.

#### `type`

What kind of request this is.

Example:

- `move_piece_requested`
- `create_piece_requested`
- `delete_piece_requested`

#### `actorId`

Who initiated action.

Can be:

- player
- designer
- system

#### `payload`

Action-specific data.

Example for move:

- piece id
- from location
- to location

## Event Envelope

Minimum planning contract:

- `eventId`
- `seq`
- `type`
- `payload`
- `causedByActionId`

Recommended later fields:

- `timestamp`
- `actorId`
- `visibility`
- `notes`

### Meaning Of Fields

#### `eventId`

Stable id of one committed fact.

#### `seq`

Monotonic order in event log.

#### `type`

What fact happened.

Example:

- `piece_moved`
- `piece_created`
- `piece_deleted`

#### `payload`

Event-specific committed data.

#### `causedByActionId`

Links fact to originating request.

## Validation Result

Validation should return structured result, not vague yes/no.

Minimum planning contract:

- `status`
- `reasonCode`

Recommended statuses:

- `allow`
- `warn`
- `block`

Recommended extra fields later:

- `messageKey`
- `normalizedAction`
- `requiresConfirmation`

### Meaning

- `allow` = can proceed
- `warn` = can proceed, but runtime/user should see warning
- `block` = action stops, no events committed

## Resolve Result

Resolution should return structured consequences.

Minimum planning contract:

- `proposedEvents[]`

Recommended later fields:

- `warnings[]`
- `followUpPrompts[]`
- `pendingWindows[]`
- `requiresHumanConfirmation`

## GameState Relation

`GameState` is authoritative runtime truth.

Important rule:

- actions do not change `GameState`
- uncommitted events do not change `GameState`
- only committed events change `GameState`

## Reducer Principle

Reducer means:

- runtime applies committed event types to state in one canonical way

This prevents hidden mutation paths.

## Table Sandbox 0.1 Scope

### Manual Action Types

Required first-set actions:

- `move_piece_requested`
- `create_piece_requested`
- `delete_piece_requested`
- `change_control_requested`
- `create_space_requested`
- `update_space_requested`
- `create_connection_requested`
- `load_save_requested`
- `save_snapshot_requested`

Possible later manual actions:

- `split_stack_requested`
- `merge_stack_requested`
- `rotate_piece_requested`
- `attach_note_requested`

### Event Types

Required first-set events:

- `piece_moved`
- `piece_created`
- `piece_deleted`
- `control_changed`
- `space_created`
- `space_updated`
- `connection_created`
- `save_snapshot_created`

Possible later events:

- `stack_split`
- `stack_merged`
- `phase_started`
- `phase_ended`
- `response_window_opened`
- `game_ended`

## Action To Event Examples

### Move Piece

Action:

- request to move piece from one location to another

Possible events:

- `piece_moved`

### Create Piece

Action:

- request to place new piece instance

Possible events:

- `piece_created`

### Change Control

Action:

- request to change controller of space

Possible events:

- `control_changed`

### Create Space

Action:

- request to create map node

Possible events:

- `space_created`

## Manual vs Assisted vs Strict

### Manual

For earliest sandbox.

Behavior:

- runtime accepts most valid-shaped actions
- rules mostly warn, not block
- human retains freedom

### Assisted

Near-future target.

Behavior:

- common illegal moves can warn/block
- graph-aware checks appear
- more event consequences auto-derived

### Strict

Future only.

Behavior:

- rules fully gate legal play
- hidden info matters
- server-authoritative mode becomes realistic

## Runtime Authority Rules

Runtime alone may:

- assign final event sequence
- commit events
- mutate canonical `GameState`
- append event log
- write save snapshot
- trigger render from canonical state

Rules layer may not:

- commit events directly
- mutate canonical state directly
- write save files
- bypass reducer

## Invariants

1. Every committed event has `seq`.
2. Every committed event has known `type`.
3. Every event caused by action links to `causedByActionId`.
4. Blocked action produces no committed events.
5. Warning action may still produce committed events.
6. All state mutation happens through committed events.
7. Renderer never becomes source of truth.
8. Event log is append-only.

## Open Questions

### Stack model

Still open:

- whether stack is derived or first-class entity.

This affects:

- action payloads
- event payloads
- reducer logic

Planning default for `Table Sandbox 0.1`:

- stack is derived from shared `locationId`;
- `Stack` is not a first-class canonical entity yet;
- `stackId` and `stackPosition` are deferred until later.

### Save granularity

Still open:

- whether save stores full snapshot only;
- or snapshot plus replay metadata.

### Response windows

Still open:

- how nested reactions will appear in event flow later.

## Recommended Follow-up

After this artifact:

1. define `first_milestone_runtime_skeleton.md`
2. define concrete JSON examples for first action/event types
3. later tighten reducer and save compatibility policy
