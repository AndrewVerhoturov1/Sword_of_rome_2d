# Notebook Entry

- External Question ID: `V1-20260524-003946`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-24_V1-20260524-003946_detailed-execution-plan-for-moving-from-accepted-planning.md`

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
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`

## Candidate Navigation Entry

Topic: Detailed execution plan for moving from accepted planning canon to first product-code implementation
Summary: Recommendation: stop broad planning after a short closure sequence—first product-code brief, technical shell decision, tiny canonical fixtures, fixed `move_piece_requested -> piece_moved`, acceptance checklist, and prototype role freeze—then start the narrow `Table Sandbox 0.1` slice: Vite/React/TypeScript/Phaser shell, load fixtures, bootstrap `GameState`, run Action/Event pipeline, render/log/save, and only afterward expand manual actions, validation, and controlled Map Editor integration.

## Raw Response

## External Question ID

V1-20260524-003946

## Context Readback

* Uploaded prompt / `Вставленный текст(18).txt` — fully read. 
* `external_chat_rules.md` — fully read. ([GitHub][1])
* Central `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — fully read. ([GitHub][4])
* Project `project_state.md` — fully read. ([GitHub][5])
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
* Project `V1_navigation.md` — fully read. No additional notebook entries were opened; the index summaries were sufficient for this execution-plan question. ([GitHub][19])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require the answer to preserve the exact `External Question ID`, give an honest `Context Readback`, separate central-doc conclusions from project-specific conclusions and not-verified material, and avoid claiming local repo/build/test/runtime access unless that access was explicitly provided. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation is only for `ai-workflow-core`; it does not authorize claims about the consumer repo unless consumer-project files are explicitly provided in the prompt. ([GitHub][2])

For this question, central docs define the response discipline only. The actual execution plan must come from the provided project-specific documents and prompt. 

### Confirmed from provided excerpts

## Current Position

The project is past the "what are we building?" stage. The accepted framing is already clear: this is not a hardcoded digital Sword of Rome, but a browser-based 2D authoring tool / editor / tabletop sandbox for counter-based wargames; Sword of Rome-like content is only a first reference/test module. ([GitHub][3])

The accepted architecture is also clear enough for a first implementation pass: Layer 1 is core/data model, Layer 2 is authoring/editor capabilities, Layer 3 is universal runtime / play sandbox, and Layer 4 is module package content plus module rules/hooks. ([GitHub][3])

The key first milestone is not "make the whole game." It is `Table Sandbox 0.1`: load canonical files, create `GameState`, process an explicit Action/Event pipeline, keep rules permissive, move one piece through the full loop, show the event log, redraw from `GameState`, and save/load the runtime snapshot. ([GitHub][12])

So the project should now move from planning into a **short closure sequence**, then into the **first narrow coding phase**.

---

# Nearest Step

The immediate next step should be:

```text id="bxnsx2"
Create one execution handoff/spec for the first coding block:
first_product_code_block.md
```

This file should not be another big architecture document. It should be a practical implementation brief that says exactly:

```text id="c3yirz"
what we build first
what files are used
what the first test module contains
what the first action/event pair is
what acceptance checks define done
what is explicitly out of scope
how the existing prototype may and may not be used
```

Why this first? Because the project now has enough planning canon. The main remaining risk is not "missing architecture"; the main risk is that the first coding agent starts too broadly, refactors the prototype, hardcodes the reference game, or bypasses `Action/Event`. The first coding block brief prevents that. ([GitHub][12])

---

# Execution Plan Overview

Recommended sequence:

```text id="tygwnd"
Phase 0 — Pre-code closure
Phase 1 — Technical bootstrap
Phase 2 — Canonical fixture seed
Phase 3 — Runtime/data bootstrap
Phase 4 — Action/Event spine
Phase 5 — First vertical slice
Phase 6 — Save/load and validation hardening
Phase 7 — Controlled Map Editor integration
Phase 8 — Immediate authoring expansion
```

Only Phases 0–5 are required to reach the first meaningful product-code proof. Phases 6–8 are immediate follow-ups after that proof works.

---

# Phase 0 — Pre-Code Closure

## Goal

Close only the small practical gaps that block clean implementation.

## Expected output / artifacts

```text id="8f6dji"
first_product_code_block.md
tiny_fixture_inventory.md or inline fixture section
first_action_event_contract.md or inline section
acceptance_checklist.md or inline checklist
prototype_usage_decision.md or inline decision
```

These can be one compact document instead of five separate files.

## Why now

The readiness audit already concluded that broad coding is too early, but a narrow `Table Sandbox 0.1` coding slice can start after short closure. The V1 navigation records that the needed closure is: Vite + React + TypeScript + Phaser setup, tiny fixtures, fixed `move_piece_requested -> piece_moved`, acceptance checks, and prototype reuse decision. ([GitHub][19])

## Dependencies

```text id="a7lkl8"
accepted architecture
canonical file model
first vertical slice spec
prototype integration mapping
readiness audit conclusion
```

## Done condition

Phase 0 is done when a coding agent can answer these without guessing:

```text id="e8ct4q"
1. Where does product code start?
2. What technical shell is used?
3. What sample JSON files exist?
4. What is the first action?
5. What is the first event?
6. What exactly proves the first slice?
7. What must not be built yet?
8. Is the external prototype reference-only or product-code seed?
```

Recommended answers:

```text id="apscdr"
technical shell: Vite + React + TypeScript + Phaser
first action: move_piece_requested
first event: piece_moved
prototype role: reference + selective donor, not whole product foundation
```

The prototype mapping doc already says the prototype should be a reference prototype and selective donor for the Map Editor surface, not a direct product-code foundation. ([GitHub][18])

---

# Phase 1 — Technical Bootstrap

## Goal

Create the minimal browser application shell where the first slice can live.

## Expected output / artifact

```text id="1yfp52"
A locally runnable product-code skeleton:
- Vite app
- React shell
- TypeScript enabled
- Phaser installed/mounted for visual table area
- placeholder GameState outside Phaser
- placeholder event log area
```

## Why now

Layer 1 explicitly includes Phaser/React integration, render/input lifecycle, camera shell, pointer input, drag/drop, pan/zoom, snap primitives, persistence, ids, schemas and JSON formats. It also says the source of truth must stay outside Phaser objects. ([GitHub][3])

So before coding the runtime slice, the app needs a minimal technical home.

## Dependencies

```text id="j9cz35"
Phase 0 technical bootstrap decision
local Node/npm availability
chosen product-code location
```

## Done condition

Phase 1 is done when:

```text id="0qde8m"
1. App starts locally.
2. React shell renders.
3. Phaser scene/canvas area appears.
4. A placeholder table/grid can render.
5. Placeholder GameState exists outside Phaser.
6. React can display placeholder event log.
7. Phaser can emit a simple input signal upward.
8. No runtime truth lives inside Phaser scene objects.
```

## Guardrail

Do not build the actual game yet. Do not add cards, combat, rules, network play, or full editor UI. This phase proves only the technical shell.

---

# Phase 2 — Canonical Fixture Seed

## Goal

Create the smallest canonical module data that can be loaded and used by the first slice.

## Expected output / artifact

```text id="qczhm3"
fixtures/tiny-module/
  project.json
  modules/tiny/module.json
  modules/tiny/map.json
  modules/tiny/scenario.basic.json
  modules/tiny/rules.metadata.json
  saves/empty.savegame.json
```

The exact path can be different locally, but the artifact set should be this small.

## Fixture content

Use only:

```text id="e0afuz"
2–3 spaces
1–2 connections
1 map
1 scenario
1–2 factions
1–3 piece definitions
1–3 piece instances
manual/permissive rules metadata
```

For `0.1`, compact `PieceDefinition[]` and `FactionDefinition[]` may temporarily live inside `module.json`; later they can move into `pieces.json` and `factions.json`. ([GitHub][12])

## Why now

The milestone plan says the first order is canonical sample files, then `GameState` bootstrap, then Action/Event, then permissive RulesHooks, then the first thin vertical slice. Nothing stable can happen until ids, references and file ownership exist. ([GitHub][12])

## Dependencies

```text id="h1p1xu"
minimal canonical file schemas
module package model
domain schemas contract
```

## Done condition

Phase 2 is done when:

```text id="5koail"
1. Each fixture file has a clear role.
2. map.json contains topology, not runtime state.
3. scenario contains initial setup, not event history.
4. savegame contains runtime snapshot/log, not canonical definitions.
5. rules.metadata contains declarative metadata, not executable rules.
6. IDs and references are internally consistent.
```

The package model explicitly says `savegame.json` is not canonical module content; it is a runtime artifact. ([GitHub][15])

---

# Phase 3 — Runtime/Data Bootstrap

## Goal

Load fixture files and create initial authoritative `GameState`.

## Expected output / artifact

```text id="3u49kc"
Runtime can:
- load project/module/map/scenario/rules metadata
- validate minimal references
- create initial GameState
- expose GameState to renderer
- keep definitions separate from runtime state
```

## Why now

The first vertical slice requires canonical files, sample module, sample scenario, runtime loading into `GameState`, permissive rules shim and action/event log. ([GitHub][13])

## Dependencies

```text id="mwuc0d"
Phase 1 technical shell
Phase 2 canonical fixtures
```

## Done condition

Phase 3 is done when:

```text id="8pwyht"
1. Fixture module loads.
2. Initial GameState is created.
3. At least one piece exists in GameState at location A.
4. Renderer receives state from runtime.
5. Renderer does not create authoritative state itself.
6. Definitions, scenario setup and runtime state are separate.
```

---

# Phase 4 — Action/Event Spine

## Goal

Create the explicit request-to-commit runtime pipeline before real drag/drop modifies anything.

## Expected output / artifact

```text id="xjxtb4"
Action dispatcher
Validation result shape
resolveAction result shape
Event commit path
Reducer
Append-only event log
Render refresh after committed state
```

## First pair

```text id="p9vguj"
Action: move_piece_requested
Event:  piece_moved
Reducer effect: piece.locationId changes
```

## Why now

The milestone plan says the Action/Event backbone must exist before real drag/drop or editor mutation paths. The first milestone runtime skeleton also states that no state mutation should happen outside committed events. ([GitHub][12])

## Dependencies

```text id="r5l2wz"
Phase 3 GameState bootstrap
RulesHooks permissive shim
```

## Done condition

Phase 4 is done when:

```text id="4seqzq"
1. Runtime can accept a shaped action.
2. Malformed action can be rejected.
3. Valid move action can resolve into proposed piece_moved.
4. Runtime, not rules hook, commits the event.
5. Event receives sequence/order.
6. Reducer updates GameState.
7. Event log appends visibly.
8. Renderer redraws from committed state.
```

The Action/Event contract says `Action` is a request/intention and `Event` is a committed fact; only committed events mutate `GameState`. ([GitHub][10])

---

# Phase 5 — First Vertical Slice

## Goal

Prove the smallest full product loop.

## Expected output / artifact

```text id="c6id2a"
One piece moves from space A to space B through:
input → Action → validation → resolution → Event → reducer → GameState → log → render
```

## Why now

This is the first real proof that the platform foundation works. The first vertical slice spec defines exactly this: user drags one piece from `space A` to `space B`, runtime emits `move_piece_requested`, rules validate permissively, rules return `piece_moved`, runtime commits it, reducer updates `GameState`, and view redraws from committed state. ([GitHub][13])

## Dependencies

```text id="a7qa6y"
Phase 1 technical shell
Phase 2 fixtures
Phase 3 GameState bootstrap
Phase 4 Action/Event spine
permissive RulesHooks shim
```

## Done condition

Phase 5 is done only if all these are true:

```text id="q36tg8"
1. App loads the tiny module.
2. Board/spaces render.
3. A piece appears in space A.
4. User drags or requests moving the piece to space B.
5. Runtime emits move_piece_requested.
6. Validation allows the action.
7. Resolution returns piece_moved.
8. Runtime commits event and appends event log.
9. Reducer changes authoritative GameState.
10. Piece appears in space B after render refresh.
11. No hidden mutation path exists in renderer, Phaser or rules hook.
12. The test module does not require special-case lower-layer logic.
```

This slice proves canonical data load, runtime bootstrap, RulesHooks boundary, Action/Event separation, runtime ownership of state, and renderer-as-view. ([GitHub][13])

---

# Phase 6 — Save/Load And Validation Hardening

## Goal

Make the first slice repeatable and safe.

## Expected output / artifact

```text id="k350g4"
basic save runtime snapshot
load runtime snapshot
event log persists
reference validation catches broken ids
structural incompatibility blocks load
safe minor metadata mismatch warns if needed
```

## Why after the first slice

Save/load hardening is useful after there is actual runtime state and event log to preserve. Validation hardening is useful after the basic loop exists. The milestone plan puts save/load and validation hardening after the first thin vertical slice and remaining manual actions. ([GitHub][12])

## Dependencies

```text id="qrwwhg"
working first slice
event log
runtime snapshot shape
canonical ids/references
```

## Done condition

```text id="g7z8g8"
1. Current GameState can save.
2. Saved state can reload.
3. Event log survives round-trip.
4. savegame does not redefine map/piece/faction definitions.
5. Broken location/piece/map refs are reported.
6. Validation errors are readable to a human.
```

---

# Phase 7 — Controlled Map Editor Integration

## Goal

Start bringing useful behavior from the existing prototype into the product architecture without letting the prototype become the architecture.

## Expected output / artifact

```text id="4obsr6"
Map Editor surface skeleton inside Module Authoring Workspace:
- layer/map reference support
- spaces
- connections
- zones
- inspector
- map validation
- map.json export/import path
```

## Why after first slice

The prototype is useful as a reference and selective donor for the Map Editor surface, but not as a direct product-code foundation. The mapping doc explicitly warns against carrying over the single large `App.jsx`, prototype state as source of truth, prototype-local save format as canonical format, or any structure that bypasses `GameState`, Action/Event or RulesHooks. ([GitHub][18])

## Dependencies

```text id="fv6dmp"
working runtime loop
canonical map schema
clear authoring/runtime boundary
prototype integration mapping
```

## Done condition

```text id="8fjdru"
1. Map Editor writes canonical map definitions.
2. It does not write runtime GameState.
3. It does not bypass save/package boundaries.
4. It preserves useful prototype behaviors: layers, spaces, connections, zones, inspector, validation/export ideas.
5. It is integrated as a surface, not as the whole app.
```

The authoring workflow says the product should be one Module Authoring Workspace with specialized surfaces such as Map Editor, Pieces/Factions Editor, Scenario Editor, Rules Metadata Surface and Play Sandbox Preview. ([GitHub][14])

---

# Phase 8 — Immediate Authoring Expansion

## Goal

Turn the first runtime proof into the beginning of a real module-building workflow.

## Expected output / artifact

```text id="o7htcj"
minimal Module Authoring Workspace with:
- Module Settings / Manifest surface
- Map Editor surface
- Pieces/Factions surface
- Scenario surface
- Rules Metadata surface
- Validation summary
- Play Sandbox Preview launch
```

## Why here

Once the first slice proves runtime, the next product value is letting the designer create and correct the module package through authoring surfaces. The authoring workflow describes the practical day-to-day loop: edit module settings, build map, define factions/pieces, build scenario, adjust rules metadata, validate, preview, inspect event log, and return to correction. ([GitHub][14])

## Dependencies

```text id="zh4rz2"
working first slice
basic save/load
basic validation
canonical file ownership
prototype mapping
```

## Done condition

```text id="zy0zqd"
1. User can open a module workspace.
2. User can see current module/scenario context.
3. User can edit at least minimal map/scenario/content data.
4. User can validate.
5. User can launch Play Sandbox Preview.
6. Preview changes runtime state, not definitions.
7. Returning to authoring keeps mode boundaries clear.
```

The UX model says the product should be mode-based: authoring edits definitions/setup, playtest preview runs runtime proof, runtime session handles saves/snapshots, and package/save workflow validates and separates module content from runtime save. ([GitHub][16])

---

# What Is True Pre-Code Work

Only these are still worth doing before implementation:

```text id="vr6s9s"
1. first_product_code_block.md
2. technical bootstrap decision
3. tiny canonical fixtures
4. first action/event pair fixed
5. acceptance checklist
6. prototype usage decision
7. product-code starting location decision
```

This should be short. The goal is to remove ambiguity for the coding agent, not to create another architecture layer.

---

# What Is First Code Work

The first code work is:

```text id="zpdbpv"
1. create runnable technical shell
2. load tiny fixtures
3. create GameState
4. render board/spaces/piece
5. implement move_piece_requested
6. implement permissive validation/resolution
7. commit piece_moved
8. update GameState through reducer
9. show event log
10. redraw from GameState
11. save/load basic snapshot
```

Nothing else should enter the first code phase unless it directly supports this.

---

# What Must Wait Until After First Slice

Explicitly defer:

```text id="4h4vth"
full Sword of Rome rules
combat/scoring resolver
strict legality
cards/decks
hidden information
reaction windows
online/server sync
AI
advanced stack model
module dependency framework
migration framework
full playtest session manager
scenario fork from snapshot
package publishing
polished final UI
```

These are already listed as out-of-scope or later work in the `Table Sandbox 0.1` plan and first vertical slice spec. ([GitHub][12])

---

# Planning Gaps Worth Closing

## Worth closing before code

```text id="p9lqrx"
technical shell decision
first product-code location
fixture file names and IDs
first action/event payload fields
acceptance checklist
prototype reuse status
```

These are small and practical.

## Can close during implementation

```text id="k7f8qy"
exact TypeScript/Zod schema details
exact component folder names
exact reducer file organization
exact UI layout
exact Russian labels
exact validation UI presentation
basic test runner setup
```

These should not delay the first slice.

## Should not be planned now

```text id="acxqr5"
full mature package importer/exporter
full card subsystem
full rules automation
advanced stack ordering
complete save migration framework
complete playtest session manager
online play architecture
server authority
marketplace/publishing
```

The post-0.1 roadmap already places these after `0.1` foundations or later milestones. ([GitHub][17])

---

# Risks Of Wrong Order

## Risk 1 — Refactoring the prototype before runtime proof

Bad order:

```text id="etsgnd"
prototype refactor → huge Map Editor work → no GameState proof
```

Correct order:

```text id="in6kq2"
first runtime proof → then controlled Map Editor integration
```

The prototype integration doc says the prototype belongs mainly to the future Map Editor surface and should not define runtime shell, package model, Action/Event backbone or RulesHooks boundary. ([GitHub][18])

## Risk 2 — Letting Phaser own truth

Bad order:

```text id="3g81fq"
drag sprite → mutate sprite state → later try to reconstruct GameState
```

Correct order:

```text id="bgl6k9"
drag input → Action → Event → GameState → renderer redraws
```

Architecture requires serializable source of truth outside Phaser objects. ([GitHub][3])

## Risk 3 — Hardcoding Sword of Rome-like assumptions

Bad order:

```text id="hqxgqn"
specific historical rules → lower-layer data structures
```

Correct order:

```text id="3s4yi2"
universal runtime capabilities → tiny generic module → later Sword-like reference module
```

Architecture and roadmap both warn not to let the reference module shape lower layers. ([GitHub][3])

## Risk 4 — Making savegame a module package

Bad order:

```text id="5fv36j"
savegame contains everything because it is convenient
```

Correct order:

```text id="17xz66"
module package contains definitions/setup/rules metadata
savegame contains runtime snapshot/event log
```

The module package model explicitly separates module package content from runtime save artifacts. ([GitHub][15])

## Risk 5 — Endless planning

Bad order:

```text id="mtu51p"
another roadmap → another architecture note → another UX model → no code
```

Correct order:

```text id="1pt86w"
short closure → first product-code slice → learn from implementation
```

---

# Stop-Planning / Start-Coding Threshold

Stop planning and start coding when all are true:

```text id="ihuhwk"
1. first_product_code_block.md exists.
2. Technical shell is decided: Vite + React + TypeScript + Phaser.
3. Product-code location is decided.
4. Tiny canonical fixture set exists or is specified exactly.
5. First action/event pair is fixed:
   move_piece_requested -> piece_moved.
6. Acceptance checklist exists.
7. Prototype usage is frozen:
   reference + selective donor, not whole-product foundation.
8. Non-goals are visible to the coding agent.
```

At that point, more planning is lower value than implementation feedback.

---

# Safest Narrow Implementation Start

The safest first coding target is:

```text id="hpt5c3"
Build a runnable Vite + React + TypeScript + Phaser shell
that loads a tiny canonical module,
creates GameState,
renders spaces and one piece,
moves that piece through move_piece_requested -> piece_moved,
updates GameState,
shows event log,
and save/loads a runtime snapshot.
```

That is the correct bridge from the current planning state into real product code.

---

# Immediate Next Slices After First Slice Works

After the first slice works, the next slices should be:

## Slice 2 — Remaining manual table actions

```text id="k8fli0"
create piece
delete piece
change control
create/update space
create/update connection
save snapshot
load save
```

The milestone plan places these after the first thin vertical slice. ([GitHub][12])

## Slice 3 — Save/load hardening

```text id="y33iop"
round-trip savegame
event log persistence
version/reference checks
structural incompatibility block
safe metadata warnings
```

## Slice 4 — Validation hardening

```text id="rsj8qa"
unique ids
reference integrity
known action/event types
valid piece locations
schema version compatibility
clear human-readable errors
```

## Slice 5 — Tiny test module pass

```text id="c0e17p"
small generic module first
then tiny Sword of Rome-like reference pass
```

The test module must not reshape universal layers. ([GitHub][12])

## Slice 6 — Controlled Map Editor integration

```text id="dfm54s"
bring prototype-proven map editing behavior into product architecture:
layers
spaces
connections
zones
inspector
validation
export
```

Do this only after runtime foundation exists, and only as a Module Authoring Workspace surface. ([GitHub][18])

---

# Final Recommended Action Sequence

If one practical plan must be handed to Codex/Kilo now, use this:

```text id="y1pxv7"
1. Write first_product_code_block.md.
2. Decide product-code location and technical shell.
3. Freeze prototype role as reference + selective donor.
4. Create tiny canonical fixture set.
5. Freeze first action/event:
   move_piece_requested -> piece_moved.
6. Write acceptance checklist.
7. Start product-code skeleton:
   Vite + React + TypeScript + Phaser.
8. Load fixtures.
9. Bootstrap GameState.
10. Implement Action/Event spine.
11. Render board/spaces/piece.
12. Move one piece through full pipeline.
13. Show event log.
14. Add basic save/load snapshot.
15. Only then expand manual actions, validation and controlled Map Editor integration.
```

This is the shortest serious path from the current planning state to a real working foundation.

### Not available / not verified

* Local repository, branch, git status, package files, tests, runtime, build and shell were not inspected.
* It is not verified whether a product-code skeleton already exists locally.
* It is not verified whether Vite, React, TypeScript, Phaser, Node.js or npm are already installed locally.
* It is not verified whether the current external prototype builds or runs locally.
* Exact product-code folder path is not fixed by this answer.
* Exact TypeScript/Zod schema implementation is not specified here.
* Exact React/Phaser integration code is not specified here.
* Exact Kilo/Codex handoff file name may be decided locally.
* This is a planning-only execution plan, not an accepted local implementation decision.

## Candidate Navigation Entry

V1-20260524-003946: Detailed execution plan for moving from accepted planning canon to first product-code implementation. Recommendation: stop broad planning after a short closure sequence—first product-code brief, technical shell decision, tiny canonical fixtures, fixed `move_piece_requested -> piece_moved`, acceptance checklist, and prototype role freeze—then start the narrow `Table Sandbox 0.1` slice: Vite/React/TypeScript/Phaser shell, load fixtures, bootstrap `GameState`, run Action/Event pipeline, render/log/save, and only afterward expand manual actions, validation, and controlled Map Editor integration.

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
[19]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
