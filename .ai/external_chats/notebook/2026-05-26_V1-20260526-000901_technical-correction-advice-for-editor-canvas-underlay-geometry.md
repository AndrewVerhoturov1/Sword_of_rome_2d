# Notebook Entry

- External Question ID: `V1-20260526-000901`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-26_V1-20260526-000901_technical-correction-advice-for-editor-canvas-underlay-geometry.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/sessions/2026-05-23_architecture_orchestration_v1_planning.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/prototype_integration_mapping.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/EditorSurface.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/Editor.css`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/MapDraft.ts`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/App.tsx`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/App.css`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/index.css`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/fixtures/tiny-module/modules/tiny-module/map.json`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/package.json`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx`

## Candidate Navigation Entry

Topic: Technical correction advice for editor canvas / underlay geometry
Summary: Verdict: the user's intuition is right—the fixed 800×500 grid should not be treated as the whole editor world. Recommended bounded fix: introduce a clear map-plane model using `draft.coordinateSystem` as active authoring size, separate viewport camera from map-local coordinates, resize or fit map plane explicitly when loading large images, render underlay/grid/spaces/connections in one coordinate system, and avoid wholesale prototype migration or runtime/GameState mixing.

## Raw Response

## External Question ID

V1-20260526-000901

## Context Readback

* Uploaded prompt / `Вставленный текст.txt`: fully read. 
* `external_chat_rules.md`: fully read. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md))
* Central `repo_navigation.md`: fully read. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md))
* Project `.ai/external_chats/V1_navigation.md`: partially read; only visible returned content was available. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md))
* Project `.ai/repo_navigation.md`: partially read; opened, but only minimal visible content was returned. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md))
* Project `README.md`: partially read; opened, but only minimal visible content was returned. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md))
* Project `AGENTS.md`: partially read; opened, but only minimal visible content was returned. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md))
* Project `.ai/project_state.md`: fully read for available content. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md))
* Session plan `2026-05-23_architecture_orchestration_v1_planning.md`: fully read for available content. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/sessions/2026-05-23_architecture_orchestration_v1_planning.md))
* `.ai/plans/master/prototype_integration_mapping.md`: partially read; opened, but only minimal visible content was returned. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/prototype_integration_mapping.md))
* Previous notebook `V1-20260525-063455`: not read; raw open returned an internal error.
* `table-sandbox/src/editor/EditorSurface.tsx`: fully read for available raw content. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/EditorSurface.tsx))
* `table-sandbox/src/editor/Editor.css`: fully read for available raw content. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/Editor.css))
* `table-sandbox/src/editor/MapDraft.ts`: fully read for available raw content. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/MapDraft.ts))
* `table-sandbox/src/App.tsx`: partially read; opened, but only minimal visible content was returned. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/App.tsx))
* `table-sandbox/src/App.css`: partially read; opened, but only minimal visible content was returned. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/App.css))
* `table-sandbox/src/index.css`: partially read; opened, but only minimal visible content was returned. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/index.css))
* `table-sandbox/src/fixtures/tiny-module/modules/tiny-module/map.json`: fully read. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/fixtures/tiny-module/modules/tiny-module/map.json))

Prototype parts inspected:

* Prototype `package.json`: fully read; confirms React/Vite prototype without Phaser. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/package.json))
* Prototype `src/App.jsx`: fully read for available raw content. I specifically inspected visible parts around image/test map layer, layer move/scale/rotate, reset rotation, grid, context menu, binding objects to layer, inspector fields, visibility/lock, and curve-point affordance. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx))

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

`external_chat_rules.md` requires exact `External Question ID`, honest `Context Readback`, separation of confirmed and unverified information, and forbids claiming local shell/git/build/runtime access unless it was actually available. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md))

Central `repo_navigation.md` says central navigation does not authorize claims about a consumer repo unless project-specific links or excerpts were provided. In this question, project-specific links and excerpts were provided explicitly. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md))

### Confirmed from provided excerpts

The prompt says the current problem appears after starting `Map Underlay + Transform + Undo Pack`: a large custom map image is bigger than the fixed editor grid/canvas, scaling can make it "fly away," movement feels strange, and the image/point graph can drift apart. It also says the current editor plane comes from `map.json` with `coordinateSystem.width = 800` and `height = 500`, and that local review suspects transform-model inconsistency. 

The prompt also preserves key product constraints: do not move authority into Phaser, do not collapse authoring draft into runtime `GameState`, do not do wholesale prototype migration, and keep this as a bounded correction path rather than a giant editor-platform redesign. 

### Confirmed from prototype inspection

The prototype is a React/Vite editor prototype without Phaser, so it should remain a reference/donor for editor behavior rather than the product runtime/renderer architecture. Its `package.json` lists Vite and React dependencies and does not list Phaser. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/package.json))

The prototype has useful map-underlay behavior: adding an image, adding a test map, layer move, layer scale, layer rotate, reset layer rotation, grid display, layer context menu actions, and a command to bind objects to a layer. These are visible in `App.jsx`, including "Добавить изображение," "Добавить тестовую карту," "перемещать слой," "масштабировать слой," "поворачивать слой," "Сбросить поворот слоя," and "Привязать объекты к этому слою." ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx))

The prototype also exposes richer layer/object inspector behavior: layer visibility/lock, x/y, width/height, rotation and z-index fields; space fields for x/y/size/order/visibility/lock; and connection curve-point affordance. This supports using it as a mental model for editor convenience, not as a wholesale code source. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/arena-test/main/prototypes/table-map-editor-canvas-local-fixed/source/src/App.jsx))

### Not available / not verified

I did not run the local project, browser, prototype demo, typecheck, build, git status, or inspect the current local underlay implementation directly. The raw `EditorSurface.tsx` visible through GitHub appears to show the earlier fixed-plane editor and does not show the full local underlay transform code described in the prompt. Therefore, the specific "image transform around center vs helper math from top-left" issue is treated as provided local review context, not independently verified from the public raw file.

### Main assessment

The user's intuition is right: the current "small sheet with grid" should be reconceived.

The immediate bug is probably partly transform math, but the deeper product problem is the mental model: the editor currently treats `800×500` as the whole working world. That was fine for a tiny fixture, but it is wrong for a real map editor where the user may load a large custom map image.

The correction should not be a full rewrite. The bounded fix is to introduce a clear **map plane + viewport/camera + optional underlay** model and make all coordinate conversion use that model consistently.

### What the small fixed grid area currently is

Right now the small fixed grid is effectively the **logical authoring plane** of the map, not just the viewport and not the real terrain image.

This is visible in current code: `EditorSurface.tsx` reads `CANVAS_W` and `CANVAS_H` from `mapData.coordinateSystem.width/height`, then uses those constants for stage width/height, clamping and pointer-to-world conversion. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/EditorSurface.tsx))

The current fixture really is `800×500`: `map.json` has `"coordinateSystem": { "type": "pixel", "width": 800, "height": 500 }`. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/fixtures/tiny-module/modules/tiny-module/map.json))

So, in plain terms:

```text
The editor currently thinks:
my map world = 800×500.
```

That is the core reason a large custom image feels trapped or strange: the image is being inserted into a small logical map plane instead of defining or fitting a proper map plane.

### What the map underlay should be relative to that area

The underlay should not be "a big picture floating inside a small 800×500 sheet."

The better conceptual model is:

```text
Editor viewport:
the visible browser area.

Editor camera:
pan and zoom of the user's view.

Map plane:
the logical editable map surface.

Map underlay:
an optional image inside that map plane.

Map objects:
spaces, connections, zones later, all in map-plane coordinates.
```

In that model, the `800×500` area is not sacred. It is just the current fixture's map-plane size. If the user loads a large custom image, the editor should offer to make the map plane match that image size, or at least fit the image into the current map plane in a predictable way.

### Best correction direction now

Recommended correction:

```text
Map Plane Coordinate Model Fix
```

The goal is not to add more UI. The goal is to make the geometry sane.

The bounded correction should:

```text
1. Stop treating imported `mapData.coordinateSystem.width/height` constants as permanent editor-world constants.
2. Use `draft.coordinateSystem.width/height` as the current map-plane size.
3. Support resizing the map plane when a custom underlay image is loaded.
4. Separate viewport/camera pan+zoom from map-plane/underlay transform.
5. Make pointer conversion use one shared transform/inverse-transform path.
6. Render underlay, grid, spaces and connections in the same map-plane coordinate system.
```

This is a small model correction, not a giant architecture rewrite.

### Coordinate and transform model

Recommended storage:

```text
Spaces:
stored in map-local coordinates.

Connections:
stored by space IDs, not by screen points.

Map plane:
has width/height.

Underlay:
has image data/source and placement metadata.

Viewport/camera:
has pan/zoom only for viewing the editor.

Optional map-plane transform:
used only if the whole map plane is moved/scaled/rotated as one visual group.
```

Important rule:

```text
Do not rewrite every space coordinate whenever the underlay/map plane is moved, scaled or rotated.
```

A safer model:

```text
Store spaces in map-local coordinates.
Render them through the same map-plane transform as the underlay.
When the user moves a space, convert pointer position back through the inverse transform into map-local coordinates.
```

The problem to avoid:

```text
image uses one transform origin,
coordinate helpers assume another origin,
grid uses a third coordinate system.
```

That is exactly the kind of mismatch that produces "flying away," one-axis movement, and drift between image and points.

For a bounded correction, use one shared pair of helpers:

```text
mapToScreen(point)
screenToMap(point)
```

Everything interactive should go through those helpers.

### Grid meaning recommendation

There are two possible grids:

```text
1. Screen helper grid:
   stays fixed relative to the viewport.

2. Map-plane grid:
   belongs to the map and is used for snapping spaces.
```

For this project right now, the grid should be a **map-plane grid**.

That means:

```text
- it represents map-local coordinates;
- spaces snap to it;
- it scales with editor zoom;
- if the map plane is rotated, it should rotate with the map plane;
- it should be rendered in the same coordinate system as underlay, spaces and connections.
```

The current CSS background grid in `Editor.css` is just an editor background pattern; it is not enough as a real map-plane grid. It is fine as decoration, but snap/grid logic should be tied to map-plane coordinates. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/Editor.css))

### Large image handling recommendation

When the user adds a much larger custom image, the cleanest bounded behavior is:

```text
Ask/offer:
"Use image size as map size?"
```

Recommended default:

```text
For first real custom image:
set map plane width/height to the image natural width/height.
```

Alternative option:

```text
Fit image into current map size.
```

But this should be explicit, not accidental.

The useful choices are:

```text
1. Use image size as map size.
2. Fit image into current map plane.
3. Keep current map plane and place image manually.
```

For the current user problem, choice 1 is the most natural: if the user loads a large map, the editable map plane should grow to match it instead of forcing the image into `800×500`.

Also, the editor viewport should remain free: the user should pan and zoom around the map plane, not feel trapped inside a tiny fixed sheet.

### Must-fix now

1. **Stop using hardcoded fixture constants as editor-world truth.**
   `CANVAS_W` and `CANVAS_H` are currently derived from imported fixture `mapData`, not from the editable draft. That makes the editor world behave like the original tiny fixture even if the draft or underlay wants to be larger. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/EditorSurface.tsx))

2. **Use `draft.coordinateSystem.width/height` everywhere for map-plane bounds.**
   `MapDraft` already has `coordinateSystem.width/height`, so the editor should use that as the active map-plane size. ([raw.githubusercontent.com](https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/table-sandbox/src/editor/MapDraft.ts))

3. **Add a clear image-load behavior.**
   When adding a custom image, either resize the map plane to the image natural size or explicitly fit it into the current map plane. Do not let a large image silently float in a smaller coordinate plane.

4. **Unify coordinate conversion.**
   All pointer handling, object dragging, underlay rendering, grid rendering and snap should use the same map-local coordinate model.

5. **Make grid map-plane based.**
   For snapping, the grid should exist in map-local coordinates, not as an unrelated screen background.

6. **Keep authoring separate from runtime.**
   This belongs in `MapDraft` / editor state. It must not become `GameState` or runtime snapshot state.

### Nice-to-have later

1. A truly large/infinite-feeling workspace around the map plane.
2. Multiple background layers.
3. Layer ordering.
4. Rich layer inspector.
5. Separate screen grid and map grid.
6. Rotation-aware snapping improvements.
7. Export/import of image assets as part of a mature module package.
8. Zones and curved connections.
9. Full map size editor panel.
10. Advanced align tools.

These are useful, but they should wait until the basic map-plane model is fixed.

### What Codex should ask Kilo to do next

```text
Implement a bounded Map Plane Coordinate Model Fix.

Goal:
Fix the current editor canvas / underlay geometry problem so large custom map images do not behave as if trapped inside the tiny 800×500 fixture sheet.

Core correction:
- Treat the editor map as a map plane with its own coordinateSystem.
- Use draft.coordinateSystem.width/height as the active authoring plane size.
- Stop using imported fixture constants as permanent editor-world truth.
- Keep viewport/camera pan+zoom separate from map-plane coordinates.
- Render underlay, grid, spaces and connections in one consistent map-plane coordinate system.
- Make pointer conversion go through shared helpers: screen/client -> map-local and map-local -> screen/render.

Large image behavior:
- When a custom underlay image is added, provide a bounded default:
  use the image natural size as the map plane size, or explicitly fit the image into the current map plane.
- Do not silently place a large image inside a smaller fixed 800×500 plane.

Grid:
- Treat the snap grid as a map-plane grid.
- Spaces snap in map-local coordinates.
- Do not rely on only a CSS background grid for snapping.

Important boundaries:
- Do not move this state into runtime GameState.
- Do not move authority into Phaser.
- Do not migrate the prototype wholesale.
- Do not add full multi-layer system.
- Do not add zones/curved connections in this correction.
- Do not add a broad editor redesign.

Acceptance:
- A large custom image no longer feels trapped by the old 800×500 fixture plane.
- Map plane size can reflect the underlay image size or a clear explicit fit mode.
- Spaces and connections remain aligned with the underlay during pan/zoom and underlay/map-plane transforms.
- Pointer clicks and drags land in the expected map-local positions.
- Scaling does not make the image fly away.
- Moving does not collapse into mostly one-axis behavior.
- Grid/snap use map-local coordinates.
- Existing add/move/delete/rename space and create/delete connection still work.
- Preview to sandbox still works.
- Runtime GameState remains separate from authoring MapDraft.
```

## Candidate Navigation Entry

V1-20260526-000901: Technical correction advice for editor canvas / underlay geometry. Verdict: the user's intuition is right—the fixed 800×500 grid should not be treated as the whole editor world. Recommended bounded fix: introduce a clear map-plane model using `draft.coordinateSystem` as active authoring size, separate viewport camera from map-local coordinates, resize or fit map plane explicitly when loading large images, render underlay/grid/spaces/connections in one coordinate system, and avoid wholesale prototype migration or runtime/GameState mixing.
