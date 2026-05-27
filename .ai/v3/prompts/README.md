# V3 Prompts

Эта папка содержит промпты для V3 artifact-producing workflow.

## Текущий статус

**Phase 3 завершён (2026-05-27):** все 4 промпта созданы. Каждый промпт опирается на Phase 2 контракты и готов к использованию.

## Содержимое

| Файл | Назначение |
|------|------------|
| [`create_v3_request_prompt.md`](create_v3_request_prompt.md) | Промпт для Codex/человека: как подготовить V3-запрос к внешнему чату. Требует artifact package, а не текстовый совет. Опирается на [`v3_request_contract.md`](../contracts/v3_request_contract.md). |
| [`kilo_notebook_v3_mode_prompt.md`](kilo_notebook_v3_mode_prompt.md) | Mode prompt для `Kilo Notebook V3`: безопасный import flow, проверка manifest/path/checksum, create-only для MVP, journaling, стоп-условия. Не обещает готовый runtime/scripts. |
| [`codex_v3_review_prompt.md`](codex_v3_review_prompt.md) | Промпт для Codex после V3 import: проверка journal и реальных файлов, сверка с request/scope, нормализованный verdict enum, human review gates. Опирается на [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md). |
| [`v3_revision_request_prompt.md`](v3_revision_request_prompt.md) | Промпт для запроса доработки внешнему чату: что исправить, что reuse, traceability между attempts, лимиты. Опирается на [`v3_revision_contract.md`](../contracts/v3_revision_contract.md). |

Все промпты опираются на контракты из [`contracts/`](../contracts/README.md) (Phase 2) и связаны с шаблонами из [`templates/`](../templates/README.md) (Phase 3).

## Ключевые принципы

Промпты этого слоя следуют общим правилам:
- Требуют artifact package (ZIP), а не текстовый совет.
- Явно указывают, что внешний чат не имеет доступа к репозиторию.
- Требуют `manifest.yaml`, `checksums.sha256` и `files/` в структуре пакета.
- Не обещают готовый runtime/scripts (это Phase 7).
- Не пересекаются с `/v1`, `/r1`, `/v2` маршрутами.

## Связанные документы

- [`../contracts/README.md`](../contracts/README.md) — контракты V3 (Phase 2).
- [`../templates/README.md`](../templates/README.md) — шаблоны V3 (Phase 3).
- [`../README.md`](../README.md) — главный вход в V3.
- [`../V3_navigation.md`](../V3_navigation.md) — навигация по V3.
