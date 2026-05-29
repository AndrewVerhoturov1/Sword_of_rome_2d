# V3 Prompts

Эта папка содержит промпты и operating references для V3 artifact-producing workflow.

## Текущий статус

**Phase 3 завершён (2026-05-27), Phase 5+ коррекция (post-import testing):** prompt layer создан и обновлён.

Позже уточнено:

- `create_v3_request_prompt.md` — это внешний request layer. Теперь включает инструкции по post-import testing.
- `kilo_notebook_v3_mode_prompt.md` — это не handoff prompt, а raw-input operating reference для `Kilo Notebook V3`. Теперь включает post-import test prompt display.
- review и revision prompts остаются отдельными.

## Содержимое

| Файл | Назначение |
|---|---|
| [`create_v3_request_prompt.md`](create_v3_request_prompt.md) | Промпт для Codex/человека: как подготовить V3-запрос к внешнему чату. Требует artifact package, а не текстовый совет. Включает post-import testing instructions. Опирается на [`v3_request_contract.md`](../contracts/v3_request_contract.md). |
| [`kilo_notebook_v3_mode_prompt.md`](kilo_notebook_v3_mode_prompt.md) | Raw-input operating reference для `Kilo Notebook V3`: как режим принимает archive link/path, проверяет package, создаёт journal, обновляет `V3_navigation.md` и показывает `POST_IMPORT_TEST_PROMPT.md` после импорта. |
| [`codex_v3_review_prompt.md`](codex_v3_review_prompt.md) | Промпт для Codex после V3 import: проверка journal и реальных файлов, сверка с request/scope, нормализованный verdict enum, human review gates. Опирается на [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md). |
| [`v3_revision_request_prompt.md`](v3_revision_request_prompt.md) | Промпт для запроса доработки внешнему чату: что исправить, что reuse, traceability между attempts, лимиты. Опирается на [`v3_revision_contract.md`](../contracts/v3_revision_contract.md). |

## Ключевые принципы

- V3 требует artifact package (ZIP), а не текстовый совет.
- Внешний чат не имеет доступа к локальному repo.
- `Kilo Notebook V3` работает как raw-input mode, а не как обязательный handoff-mode.
- Lifecycle/archive для V3 ведётся через [`../V3_navigation.md`](../V3_navigation.md), по аналогии с `V1` и `V2`.
- Prompt layer не обещает готовый runtime/scripts.

## Связанные документы

- [`../contracts/README.md`](../contracts/README.md) — контракты V3.
- [`../templates/README.md`](../templates/README.md) — шаблоны V3.
- [`../README.md`](../README.md) — главный вход в V3.
- [`../V3_navigation.md`](../V3_navigation.md) — навигация и lifecycle index по V3.
