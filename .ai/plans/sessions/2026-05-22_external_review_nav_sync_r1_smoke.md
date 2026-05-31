# Session: external_review_nav_sync_r1_smoke

## Session ID

`2026-05-22_external_review_nav_sync_r1_smoke`

## Status

active

## Goal

Узко подготовить три следующих шага без широких изменений repo:

1. один prompt-only внешний обзорный вопрос по GitHub repo;
2. один маленький Kilo handoff для проверки и минимального обновления `.ai/repo_navigation.md`;
3. один `/r1` readiness audit с явным verdict и blocker list.

## Approved Plan

### P1: External Overview Prompt

- Status: completed.
- Подготовить один внешний prompt c профилем `понимание проекта + дыры`.
- Не превращать prompt в `/r1`: без published task bundle, recorder payload и handoff bundle.
- Дать внешнему чату GitHub repo URL и ссылки на ключевые public docs.

### P2: Kilo Repo Navigation Sync

- Status: completed.
- Подготовить один маленький Kilo handoff только для `.ai/repo_navigation.md`.
- Разрешить только минимальный patch по подтвержденным расхождениям.
- Не расширять scope на `.ai/project_state.md` без отдельного решения после review.

### P3: `/r1` Readiness Audit

- Status: completed.
- Проверить readiness published-artifact route без full external run.
- Явно зафиксировать blockers, warnings и minimum change set.

### P4: `/r1` Smoke Launch Package

- Status: completed.
- Подготовить один production-like external launch package под smoke-вопрос о достаточности published public context.
- Создать один published task bundle без лишних side-files.
- Подготовить recorder-ready response contract, но не создавать recorder package заранее.

## Active Plan Item

`none`

## Runs

- `Session run: 001` - accepted after review. Kilo обновил только `.ai/repo_navigation.md`, stale GitHub-publication wording исправлен, scope не расширен.
- `External run prep: EXT-0001` - completed. Published task bundle создан, external launch package прошёл validator.

## User Overrides

- Пользователь явно попросил двигаться узко, по факту и по одному шагу.
- Лишние handoff-файлы заранее не создавать.
- Маленькая Kilo-задача должна трогать только `.ai/repo_navigation.md`, если не обнаружится отдельная необходимость расширить scope после review.
- Для обзорного внешнего теста нужен профиль `понимание проекта + дыры`, а не полноценный `/r1`.
- После принятия Kilo review пользователь выбрал следующий шаг: подготовить конкретный `/r1` launch package.

## Checkpoint State

- `P1` оформлен как prompt-only artifact и не требует checkpoint.
- `P2` принят после review; checkpoint пока не выполнен.
- `P3` зафиксирован как локальный audit report; базовый `/r1` blocker снят.
- `P4` завершён: один task bundle опубликован, один external launch package готов к ручной отправке.
