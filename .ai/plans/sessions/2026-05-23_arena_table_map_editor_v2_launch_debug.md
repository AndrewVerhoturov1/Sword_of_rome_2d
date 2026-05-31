# Session: arena_table_map_editor_v2_launch_debug

## Session ID

`2026-05-23_arena_table_map_editor_v2_launch_debug`

## Status

planned

## Goal

Выяснить, почему prototype `table-map-editor-v2 gpt` не запускается из локальной Arena prototypes launcher, и подготовить узкий безопасный fix без широкого refactor.

## Approved Plan

### P1: Reproduce And Fix Arena Launch Failure

- Status: planned.
- Воспроизвести запуск prototype `table-map-editor-v2-gpt` через Arena launcher.
- Отделить проблему конкретного prototype от общих проблем launcher runtime.
- Найти root cause по evidence: install/start command, порт, ready/open URL, runtime logs или ошибка внутри prototype.
- Если fix локальный и безопасный, внести минимальную правку только в launcher, registry entry и/или сам prototype.
- Если честный fix требует более широкого scope, вернуть `Blocked` или `Needs scope decision` с доказательствами.

## Active Plan Item

`P1: Reproduce And Fix Arena Launch Failure`

## Runs

- `Session run: 001` - pending.

## User Overrides

- Пользователь явно попросил создать Kilo-задачу, а не делать substantive debug напрямую в Codex.
- Фокус только на проблеме запуска prototype `table-map-editor-v2 gpt` в Arena.
- Local-only слои `arena-prototype-launcher/` и `_local/prototypes/` допустимы для этой задачи.
- Широкий refactor launcher без доказанной необходимости запрещён.

## Checkpoint State

- Prototype зарегистрирован в launcher registry как `table-map-editor-v2-gpt`.
- Registry entry сейчас указывает:
  - path: `D:\Codex+Kilocode\projects\sword-of-rome-web\_local\prototypes\arena-tests\table-map-editor-v2 gpt`
  - port: `5181`
  - startCommand: `npx vite --port {port}`
  - openUrl: `http://localhost:5181`
- В папке prototype сейчас нет `node_modules`, значит launcher path сначала должен пройти через `installCommand`.
- В server route `POST /api/projects/:id/start` install и start выполняются автоматически, если `node_modules` отсутствует.
- В `processManager.ts` есть fallback, который через `2000 ms` может перевести проект в `running` и открыть `readyUrl` даже если точная готовность не подтверждена логами.
- В общих launcher logs есть следы отдельных runtime-проблем launcher; это контекст, но не доказательство причины именно для `table-map-editor-v2-gpt`.
