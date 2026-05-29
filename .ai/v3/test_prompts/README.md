# test_prompts/ — Tester Prompt Copies

## Что лежит в этой папке

Здесь хранятся **tester prompt copies** — локальные копии `POST_IMPORT_TEST_PROMPT.md`, сохранённые `Kilo Notebook V3` после успешного импорта V3 artifact package.

Имя файла: `<V3-ID>_post_import_test_prompt.md`.

## Кто это создаёт

`Kilo Notebook V3` автоматически сохраняет tester prompt после импорта, если:

- в пакете есть `POST_IMPORT_TEST_PROMPT.md`;
- `manifest.post_import_testing.mode != waived`.

## Local-only или tracked

**Local-only.** Tester prompt copy — это локальный workflow artifact. Он не tracked в git и не повышается в journal.

## Кто это читает дальше

- **Человек** копирует содержимое этого файла и передаёт его в обычный Kilo code run.
- **Обычный Kilo code run** использует prompt из этого файла для выполнения post-import testing.

## Чем это НЕ является

- **Не journal.** Это prompt для тестирования, а не запись импорта.
- **Не lifecycle registry.** Здесь нет статусов циклов.
- **Не external artifact.** Это локальная копия, созданная внутри repo.
- **Не replacement for human verdict.** Tester prompt и machine-check report — это шаги перед human verdict, а не замена ему.
- **Не tracked accepted result.** Даже после human accept tester prompt остаётся local-only.

## Связанные документы

- [`../test_reports/README.md`](../test_reports/README.md) — machine-check reports.
- [`../contracts/v3_storage_policy.md`](../contracts/v3_storage_policy.md) — что tracked, что local-only.
- [`../contracts/v3_artifact_package_contract.md`](../contracts/v3_artifact_package_contract.md) — контракт package, включая `POST_IMPORT_TEST_PROMPT.md`.
