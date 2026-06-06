# Session: codex_token_monitor_v2_live_threads

## Session ID

`2026-06-05_codex_token_monitor_v2_live_threads`

## Status

active follow-up

## Goal

Подготовить и выполнить один Kilo handoff на реализацию `Codex Token Monitor v2` как гибридного monitor layer: реальные локальные чаты Codex плюс архивные OTel/test runs, без новых OTel-экспериментов и без записи в Codex state.

## Approved Plan

### P1: Add a source-aware hybrid monitor

- Status: planned.
- Добавить явное разделение источников: `Реальные чаты Codex` и `Архив тестов OTel`.
- Исправить misleading смысл `projectSelect` и session titles.

### P2: Materialize the live Codex chat adapter

- Status: planned.
- Читать `C:/Users/andre/.codex/state_5.sqlite`, `session_index.jsonl` и `sessions/**/rollout-*.jsonl` только read-only.
- Показывать реальные chat titles, model, reasoning, cwd и prompt/answer, если они доступны и надежно сопоставлены.

### P3: Preserve archive forensics without pretending it is a live chat list

- Status: planned.
- Сохранить archive source поверх `_local/codex-token-debugger/**`.
- Предпочитать `selected_turn` для confirmation-runs и явно помечать `mixed/noisy`.

### P4: Verify and document

- Status: planned.
- Обновить tests и docs.
- Прогнать unit tests и `git diff --check`.

## Active Plan Item

`P1: Add a source-aware hybrid monitor`

## Runs

| Session run | Summary |
|---|---|
| 001 | Prepared planning artifact and Kilo handoff for `Codex Token Monitor v2` hybrid live/archive implementation. |
| 002 | Direct Codex hardening turned the hybrid monitor into a working live/archive baseline; remaining open slice is `cache semantics + rich export`. |

## User Overrides

- Реальные чаты Codex должны стать основным источником данных.
- Архив тестов OTel должен остаться доступным, но как отдельный source mode.
- Prompt/answer скрывать по умолчанию.
- Не запускать новый OTel.
- Не менять live Codex config.
- Не писать в `C:/Users/andre/.codex/**`.

## Checkpoint State

- `Codex Token Monitor Server v1` принят как archive viewer baseline.
- Принято решение [D-20260605-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-004): следующая версия должна разделять реальные чаты и архивные run artifacts.
- Следующий ожидаемый шаг: один Kilo implementation run по handoff `0047_codex_token_monitor_v2_live_threads.md`.
## Review checkpoint - 2026-06-06

- Hybrid monitor now exists as the current working baseline for local live/archive inspection.
- The source split itself is no longer the main open problem.
- The next focused follow-up is narrower:
  - verify live `cached_tokens` semantics on short chats;
  - redesign monitor copy/export actions to emit full useful step/session detail.
