# Send Note - V3 Token Cost Normalizer V1 Implementation Pack

## Что отправить во внешний чат

1. Открой [V3-20260605-141503-token-cost-normalizer-v1_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260605-141503-token-cost-normalizer-v1_prompt.md).
2. Скопируй весь prompt целиком, начиная со строки `Ты участвуешь в V3 artifact-producing workflow.`.
3. Отправь его во внешний чат.

## Что попросить вернуть

- настоящий ZIP artifact package;
- или ZIP-ready package representation с полным содержимым:
  - `manifest.yaml`
  - `README_FOR_KILO.md`
  - `README_FOR_CODEX.md`
  - `checksums.sha256`
  - `files/.ai/subprojects/tokken_dashboard/drafts/token_cost_normalizer_v1_implementation_pack.md`

## Что делать после ответа

- не нужно вручную раскладывать ZIP по `_local/...`;
- следующий штатный шаг: передать полученный ZIP package source в обычный V3 import route через `Kilo Notebook V3`;
- то есть этот send note готовит внешний запрос, а импорт пакета пойдет отдельным нормальным шагом после получения ответа.

## Важная граница

- Это не `/v3` import в рамках этого внешнего запроса.
- Но после получения ZIP пакет должен быть пригоден для обычного штатного импорта через `Kilo Notebook V3`.
- Это не запись в репозиторий.
- Это не прямое создание `scripts/`, `config/`, `tests/` и live docs.
- Это только один repo-local implementation pack для последующего локального применения через Kilo.
