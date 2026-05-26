# Bug Journal

This journal records important, repeated, or non-obvious bugs and difficulties found during project work.

Use it so future agents can check whether a similar issue already happened and how it was solved.

Do not record every tiny typo. Record issues that may help future debugging.

## Entries

### BUG-20260527-001 — Play/test spaces/connections render без underlay transform (coordinate misalignment)

Status: fixed

Area:
table-sandbox, Phaser scene, Editor → Play continuity, Handoff 0029, Map Plane Alignment 0.1

Symptoms:
После Handoff 0029 (MapRenderModel Contract Wire-Up) в play/test mode mapVisual debug bounds и underlay bounds видны, но spaces, connections и pieces визуально не совпадают с ними по расположению относительно редактора. Точки и связи выглядят так, как будто рисуются в другой системе координат.

Cause:
`phaserScene.ts` рисовал spaces/connections/pieces по координатам `space.x`, `space.y` напрямую — в raw map-local координатах. Редактор (`EditorSurface.tsx`) применяет `mapLocalToWorld(space.x, space.y, underlay)` — center-based offset+scale+rotation transform — ко всем объектам. Без этого transform в play/test объекты оказывались в другом месте относительно map/underlay bounds.

Fix:
1. Добавлен `mapLocalToWorld()` helper в [`MapRenderModel.ts`](table-sandbox/src/map/MapRenderModel.ts:53) — работает только с `MapRenderUnderlay`, не тянет `MapDraft` в renderer.
2. В [`phaserScene.ts`](table-sandbox/src/renderer/phaserScene.ts) добавлено поле `currentUnderlay`, сохраняемое из `mapVisual.underlay` в `updateFromState`.
3. Transform применён единообразно в `drawSpaces`, `drawConnections`, `drawPieces`, `drawMapVisualDebug`.
4. Hit-test (`cachedSpaces`, `cachedPieceBoxes`) теперь в world-координатах — корректно, т.к. pointer input тоже в world.
5. [P1 correction] Map bounds AABB исправлен с 2-углового (`strokeRect(tl.x, tl.y, br.x - tl.x, br.y - tl.y)`) на 4-угловой (min/max по всем transformed corners), идентично underlay bounds. Для rotated карт 2-угловой подход давал неверные размеры.

Дополнительно в рамках этого же цикла:
- V2 external review (GPT-5.5 Thinking) нашёл неявный debug depth (0/1) — исправлен на `DEBUG_DEPTH = -20`.
- Ложное V2 срабатывание: `useState(null)` без generic — не подтвердилось, generic уже был в коде.
- Path truncation в `write_to_file` при создании V2 артефактов — обойдено через `edit_file`.
- Потеря working tree после V2 push/review-branch — восстановлено cherry-pick.

Verification:
- `npm run typecheck` — passes
- `npm run build` — passes
- Browser check: не проводился, делегирован человеку

Human check:
suggested — `table-sandbox/Запуск.bat` → Editor → Preview → точки/связи должны совпадать с map/underlay bounds. Сброс/загрузка чистят debug-слой.

Related files:
- [`table-sandbox/src/map/MapRenderModel.ts`](table-sandbox/src/map/MapRenderModel.ts)
- [`table-sandbox/src/renderer/phaserScene.ts`](table-sandbox/src/renderer/phaserScene.ts)
- [`table-sandbox/src/editor/MapDraft.ts`](table-sandbox/src/editor/MapDraft.ts) (read-only reference)
- [`.ai/reports/0029_map_plane_alignment_play_preview_0_1_report.md`](.ai/reports/0029_map_plane_alignment_play_preview_0_1_report.md)

### BUG-20260526-002 — Editor map-plane / large image geometry drift

Status: open

Area:
editor branch, `0020`, underlay, map-plane geometry

Symptoms:
При загрузке большой custom map image карта может вести себя не как реальная рабочая плоскость редактора: раньше были drift image vs points, странное движение при scale/move, ощущение что весь editor world всё ещё равен tiny fixture sheet.

Cause:
Проблема оказалась не в одной подложке, а в editor geometry model:
- fixed tiny plane долго оставался implicit source of truth;
- underlay, grid, pointer conversion и map-local coordinates расходились по смыслу;
- large image edge cases начали проявляться сильнее tiny-fixture сценария.

Current state:
В `0020` и correction-pass большая часть модели уже переделана:
- active draft size снова идёт из реального `coordinateSystem`, а не из forced `6000x4000`;
- build/typecheck проходят;
- но текущий checkpoint всё ещё допускает, что на живой большой карте могут остаться browser-level edge cases.

Fix direction:
Следующий узкий шаг должен проверять и добивать только large custom image / map-plane ergonomics поверх текущего checkpoint, без wholesale editor redesign.

Verification:
- `npm run typecheck`
- `npm run build`
- Codex code review of [`MapDraft.ts`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/MapDraft.ts) and [`EditorSurface.tsx`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/EditorSurface.tsx)

Human check:
suggested — на живой большой custom карте проверить move / scale / rotate / space placement / preview.

Related files:
- [`table-sandbox/src/editor/MapDraft.ts`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/MapDraft.ts)
- [`table-sandbox/src/editor/EditorSurface.tsx`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/EditorSurface.tsx)
- [`table-sandbox/src/editor/Editor.css`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/Editor.css)

### BUG-20260524-001 — Phaser canvas исчезает при StrictMode double-mount

Status: fixed

Area:
table-sandbox, Phaser, React StrictMode

Symptoms:
Зелёный Phaser-холст не отображается. В консоли видно `Phaser v3.90.0 (WebGL | Web Audio)`, но `canvasCount: 0`. Пользователь видит страницу без поля для кликов.

Cause:
React 18 StrictMode (в [`main.tsx`](table-sandbox/src/main.tsx)) делает double-mount. [`PhaserStage.tsx`](table-sandbox/src/renderer/PhaserStage.tsx) в `useEffect` создавал `new Phaser.Game(config)`. StrictMode: mount → эффект → cleanup (`game.destroy(true)`) → mount → эффект. `game.destroy(true)` удаляет canvas **асинхронно**. Второй mount проверял `container.querySelector("canvas")` — видел ещё не удалённый canvas от первой игры → скипал создание. Потом destroy заканчивал удаление → холст исчезал.

Fix:
Заменить хрупкий DOM-based guard на синхронную очистку: перед созданием игры всегда удалять предыдущий `gameRef.current`, затем синхронно удалять любой оставшийся canvas через `leftoverCanvas.remove()`. Файл: [`PhaserStage.tsx`](table-sandbox/src/renderer/PhaserStage.tsx:23-31).

Verification:
- Playwright: `canvasCount: 1`, `canvasWidth: 800`, `canvasHeight: 500`
- `npx tsc --noEmit` — 0 ошибок
- `npx vite build` — 40 modules, built 8.26s

Human check:
suggested — открыть страницу, убедиться что зелёное поле с сеткой видно, кликнуть и проверить координаты в DebugPanel.

Related files:
- [`table-sandbox/src/renderer/PhaserStage.tsx`](table-sandbox/src/renderer/PhaserStage.tsx)
- [`table-sandbox/src/main.tsx`](table-sandbox/src/main.tsx) (StrictMode — не менялся, но влияет)

Notes for future agents:
При работе с Phaser + React 18 StrictMode нельзя полагаться на DOM-проверки (`querySelector`) для защиты от double-mount. `game.destroy(true)` асинхронный — canvas может оставаться в DOM после вызова. Нужно синхронно удалять canvas до создания нового экземпляра. Либо рассмотреть отказ от StrictMode для Phaser-компонентов.
