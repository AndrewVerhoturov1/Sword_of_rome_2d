# Notebook Entry

- External Question ID: `V1-20260523-062449`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_brief.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/canon/context/sword_of_rome_web_project_context.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md`

## Candidate Navigation Entry

Topic: RulesHooksInterface second opinion for the universal 2D counter-based wargame authoring platform
Summary: Recommendation: use a hybrid resolution model where module rules return proposed events through `resolveAction`, but runtime remains the sole committer that applies events, mutates `GameState`, appends the log, persists saves, and triggers render; Table Sandbox 0.1 should stay manual-to-assisted, not strict.

## Raw Response

## External Question ID

V1-20260523-062449

## Context Readback

* Uploaded task prompt / `Вставленный текст(8).txt`: fully read 
* Central rules — `external_chat_rules.md`: fully read ([GitHub][1])
* Central navigation — `repo_navigation.md`: fully read ([GitHub][2])
* Project repo navigation — `.ai/repo_navigation.md`: fully read ([GitHub][3])
* Project brief — `.ai/project_brief.md`: fully read ([GitHub][4])
* Project state — `.ai/project_state.md`: fully read ([GitHub][5])
* Project architecture — `.ai/architecture.md`: fully read ([GitHub][6])
* Project decisions — `.ai/decisions.md`: fully read ([GitHub][7])
* Main project context — `canon/context/sword_of_rome_web_project_context.md`: fully read ([GitHub][8])
* README: fully read ([GitHub][9])
* Navigation-discovered `AGENTS.md`: fully read ([GitHub][10])
* Navigation-discovered `.ai/plans/master/rules_hooks_interface.md`: fully read ([GitHub][11])
* Navigation-discovered `.ai/plans/master/domain_schemas_contract.md`: fully read ([GitHub][12])

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Boundary Framing

Boundary понимаю так: **Universal Runtime / Play Sandbox не знает конкретных правил Sword of Rome-like или другого модуля; он знает только универсальные Action, Event, GameState, phase shell, persistence и render update. Module Rules/Hooks знают module-specific legality, phases, restrictions, consequences and victory checks, но не владеют authoritative state и не пишут save-файлы напрямую.**

Ключевая формула правильная и её стоит закрепить как канон:

```text
runtime asks
module rules answer
runtime applies and logs
```

Это совпадает с уже опубликованной архитектурой: Layer 3 исполняет универсальный цикл `Action -> Event -> GameState -> Render`, а Layer 4 содержит `Module Content` и `Module Rules/Hooks`; `RulesHooksInterface` уже назван обязательным швом между ними. ([GitHub][6])

Также подтверждается, что Phaser не источник истины: истина живёт в `GameState`, JSON и событиях; Phaser только отображает состояние и переводит input в action/event pipeline. ([GitHub][8])

### Recommended Hook Set

Текущий minimal hook set **почти достаточен**, но я бы сделал `resolveAction(...)` не optional-идеей, а **near-term mandatory для первого нормального Play/Runtime skeleton**, даже если в Table Sandbox 0.1 он пока будет тривиальным.

**Final minimal viable hook set для Table Sandbox 0.1:**

1. `getAllowedActions(context)`
2. `validateAction(context, action)`
3. `resolveAction(context, action)`
4. `checkWinCondition(context)`

**Можно stub/placeholder в Table Sandbox 0.1:**

5. `getPhaseActions(context)`
6. `onPhaseStart(context)`

Причина: в Table Sandbox 0.1 фокус — ручной Vassal-like стол, drag/drop, snap, stacks, log, save/load; полная phase automation и strict rules не входят в 0.1. ([GitHub][8])

**Near-future hook set для later phases:**

1. `getAllowedActions(context)`
2. `validateAction(context, action)`
3. `resolveAction(context, action)`
4. `getPhaseActions(context)`
5. `onPhaseStart(context)`
6. `onPhaseEnd(context)` — добавить позже, когда появятся автоматические cleanup/end-phase effects.
7. `checkWinCondition(context)`
8. `getPlayerView(context, actorId)` — later, для hidden info / server-authoritative future.
9. `getResponseWindows(context, eventOrAction)` — later, для reactions, cards, interrupts.
10. `resolveResponse(context, responseAction)` — later, когда появятся response windows/cards.
11. `getSetupOptions(context)` — later, если сценарии начнут иметь selectable setup variants.
12. `getAutomationProfile(context)` — optional later, если module/rules variants будут менять manual/assisted/strict behavior.

### Hook-by-Hook Contract

#### `getAllowedActions(context)`

**Purpose:** сказать runtime, какие действия сейчас можно показать игроку/разработчику как доступные.

**Inputs:**

* read-only `GameState`
* read-only module content
* actor context: `actorId`, `role`, `factionId`, permissions
* phase/turn context
* automation level: `manual`, `assisted`, `strict`
* optional selected object context: selected piece/space/card later

**Outputs:**

* list of action descriptors:

  * `actionType`
  * target requirements
  * UI label / hint key
  * enabled/disabled state
  * reason code if disabled
  * optional payload template

**Must not do:**

* mutate `GameState`
* move pieces
* append events
* touch Phaser/DOM
* save files
* secretly filter by hidden state without explicit visibility model later

#### `validateAction(context, action)`

**Purpose:** проверить, допустим ли requested action.

**Inputs:**

* read-only `GameState`
* read-only module content
* action payload
* actor context
* phase/turn context
* automation level

**Outputs:**

* `valid: true/false`
* `severity`: `allow`, `warn`, `block`
* `reasonCode`
* human-readable message key
* optional normalized action payload
* optional required confirmation flag in manual/assisted mode

**Must not do:**

* produce committed events directly as side effect
* mutate state in place
* throw UI-specific errors as control flow
* assume client authority in future online mode

#### `resolveAction(context, action)`

**Purpose:** превратить уже validated action в **proposed events**.

**Inputs:**

* read-only `GameState`
* read-only module content
* validated/normalized action
* actor context
* phase/turn context
* deterministic services, later:

  * RNG abstraction
  * clock abstraction
  * id generator abstraction

**Outputs:**

* ordered proposed event list
* optional follow-up prompts
* optional pending response windows later
* optional warnings/notes
* optional `requiresHumanConfirmation` in assisted/manual mode

**Must not do:**

* commit events by itself
* write event log by itself
* mutate `GameState` in place
* mutate Phaser/DOM
* save/load directly
* call non-deterministic global random/time directly if replay matters

This hook is the answer to the open question: rules should return **proposed events**, runtime commits them. The existing planning artifact already points this way: rules return proposed events; runtime commits them. ([GitHub][11])

#### `getPhaseActions(context)`

**Purpose:** expose phase-specific actions and required steps.

**Inputs:**

* current `PhaseState`
* `TurnState`
* read-only `GameState`
* actor context
* module rules metadata

**Outputs:**

* phase action descriptors
* required actions
* optional phase prompts
* optional skip/end phase eligibility

**Must not do:**

* advance phase directly
* mutate state
* decide UI layout
* create events as side effect

For Table Sandbox 0.1 this can be placeholder because phase tracker is later than the first manual sandbox. ([GitHub][8])

#### `onPhaseStart(context)`

**Purpose:** describe automatic or prompted consequences when a phase starts.

**Inputs:**

* previous phase
* new phase
* read-only `GameState`
* actor/system context
* module content
* rules metadata

**Outputs:**

* proposed events
* prompts / required decisions
* pending windows
* log notes

**Must not do:**

* mutate state in place
* append log directly
* query UI directly
* hide mutation in internal module state

#### `onPhaseEnd(context)` — later addition

**Purpose:** symmetrical cleanup hook for end-phase effects.

**Inputs:**

* ending phase
* read-only `GameState`
* actor/system context
* module content

**Outputs:**

* proposed cleanup events
* next phase recommendation
* unresolved mandatory action warnings

**Must not do:**

* advance turn directly
* mutate state
* bypass event log

This should be later, not first block, because early milestone is manual table sandbox, not full turn/phase automation.

#### `checkWinCondition(context)`

**Purpose:** answer whether the current state has reached terminal victory or scoring threshold.

**Inputs:**

* read-only `GameState`
* scenario definition
* module content
* rules metadata
* phase/turn context, if victory is phase-gated

**Outputs:**

* `status`: `none`, `winner`, `draw`, `scenarioEnded`
* optional `winnerFactionId`
* reason codes
* score snapshot if needed

**Must not do:**

* end game directly
* mutate save
* append final event directly
* display modal directly

Runtime can call this after committed events and then, if needed, create/commit a universal `game_ended` or `win_condition_met` event.

#### `getPlayerView(context, actorId)` — later

**Purpose:** prepare player-specific view for hidden info and server-authoritative future.

**Inputs:**

* full authoritative `GameState`
* actor/player id
* module content
* visibility rules

**Outputs:**

* redacted `PlayerView`
* allowed public/private info
* hidden placeholders

**Must not do:**

* mutate authoritative state
* leak hidden info into client-visible structures
* replace canonical `GameState`

This directly aligns with the future Rally-like architecture in project context: server/rules engine eventually gives player-specific views, clients send action requests, server validates and appends event log. ([GitHub][8])

#### `getResponseWindows(context, eventOrAction)` — later

**Purpose:** detect whether a just-proposed or just-committed action/event opens response/reaction opportunities.

**Inputs:**

* action or event
* read-only `GameState`
* actor context
* phase context
* card/hand state later

**Outputs:**

* response window descriptors
* eligible actors
* allowed response actions
* timeout/manual close rules

**Must not do:**

* pause UI by direct DOM manipulation
* mutate state without event
* create hidden queue outside runtime

### Recommended Resolution Model

Рекомендация: **hybrid split, but with runtime as final committer.**

То есть:

```text
rules hook derives proposed events
runtime validates event shape/invariants
runtime commits events
runtime applies reducer to GameState
runtime appends log
runtime triggers render/update
```

Не стоит делать так, чтобы runtime сам после validation всегда выводил events без rules hook. Это быстро сломается на module-specific consequences: movement restrictions, phase effects, card effects, victory/scoring, special procedures.

Но и не стоит давать rules hook полную власть "сразу менять state". Это сломает replay, undo, online sync, save/load, debugging and server-authoritative future.

Правильная формула:

```text
Module rules own consequence knowledge.
Runtime owns authority and commit.
```

Для generic sandbox actions runtime может иметь built-in default resolvers. Например, `move_piece_manual`, `create_piece`, `delete_piece`, `set_control_manual`, `add_note`. Но даже они должны проходить через тот же envelope:

```text
Action -> validate -> resolve to Event[] -> commit Event[] -> apply to GameState
```

Иначе появятся два разных runtime пути: "настоящие rules events" и "ручные editor mutations". Это опасно.

### Runtime Pipeline

Recommended pipeline:

```text
1. Input
   Phaser/React captures user interaction.

2. Action Request
   InputPipeline creates Action object.
   Example: move_piece_requested.

3. Runtime Precheck
   Runtime checks schema, actor, target ids, mode, basic invariants.

4. Allowed Actions Query
   Runtime may call getAllowedActions(context) for UI hints or pre-filtering.

5. Validation
   Runtime calls validateAction(context, action).
   Result can be allow / warn / block depending on automation level.

6. Resolution
   Runtime calls resolveAction(context, normalizedAction).
   Hook returns proposed Event[].

7. Event Verification
   Runtime checks event schema, references, sequenceability, no forbidden event types.

8. Commit
   Runtime appends events to event log.

9. State Apply
   Runtime reducer applies events to GameState.

10. Post-Commit Hooks
   Runtime may call checkWinCondition(context).
   Later: getResponseWindows(context, committedEvents).

11. Persistence Boundary
   Persistence module can save GameState/event log.
   Rules hooks do not save.

12. Render
   React/Phaser re-render from GameState/PlayerView.
```

For first milestone, the pipeline can be simple but should already preserve the distinction between `Action` as request and `Event` as committed fact. The existing domain contract explicitly says `Action` and `Event` must remain separate and runtime state changes go through the action/event pipeline. ([GitHub][12])

### Automation Levels

#### `manual`

Target for Table Sandbox 0.1.

Behavior:

* most actions are allowed;
* validation catches only schema/reference errors;
* rule violations are warnings, not blockers;
* user/developer can override;
* logs still record events;
* save/load still works;
* Phaser still not source of truth.

Example:

```text
move any piece to any space -> allowed
stacking limit violation -> no block, maybe warning later
phase mismatch -> ignored or informational
```

This matches the project context: 0.1 is effectively Designer Mode + soft hints, with free movement and no stacking limits yet. ([GitHub][8])

#### `assisted`

Target after manual sandbox stabilizes.

Behavior:

* common illegal actions get warnings or soft blocks;
* movement can check graph connectivity;
* phase-specific action hints appear;
* common consequences can be auto-derived;
* humans can still confirm/override uncertain outcomes;
* action log remains canonical.

Example:

```text
move by connected spaces -> allowed
move through impossible connection -> warning or blocked depending setting
combat/card effects -> may require manual confirmation
```

#### `strict`

Future only.

Behavior:

* illegal actions are blocked;
* phase sequence is enforced;
* hidden info is respected;
* response windows are structured;
* client cannot self-authorize rules;
* server can become final authority.

Example:

```text
client sends action request
server validates via hooks
server resolves events
server commits state
client receives player-specific view
```

Do not optimize for strict too early. The planning artifact already recommends `manual` to `assisted` for early Table Sandbox 0.1 and explicitly says not to optimize for strict too early. ([GitHub][11])

### What Must Exist In First Product-Code Block

Minimum required now:

1. **Action envelope**

   * `actionId`
   * `type`
   * `actorId`
   * `payload`
   * optional `timestamp`
   * optional `correlationId`

2. **Event envelope**

   * `eventId`
   * `seq`
   * `type`
   * `payload`
   * `causedByActionId`
   * optional `actorId`
   * optional `timestamp`

3. **Runtime dispatcher**

   * receives action
   * validates schema
   * calls hooks/default resolver
   * commits events
   * applies reducer
   * updates log

4. **Minimal `RulesHooksInterface` object**

   * even if default permissive implementation is used.

5. **Default permissive module rules**

   * `getAllowedActions`: returns generic table actions.
   * `validateAction`: checks references, blocks malformed actions only.
   * `resolveAction`: returns generic events for manual actions.
   * `checkWinCondition`: returns no winner.

6. **Event reducer**

   * `piece_moved`
   * `piece_created`
   * `piece_deleted`
   * `control_changed`
   * `space_created`
   * `space_updated`
   * `connection_created`

7. **Mode flag**

   * `designer`
   * `play`
   * initially both can use mostly manual behavior, but the boundary is present.

Can be delayed:

* full phase automation;
* real Sword of Rome-like rules;
* combat resolver;
* card engine;
* response windows;
* hidden info;
* server-authoritative sync;
* strict enforcement;
* full `getPlayerView`.

### Later Extensions

#### Phase logic

Near-future:

* `getPhaseActions`
* `onPhaseStart`
* maybe `onPhaseEnd`
* phase metadata in `rules.metadata.json`
* runtime owns phase state, rules only propose valid phase actions/consequences.

Do not put phase mutation directly in rules hook. Rules says "phase start causes these proposed events"; runtime commits.

#### Hidden info later

Add:

* `getPlayerView(context, actorId)`
* visibility metadata in `rules.metadata.json`
* private event visibility flags later.

Important invariant:

```text
GameState is authoritative.
PlayerView is derived.
Client never receives hidden full state in server future.
```

#### Response windows later

Add:

* `getResponseWindows(context, eventOrAction)`
* `validateResponseAction`
* `resolveResponse`

Recommended model:

```text
committed event -> rules detect response window -> runtime creates pending window state -> eligible actor submits response action -> same action pipeline
```

Do not make response windows an ad hoc UI modal that bypasses state.

#### Server-authoritative future

The current interface should be server-compatible from day one:

```text
client input -> Action request
server/runtime -> validateAction
rules -> resolveAction proposed events
server/runtime -> commit events
server -> sends PlayerView
client -> renders
```

Even before server exists, local runtime should behave as if it is the authority. This keeps migration to online rooms realistic later. ([GitHub][8])

### Boundary Risks

1. **Letting rules mutate `GameState` directly.** This destroys replay, undo, event log, sync and debugging.

2. **Letting runtime hardcode Sword of Rome-like rules.** Then the platform becomes one game, not an authoring tool. The architecture explicitly says Sword of Rome-like module must stay in Layer 4 and not leak into lower layers. ([GitHub][6])

3. **Skipping `resolveAction`.** Validation alone is not enough; complex module-specific consequences need a clean place to become proposed events.

4. **Making hooks call Phaser/React.** Hooks should know game state and module content, not renderer objects.

5. **Confusing allowed-actions UI hints with actual authority.** `getAllowedActions` helps UI, but final authority is validation + resolution + commit.

6. **Creating two mutation paths: manual editor mutation and rules mutation.** Even manual sandbox actions should produce events.

7. **Putting executable rules in `rules.metadata.json`.** Metadata should describe phases/action kinds/automation level, not become a hidden scripting language. The domain schema contract says executable rules are not stored inline in metadata. ([GitHub][12])

8. **Designing strict enforcement too early.** For Table Sandbox 0.1, manual/assisted is enough. Strict should come after state, events, save/load and generic table behavior are stable.

### Recommended Next Planning Artifact

Recommended next artifact: **`action_event_contract.md`**.

Reason: `RulesHooksInterface` depends on the exact shape of `Action`, `Event`, `ValidationResult`, `ResolveResult`, event ordering, reducer behavior and log semantics. Without this, hook signatures will look clean but implementation will drift.

Suggested contents:

```text
1. Action envelope
2. Event envelope
3. ValidationResult
4. ResolveResult
5. Manual action types for Table Sandbox 0.1
6. Event types for Table Sandbox 0.1
7. Runtime reducer rules
8. Event ordering and seq policy
9. Error/warning/override policy by automation level
10. Examples:
    - move piece
    - create piece
    - change control
    - create space
    - create connection
```

After that, do **`first_milestone_runtime_skeleton.md`** or equivalent implementation breakdown for Table Sandbox 0.1.

### Not available / not verified

* No local filesystem, git status, tests, runtime, or actual implementation were inspected.
* README says the repo mainly contains project context/workflow/canon/reference materials and that first product-code block is not yet implemented as a working app. ([GitHub][9])
* Exact TypeScript signatures are not verified and should be decided later.
* Exact reducer implementation is not available.
* Exact stack model, save compatibility policy and module dependency policy remain open in the published planning docs. ([GitHub][12])
* Exact Sword of Rome-like rule details were not needed for this boundary contract.

## Candidate Navigation Entry

V1-20260523-062449: RulesHooksInterface second opinion for the universal 2D counter-based wargame authoring platform. Recommendation: use a hybrid resolution model where module rules return proposed events through `resolveAction`, but runtime remains the sole committer that applies events, mutates `GameState`, appends the log, persists saves, and triggers render; Table Sandbox 0.1 should stay manual-to-assisted, not strict.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_brief.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/canon/context/sword_of_rome_web_project_context.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md "raw.githubusercontent.com"
