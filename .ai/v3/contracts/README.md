# V3 Contracts

Эта папка будет содержать формальные контракты V3 artifact-producing workflow.

## Текущий статус

Placeholder. Контракты ещё не созданы — это задача Phase 2 rollout.

## Ожидаемое содержимое (Phase 2)

- **Request contract** — как формулировать V3-запрос: обязательные поля, scope, allowed paths, forbidden paths.
- **Artifact package contract** — структура V3 ZIP-пакета: manifest.yaml, README_FOR_KILO.md, README_FOR_CODEX.md, checksums.sha256, files/.
- **Manifest contract** — поля manifest.yaml: v3_id, task_title, generated_by, write_policy, allowed_paths, forbidden_paths, files, acceptance_criteria, known_risks.
- **Journal contract** — формат journal entry: v3_id, timestamp, files_written, verification, human_review_status.
- **Codex review contract** — как Codex проверяет импортированные артефакты: журнал, реальные файлы, сверка с задачей, риски.
- **Revision contract** — как запросить доработку у внешнего чата: revision request, уточнение scope, повторный импорт.
- **Storage policy** — где хранить raw ZIP, staging, journal; что tracked, что local-only.
- **Scope policy** — уровни scope: docs_only, workflow_docs, schemas, scripts, product_code; acceptance gates для каждого.
- **Acceptance policy** — как человек принимает/отклоняет V3-результат: критерии, человеческий verdict, фиксация в journal.

См. также [`v3_artifact_producing_workflow_contract.md`](../../plans/master/v3_artifact_producing_workflow_contract.md) — проектный контракт V3 (draft 0.1).
