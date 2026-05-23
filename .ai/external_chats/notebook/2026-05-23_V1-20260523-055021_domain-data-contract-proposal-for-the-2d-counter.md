# Notebook Entry

- External Question ID: `V1-20260523-055021`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-055021_domain-data-contract-proposal-for-the-2d-counter.md`

## Context Links

- `https://chatgpt.com/c/6a10f53c-e758-83eb-b1d0-b4e7146e5e67`
- `https://chatgpt.com/c/6a10cfd2-8908-83eb-9381-728ec50eabe9`
- `https://chatgpt.com/c/6a10d2c8-71dc-83eb-96ff-e57659b4f89f`
- `https://chatgpt.com/c/6a0bc340-aafc-83eb-aa6c-37a4d7a572d9`
- `https://chatgpt.com/c/6a10e3c3-74d0-83eb-a2ea-37299d008467`
- `https://chatgpt.com/c/6a0cadc4-203c-8387-9090-913bcc2c5300`
- `https://chatgpt.com/c/6a0cacbb-b9e0-8384-9720-7b74055f3b89`
- `https://chatgpt.com/c/6a0c8773-da0c-8390-8ae9-d1c1fb5bfc77`
- `https://chatgpt.com/c/6a09a8f6-0278-8396-aed5-516e8faca4ed`
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

## Candidate Navigation Entry

Topic: Domain/data contract proposal for the 2D counter-based wargame authoring platform
Summary: Main recommendation: define `project.json`, `module.json`, `map.json`, `scenario.json`, `savegame.json`, and optional `rules.metadata.json`, with strict separation between immutable module definitions, scenario initial state, mutable save/runtime state, and module-specific rules hooks.

## Raw Response

## External Question ID

V1-20260523-055021

## Context Readback

* Uploaded task prompt / `Вставленный текст.txt`: fully read 
* Central rules — `external_chat_rules.md`: fully read ([GitHub][10])
* Central navigation — `repo_navigation.md`: fully read ([GitHub][11])
* Project repo navigation — `.ai/repo_navigation.md`: fully read ([GitHub][12])
* Project brief — `.ai/project_brief.md`: fully read ([GitHub][13])
* Project state — `.ai/project_state.md`: fully read ([GitHub][14])
* Project architecture — `.ai/architecture.md`: fully read ([GitHub][15])
* Project decisions — `.ai/decisions.md`: fully read ([GitHub][16])
* Main project context — `canon/context/sword_of_rome_web_project_context.md`: fully read ([GitHub][17])
* README: fully read ([GitHub][18])
* Navigation-discovered Project AGENTS — `AGENTS.md`: fully read ([GitHub][19])

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Domain Framing

Проект надо моделировать как **универсальную browser-based платформу для создания, настройки, плейтеста и дальнейшего розыгрыша 2D counter-based варгеймов**, а не как одну игру Sword of Rome. Это прямо подтверждается README, project brief, architecture/decisions и главным project context: Sword of Rome-like модуль — первый тестовый/reference module поверх универсального authoring/runtime tool. ([GitHub][18])

Главная domain boundary: **universal engine owns data shape, persistence, authoring tools, runtime state, actions/events; module package owns content definitions and rules hooks**. Inline planning context новее опубликованных architecture/decisions и уже фиксирует 4 слоя, `RulesHooksInterface`, `map.json`, `scenario.json`, `savegame.json`, а также принцип `Phaser is not source of truth`. 

Практическое правило: Phaser/React — presentation/input layer. Истина живёт в JSON definitions, `GameState`, `Action`, `Event` и save/log stream. Это совпадает с главным project context: Phaser не должен хранить истинное состояние, он только отображает состояние и превращает ввод пользователя в action/event. ([GitHub][17])

### Core Entities

| Entity                             | Role                                             | Required fields                                                      | Optional fields                                                             | Relations                                                   |
| ---------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `Project`                          | Workspace/root для authoring platform            | `projectId`, `name`, `schemaVersion`, `modules[]`                    | `activeModuleId`, `assetRoots`, `createdAt`, `updatedAt`                    | References `ModuleManifest` files                           |
| `ModulePackage`                    | Упакованный игровой модуль                       | `moduleId`, `manifest`, `content`, `rules`                           | `localization`, `documents`, `assets`                                       | Contains `MapDefinition`, scenarios, pieces, rules metadata |
| `ModuleManifest`                   | Entry point модуля                               | `moduleId`, `name`, `version`, `engineCompatibility`, `contentFiles` | `rulesEntry`, `rulesMetadataFile`, `defaultScenarioId`, `locale`            | References map/scenario/pieces/rules/docs/assets            |
| `Asset`                            | Raster map, counter image, icon, document, table | `assetId`, `type`, `path`                                            | `license`, `source`, `width`, `height`, `hash`                              | Referenced by map, pieces, documents                        |
| `MapDefinition`                    | Immutable-ish point-to-point map graph           | `mapId`, `version`, `coordinateSystem`, `spaces[]`, `connections[]`  | `zones[]`, `labels`, `visualLayers`, `mapSheetAssetId`                      | Referenced by scenarios and saves                           |
| `SpaceDefinition`                  | Node in point-to-point graph                     | `spaceId`, `nameKey`, `x`, `y`, `kind`                               | `radius`, `homeFactionId`, `tags`, `cityDefinition`, `port`, `victorySpace` | Connected by `ConnectionDefinition`; used as piece location |
| `ConnectionDefinition`             | Edge between spaces                              | `connectionId`, `fromSpaceId`, `toSpaceId`, `kind`                   | `tags`, `movementCost`, `visualPath`                                        | References two `SpaceDefinition` ids                        |
| `ZoneDefinition` / `BoxDefinition` | Off-map or table zone                            | `zoneId`, `nameKey`, `kind`                                          | `x`, `y`, `width`, `height`, `allowedPieceTypes`                            | Can be `locationId` for pieces                              |
| `FactionDefinition`                | Stable faction/player-side definition            | `factionId`, `nameKey`                                               | `colorToken`, `homeRegionTags`, `playerAssignable`                          | Used by spaces, pieces, scenario seats                      |
| `PieceDefinition`                  | Template/type of a counter                       | `pieceDefId`, `nameKey`, `kind`, `ownerFactionId` or `ownerType`     | `combatValues`, `imageAssetId`, `tags`, `stackingClass`                     | Referenced by `PieceInstance`                               |
| `PieceInstance`                    | Concrete counter in scenario/save                | `pieceId`, `pieceDefId`, `locationId`                                | `faceUp`, `rotation`, `status`, `side`, `ownerOverride`                     | References `PieceDefinition` and location                   |
| `ScenarioDefinition`               | Named initial setup template                     | `scenarioId`, `moduleId`, `mapId`, `initialState`                    | `description`, `playerSeats`, `startTurn`, `startPhase`, `setupRules`       | References map, factions, piece definitions                 |
| `ScenarioState`                    | Initial mutable values at scenario start         | `controlBySpace`, `cityStateBySpace`, `pieces[]`                     | `deckState`, `hands`, `markers`, `variables`                                | Becomes initial `GameState`                                 |
| `SaveGameState`                    | Concrete play session state                      | `saveId`, `moduleId`, `scenarioId`, `mapId`, `gameState`, `eventLog` | `players`, `rngState`, `undoStack`, `notes`                                 | References versions/hashes of definitions                   |
| `GameState`                        | Source-of-truth runtime state                    | `stateId`, `turnState`, `mapState`, `pieceState`, `mode`             | `deckState`, `ruleVariables`, `visibilityState`                             | Mutated only via accepted actions/events                    |
| `TurnState` / `PhaseState`         | Current temporal state                           | `round`, `phaseId`, `activeFactionId`                                | `stepId`, `initiative`, `pendingWindows`                                    | Used by rules hooks                                         |
| `Action`                           | Player/system request/intention                  | `actionId`, `type`, `actorId`, `payload`                             | `clientId`, `timestamp`, `correlationId`                                    | Validated by rules; may produce events                      |
| `Event`                            | Committed fact that changed state/log            | `eventId`, `seq`, `type`, `payload`, `causedByActionId`              | `timestamp`, `actorId`, `visibility`                                        | Replays into `GameState`                                    |
| `RulesHookContract`                | Boundary between runtime and module rules        | hook names, input/output schemas                                     | capabilities, phase metadata                                                | Runtime calls module rules; module rules do not own storage |
| `DocumentDefinition`               | Rules/player aid/reference docs                  | `documentId`, `titleKey`, `assetId` or `contentPath`                 | `category`, `pinnable`, `defaultOpen`                                       | Referenced by module manifest/UI                            |

### File Contract

Recommended minimal scalable structure:

```txt
project.json
modules/<moduleId>/module.json
modules/<moduleId>/map.json
modules/<moduleId>/scenario.<scenarioId>.json
modules/<moduleId>/rules.metadata.json
saves/<saveId>.savegame.json
```

Later, when content grows, split `pieces.json`, `factions.json`, `cards.json`, `documents.json`, `locales/*.json`, but do not split too early unless files become hard to review.

| File                             | Purpose                                         | Stores                                                                                                                                                                                                         | Does not store                                                                                              | Owner                                                                    |
| -------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `project.json`                   | Root workspace/index for the authoring platform | `projectId`, project name, `schemaVersion`, list of available modules, active module, asset roots, editor/project metadata                                                                                     | Map spaces, piece instances, scenario setup, game state, rules logic                                        | Layer 1 — Core Infrastructure + Project/Data Model                       |
| `module.json` / `ModuleManifest` | Entry point for one playable/editable module    | `moduleId`, `name`, `version`, `engineCompatibility`, content file paths, default map/scenario, rules metadata pointer, rules hook entry pointer, assets/docs/locales index                                    | Full map graph, full scenario state, full save state, executable rules implementation                       | Layer 4 — Module Package / Module Content                                |
| `map.json`                       | Stable map graph and board definition           | `mapId`, `version`, coordinate system, map sheet asset reference, spaces, connections, off-map boxes/zones, label definitions, visual layer metadata                                                           | Current control, current piece positions, action log, current phase, save-specific state                    | Module Content, validated by Layer 1 schema; edited by Layer 2 Authoring |
| `scenario.json`                  | Initial setup template for a play session       | `scenarioId`, `moduleId`, `mapId`, player seats, starting turn/phase, starting control, city states, initial piece instances, setup variables                                                                  | Ongoing play history, event log after start, UI camera/panel state, changed runtime state after play begins | Module Content; authored by Layer 2; consumed by Layer 3 Runtime         |
| `savegame.json`                  | Concrete state of an actual session/playtest    | `saveId`, referenced `moduleId`, `moduleVersion`, `scenarioId`, `mapId`, definition hashes, current `GameState`, event log, current phase/turn, mutable piece/map/city/control state, RNG seed/state if needed | Authoring definitions, map graph edits, piece definitions, executable rules logic, raster assets            | Layer 3 Runtime/Play + Layer 1 Persistence                               |
| `rules.metadata.json`            | Declarative metadata for module rules/hooks     | `rulesVersion`, `hookContractVersion`, supported action types, phase ids, rule variants, automation level, visibility capabilities, optional schemas for actions                                               | The actual source of truth state, full rule code, save data, hidden side effects                            | Module Rules/Hooks                                                       |
| Optional `pieces.json`           | Scalable split for piece/faction definitions    | `PieceDefinition[]`, optionally `FactionDefinition[]`                                                                                                                                                          | Concrete piece locations and current damage/status unless those are definition defaults                     | Module Content                                                           |
| Optional `documents.json`        | Rules/player aid/document registry              | document ids, categories, file refs, title keys                                                                                                                                                                | Runtime pinned window positions, player-specific UI state                                                   | Module Content + DocumentsModule                                         |

`ModuleManifest` is needed. Without it, the runtime will have to guess which map/scenario/rules/assets belong together. Minimum `ModuleManifest` fields:

```txt
moduleId
name
version
engineCompatibility
schemaVersions
contentFiles: { map, scenarios, pieces?, factions?, cards?, documents? }
defaultMapId
defaultScenarioId
rules: { metadataFile?, hookEntry?, hookContractVersion, automationLevel }
assets: { root, manifestFile? }
localization: { defaultLocale, files? }
```

### Entity Ownership By Layer

| Layer                                     | Owns                                                                                                                                                | Must not own                                                                                              |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Core Infrastructure + Project/Data Model  | Schemas, IDs, file loading, validation, migrations, persistence, canonical `Action`/`Event` envelope, `GameState` shape, reference integrity        | Module-specific victory rules, faction-specific exceptions, Phaser sprite state                           |
| Universal Authoring / Editor Capabilities | Editing workflows for maps, spaces, connections, pieces, scenarios, documents, JSON import/export, validation display                               | Runtime authority over legal play, hidden rule decisions, committed event semantics                       |
| Universal Runtime / Play Sandbox          | Session creation, applying validated actions, event log, save/load, undo/replay basis, player view preparation later                                | Game-specific rules hardcoded into engine, module content definitions                                     |
| Module Content                            | Module manifest, map graph, piece/faction/card definitions, scenarios, documents, assets, localization                                              | Mutable save state, generic engine schemas, universal persistence                                         |
| Module Rules/Hooks                        | `getAllowedActions`, `validateAction`, `getPhaseActions`, `onPhaseStart`, `checkWinCondition`, rule metadata, action-specific validation/derivation | Direct file writes, Phaser/DOM mutation, hidden state mutation without events, universal schema ownership |

Boundary recommendation: **runtime asks rules hooks questions; rules hooks return structured answers; runtime applies state transitions and appends events**. For early versions, hooks may be "manual permissive", but the interface should already exist.

### Definitions vs Runtime State

**Immutable or release-stable definitions**

* `ModuleManifest`
* `FactionDefinition`
* `PieceDefinition`
* `MapDefinition`
* `SpaceDefinition`
* `ConnectionDefinition`
* `ZoneDefinition`
* `DocumentDefinition`
* `CardDefinition` later
* `RulesMetadata`
* Published `ScenarioDefinition`

These can be edited in Designer/Authoring mode, but once a scenario/save references a released version, treat them as immutable for that save unless migration is explicit.

**Mutable runtime state**

* `SaveGameState`
* `GameState`
* `TurnState` / `PhaseState`
* `PieceInstance.locationId`
* `PieceInstance.faceUp/status/rotation/side`
* current `controlBySpace`
* current `cityStateBySpace`
* current markers
* current deck/hand/discard state later
* event log
* rule variables
* RNG state
* pending action windows

**Important separations**

* `PieceDefinition` = what a counter type is. Example: "Roman combat unit", art, base values, owner faction, tags.
* `PieceInstance` = one concrete counter in a scenario/save. Example: `rome_cu_001` at `rome`, face up, status normal.
* `MapDefinition` = graph and geometry: spaces/connections/zones.
* `ScenarioState` = starting setup over that map: initial control, initial pieces, initial city states.
* `SaveGameState` = current state after actions/events changed the scenario.
* `Module Content` = declarative game material.
* `Module Rules metadata` = declarative description of rules capabilities/phases/actions.
* `Module Rules hooks` = executable or callable logic behind the boundary.
* `Action` = request: "move this piece from A to B".
* `Event` = committed fact: "piece moved from A to B as event sequence 42".

### Validation Rules And Invariants

Minimum validation should run at four moments: file load, authoring export, scenario start, save load.

1. **Unique IDs**

   * IDs unique within namespace: `moduleId`, `mapId`, `spaceId`, `connectionId`, `pieceDefId`, `pieceId`, `scenarioId`, `saveId`.
   * Prefer typed IDs or prefixes: `space:rome`, `pieceDef:roman_cu`, `piece:rome_cu_001`.

2. **Reference integrity**

   * Every `connection.fromSpaceId` and `toSpaceId` must exist.
   * Every `PieceInstance.pieceDefId` must exist.
   * Every `PieceInstance.locationId` must reference a `SpaceDefinition` or `ZoneDefinition`.
   * Every scenario `mapId` must match an existing `MapDefinition`.
   * Every save must reference known `moduleId`, `scenarioId`, `mapId`, and compatible definition versions/hashes.

3. **Versioning**

   * Every file has `schemaVersion`.
   * Module has `moduleVersion`.
   * Save stores `engineVersion`, `moduleVersion`, `mapVersion`, `scenarioVersion`, and ideally content hashes.
   * If hashes mismatch, load should be blocked, warning-only, or migration-required; do not silently accept.

4. **Layer ownership boundaries**

   * `map.json` cannot contain current piece positions or action log.
   * `scenario.json` cannot contain post-play event history.
   * `savegame.json` cannot redefine map graph or piece definitions.
   * `rules.metadata.json` cannot be the source of mutable game state.
   * Phaser sprite state cannot be serialized as canonical game state.

5. **Action/Event invariants**

   * Every committed `Event` has monotonic `seq`.
   * Every event caused by player input links to `causedByActionId`.
   * Events are replayable against a prior state.
   * Actions may fail validation; failed actions should not mutate `GameState`.
   * If an action produces multiple events, event ordering must be deterministic.

6. **Map graph invariants**

   * Connections cannot reference missing spaces.
   * Duplicate undirected connections should be rejected unless explicitly allowed.
   * Coordinates must be inside declared map coordinate system or explicitly marked off-map.
   * `kind` values must come from known enums or module-declared extensions.

7. **Runtime state invariants**

   * A `PieceInstance` has one canonical location.
   * A stack is derived from pieces sharing `locationId`; it is not a separate source of truth unless later needed for ordering.
   * Current control is runtime/scenario/save state, while `homeFactionId` is definition/default identity.
   * UI selection, hover, camera, open panels should not be part of canonical `GameState`; keep them in local UI state or optional user preferences.

8. **Rules hook invariants**

   * Hooks should be deterministic for the same input.
   * Hooks should not mutate passed state directly.
   * Hooks should return validation result, allowed actions, derived events, phase actions, or win condition result.
   * Runtime remains responsible for applying returned events and persisting state.

### Data Model Risks

1. **Hardcoding Sword of Rome into universal schema.** Keep Sword of Rome-like concepts as module content/rules unless they are truly generic: spaces, connections, pieces, scenarios, actions, events.

2. **Mixing definitions and runtime state.** The most dangerous version is putting current control/piece positions/action log into `map.json`.

3. **Letting Phaser become the source of truth.** Sprite coordinates can exist for rendering, but piece truth should be `locationId`, not sprite `x/y`. The project context explicitly warns against Phaser sprites holding true game state. ([GitHub][17])

4. **No `ModuleManifest`.** Without a manifest, module loading becomes path guessing and later breaks when cards, documents, localization, assets, and rules hooks appear.

5. **Confusing Action with Event.** Actions are intentions/requests; events are committed facts. Mixing them will hurt undo, replay, online sync, validation, and debugging.

6. **Making `savegame.json` a giant all-purpose archive.** A save should reference definitions by id/version/hash, not copy/redefine the whole module.

7. **Putting executable rule logic into JSON metadata.** `rules.metadata.json` should describe hooks/capabilities/phases/action types, not become a pseudo-programming language.

8. **No migration/version strategy.** Even simple authoring tools quickly create old saves and old scenarios. Define compatibility behavior early: strict block, warning, or explicit migration.

### Recommended Next Planning Artifact

Recommended next artifact: **`domain_schemas_contract.md`**.

It should combine three things in one compact planning document:

1. **Glossary** — canonical meanings of `Project`, `Module`, `MapDefinition`, `ScenarioDefinition`, `ScenarioState`, `SaveGameState`, `Action`, `Event`, `PieceDefinition`, `PieceInstance`.
2. **File schemas doc** — practical JSON contract for `project.json`, `module.json`, `map.json`, `scenario.json`, `savegame.json`, `rules.metadata.json`.
3. **Boundary/invariants section** — what each layer owns, what each file must not contain, and validation rules.

After that, the next separate artifact should be **`rules_hooks_interface.md`**, because `RulesHooksInterface` is a clean boundary and should not be buried inside broad architecture prose.

### Not available / not verified

* I did not inspect local filesystem, local git, runtime, tests, or actual product-code implementation.
* Published README/project state say the repo mostly contains context/workflow/canon and that the first product-code block is not yet implemented as a working app. ([GitHub][18])
* Exact folder layout for future product code is not verified as accepted implementation.
* Exact JSON schema syntax, Zod implementation, migrations, and TypeScript types are not available in the provided context.
* Exact Sword of Rome-like rule details are not needed for this domain contract and were not validated here.

## Candidate Navigation Entry

V1-20260523-055021: Domain/data contract proposal for the 2D counter-based wargame authoring platform. Main recommendation: define `project.json`, `module.json`, `map.json`, `scenario.json`, `savegame.json`, and optional `rules.metadata.json`, with strict separation between immutable module definitions, scenario initial state, mutable save/runtime state, and module-specific rules hooks.

[1]: https://chatgpt.com/c/6a10f53c-e758-83eb-b1d0-b4e7146e5e67 "Проект Sword of Rome"
[2]: https://chatgpt.com/c/6a10cfd2-8908-83eb-9381-728ec50eabe9 "External context review"
[3]: https://chatgpt.com/c/6a10d2c8-71dc-83eb-96ff-e57659b4f89f "Проверка после smoke"
[4]: https://chatgpt.com/c/6a0bc340-aafc-83eb-aa6c-37a4d7a572d9 "Проект Sword of Rome"
[5]: https://chatgpt.com/c/6a10e3c3-74d0-83eb-a2ea-37299d008467 "Проект для 2D варгеймов"
[6]: https://chatgpt.com/c/6a0cadc4-203c-8387-9090-913bcc2c5300 "P3.1 Narrow Design Proposal"
[7]: https://chatgpt.com/c/6a0cacbb-b9e0-8384-9720-7b74055f3b89 "P3.1 Scope and Proposal"
[8]: https://chatgpt.com/c/6a0c8773-da0c-8390-8ae9-d1c1fb5bfc77 "Технические детали маршрута"
[9]: https://chatgpt.com/c/6a09a8f6-0278-8396-aed5-516e8faca4ed "Static Manual Critique"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_brief.md "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/canon/context/sword_of_rome_web_project_context.md "raw.githubusercontent.com"
[18]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md "raw.githubusercontent.com"
[19]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md "raw.githubusercontent.com"
