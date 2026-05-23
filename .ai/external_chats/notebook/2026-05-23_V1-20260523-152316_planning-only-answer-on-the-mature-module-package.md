# Notebook Entry

- External Question ID: `V1-20260523-152316`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-152316_planning-only-answer-on-the-mature-module-package.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-141825_planning-only-otvet-po-trem-ostavshimsya-voprosam-dlya.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-142942_planning-only-otvet-po-developer-side-authoring-workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-150830_macro-roadmap-posle-table-sandbox-0-1.md`

## Candidate Navigation Entry

Topic: Planning-only answer on the mature `module package` model
Summary: Recommendation: evolve from compact `0.1` layout toward a validated, versioned package with `module.json` as manifest, separate maps/scenarios/content/rules/documents/assets/locales/package metadata, and keep `savegame.json` outside canonical module content; split `pieces.json` and `factions.json` out of `module.json` once content grows beyond tiny test-module scale.

## Raw Response

## External Question ID

V1-20260523-152316

## Context Readback

* Uploaded prompt / `Вставленный текст(14).txt` — fully read. 
* `external_chat_rules.md` — fully read. ([GitHub][1])
* `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — fully read. ([GitHub][4])
* `domain_schemas_contract.md` — fully read. ([GitHub][5])
* `minimal_canonical_file_schemas.md` — fully read. ([GitHub][6])
* `module_authoring_workflow.md` — fully read. ([GitHub][7])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][8])
* `post_0_1_platform_roadmap.md` — fully read. ([GitHub][9])
* `action_event_contract.md` — fully read. ([GitHub][10])
* `rules_hooks_interface.md` — fully read. ([GitHub][11])
* Project `V1_navigation.md` — fully read. ([GitHub][12])
* V1-navigation-discovered `V1-20260523-141825` notebook entry — fully read. ([GitHub][13])
* V1-navigation-discovered `V1-20260523-142942` notebook entry — partially read. ([GitHub][14])
* V1-navigation-discovered `V1-20260523-130238` notebook entry — partially read. ([GitHub][15])
* V1-navigation-discovered `V1-20260523-150830` notebook entry — partially read. ([GitHub][16])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require honest `Context Readback`, separation between central-doc conclusions, project-specific conclusions, and not-verified material. They also prohibit claiming local repo/runtime/test access unless that was explicitly provided. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation covers `ai-workflow-core` only and does not authorize claims about a consumer repo unless consumer-project files are explicitly provided. ([GitHub][2])

For this question, central docs define answer discipline only. They do not define the mature `module package` model.

### Confirmed from provided excerpts

The accepted base is that this project is a universal browser-based 2D wargame authoring/runtime platform, not a hardcoded Sword of Rome-like game. The four-layer architecture separates core/data model, universal authoring, universal runtime/play sandbox, and module package with content plus rules/hooks. ([GitHub][3])

The mature `module package` should therefore be treated as a **product entity**: a portable, validated, versioned bundle of module content and module-specific rules boundary metadata that the universal platform can load, edit, validate, preview, save against, and later export/import. It should not be a dump of runtime saves, and it should not contain hidden hardcoded engine logic. ([GitHub][5])

---

## Target mature package model

Recommended mature package shape:

```text
modules/<moduleId>/
  module.json

  maps/
    <mapId>.map.json

  scenarios/
    <scenarioId>.scenario.json

  content/
    factions.json
    pieces.json
    cards.json              optional
    decks.json              optional
    markers.json            optional later

  rules/
    rules.metadata.json
    hooks/                  optional / implementation-dependent later

  documents/
    documents.json          optional
    player-aids/            optional

  assets/
    assets.json             optional but practically important
    images/
    maps/
    counters/
    cards/

  locales/
    ru.json                 optional
    en.json                 optional

  package/
    package.metadata.json   optional later
    validation.report.json  generated, optional
    changelog.md            optional
    license.md              optional
```

This structure is not needed in full for `Table Sandbox 0.1`. It is the **mature target**. The 0.1 compact layout should remain smaller and evolve toward this shape gradually. The already accepted compact 0.1 layout begins with `project.json`, `module.json`, `map.json`, `scenario.<scenarioId>.json`, `rules.metadata.json`, and `savegame.json`, while keeping definitions/runtime/rules separate. ([GitHub][6])

---

## Package groups

### 1. Core required files

#### `module.json`

**Required:** yes.

**Responsibility:** module manifest / entry point. It tells the platform what the module is, which files belong to it, which map/scenario are default, which schema versions are used, and where rules metadata lives.

**Should link to:**

```text
maps
scenarios
rules.metadata.json
pieces/factions files later
cards/decks later
documents/assets/locales later
```

**Should contain:**

```text
moduleId
name
version
engineCompatibility
schemaVersions
defaultMapId
defaultScenarioId
files
rules metadata pointer
optional package metadata pointer later
```

**Should not contain:**

```text
full map graph
current GameState
eventLog
save data
runtime piece positions
executable rules logic
large content dumps in mature format
```

For `0.1`, small `PieceDefinition[]` and `FactionDefinition[]` inside `module.json` are acceptable as a compact first-milestone simplification, but the mature package should move them out to dedicated files. ([GitHub][13])

---

#### `maps/<mapId>.map.json`

**Required:** yes, at least one map for a map-based module.

**Responsibility:** map/topology definition.

**Should contain:**

```text
mapId
moduleId
schemaVersion
version
coordinateSystem
background / map asset reference
spaces[]
connections[]
zones[]
optional visual metadata
```

**Should link to:**

```text
module.json
assets map image references
scenario.locationId references
savegame location references
```

**Should not contain:**

```text
current piece positions
current control
current phase
eventLog
save state
scenario setup
rules behavior
```

This preserves the accepted boundary: `map.json` is map definition, not runtime state. ([GitHub][5])

---

#### `scenarios/<scenarioId>.scenario.json`

**Required:** yes, at least one default scenario.

**Responsibility:** initial setup template.

**Should contain:**

```text
scenarioId
moduleId
mapId
name
initial turn/phase
initial piece instances
initial controlBySpace
initial variables
setup notes
```

**Should link to:**

```text
mapId
pieceDefId
factionId / ownerId
spaceId / zoneId
rules.metadata phases
```

**Should not contain:**

```text
post-start event log
current save history
full map graph
full piece definitions
runtime undo stack
current playtest-only state
```

A scenario is "how the game starts," not "what happened during playtest." This boundary is already part of the accepted file contract. ([GitHub][5])

---

#### `rules/rules.metadata.json`

**Required:** yes, even for manual modules.

**Responsibility:** declarative metadata about rules capabilities, action/event types, phases, automation level, and hook contract version.

**Should contain:**

```text
rulesVersion
hookContractVersion
automationLevel
supportedActionTypes[]
supportedEventTypes[]
phases[]
rule options / variants later
```

**Should link to:**

```text
module.json rules pointer
scenario start phase
runtime Action/Event contract
RulesHooksInterface version
```

**Should not contain:**

```text
executable rules code
hidden mutable state
save data
GameState
Phaser/DOM references
direct persistence logic
```

This is important because the rules boundary is already fixed: runtime asks, module rules answer, runtime applies and logs. Rules metadata must not become a hidden scripting language or a place for executable logic. ([GitHub][11])

---

### 2. Gameplay content files

#### `content/factions.json`

**Required in mature package:** practically yes for most counter-based games.
**Optional in 0.1 compact layout:** yes; can temporarily live in `module.json`.

**Responsibility:** stable faction/player-side definitions.

**Should contain:**

```text
factionId
name
color / display hints
playerAssignable
optional tags
```

**Should link to:**

```text
PieceDefinition.ownerFactionId
Scenario player seats
controlBySpace
rules hooks
```

**Should not contain:**

```text
current score
current control state
current player decisions
runtime diplomacy/state
```

Current control belongs to scenario setup or save/runtime state, not to faction definitions.

---

#### `content/pieces.json`

**Required in mature package:** yes for counter-based modules.
**Optional in 0.1 compact layout:** can temporarily live in `module.json`.

**Responsibility:** `PieceDefinition[]`, not concrete pieces on the board.

**Should contain:**

```text
pieceDefId
name
kind
ownerFactionId or ownerType
imageAssetId
base values
tags
stackingClass optional later
```

**Should link to:**

```text
scenario setup PieceInstance.pieceDefId
savegame GameState piecesById[*].pieceDefId
assets/counter images
rules hooks
```

**Should not contain:**

```text
PieceInstance[]
current locationId
current status
current face-up/hidden runtime state
event log
```

The existing domain model already separates `PieceDefinition` from `PieceInstance`; mature package format should preserve that separation. ([GitHub][5])

---

#### `content/cards.json` and `content/decks.json`

**Required:** optional. Needed only for card-driven or card-assisted modules.

**Responsibility:** generic card and deck definitions.

**Should contain:**

```text
cardId
deckId
title
text
type
artAssetId
tags
deck composition
```

**Should link to:**

```text
assets card images
rules hooks for card effects
scenario initial deck setup
runtime deck/hand/discard state
```

**Should not contain:**

```text
current hand contents
current deck order
discard pile runtime state
executable card effects embedded as code
```

Card definitions are content. Current hands/decks/discards are runtime state. Card effects should route through module rules/hooks, not through executable code hidden inside JSON metadata. ([GitHub][9])

---

### 3. Rich content / reference files

#### `documents/documents.json`

**Required:** optional, but important for richer modules.

**Responsibility:** rules references, player aids, charts, setup notes, examples.

**Should contain:**

```text
documentId
title
category
path
language
related scenario/card/faction references optional
```

**Should link to:**

```text
assets or document files
module.json file pointers
UI document surface
```

**Should not contain:**

```text
runtime state
save data
rules execution
current open window state as canonical truth
```

---

#### `assets/assets.json`

**Required:** optional in pure data tests; practically required for real visual modules.

**Responsibility:** asset registry.

**Should contain:**

```text
assetId
type
path
width/height optional
hash optional later
license/source optional
```

**Should link to:**

```text
map background
piece images
card art
documents
module manifest
```

**Should not contain:**

```text
runtime sprite positions
Phaser scene state
current selection
editor camera as canonical game truth
```

Assets are resources. They are not game state.

---

#### `locales/*.json`

**Required:** optional.

**Responsibility:** translations/localized names and text.

**Should contain:**

```text
translation keys
localized names
localized card text
localized document titles
```

**Should link to:**

```text
module content ids
UI language settings
```

**Should not contain:**

```text
rules behavior
runtime state
save data
```

---

### 4. Runtime/save files

#### `saves/<saveId>.savegame.json`

**Required part of canonical module package:** no.

**Responsibility:** current playtest/session state.

**May be stored near project:** yes.
**May be bundled as examples/test fixtures later:** yes, but clearly outside canonical module content.

**Should contain:**

```text
saveId
engineVersion
moduleId
moduleVersion
mapId
mapVersion
scenarioId
scenarioVersion
GameState
eventLog[]
```

**Should link to:**

```text
moduleId
mapId
scenarioId
pieceDefId
locationId
rules metadata version
```

**Should not contain:**

```text
full MapDefinition
full PieceDefinition catalog
full FactionDefinition catalog
module manifest copy
executable rules
canonical content definitions
```

This is one of the most important package boundaries: `savegame.json` is not part of canonical module content. It references the module package; it does not define the module package. ([GitHub][5])

---

### 5. Packaging / publishing metadata

#### `package/package.metadata.json`

**Required:** optional later.

**Responsibility:** distribution metadata, not gameplay data.

**Should contain later:**

```text
packageId
moduleId
packageVersion
author
license
description
engineCompatibility
content hashes
createdAt / publishedAt optional
dependencies optional later
```

**Should link to:**

```text
module.json
assets
validation report
publish/import/export tools
```

**Should not contain:**

```text
game state
scenario setup
rules behavior
map topology
piece definitions
```

This becomes useful when module import/export and compatibility policies mature, but it is too heavy for `0.1`.

---

## Required vs optional package parts

### Almost every mature module package needs

```text
module.json
one or more maps
one or more scenarios
rules.metadata.json
factions
pieces
basic assets, if visual
validation-readable schema versions
```

### Richer modules may add

```text
cards
decks
documents
player aids
localization
asset catalog
rules variants
scenario variants
package metadata
validation report
changelog/license
```

### Runtime/session layer, not canonical module content

```text
savegame.json
autosaves
playtest sessions
event logs from played games
runtime undo stacks
player-specific hidden views
```

Saves may reference package content, but should not be treated as canonical content. This protects the package from becoming a dump of whatever happened in a playtest. ([GitHub][5])

---

## Evolution path

### Stage A — compact `0.1` layout

Good for `Table Sandbox 0.1`:

```text
project.json
modules/<moduleId>/module.json
modules/<moduleId>/map.json
modules/<moduleId>/scenario.basic.json
modules/<moduleId>/rules.metadata.json
saves/<saveId>.savegame.json
```

Temporary compact choice:

```text
module.json may contain small factions[]
module.json may contain small pieceDefinitions[]
```

This is acceptable only while the module is tiny and the goal is to prove the first vertical slice. Prior V1 planning already recommended this compact layout as a safe first milestone compromise, not a mature target. ([GitHub][13])

---

### Stage B — intermediate package format

Move from "small proof" to "real module editing":

```text
modules/<moduleId>/
  module.json
  map.json or maps/<mapId>.map.json
  scenarios/<scenarioId>.scenario.json
  content/
    factions.json
    pieces.json
  rules/
    rules.metadata.json
  assets/
    assets.json optional
```

At this stage:

* `module.json` becomes mostly manifest again;
* `scenario.json` references `pieceDefId`, not inline piece definitions;
* `savegame.json` remains outside canonical content;
* module validation becomes more important;
* multiple scenarios become realistic.

This matches the accepted roadmap direction: after `0.1`, strengthen validation/save compatibility, expand authoring surfaces, and then add assisted runtime and richer content. ([GitHub][9])

---

### Stage C — mature package format

Target for platform alpha / richer modules:

```text
modules/<moduleId>/
  module.json

  maps/
  scenarios/
  content/
    factions.json
    pieces.json
    cards.json
    decks.json
    markers.json optional

  rules/
    rules.metadata.json
    hooks/ optional later

  documents/
  assets/
  locales/
  package/
```

At this stage, the package is a real product artifact:

* portable;
* validated;
* versioned;
* importable/exportable;
* reusable across multiple scenarios;
* compatible with multiple module types;
* not hardcoded to Sword of Rome-like assumptions.

---

## Triggers for extracting content out of `module.json`

Move `factions[]` and `pieceDefinitions[]` out of `module.json` when any of these happens:

```text
more than 10–20 piece definitions
more than 4–6 factions
multiple scenarios reuse the same piece catalog
piece definitions need image/icon references
piece definitions have multiple categories or shapes
a dedicated pieces/factions editor surface appears
module.json becomes hard to read
cards/decks/documents/localization appear
validation needs separate content-level reports
Sword of Rome-like content starts growing beyond tiny reference data
```

The previous V1 answer already identified the same direction: compact definitions in `module.json` are fine for 0.1, but mature package should use `pieces.json` and `factions.json`. ([GitHub][13])

---

## Anti-bloat / anti-hardcoding rules

1. **Do not let `module.json` become a content dump.**
   It starts compact in 0.1, but mature `module.json` should be a manifest.

2. **Do not put runtime state into content files.**
   `map.json` is not a save. `scenario.json` is not a play log. `rules.metadata.json` is not mutable state.

3. **Do not put canonical definitions into `savegame.json`.**
   Save files reference module content. They do not define module content.

4. **Do not put executable rules into `rules.metadata.json`.**
   Rules behavior belongs behind the rules hooks boundary. Metadata only describes capabilities, phases, action/event types, automation level, and versions. ([GitHub][11])

5. **Do not shape the package around Sword of Rome-like content too early.**
   If a field only makes sense for the Sword of Rome-like module, it should be module content or module rules, not universal package format.

6. **Keep at least one tiny generic test module.**
   A neutral module helps verify that package format remains platform-level, not one-game-specific.

7. **Version everything that affects compatibility.**
   At minimum: module version, schema versions, map/scenario/rules versions. Content hashes can come later. Prior planning already recommended limited compatibility now and migration later. ([GitHub][13])

---

## Safe default now

For `Table Sandbox 0.1`:

```text
Keep package compact.
Keep module.json as manifest plus tiny temporary factions/pieceDefinitions.
Keep one map.
Keep one scenario.
Keep one rules.metadata.json.
Keep savegame outside canonical module content.
Do not add mature package folders until the module actually grows.
```

This avoids painful overengineering and still keeps a clear migration path.

---

## Intermediate package shape

For post-0.1 / 0.2–0.3:

```text
module.json
maps/map.json or maps/<mapId>.map.json
scenarios/basic.scenario.json
content/factions.json
content/pieces.json
rules/rules.metadata.json
assets/assets.json optional
```

This is the best next structural step once the first editor surfaces become useful.

---

## Mature package shape

For platform alpha / 1.0-level package:

```text
module.json
maps/
scenarios/
content/
rules/
documents/
assets/
locales/
package/
```

This makes the package understandable as a product: module manifest, content definitions, scenario setup, rules boundary, reference materials, assets, localization, and packaging metadata are separate but connected.

---

### Not available / not verified

* Local repository, product code, actual JSON files, tests, build, and runtime were not inspected.
* It is not verified whether any current local implementation already matches or conflicts with this package model.
* Exact folder names are not accepted implementation decisions.
* Exact JSON Schema / Zod / TypeScript types are not fixed here.
* Exact package importer/exporter behavior is not specified here.
* Exact rules hook implementation packaging is still open.
* Exact content hash and migration policy remain open.
* Exact threshold for splitting files is a planning recommendation, not a final local decision.
* This answer is a planning-only proposal, not an accepted local implementation decision.

## Candidate Navigation Entry

V1-20260523-152316: Planning-only answer on the mature `module package` model. Recommendation: evolve from compact `0.1` layout toward a validated, versioned package with `module.json` as manifest, separate maps/scenarios/content/rules/documents/assets/locales/package metadata, and keep `savegame.json` outside canonical module content; split `pieces.json` and `factions.json` out of `module.json` once content grows beyond tiny test-module scale.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/post_0_1_platform_roadmap.md
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-141825_planning-only-otvet-po-trem-ostavshimsya-voprosam-dlya.md
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-142942_planning-only-otvet-po-developer-side-authoring-workflow.md
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-150830_macro-roadmap-posle-table-sandbox-0-1.md
