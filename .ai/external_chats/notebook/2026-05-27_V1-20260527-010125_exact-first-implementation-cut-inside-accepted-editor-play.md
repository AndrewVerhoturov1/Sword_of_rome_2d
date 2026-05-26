# Notebook Entry

- External Question ID: `V1-20260527-010125`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-27_V1-20260527-010125_exact-first-implementation-cut-inside-accepted-editor-play.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/plans/implementation/editor_play_visual_continuity_route.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/external_chats/notebook/2026-05-27_V1-20260527-003610_practical-route-to-dual-goal-editor-parity-with.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/project_state.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/plans/master/prototype_integration_mapping.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/plans/master/module_authoring_workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/App.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/editor/MapDraft.ts`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/editor/EditorSurface.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/renderer/PhaserStage.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/renderer/phaserScene.ts`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/package.json`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/README.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx`

## Candidate Navigation Entry

Topic: Exact first implementation cut inside accepted `Editor -> Play Visual Continuity Bridge 0.1`
Summary: Recommendation: start with `MapRenderModel Contract Wire-Up 0.1`: create a shared `MapRenderModel` type, derive it from `MapDraft` in `App.tsx`, pass it separately from `GameState` into `PhaserStage`/`TableSandboxScene`, and render only a lightweight map/underlay bounds debug layer. Do not yet implement actual underlay image texture loading, zoom, pan, fit-to-map, scenario pieces, or GameState shape changes.

## Raw Response

## External Question ID

V1-20260527-010125

## Context Readback

* `external_chat_rules.md`: fully read. ([GitHub][1])
* Central `repo_navigation.md`: fully read. ([GitHub][2])
* Published implementation route `editor_play_visual_continuity_route.md`: fully read. ([GitHub][3])
* Published source V1 answer `V1-20260527-003610`: partially read; relevant route summary and raw-answer sections were read. ([GitHub][4])
* Project `V1_navigation.md`: partially read; relevant continuity entry was read, V2 workflow entries were not used as primary context. ([GitHub][5])
* Project `.ai/repo_navigation.md`: fully read for available content. ([GitHub][6])
* Project `.ai/project_state.md`: fully read for available content. ([GitHub][7])
* `prototype_integration_mapping.md`: fully read. ([GitHub][8])
* `module_authoring_workflow.md`: fully read. ([GitHub][9])
* `table-sandbox/src/App.tsx`: partially read; relevant `editorDraft`, `draftToGameState`, preview/play switch, runtime actions and UI sections were read. ([GitHub][10])
* `table-sandbox/src/editor/MapDraft.ts`: partially read; relevant `MapDraft`, `UnderlayState`, `EditorSettings`, and separation comments were read. ([GitHub][11])
* `table-sandbox/src/editor/EditorSurface.tsx`: partially read; relevant preview button and underlay controls were inspected. ([GitHub][12])
* `table-sandbox/src/renderer/PhaserStage.tsx`: fully read for available content. ([GitHub][13])
* `table-sandbox/src/renderer/phaserScene.ts`: partially read; relevant renderer/input boundary, `updateFromState`, drawing and drag behavior were read. ([GitHub][14])
* `table-sandbox/package.json`: fully read; opened through project navigation because build/typecheck commands are relevant. ([GitHub][15])
* Reference prototype `README.md`: fully read; not heavily used for this first implementation cut. ([GitHub][16])
* Reference prototype `src/App.jsx`: opened but only partially read; not used as a direct source for first-slice implementation details. ([GitHub][17])
* Context Excerpts from prompt: fully read.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require exact external question ID, honest context readback, separation of central-doc facts, provided project facts, and not-verified claims. They also prohibit claiming local shell, git, tests or runtime access unless it was explicitly provided. ([GitHub][1])

Central navigation is only an allowed navigation index for central core files. It does not authorize claims about the consumer repo; consumer repo claims must come from project-specific links or excerpts. ([GitHub][2])

### Confirmed from provided excerpts

The accepted implementation route already fixes the priority: `continuity first -> parity second -> scenario later`. It also says the current blocker is that editor and play/test do not share one explicit visual/render contract. ([GitHub][3])

The same route names the next candidate as `Editor -> Play Visual Continuity Bridge 0.1`, but explicitly leaves the exact first patch set, minimal type shape, grid inclusion, and first-slice acceptance checklist open for this next `/v1`. ([GitHub][3])

Current project state confirms the editor already has underlay, move/scale/rotate, opacity, visibility, lock, grid/snap, undo/redo, spaces/connections, and still keeps authoring draft separate from runtime `GameState`. ([GitHub][7])

`App.tsx` confirms the current bridge gap: `draftToGameState()` converts `MapDraft` into runtime `GameState`, but carries only `spaces` and `connections`; it creates `pieces: []`, `controlState: {}`, and `bootstrapMeta.source = "editor-preview"`. ([GitHub][10])

`MapDraft.ts` already has the needed authoring data for the first visual contract: `coordinateSystem`, `underlay`, `UnderlayState.src`, `offsetX`, `offsetY`, `scale`, `rotation`, `opacity`, `visible`, `locked`, `naturalWidth`, and `naturalHeight`. ([GitHub][11])

`PhaserStage.tsx` currently passes only `gameState`, selection and callbacks into the scene, and still creates a fixed `800×500` Phaser config with `Scale.FIT`. ([GitHub][13])

`phaserScene.ts` states that Phaser is renderer/input only, not authoritative state, and currently renders `spaces`, `connections`, and `pieces` from `GameState`. ([GitHub][14])

The authoring workflow requires authoring changes and runtime changes to remain separate: authoring edits definitions/package data, while Play Sandbox changes runtime `GameState`, event log and save snapshots. ([GitHub][9])

Prototype mapping confirms that the reference prototype should remain a selective donor/reference, not product-code foundation or runtime architecture authority. ([GitHub][8])

### Not available / not verified

I did not run the app, build, typecheck, browser, VS Code, Kilo, local git, or runtime.

I did not verify actual visual behavior in the browser.

I did not inspect all CSS or every line of the long React/Phaser files.

The answer below is therefore a bounded implementation recommendation based on the opened source links, not a claim that the patch has already been tested.

### Chosen First Step

`MapRenderModel Contract Wire-Up 0.1`

Это первый маленький implementation slice внутри `Editor -> Play Visual Continuity Bridge 0.1`.

Смысл: **не пытаться сразу сделать весь bridge**, а сначала ввести минимальный визуальный контракт карты, получить его из `MapDraft` при preview, передать рядом с `GameState` в `PhaserStage` и дальше в `TableSandboxScene`, а в play/test показать лёгкий видимый признак, что runtime renderer получил authored map visual data.

### Why This First Step

Это правильный первый шаг, потому что принятый route говорит: главная проблема сейчас не в слабости editor, а в отсутствии явного visual/render contract между editor и play/test. ([GitHub][3])

Сразу делать image texture loading, camera/world bounds, zoom, pan, fit-to-map и полноценный underlay rendering — слишком большой первый pack. Route сам разделяет эти вещи на отдельные этапы: сначала visual contract, потом viewport/map-size support, потом runtime underlay rendering. ([GitHub][3])

Но делать только тип `MapRenderModel` без передачи в Phaser тоже слишком мало: такой slice не докажет, что renderer boundary реально начал меняться. Поэтому лучший первый cut: **тип + derive from draft + App state + PhaserStage prop + Scene update argument + простой debug/bounds render**.

### Exact Scope

В первый slice входит:

1. Создать минимальный shared type `MapRenderModel`.

2. В `App.tsx` добавить отдельное состояние, например:

```ts
const [mapVisual, setMapVisual] = useState<MapRenderModel | null>(null);
```

3. Добавить локальный adapter в `App.tsx`:

```ts
draftToMapRenderModel(draft: MapDraft): MapRenderModel
```

4. В `handlePreview(draft)` делать две разные вещи:

```text
draftToGameState(draft)       -> runtime GameState
draftToMapRenderModel(draft)  -> visual render contract
```

5. Передать `mapVisual` в `PhaserStage` отдельным prop.

6. Передать `mapVisual` из `PhaserStage` в `scene.updateFromState(...)`.

7. В `phaserScene.ts` добавить минимальный render/debug слой **до** connections/spaces/pieces:

```text
map bounds rectangle / label
optional underlay bounds rectangle / label
```

8. Если `mapVisual === null`, play/test работает как раньше с fixture/runtime state.

9. При fixture reset/load или обычном переходе в fixture play не должно оставаться stale editor `mapVisual`.

10. Существующий `GameState`, Action/Event pipeline, drag pieces и runtime snapshot logic не должны менять смысл.

### Out Of Scope

Не входит в первый slice:

```text
- полноценная загрузка и отрисовка image/dataURL texture в Phaser;
- Phaser texture lifecycle / async image loader;
- zoom controls;
- pan camera;
- fit-to-map;
- изменение Phaser config width/height;
- world bounds from authored map;
- сохранение mapVisual в runtime snapshot;
- Scenario Editor;
- автоматическое создание настоящих scenario pieces;
- изменение GameState shape;
- перенос underlay внутрь GameState;
- full layer system;
- zones;
- curved connections;
- prototype migration;
- polishing editor inspector/object tree.
```

Главное: первый slice должен только провести "провод" visual contract от editor preview до renderer и показать, что он дошёл.

### Minimal Contract

Минимальный контракт лучше сделать отдельным shared type, без зависимости runtime от editor:

```ts
export interface MapRenderModel {
  source: "editor-preview";
  mapId: string;
  name: string;
  coordinateSystem: {
    type: "pixel";
    width: number;
    height: number;
  };
  underlay: MapRenderUnderlay | null;
}

export interface MapRenderUnderlay {
  src: string | null;
  offsetX: number;
  offsetY: number;
  scale: number;
  rotationDeg: number;
  opacityPercent: number;
  visible: boolean;
  naturalWidth: number;
  naturalHeight: number;
}
```

Почему так:

```text
- `MapRenderModel` не является GameState.
- `GameState` остаётся runtime source of truth.
- `MapRenderModel` описывает только visual/display contract.
- opacity лучше назвать `opacityPercent`, чтобы не путать 0–100 из draft с Phaser alpha 0–1.
- rotation лучше назвать `rotationDeg`, чтобы не путать degrees/radians.
- grid metadata не добавлять в первый slice.
- locked не передавать в первый slice: это editor-only behavior, rendererу сейчас не нужно.
```

### Exact File Set

* Modify:

  * `table-sandbox/src/App.tsx`
  * `table-sandbox/src/renderer/PhaserStage.tsx`
  * `table-sandbox/src/renderer/phaserScene.ts`

* Create:

  * `table-sandbox/src/map/MapRenderModel.ts`

* Do not touch yet:

  * `table-sandbox/src/runtime/GameState.ts`
  * `table-sandbox/src/runtime/actionEvent.ts`
  * `table-sandbox/src/runtime/rulesHooks.ts`
  * `table-sandbox/src/runtime/bootstrap.ts`
  * `table-sandbox/src/runtime/snapshot.ts`
  * `table-sandbox/src/editor/MapDraft.ts`
  * `table-sandbox/src/editor/EditorSurface.tsx`
  * `table-sandbox/src/fixtures/**`
  * reference prototype files
  * package/export/import code
  * scenario-related code

`MapDraft.ts` уже содержит нужные поля, поэтому его не нужно менять в первом slice. ([GitHub][11])

### Implementation Order

1. **Create `MapRenderModel.ts`.**
   Только типы. Без runtime logic, без Phaser imports, без editor imports.

2. **Add `draftToMapRenderModel()` inside `App.tsx`.**
   На первом slice лучше держать adapter локально в `App.tsx`, чтобы не создавать premature shared conversion layer.

3. **Add `mapVisual` state in `App.tsx`.**
   Initial value: `null`.

4. **Update `handlePreview(draft)`.**
   После `const gs = draftToGameState(draft)` добавить:

```ts
const visual = draftToMapRenderModel(draft);
setMapVisual(visual);
```

5. **Clear stale `mapVisual` on fixture flows.**
   При reset to fixture, load runtime snapshot, or direct "Играть (fixture)" transition — `setMapVisual(null)`.

6. **Pass `mapVisual` to `PhaserStage`.**

7. **Update `PhaserStageProps`.**
   Add:

```ts
mapVisual: MapRenderModel | null;
```

8. **Update scene call.**
   Change:

```ts
scene.updateFromState(gameState, selectedPieceId, selectedSpaceId);
```

to:

```ts
scene.updateFromState(gameState, selectedPieceId, selectedSpaceId, mapVisual);
```

9. **Update `TableSandboxScene.updateFromState`.**
   Add optional fourth argument:

```ts
mapVisual: MapRenderModel | null
```

10. **Add minimal map visual debug render.**
    Before `drawConnections(state)`, draw:

* map bounds rectangle from `coordinateSystem.width/height`;
* small label: `Map visual: <mapId> <width>x<height>`;
* if underlay exists and visible, draw transformed underlay bounds rectangle using offset/scale/rotation; not the image itself.

11. **Keep all existing interaction behavior unchanged.**
    Piece drag, space click, right-click movement, create/delete/change-control should remain untouched.

### Acceptance Checks

#### Code-level checks

* `MapRenderModel` exists in `table-sandbox/src/map/MapRenderModel.ts`.
* `GameState.ts` is unchanged.
* `draftToGameState()` still returns runtime data only and does not receive underlay fields.
* `draftToMapRenderModel()` exists separately from `draftToGameState()`.
* `PhaserStage` accepts `mapVisual` as a separate prop.
* `TableSandboxScene.updateFromState()` accepts `mapVisual` separately from `GameState`.
* `phaserScene.ts` imports only the shared `MapRenderModel` type, not `MapDraft`.
* No prototype files are copied.
* No new scenario/persistence/export system is added.
* No `any`-based shortcut is introduced just to silence TypeScript.

#### Build/typecheck-level checks

Use the existing scripts from `table-sandbox/package.json`: `typecheck` is `tsc --noEmit`, and `build` is `tsc --noEmit && vite build`. ([GitHub][15])

Required commands:

```bash
cd table-sandbox
npm run typecheck
npm run build
```

Expected result:

```text
typecheck passes
build passes
no new TypeScript errors
no new runtime import cycle caused by editor/runtime coupling
```

#### Human-visible behavior-level checks

1. Open editor.
2. Use existing editor map with underlay/spaces/connections.
3. Press preview.
4. Play/test mode opens as before.
5. Existing spaces and connections still render.
6. Existing play/test interactions still work:

   * select space;
   * create piece;
   * drag piece if possible;
   * right-click fallback if relevant;
   * delete piece;
   * change control.
7. Canvas or play surface shows visible proof of `mapVisual`, for example:

   * map bounds rectangle;
   * map id / size label;
   * underlay bounds rectangle if underlay is present and visible.
8. Actual image rendering is not expected yet.
9. Zoom/pan/fit-to-map is not expected yet.
10. Switching to fixture/reset/load does not leave stale editor map visual on screen.

### Over-Scoping Risks

1. **Trying to render the actual underlay image immediately.**
   That pulls in Phaser texture lifecycle, async loading, data URL handling, texture replacement, cleanup, and error handling. This belongs to the next slice, not the first.

2. **Changing Phaser viewport and camera in the same patch.**
   Viewport, world bounds, zoom, pan, and fit-to-map are separate enough to deserve their own slice after contract wiring.

3. **Putting underlay into `GameState`.**
   This breaks the accepted boundary. Runtime `GameState` should not become the source of truth for authoring visual data.

4. **Importing `MapDraft` into renderer/scene.**
   Renderer should consume `MapRenderModel`, not editor authoring draft. `App.tsx` is the right bridge point for now.

5. **Adding grid metadata too early.**
   Grid is not necessary to prove visual continuity. It can be added later if play/test needs it visually.

6. **Adding Scenario Editor or real initial pieces.**
   Current preview creates `pieces: []`; test pieces are a later slice. First slice should not solve scenario authoring.

7. **Reopening prototype parity work.**
   Object tree, inspector polish, curved connections, zones and layer system are not part of this first continuity cut.

8. **Returning to old rotate/map-plane bug as the main task.**
   It is background risk only. The first implementation step should be about the new bridge contract.

### Optional Second-Best Variant

Second-best variant: **type-only contract slice**.

That would create `MapRenderModel.ts` and `draftToMapRenderModel()`, but not pass it into `PhaserStage` or `phaserScene`.

Why it is worse: it is safer, but too invisible. It does not prove the renderer boundary, does not create a human-visible check, and leaves the project still one step away from knowing whether play/test can receive authored visual data.

The chosen slice is better because it is still small, but it proves the full first wire:

```text
MapDraft -> MapRenderModel -> App state -> PhaserStage prop -> Scene update -> visible debug/bounds render
```

## Candidate Navigation Entry

V1-20260527-010125: Exact first implementation cut inside accepted `Editor -> Play Visual Continuity Bridge 0.1`. Recommendation: start with `MapRenderModel Contract Wire-Up 0.1`: create a shared `MapRenderModel` type, derive it from `MapDraft` in `App.tsx`, pass it separately from `GameState` into `PhaserStage`/`TableSandboxScene`, and render only a lightweight map/underlay bounds debug layer. Do not yet implement actual underlay image texture loading, zoom, pan, fit-to-map, scenario pieces, or GameState shape changes.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/plans/implementation/editor_play_visual_continuity_route.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/external_chats/notebook/2026-05-27_V1-20260527-003610_practical-route-to-dual-goal-editor-parity-with.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/repo_navigation.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/project_state.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/plans/master/prototype_integration_mapping.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/.ai/plans/master/module_authoring_workflow.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/App.tsx "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/editor/MapDraft.ts "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/editor/EditorSurface.tsx "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/renderer/PhaserStage.tsx "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/src/renderer/phaserScene.ts "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/03efb8e3b98363b8510706892fde742174cdf84c/table-sandbox/package.json "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/README.md "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx "raw.githubusercontent.com"
