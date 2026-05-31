# Session: b1_bos_legacy_inventory

## Session ID

`2026-05-31_b1_bos_legacy_inventory`

## Status

in_progress

## Goal

Подготовить и провести через Kilo read-only инвентаризацию всей старой `B1/BOS/block-orchestration` системы по репозиторию, чтобы получить один документ со списком:

- прямых файлов старой системы;
- файлов с упоминаниями старой системы;
- краткой классификацией;
- локальными путями;
- GitHub-ссылками.

## Approved Plan

### P1: B1/BOS Legacy Inventory

- Status: ready.
- Просканировать весь repo на предмет старой `B1/BOS/block-orchestration` системы.
- Разделить результаты на:
  - direct system files;
  - mention-only files.
- Не менять repo files, не удалять, не переносить.
- Разрешён только один новый report-document.
- Для каждого найденного файла зафиксировать:
  - что это;
  - почему относится к старой системе;
  - local path;
  - GitHub link.
- Явно отфильтровать ложные срабатывания по словам `B1`, `Boss`, `block`.

## Active Plan Item

`P1: B1/BOS Legacy Inventory`

## Runs

- `Session run: 001` - prepare Kilo inventory handoff for repo-wide read-only scan.

## User Overrides

- Ничего не изменять.
- Ничего не удалять.
- Ничего не переносить.
- Нужен только отчёт-инвентаризация.
- Сканировать по всему репозиторию.
- Результат должен различать:
  - файлы самой старой системы;
  - файлы, где есть только упоминание.
- В отчёте нужны ссылки на GitHub.

## Checkpoint State

- Старый `B1/BOS` rollout закрыт пользователем и уже опубликован в `main`.
- Closure artifacts старой системы теперь tracked и доступны для GitHub-ссылок.
- Новый Kilo run должен быть read-only except report.
