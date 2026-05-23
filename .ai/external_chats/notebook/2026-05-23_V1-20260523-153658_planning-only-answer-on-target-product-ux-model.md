# Notebook Entry

- External Question ID: `V1-20260523-153658`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-153658_planning-only-answer-on-target-product-ux-model.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_package_model.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-142942_planning-only-otvet-po-developer-side-authoring-workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-150830_macro-roadmap-posle-table-sandbox-0-1.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-141825_planning-only-otvet-po-trem-ostavshimsya-voprosam-dlya.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-144154_planning-only-otvet-po-validation-undo-redo-i.md`

## Candidate Navigation Entry

Topic: Planning-only answer on target product UX model
Summary: Recommendation: treat the product as a workflow loop — Module Authoring Workspace creates/validates a module package, Play Sandbox Preview runs it through `GameState` and Action/Event pipeline, the designer inspects logs/errors, returns to authoring, fixes content/setup, and repeats; keep authoring, playtest/runtime, package, and save/snapshot workflows explicit so definitions, scenario setup, and runtime state do not mix.

## Raw Response

## External Question ID

V1-20260523-153658

## Context Readback

* Uploaded prompt / `Вставленный текст(15).txt` — fully read. 
* `external_chat_rules.md` — fully read. ([GitHub][1])
* `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — fully read. ([GitHub][4])
* `domain_schemas_contract.md` — fully read. ([GitHub][5])
* `minimal_canonical_file_schemas.md` — fully read. ([GitHub][6])
* `module_authoring_workflow.md` — fully read. ([GitHub][7])
* `module_package_model.md` — fully read. ([GitHub][8])
* `post_0_1_platform_roadmap.md` — fully read. ([GitHub][9])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][10])
* `action_event_contract.md` — fully read. ([GitHub][11])
* `rules_hooks_interface.md` — fully read. ([GitHub][12])
* Project `V1_navigation.md` — fully read. ([GitHub][13])
* V1-navigation-discovered `V1-20260523-142942` notebook entry — partially read. ([GitHub][14])
* V1-navigation-discovered `V1-20260523-150830` notebook entry — partially read. ([GitHub][15])
* V1-navigation-discovered `V1-20260523-141825` notebook entry — partially read. ([GitHub][16])
* V1-navigation-discovered `V1-20260523-144154` notebook entry — partially read. ([GitHub][17])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require honest `Context Readback`, separation between central-doc conclusions, project-specific conclusions, and not-verified material. They also prohibit claiming local repo/runtime/test access unless that access was explicitly provided. ([GitHub][1])

Central `repo_navigation.md` is only a navigation aid for `ai-workflow-core`; it does not authorize claims about the consumer project unless project-specific links or excerpts are provided. ([GitHub][2])

For this question, central docs define the answer discipline only. They do not define the product UX model.

### Confirmed from provided excerpts

The accepted base is already clear: the project is a universal browser-based authoring/runtime platform for 2D counter-based wargames, not a hardcoded Sword of Rome-like game. The architecture separates universal authoring, universal runtime/play sandbox, and module package with module content plus module rules/hooks. ([GitHub][3])

The product UX model should therefore be built around one core idea:

```text
Дизайнер создаёт module package в Authoring Workspace.
Потом запускает его в Play Sandbox Preview.
Песочница создаёт runtime state и event log.
После проверки дизайнер возвращается в authoring, исправляет module package и снова запускает preview.
```

This matches the accepted hybrid authoring workflow: one Module Authoring Workspace with specialized editor surfaces, plus a separate Play Sandbox Preview that runs through `GameState` and the Action/Event pipeline. ([GitHub][7])

---

## Recommended UX model

The target product UX should be a **loop**, not a one-way wizard.

Recommended product loop:

```text
Создать / открыть модуль
→ собрать карту, фишки, стороны, сценарий
→ проверить пакет модуля
→ запустить песочницу
→ сделать тестовые действия
→ увидеть журнал и ошибки
→ сохранить снимок или начать заново
→ вернуться к редактированию
→ исправить карту / сценарий / фишки / правила
→ снова запустить песочницу
→ довести модуль до рабочего состояния
→ подготовить package к использованию / экспорту
```

The UX model should make three things constantly visible to the user:

1. **What am I editing now?**
   Definitions, scenario setup, or runtime state?

2. **What will be changed by this action?**
   `map.json`, `scenario.json`, `module.json`, `rules.metadata.json`, or `savegame.json`?

3. **Can this module be safely launched?**
   Validation status before preview/playtest.

This directly supports the accepted split between definitions, runtime state, and module rules. `map.json` is not current play state, `scenario.json` is initial setup, `savegame.json` is runtime state, and rules metadata is not executable rules. ([GitHub][5])

---

## Daily workflow loop

A practical daily workflow for a designer should look like this:

```text
1. Open workspace.
2. Choose module.
3. Check validation status.
4. Edit map.
5. Edit pieces/factions.
6. Edit scenario setup.
7. Check validation again.
8. Launch Play Sandbox Preview.
9. Move pieces / test flow.
10. Watch event log and current state.
11. Save snapshot or restart from scenario.
12. Return to authoring.
13. Fix broken setup or content.
14. Repeat.
```

This day-to-day loop should be the center of the product. The user should not feel like they are manually managing random JSON files. The product should feel like a workshop:

```text
I build the module.
I test the module.
I fix the module.
I test again.
```

The important UX point: the designer may switch quickly between authoring and playtest, but the product must never silently change the meaning of an action.

Example:

```text
Move a space in Map Editor
→ changes map definition.

Move a piece in Scenario Editor
→ changes scenario starting setup.

Move a piece in Play Sandbox
→ creates Action/Event and changes runtime GameState.
```

These actions may look visually similar, but they must be different workflow states.

---

## Main working modes

### 1. Module Authoring Mode

**Purpose:** create and edit the module package.

This mode owns:

```text
module.json
map.json
scenario.json
rules.metadata.json
pieces/factions content
cards/documents/assets later
```

Main surfaces:

```text
Module Settings
Map Editor
Pieces/Factions Editor
Scenario Setup Editor
Rules Metadata Editor
Cards Editor later
Documents Editor later
Assets Library later
```

This mode changes definitions and setup. It should not write runtime event logs or current playtest state into content files.

---

### 2. Validation / Readiness Mode

This can be a separate screen or a persistent panel inside the workspace.

**Purpose:** answer:

```text
Can this module be launched?
What is broken?
Where should I fix it?
```

It should check:

```text
module points to existing map
module points to existing scenario
scenario points to existing map
scenario piece instances point to existing piece definitions
piece locations point to existing spaces/zones
rules metadata has required action/event/phase info
save references are compatible if launching from save
```

Blocking errors should prevent Play Sandbox Preview. Warning-only issues should not block launch if they are safe. Previous planning already recommended blocking structurally invalid module/save references and leaving safe metadata/minor cases as warnings. ([GitHub][17])

---

### 3. Play Sandbox Preview

**Purpose:** launch the module from current definitions and scenario setup.

This mode should create an initial `GameState` and then run through the accepted pipeline:

```text
input
→ Action
→ validation
→ resolution
→ Event
→ GameState
→ event log
→ render
```

The action/event contract already fixes this backbone: actions are requests, events are committed facts, and only committed events mutate authoritative `GameState`. ([GitHub][11])

Play Sandbox Preview is not the same as editing the module.

It should allow:

```text
move piece
create/delete piece if manual sandbox allows
change control
save snapshot
load snapshot
restart from scenario
inspect event log
```

It should not silently edit:

```text
map.json
scenario.json
module.json
piece definitions
rules metadata
```

---

### 4. Runtime Mode

Runtime mode is the more "player-facing" version of Play Sandbox.

For early work, Play Sandbox Preview and Runtime Mode can be very close. Later they should diverge:

```text
Play Sandbox Preview
→ developer/designer testing mode
→ more diagnostics, validation, reset tools, inspect state

Runtime Mode
→ normal use/play mode
→ fewer editing tools, cleaner interaction, module behaves like playable content
```

Runtime Mode should still use the same core pipeline:

```text
Action → Event → GameState → log → render
```

The difference is not architecture; the difference is product UX and permissions.

---

### 5. Package / Export Mode

**Purpose:** prepare the module as a product artifact.

This mode should answer:

```text
What files are in this module?
Is the package valid?
What version is it?
Can it be exported/imported?
What assets are missing?
Are saves separate from canonical content?
```

The accepted mature package model says `module.json` should be the manifest, maps/scenarios/content/rules/assets/documents should be separate package parts later, and `savegame.json` should not be canonical module content. ([GitHub][8])

For `0.1`, package workflow can be minimal:

```text
Save module files.
Validate module.
Launch preview.
```

Later it becomes:

```text
Validate package.
Export package.
Import package.
Publish/share package.
Check compatibility.
```

---

## Mode map

Recommended mode map:

```text
Home / Project Picker
  ↓
Module Authoring Workspace
  ├─ Module Settings
  ├─ Map Editor
  ├─ Pieces/Factions Editor
  ├─ Scenario Setup Editor
  ├─ Rules Metadata
  ├─ Validation Summary
  ↓
Play Sandbox Preview
  ├─ Runtime state
  ├─ Event log
  ├─ Save snapshot
  ├─ Restart from scenario
  ↓
Back to Authoring
  ↓
Package / Export later
```

For `Table Sandbox 0.1`, the central modes should be only:

```text
Module Authoring Workspace
Validation Summary
Play Sandbox Preview
Save/Load Snapshot
```

Later modes:

```text
Playtest Session Manager
Package Export/Import
Cards/Decks Editor
Documents/Player Aids Editor
Asset Library
Migration/Compatibility Tools
Strict Runtime Mode
Server/online Runtime later
```

The post-0.1 roadmap already points in this direction: first harden validation/save compatibility, then expand authoring workspace, then add assisted runtime/rules hooks, then generic cards/documents, then modular platform alpha. ([GitHub][9])

---

## Designer workflow

The designer workflow is about creating the module package.

A good designer workflow:

```text
Create module
→ set module name/version/default scenario
→ create map spaces/connections/zones
→ create factions and piece definitions
→ create scenario starting setup
→ define minimal rules metadata
→ validate
→ preview
```

The UX should make references visible:

```text
This scenario uses this map.
This piece instance uses this piece definition.
This piece location must be a map space or zone.
This phase must exist in rules metadata.
```

The authoring workspace should protect the user from broken references. If a scenario points to a deleted space, the product should show that clearly before preview.

---

## Playtest workflow

The playtest workflow is about discovering whether the module works.

Recommended playtest loop:

```text
Start from scenario
→ test a few actions
→ watch log
→ identify problem
→ save snapshot if useful
→ return to authoring
→ fix source problem
→ relaunch
```

Good playtest UX should include:

```text
current scenario name
current module version
current mode: manual / assisted / strict later
event log
current validation warnings
restart from scenario
save snapshot
load snapshot
```

For `0.1`, playtest should stay manual/permissive. Strict enforcement is a later goal. The rules hooks contract already says early Table Sandbox should target manual to assisted, not strict too early. ([GitHub][12])

---

## Runtime workflow

Runtime workflow is what happens when the module is used as playable content.

For early product stages, runtime can be simple:

```text
choose module
choose scenario
start session
perform actions
save/load
```

Later runtime may add:

```text
player seats
hidden information
hands/decks
response windows
strict rule enforcement
server-authoritative play
```

But these should not drive the first UX model. The first UX model should remain authoring-centered because the product is currently a module-building platform, not a finished online game client.

---

## Module/package workflow

The module/package workflow should keep a clean distinction:

```text
Module package = reusable content and rules boundary.
Save/snapshot = one current playtest or game state.
```

Recommended package lifecycle:

```text
Draft module
→ validate draft
→ preview in sandbox
→ revise content/setup
→ validate again
→ mark as playable/testable
→ export/package later
```

The mature module package should eventually contain:

```text
manifest
maps
scenarios
pieces
factions
rules metadata
cards/decks optional
documents optional
assets optional
localization optional
package metadata later
```

But saves should remain outside canonical module content. A save can reference the package; it should not become the package. ([GitHub][8])

---

## Save / snapshot / fork workflow

For `0.1`, keep this simple.

### Safe default now

Use:

```text
Save snapshot
Load snapshot
Restart from scenario
```

Do not make "save as scenario" central yet.

### Later

Add explicit workflows:

```text
Create new scenario from current state
Fork scenario
Fork playtest session
Compare scenario with save
Promote playtest state to scenario setup
```

But these must be explicit. The system should never silently turn runtime state into scenario setup. Prior planning recommends `save as scenario` later as an explicit "create new scenario from extracted setup" operation without event log. ([GitHub][17])

Correct later flow:

```text
current GameState
→ extract piece positions/control/turn setup
→ remove event log
→ create new scenarioId
→ write new scenario file
→ add to module manifest
```

Wrong flow:

```text
copy savegame.json into scenario.json
```

---

## How Module Authoring Workspace and Play Sandbox Preview relate

They should be close, but not blended.

```text
Authoring Workspace creates package.
Play Sandbox Preview runs package.
```

Transition from authoring to playtest:

```text
Validate module
→ if blocking errors: stay in authoring
→ if valid/warnings only: launch preview
→ build initial GameState from scenario
```

Transition from playtest back to authoring:

```text
Stop preview
→ keep or discard snapshot
→ return to the same module/scenario
→ fix definitions/setup
```

The user should always know whether they are changing:

```text
module content
scenario setup
runtime state
```

This is the central anti-confusion rule.

---

## What is needed for Table Sandbox 0.1

For `0.1`, keep the UX small:

```text
1. Open module workspace.
2. Edit minimal module settings.
3. Edit map spaces/connections/zones.
4. Edit tiny piece/faction definitions, possibly compact in module.json.
5. Edit basic scenario setup.
6. Validate module.
7. Launch Play Sandbox Preview.
8. Move one piece through full Action/Event pipeline.
9. See event log.
10. Save/load snapshot.
11. Restart from scenario.
```

Not needed for `0.1`:

```text
package publishing
full playtest session manager
full cards/decks editor
documents editor
asset library manager
strict rules runtime
online multiplayer
server-authoritative runtime
AI
full migration tools
polished player-facing UX
```

The first milestone plan is already focused on proving the thin vertical slice and avoiding broad feature creep. ([GitHub][10])

---

## What should appear later

Later, the UX can grow into:

```text
Playtest Session Manager
Package Export/Import
Scenario Forking
Save-as-New-Scenario
Cards/Decks Editor
Documents/Player Aids
Asset Library
Rules Variant Editor
Validation/Migration Center
Player-facing Runtime Mode
```

But these should appear only when the foundation is stable.

---

## Anti-confusion rules

1. **Every workspace action should have a visible target.**

```text
This changes map definition.
This changes scenario setup.
This changes current runtime state.
```

2. **Play Sandbox must not silently edit definitions.**

Moving a piece in playtest should create runtime event/state, not rewrite the scenario.

3. **Scenario Editor must not contain event log.**

Scenario is starting setup, not play history.

4. **Save/snapshot must not become module content.**

Save references the module; it does not define the module.

5. **Rules metadata must not become executable rules.**

Rules behavior goes through hooks; metadata describes supported actions/events/phases.

6. **Sword of Rome-like test module must not shape the whole UX.**

UX labels and flows should stay generic:

```text
module
map
space
connection
piece
scenario
deck
document
rules metadata
```

not:

```text
Rome phase
Carthage event
Gallic control
Sword-specific procedure
```

Special Sword of Rome-like behavior belongs inside the reference module's content/rules, not in the universal UX.

---

## How not to make Sword of Rome-like module the center of UX

Use at least two UX testing examples:

```text
tiny generic test module
Sword of Rome-like reference module
```

If a UX decision only makes sense for the Sword-like module, keep it out of universal UX.

Universal UX should ask:

```text
Can a designer make a map?
Can a designer make pieces?
Can a designer make a scenario?
Can a designer validate the package?
Can a designer run a playtest?
Can a designer save a runtime snapshot?
```

It should not ask first:

```text
Can this exact historical rule be automated?
```

That question comes later, inside module-specific rules/hooks.

---

## UX maturity path

### 0.1 UX

```text
Minimal authoring workspace
basic validation
play sandbox preview
move piece
event log
save/load snapshot
restart from scenario
```

### 0.2 UX

```text
stronger validation
better error reporting
save compatibility warnings/blocks
authoring undo/redo
clearer package readiness
```

### 0.3 UX

```text
fuller authoring workspace
separate surfaces for map, pieces, scenario, rules metadata
optional save-as-new-scenario
better workflow from draft to playable package
```

### 0.4 UX

```text
assisted playtest
allowed actions
warnings
basic phase scaffolding
rules hooks visible through behavior, not hardcoded UI
```

### 0.5+ UX

```text
cards/decks
documents/player aids
asset library
package export/import
multiple modules
playtest sessions
```

### 1.0 UX

```text
module platform alpha:
create package
validate package
playtest package
save sessions
export/import package
support multiple modules
```

This aligns with the accepted post-0.1 platform roadmap. ([GitHub][9])

---

## Recommended next planning artifact

Recommended next artifact:

```text
product_ux_model.md
```

Suggested sections:

```text
1. Product UX principle
2. Daily designer loop
3. Workflow modes
4. Mode transition rules
5. Authoring vs playtest boundary
6. Package vs save boundary
7. 0.1 required UX
8. Later UX expansion
9. Anti-confusion rules
10. Anti-hardcoding rules for test module
```

### Not available / not verified

* Local repository, product code, runtime, tests, build, and actual UI implementation were not inspected.
* It is not verified whether any current prototype already implements these workflows.
* Exact screen layout, navigation, labels, component structure, and UI design are not specified here.
* Exact playtest session manager behavior is still open.
* Exact save-as-scenario workflow is still open beyond planning direction.
* Exact package export/import UX is not fixed.
* Exact runtime/player-facing UX is not fixed.
* This answer is a planning-only UX model proposal, not an accepted local implementation decision.

## Candidate Navigation Entry

V1-20260523-153658: Planning-only answer on target product UX model. Recommendation: treat the product as a workflow loop — Module Authoring Workspace creates/validates a module package, Play Sandbox Preview runs it through `GameState` and Action/Event pipeline, the designer inspects logs/errors, returns to authoring, fixes content/setup, and repeats; keep authoring, playtest/runtime, package, and save/snapshot workflows explicit so definitions, scenario setup, and runtime state do not mix.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_package_model.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-142942_planning-only-otvet-po-developer-side-authoring-workflow.md "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-150830_macro-roadmap-posle-table-sandbox-0-1.md "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-141825_planning-only-otvet-po-trem-ostavshimsya-voprosam-dlya.md "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-144154_planning-only-otvet-po-validation-undo-redo-i.md "raw.githubusercontent.com"
