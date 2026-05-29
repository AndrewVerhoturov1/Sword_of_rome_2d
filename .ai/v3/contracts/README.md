# V3 Contracts

Эта папка содержит формальные контракты V3 artifact-producing workflow.

## Текущий статус

**Phase 2 завершён, Phase 6 lifecycle hardening:** все 9 контрактов созданы и обновлены. V3 описан как формальный процесс с post-import testing layer, lifecycle closure rules и accepted journal policy.

## Содержимое

| Файл | Назначение |
|------|------------|
| [`v3_request_contract.md`](v3_request_contract.md) | Контракт V3-запроса: обязательные поля, scope, allowed/forbidden paths, action model, post-import testing. Request ≠ готовый package. |
| [`v3_artifact_package_contract.md`](v3_artifact_package_contract.md) | Структура V3 ZIP-пакета: manifest.yaml, README_FOR_KILO.md, README_FOR_CODEX.md, checksums.sha256, files/. Включает `POST_IMPORT_TEST_PROMPT.md` как опциональный control file. |
| [`v3_manifest_contract.md`](v3_manifest_contract.md) | Поля manifest.yaml: v3_id, task_title, generated_by, action, scope, write_policy, post_import_testing, allowed_paths, forbidden_paths, files, acceptance_criteria, known_risks. |
| [`v3_journal_contract.md`](v3_journal_contract.md) | Формат journal entry: подробный import trace. Не заменяет `V3_navigation.md`, а дополняет его. |
| [`v3_codex_review_contract.md`](v3_codex_review_contract.md) | Как Codex проверяет импортированные артефакты: journal, реальные файлы, post-import testing status, сверка с request/scope, риски. |
| [`v3_revision_contract.md`](v3_revision_contract.md) | Как запрашивается доработка у внешнего чата: revision request, что повторно используется, traceability, лимиты. |
| [`v3_storage_policy.md`](v3_storage_policy.md) | Хранение V3 артефактов: persistent (tracked) vs local-only, raw input sources, lifecycle archive, cleanup после accept/reject. |
| [`v3_scope_policy.md`](v3_scope_policy.md) | Уровни scope: docs_only, workflow_docs, schemas, scripts, product_code. Acceptance gates для каждого. MVP-ограничения. |
| [`v3_acceptance_policy.md`](v3_acceptance_policy.md) | Как человек принимает/отклоняет V3-результат: minimal gates (включая post-import testing gate и waiver path), verdict types (accept/revision/reject), фиксация в journal. |

## Что будет дальше

Phase 6 завершил lifecycle hardening. Phase 7 завершён: `scripts/v3/` helper layer существует, `/v3` shortcut активирован как explicit V3 import-entry mode, канонический шаблон [`.ai/prompts/create_v3_shortcut_prompt.md`](../../prompts/create_v3_shortcut_prompt.md) создан. Далее:

- Возможное расширение helper layer (будущие фазы).
- `apply_v3_package.py` остаётся не созданным.

## Связанные документы

- [`v3_artifact_producing_workflow_contract.md`](../../plans/master/v3_artifact_producing_workflow_contract.md) — проектный контракт V3 (draft 0.1).
- [`v3_workflow_implementation_plan.md`](../../plans/master/v3_workflow_implementation_plan.md) — поэтапный план внедрения V3.
