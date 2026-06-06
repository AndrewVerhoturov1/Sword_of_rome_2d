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

### P5: Add Codex Token Monitor Audit as the next verification layer

- Status: completed.
- Реализовать отдельный audit layer поверх current hybrid monitor без нового OTel и без source-split churn.
- Разделить `Audit` и `Honesty hardening`: сначала technical truth checks и audit artifacts, потом отдельный human-facing wording slice.

## Active Plan Item

`none - waiting for the next approved slice`

## Runs

| Session run | Summary |
|---|---|
| 001 | Prepared planning artifact and Kilo handoff for `Codex Token Monitor v2` hybrid live/archive implementation. |
| 002 | Direct Codex hardening turned the hybrid monitor into a working live/archive baseline; remaining open slice is `cache semantics + rich export`. |
| 003 | External forensic audit and documentation pass confirmed hybrid baseline, explained `cached_tokens` as mixed-case live semantics, and narrowed next slice to semantic honesty plus rich export wording. |
| 004 | External planning answer `V1-20260607-014953` defined `Codex Token Monitor Audit` as the next execution slice; docs and next Kilo handoff retargeted from generic hardening to a separate verification layer. |
| 005 | Reviewed Kilo run 0048 and accepted only audit UI/API baseline. Main truth-risk stayed open because audit could self-certify monitor detail without enough upstream evidence. Prepared narrow correction handoff focused on truth gap and regression tests. |
| 006 | Reviewed corrected Kilo run 0049, accepted the audit truth-fix, and recorded the accepted baseline: fake verified evidence without explicit note is blocked; evidence/scope metadata survives API and export; next slice is Honesty hardening. |

## User Overrides

- Реальные чаты Codex должны стать основным источником данных.
- Архив тестов OTel должен остаться доступным, но как отдельный source mode.
- Prompt/answer скрывать по умолчанию.
- Не запускать новый OTel.
- Не менять live Codex config.
- Не писать в `C:/Users/andre/.codex/**`.
- Не переделывать source split.
- Для follow-up по `cached_tokens` и export сначала реализовать `Audit` как technical truth layer, а уже потом делать отдельный human-facing `Honesty hardening`.

## Checkpoint State

- `Codex Token Monitor Server v1` принят как archive viewer baseline.
- Принято решение [D-20260605-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-004): следующая версия должна разделять реальные чаты и архивные run artifacts.
- Принято решение [D-20260607-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-001): live cache spikes сначала трактовать как semantics/confidence risk, а не как доказанный math bug.
- Принято решение [D-20260607-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-002): следующий execution slice = `Codex Token Monitor Audit` как отдельный verification layer.
- Принято решение [D-20260607-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-003): audit не может сам себя сертифицировать без upstream evidence.
- Принято решение [D-20260607-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-004): audit truth-fix accepted, verified evidence now requires explicit note and evidence/scope metadata must survive export.
- Следующий ожидаемый шаг: отдельный slice `Honesty hardening`, при нужде позже добавить ordinary UI/API wiring для `evidence_note`.
## Review checkpoint - 2026-06-06

- Hybrid monitor now exists as the current working baseline for local live/archive inspection.
- The source split itself is no longer the main open problem.
- The next focused follow-up is narrower:
  - verify live `cached_tokens` semantics on short chats;
  - redesign monitor copy/export actions to emit full useful step/session detail.

## Review checkpoint - 2026-06-07

- External notebook audit `V1-20260607-live-monitor-audit-r2` read the published forensic pack and leaned toward real live telemetry semantics, not a simple mapping bug.
- Accepted interpretation update:
  - first visible live step is not equal to cold-start provider request;
  - high `cached_tokens` may include hidden `system / developer / plugin / runtime` context;
  - current risk is semantic overconfidence in UI/export wording.
- This slice is now explicitly tracked as:
  - `cache semantics + rich export`
  - with doc + wording hardening before any further behavioral changes.

## Review checkpoint - 2026-06-07 audit planning follow-up

- External notebook plan `V1-20260607-014953` is accepted as planning baseline for the next run.
- Scope is now split more strictly:
  - current run: implement `Codex Token Monitor Audit`;
  - later run: `Honesty hardening`.
- Kilo handoff should target audit module, audit statuses, audit JSON/MD artifacts, minimal API/UI integration and tests.

## Review checkpoint - 2026-06-07 audit run review

- Kilo run `0048_codex_token_monitor_audit` materially advanced project:
  - audit module exists;
  - audit endpoint exists;
  - audit panel exists;
  - audit tests exist.
- But main technical risk is still open:
  - audit can currently mark `ok / all_confirmed / high / per_step_estimated` by re-reading monitor-produced `session detail` without enough upstream evidence.
- Accepted outcome:
  - partial acceptance only;
  - keep audit feature baseline;
  - next run must focus on truth-gap correction and regression tests before any honesty-hardening slice.

## Review checkpoint - 2026-06-07 audit truth-fix acceptance

- Kilo correction run `0049_codex_token_monitor_audit_truth_fix` is accepted.
- Main outcome:
  - audit no longer reaches `verified_against_source_evidence` from a boolean-only upstream flag;
  - forensic live fixture now downgrades correctly when explicit evidence note is missing;
  - audit artifacts and API preserve `evidence_note` and exact selected-step scope.
- Residual gap:
  - ordinary monitor UI/API flow still does not provide `evidence_note`;
  - this is accepted as non-blocking because it limits verified-flow reachability, not truth-safety.
- Next expected slice:
  - `Honesty hardening` as a separate follow-up over the now-accepted audit truth layer.
