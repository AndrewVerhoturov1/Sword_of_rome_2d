# Notebook Entry

- External Question ID: `V1-20260523-144154`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-144154_planning-only-otvet-po-validation-undo-redo-i.md`

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
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-131910_planning-only-otvet-po-stack-model-dlya-table.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md`

## Candidate Navigation Entry

Topic: Planning-only ответ по validation, undo/redo и `save as scenario` для `Table Sandbox 0.1`
Summary: Рекомендация: перед Play Sandbox Preview блокировать структурно невалидные module/save references, warning-only оставить для безопасных metadata cases; authoring undo/redo и runtime undo/redo разделить концептуально, runtime undo лучше отложить; `save as scenario` не делать частью первого slice, later реализовать как явное создание нового scenario из extracted setup без event log.

## Raw Response

## External Question ID

V1-20260523-144154

## Context Readback

* Uploaded prompt / `Вставленный текст(12).txt` — fully read. 
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
* `module_authoring_workflow.md` — fully read. ([GitHub][12])
* Project `V1_navigation.md` — fully read. ([GitHub][13])
* V1-navigation-discovered `V1-20260523-130238` notebook entry — partially read. ([GitHub][14])
* V1-navigation-discovered `V1-20260523-124734` notebook entry — partially read. ([GitHub][15])
* V1-navigation-discovered `V1-20260523-131910` notebook entry — partially read. ([GitHub][16])
* V1-navigation-discovered `V1-20260523-062449` notebook entry — partially read. ([GitHub][17])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require honest `Context Readback`, clear separation between central-doc conclusions, project-specific conclusions, and not-verified material. The same contract forbids claiming local repo/runtime/test access unless that was explicitly provided. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation covers only `ai-workflow-core`; it does not authorize claims about the consumer repo unless consumer-project files are explicitly provided. ([GitHub][2])

For this question, central docs define the answer discipline only. They do not define module validation, undo/redo, or "save as scenario".

### Confirmed from provided excerpts

The accepted project base is: universal authoring/runtime platform first, not a hardcoded Sword of Rome game; four layers are already accepted; Layer 2 owns authoring surfaces, Layer 3 owns universal runtime/play sandbox, and Layer 4 owns module content plus module rules/hooks. ([GitHub][3])

The canonical split is already fixed: definitions, runtime state, and module rules must not be mixed. `map.json` is map/topology, `scenario.json` is initial setup, `rules.metadata.json` is declarative rules metadata, and `savegame.json` is mutable runtime state with `GameState` and `eventLog[]`. ([GitHub][5])

Runtime changes must follow the `Action -> validation -> resolution -> Event -> GameState -> log -> render` pipeline. Only committed events mutate authoritative `GameState`; renderer state is not the source of truth. ([GitHub][7])

`Table Sandbox 0.1` should stay narrow: canonical files, runtime bootstrap, permissive rules, first vertical slice, then save/load and validation hardening. Migration engine, strict legality, hidden info, online sync, and advanced workflows are out of scope. ([GitHub][8])

---

#### Вопрос 1. Module package validation

**Recommended safe default now:**
Перед запуском `Play Sandbox Preview` нужна простая, но обязательная проверка пакета модуля. Она должна отвечать на вопрос: "Можно ли из этих файлов безопасно собрать начальный `GameState` и запустить песочницу?" Не надо делать полноценный rules validator или migration engine.

**Обязательные проверки, которые должны блокировать запуск:**

1. **Наличие файлов**

   * есть `project.json`;
   * есть `module.json`;
   * есть `map.json`;
   * есть выбранный `scenario.<scenarioId>.json`;
   * есть `rules.metadata.json`.

2. **Согласованность manifest**

   * `project.activeModuleId` существует в `project.modules[]`;
   * `project.modules[].path` ведёт к существующему `module.json`;
   * `module.defaultMapId` совпадает с `map.mapId`;
   * `module.defaultScenarioId` есть в `module.files.scenarios[]`;
   * `module.files.rulesMetadata` указывает на существующий `rules.metadata.json`.

3. **Согласованность карты**

   * все `spaceId` уникальны;
   * все `connectionId` уникальны;
   * все `zoneId` уникальны;
   * каждая связь ссылается на существующие `spaceId`;
   * связь не должна ссылаться сама на себя;
   * `map.json` не содержит runtime-состояние: текущие фишки, event log, текущую фазу, save state.

4. **Согласованность сценария**

   * `scenario.moduleId` совпадает с `module.moduleId`;
   * `scenario.mapId` совпадает с `map.mapId`;
   * все `pieceId` в стартовой расстановке уникальны;
   * каждый `pieceDefId` существует в `PieceDefinition`;
   * каждый `ownerId` существует в `FactionDefinition`, если factions уже заведены;
   * каждый `locationId` ссылается на существующий `spaceId` или `zoneId`;
   * `scenario.turnState.phaseId` известен в `rules.metadata.phases[]`;
   * `scenario.json` не содержит post-start event log.

5. **Согласованность rules metadata**

   * `hookContractVersion` совместим с `module.rules.hookContractVersion`;
   * `automationLevel` задан и для `0.1` обычно равен `manual`;
   * `supportedActionTypes[]` содержит минимум `move_piece_requested`;
   * `supportedEventTypes[]` содержит минимум `piece_moved`;
   * `phases[]` содержит хотя бы `manual` phase или фазу, указанную в scenario.

6. **Минимальная save compatibility для preview-from-save**

   * если запускается не сценарий, а save, то `savegame.moduleId/mapId/scenarioId` должны совпадать с доступными module/map/scenario;
   * piece references в save должны быть валидны;
   * `eventLog[].seq` должен быть монотонным;
   * структурно несовместимый save должен блокироваться, а не молча загружаться.

**Warning-only проверки:**

* отсутствует красивое имя у объекта, но есть id;
* есть неиспользуемые `PieceDefinition`;
* есть неиспользуемые `FactionDefinition`;
* есть isolated space без связей;
* есть пустая `zones[]`;
* есть metadata mismatch, который не влияет на references;
* scenario содержит zero pieces, если это осознанный тест;
* есть неизвестные optional поля, которые можно безопасно игнорировать.

**What to defer later:**

* migration engine;
* semantic version compatibility matrix;
* content hashes as hard policy;
* full rules legality validation;
* strict phase validation;
* validation hidden information / response windows;
* auto-repair tools;
* visual validation UI with jump-to-error polish.

**What should remain explicitly open:**

* точная политика `warn` vs `block` для minor version mismatch;
* когда добавлять content hashes;
* будет ли отдельный "inspect incompatible save" режим;
* будет ли validator работать как отдельная команда или только внутри authoring workspace;
* нужно ли валидировать action history, если позже он появится отдельно от event log.

---

#### Вопрос 2. Undo/redo

**Recommended safe default now:**
Для `0.1` undo/redo лучше **разделить по режимам концептуально сразу**, но реализовать минимально:

```text
Authoring undo/redo — отдельно
Play/runtime undo/redo — либо очень ограниченно, либо отложить
```

Причина: authoring и play меняют разные вещи. Authoring меняет definitions и setup-файлы; play sandbox меняет текущий `GameState` через committed events. Эти пути уже должны быть разделены. ([GitHub][12])

**Safe default для authoring undo/redo:**

* в `Map Editor`, `Scenario Editor`, `Pieces/Factions Editor` можно иметь обычный локальный undo/redo для действий редактирования;
* он работает в пределах authoring state;
* он не должен писать в runtime `eventLog[]`;
* он не должен выглядеть как ход игры.

Примеры authoring undo:

* отменить создание точки;
* отменить перемещение точки карты;
* отменить создание связи;
* отменить добавление стартовой фишки в scenario.

**Safe default для play/runtime undo/redo:**

Для первого тонкого среза допустим один из двух вариантов:

1. **Самый безопасный:** runtime undo/redo не делать в первом slice; вместо этого иметь `Начать заново` / reload from scenario.
2. **Минимальный допустимый:** allow "undo last runtime event" только как developer/test tool, если он явно работает через event log или snapshot restore, а не через ручное изменение `GameState`.

Я бы выбрал первый вариант для самого начала: **не делать полноценный play undo/redo до стабилизации event log, save/load и reducer**.

**Почему нельзя смешивать authoring undo и play undo:**

* undo создания space в `map.json` и undo перемещения фишки в `GameState` — разные операции;
* play undo не должен удалять `PieceDefinition`;
* authoring undo не должен стирать runtime event log;
* если сделать один общий undo stack для всего, быстро появится скрытая путаница между definitions и runtime state.

**What to defer later:**

* unified command model;
* authoring transaction log;
* runtime undo by event replay;
* runtime undo by inverse events;
* redo after branching;
* undo across save/load boundary;
* collaborative undo;
* UI polish for history timeline.

**What should remain explicitly open:**

* будет ли authoring иметь свой transaction log;
* будет ли play undo строиться через replay event log или snapshots;
* надо ли сохранять undo stack в `savegame.json`;
* можно ли откатывать события, если позже появятся hidden info, RNG, response windows;
* нужно ли отделять "developer undo" от "player-facing undo".

**Практическая рекомендация:**
Для `0.1` достаточно:

```text
Authoring: простой локальный undo/redo для редактирования.
Play Sandbox: restart from scenario + save/load; полноценный undo позже.
```

---

#### Вопрос 3. `save as scenario` / `apply current playtest state as new scenario setup`

**Recommended safe default now:**
Для `Table Sandbox 0.1` этот workflow лучше **не делать обязательной частью первого тонкого среза**. Его можно оставить как later tool после стабилизации save/load и validation.

Причина: "сохранить текущую проверочную партию как новый сценарий" звучит удобно, но это опасный мост между runtime state и scenario authoring. Если сделать его слишком рано, можно случайно начать смешивать `savegame.json` и `scenario.json`.

**Что можно сделать в `0.1` безопасно:**

* не автоматический "apply current state to current scenario";
* максимум — отдельная ручная команда later-in-0.1:
  **"Создать новый сценарий из текущего состояния…"**
* команда должна всегда создавать **новый scenario file**, а не молча перезаписывать исходный scenario.

**Правильная граница:**

`runtime save` хранит:

* текущий `GameState`;
* текущие позиции фишек;
* текущий control;
* текущую фазу;
* event log;
* mutable runtime variables.

`scenario setup` хранит:

* стартовые `PieceInstance[]`;
* стартовый `controlBySpace`;
* стартовый `turnState`;
* стартовые variables;
* без event log;
* без post-start history.

**Если later делать "save as scenario", то правильный поток такой:**

```text
current savegame / GameState
→ extract setup only
→ remove eventLog
→ choose new scenarioId
→ choose scenario name
→ validate references against module/map/pieces/factions
→ write new scenario.<newScenarioId>.json
→ add it to module.files.scenarios[]
→ do not overwrite original scenario unless user explicitly chooses
```

**Что нельзя делать:**

* нельзя копировать event log в scenario;
* нельзя копировать full savegame as scenario;
* нельзя копировать map definitions из save;
* нельзя сохранять новый scenario без нового `scenarioId`;
* нельзя silently replace canonical scenario after playtest;
* нельзя делать "текущее положение фишек стало стартовой расстановкой" без явного действия пользователя.

**Why:**

* `scenario.json` — это initial setup, а не история партии;
* `savegame.json` — это mutable runtime snapshot, а не canonical module definition;
* accepted workflow says authoring creates module package, play sandbox creates runtime state/save snapshot, and the same gesture must not silently switch meaning between modes. ([GitHub][12])

**What to defer later:**

* polished "Save as new scenario" wizard;
* scenario diff preview;
* "apply to existing scenario" with confirmation;
* fork scenario from save;
* migrate saves after map edits;
* scenario variants;
* audit trail for scenario generation.

**What should remain explicitly open:**

* нужно ли разрешать overwrite existing scenario;
* какие runtime variables можно переносить в scenario setup;
* переносить ли current phase/turn as start phase/turn;
* как обрабатывать pieces created during playtest;
* как обрабатывать deleted pieces;
* как обрабатывать hidden info/RNG later;
* нужно ли сохранять ссылку на source save.

---

#### Связь между тремя вопросами

Все три решения держатся на одном принципе: **не смешивать definitions, scenario setup и runtime state**.

* Validation не должна просто "проверять JSON"; она должна защищать границы файлов.
* Undo/redo должен быть разделён хотя бы концептуально, потому что authoring undo и runtime undo откатывают разные миры.
* `save as scenario` должен быть явным экспортом setup из runtime state, а не молчаливым превращением save в scenario.

Для `Table Sandbox 0.1` правильная линия такая:

```text
сначала validation + clean first slice + save/load
потом простой authoring undo
потом осторожный save-as-new-scenario
и только позже migration/advanced undo/scenario fork tools
```

### Not available / not verified

* Локальный репозиторий, ветка, git status, product-code skeleton, tests, runtime и реальные JSON-файлы не проверялись.
* Не проверено, есть ли уже реализованные validator, undo/redo, save/load или scenario authoring tools.
* Exact TypeScript/Zod schemas не фиксировались.
* Exact semver/content hash policy не зафиксирована.
* Exact authoring transaction model не зафиксирован.
* Exact runtime undo strategy не принят.
* Exact "save as scenario" UX и правила переноса runtime variables не приняты.
* Этот ответ — planning-only recommendation, не accepted local decision.

## Candidate Navigation Entry

V1-20260523-144154: Planning-only ответ по validation, undo/redo и `save as scenario` для `Table Sandbox 0.1`. Рекомендация: перед Play Sandbox Preview блокировать структурно невалидные module/save references, warning-only оставить для безопасных metadata cases; authoring undo/redo и runtime undo/redo разделить концептуально, runtime undo лучше отложить; `save as scenario` не делать частью первого slice, later реализовать как явное создание нового scenario из extracted setup без event log.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-131910_planning-only-otvet-po-stack-model-dlya-table.md "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md "raw.githubusercontent.com"
