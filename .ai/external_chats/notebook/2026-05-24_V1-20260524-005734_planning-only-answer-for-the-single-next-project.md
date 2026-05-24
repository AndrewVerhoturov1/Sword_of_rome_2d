# Notebook Entry

- External Question ID: `V1-20260524-005734`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-24_V1-20260524-005734_planning-only-answer-for-the-single-next-project.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_package_model.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_product_ux_model.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/prototype_integration_mapping.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/pre_code_closure_and_first_execution_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`

## Candidate Navigation Entry

Topic: Planning-only answer for the single next project step
Summary: Recommendation: first create and accept `first_product_code_block.md`, a compact implementation brief that freezes the narrow `Table Sandbox 0.1` target, technical shell, tiny fixtures, `move_piece_requested -> piece_moved`, acceptance checklist, prototype role, and non-goals before any coding begins.

## Raw Response

## External Question ID

V1-20260524-005734

## Context Readback

* Uploaded prompt / `Вставленный текст(19).txt` — fully read. 
* `external_chat_rules.md` — fully read. ([GitHub][1])
* Central `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — partially read; opened, but tool returned minimal/no readable body lines. ([GitHub][4])
* Project `project_state.md` — partially read; opened, but tool returned minimal/no readable body lines. ([GitHub][5])
* Project `.ai/repo_navigation.md` — fully read. ([GitHub][6])
* `domain_schemas_contract.md` — fully read. ([GitHub][7])
* `minimal_canonical_file_schemas.md` — fully read. ([GitHub][8])
* `rules_hooks_interface.md` — fully read. ([GitHub][9])
* `action_event_contract.md` — fully read. ([GitHub][10])
* `first_milestone_runtime_skeleton.md` — fully read. ([GitHub][11])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][12])
* `first_vertical_slice_spec.md` — fully read. ([GitHub][13])
* `module_authoring_workflow.md` — fully read. ([GitHub][14])
* `module_package_model.md` — fully read. ([GitHub][15])
* `module_product_ux_model.md` — fully read. ([GitHub][16])
* `post_0_1_platform_roadmap.md` — fully read. ([GitHub][17])
* `prototype_integration_mapping.md` — fully read. ([GitHub][18])
* `pre_code_closure_and_first_execution_plan.md` — fully read. ([GitHub][19])
* Project `V1_navigation.md` — fully read. No additional notebook entries were opened; the index summaries were sufficient for this narrow next-step question. ([GitHub][20])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

`external_chat_rules.md` requires the answer to preserve the exact `External Question ID`, include `Context Readback`, identify provider/model, separate central-doc conclusions from project-specific/provided-context conclusions, and include `Candidate Navigation Entry`. It also requires honest readback and prohibits claiming local repo, shell, tests, build, runtime, git state, or local implementation access unless that access was actually provided. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation is only for `ai-workflow-core` and does not authorize claims about the consumer project unless consumer-project files are explicitly provided in the prompt. ([GitHub][2])

For this answer, central docs define the response discipline only. The actual chosen next step comes from the project-specific planning canon and the uploaded prompt. 

### Confirmed from provided excerpts

# Chosen First Step

The next step project should perform first is:

```text
Create and accept `first_product_code_block.md`.
```

This should be a **single compact execution brief** for the first product-code block. It should not be another architecture document, not a new roadmap, and not a React/Phaser implementation spec.

Its job is to freeze the narrowest safe coding target before any real product-code work starts.

The already accepted bridge doc says the nearest step is to create and accept a tiny first product-code brief for the narrowest `Table Sandbox 0.1` slice, locking the runtime shell direction, tiny fixture set, first action/event pair, and first observable acceptance checklist. ([GitHub][19])

---

# Why This Comes First

This step comes before technical bootstrap, fixture creation, Phaser setup, runtime coding, and prototype migration because the project's main risk now is **implementation drift**, not lack of architecture.

Without this brief, the first coding agent may incorrectly start with one of these:

```text
- refactor the whole external prototype;
- build a broad map editor first;
- make Phaser the source of truth;
- hardcode Sword of Rome-like behavior;
- implement cards/combat/rules too early;
- skip canonical fixtures;
- bypass the Action/Event pipeline;
- blur authoring and runtime modes.
```

The planning canon already says the external prototype should not become the starting architecture for `0.1`; it should remain a UX reference for future map editing behavior while the first coding slice stays anchored in canonical data and runtime pipeline. ([GitHub][12])

So the first step must be an execution-control artifact:

```text
a small document that tells the coding agent exactly what to build first,
what not to build,
and what counts as done.
```

This is the right first step because `Table Sandbox 0.1` already has an accepted dependency order: canonical sample files → `GameState` bootstrap → Action/Event backbone → permissive RulesHooks → first thin vertical slice. The first brief is the handoff that prevents that order from being lost during implementation. ([GitHub][12])

---

# Exact Scope

## Artifact name

Recommended file:

```text
.ai/plans/implementation/first_product_code_block.md
```

Acceptable alternative:

```text
.ai/handoffs/first_product_code_block.md
```

Preferred location is `.ai/plans/implementation/` because this is an implementation planning artifact, not a Kilo report or runtime result.

## Purpose

The artifact should answer exactly:

```text
1. What is the first coding block?
2. What technical shell is used?
3. What tiny fixture files are required?
4. What is the first Action?
5. What is the first Event?
6. What must the first slice prove?
7. What is explicitly out of scope?
8. How should the existing prototype be treated?
```

## Output

A short, practical Markdown file that can be handed directly to Codex/Kilo as the first implementation brief.

## It should include

```text
- status;
- goal;
- technical shell decision;
- prototype usage decision;
- product-code starting boundary;
- tiny fixture set;
- first action;
- first event;
- runtime rule;
- acceptance checklist;
- explicit non-goals;
- stop condition;
- immediate next step after completion.
```

## It should not include

```text
- new architecture;
- full roadmap;
- detailed React code;
- detailed Phaser code;
- final folder-by-folder implementation design;
- mature package importer/exporter design;
- full Sword of Rome-like rules;
- card/deck subsystem;
- combat/scoring;
- hidden information;
- online play;
- AI;
- migration framework.
```

The post-`0.1` roadmap explicitly warns that the safe branch is platform-first, while the risky branch is to jump from the move-piece slice into full Sword of Rome rules, cards, combat, scoring, and then try to generalize later. ([GitHub][17])

---

# Execution Breakdown

## Step 1 — Create the file

Create:

```text
.ai/plans/implementation/first_product_code_block.md
```

If the folder does not exist, create it.

This should be the one file the coding agent reads immediately before beginning product-code work.

---

## Step 2 — Add status and intent

Add:

```markdown
# First Product Code Block

## Status

Draft for implementation handoff.

## Intent

This document freezes the first narrow product-code block for Table Sandbox 0.1.
It does not introduce new architecture.
It translates the accepted planning canon into one executable implementation target.
```

The wording matters. It should say clearly that this is a **freeze/brief**, not a new design pass.

---

## Step 3 — Define the goal

Add:

```markdown
## Goal

Build the first narrow Table Sandbox 0.1 product-code slice.

The goal is not to build the full product, full game, full authoring workspace, or full Sword of Rome-like module.

The goal is to prove the smallest working product foundation:

tiny canonical fixture module
→ initial GameState
→ render board/spaces/piece
→ move_piece_requested Action
→ permissive validation
→ piece_moved Event
→ reducer updates GameState
→ event log updates
→ renderer redraws from GameState
→ basic save/load snapshot.
```

This goal is directly aligned with the first vertical slice spec: one piece moves from one space to another through the full canonical pipeline. ([GitHub][13])

---

## Step 4 — Freeze the technical shell decision

Add:

```markdown
## Technical Shell Decision

Use:

- Vite
- React
- TypeScript
- Phaser

Role split:

- React owns the application/editor shell.
- Phaser owns visual table rendering and pointer input.
- Runtime owns GameState, Action/Event pipeline, reducer and event log.
- RulesHooks answer runtime questions; they do not own state.
- Phaser must not be the source of truth.
```

This is necessary because the project architecture says Layer 1 must keep serializable source of truth outside Phaser objects. ([GitHub][3])

The brief should also include the hard boundary:

```markdown
Renderer input may request actions.
Renderer objects must not directly mutate authoritative GameState.
```

This matches the Action/Event contract: only committed events change `GameState`, and renderer must never become source of truth. ([GitHub][10])

---

## Step 5 — Freeze the prototype decision

Add:

```markdown
## Prototype Decision

The existing `table-map-editor-canvas-local-fixed` prototype is reference + selective donor.

Use it for ideas:

- layers;
- spaces;
- connections;
- curved paths;
- zones;
- inspector behavior;
- validation ideas;
- map.json export ideas;
- Russian UI behavior.

Do not copy it wholesale as product architecture.
Do not treat its single-file React structure as the product foundation.
Do not treat its local state or project export as canonical runtime/package format.
```

This is required because the prototype integration mapping classifies the prototype as reference prototype and selective donor for the future Map Editor surface, not as direct product-code foundation or substitute for canonical architecture. ([GitHub][18])

---

## Step 6 — Define the product-code starting boundary

Add:

```markdown
## Product-Code Starting Boundary

Start a new product-code skeleton clearly separated from old prototypes.

The first implementation block may create the smallest app shell needed for the slice, but must not migrate the whole prototype.

The product code should keep these responsibilities separate:

- runtime;
- renderer/table surface;
- fixtures;
- persistence;
- validation;
- rules hooks shim;
- event log.
```

This section avoids the common mistake of starting inside the prototype and slowly turning it into the product without boundary control.

The project-specific navigation warns not to confuse planned architecture and local/prototype layers with implemented product code or public canon. ([GitHub][6])

---

## Step 7 — Define the tiny fixture set

Add:

```markdown
## Tiny Fixture Set

Create or specify the smallest canonical fixture set:

- project.json
- module.json
- map.json
- scenario.basic.json
- rules.metadata.json
- savegame.empty.json

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
```

Then add file role rules:

```markdown
File role rules:

- project.json is workspace index.
- module.json is module manifest.
- map.json is board topology.
- scenario.basic.json is initial setup.
- rules.metadata.json is declarative rules capability metadata.
- savegame.empty.json is runtime snapshot state, not canonical module content.
```

The minimal canonical schemas document requires exactly this separation: `project.json`, `module.json`, `map.json`, `scenario.json`, `rules.metadata.json`, and `savegame.json` must not mix roles. ([GitHub][8])

---

## Step 8 — Freeze the first action

Add:

```markdown
## First Action

Type:

`move_piece_requested`

Meaning:

The user/system requests moving one piece from one map location to another.

Minimum payload:

- pieceId
- fromLocationId
- toLocationId
```

This is not the event yet. It is only a request.

---

## Step 9 — Freeze the first event

Add:

```markdown
## First Event

Type:

`piece_moved`

Meaning:

The runtime has accepted and committed the move.

Minimum payload:

- pieceId
- fromLocationId
- toLocationId
```

Then add:

```markdown
Action = request / intention.
Event = committed fact.
```

The Action/Event contract explicitly defines this distinction and uses `move_piece_requested` and `piece_moved` as the first move example. ([GitHub][10])

---

## Step 10 — Define the runtime rule

Add:

```markdown
## Runtime Rule

No direct state mutation from renderer, Phaser scene, UI component, or rules hook.

Correct flow:

Phaser/input
→ Runtime creates Action
→ RulesHooks validate/resolve
→ Runtime commits Event
→ Reducer updates GameState
→ Event log appends
→ Renderer redraws from GameState
```

The rules hooks contract says runtime asks, module rules answer, and runtime applies/logs; hooks must not mutate Phaser directly or silently mutate authoritative state outside the runtime pipeline. ([GitHub][9])

---

## Step 11 — Write the acceptance checklist

Add:

```markdown
## Acceptance Checklist

The first product-code block is done only when:

- app starts locally;
- React shell renders;
- Phaser scene/table area renders inside the shell;
- tiny fixture module loads;
- initial GameState is created from fixture data;
- spaces render;
- one piece renders at location A;
- user can request moving the piece to location B;
- runtime creates move_piece_requested;
- validation allows the action;
- resolution returns piece_moved;
- runtime commits the event;
- committed event receives event sequence/order;
- event log displays the committed event;
- reducer changes piece location in GameState;
- renderer redraws the piece at location B;
- basic save/load preserves GameState and event log;
- no Phaser object is authoritative source of truth;
- no Sword of Rome-specific lower-layer logic is introduced.
```

This checklist must be observable. It is not enough that "the UI seems to move a piece." The event log and `GameState` update must prove that the correct pipeline happened.

The first vertical slice spec says the slice is valid only if validation, resolution, commit, reducer, log, and render all happen visibly through the canonical `Action -> Event -> GameState` pipeline. ([GitHub][13])

---

## Step 12 — Write explicit non-goals

Add:

```markdown
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
```

This is necessary because the `Table Sandbox 0.1` milestone explicitly defers full Sword of Rome rules, combat, strict legality, hidden info, online sync, AI, advanced stack model, module dependencies, and migration engine. ([GitHub][12])

---

## Step 13 — Define the stop condition

Add:

```markdown
## Stop Condition

Stop this implementation block when one piece can move from one space to another through:

Action
→ Event
→ GameState
→ event log
→ render
→ save/load.

After that, create a short implementation report before expanding scope.
```

This prevents scope creep. The first block should stop when the proof is complete, not continue into broad editor expansion.

---

## Step 14 — Define the immediate next step after completion

Add:

```markdown
## Immediate Next Step After This Block

After this block is complete, do not jump to full rules or full editor migration.

Next candidates are, in this order:

1. harden the same first slice;
2. add one more manual action;
3. improve fixture validation;
4. improve save/load boundaries;
5. only then begin controlled Map Editor integration.
```

The accepted bridge doc says immediate post-first-slice work should remain narrow: harden the slice, add one more manual action, improve validation/save-load boundaries, and only then expand toward controlled authoring-side surfaces. ([GitHub][19])

---

# Pitfalls

## Pitfall 1 — Making the brief too big

Bad:

```text
turn first_product_code_block.md into another 30-page architecture document
```

Good:

```text
make it short, direct, implementation-facing
```

The brief should freeze decisions, not reopen them.

---

## Pitfall 2 — Starting with the prototype

Bad:

```text
first task = migrate/refactor the entire map editor prototype
```

Good:

```text
first task = runtime foundation;
prototype = reference + selective donor
```

The prototype integration mapping explicitly says the prototype should not define the runtime shell, package model, canonical file contract, Action/Event backbone, RulesHooks boundary, or product-wide UX model. ([GitHub][18])

---

## Pitfall 3 — Letting Phaser own state

Bad:

```text
sprite position changes;
later we infer GameState from sprite position
```

Good:

```text
input requests action;
runtime commits event;
GameState changes;
Phaser redraws from GameState
```

The domain contract lists as invariants that Phaser is never source of truth and runtime state changes only through the action/event pipeline. ([GitHub][7])

---

## Pitfall 4 — Blurring authoring and runtime

Bad:

```text
same drag gesture sometimes changes map.json,
sometimes scenario.json,
sometimes savegame.json,
without explicit mode
```

Good:

```text
authoring changes definitions/setup;
play sandbox changes runtime state through Action/Event
```

The module authoring workflow explicitly separates authoring mode from Play Sandbox mode and says the same visual gesture must not silently switch meaning between these modes. ([GitHub][14])

---

## Pitfall 5 — Sneaking in Sword of Rome-specific logic

Bad:

```text
make first slice depend on Roman factions, historical phases, or Sword-specific rules
```

Good:

```text
use tiny generic test module first
```

The architecture and roadmap both state that Sword of Rome-like content is a test/reference module and should not shape lower platform layers. ([GitHub][3])

---

# Criteria of Done

This first step is done when `first_product_code_block.md` exists and can be used as the exact handoff for the first coding block.

A reviewer should be able to open the file and answer:

```text
1. What is the first coding target?
2. What technical shell is expected?
3. What fixtures are required?
4. What is the first action?
5. What is the first event?
6. What proves that the slice is done?
7. What is explicitly forbidden for this block?
8. How is the external prototype treated?
9. What happens immediately after this block?
```

The file is not done if:

```text
- it still allows broad implementation;
- it does not mention Vite + React + TypeScript + Phaser;
- it does not freeze move_piece_requested -> piece_moved;
- it does not include acceptance checks;
- it does not define prototype as reference/selective donor;
- it lets Phaser or UI mutate GameState directly;
- it omits explicit non-goals.
```

---

# Immediate Next Step

After `first_product_code_block.md` is created and accepted, the immediate next step is:

```text
Technical Bootstrap:
create the smallest runnable Vite + React + TypeScript + Phaser product shell,
with GameState explicitly outside Phaser.
```

Do not start fixture loading or the move-piece pipeline before the shell boundary is clear.

The accepted pre-code plan says Phase 1 after the brief is technical bootstrap: Vite host app, React shell, TypeScript baseline, Phaser integration boundary, and explicit rule that canonical runtime state lives outside Phaser. ([GitHub][19])

---

# Recommended Minimal Content To Paste Into The File

```markdown
# First Product Code Block

## Status

Draft for implementation handoff.

## Intent

Freeze the first narrow product-code block for Table Sandbox 0.1.
This document does not introduce new architecture.
It translates accepted planning canon into one executable implementation target.

## Goal

Build the first narrow Table Sandbox 0.1 slice:

tiny canonical fixture module
→ initial GameState
→ render board/spaces/piece
→ move_piece_requested Action
→ permissive validation
→ piece_moved Event
→ reducer updates GameState
→ event log updates
→ renderer redraws from GameState
→ basic save/load snapshot.

## Technical Shell Decision

Use:

- Vite
- React
- TypeScript
- Phaser

Role split:

- React owns application/editor shell.
- Phaser owns visual table rendering and pointer input.
- Runtime owns GameState, Action/Event pipeline, reducer and event log.
- RulesHooks answer runtime questions.
- Phaser must not be source of truth.

## Prototype Decision

The existing table-map-editor-canvas-local-fixed prototype is reference + selective donor.

Use it for ideas:

- layers
- spaces
- connections
- curved paths
- zones
- inspector behavior
- validation ideas
- map.json export ideas
- Russian UI behavior

Do not copy it wholesale as product architecture.

## Tiny Fixture Set

Required fixture files:

- project.json
- module.json
- map.json
- scenario.basic.json
- rules.metadata.json
- savegame.empty.json

Minimum content:

- 1 project
- 1 module
- 1 map
- 2 spaces
- 1 connection
- 1 scenario
- 1 or 2 factions
- 1 or 2 piece definitions
- 1 movable piece instance
- permissive/manual rules metadata

## First Action

Type:

move_piece_requested

Payload:

- pieceId
- fromLocationId
- toLocationId

Meaning:

The user/system requests moving one piece from one location to another.

## First Event

Type:

piece_moved

Payload:

- pieceId
- fromLocationId
- toLocationId

Meaning:

The runtime has accepted and committed the move.

## Runtime Rule

No direct state mutation from renderer, Phaser scene, UI component, or rules hook.

Correct flow:

Phaser/input
→ Runtime creates Action
→ RulesHooks validate/resolve
→ Runtime commits Event
→ Reducer updates GameState
→ Event log appends
→ Renderer redraws from GameState

## Acceptance Checklist

Done only when:

- app starts locally
- React shell renders
- Phaser scene/table area renders inside the shell
- tiny fixture module loads
- initial GameState is created from fixture data
- spaces render
- one piece renders at location A
- user can request moving the piece to location B
- runtime creates move_piece_requested
- validation allows the action
- resolution returns piece_moved
- runtime commits the event
- committed event receives sequence/order
- event log displays the committed event
- reducer changes piece location in GameState
- renderer redraws the piece at location B
- basic save/load preserves GameState and event log
- no Phaser object is authoritative source of truth
- no Sword of Rome-specific lower-layer logic is introduced

## Explicit Non-Goals

Do not implement in this block:

- full Sword of Rome rules
- combat
- scoring
- cards/decks
- strict legality
- hidden information
- multiplayer
- online/server authority
- AI
- full module package importer/exporter
- full Map Editor migration
- mature asset system
- full Scenario Editor
- full Pieces/Factions Editor
- advanced stack model
- save migration framework
- polished final UI

## Stop Condition

Stop this implementation block when one piece can move from one space to another through:

Action
→ Event
→ GameState
→ event log
→ render
→ save/load.

After that, create a short implementation report before expanding scope.

## Immediate Next Step After This Block

After this block is complete, do not jump to full rules or full editor migration.

Next candidates are, in this order:

1. harden the same first slice;
2. add one more manual action;
3. improve fixture validation;
4. improve save/load boundaries;
5. only then begin controlled Map Editor integration.
```

### Not available / not verified

* I did not inspect the local repository, local branch, git status, package files, tests, build, runtime, or shell.
* I did not verify whether `.ai/plans/implementation/` already exists locally.
* I did not verify whether `first_product_code_block.md` already exists locally.
* I did not verify whether a product-code skeleton already exists.
* I did not verify whether Node/Vite/React/TypeScript/Phaser are installed locally.
* I did not decide exact local product-code folder path.
* I did not provide React/Phaser code implementation details.
* This is a planning-only next-step breakdown, not an accepted local implementation decision.

## Candidate Navigation Entry

V1-20260524-005734: Planning-only answer for the single next project step. Recommendation: first create and accept `first_product_code_block.md`, a compact implementation brief that freezes the narrow `Table Sandbox 0.1` target, technical shell, tiny fixtures, `move_piece_requested -> piece_moved`, acceptance checklist, prototype role, and non-goals before any coding begins.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_package_model.md "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_product_ux_model.md "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md "raw.githubusercontent.com"
[18]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/prototype_integration_mapping.md "raw.githubusercontent.com"
[19]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/pre_code_closure_and_first_execution_plan.md "raw.githubusercontent.com"
[20]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
