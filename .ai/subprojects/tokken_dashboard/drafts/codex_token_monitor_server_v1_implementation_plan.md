# Codex Token Monitor Server v1 Implementation Plan

Date: `2026-06-05`
Status: `draft artifact`
Scope: `plan only, no implementation`

## Summary

Сделать локальную MVP-утилиту `Codex Token Monitor` как repo-tracked слой поверх уже существующих `_local/codex-token-debugger/*` артефактов и живого `Token Cost Normalizer v1`.

Опорный UI брать строго из [codex_token_monitor_compact_archive_prototype.html](C:/Users/andre/Downloads/codex_token_monitor_compact_archive_prototype.html): тот же layout, compact dark style, resizable split, collapsible left block, archived sessions, step cards, hidden prompt/answer by default, UI shutdown button.

Ключевое архитектурное решение: в MVP список “сессий” монитора строить по run-папкам в `_local/codex-token-debugger`, а не по `thread_id` из текущего normalizer. Это лучше совпадает с уже существующей структурой данных и avoids ложные mixed-thread aggregates, которые сейчас видны в normalized outputs.

## Key Changes

### 1. Backend server

Создать `scripts/codex_token_monitor_server.py` на чистом Python stdlib:
- `ThreadingHTTPServer` + кастомный handler.
- Отдача static UI из `static/codex-token-monitor/`.
- JSON API:
  - `GET /`
  - `GET /api/status`
  - `GET /api/projects`
  - `GET /api/sessions?project_id=...`
  - `GET /api/session?project_id=...&session_id=...`
  - `POST /api/refresh`
  - `POST /api/archive`
  - `POST /api/unarchive`
  - `POST /api/shutdown`
- `--host`, `--port`, `--open-browser` CLI flags.
- Shutdown делать через delayed `server.shutdown()` после успешного JSON response.
- Collector management оставить best-effort: status поле есть, но реальный stop/start collector в MVP не обязателен.

### 2. Discovery and cache layer

Серверу нужен внутренний read-only adapter над текущими artifacts:
- `config/codex_token_monitor_projects.json` как источник проектов.
- Discovery runs в `project.path / project.runs_dir`.
- Run считается валидным monitor-session, если есть:
  - `token-cost-normalized/token_cost_dashboard_data.json`, или
  - `parsed/token_usage.jsonl`.
- Если normalized data отсутствует или устарела относительно `parsed/*`, `POST /api/refresh` запускает существующий `scripts/codex_token_cost_normalizer.py` как subprocess.
- Использовать mtime-based cache по run-dir, чтобы auto-refresh не пересчитывал все постоянно.
- Archive state хранить в `_local/codex-token-monitor/archive_state.json`.

### 3. Data model adapter

Не ломать current normalizer formulas. Вместо этого в monitor server сделать mapping из run-level artifacts в UI session model:
- `session_id` = имя run-папки.
- `title` = best-effort human title:
  - сначала из известных summary/report hints, если есть;
  - иначе из имени run-папки.
- `date` = best-effort:
  - сначала earliest/latest turn timestamp;
  - иначе mtime run-dir.
- `model` = single model или `mixed`.
- `reasoning` = single effort или `mixed`.
- `workdir` = из turn/environment fields, если есть; иначе project path.
- `summary` брать из `token_cost_dashboard_data.json`.
- `steps` строить из `turns[]` normalized payload.

Prompt/answer handling:
- server и UI всегда возвращают структуру `user_prompt` / `assistant_answer`;
- если текст есть в local normalized/parsed sources, показывать его;
- если текста нет, честно возвращать `available=false`, `text=""`;
- ничего не выдумывать и не парсить “по аналогии”.

### 4. Static UI materialization

Разбить прототип на:
- `static/codex-token-monitor/index.html`
- `static/codex-token-monitor/styles.css`
- `static/codex-token-monitor/app.js`

UI сохранить максимально близким к прототипу:
- left panel with project select, path button, collector/prompt logging/auto refresh/last update, search, filters, session list, archive toggle.
- right panel with session title/meta, actions, summary cards, selected totals, steps list.
- step cards with:
  - checkbox
  - copy
  - compact metrics
  - prompt preview
  - answer preview
  - expand-on-card-click
- detail sections with collapsed prompt/answer blocks, tokens, cost, environment.
- localStorage only for:
  - left panel width
  - collapsed setup block
  - show archived flag

UI should call API only; demo data from prototype must be removed.

### 5. Startup and config

Добавить:
- `start_codex_token_monitor.bat`
- `config/codex_token_monitor_projects.json`

`start_codex_token_monitor.bat`:
- `cd /d %~dp0`
- проверяет наличие server script
- запускает `python scripts\codex_token_monitor_server.py --host 127.0.0.1 --port 8765 --open-browser`
- оставляет окно открытым для ошибок

Status logic:
- `prompt_logging` читать best-effort из local Codex config, если это безопасно и просто;
- если reliable read не готов, для MVP можно показывать expected state `true` с warning only when needed;
- `collector` status в MVP: `unknown` или `running/stopped` best-effort, без hard dependency на реальный OTel collector process manager.

### 6. Docs and decisions

Обновить:
- [tokken_dashboard_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md)
- [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md)
- [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md)
- [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md)

Нужно зафиксировать:
- `Codex Token Monitor UI v1` adopts the accepted compact prototype as UX source of truth.
- Monitor MVP is a local utility over normalized local artifacts, not a new OTel experiment.
- Prompt/answer are schema-first and best-effort; absence is explicit, not hidden.

## Public Interfaces

### New config

`config/codex_token_monitor_projects.json`
- `version`
- `default_project_id`
- `projects[] { id, name, path, runs_dir }`

### New archive file

`_local/codex-token-monitor/archive_state.json`
- `version`
- `archived_sessions: { [project_id]: string[] }`

### API response shape

`GET /api/session` should return:
- run-level session metadata
- `summary`
- `steps[]`
- each step has:
  - `step_index`
  - `model`
  - `reasoning_effort`
  - `user_prompt`
  - `assistant_answer`
  - `usage`
  - `environment`
  - `warnings`

This API is the stable contract for the frontend. The UI should not read `_local` files directly.

## Test Plan

Добавить `tests/test_codex_token_monitor_server.py` и покрыть:
- project config loads
- invalid project path yields warning, not crash
- discovery prefers existing `token_cost_dashboard_data.json`
- missing normalized output falls back without crash
- refresh calls normalizer in stubbed mode
- archive/unarchive persists `_local/codex-token-monitor/archive_state.json`
- session listing hides archived items by default
- status payload returns collector/prompt_logging/last_update/server_pid
- absent prompt/answer yields `available=false`
- shutdown endpoint returns response and schedules stop

После этого гонять:
- `python -m unittest tests.test_codex_token_monitor_server tests.test_codex_token_cost_normalizer tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment`
- `git diff --check`

## Assumptions and Defaults

- Server implementation без новых Python dependencies; stdlib-only is the default.
- MVP uses run-folder as monitor session identity. Thread-level reconciliation is deferred.
- Existing normalizer remains source of truth for token/cost math; monitor adds an adapter, not a replacement.
- Prompt text and especially answer text may remain unavailable for part of current historical runs; UI must still render cleanly.
- Collector lifecycle stays best-effort in MVP. Full collector orchestration is later work.
- Prototype visuals should be preserved closely, but code should be split into maintainable repo files and connected to real API data.
