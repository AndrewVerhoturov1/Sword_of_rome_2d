# V3 Send Note — Phase 5 Safe Pilot

## Что уже подготовлено

- [V3-20260528-030442-phase5-safe-pilot_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260528-030442-phase5-safe-pilot_request.md) — структурированный V3 request.
- [V3-20260528-030442-phase5-safe-pilot_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260528-030442-phase5-safe-pilot_prompt.md) — готовый copy-paste prompt для нижнего чата.

## Что отправить во внешний чат

1. Вставить целиком prompt из [V3-20260528-030442-phase5-safe-pilot_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260528-030442-phase5-safe-pilot_prompt.md).
2. Ничего руками прикладывать не нужно:
   - внутри prompt уже есть commit-pinned GitHub links;
   - внешний чат должен сам прочитать контекст по этим ссылкам.

## Что должно прийти в ответ

- либо реальный ZIP-файл;
- либо ZIP-ready representation с полным содержимым:
  - `manifest.yaml`
  - `README_FOR_KILO.md`
  - `README_FOR_CODEX.md`
  - `checksums.sha256`
  - `files/.ai/v3/docs/pilots/phase5_safe_pilot_note.md`

## Что делать после ответа

1. Если нижний чат дал ZIP или ZIP-ready artifact package, сохранить его локально.
2. Затем вернуться сюда с ответом `Нижний чат ответил`.
3. После этого следующим шагом пойдёт импорт через [0035_v3_phase5_safe_pilot.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/handoffs/0035_v3_phase5_safe_pilot.md).

## Что не считается успехом

- просто совет;
- просто план;
- просто текст markdown-файла без package structure;
- package с двумя и более project files;
- package вне `docs_only` scope.
