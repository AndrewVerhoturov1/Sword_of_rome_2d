# Notebook Entry

- External Question ID: `V1-20260527-003610`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-27_V1-20260527-003610_practical-route-to-dual-goal-editor-parity-with.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/project_state.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/plans/master/prototype_integration_mapping.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/plans/master/module_authoring_workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/table-sandbox/src/App.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/table-sandbox/src/editor/EditorSurface.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/table-sandbox/src/renderer/PhaserStage.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/table-sandbox/src/renderer/phaserScene.ts`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/README.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/external_chats/V1_navigation.md`

## Candidate Navigation Entry

Topic: Practical route to dual goal: editor parity with the map-editor prototype and play/test continuity with authored editor results
Summary: Recommendation: first build `Editor → Play Visual Continuity Bridge 0.1` by deriving separate `MapRenderModel` from `MapDraft`, passing it to Phaser alongside `GameState`, rendering authored underlay/map size in play mode with zoom/fit-to-map, and keeping `GameState` separate. Then proceed through runtime viewport/underlay rendering, test pieces, validation bridge, editor UI parity packs, connection parity, map save/export hardening, and later Scenario Authoring 0.1.

## Raw Response

## External Question ID

V1-20260527-003610

## Context Readback

* `external_chat_rules.md`: fully read. ([GitHub][1])
* Central `repo_navigation.md`: fully read. ([GitHub][2])
* Project `.ai/repo_navigation.md`: partially read; visible public/project-specific context, reading order, and local-only boundary were read. ([GitHub][3])
* Project `.ai/project_state.md`: fully read for available content. ([GitHub][4])
* `prototype_integration_mapping.md`: fully read. ([GitHub][5])
* `module_authoring_workflow.md`: fully read. ([GitHub][6])
* `table-sandbox/src/App.tsx`: partially read; relevant `editorDraft`, `draftToGameState`, editor/play switch and runtime action sections were read. ([GitHub][7])
* `table-sandbox/src/editor/MapDraft.ts`: attempted, but raw open returned an internal error; not read directly in this pass. 
* `table-sandbox/src/editor/EditorSurface.tsx`: partially read; relevant editor tools, underlay, grid/snap, undo/redo, spaces/connections and preview behavior were read. ([GitHub][8])
* `table-sandbox/src/renderer/PhaserStage.tsx`: fully read for available content. ([GitHub][9])
* `table-sandbox/src/renderer/phaserScene.ts`: partially read; relevant renderer/input, spaces/connections/pieces and drag behavior were read. ([GitHub][10])
* Reference prototype tree: partially read through provided prototype source links.
* Reference prototype `README.md`: fully read. ([GitHub][11])
* Reference prototype `src/App.jsx`: partially read; relevant map/image/layer/grid/snap/spaces/connections/zones/curve-point behavior was inspected. ([GitHub][12])
* Project `V1_navigation.md`: partially read; visible relevant editor/prototype/runtime continuity entries were read, recent V2 workflow reviews were not used as primary context. ([GitHub][13])
* Earlier V1 `V1-20260526-000901`: not re-opened in this final pass; prior summary only, not used as direct source claim.
* Earlier V1 `V1-20260525-063455`: not re-opened in this final pass; prior summary only, not used as direct source claim.
* Earlier V1 `V1-20260525-051950`: not re-opened in this final pass; prior summary only, not used as direct source claim.
* Earlier V1 `V1-20260523-161245`: not re-opened in this final pass.
* Earlier V1 `V1-20260523-153658`: not re-opened in this final pass.
* Context Excerpts from prompt: fully read.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

`external_chat_rules.md` требует точный `External Question ID`, честный `Context Readback`, разделение подтверждённых фактов и непроверенного, а также запрещает утверждать, что внешний чат видел локальный shell, git, tests или runtime, если это не было явно передано. ([GitHub][1])

Central `repo_navigation.md` подтверждает, что central navigation не даёт права утверждать факты о consumer repo без явно переданных project-specific links/excerpts. ([GitHub][2])

### Confirmed from provided excerpts

Project navigation подтверждает, что это repo про browser-based editor / authoring tool для 2D counter-based варгеймов, а Sword of Rome-like материалы здесь являются первым тестовым модулем и reference layer, не конечной целью продукта. ([GitHub][3])

Project state подтверждает текущий этап: `Table Sandbox 0.1: Play Sandbox Ready + Map Authoring 0.1 accepted baseline + 0020 checkpointed editor-growth state`. Там же зафиксировано, что уже есть `0017` Play Sandbox Readiness, `0018` Map Authoring 0.1, а `0020` добавил underlay / terrain image, move/scale/rotate, opacity, visibility, lock, grid/snap и editor-only undo/redo, но ещё не считается полностью polished baseline. ([GitHub][4])

`App.tsx` подтверждает главный bridge-gap: `editorDraft` живёт отдельно, `draftToGameState()` переносит в runtime только `spaces` и `connections`, создаёт `pieces: []`, `controlState: {}`, и помечает `bootstrapMeta.source = "editor-preview"`. ([GitHub][7])

`PhaserStage.tsx` подтверждает, что play/test renderer сейчас создаётся с фиксированными `width: 800`, `height: 500` и `Phaser.Scale.FIT`, то есть play/test mode пока не следует настоящему размеру authored map. ([GitHub][9])

`phaserScene.ts` подтверждает, что Phaser-сцена сейчас является renderer/input layer: она рендерит `spaces`, `connections`, `pieces` из `GameState`, принимает input, обрабатывает drag pieces и передаёт structured input наружу; source of truth остаётся вне Phaser. Видимого пути для editor underlay / terrain image внутри runtime scene в прочитанном фрагменте нет. ([GitHub][10])

`module_authoring_workflow.md` подтверждает целевую рабочую петлю: авторинг создаёт module package, Play Sandbox Preview проверяет runtime behavior, runtime changes идут через `GameState`/`eventLog`, а Play Sandbox не должен молча переписывать authoring definitions. ([GitHub][6])

`prototype_integration_mapping.md` подтверждает важную границу: prototype — reference/selective donor for Map Editor, но не product-code foundation; можно адаптировать layout, object list, inspector, canvas interactions, validation affordances, export affordances, zoom/pan/snap, но нельзя слепо переносить single large `App.jsx`, prototype state или anything that blurs authoring and runtime. ([GitHub][5])

Reference prototype показывает полезные UX-фичи для parity: image/test map, layer/object behavior, grid/snap, map objects following underlay, spaces, connections, zones and curve-point behavior. ([GitHub][12])

Из prompt excerpts также принято как более свежий human override: текущая тема `map-plane / rotate / underlay geometry` считается достаточно закрытой для движения дальше; её можно учитывать как background risk, но не делать главным следующим шагом.

### Not available / not verified

Я не запускал приложение, браузер, сборку, typecheck, тесты, git или локальный runtime. Я не проверял фактическое пользовательское поведение play/test mode глазами, кроме того, что описано в prompt excerpts.

`MapDraft.ts` в этом финальном проходе не был прочитан напрямую из-за internal error raw-open; выводы по модели draft опираются на `project_state.md`, `App.tsx`, `EditorSurface.tsx` и prompt excerpts. 

Я не делал полный review всего CSS/visual polish. План ниже — bounded architectural/product route, а не UI-pixel audit.

### Current State Assessment

Текущий проект уже имеет два важных слоя: **map editor** и **play/test sandbox**. Editor уже умеет гораздо больше, чем первый минимальный slice: есть underlay, transform controls, opacity/show-hide/lock, grid/snap, undo/redo, spaces, connections, object list, inspector, validation и preview. Это хорошая база для движения к prototype parity. ([GitHub][4])

Play/test mode тоже не пустой: он уже умеет runtime `GameState`, Action/Event pipeline, drag фишек, выбор stack, create/delete pieces, change control, reset, save/load snapshot. Но как preview созданной в editor карты он пока слабый. `draftToGameState()` передаёт только graph data: spaces and connections. Underlay, authored visual map, map display settings and real map size currently do not appear as an explicit runtime render contract. ([GitHub][7])

Главная текущая проблема не в том, что редактор совсем слабый. Главная проблема в том, что **editor и play/test mode не говорят на одном визуальном языке**. В editor пользователь собирает карту с подложкой, а play/test пока больше похож на старую runtime-схему в фиксированном `800×500` Phaser canvas. ([GitHub][9])

### Gap To Goal

#### 1. Gap: editor vs reference prototype

До prototype parity по карте, точкам и связям editor-у ещё не хватает не столько "ядра", сколько удобства и широты UX:

```text
- более зрелая левая панель объектов / дерево объектов;
- более удобный inspector для карты, подложки, точек и связей;
- visibility / lock / object-state affordances для map objects;
- более удобные context menus;
- более сильный connection editor;
- выделение, редактирование, удаление, типы / свойства связей;
- позднее — curve points / изгибы связей;
- validation/export affordances ближе к prototype;
- визуальное ощущение полноценного рабочего стола карты.
```

Prototype полезен как UX-донор именно для этих вещей, но не как архитектурная база. Это прямо согласовано с project plan: "controlled reference + selective extraction," not wholesale migration. ([GitHub][5])

#### 2. Gap: runtime/play vs authored editor result

Это более приоритетный gap.

Сейчас pipeline выглядит примерно так:

```text
MapDraft в editor
→ draftToGameState()
→ GameState со spaces/connections
→ pieces: []
→ Phaser 800×500
→ renderer рисует spaces/connections/pieces
→ underlay/map visual отсутствует как явный contract
```

Это подтверждается `App.tsx`, `PhaserStage.tsx` and `phaserScene.ts`. ([GitHub][7])

То есть editor может уже быть довольно богатым, но play/test не является полноценной проверкой authored map. Пользовательская цель "создал карту → нажал проверить → увидел ту же карту → приблизил → подвигал фишки" пока не закрыта.

Правильная целевая граница:

```text
GameState = runtime state:
pieces, piece locations, control, turn, event log.

MapRenderModel / MapVisual = display model:
map size, underlay image, underlay transform/display settings, coordinate basis.
```

Так мы не смешиваем authoring draft и runtime `GameState`, но даём play/test mode возможность реально отрисовать authored map. Это соответствует workflow boundary: authoring edits definitions, play sandbox edits runtime state and event log, and runtime must not silently rewrite definitions. ([GitHub][6])

### Recommended Route

#### 1. Editor → Play Visual Continuity Bridge

Это первый фундаментальный этап всей цели.

Нужно ввести отдельный shared display contract между editor и runtime renderer:

```text
MapRenderModel / MapVisualState:
- mapId;
- coordinateSystem width/height;
- underlay src / naturalWidth / naturalHeight;
- underlay offset / scale / rotation;
- opacity;
- visible;
- maybe display-only grid metadata, если нужно.
```

В `App.tsx` при preview нужно производить две вещи:

```text
1. runtime GameState из spaces/connections;
2. отдельный mapVisual из coordinateSystem + underlay.
```

`GameState` не должен становиться хранилищем картинки карты. Но `PhaserStage` должен получать `mapVisual` рядом с `gameState`.

Результат этапа:

```text
нажал "preview" → play/test получает не только graph, но и визуальную карту.
```

#### 2. Phaser viewport / map-size support

После появления `mapVisual` нужно убрать ощущение маленького фиксированного окна.

`PhaserStage.tsx` сейчас создаёт Phaser config с `width: 800`, `height: 500`, `Scale.FIT`. Это нормально для early sandbox, но плохо для authored maps. ([GitHub][9])

Нужно сделать bounded viewport pack:

```text
- world bounds берутся из authored map/mapVisual;
- initial camera = fit-to-map;
- zoom in/out;
- reset camera / fit map;
- pan или drag camera;
- сохранить piece drag behavior.
```

Результат этапа:

```text
большая карта видна в play/test,
её можно приблизить/отдалить,
и она не живёт внутри старого 800×500 мира.
```

#### 3. Runtime underlay rendering

Теперь Phaser scene должна отрисовать authored underlay behind connections/spaces/pieces.

Порядок слоёв:

```text
underlay image
→ connections
→ spaces
→ pieces
→ selection / drag visuals
```

При этом Phaser остаётся renderer/input only. Source of truth остаётся в React/runtime state. Это важно, потому что `phaserScene.ts` уже явно описывает Phaser как слой, который не хранит authoritative runtime state. ([GitHub][10])

Результат этапа:

```text
точки, связи и фишки визуально совпадают с картой-подложкой.
```

#### 4. Test pieces for preview

Сейчас `draftToGameState()` создаёт `pieces: []`, значит из editor preview пользователь попадает в play/test без фишек. ([GitHub][7])

Полноценный Scenario Editor делать ещё рано, но для проверки карты нужен временный test affordance:

```text
- кнопка "Добавить тестовую фишку";
- поставить тестовую фишку на выбранную/первую точку;
- двигать её по связям;
- не сохранять это как authored scenario silently.
```

Лучший bounded вариант: кнопка в play/test mode, а не автоматическое создание "настоящего сценария".

Результат этапа:

```text
можно проверить карту как игровую поверхность,
даже до полноценного Scenario Editor.
```

#### 5. Runtime/editor validation bridge

Добавить проверки, что authored map действительно можно показать и протестировать:

```text
- map has spaces;
- connections point to existing spaces;
- underlay display data exists or is intentionally absent;
- mapVisual can be rendered;
- play/test can fit authored bounds;
- if pieces are empty, UI explains how to add a test piece.
```

Это должен быть validation bridge между editor and play/test, а не broad rules engine.

#### 6. Editor UI Parity Pack 1 — panels and inspectors

Когда continuity закрыта, начать догонять prototype по editor UX:

```text
- левая object tree / object list лучше, чем сейчас;
- отдельные группы: карта / подложка / точки / связи;
- более аккуратный inspector;
- ясные actions: rename, delete, lock, visible;
- context menu polish;
- validation panel polish.
```

Это можно адаптировать из prototype как UX pattern. Prototype integration mapping explicitly allows adapting left object list, right inspector layout, canvas interaction, validation affordances, zoom/pan/snap ideas. ([GitHub][5])

#### 7. Editor Connection Parity Pack

Довести связи ближе к prototype:

```text
- легче выбрать связь;
- clearer selected connection visual;
- delete/edit from inspector and context menu;
- connection type/name;
- maybe label;
- later: curve point / bend / make straight.
```

Curve points есть в prototype, но они должны идти после continuity and basic connection UX, not before. ([GitHub][12])

#### 8. Editor Map Surface Polish Pack

Довести визуальные ощущения editor до уровня prototype:

```text
- better hover/selection states;
- grid and snap UX polish;
- map pan/zoom controls;
- underlay inspector polish;
- nicer Russian UI text;
- object state indicators.
```

Это уже parity polish, а не foundation.

#### 9. Map save/export/import hardening

После continuity и basic parity нужно закрепить, что считается canonical map data, а что editor-only:

```text
canonical:
- spaces;
- connections;
- coordinateSystem;
- map visual underlay metadata, если решено считать её частью карты.

editor-only:
- current zoom;
- current selection;
- transient messages;
- local UI state.

runtime-only:
- pieces created for playtest;
- event log;
- save snapshot.
```

Это важно, чтобы сохранить границу authoring mode vs play sandbox mode. ([GitHub][6])

#### 10. Scenario Authoring 0.1

Только после того как map editor and play/test continuity работают, переходить к сценарию:

```text
- стартовые фишки;
- стартовые позиции;
- стартовый контроль;
- scenario validation;
- preview in play sandbox.
```

Это логично по module authoring workflow: сначала map, потом pieces/factions and scenario setup, then preview and runtime loop. ([GitHub][6])

### Best Next Step

Лучший следующий bounded practical step:

```text
Editor → Play Visual Continuity Bridge 0.1
```

Состав:

```text
1. Создать отдельный `MapRenderModel` / `MapVisualState`, не смешивая его с `GameState`.
2. В `App.tsx` при preview получать:
   - `GameState` из spaces/connections;
   - `mapVisual` из coordinateSystem + underlay.
3. Передать `mapVisual` в `PhaserStage`.
4. Подготовить `PhaserStage`/scene к authored map size вместо фиксированного 800×500.
5. Отрисовать underlay в play/test под spaces/connections/pieces.
6. Добавить fit-to-map / zoom controls.
7. Сохранить drag pieces and Action/Event pipeline.
```

Почему именно это первым: если сначала делать editor красивее, но play/test всё ещё не показывает authored map, основной рабочий цикл продукта останется сломанным. Product route должен сначала закрыть "создал → проверил → вернулся исправить". Это прямо соответствует module authoring workflow, где Play Sandbox Preview является частью authoring loop, но не заменяет authoring definitions. ([GitHub][6])

### Non-Goals / What To Avoid

Не возвращать старую `map-plane / rotate / underlay geometry` тему как главный следующий этап. Prompt explicitly says it is closed enough to move on; treat it only as background risk.

Не делать wholesale prototype migration. Prototype должен быть reference/selective donor, not product-code foundation. ([GitHub][5])

Не переносить underlay image directly into `GameState` as authoritative runtime state. Для этого нужен отдельный display/render contract.

Не строить сразу full layer system, zones, curved connections, full package export/import, cards, documents, rules editor or scenario editor in one step.

Не делать Phaser source of truth. Current scene already states Phaser is renderer/input only and source of truth is outside Phaser. ([GitHub][10])

Не создавать "настоящий сценарий" из play/test runtime actions silently. Runtime snapshot and authoring definitions must stay separate. ([GitHub][6])

## Candidate Navigation Entry

V1-20260527-003610: Practical route to dual goal: editor parity with the map-editor prototype and play/test continuity with authored editor results. Recommendation: first build `Editor → Play Visual Continuity Bridge 0.1` by deriving separate `MapRenderModel` from `MapDraft`, passing it to Phaser alongside `GameState`, rendering authored underlay/map size in play mode with zoom/fit-to-map, and keeping `GameState` separate. Then proceed through runtime viewport/underlay rendering, test pieces, validation bridge, editor UI parity packs, connection parity, map save/export hardening, and later Scenario Authoring 0.1.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/repo_navigation.md
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/project_state.md
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/plans/master/prototype_integration_mapping.md
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/plans/master/module_authoring_workflow.md
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/table-sandbox/src/App.tsx
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/table-sandbox/src/editor/EditorSurface.tsx
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/table-sandbox/src/renderer/PhaserStage.tsx
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/table-sandbox/src/renderer/phaserScene.ts
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/README.md
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/c313aa9e99c81c22eb4bd0b644e45ca12b89cea8/.ai/external_chats/V1_navigation.md
