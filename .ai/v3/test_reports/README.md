# test_reports/ — Machine-Check Reports

## Что лежит в этой папке

Здесь хранятся **machine-check reports** — отчёты о результатах post-import testing, выполненных обычным Kilo code run.

Имя файла: `<V3-ID>_machine_check_report.md`.

## Кто это создаёт

**Обычный Kilo code run** после выполнения machine checks из `POST_IMPORT_TEST_PROMPT.md`. Prompt берётся из [`../test_prompts/<V3-ID>_post_import_test_prompt.md`](../test_prompts/).

## Local-only или tracked

**Local-only.** Machine-check report — это локальный workflow artifact. Он не tracked в git и не повышается в journal.

## Кто это читает дальше

- **Codex** читает этот файл как **главный источник** machine-check результатов при review (если `manifest.post_import_testing.mode = required`).
- **Человек** может ознакомиться с результатами machine checks.

## Чем это НЕ является

- **Не journal.** Это отчёт о тестировании, а не запись импорта. Machine-check report не заменяет journal и не повышается в journal.
- **Не lifecycle registry.** Здесь нет статусов циклов.
- **Не external artifact.** Это локальный отчёт, созданный внутри repo.
- **Не replacement for human verdict.** Machine-check report — это один из шагов перед human verdict, а не замена ему.
- **Не tracked accepted result.** Даже после human accept machine-check report остаётся local-only.

## Когда machine-check report обязателен

Machine-check report обязателен только если `manifest.post_import_testing.mode = required`. В этом случае:

- Отсутствие machine-check report блокирует Codex verdict `accept`.
- Codex может дать только `revision_needed` или `accept_with_notes` (при testing waiver).

Если `mode = optional` или `waived`, machine-check report не обязателен.

## Связанные документы

- [`../test_prompts/README.md`](../test_prompts/README.md) — tester prompt copies.
- [`../contracts/v3_storage_policy.md`](../contracts/v3_storage_policy.md) — что tracked, что local-only.
- [`../contracts/v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md) — как Codex использует machine-check report.
- [`../contracts/v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md) — testing gate в acceptance flow.
