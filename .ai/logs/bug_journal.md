# Bug Journal

This journal records important, repeated, or non-obvious bugs and difficulties found during project work.

Use it so future agents can check whether a similar issue already happened and how it was solved.

Do not record every tiny typo. Record issues that may help future debugging.

## Entries

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
