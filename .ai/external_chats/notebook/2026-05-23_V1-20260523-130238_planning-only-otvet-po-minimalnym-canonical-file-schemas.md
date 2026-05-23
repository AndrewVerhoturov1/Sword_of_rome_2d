# Notebook Entry

- External Question ID: `V1-20260523-130238`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-055021_domain-data-contract-proposal-for-the-2d-counter.md`

## Candidate Navigation Entry

Topic: Planning-only ответ по минимальным canonical file schemas для `Table Sandbox 0.1`
Summary: Рекомендация: начать с компактного набора `project.json`, `module.json`, `map.json`, `scenario.<scenarioId>.json`, `rules.metadata.json`, `savegame.json`, строго разделив workspace/module manifest, map definitions, scenario initial setup, rules metadata и mutable save/runtime state; первый slice должен сохранить путь к Action/Event pipeline и не превращать `savegame.json` или `map.json` в скрытые хранилища definitions/runtime state.

## Raw Response

# External Chat Raw Response

## External Question ID

V1-20260523-130238

## Context Readback

* `external_chat_rules.md` — fully read. ([GitHub][1])
* `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — fully read. ([GitHub][4])
* `domain_schemas_contract.md` — fully read. ([GitHub][5])
* `rules_hooks_interface.md` — fully read. ([GitHub][6])
* `action_event_contract.md` — fully read. ([GitHub][7])
* `first_milestone_runtime_skeleton.md` — fully read. ([GitHub][8])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][9])
* `V1_navigation.md` — fully read. ([GitHub][10])
* V1-navigation-discovered `V1-20260523-124734` notebook entry — fully read. ([GitHub][11])
* V1-navigation-discovered `V1-20260523-062449` notebook entry — fully read. ([GitHub][12])
* V1-navigation-discovered `V1-20260523-055021` notebook entry — fully read. ([GitHub][13])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond the required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules требуют честный `Context Readback`, запрещают писать `fully read` для неоткрытых ссылок и требуют отделять выводы из central docs, project-specific context и not verified. ([GitHub][1])

Central `repo_navigation.md` подтверждает, что central navigation — это closed set allowed navigation targets только для `ai-workflow-core`; он не даёт права делать claims о consumer repo без явно переданных project-specific links/excerpts. ([GitHub][2])

Из central docs для этого вопроса следует только workflow-граница: ответ должен быть grounded, planning-only и честно отделять проверенное от непроверенного. Central docs не определяют сами схемы `project.json`, `module.json`, `map.json`, `scenario.json`, `rules.metadata.json`, `savegame.json`.

### Confirmed from provided excerpts

Project-specific документы уже фиксируют, что проект — это не одна игра, а browser-based 2D authoring tool / editor / tabletop sandbox; Sword of Rome-like модуль должен быть test module, а не hardcoded центр платформы. ([GitHub][3])

Принята 4-layer модель: Layer 1 — Core Infrastructure + Project/Data Model, Layer 2 — Universal Authoring, Layer 3 — Universal Runtime / Play Sandbox, Layer 4 — Module Package. Layer 3 должен исполнять универсальный цикл `Action -> Event -> GameState -> Render`, а Layer 4 содержит module content и module rules/hooks. ([GitHub][3])

`domain_schemas_contract.md` уже фиксирует canonical split: definitions, runtime state и rules layer. Там же зафиксирован canonical file set и границы: `map.json` не хранит текущие позиции фишек/control/phase/event log; `scenario.json` хранит initial setup, но не post-start history; `savegame.json` хранит concrete play session state, но не canonical map graph или piece definitions. ([GitHub][5])

`rules_hooks_interface.md` фиксирует принцип: runtime asks, module rules answer, runtime applies and logs. Для `Table Sandbox 0.1` default должен быть manual → assisted, не strict. ([GitHub][6])

`action_event_contract.md` фиксирует backbone: `Action` = запрос/намерение, `Event` = подтверждённый факт; только committed events меняют authoritative `GameState`. ([GitHub][7])

`first_milestone_runtime_skeleton.md` и `table_sandbox_0_1_milestone_plan.md` подтверждают порядок: сначала минимальный canonical data seed, потом bootstrap `GameState`, потом Action/Event backbone, permissive RulesHooks, затем первый thin vertical slice — перемещение одной фишки между двумя spaces через полный pipeline. ([GitHub][8])

Ниже — минимальная первая версия схем именно для `Table Sandbox 0.1`, без TypeScript/Zod implementation.

---

#### 1. `project.json`

**Назначение:** root workspace index. Он говорит платформе, какие module packages доступны в проекте и какой модуль открыть по умолчанию.

**Обязательные поля первого прохода:**

```text
schemaVersion
projectId
name
activeModuleId
modules[]
```

**Минимальная структура `modules[]`:**

```text
moduleId
path
```

**Safe default for now:**

```text
schemaVersion: "0.1"
projectId: stable project id
name: human-readable project name
activeModuleId: id of the sample module
modules: [{ moduleId, path }]
```

**Связи:**

* `activeModuleId` должен ссылаться на один из `modules[].moduleId`.
* `modules[].path` должен указывать на `modules/<moduleId>/module.json`.
* `project.json` связан с `module.json`, но не должен знать внутренности `map.json`, `scenario.json` или `savegame.json`.

**Чего здесь быть не должно:**

* spaces;
* connections;
* piece definitions;
* piece instances;
* scenario setup;
* current `GameState`;
* event log;
* rules logic;
* Phaser/renderer state.

**Later extension:**

* `assetRoots`;
* project metadata;
* recent files;
* editor preferences;
* multiple active workspaces;
* project-level validation summary.

**Still open / not fixed:**

* нужен ли project-level `createdAt/updatedAt`;
* нужна ли project-level локализация;
* должен ли `activeModuleId` быть обязательным всегда или только для 0.1 convenience.

---

#### 2. `modules/<moduleId>/module.json`

**Назначение:** `ModuleManifest`. Это entry point модуля. Runtime не должен угадывать, где лежат map/scenario/rules metadata.

**Обязательные поля первого прохода:**

```text
schemaVersion
moduleId
name
version
engineCompatibility
defaultMapId
defaultScenarioId
files
rules
```

**Минимальная структура `files`:**

```text
map
scenarios[]
rulesMetadata
```

**Минимальная структура `scenarios[]`:**

```text
scenarioId
path
```

**Минимальная структура `rules`:**

```text
metadataFile
hookContractVersion
automationLevel
```

**Safe default for now:**

```text
automationLevel: "manual"
files.map: "map.json"
files.rulesMetadata: "rules.metadata.json"
files.scenarios: [{ scenarioId: "basic", path: "scenario.basic.json" }]
```

**Связи:**

* `moduleId` должен совпадать с `project.json -> modules[].moduleId`.
* `defaultMapId` должен совпадать с `map.json -> mapId`.
* `defaultScenarioId` должен совпадать с одним из `files.scenarios[].scenarioId`.
* `files.rulesMetadata` должен указывать на `rules.metadata.json`.
* `rules.hookContractVersion` должен быть совместим с `rules.metadata.json -> hookContractVersion`.

**Чего здесь быть не должно:**

* полный graph карты;
* список spaces/connections;
* конкретные стартовые piece instances;
* current save state;
* event log;
* executable rules code inline;
* renderer-specific state.

**Later extension:**

* `assets`;
* `localization`;
* `documents`;
* `pieceDefinitionsFile`;
* `factionDefinitionsFile`;
* `cardsFile`;
* `rulesEntry`;
* module dependencies.

**Still open / not fixed:**

* должны ли `PieceDefinition` и `FactionDefinition` в 0.1 жить прямо в `module.json` или в отдельном файле.
* Для `Table Sandbox 0.1` safe default: держать маленький набор definitions прямо в `scenario.json` или `map.json` не стоит; лучше держать минимальные `pieceDefinitions` и `factions` в `module.json`, но это временный компактный вариант. Позже их лучше вынести в `pieces.json` / `factions.json`.

---

#### 3. `modules/<moduleId>/map.json`

**Назначение:** immutable-ish board/map definition: карта, spaces, connections, zones, координаты и базовая визуальная геометрия.

**Обязательные поля первого прохода:**

```text
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

**Минимальная структура `coordinateSystem`:**

```text
type
width
height
```

**Минимальная структура `spaces[]`:**

```text
spaceId
name
x
y
kind
```

**Минимальная структура `connections[]`:**

```text
connectionId
fromSpaceId
toSpaceId
kind
```

**Минимальная структура `zones[]`:**

```text
zoneId
name
kind
```

`zones[]` можно оставить пустым массивом, но поле лучше иметь уже в 0.1, потому что off-map boxes и holding areas для counter-based игр почти неизбежны.

**Safe default for now:**

```text
coordinateSystem.type: "pixel"
spaces[].kind: "point"
connections[].kind: "path"
zones: []
```

**Связи:**

* `moduleId` должен совпадать с `module.json -> moduleId`.
* `mapId` должен совпадать с `module.json -> defaultMapId`, если это default map.
* `connections[].fromSpaceId` и `connections[].toSpaceId` должны ссылаться на существующие `spaces[].spaceId`.
* `scenario.<scenarioId>.json -> mapId` должен ссылаться на этот `mapId`.
* `savegame.json -> mapId` должен ссылаться на этот `mapId`.

**Чего здесь быть не должно:**

* текущие позиции фишек;
* `PieceInstance[]`;
* текущий control spaces;
* текущие markers;
* текущая фаза;
* event log;
* current player;
* save state;
* game-rule legality;
* hidden info.

**Later extension:**

* `mapSheetAssetId`;
* visual layers;
* labels;
* terrain/tags;
* ports;
* regions;
* victory space metadata;
* movement cost metadata;
* custom connection geometry.

**Still open / not fixed:**

* точная модель `zones`;
* нужны ли directed connections;
* нужно ли разрешать duplicate edges;
* нужно ли хранить `SpaceDefinition.homeFactionId` уже в 0.1. Safe default: не хранить, пока это не нужно для первого thin slice.

---

#### 4. `modules/<moduleId>/scenario.<scenarioId>.json`

**Назначение:** initial setup template. Это не save. Это стартовое состояние, из которого runtime собирает initial `GameState`.

**Обязательные поля первого прохода:**

```text
schemaVersion
scenarioId
moduleId
mapId
name
setup
```

**Минимальная структура `setup`:**

```text
turnState
pieces[]
controlBySpace
variables
```

**Минимальная структура `turnState`:**

```text
round
phaseId
activeActorId
```

Для 0.1 это может быть формально и почти не использоваться.

**Минимальная структура `pieces[]`:**

```text
pieceId
pieceDefId
locationId
ownerId
```

**Минимальная структура `controlBySpace`:**

```text
[spaceId]: factionId | null
```

**Минимальная структура `variables`:**

```text
{}
```

**Safe default for now:**

```text
turnState.round: 1
turnState.phaseId: "manual"
turnState.activeActorId: "designer"
variables: {}
```

**Связи:**

* `moduleId` должен совпадать с `module.json -> moduleId`.
* `mapId` должен ссылаться на `map.json -> mapId`.
* `scenarioId` должен быть перечислен в `module.json -> files.scenarios[]`.
* `pieces[].pieceDefId` должен ссылаться на существующий `PieceDefinition`.
* `pieces[].locationId` должен ссылаться на существующий `spaceId` или `zoneId`.
* `controlBySpace` keys должны ссылаться на существующие `spaceId`.
* `ownerId` должен ссылаться на известную faction/player-side definition, если такая уже введена.

**Чего здесь быть не должно:**

* post-start event log;
* history after play begins;
* committed event sequence;
* save snapshots;
* full map graph;
* full rules logic;
* renderer camera state;
* UI panels state.

**Later extension:**

* scenario variants;
* setup options;
* scripted setup;
* initial deck/hand state;
* special scenario rules;
* victory condition overrides;
* player seats;
* scenario notes/documents.

**Still open / not fixed:**

* где в 0.1 лучше хранить `FactionDefinition` и `PieceDefinition`.
* Safe default: для первого data seed можно держать минимальные `factions[]` и `pieceDefinitions[]` в `module.json`, чтобы `scenario` хранил только instances. Если разработке проще, можно временно держать их в `scenario`, но это хуже как canonical direction, потому что смешивает module definitions и scenario setup.

---

#### 5. `modules/<moduleId>/rules.metadata.json`

**Назначение:** declarative metadata для rules boundary. Это не rules implementation и не runtime state.

**Обязательные поля первого прохода:**

```text
schemaVersion
rulesVersion
hookContractVersion
automationLevel
supportedActionTypes[]
supportedEventTypes[]
phases[]
```

**Минимальная структура `supportedActionTypes[]`:**

```text
actionType
mode
```

**Минимальная структура `supportedEventTypes[]`:**

```text
eventType
```

**Минимальная структура `phases[]`:**

```text
phaseId
name
```

**Safe default for now:**

```text
automationLevel: "manual"
phases: [{ phaseId: "manual", name: "Manual Sandbox" }]
supportedActionTypes:
  - move_piece_requested
  - create_piece_requested
  - delete_piece_requested
  - change_control_requested
supportedEventTypes:
  - piece_moved
  - piece_created
  - piece_deleted
  - control_changed
```

**Связи:**

* `hookContractVersion` должен совпадать или быть совместимым с `module.json -> rules.hookContractVersion`.
* `automationLevel` должен совпадать с `module.json -> rules.automationLevel` или иметь понятный override rule.
* `supportedActionTypes[]` должен покрывать action types, которые первый runtime slice реально создаёт.
* `supportedEventTypes[]` должен покрывать event types, которые `resolveAction` может предложить.
* `phases[].phaseId` должен покрывать `scenario.setup.turnState.phaseId`.

**Чего здесь быть не должно:**

* executable rules code;
* actual hook functions;
* current `GameState`;
* save data;
* hidden mutable state;
* event log;
* UI-specific behavior;
* Phaser/DOM references.

**Later extension:**

* visibility capabilities;
* response windows capabilities;
* strict/assisted rule variants;
* phase order;
* action schemas;
* event schemas;
* rule options;
* player view policy.

**Still open / not fixed:**

* нужен ли отдельный `rulesEntry` уже в 0.1.
* Safe default: `rules.metadata.json` описывает capabilities, а actual hooks на 0.1 могут быть default permissive implementation внутри runtime/module seam, без полноценного external script entry.

---

#### 6. `saves/<saveId>.savegame.json`

**Назначение:** concrete play session snapshot. Это текущее состояние партии/плейтеста, но не место для canonical definitions.

**Обязательные поля первого прохода:**

```text
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

**Минимальная структура `gameState`:**

```text
stateId
mode
turnState
piecesById
controlBySpace
variables
```

**Минимальная структура `turnState`:**

```text
round
phaseId
activeActorId
```

**Минимальная структура `piecesById`:**

```text
[pieceId]:
  pieceId
  pieceDefId
  locationId
  ownerId
  status
```

**Минимальная структура `eventLog[]`:**

```text
eventId
seq
type
payload
causedByActionId
actorId
```

**Safe default for now:**

```text
mode: "manual"
variables: {}
eventLog: []
status: "normal"
```

Для первого generated save можно создать `gameState` из `scenario.setup` и пустой `eventLog`. После первого move-piece vertical slice `eventLog` уже должен содержать `piece_moved`.

**Связи:**

* `moduleId` и `moduleVersion` должны ссылаться на `module.json`.
* `mapId` и `mapVersion` должны ссылаться на `map.json`.
* `scenarioId` и `scenarioVersion` должны ссылаться на `scenario.<scenarioId>.json`.
* `gameState.turnState.phaseId` должен быть известен в `rules.metadata.json -> phases[]`.
* `piecesById[*].pieceDefId` должен ссылаться на existing `PieceDefinition`.
* `piecesById[*].locationId` должен ссылаться на existing `spaceId` или `zoneId`.
* `eventLog[].seq` должен быть монотонным.
* `eventLog[].causedByActionId` должен ссылаться на action request, если action history хранится; если action history не хранится в 0.1, допустимо сохранять только id как trace reference.

**Чего здесь быть не должно:**

* full `MapDefinition`;
* full `SpaceDefinition[]`;
* full `ConnectionDefinition[]`;
* full `PieceDefinition[]`;
* module manifest copy;
* executable rules logic;
* raw Phaser sprite state;
* editor panel state as canonical truth.

**Later extension:**

* content hashes;
* RNG state;
* undo stack;
* action history;
* player seats;
* visibility state;
* pending response windows;
* autosave metadata;
* migration metadata.

**Still open / not fixed:**

* exact save compatibility policy.
* Safe default for 0.1: store versions and warn/block on mismatch; do not attempt migration yet.
* whether to store full action history in addition to event log. Safe default: event log is required; action history can wait unless debugging needs it immediately.

---

#### Минимальные связи между всеми файлами

```text
project.json
  -> modules[].moduleId
  -> modules[].path
      -> module.json

module.json
  -> defaultMapId
  -> files.map
      -> map.json

module.json
  -> defaultScenarioId
  -> files.scenarios[].scenarioId/path
      -> scenario.<scenarioId>.json

module.json
  -> rules.metadataFile
      -> rules.metadata.json

scenario.<scenarioId>.json
  -> moduleId
  -> mapId
  -> setup.pieces[].pieceDefId
  -> setup.pieces[].locationId

savegame.json
  -> moduleId/moduleVersion
  -> mapId/mapVersion
  -> scenarioId/scenarioVersion
  -> gameState
  -> eventLog[]
```

Главная practical dependency:

```text
project.json
→ module.json
→ map.json + scenario.json + rules.metadata.json
→ initial GameState
→ Action/Event pipeline
→ savegame.json
```

---

#### Минимальные invariants и проверки целостности

**ID / reference integrity:**

* `projectId`, `moduleId`, `mapId`, `scenarioId`, `saveId` обязательны.
* Все ids должны быть стабильными строками.
* `activeModuleId` должен существовать в `project.modules[]`.
* `module.defaultMapId` должен совпадать с `map.mapId`.
* `module.defaultScenarioId` должен существовать в `module.files.scenarios[]`.
* `scenario.mapId` должен совпадать с existing `mapId`.
* `connection.fromSpaceId` и `connection.toSpaceId` должны ссылаться на existing spaces.
* `piece.locationId` должен ссылаться на existing space или zone.
* `piece.pieceDefId` должен ссылаться на existing piece definition.
* `savegame` не должен загружаться silently, если module/map/scenario versions несовместимы.

**Definitions vs runtime state:**

* `map.json` = topology/geometry only.
* `scenario.json` = initial setup only.
* `savegame.json` = mutable current state only.
* `rules.metadata.json` = declarative rules capabilities only.
* Runtime state changes only through committed events.

**Action/Event invariants:**

* `Action` не меняет `GameState`.
* `proposed Event[]` не меняют `GameState`.
* Только committed `Event[]` меняют `GameState`.
* `eventLog[].seq` монотонный.
* `eventLog[]` append-only для 0.1.
* `piece_moved` должен менять `piecesById[pieceId].locationId`, а не sprite coordinates.

**Renderer boundary:**

* Phaser/React state не является canonical.
* Sprite position может быть derived view от `GameState`, но не source of truth.

---

#### Минимальный набор action/event типов для первого thin vertical slice

Для самого первого slice достаточно:

```text
Action:
move_piece_requested

Event:
piece_moved
```

Для завершения `Table Sandbox 0.1` добавить:

```text
Actions:
create_piece_requested
delete_piece_requested
change_control_requested
create_space_requested
update_space_requested
create_connection_requested
save_snapshot_requested
load_save_requested

Events:
piece_created
piece_deleted
control_changed
space_created
space_updated
connection_created
save_snapshot_created
save_loaded
```

Важно: даже manual sandbox действия должны проходить через visible pipeline, а не напрямую менять состояние.

---

#### Safe default for now

Для `Table Sandbox 0.1` safest minimal contract:

```text
project.json:
  только workspace index

module.json:
  manifest + minimal factions/pieceDefinitions if needed for 0.1

map.json:
  spaces + connections + zones, no runtime state

scenario.json:
  initial piece instances + initial control + initial turnState

rules.metadata.json:
  manual automation, supported action/event types, one manual phase

savegame.json:
  GameState + eventLog + version references, no definitions
```

`PieceDefinition` и `FactionDefinition` — единственное спорное место для первого прохода. Safe default: временно держать маленькие `factions[]` и `pieceDefinitions[]` в `module.json`, потому что отдельные `pieces.json` / `factions.json` могут быть лишней сложностью для первого slice. Но это нужно явно пометить как temporary compact layout.

---

#### Later extension

После `Table Sandbox 0.1` можно выносить:

```text
modules/<moduleId>/pieces.json
modules/<moduleId>/factions.json
modules/<moduleId>/cards.json
modules/<moduleId>/documents.json
modules/<moduleId>/assets.json
modules/<moduleId>/locales/*.json
```

Также позже можно добавить:

* content hashes;
* migration policy;
* visibility model;
* response windows;
* strict phase order;
* server-authoritative player views;
* advanced stack ordering;
* undo/replay policy.

---

#### Still open / not fixed

* точное место для `FactionDefinition` и `PieceDefinition` в первом compact file set;
* точная save compatibility policy;
* точная stack model;
* нужно ли хранить action history отдельно от event log;
* точный формат content hashes;
* точный формат `rulesEntry`;
* exact JSON Schema / Zod / TypeScript signatures;
* нужно ли authoring definition changes проводить через отдельный transaction log или через тот же Action/Event mechanism.

### Not available / not verified

* Локальный репозиторий, ветка, git status, product-code skeleton, tests, build и runtime не проверялись.
* Не проверено, существуют ли уже реальные JSON-файлы в локальном repo.
* Не проверена фактическая структура будущих папок product code.
* Не проверены реальные Zod/TypeScript schemas.
* Ответ является planning-only contract proposal для первого прохода `Table Sandbox 0.1`, а не implementation spec.

## Candidate Navigation Entry

V1-20260523-130238: Planning-only ответ по минимальным canonical file schemas для `Table Sandbox 0.1`. Рекомендация: начать с компактного набора `project.json`, `module.json`, `map.json`, `scenario.<scenarioId>.json`, `rules.metadata.json`, `savegame.json`, строго разделив workspace/module manifest, map definitions, scenario initial setup, rules metadata и mutable save/runtime state; первый slice должен сохранить путь к Action/Event pipeline и не превращать `savegame.json` или `map.json` в скрытые хранилища definitions/runtime state.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-055021_domain-data-contract-proposal-for-the-2d-counter.md "raw.githubusercontent.com"
