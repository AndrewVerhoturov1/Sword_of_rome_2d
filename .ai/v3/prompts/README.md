# V3 Prompts

Эта папка будет содержать промпты для V3 artifact-producing workflow.

## Текущий статус

Placeholder. Промпты ещё не созданы — это задача Phase 3 rollout.

## Ожидаемое содержимое (Phase 3)

- **create_v3_request_prompt.md** — промпт для Codex: как подготовить V3-запрос для внешнего чата.
- **kilo_notebook_v3_mode_prompt.md** — промпт для Kilo Notebook V3: безопасный import flow, проверка manifest, запись файлов, journaling.
- **codex_v3_review_prompt.md** — промпт для Codex: проверка journal, сверка файлов с задачей, human review gates.
- **v3_revision_request_prompt.md** — промпт для запроса доработки: что исправить, уточнение scope.

Эти промпты будут опираться на контракты из [`contracts/`](../contracts/README.md) и шаблоны из [`templates/`](../templates/README.md).

Промпты для внешнего чата должны:
- требовать artifact package (ZIP), а не текстовый совет;
- явно указывать, что модель не имеет доступа к репозиторию;
- требовать manifest, checksums и files/ в структуре пакета.
