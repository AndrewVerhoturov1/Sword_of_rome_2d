# Session: v2_external_review_docs_implementation

## Session ID

`2026-05-26_v2_external_review_docs_implementation`

## Status

in_progress

## Goal

Подготовить и провести первый Kilo docs run для внедрения project-local системы V2 External Senior Review: создать V2 docs/templates/navigation и минимально обновить repo-level workflow rules так, чтобы `/v2` стал discoverable и совместимым с текущим контрактом Kilo.

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

- Status: pending.
- После принятия docs patch подготовить low-risk manual pilot на `/v2 preview`.

## Active Plan Item

`P2: V2 Verification`

## Runs

- `Session run: 001` - prepared handoff `0021_v2_external_review_docs_foundation.md` for the first V2 docs implementation run.
- `Session run: 002` - prepared handoff `0022_v2_manual_ingest_correction.md` for the V2 ingest-boundary correction after Codex review.
- `Session run: 003` - prepared handoff `0023_v2_docs_verifier.md` for read-only verification of the current V2 docs set.

## User Overrides

- Основные V2 документы и шаблоны должны быть написаны по-русски.
- Технические identifiers, status values, branch names, file names и machine-readable fields остаются на английском.
- Новый Kilo mode создавать нельзя.
- Raw V2 runtime artifacts не должны трекаться в `main` по умолчанию.
- `/v2 preview` обязателен перед любым V2 push.
- Сейчас нужен один Kilo task на docs implementation, а не новый `/v1` и не прямое исполнение.
- Для первой версии V2 `kilo-recorder` не нужен: пользователь будет передавать raw external answer в Kilo вручную.
- `kilo-notebook` пока остаётся `/v1-only` и в V2 не расширяется.

## Checkpoint State

- Public master-plan updated in `.ai/plans/master/v2_external_senior_review_system.md`.
- P1 accepted by Codex after correction run `002`; checkpoint commit created for accepted workflow files only.
- Clarification about template-layer vs instantiated V2 artifacts added and pushed to `main`.
- В worktree уже есть unrelated V1 runtime artifacts:
  - `.ai/external_chats/V1_navigation.md`
  - `.ai/external_chats/notebook/2026-05-26_V1-20260526-103939_senior-review-of-the-proposed-v2-external-senior.md`
- Эти V1 runtime files не входят в scope handoff `0021`.
- Результат handoff `0021` принят только после correction run `0022`.
