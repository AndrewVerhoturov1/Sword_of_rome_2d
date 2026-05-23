# Notebook Entry

- External Question ID: `V1-20260523-161245`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-161245_planning-only-analysis-of-how-to-use-external.md`

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
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_package_model.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_product_ux_model.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://github.com/AndrewVerhoturov1/arena-test/tree/main/prototypes/table-map-editor-canvas-local-fixed/source`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/README.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/package.json`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/vite.config.js`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/main.jsx`

## Candidate Navigation Entry

Topic: Planning-only analysis of how to use external prototype `table-map-editor-canvas-local-fixed`
Summary: Recommendation: treat it as a reference prototype and selective donor for the future Map Editor surface, preserving UX/interaction ideas like layers, spaces, connections, zones, inspector, validation and export, but do not promote the single-file React prototype wholesale into product code or let it override canonical package, authoring/runtime, Action/Event, and RulesHooks boundaries.

## Raw Response

## External Question ID

V1-20260523-161245

## Context Readback

* Uploaded prompt / `Вставленный текст(17).txt` — fully read. 
* Uploaded prototype capability description / `Вставленная ​​уценка(3).md` — fully read earlier in this conversation and used as provided prototype description. 
* `external_chat_rules.md` — fully read. ([GitHub][1])
* Central `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — opened; content returned as short file, treated as fully read for available content. ([GitHub][4])
* Project `project_state.md` — opened; content returned as very short file, treated as fully read for available content. ([GitHub][5])
* Project `.ai/repo_navigation.md` — fully read. ([GitHub][6])
* `domain_schemas_contract.md` — fully read. ([GitHub][7])
* `minimal_canonical_file_schemas.md` — fully read. ([GitHub][8])
* `rules_hooks_interface.md` — fully read. ([GitHub][9])
* `action_event_contract.md` — fully read. ([GitHub][10])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][11])
* `first_vertical_slice_spec.md` — fully read. ([GitHub][12])
* `module_authoring_workflow.md` — fully read. ([GitHub][13])
* `module_package_model.md` — fully read. ([GitHub][14])
* `module_product_ux_model.md` — opened; short readable content returned, treated as fully read for available content. ([GitHub][15])
* `post_0_1_platform_roadmap.md` — opened; short readable content returned, treated as fully read for available content. ([GitHub][16])
* Project `V1_navigation.md` — fully read. No additional notebook entries were opened for this answer. ([GitHub][17])
* External prototype GitHub folder — opened and inspected as repository tree view. ([GitHub][18])
* Prototype `README.md` — fully read. ([GitHub][19])
* Prototype `package.json` — fully read. ([GitHub][20])
* Prototype `vite.config.js` — fully read. ([GitHub][21])
* Prototype `src/App.jsx` — partially read; opened and inspected in relevant sections, but treated as partially read because the raw JSX is compact/flattened and not ideal for full line-by-line review here. ([GitHub][22])
* Prototype `src/main.jsx` — fully read; short entry file. ([GitHub][23])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require exact `External Question ID`, honest `Context Readback`, separation of central-doc conclusions, project-specific/provided-context conclusions, and not-verified items. They also prohibit claiming local repo, shell, build, runtime, tests, git status, or local implementation behavior unless that was explicitly provided and checked. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation is only a closed navigation set for `ai-workflow-core`; it does not authorize claims about the consumer project unless consumer-project links or excerpts are explicitly provided. ([GitHub][2])

For this answer, central docs define response discipline only. They do not decide how to integrate the external prototype.

### Confirmed from provided excerpts

## Prototype verdict

The prototype `table-map-editor-canvas-local-fixed` should be classified as:

```text
primary role: reference prototype
secondary role: donor of selected ideas and isolated logic
not recommended role: direct product-code foundation
```

It is **not throwaway**. It is useful and should be preserved. But it should not be promoted wholesale into the main product as the foundation without controlled extraction.

The reason is simple: the main project canon already separates module package content, authoring surfaces, Play Sandbox Preview, runtime `GameState`, Action/Event pipeline, and RulesHooks boundary. The prototype, by contrast, is a compact React prototype focused mainly on table/map authoring behavior, with much of the logic in one large `App.jsx`. The prototype repo confirms a Vite/React setup, while `App.jsx` contains the main UI and interaction implementation in a compact single-file form. ([GitHub][20])

So the safest reading is:

```text
This prototype proves useful map-editor UX and interaction ideas.
It does not define the final product architecture.
```

This also matches the project canon: `Table Sandbox 0.1` must prove canonical files, `GameState`, Action/Event, permissive RulesHooks, and first vertical slice; it should not let a prototype reshape the universal architecture. ([GitHub][11])

---

## What the prototype is

The prototype is a browser-based React/Vite map/table editor. Its `package.json` shows a Vite/React setup with `dev`, `build`, and `preview` scripts, and `vite.config.js` sets the base path for the GitHub Pages location. ([GitHub][20])

Based on the provided feature description and inspected source, it supports the core authoring concepts that matter for a point-to-point map editor:

```text
visual layers / map underlays
spaces / points
connections
curved connection points
zones
left object lists
right inspector
grid and snap
zoom and pan
localStorage save/load
undo/redo
validation
map.json export
full project JSON export
```

The uploaded prototype description explicitly frames it as a React prototype for editing table, map, points, links, and zones, not as a full game or rules engine. 

This is exactly why it is valuable: it already demonstrates the **authoring feel** of a future Map Editor surface.

---

## Relation to main project canon

The main project canon says the product is not a one-off Sword of Rome implementation. It is a reusable browser-based authoring/runtime platform for 2D counter-based wargames. ([GitHub][3])

The authoring workflow canon says the product should have one Module Authoring Workspace with specialized surfaces inside it, including `Map Editor`, `Pieces / Factions Editor`, `Scenario Editor`, `Rules Metadata Surface`, and `Play Sandbox Preview`. ([GitHub][13])

Therefore, this prototype maps best to only one part of the future product:

```text
Module Authoring Workspace
└── Map Editor surface
```

It should not be treated as:

```text
the whole product
the whole runtime
the module package system
the rules engine
the Play Sandbox architecture
the final source-of-truth model
```

The prototype is most relevant to the **Map Editor surface** and partly to future **table/canvas interaction patterns**.

---

## Reusable parts

### 1. Exact reuse candidates

These are things that may be reusable with little conceptual change, but still need local code review before copying.

```text
Vite static prototype setup
GitHub Pages base-path idea
simple React app bootstrapping
some CSS/UI layout ideas
some object-list/inspector patterns
some export/download helper patterns
basic localStorage draft persistence pattern
```

The Vite config's explicit base path is useful as a deployment reference for static demos. ([GitHub][21])

But "exact reuse" should be limited. Even if code works, direct copying should not become the default strategy because the main project needs stronger architecture boundaries.

---

### 2. Adapted reuse candidates

These are the strongest candidates.

#### Map editor interaction model

The prototype's interaction model is valuable:

```text
add map layer
select object
move layer
scale layer
rotate layer
add point
add connection
add zone
edit properties
validate
export
save locally
```

This should be preserved at the product behavior level. The uploaded prototype description confirms these features and frames them as the current working capability set. 

Recommended use:

```text
Keep the behavior.
Refactor the implementation.
```

#### Left panel / right inspector pattern

The left panel listing layers/map objects and the right properties panel are a good UX pattern for the future Map Editor surface. The source snippets show UI labels and inspector sections for layer/space/connection/zone editing. ([GitHub][22])

Recommended use:

```text
Reuse the UX structure.
Rewrite into product components.
```

#### Topology model hints

The prototype already uses the right conceptual objects:

```text
layers
spaces
connections
zones
```

These match the main project's map/topology needs well. The canonical file model also expects `map.json` to contain board topology, not runtime state. ([GitHub][8])

Recommended use:

```text
Use prototype object names as hints.
Normalize them against the canonical MapDefinition contract.
```

#### Validation ideas

The prototype validates IDs, duplicate references, broken connection references, self-connections and map object issues according to the uploaded feature description. 

Recommended use:

```text
Keep validation categories.
Rebuild validation as a separate product validation module.
```

#### Geometry/transformation ideas

The prototype includes important map-editor ideas:

```text
grid
snap
zoom/pan
layer transform
space/connection/zone ordering
curved connection points
objects following a transformed map layer
```

These are very useful for Map Editor authoring.

Recommended use:

```text
Extract concepts into geometry/transform utilities later.
Do not leave them buried inside one UI component.
```

---

### 3. Concept-only reuse candidates

These should be reused as ideas, not code.

```text
single-file prototype structure
current internal state shape
current export shape
current localStorage project format
current DOM/SVG rendering approach as final rendering architecture
current object mutation style
current implicit editor/runtime boundary
```

Why concept-only? Because the main product must separate:

```text
definitions
scenario setup
runtime state
rules metadata
rules behavior
saves
```

The module package model explicitly says `map.json` is topology, `scenario` is initial setup, `savegame.json` is runtime, and `rules.metadata.json` is metadata, not executable rules. ([GitHub][14])

---

## Dangerous carryovers

These are the things that should **not** be carried into the main repo blindly.

### 1. Single large `App.jsx` as product architecture

The prototype source is centered around one main `App.jsx`, with many UI and interaction concerns living together. ([GitHub][22])

Danger:

```text
The product could inherit prototype complexity before architecture is ready.
```

Safer product split:

```text
components/
map-editor/
model/
store/
io/
validation/
geometry/
runtime/
fixtures/
```

---

### 2. Prototype state as source of truth

The prototype likely holds editor state directly in React component state. That is acceptable for a prototype. It is dangerous for the product if it becomes the canonical source of runtime truth.

Main canon says runtime state must go through:

```text
Action → validation → resolveAction → Event → reducer → GameState → log → render
```

The Action/Event contract says actions are requests and events are committed facts; only committed events mutate `GameState`. ([GitHub][10])

Danger:

```text
Dragging an object directly mutates authoritative runtime state.
```

Safe boundary:

```text
Authoring editor can edit definitions/setup.
Play Sandbox runtime must use Action/Event.
```

---

### 3. Mixing authoring and runtime

The prototype is an authoring map editor. It should not become the runtime/play sandbox.

The module authoring workflow defines a hard boundary:

```text
Authoring Mode changes definitions/setup/module metadata/rules metadata.
Play Sandbox Mode changes current runtime state/event log/save snapshot.
The same visual gesture must not silently switch meaning between modes.
```

([GitHub][13])

Danger:

```text
Moving a point, moving a start piece, and moving a runtime piece feel visually similar,
so the product could accidentally blur authoring and playtest state.
```

Safe use:

```text
Use this prototype for map authoring only.
Build Play Sandbox separately around GameState and Action/Event.
```

---

### 4. Treating prototype export as final package format

The prototype's `map.json` export is useful, but it should be normalized against the accepted canonical file model.

The canonical model requires:

```text
project.json = workspace index
module.json = module manifest
map.json = board topology
scenario.json = initial setup
rules.metadata.json = rules capability metadata
savegame.json = mutable runtime snapshot
```

([GitHub][11])

Danger:

```text
Prototype project JSON becomes the final module package by accident.
```

Safe use:

```text
Prototype export can become an adapter input.
Canonical export must follow main repo schema docs.
```

---

### 5. Letting map editor needs dominate runtime design

The prototype is strong in visual editing. But `Table Sandbox 0.1` first slice is not "make the best map editor." It is:

```text
load sample module
create GameState
move one piece through Action/Event
commit event
update GameState
show log
render from GameState
```

([GitHub][12])

Danger:

```text
Team spends weeks improving map editor before proving runtime backbone.
```

Safe order:

```text
Use prototype as reference.
Start first product slice with canonical fixtures and runtime loop.
Bring map editor capabilities in after the runtime skeleton is stable.
```

---

## Best integration strategy

Recommended strategy:

```text
Controlled reference + selective extraction
```

Not:

```text
copy whole prototype into main product and build everything inside it
```

Not:

```text
throw prototype away
```

The safest approach is:

### Phase 1 — Freeze prototype as reference

Keep the prototype repo/demo as the current reference for desired Map Editor behavior.

Output:

```text
prototype_inventory.md
```

Purpose:

```text
Document which behaviors must be preserved:
layers, spaces, connections, zones, curve handles, grid/snap, inspector, validation, export.
```

The uploaded feature description already gives most of this inventory. 

---

### Phase 2 — Create product-code skeleton separately

Start product code from the accepted stack/path, not from the prototype blindly.

Given the previous readiness audit, the first product shell should be:

```text
Vite + React + TypeScript + Phaser
```

But with the correct role split:

```text
React = editor/workspace shell
Phaser = visual table/runtime canvas later
GameState = source of truth outside renderer
RulesHooks = module-specific behavior boundary
```

The prototype itself currently demonstrates a Vite/React setup, but it does not prove Phaser/runtime integration. `package.json` shows Vite/React dependencies, not a full Phaser runtime foundation. ([GitHub][20])

---

### Phase 3 — Build first `Table Sandbox 0.1` slice from fixtures

Use the main project canon first:

```text
canonical sample files
→ GameState bootstrap
→ Action/Event
→ permissive RulesHooks
→ first move-piece slice
```

The milestone plan explicitly orders the work this way. ([GitHub][11])

The prototype can help with the **rendering/editor feel**, but it should not block this first runtime slice.

---

### Phase 4 — Controlled extraction from prototype

After the first runtime skeleton exists, extract useful prototype ideas into product modules:

```text
map editor components
geometry utilities
map validation rules
map export adapter
layer/space/connection/zone inspector UX
```

Do this by mapping each prototype feature to a product layer:

```text
prototype feature → product destination → rewrite/adapt/exact copy decision
```

---

## Recommended reusable mapping

```text
Prototype layers
→ Map Editor surface / visual layer subsystem
→ adapted reuse

Prototype spaces
→ MapDefinition.spaces
→ adapted reuse, normalized to canonical schema

Prototype connections
→ MapDefinition.connections
→ adapted reuse, preserve curved-path concept as visual metadata if needed

Prototype zones
→ MapDefinition.zones
→ adapted reuse

Prototype validation
→ validation/mapValidation module
→ rewrite with same checks

Prototype map.json export
→ canonical map export adapter
→ adapted rewrite

Prototype full project export
→ editor workspace draft format
→ concept-only, not canonical module package

Prototype localStorage save
→ temporary draft persistence
→ adapted later, not canonical persistence

Prototype undo/redo
→ authoring undo/redo idea
→ concept-only until authoring transaction model is decided

Prototype left/right UI layout
→ Module Authoring Workspace / Map Editor surface
→ adapted reuse

Prototype one-file React implementation
→ no direct reuse as architecture
→ do not carry over
```

---

## What can be transferred almost directly

Very little should be transferred truly "as-is."

Possible near-direct transfers after local review:

```text
static demo Vite config idea
some simple helper functions
some CSS visual ideas
some labels in Russian
small download/export helper
small localStorage helper
```

Even these should be copied only after checking license/project fit and product folder conventions.

The stronger reuse is not code copying. It is **behavior copying**.

---

## What should be rewritten from scratch while preserving the idea

These should be rewritten:

```text
state management
map model normalization
validation module
import/export layer
geometry transforms
selection model
inspector components
layer list
map object tree
undo/redo
project draft save/load
```

Reason: these need to align with the main product's canonical definitions, package model, authoring/runtime boundary, and future TypeScript/data contracts.

---

## What should not be taken into the main project

Do not take:

```text
single giant App.jsx structure
prototype state shape as canonical schema
prototype full-project JSON as module package
prototype localStorage as persistence architecture
prototype direct object mutation as runtime model
prototype UI as final product UX without re-validation
prototype map editor as the whole product shell
```

The main project already defines the larger UX loop: Module Authoring Workspace creates and validates a module package; Play Sandbox Preview runs it; save/snapshot remains separate from canonical content. ([GitHub][15])

---

## Relation to first coding slice

The prototype can help the first `Table Sandbox 0.1` slice in these ways:

```text
visual reference for board/table feel
reference for object selection
reference for grid/snap/zoom/pan behavior
reference for map topology export
reference for Russian UI vocabulary
reference for validation categories
```

But it can hurt the first slice if it causes this drift:

```text
start by refactoring the whole prototype
delay canonical fixtures
delay GameState bootstrap
delay Action/Event pipeline
treat editor state as runtime state
turn map editing into the first milestone instead of move-piece pipeline
```

The first slice remains:

```text
one piece moves from one space to another through Action → Event → GameState → log → render
```

That is the product foundation. The prototype should support it, not replace it. ([GitHub][12])

---

## Recommended pre-code action around the prototype

Before product code starts, do one small artifact:

```text
prototype_integration_mapping.md
```

It should be short and practical.

Suggested sections:

```text
1. Prototype role
2. Features to preserve
3. Features to rewrite
4. Features not to carry over
5. Mapping to product layers
6. First-slice relevance
7. Prototype reuse decision
```

Recommended content:

```text
Role:
reference prototype + selective donor

Use directly:
almost nothing without local review

Adapt:
layers, spaces, connections, zones, inspector, validation, export concepts

Do not carry:
single-file architecture, prototype project format as canonical package,
direct mutation runtime model, authoring/runtime mixing

First slice:
do not block Action/Event/GameState implementation on prototype migration
```

This is enough. Do not create a long migration plan before first code.

---

## Final recommendation

If one working decision must be made now, make this decision:

```text
Treat `table-map-editor-canvas-local-fixed` as the current reference prototype for the Map Editor surface.
Do not promote it wholesale into product code.
Use it as a donor of UX behavior, map-editor concepts, and selected isolated utilities after local review.
Start Table Sandbox 0.1 from the canonical product skeleton and first vertical slice.
```

Best immediate path:

```text
1. Freeze prototype as reference.
2. Write a short prototype integration mapping.
3. Start product-code skeleton separately.
4. Implement first Table Sandbox 0.1 vertical slice.
5. Later extract/adapt map-editor features into the Module Authoring Workspace.
```

This balances both risks:

```text
Do not throw away useful work.
Do not let prototype architecture hijack the product canon.
```

### Not available / not verified

* I did not run the prototype locally.
* I did not test the public demo interactively.
* I did not inspect git history, build output, or local branches.
* I did not verify whether the prototype currently builds successfully.
* I did not inspect the entire `App.jsx` line-by-line as a code review.
* I did not verify whether `dist` exists in a downloadable archive outside the opened repository tree.
* I did not check license, deployment artifacts, or CI.
* I did not decide final product folder paths.
* I did not decide whether the main project will use Phaser for authoring, runtime, or only runtime canvas.
* This answer is a planning-only integration analysis, not an accepted local implementation decision.

## Candidate Navigation Entry

V1-20260523-161245: Planning-only analysis of how to use external prototype `table-map-editor-canvas-local-fixed`. Recommendation: treat it as a reference prototype and selective donor for the future Map Editor surface, preserving UX/interaction ideas like layers, spaces, connections, zones, inspector, validation and export, but do not promote the single-file React prototype wholesale into product code or let it override canonical package, authoring/runtime, Action/Event, and RulesHooks boundaries.

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
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_package_model.md "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_product_ux_model.md "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[18]: https://github.com/AndrewVerhoturov1/arena-test/tree/main/prototypes/table-map-editor-canvas-local-fixed/source "arena-test/prototypes/table-map-editor-canvas-local-fixed/source at main · AndrewVerhoturov1/arena-test · GitHub"
[19]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/README.md "raw.githubusercontent.com"
[20]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/package.json "raw.githubusercontent.com"
[21]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/vite.config.js "raw.githubusercontent.com"
[22]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx "raw.githubusercontent.com"
[23]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/main.jsx "raw.githubusercontent.com"
