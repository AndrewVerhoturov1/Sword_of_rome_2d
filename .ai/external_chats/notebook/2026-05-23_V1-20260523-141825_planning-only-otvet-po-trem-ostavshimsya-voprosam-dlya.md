# Notebook Entry

- External Question ID: `V1-20260523-141825`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-141825_planning-only-otvet-po-trem-ostavshimsya-voprosam-dlya.md`

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
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-131910_planning-only-otvet-po-stack-model-dlya-table.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md`

## Candidate Navigation Entry

Topic: Planning-only ответ по трём оставшимся вопросам для `Table Sandbox 0.1`
Summary: Рекомендация: для save compatibility использовать ограниченную политику с блокировкой структурно несовместимых save-файлов и warning-only для безопасных metadata/minor cases; authoring changes и runtime changes разделить явными режимами; `PieceDefinition[]` и `FactionDefinition[]` можно временно держать в `module.json` как compact 0.1 layout, но позже вынести в `pieces.json` и `factions.json`.

## Raw Response

## External Question ID

V1-20260523-141825

## Context Readback

* Uploaded prompt / `Вставленный текст(9).txt` — fully read. 
* `external_chat_rules.md` — fully read. ([GitHub][1])
* `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — fully read. ([GitHub][4])
* `domain_schemas_contract.md` — fully read. ([GitHub][5])
* `rules_hooks_interface.md` — fully read. ([GitHub][6])
* `action_event_contract.md` — fully read. ([GitHub][7])
* `first_milestone_runtime_skeleton.md` — fully read. ([GitHub][8])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][9])
* `first_vertical_slice_spec.md` — fully read. ([GitHub][10])
* `minimal_canonical_file_schemas.md` — fully read. ([GitHub][11])
* Project `V1_navigation.md` — fully read. ([GitHub][12])
* V1-navigation-discovered `V1-20260523-131910` notebook entry — fully read. ([GitHub][13])
* V1-navigation-discovered `V1-20260523-130238` notebook entry — partially read. ([GitHub][14])
* V1-navigation-discovered `V1-20260523-124734` notebook entry — partially read. ([GitHub][15])
* V1-navigation-discovered `V1-20260523-062449` notebook entry — partially read. ([GitHub][16])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` contract requires honest `Context Readback`, clear separation between central-doc conclusions, project-specific conclusions, and not-verified material. It also says external chat is not authority over the local repo and can only make repo claims from explicitly provided project-specific context. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation only covers `ai-workflow-core` files and does not authorize claims about the consumer repo unless consumer-project files are explicitly provided. ([GitHub][2])

For this question, central docs confirm the workflow boundary only. They do not define save compatibility, authoring/runtime boundary, or where `PieceDefinition[]` / `FactionDefinition[]` should live.

### Confirmed from provided excerpts

Project-specific docs confirm the base: this is a universal browser-based 2D authoring/runtime sandbox, not a hardcoded Sword of Rome implementation. The accepted product architecture has four layers, with Layer 1 owning schemas/versioning/persistence, Layer 2 authoring, Layer 3 runtime/play sandbox, and Layer 4 module content plus module rules/hooks. ([GitHub][3])

The domain contract fixes the key split: `definitions`, `runtime state`, and `module rules`. It also states that `map.json` must not store current piece positions/control/phase/event log, `scenario.json` is initial setup, and `savegame.json` is mutable runtime/session state rather than a place for canonical definitions. It also explicitly allows, as a first-pass simplification, small `pieces/factions` definitions inside `module.json`, but not as the long-term canonical target. ([GitHub][5])

The runtime/rules contract fixes the principle: runtime asks, module rules answer, runtime applies and logs. Rules hooks must not own save files or silently mutate authoritative state. ([GitHub][6])

The action/event contract fixes the backbone: `Action` is a request, `Event` is a committed fact, and only runtime may append committed events, mutate authoritative `GameState`, persist save state, and trigger render from committed state. ([GitHub][7])

The milestone docs fix the early goal: `Table Sandbox 0.1` should first prove canonical files, `GameState` bootstrap, Action/Event dispatcher, permissive rules hooks, and the first vertical slice: moving one piece through `move_piece_requested -> piece_moved -> GameState -> log -> render`. Advanced stack model, migration engine, strict legality, hidden information, online/server sync, and polished UX are out of scope for 0.1. ([GitHub][8])

---

#### Вопрос 1. Save compatibility policy

**Recommended safe default now:**
Для `Table Sandbox 0.1` лучше выбрать **ограниченную совместимость с жёстким блоком для структурно несовместимых save-файлов**.

То есть не просто "всегда предупреждать" и не полноценный migration engine. Правильная политика:

```text
compatible save        -> load normally
minor uncertain save   -> warn and allow only if references still valid
incompatible save      -> block load
migration needed       -> block; no automatic migration in 0.1
```

**Что считать несовместимым и блокировать:**

* `savegame.schemaVersion` несовместим с текущим reader;
* `moduleId` из save не найден;
* `mapId` из save не найден;
* `scenarioId` из save не найден;
* `moduleVersion`, `mapVersion`, `scenarioVersion` явно не совпадают и нет правила совместимости;
* piece в save ссылается на missing `pieceDefId`;
* piece в save ссылается на missing `locationId`;
* event log содержит неизвестный event type, который нельзя безопасно проигнорировать;
* `rules.metadata` / `hookContractVersion` несовместим с save/runtime.

**Что можно разрешить с предупреждением:**

* изменилось human-readable имя модуля;
* изменился display label;
* изменились неканонические editor metadata;
* save старый, но все referenced ids, versions and required fields валидны;
* отсутствуют optional поля, для которых есть безопасные defaults.

**Почему это лучше:**

* `savegame.json` не должен превращаться в копию всех definitions; значит save зависит от внешних `module.json`, `map.json`, `scenario.json`, `PieceDefinition[]`, `FactionDefinition[]`.
* Если definitions изменились, save может стать опасным: фишка может ссылаться на несуществующий space или piece definition.
* Warn-only опасен: можно загрузить битое состояние и потом не понять, где ошибка.
* Full migration engine слишком рано: он уже вынесен за пределы 0.1 как non-goal.
* Strict block для всего подряд тоже неудобен: мелкие metadata-изменения не должны ломать плейтест.

**Минимальные поля для save compatibility в `savegame.json`:**

```text
schemaVersion
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

Желательно later, но не обязательно для самого первого slice:

```text
moduleContentHash
mapContentHash
scenarioContentHash
rulesMetadataHash
```

**What to defer later:**

* migration engine;
* automatic save upgrade;
* partial content migration;
* replay-based migration;
* old save repair UI;
* compatibility matrix between module versions;
* semantic version policy beyond simple block/warn rules.

**What should remain explicitly open:**

* exact version matching rule: strict equality vs semver-compatible minor versions;
* when to introduce content hashes;
* whether load should support read-only inspect mode for incompatible saves;
* whether old event logs should be replayed or save snapshots loaded directly;
* whether action history is stored in addition to event log.

---

#### Вопрос 2. Граница между authoring changes и runtime changes

**Recommended safe default now:**
Для `Table Sandbox 0.1` нужно явно разделить два режима:

```text
Authoring Mode  -> меняет definitions / setup files
Play Sandbox Mode -> меняет runtime GameState through Action/Event
```

Даже если визуально действие похоже, смысл разный.

Пример:

```text
передвинуть точку карты      -> authoring change в map.json
передвинуть фишку во время партии -> runtime change через Action/Event
поменять стартовую расстановку    -> scenario authoring
поменять текущее положение фишки   -> save/runtime event
```

**Граница ответственности:**

| Тип изменения                            | Где живёт                     | Через что проходит                      | Что не должно происходить                         |
| ---------------------------------------- | ----------------------------- | --------------------------------------- | ------------------------------------------------- |
| Изменение карты: space, connection, zone | `map.json`                    | authoring transaction / definition edit | не писать это в `savegame.json` как runtime state |
| Изменение стартовой расстановки          | `scenario.json`               | scenario authoring                      | не смешивать с текущим save                       |
| Перемещение фишки во время sandbox/play  | `GameState` / `savegame.json` | `Action -> Event -> GameState -> log`   | не менять sprite напрямую как truth               |
| Изменение текущего control               | `GameState` / `savegame.json` | committed event                         | не писать current control в `map.json`            |
| Правила/доступные действия               | `rules.metadata.json` + hooks | rules boundary                          | не хранить state внутри rules metadata            |

**Safe default now:**

1. Ввести явный `mode`:

   * `authoring`;
   * `playSandbox`.

2. В `authoring`:

   * изменения definitions идут в `project.json`, `module.json`, `map.json`, `scenario.json`;
   * можно иметь отдельный authoring transaction или simple deterministic file update;
   * не обязательно проводить всё через play event log в 0.1.

3. В `playSandbox`:

   * изменения текущей партии идут только через `Action/Event`;
   * результат попадает в `GameState`, `eventLog[]`, потом в `savegame.json`;
   * renderer redraws from committed state.

4. Не делать "тихий режим", где drag/drop иногда меняет definition, а иногда runtime state без явного mode.

**Почему это лучше:**

* Сохраняется canonical split `definitions / runtime state / module rules`.
* `map.json` не становится носителем текущего состояния.
* `savegame.json` не начинает переписывать карту и definitions.
* Первый thin vertical slice остаётся чистым: пользователь двигает фишку, runtime создаёт action, rules разрешают, runtime commits event, reducer меняет `GameState`, log обновляется, renderer перерисовывает. ([GitHub][10])

**Главные смешения, которых надо избежать:**

* редактирование `map.json` во время play без явного authoring mode;
* запись текущих piece positions в `map.json`;
* запись post-start event history в `scenario.json`;
* сохранение full `MapDefinition` и `PieceDefinition[]` в `savegame.json`;
* прямое изменение Phaser objects как authoritative state;
* rules hook, который сам пишет save или меняет `GameState`.

**What to defer later:**

* полноценный definition transaction log;
* undo/redo для authoring отдельно от play undo;
* scenario fork from current save;
* "apply current save as new scenario setup";
* migration after definition changes;
* collaborative editing.

**What should remain explicitly open:**

* должны ли authoring changes позже тоже иметь event-like audit log;
* нужен ли единый command model для authoring и runtime или два разных pipeline;
* как именно UI будет предупреждать пользователя, что он сейчас меняет definition, а не текущую партию;
* как сохранять текущий playtest, если user меняет definitions в середине sandbox session.

---

#### Вопрос 3. Временное место для `PieceDefinition[]` и `FactionDefinition[]`

**Recommended safe default now:**
Для `Table Sandbox 0.1` временно держать маленькие `PieceDefinition[]` и `FactionDefinition[]` прямо в `module.json` — **нормальный safe default**, если явно пометить это как compact first-milestone layout, а не долгосрочный canonical target.

Рекомендуемая граница:

```text
0.1:
module.json содержит маленькие factions[] и pieceDefinitions[]

later:
вынести в pieces.json и factions.json
module.json оставляет только file pointers
```

Это согласуется с `domain_schemas_contract.md`, где прямо сказано: если отдельные `pieces.json` / `factions.json` слишком тяжелы для первого thin slice, маленький временный compact layout внутри `module.json` допустим, но это short-term simplification. ([GitHub][5])

**Почему это хороший safe default now:**

* меньше файлов для первого data seed;
* проще проверить первый vertical slice;
* проще связать `scenario.setup.pieces[].pieceDefId` с definitions;
* не надо раньше времени проектировать full content package system;
* `module.json` всё ещё остаётся manifest, если definitions маленькие и явно scoped.

**Минимально допустимый compact layout:**

```text
module.json:
  moduleId
  name
  version
  files
  rules
  factions[]
  pieceDefinitions[]
```

Но важно: `module.json` не должен хранить:

* `PieceInstance[]`;
* текущие позиции фишек;
* current control;
* event log;
* save state;
* full map graph;
* executable rules.

`PieceInstance[]` должны быть в `scenario.json` как initial setup, а потом в `savegame.json` как runtime state. `PieceDefinition[]` описывают типы фишек, а не конкретные фишки на столе. ([GitHub][5])

**Плюсы compact layout:**

* быстро стартовать;
* меньше boilerplate;
* меньше риск, что первый milestone утонет в package management;
* проще читать глазами;
* достаточно для 3-5 тестовых фишек и 2-3 фракций;
* хорошо подходит для fake/test module.

**Риски compact layout:**

* `module.json` может распухнуть и перестать быть manifest;
* появится соблазн засунуть туда scenario state или save state;
* later extraction в `pieces.json` / `factions.json` всё равно понадобится;
* если слишком рано добавить много Sword of Rome-like content, module manifest станет content dump;
* можно размазать границу между module metadata и module content.

**Критерий, когда пора выносить в `pieces.json` и `factions.json`:**

Выносить, когда выполнено хотя бы одно условие:

* больше примерно 10-20 `PieceDefinition`;
* больше 4-6 factions;
* появляются разные категории фишек с разными полями;
* нужны assets/icons per piece;
* нужно редактировать piece catalog отдельным editor surface;
* definitions начинают мешать чтению `module.json`;
* появляются cards/decks/documents/localization;
* module package начинает напоминать реальный content package, а не tiny test module;
* нужно поддержать несколько scenario files, которые переиспользуют один большой piece catalog.

**Правильный later path:**

```text
module.json:
  files:
    pieces: "pieces.json"
    factions: "factions.json"

pieces.json:
  schemaVersion
  moduleId
  pieceDefinitions[]

factions.json:
  schemaVersion
  moduleId
  factions[]
```

После выноса `scenario.json` всё равно должен ссылаться на `pieceDefId` и `factionId`, а не копировать definitions внутрь scenario. `savegame.json` тоже должен ссылаться на `pieceDefId`, а не хранить полное определение фишки.

**What to defer later:**

* separate `pieces.json`;
* separate `factions.json`;
* asset catalog;
* localization;
* piece editor catalog UI;
* inheritance/templates for piece definitions;
* module dependency/content package loader.

**What should remain explicitly open:**

* точный порог выноса definitions из `module.json`;
* exact shape of `PieceDefinition`;
* exact shape of `FactionDefinition`;
* будут ли piece definitions поддерживать sides/front-back;
* где хранить art/icon references;
* нужны ли definition ids с namespace prefix.

---

#### Связь между тремя вопросами

Эти три решения связаны одним принципом: **не делать ранние файлы слишком умными**.

* Save compatibility должна быть простой: versions/references valid — load; structural mismatch — block; migration later.
* Authoring/runtime boundary должна быть явной: definitions меняются отдельно, runtime state меняется через Action/Event.
* `module.json` может временно держать маленькие definitions, но не должен превращаться в dump всей игры.
* `savegame.json` не должен хранить canonical definitions.
* `map.json` не должен хранить runtime state.
* Первый thin vertical slice должен остаться чистым: `move_piece_requested -> piece_moved -> GameState -> eventLog -> render`.

### Not available / not verified

* Локальный репозиторий, ветка, git status, tests, build, runtime и реальные JSON-файлы не проверялись.
* Не проверено, есть ли уже product-code skeleton или частичная реализация этих решений.
* Exact TypeScript/Zod schemas не фиксировались.
* Exact semantic versioning policy не зафиксирована.
* Exact content hash policy не зафиксирована.
* Exact authoring transaction model не зафиксирован.
* Exact threshold for extracting `pieces.json` / `factions.json` не принят как local decision.
* Этот ответ — planning-only recommendation, не accepted local decision.

## Candidate Navigation Entry

V1-20260523-141825: Planning-only ответ по трём оставшимся вопросам для `Table Sandbox 0.1`. Рекомендация: для save compatibility использовать ограниченную политику с блокировкой структурно несовместимых save-файлов и warning-only для безопасных metadata/minor cases; authoring changes и runtime changes разделить явными режимами; `PieceDefinition[]` и `FactionDefinition[]` можно временно держать в `module.json` как compact 0.1 layout, но позже вынести в `pieces.json` и `factions.json`.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-131910_planning-only-otvet-po-stack-model-dlya-table.md
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md
