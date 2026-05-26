# Session: v2_external_review_docs_implementation

## Session ID

`2026-05-26_v2_external_review_docs_implementation`

## Status

in_progress

## Goal

Подготовить, внедрить и проверить project-local систему V2 External Senior Review: сначала docs/rules foundation, затем verifier, затем manual pilot, а после первого реального pilot довести V2 до жёсткого operational contract.

## Approved Plan

### P1: V2 Docs Foundation

- Status: completed.
- Создать `.ai/external_reviews/README.md`.
- Создать `V2_navigation.md`.
- Создать V2 templates и safety checklist.
- Обновить минимально необходимые repo-level docs/rules для discoverability.
- Сохранить rule boundary: без нового Kilo mode, без helper script, без raw V2 artifacts в `main` по умолчанию.
- Correction scope after review:
  - убрать `kilo-recorder` из V2 first version;
  - не расширять `kilo-notebook` на V2;
  - зафиксировать только manual V2 ingest paths:
    - raw external answer pasted directly into ordinary Kilo run;
    - raw external answer saved in local V2 response file and passed to ordinary Kilo run;
  - убрать для V2 требования `Recorder Payload` и `/r1`-style recorder flow.

### P2: V2 Verification

- Status: ready.
- Подготовить отдельный verifier handoff после docs run.
- Проверить consistency документов и контрактов.

### P3: V2 Manual Pilot Prep

- Status: completed.
- Сначала внедрить policy layer для `YOLO Stop Gates`, `Blocked Report Contract` и `V2 Recommendation Gate`.
- Только после этого готовить следующий manual pilot на `/v2 preview`.
- Intentional impossible seed уже использован как диагностический сигнал, но не является достаточным policy implementation.

### P4: V2 Process Hardening After First Real Pilot

- Status: in_progress.
- По итогам real pilot `0026` довести V2 до жёсткого operational contract.
- Внедрить обязательную связку `push -> instantiated prompt -> waiting_external_answer`.
- Сделать явный contract для `/v2` как interrupt-команды внутри уже идущего Kilo task.
- Зафиксировать Codex-owned post-accept cleanup вместо Kilo-owned cleanup.
- Сделать `V2_navigation.md` обязательным lifecycle index.
- Уточнить минимальный набор runtime artifacts, YOLO push-gate stop-state и fallback на path/write issues.

## Active Plan Item

`P4: V2 Process Hardening After First Real Pilot`

## Runs

- `Session run: 001` - prepared handoff `0021_v2_external_review_docs_foundation.md` for the first V2 docs implementation run.
- `Session run: 002` - prepared handoff `0022_v2_manual_ingest_correction.md` for the V2 ingest-boundary correction after Codex review.
- `Session run: 003` - prepared handoff `0023_v2_docs_verifier.md` for read-only verification of the current V2 docs set.
- `Session run: 004` - prepared handoff `0024_v2_intentional_impossible_pilot_seed.md` for an intentional impossible task to test honest blocked handling before V2 escalation.
- `Session run: 005` - prepared handoff `0025_yolo_stop_gates_and_v2_escalation.md` to implement stop-gates, blocked report semantics, and V2 escalation rules.
- `Session run: 006` - prepared handoff `0026_underlay_alignment_v2_pilot.md` for a real WIP underlay-alignment pilot that should exercise the new stop-gates and V2 recommendation rules.
- `Session run: 007` - prepared handoff `0027_v2_process_hardening_after_first_real_pilot.md` to harden V2 lifecycle, interrupt semantics, Codex-owned cleanup, navigation updates and runtime artifact rules after the first successful real V2 run.

## User Overrides

- Основные V2 документы и шаблоны должны быть написаны по-русски.
- Технические identifiers, status values, branch names, file names и machine-readable fields остаются на английском.
- Новый Kilo mode создавать нельзя.
- Raw V2 runtime artifacts не должны трекаться в `main` по умолчанию.
- `/v2 preview` обязателен перед любым V2 push.
- Для первой версии V2 `kilo-recorder` не нужен: пользователь передаёт raw external answer в Kilo вручную.
- `kilo-notebook` остаётся `/v1-only` и на V2 не расширяется.
- После принятого V2-result cleanup делает Codex, а не Kilo.
- Если человек ничего отдельно не сказал, действует default cleanup policy: Codex удаляет temporary review branch и temporary V2 runtime artifacts.
- Если человек явно сказал сохранить ветку или artifacts, это фиксируется как `kept_by_decision` или `cleanup_pending`.

## Checkpoint State

- Public master-plan updated in `.ai/plans/master/v2_external_senior_review_system.md`.
- P1 accepted by Codex after correction run `002`; checkpoint commit created for accepted workflow files only.
- Clarification about template-layer vs instantiated V2 artifacts added and pushed to `main`.
- Verifier run `0023` accepted with one narrow follow-up fix in `kilo_mode_contract.md`; that follow-up is already closed.
- Impossible pilot seed `0024` validated honest blocked behavior but exposed missing policy layer for mandatory stop-gates and V2 escalation semantics.
- Real pilot `0026` proved V2 technical usefulness on live WIP, but exposed process gaps: `push -> prompt` break, weak `/v2` interrupt semantics, stale `V2_navigation.md`, unclear runtime artifact minimum set, unclear cleanup ownership, YOLO friction around push gate, and path/write fallback gap.
