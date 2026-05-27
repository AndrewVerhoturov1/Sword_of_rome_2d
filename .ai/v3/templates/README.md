# V3 Templates

Эта папка содержит шаблоны для V3 artifact-producing workflow.

## Текущий статус

**Phase 3 завершён (2026-05-27):** все 5 шаблонов созданы. Каждый шаблон содержит валидный скелет с placeholder-полями и комментариями по заполнению.

## Содержимое

| Файл | Назначение |
|------|------------|
| [`v3_request_template.md`](v3_request_template.md) | Шаблон V3 request: структурированная форма с placeholder-полями и комментариями для Codex/человека перед отправкой внешнему чату. |
| [`v3_manifest_template.yaml`](v3_manifest_template.yaml) | Шаблон `manifest.yaml`: валидный YAML-скелет с обязательными полями, комментариями и placeholder values для внешнего чата. |
| [`v3_journal_template.yaml`](v3_journal_template.yaml) | Шаблон journal entry: полный YAML-скелет с полями import_status, imported_files, skipped_files, verification_notes, human_review_status. |
| [`v3_codex_review_template.md`](v3_codex_review_template.md) | Шаблон review note для Codex: summary, checks, verdict, human-review guidance, open risks. С примером заполнения. |
| [`v3_revision_request_template.md`](v3_revision_request_template.md) | Шаблон revision request: структурированная форма с what_to_fix, what_to_reuse, scope_changes для повторного запроса к внешнему чату. |

Все шаблоны опираются на контракты из [`contracts/`](../contracts/README.md) (Phase 2) и связаны с промптами из [`prompts/`](../prompts/README.md) (Phase 3).

## Ключевые принципы

- Каждый шаблон — заполняемая форма, а не абстрактное описание.
- Placeholder-поля помечены `<...>` и снабжены комментариями.
- YAML-шаблоны — валидный YAML (можно распарсить).
- Markdown-шаблоны содержат примеры заполнения.
- Шаблоны не обещают готовый runtime/scripts (это Phase 7).

## Связанные документы

- [`../contracts/README.md`](../contracts/README.md) — контракты V3 (Phase 2).
- [`../prompts/README.md`](../prompts/README.md) — промпты V3 (Phase 3).
- [`../README.md`](../README.md) — главный вход в V3.
- [`../V3_navigation.md`](../V3_navigation.md) — навигация по V3.
