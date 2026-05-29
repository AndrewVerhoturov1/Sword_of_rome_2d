# scripts/v3 — V3 Scripted Support

Helper-слой для V3 artifact-producing workflow. Создан в Phase 7 (Scripted Support Foundation).

## Статус

Phase 7 foundation запущен. `/v3` shortcut не активирован. `apply_v3_package.py` не создан. Manual flow остаётся primary.

## Скрипты

| Скрипт | Назначение | Пишет в project paths? |
|--------|------------|------------------------|
| [`validate_v3_package.py`](validate_v3_package.py) | Валидация структуры, manifest, checksums и путей V3 ZIP-пакета | Нет (read-only) |
| [`stage_v3_package.py`](stage_v3_package.py) | Validate + extract в `.ai/v3/staging/<V3-ID>/` + staging report | Только в staging |
| [`write_v3_journal.py`](write_v3_journal.py) | Создание draft journal в `.ai/v3/journals/drafts/` | Только draft journal |

## Safety boundaries

- Все три скрипта — helpers, не automation.
- Не заменяют Codex review и human verdict.
- `write_v3_journal.py` не трогает `V3_navigation.md`.
- `stage_v3_package.py` не пишет в project target paths.
- `validate_v3_package.py` ничего не меняет на диске.

## Требования

- Python 3.9+
- PyYAML (`pip install pyyaml`)

## Связанные документы

- [`.ai/v3/README.md`](../../.ai/v3/README.md) — V3 workflow layer.
- [`.ai/v3/contracts/v3_artifact_package_contract.md`](../../.ai/v3/contracts/v3_artifact_package_contract.md) — структура пакета.
- [`.ai/v3/contracts/v3_manifest_contract.md`](../../.ai/v3/contracts/v3_manifest_contract.md) — manifest contract.
- [`.ai/v3/contracts/v3_journal_contract.md`](../../.ai/v3/contracts/v3_journal_contract.md) — journal contract.
- [`.ai/v3/contracts/v3_storage_policy.md`](../../.ai/v3/contracts/v3_storage_policy.md) — storage policy.
- [`.ai/plans/master/v3_workflow_implementation_plan.md`](../../.ai/plans/master/v3_workflow_implementation_plan.md) — план внедрения.
