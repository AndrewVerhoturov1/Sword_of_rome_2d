# Session: editor_play_visual_continuity_next_phase

## Latest Accepted Synthesis

- Accepted route from external answer `V1-20260527-003610`:
  - main current gap is not "editor too weak", but missing visual/render contract between editor and play/test;
  - editor already has meaningful authoring baseline: underlay, transform, grid/snap, undo/redo, spaces, connections, inspector, validation, preview;
  - play/test already has meaningful runtime baseline: `GameState`, Action/Event pipeline, piece drag, selection, create/delete piece, change control, reset, save/load snapshot;
  - current preview bridge is too narrow: `draftToGameState()` carries spaces/connections, but not authored map visual;
  - first priority is `Editor -> Play Visual Continuity Bridge 0.1`, not more editor breadth and not old underlay/rotate tail.

- Accepted boundary:
  - prototype `table-map-editor-canvas-local-fixed` stays reference/selective donor;
  - no wholesale prototype migration;
  - authoring draft and runtime `GameState` stay separate;
  - authored map visual should move through separate render/display contract.

## Session ID

`2026-05-27_editor_play_visual_continuity_next_phase`

## Status

in_progress

## Goal

Зафиксировать accepted route от текущего editor baseline к рабочей связке `editor -> play/test` и к дальнейшему prototype parity, затем через следующий `/v1` уточнить exact first implementation step без broad redesign.

## Approved Plan

### P1: Freeze Route And Boundaries

- Status: completed.
- Зафиксировать, что текущая тема `map-plane / rotate / underlay geometry` закрыта достаточно для движения дальше.
- Зафиксировать, что следующий приоритет = `editor -> play/test continuity`.
- Зафиксировать, что prototype используется как UX/reference donor, а не как product-code foundation.
- Зафиксировать, что underlay/map visual не надо делать частью authoritative runtime `GameState`.

### P2: Delivery Route For Next Phase

- Status: completed.
- Идти по следующему route:
  1. `Editor -> Play Visual Continuity Bridge 0.1`
  2. Phaser viewport / map-size support
  3. Runtime underlay rendering
  4. Test pieces for preview
  5. Runtime/editor validation bridge
  6. Editor UI Parity Pack 1
  7. Editor Connection Parity Pack
  8. Editor Map Surface Polish Pack
  9. Map save/export/import hardening
  10. Scenario Authoring 0.1
- Держать приоритет: continuity first, parity second, scenario later.

### P3: Refine Exact First Step

- Status: completed.
- Подготовить следующий `/v1` вопрос не про broad roadmap, а про exact first implementation step внутри `Editor -> Play Visual Continuity Bridge 0.1`.
- Попросить bounded decomposition:
  - какой минимальный contract ввести первым;
  - какие файлы должны стать первыми точками правки;
  - какой scope держать вне первого шага;
  - какие acceptance checks нужны до расширения в viewport/zoom/test pieces.

### P4: Execute First Continuity Slice

- Status: ready.
- Дать один узкий Kilo handoff на `MapRenderModel Contract Wire-Up 0.1`.
- Сохранить separation boundary:
  - authoring draft отдельно;
  - runtime `GameState` отдельно;
  - `MapRenderModel` как отдельный visual/render contract.
- Ограничить первый slice:
  - новый shared type;
  - derive from draft в `App.tsx`;
  - передача `mapVisual` в `PhaserStage` и `phaserScene`;
  - только debug/bounds render в Phaser.
- Не включать в этот run:
  - actual underlay image rendering;
  - zoom / pan / fit-to-map;
  - изменения `GameState`;
  - editor polish pack;
  - prototype parity breadth.

## Active Plan Item

`P4: Execute First Continuity Slice`

## Runs

- `Session run: 001` - accepted external route `V1-20260527-003610`: continuity gap recognized as main blocker; first candidate step = `Editor -> Play Visual Continuity Bridge 0.1`.
- `Session run: 002` - prepared public session artifact for the accepted route so the next external question can reference a stable published plan.
- `Session run: 003` - accepted exact first implementation cut from external answer `V1-20260527-010125`: chosen slice = `MapRenderModel Contract Wire-Up 0.1`.

## User Overrides

- Отдельно не возвращаться в старый `0020` tail как в главную тему.
- Не расползаться в новый большой editor pack до закрытия `editor -> play/test` continuity.
- Не делать wholesale prototype migration.
- Не смешивать authoring draft и runtime `GameState`.
- Следующий внешний вопрос должен уточнять первый practical implementation step, а не снова обсуждать весь проект целиком.

## Checkpoint State

- Accepted route source: `.ai/external_chats/notebook/2026-05-27_V1-20260527-003610_practical-route-to-dual-goal-editor-parity-with.md`
- Published plan artifact: `.ai/plans/implementation/editor_play_visual_continuity_route.md`
- Exact first-step source: `.ai/external_chats/notebook/2026-05-27_V1-20260527-010125_exact-first-implementation-cut-inside-accepted-editor-play.md`
