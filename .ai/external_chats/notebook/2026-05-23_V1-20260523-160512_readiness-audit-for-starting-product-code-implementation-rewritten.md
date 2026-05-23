# Notebook Entry

- External Question ID: `V1-20260523-160512`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-160512_readiness-audit-for-starting-product-code-implementation-rewritten.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md`
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
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://docs.phaser.io/phaser/getting-started/installation`
- `https://vite.dev/guide/`
- `https://react.dev/learn/build-a-react-app-from-scratch`

## Candidate Navigation Entry

Topic: Readiness audit for starting product-code implementation, rewritten with technical bootstrap included under the same ID
Summary: Verdict: broad implementation should not start yet, but a narrow `Table Sandbox 0.1` coding slice can start after short closure: set up Vite + React + TypeScript + Phaser with `GameState` outside Phaser, create tiny canonical fixtures, freeze `move_piece_requested -> piece_moved`, write acceptance checks, and decide whether the existing prototype is reference-only or product-code starting point.

## Raw Response

## External Question ID

V1-20260523-160512

## Context Readback

* Uploaded prompt / `Вставленный текст(16).txt` — fully read. 
* `external_chat_rules.md` — fully read. ([GitHub][1])
* Central `repo_navigation.md` — fully read. ([GitHub][2])
* Project `.ai/repo_navigation.md` — fully read. ([GitHub][3])
* Project `architecture.md` — fully read. ([GitHub][4])
* Project `decisions.md` — partially read; opened, but tool returned minimal/no readable body lines. ([GitHub][5])
* Project `project_state.md` — partially read; opened, but tool returned minimal/no readable body lines. ([GitHub][6])
* `domain_schemas_contract.md` — fully read. ([GitHub][7])
* `minimal_canonical_file_schemas.md` — fully read. ([GitHub][8])
* `rules_hooks_interface.md` — fully read. ([GitHub][9])
* `action_event_contract.md` — fully read. ([GitHub][10])
* `first_milestone_runtime_skeleton.md` — opened, but content returned with minimal readable lines, treated as partially read. ([GitHub][11])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][12])
* `first_vertical_slice_spec.md` — fully read. ([GitHub][13])
* `module_authoring_workflow.md` — fully read. ([GitHub][14])
* `module_package_model.md` — fully read. ([GitHub][15])
* `module_product_ux_model.md` — fully read. ([GitHub][16])
* `post_0_1_platform_roadmap.md` — fully read. ([GitHub][17])
* Project `V1_navigation.md` — fully read. ([GitHub][18])
* Official Phaser installation docs — fully read for installation options. ([docs.phaser.io][19])
* Official Vite guide — fully read for scaffolding, templates, dev server and Node requirement. ([vitejs][20])
* Official React "Build a React app from Scratch" page — fully read for React + Vite + TypeScript setup guidance. ([react.dev][21])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require the response to preserve the exact `External Question ID`, give honest `Context Readback`, separate central-doc conclusions from project-specific conclusions and not-verified material, and avoid pretending to have local repo/runtime/test access unless that access was explicitly provided. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation is only for `ai-workflow-core`; it does not authorize claims about the consumer repo unless consumer-project files are explicitly provided. ([GitHub][2])

For this answer, central docs define the answer discipline only. They do not decide whether product code is ready or which technical stack should be installed.

### Confirmed from provided excerpts

## Readiness verdict

**Verdict: `can start only with a narrow coding scope`.**

The project is ready to start **only a narrow first product-code slice**, not broad implementation of the whole product.

The safe first coding target is:

```text
Table Sandbox 0.1 — first vertical slice:

technical bootstrap
→ canonical fixture files
→ load sample module/scenario
→ bootstrap GameState
→ Action/Event dispatcher
→ permissive RulesHooks
→ render board/spaces/piece
→ move one piece between two spaces
→ commit piece_moved event
→ update GameState
→ append event log
→ render from GameState
→ basic save/load snapshot
```

Important amendment compared to the earlier readiness answer: before the first runtime slice, there must be a **Technical Bootstrap** step:

```text
Vite + React + TypeScript + Phaser
```

The project architecture already says the product is a browser-based authoring tool / editor / tabletop sandbox, not a hardcoded Sword of Rome game, and it says source of truth must stay outside Phaser objects. ([GitHub][4])

So Phaser should be introduced as a **visual table / rendering / input layer**, not as the owner of game state.

---

## Already good enough

The following foundations are good enough to start a narrow implementation phase.

### 1. Product framing is clear

The project is a reusable browser-based authoring/runtime platform for 2D counter-based wargames. Sword of Rome-like material is a test/reference module, not the source of universal architecture. ([GitHub][4])

### 2. Product layers are clear

The accepted product architecture has four layers:

```text
Layer 1 — Core Infrastructure + Project/Data Model
Layer 2 — Universal Authoring / Editor Capabilities
Layer 3 — Universal Runtime / Play Sandbox
Layer 4 — Module Package
```

Layer 1 includes schemas, ids, versioning, JSON formats and the source-of-truth data model; Layer 3 includes `GameState`, action/event pipeline and play-mode shell; Layer 4 contains module content and module rules/hooks. ([GitHub][4])

### 3. Canonical split is clear

The docs already separate:

```text
definitions
runtime state
module rules
```

They also separate `PieceDefinition` from `PieceInstance`, `MapDefinition` from runtime state, `ScenarioDefinition` from save state, and `Action` from `Event`. ([GitHub][7])

### 4. First file set is clear enough

The first pass uses:

```text
project.json
module.json
map.json
scenario.<scenarioId>.json
rules.metadata.json
savegame.json
```

The schema planning explicitly says what each file should and should not contain. For example, `map.json` must not contain current piece positions, `scenario.json` must not contain post-start event history, and `savegame.json` must not redefine canonical definitions. ([GitHub][8])

### 5. Action/Event backbone is clear enough

The runtime contract says:

```text
Action = request / intention
Event = committed fact
```

Only runtime commits events, mutates authoritative `GameState`, persists save state and triggers render from committed state. ([GitHub][10])

### 6. Rules boundary is clear enough

The rules contract is:

```text
runtime asks
module rules answer
runtime applies and logs
```

Rules hooks may read `GameState` and module content, but must not mutate Phaser directly, own save files, or silently mutate authoritative state. ([GitHub][9])

### 7. `Table Sandbox 0.1` scope is clear enough

The milestone plan says `0.1` should prove a minimal universal tabletop sandbox: canonical files load/save, runtime owns `GameState`, actions become events through a visible pipeline, rules stay permissive, and one tiny end-to-end slice proves the architecture. ([GitHub][12])

---

## Missing item added: Technical Bootstrap

The original readiness answer missed a practical pre-code step: **technical setup of the browser app and visual engine**.

Before writing the first product slice, add:

```text
0. Technical Bootstrap
```

Purpose:

```text
Create a minimal working browser app shell where:

React hosts the editor/workspace UI,
Phaser hosts the interactive table/canvas,
GameState remains outside Phaser as the source of truth.
```

This is not "build the whole game engine."
This is only the technical foundation needed before the first `Table Sandbox 0.1` vertical slice.

---

## Recommended technical stack

For the first product-code block, use:

```text
Node.js
npm
Vite
React
TypeScript
Phaser
```

### Why this stack

**Vite** gives local development server and build setup. Vite officially supports scaffolding with `npm create vite@latest` and has a `react-ts` template. It currently requires Node.js `20.19+` or `22.12+`. ([vitejs][20])

**React** should host the product/editor shell: panels, buttons, lists, inspectors, validation panel and event log. React's official documentation shows Vite + React + TypeScript setup with:

```text
npm create vite@latest my-app -- --template react-ts
```

([react.dev][21])

**Phaser** should render and handle input for the visual table: map, spaces, pieces, dragging, panning and zooming. Phaser official docs list `npm install phaser` for npm installation, and also provide `npm create @phaserjs/game@latest` for Phaser's own templates. ([docs.phaser.io][19])

For this project, the safer default is:

```text
Use Vite + React + TypeScript as the app shell.
Install Phaser inside that app as a dependency.
Do not start from a pure Phaser-only game template unless local review explicitly decides that.
```

Reason: this product is not just a Phaser game. It is an authoring/runtime platform with editor panels, module files, validation, package workflow and playtest preview.

---

## Required local environment preflight

Before installation, the coding agent should check:

```text
node --version
npm --version
```

If the local Node.js version is below the current Vite requirement, Node must be updated before debugging the app setup. Vite's guide lists Node.js `20.19+` or `22.12+` as required. ([vitejs][20])

---

## Correct role split: React / Phaser / Runtime

The technical stack must preserve the accepted architecture.

```text
React       = product/editor shell
Phaser      = visual table / canvas interaction
Runtime     = source-of-truth GameState and Action/Event pipeline
RulesHooks  = module-specific rules boundary
Persistence = JSON load/save
```

### React owns

```text
Module workspace shell
Top toolbar
Left navigation
Right inspector
Validation panel
Event log panel
File/package status
Play Sandbox controls
```

### Phaser owns

```text
Canvas/table rendering
Map image rendering
Space markers rendering
Piece sprites rendering
Pointer input
Drag/drop gesture capture
Camera pan/zoom
Selection visuals
```

### Runtime owns

```text
GameState
Action dispatch
Validation result
Resolve result
Committed events
Reducer
Event log
Save/load state
```

### Phaser must not own

```text
authoritative piece location
canonical GameState
event log
savegame truth
rules decisions
module file data
```

This matters because the accepted Action/Event contract says actions do not change `GameState`, uncommitted events do not change `GameState`, and only committed events change `GameState`. ([GitHub][10])

---

## Updated true blockers before code

There are **no remaining large architectural blockers** for a narrow first implementation slice.

But there are several **short pre-code closure blockers**.

### 1. Technical bootstrap decision

**Why this is a gap:**
Without deciding where React, Phaser and the runtime live, the first vertical slice has no technical home.

**Blocking level:**
Blocking before first product-code slice.

**What to define:**

```text
First app shell = Vite + React + TypeScript.
Phaser is installed as rendering/input dependency.
GameState remains outside Phaser.
```

**Closure type:**
Short decision note.

---

### 2. First product-code block brief

**Why this is a gap:**
The planning docs are strong, but an implementation agent still needs one compact brief saying exactly what to build first and what not to build.

**Blocking level:**
Blocking for clean coding start.

**What to define:**

```text
Goal
Input files
Minimal sample data
Allowed actions/events
Acceptance checks
Non-goals
Do-not-cross boundaries
Technical stack
```

**Closure type:**
Lightweight spec, not more architecture.

---

### 3. Tiny canonical fixture files

**Why this is a gap:**
The runtime needs real sample data to load and round-trip.

**Blocking level:**
Blocking for the first loader/runtime slice.

**What to define:**

```text
project.json
module.json
map.json
scenario.basic.json
rules.metadata.json
savegame.empty.json
```

With a tiny sample:

```text
2–3 spaces
1–2 connections
1–2 factions
1–3 piece definitions
1–3 piece instances
manual phase
move_piece_requested
piece_moved
```

The table milestone plan says canonical sample files must come before stable runtime state and Action/Event work. ([GitHub][12])

---

### 4. Fixed first action/event pair

**Why this is a gap:**
The first slice depends on a concrete action and event.

**Blocking level:**
Blocking for the first runtime slice.

**What to define:**

```text
Action: move_piece_requested
Event:  piece_moved
Reducer effect: PieceInstance.locationId changes
```

This is exactly the first vertical slice described in the planning docs. ([GitHub][13])

---

### 5. Acceptance checklist

**Why this is a gap:**
The coding phase needs "done means done" criteria.

**Blocking level:**
Blocking for avoiding drift.

**What to define:**

```text
- app starts locally
- React shell renders
- Phaser canvas renders
- sample module loads
- initial GameState is created
- one piece appears at location A
- move action is created
- validation allows it
- resolveAction returns piece_moved
- runtime commits event with seq
- reducer changes locationId
- event log contains the event
- renderer displays piece at location B
- save/load preserves state
```

**Closure type:**
Acceptance checklist.

---

### 6. Prototype reuse decision

**Why this is a gap:**
There is already a table/map editor prototype, but the project navigation warns not to confuse planned architecture and prototype/local-only paths with implemented product code or public canon. ([GitHub][3])

**Blocking level:**
Blocking if implementation starts by modifying that prototype.
Not blocking if the first slice starts as a clean product-code skeleton.

**What to define:**

```text
Use existing prototype as:
A. reference only;
B. source to adapt/promote;
C. separate prototype kept isolated.
```

**Recommendation:**
Treat the prototype as **reference only** until local Codex/code review confirms it is safe to promote into product code.

---

## Technical Bootstrap acceptance checks

The technical bootstrap is done when:

```text
1. Supported Node.js version is available.
2. Dependencies install successfully.
3. Local dev server starts.
4. React shell is visible.
5. Phaser scene mounts inside the React app.
6. Phaser draws a blank table or simple grid.
7. React can show a placeholder event log.
8. Placeholder GameState exists outside Phaser.
9. Phaser can receive state-like data and redraw.
10. Phaser can emit a simple pointer/click/drag notification upward.
```

Only after this should implementation move into real canonical files and the Action/Event runtime.

---

## Updated implementation order

The first coding sequence should be:

```text
0. Technical Bootstrap
1. First product-code block brief
2. Tiny canonical fixture files
3. Load project/module/map/scenario/rules metadata
4. Bootstrap initial GameState
5. Mount React shell
6. Mount Phaser table inside shell
7. Render spaces and one piece from GameState
8. Convert drag/drop into move_piece_requested Action
9. Validate permissively through RulesHooks
10. Resolve into piece_moved proposed Event
11. Runtime commits Event
12. Reducer updates GameState
13. Event log updates
14. Phaser redraws from GameState
15. Save/load basic snapshot
```

This preserves the accepted order: canonical files → `GameState` bootstrap → Action/Event backbone → permissive RulesHooks → first thin vertical slice. ([GitHub][12])

---

## Safest initial coding scope

The first product-code scope should be:

```text
Build the first Table Sandbox 0.1 vertical slice on top of a
Vite + React + TypeScript + Phaser technical shell.
```

### Technical part

```text
- verify supported Node/npm
- create or prepare Vite React TypeScript app
- install Phaser
- run local dev server
- mount Phaser scene inside React shell
- keep GameState outside Phaser
```

### Runtime part

```text
- load tiny canonical fixture files
- create initial GameState
- render spaces and one piece
- drag one piece from one space to another
- emit move_piece_requested
- validate permissively
- resolve to piece_moved
- commit event
- update GameState
- append event log
- redraw from GameState
- save/load basic snapshot
```

### Non-goals

Do not include:

```text
full Sword of Rome rules
combat
cards/decks
strict legality
hidden information
online multiplayer
server authority
AI
full editor UX
mature package import/export
migration engine
advanced stack model
polished UI
```

The milestone plan explicitly defers strict legality, combat, cards, hidden info, online sync, AI, advanced stack model, module dependencies and migration engine. ([GitHub][12])

---

## Important but non-blocking gaps

These should be tracked, but they should not stop the first narrow coding slice.

### 1. Exact TypeScript/Zod schemas

Eventually the human-readable file contracts need real schemas. But the docs explicitly say the schema planning is not yet TypeScript/Zod implementation. ([GitHub][8])

**Blocking level:**
Not blocking for first narrow slice if fixtures are small and validation is lightweight.

### 2. Exact full product-code folder layout

A minimal product-code home must be chosen before coding, but the full final folder layout can evolve.

**Blocking level:**
Partly blocking only as a local setup decision.

### 3. Authoring undo/redo

Authoring undo/redo is important later, but the first vertical slice can proceed without full history tooling. Module authoring workflow marks authoring transaction log and undo/redo separation as still open. ([GitHub][14])

### 4. Runtime undo/replay

Action/Event enables replay and undo later, but full runtime undo is not needed for the first move-piece slice.

### 5. Save granularity

For `0.1`, a snapshot plus event log is enough. More advanced replay/action-history policy can wait.

### 6. Module dependencies

Module dependencies are still open and not needed for `0.1`. ([GitHub][7])

### 7. Mature package import/export

The mature package model deliberately leaves exact package importer/exporter behavior, content hashes and migration/versioning policy open. ([GitHub][15])

---

## Later clarifications that can happen during implementation

These can safely wait:

```text
exact UI chrome
polished Russian labels
visual styling
exact inspector layout
future cards/decks/documents
advanced stack model
strict rules
response windows
hidden information
online/server-authoritative runtime
AI
package publishing
marketplace/module library
full migration framework
```

The post-0.1 roadmap deliberately defers full strict rules, full Sword of Rome rules, combat, hidden information, online multiplayer, AI, full migration engine and advanced stack model until after stable platform foundations. ([GitHub][17])

---

## Contradictions / weak boundaries check

### 1. Stack model: open vs safe default

Older docs list stack model as open, but later planning defines the `0.1` safe default: stack is derived from shared `locationId`, not a first-class `Stack`. ([GitHub][7])

**Audit result:**
Not a contradiction. For first code, use the `0.1` safe default.

---

### 2. Save compatibility: open vs 0.1 policy

The domain contract says save compatibility needed explicit decision, and the minimal schema doc gives the `0.1` safe default: compatible saves load, minor safe mismatches warn, structural incompatibility blocks, migration-required blocks. ([GitHub][7])

**Audit result:**
Not a contradiction. Implement only the `0.1` policy.

---

### 3. Event derivation boundary

The rules hook doc still lists event derivation as an open question, but recommends rules return proposed events and runtime commits them. The action/event contract also uses that model. ([GitHub][9])

**Audit result:**
Weak wording, but enough for `0.1`. Close with a short decision note:

```text
resolveAction returns proposed events;
runtime is sole committer.
```

---

### 4. Authoring changes vs runtime Action/Event

Runtime changes must go through Action/Event. Authoring changes may be separate editor transactions. The authoring workflow separates authoring mode from play sandbox mode and says the same gesture must not silently switch meaning between modes. ([GitHub][14])

**Audit result:**
Not blocking for first runtime slice. Avoid full authoring complexity at first.

---

### 5. Prototype vs product-code status

Project-specific navigation warns that planned architecture is not the same as implemented product code, and local-only paths/prototypes are not automatically public canon. ([GitHub][3])

**Audit result:**
This is a practical risk. Make a prototype reuse decision before coding.

---

## Updated pre-code closure plan

Do **not** add many more large planning docs. Do these steps only.

### Step 1 — Decide technical bootstrap

```text
Vite + React + TypeScript app shell.
Phaser installed inside it.
GameState outside Phaser.
```

### Step 2 — Verify local environment

```text
node --version
npm --version
npm install
npm run dev
```

Use a Node version compatible with current Vite requirements. ([vitejs][20])

### Step 3 — Decide prototype reuse

Choose one:

```text
reference only
adapt/promote
clean skeleton
```

Recommended: reference only until local code review says otherwise.

### Step 4 — Write `first_product_code_block.md`

It should include:

```text
technical stack
goal
scope
fixtures
first action/event
acceptance checks
non-goals
architecture boundaries
```

### Step 5 — Create tiny canonical fixtures

```text
project.json
module.json
map.json
scenario.basic.json
rules.metadata.json
savegame.empty.json
```

### Step 6 — Freeze first action/event

```text
move_piece_requested -> piece_moved
```

### Step 7 — Start coding the first vertical slice

```text
load fixture module
→ create GameState
→ render one piece
→ drag piece
→ Action
→ Event
→ GameState update
→ event log
→ render refresh
→ save/load
```

After these seven steps, planning should stop and implementation should begin.

---

## Start-coding threshold

The project is ready to start the first product-code implementation when all of this is true:

```text
1. Supported Node.js version is available.
2. Vite + React + TypeScript app starts locally.
3. Phaser is installed and can render a blank scene inside React.
4. GameState is explicitly outside Phaser.
5. First product-code block brief exists.
6. Tiny canonical fixture files exist.
7. move_piece_requested and piece_moved are fixed as the first action/event.
8. Acceptance checklist exists.
9. Prototype reuse decision is explicit.
10. Non-goals are visible to the coding agent.
```

At that point, more planning should stop. The next useful information will come from implementation feedback.

---

## Final audit answer

**Can start broadly?**
No.

**Not yet at all?**
Also no. The architectural base is already strong enough.

**Best answer:**
Can start **only with a narrow coding scope**, after a short technical bootstrap.

The first useful coding target is:

```text
Technical Bootstrap:
Vite + React + TypeScript + Phaser
with GameState outside Phaser.

Then Table Sandbox 0.1 first slice:
load module/scenario
→ create GameState
→ render board/spaces/piece
→ drag piece
→ move_piece_requested
→ permissive validation
→ piece_moved
→ runtime commit
→ reducer updates GameState
→ event log
→ render from GameState
→ save/load.
```

Most important rule:

```text
Phaser renders and captures input.
Runtime owns GameState.
Actions and events mutate state.
React hosts the editor/workspace.
```

### Not available / not verified

* Local repository, branch, git status, package files, build scripts, tests and runtime were not inspected.
* It is not verified whether Node.js, npm, Vite, React, TypeScript or Phaser are already installed locally.
* It is not verified whether a product-code skeleton already exists locally.
* It is not verified whether the existing table/map prototype should be reused as product-code.
* Exact framework folder paths are not fixed here.
* Exact TypeScript/Zod schemas are not fixed here.
* Exact React/Phaser integration implementation is not specified here.
* Exact local acceptance test setup is not available.
* This answer is a planning-only readiness audit, not an accepted local implementation decision.

## Candidate Navigation Entry

V1-20260523-160512: Readiness audit for starting product-code implementation, rewritten with technical bootstrap included under the same ID. Verdict: broad implementation should not start yet, but a narrow `Table Sandbox 0.1` coding slice can start after short closure: set up Vite + React + TypeScript + Phaser with `GameState` outside Phaser, create tiny canonical fixtures, freeze `move_piece_requested -> piece_moved`, write acceptance checks, and decide whether the existing prototype is reference-only or product-code starting point.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_package_model.md
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_product_ux_model.md
[17]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md
[18]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md
[19]: https://docs.phaser.io/phaser/getting-started/installation
[20]: https://vite.dev/guide/
[21]: https://react.dev/learn/build-a-react-app-from-scratch
