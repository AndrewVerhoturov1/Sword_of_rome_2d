# V3 Send Note - Phase 5A-5C Deep Doc Pack

## Что уже подготовлено

- [V3-20260528-195750-phase5A-5C-deep-doc-pack_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260528-195750-phase5A-5C-deep-doc-pack_request.md) — структурированный V3 request.
- [V3-20260528-195750-phase5A-5C-deep-doc-pack_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260528-195750-phase5A-5C-deep-doc-pack_prompt.md) — готовый copy-paste prompt для внешнего чата.

## Что отправить во внешний чат

1. Вставить целиком prompt из [V3-20260528-195750-phase5A-5C-deep-doc-pack_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260528-195750-phase5A-5C-deep-doc-pack_prompt.md).
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
  - `files/.ai/v3/docs/phase5A_external_artifact_generation_pilot_detailed_implementation.md`
  - `files/.ai/v3/docs/phase5B_pre_kilo_package_review_detailed_implementation.md`
  - `files/.ai/v3/docs/phase5C_kilo_notebook_v3_ui_setup_detailed_implementation.md`

## Что делать после ответа

1. Если внешний чат дал ZIP или ZIP-ready artifact package, сохранить его локально.
2. Затем вернуться сюда с ответом `Нижний чат ответил`.
3. После этого пойдёт pre-Kilo package review, без Kilo import.

## Что не считается успехом

- просто советы;
- просто общий план;
- один короткий markdown вместо 3 отдельных файлов;
- пакет с лишними project files;
- пакет, который уходит в `Phase 5D` import-stage вместо `Phase 5A/5B/5C` docs-разбора.
