# Session: v2_local_workspace_preservation_hardening

## Session ID

`2026-05-30_v2_local_workspace_preservation_hardening`

## Status

in_progress

## Goal

Подготовить и провести через Kilo docs-only hardening V2, который закрепляет сохранность локального workspace при V2 snapshot и закрывает remaining contract gap после `BUG-20260527-004` и `BUG-20260528-005`.

## Approved Plan

### P1: V2 Local Workspace Preservation Hardening

- Status: ready.
- Обновить V2 operational contract без helper scripts, automation и product-code правок.
- Зафиксировать верхнеуровневый инвариант: `review/v2/...` — published snapshot copy, а не ownership transfer локального WIP.
- Добавить `Snapshot method` с preferred `separate-worktree` и fallback `same-worktree-with-restore`.
- Вставить обязательный checkpoint `local_workspace_verified` между `snapshot_pushed` и `prompt_ready`.
- Обновить `README.md`, `V2_navigation.md`, `v2_request_template.md`, `v2_safety_checklist.md`, `AGENTS.md`, `kilo_mode_contract.md`.
- Backfill старых строк `V2_navigation.md` только legacy-маркерами `unknown_legacy` / `legacy-not-recorded`, без догадок задним числом.
- Проверить handoff/docs consistency командами из плана и зафиксировать truthful report.

## Active Plan Item

`P1: V2 Local Workspace Preservation Hardening`

## Runs

- `Session run: 001` - prepared handoff `0042_v2_local_workspace_preservation_hardening.md` for the docs-only Kilo implementation run.

## User Overrides

- Основные docs/templates/rules для V2 остаются на русском.
- Технические identifiers, status values, enum values, branch names, file names и machine-readable fields остаются на английском.
- Scope только docs/contracts hardening.
- Helper script, automation, product-code changes и broad redesign вне scope.
- Historical master plan `.ai/plans/master/v2_external_senior_review_system.md` не менять, если live-contract не требует явного anti-conflict sync.
- Новый `/v1` для этой правки не нужен.

## Checkpoint State

- В repo уже зафиксированы два related fixes:
  - `BUG-20260527-004` — stash with `--include-untracked` для V2 snapshot.
  - `BUG-20260528-005` — обязательный `restore-to-working-branch` step после V2 implementation.
- Current remaining gap: V2 ещё не требует явной проверки, что локальный workspace сохранён или подтверждён после snapshot push и до выдачи prompt.
- Operational source of truth для V2 сейчас: `.ai/external_reviews/README.md` и `.ai/external_reviews/V2_navigation.md`.
