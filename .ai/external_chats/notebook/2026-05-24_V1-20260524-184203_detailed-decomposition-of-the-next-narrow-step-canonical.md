# Notebook Entry

- External Question ID: `V1-20260524-184203`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-24_V1-20260524-184203_detailed-decomposition-of-the-next-narrow-step-canonical.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/pre_code_closure_and_first_execution_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/implementation/first_product_code_block.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/App.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/runtime/GameState.ts`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/runtime/actionEvent.ts`

## Candidate Navigation Entry

Topic: Detailed decomposition of the next narrow step, `Canonical Fixture Seed`
Summary: Recommendation: create a tiny data-only fixture set under `table-sandbox/src/fixtures/tiny-module/` with `project.json`, `module.json`, `map.json`, `scenario.basic.json`, `rules.metadata.json`, `savegame.empty.json`, and README; keep it neutral, internally consistent, and exclude loader/runtime/Phaser/prototype work until the next handoff.

## Raw Response

## External Question ID

V1-20260524-184203

## Context Readback

* Uploaded prompt / `Вставленный текст(21).txt`: fully read. 
* `external_chat_rules.md`: fully read. ([GitHub][1])
* Central `repo_navigation.md`: fully read. ([GitHub][2])
* Project `V1_navigation.md`: fully read for available current content. ([GitHub][3])
* Project `README.md`: opened; minimal/no readable body returned, treated as partially read. ([GitHub][4])
* Project `AGENTS.md`: fully read. ([GitHub][5])
* Project `.ai/repo_navigation.md`: opened; minimal/no readable body returned, treated as partially read. ([GitHub][6])
* `pre_code_closure_and_first_execution_plan.md`: opened; minimal/no readable body returned, treated as partially read. ([GitHub][7])
* `first_product_code_block.md`: opened; minimal/no readable body returned, treated as partially read. ([GitHub][8])
* Notebook `V1-20260524-182956_second-opinion...`: not read; raw link returned 404. 
* Notebook `V1-20260523-130238_minimal canonical file schemas`: fully read. ([GitHub][9])
* Notebook `V1-20260523-124734_table_sandbox_0_1 sequencing`: opened; minimal/no readable body returned, treated as partially read. ([GitHub][10])
* `table-sandbox/src/App.tsx`: opened; minimal/no readable body returned, treated as partially read. ([GitHub][11])
* `table-sandbox/src/runtime/GameState.ts`: fully read. ([GitHub][12])
* `table-sandbox/src/runtime/actionEvent.ts`: fully read. ([GitHub][13])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

`external_chat_rules.md` requires exact `External Question ID`, honest `Context Readback`, separation of central-doc conclusions, provided-context conclusions, and not-verified items. It also forbids claiming local repo/build/runtime/test access unless that was explicitly provided. ([GitHub][1])

Central `repo_navigation.md` says central navigation is a closed allowed-navigation set for `ai-workflow-core` and does not authorize consumer-repo claims unless consumer project files are explicitly provided. ([GitHub][2])

### Confirmed from provided excerpts

The uploaded prompt says the local orchestrator accepted the previous `0008 / Phase 1 - Technical Bootstrap` meaning: `table-sandbox/` exists, React owns runtime/debug state, Phaser is renderer/input only, green field is visible, clicks update debug/runtime state, and the chosen next candidate is `Canonical Fixture Seed`. I did not re-run that locally; this is provided context. 

Project `AGENTS.md` confirms the repo is about a browser-based authoring tool for 2D counter-based wargames, with Sword of Rome-like content as a first test module rather than the whole project; it also says Kilo should receive small isolated tasks. ([GitHub][5])

The minimal canonical file schemas notebook recommends the compact first file set: `project.json`, `module.json`, `map.json`, `scenario.*.json`, `rules.metadata.json`, and `savegame.json`, while keeping `map.json` as topology, `scenario.json` as initial setup, `rules.metadata.json` as declarative metadata, and `savegame.json` as runtime state rather than canonical definitions. ([GitHub][9])

Current `GameState.ts` is still a Phase 1 placeholder and explicitly says real structure will be expanded in Runtime/Data Bootstrap, while `actionEvent.ts` is also a placeholder seam with Action as request and Event as committed fact. That makes a data fixture step appropriate before expanding runtime structure. ([GitHub][12])

### Not available / not verified

I did not run local build, typecheck, dev server, browser, or tests. I did not inspect git status, local diffs, actual fixture folders, Vite config, CSS, or package lock. The provided notebook link for `V1-20260524-182956` returned 404, so I rely on the uploaded prompt's summary of that answer and on files that were readable. 

### Main assessment

`Canonical Fixture Seed` is the correct next small step. It is the smallest product-shaped move after Technical Bootstrap: it creates stable canonical data for the next slice without mixing in loader work, runtime refactor, Phaser rendering changes, or prototype migration.

### Recommended fixture scope

Recommended scope: **create tiny static JSON fixtures only**.

Do not implement a loader yet. Do not modify Phaser rendering yet. Do not implement `move_piece_requested -> piece_moved` yet. This step should only add the smallest internally consistent fixture set that the next handoff can load into `GameState`.

Include `savegame.empty.json`, but keep it intentionally minimal. It is useful now because it establishes the save/package boundary early. It should not be used to duplicate definitions.

### Recommended file tree

```text id="v1-20260524-184203-fixture-tree"
table-sandbox/
  src/
    fixtures/
      tiny-module/
        project.json
        modules/
          tiny-module/
            module.json
            map.json
            scenario.basic.json
            rules.metadata.json
        saves/
          savegame.empty.json
        README.md
```

`README.md` is optional but recommended because it can explain that this folder is a fixture seed, not production content.

### File roles

#### `project.json`

Should contain:

```text id="project-json-outline"
schemaVersion
projectId
name
activeModuleId
modules[]
```

Minimal values:

```text id="project-json-values"
projectId: "tiny-project"
activeModuleId: "tiny-module"
modules[0].moduleId: "tiny-module"
modules[0].path: "modules/tiny-module/module.json"
```

Should not contain: spaces, connections, piece instances, event log, current game state, rules logic, Phaser state.

#### `modules/tiny-module/module.json`

Should contain:

```text id="module-json-outline"
schemaVersion
moduleId
name
version
engineCompatibility
defaultMapId
defaultScenarioId
files
rules
factions[]
pieceDefinitions[]
```

Recommended compact 0.1 choice: keep very small `factions[]` and `pieceDefinitions[]` inside `module.json` for now. This matches the prior safe default for a first fixture seed and avoids creating `pieces.json` / `factions.json` too early. ([GitHub][9])

Minimal content:

```text id="module-json-values"
moduleId: "tiny-module"
defaultMapId: "tiny-map"
defaultScenarioId: "basic"
files.map: "map.json"
files.scenarios[0].scenarioId: "basic"
files.scenarios[0].path: "scenario.basic.json"
files.rulesMetadata: "rules.metadata.json"
rules.hookContractVersion: "0.1"
rules.automationLevel: "manual"
factions: tiny-red, tiny-blue
pieceDefinitions: infantry
```

Should not contain: map graph, current piece positions, event log, save state, executable rules.

#### `modules/tiny-module/map.json`

Should contain:

```text id="map-json-outline"
schemaVersion
mapId
moduleId
version
name
coordinateSystem
spaces[]
connections[]
zones[]
```

Minimum:

```text id="map-json-values"
mapId: "tiny-map"
moduleId: "tiny-module"
coordinateSystem.type: "pixel"
coordinateSystem.width: 800
coordinateSystem.height: 500
spaces:
  - space-a
  - space-b
connections:
  - connection-a-b from space-a to space-b
zones: []
```

Should not contain: piece instances, current control, event log, turn/phase, save state, rules logic.

#### `modules/tiny-module/scenario.basic.json`

Should contain:

```text id="scenario-json-outline"
schemaVersion
scenarioId
moduleId
mapId
name
setup
```

Minimum setup:

```text id="scenario-json-values"
turnState.round: 1
turnState.phaseId: "manual"
turnState.activeActorId: "designer"
pieces:
  - piece-1
    pieceDefId: "infantry"
    locationId: "space-a"
    ownerId: "tiny-red"
controlBySpace:
  space-a: "tiny-red"
  space-b: null
variables: {}
```

Should not contain: event log, save snapshots, full map graph, full rules logic, renderer camera, UI panel state.

#### `modules/tiny-module/rules.metadata.json`

Should contain:

```text id="rules-metadata-outline"
schemaVersion
rulesVersion
hookContractVersion
automationLevel
supportedActionTypes[]
supportedEventTypes[]
phases[]
```

Minimum:

```text id="rules-metadata-values"
automationLevel: "manual"
phases:
  - phaseId: "manual"
    name: "Manual Sandbox"
supportedActionTypes:
  - move_piece_requested
supportedEventTypes:
  - piece_moved
```

Should not contain: executable rule functions, actual hook implementation, current `GameState`, save data, event log, Phaser/DOM references.

#### `saves/savegame.empty.json`

Should contain a tiny empty/basic runtime snapshot reference:

```text id="savegame-outline"
schemaVersion
saveId
engineVersion
moduleId
moduleVersion
mapId
mapVersion
scenarioId
scenarioVersion
gameState
eventLog[]
```

For this step, either of these is acceptable, but choose one and be consistent:

```text id="savegame-options"
Recommended: gameState mirrors initial scenario setup with eventLog: []
Alternative: gameState is minimal placeholder marked as empty/unstarted
```

I recommend the first option: generate a simple initial snapshot from the scenario shape by hand. That gives the next loader/bootstrap step something concrete to compare against.

Should not contain: full `MapDefinition`, full `spaces[]`, full `connections[]`, full `pieceDefinitions[]`, full module manifest, executable rules, raw Phaser sprite state.

#### `README.md`

Should say:

```text id="fixture-readme-outline"
This is the tiny canonical fixture seed for Table Sandbox 0.1.
It is not a real game module.
It is used by the next Runtime/Data Bootstrap step.
Definitions live in module/map/scenario/rules files.
Runtime snapshot lives in saves/savegame.empty.json.
```

### IDs and consistency rules

Use stable, boring IDs:

```text id="ids"
projectId: tiny-project
moduleId: tiny-module
mapId: tiny-map
scenarioId: basic
saveId: tiny-empty-save
factionIds: tiny-red, tiny-blue
pieceDefId: infantry
pieceId: piece-1
spaceIds: space-a, space-b
connectionId: connection-a-b
phaseId: manual
```

Required consistency:

```text id="consistency"
project.activeModuleId == module.moduleId
project.modules[0].moduleId == module.moduleId
module.defaultMapId == map.mapId
module.defaultScenarioId == scenario.scenarioId
scenario.moduleId == module.moduleId
scenario.mapId == map.mapId
map.moduleId == module.moduleId
connection.fromSpaceId and toSpaceId exist in map.spaces
scenario.setup.pieces[0].pieceDefId exists in module.pieceDefinitions
scenario.setup.pieces[0].locationId exists in map.spaces or map.zones
scenario.setup.pieces[0].ownerId exists in module.factions
scenario.setup.turnState.phaseId exists in rules.metadata.phases
rules.supportedActionTypes includes move_piece_requested
rules.supportedEventTypes includes piece_moved
savegame module/map/scenario ids and versions match fixture files
savegame.eventLog is []
```

### What to exclude for now

Do not include:

```text id="exclusions"
loader implementation
runtime GameState expansion
Phaser rendering updates
piece movement implementation
Action/Event reducer changes
rules hook implementation
schema validator library
Zod/TypeScript schema generation
map editor prototype migration
asset pipeline
cards/decks
combat
hidden information
multiple scenarios
multiple maps
full Sword of Rome-like content
complex zones
directed connections
movement costs
advanced stack model
save migration logic
```

Keep this handoff as data-only.

### Acceptance checks

Codex should check after Kilo-run:

```text id="acceptance"
1. Fixture folder exists at the agreed path.
2. Exactly the requested core files exist.
3. JSON parses.
4. File roles are not mixed.
5. IDs are stable and human-readable.
6. All cross-file references resolve.
7. map.json contains topology only.
8. scenario.basic.json contains initial setup only.
9. rules.metadata.json contains metadata only, not executable rules.
10. savegame.empty.json does not duplicate map/piece/faction definitions.
11. supportedActionTypes includes move_piece_requested.
12. supportedEventTypes includes piece_moved.
13. phaseId "manual" is consistent between scenario and rules metadata.
14. There are no changes to Phaser rendering.
15. There is no loader implementation unless explicitly approved.
16. There is no prototype migration.
```

### Common failure modes

1. **Turning fixture seed into loader/runtime work.**
   This step should create data only. Loader is the next step.

2. **Putting piece definitions into scenario.**
   For this compact seed, put `pieceDefinitions[]` and `factions[]` in `module.json`; `scenario.basic.json` should contain piece instances only.

3. **Making `savegame.empty.json` a copy of the whole module.**
   Savegame should reference module/map/scenario versions and contain runtime state/event log, not duplicate canonical definitions.

4. **Using Sword-specific IDs too early.**
   Use neutral tiny IDs like `space-a`, `space-b`, `tiny-red`, `infantry`, not Rome/Carthage-specific names.

5. **Adding too much data.**
   Two spaces, one connection, one piece is enough for the next runtime slice.

### What Codex should ask Kilo to do next

```text id="kilo-handoff-content"
Task: Create Canonical Fixture Seed for table-sandbox.

Goal:
Add the smallest canonical fixture set needed for the next Runtime/Data Bootstrap step.

Scope:
Data-only fixture creation. Do not implement loader, renderer changes, move-piece runtime, schema library, or prototype migration.

Create:
table-sandbox/src/fixtures/tiny-module/project.json
table-sandbox/src/fixtures/tiny-module/modules/tiny-module/module.json
table-sandbox/src/fixtures/tiny-module/modules/tiny-module/map.json
table-sandbox/src/fixtures/tiny-module/modules/tiny-module/scenario.basic.json
table-sandbox/src/fixtures/tiny-module/modules/tiny-module/rules.metadata.json
table-sandbox/src/fixtures/tiny-module/saves/savegame.empty.json
table-sandbox/src/fixtures/tiny-module/README.md

Fixture content:
- one project: tiny-project
- one module: tiny-module
- one map: tiny-map
- two spaces: space-a, space-b
- one connection: connection-a-b
- one scenario: basic
- factions: tiny-red, tiny-blue
- one piece definition: infantry
- one piece instance: piece-1 at space-a owned by tiny-red
- one manual phase: manual
- supported action: move_piece_requested
- supported event: piece_moved
- empty/basic savegame with eventLog: []

Rules:
- map.json is topology only.
- scenario.basic.json is initial setup only.
- module.json is manifest plus compact 0.1 factions/pieceDefinitions.
- rules.metadata.json is declarative metadata only.
- savegame.empty.json is runtime/save artifact only and must not duplicate definitions.
- No Phaser changes.
- No loader implementation.
- No prototype migration.

Acceptance:
- all JSON files parse;
- all IDs and references are internally consistent;
- fixture is small enough for the next runtime bootstrap;
- no scope creep beyond fixture data.
```

## Candidate Navigation Entry

V1-20260524-184203: Detailed decomposition of the next narrow step, `Canonical Fixture Seed`. Recommendation: create a tiny data-only fixture set under `table-sandbox/src/fixtures/tiny-module/` with `project.json`, `module.json`, `map.json`, `scenario.basic.json`, `rules.metadata.json`, `savegame.empty.json`, and README; keep it neutral, internally consistent, and exclude loader/runtime/Phaser/prototype work until the next handoff.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/pre_code_closure_and_first_execution_plan.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/implementation/first_product_code_block.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/App.tsx "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/runtime/GameState.ts "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/runtime/actionEvent.ts "raw.githubusercontent.com"
