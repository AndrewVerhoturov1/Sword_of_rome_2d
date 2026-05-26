# V2 Response: <краткое название>

## V2 ID

`V2-YYYYMMDD-HHMMSS`

## Response path

`.ai/external_reviews/responses/V2-YYYYMMDD-HHMMSS_response.md`

## Статус

`raw_response_captured` / `ingested`

## Provider/Model

`<провайдер> / <модель>` или `not available`

## Source request

Ссылка на V2 request: `.ai/external_reviews/requests/V2-YYYYMMDD-HHMMSS_request.md`

## Ingest method

`manual paste into ordinary Kilo run` — ответ вставлен вручную в запуск Kilo

Или:

`manual local V2 response file` — ответ сохранён в локальный файл и передан в ordinary Kilo run

## Manual ingest note

- Ответ передан в ordinary Kilo run (`kilo-handoff-runner` или `kilo-debugger`).
- `kilo-recorder` в первой версии V2 не используется.
- Ответ не интерпретирован как факт о repo без локальной проверки.
- Это verbatim копия ответа внешнего чата.

## V2 External Answer (Raw)

[Здесь verbatim ответ внешнего чата со всеми обязательными секциями:

- V2 ID
- Context Readback
- Provider/Model
- Answer
  - Confirmed from central docs
  - Confirmed from project docs
  - Confirmed from WIP snapshot
  - Confirmed from base comparison
  - Not available / not verified
  - Main assessment
  - Root cause hypothesis
  - Recommended correction path
  - Risks
  - Suggested implementation notes
  - Questions back to Kilo/user, if any
- Candidate Navigation Entry]

## Ограничения ответа

Что внешний чат не смог или не стал проверять. Цитаты из `Not available / not verified`.

## Метаданные

- Дата получения ответа: YYYY-MM-DD
- Внешний чат: <название>
- Длительность: <если известно>

## Следующий шаг

`/v2 ingest` — запустить interpretation step для формулирования Kilo understanding summary.
