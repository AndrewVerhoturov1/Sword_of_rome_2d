# V3 Send Note - Project and Sword of Rome Briefs

## Что уже подготовлено

- [V3-20260529-040855-project-and-sword-of-rome-briefs_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-040855-project-and-sword-of-rome-briefs_request.md) — структурированный V3 request.
- [V3-20260529-040855-project-and-sword-of-rome-briefs_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-040855-project-and-sword-of-rome-briefs_prompt.md) — готовый copy-paste prompt для внешнего чата.

## Что отправить во внешний чат

1. Вставить целиком prompt из [V3-20260529-040855-project-and-sword-of-rome-briefs_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-040855-project-and-sword-of-rome-briefs_prompt.md).
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
  - `files/.ai/v3/docs/project_brief_2d_wargame_constructor.md`
  - `files/.ai/v3/docs/sword_of_rome_module_brief.md`

## Что должно быть внутри project files

- два отдельных markdown-файла;
- оба на русском;
- оба короткие и понятные;
- один про весь проект;
- второй отдельно про `Меч Рима` как тестовый модуль.

## Что делать после ответа

1. Если внешний чат дал ZIP или ZIP-ready artifact package, сохранить его локально.
2. Затем вернуться сюда с ответом `Нижний чат ответил`.
3. После этого пойдёт package review.
4. Только потом будем решать, нужен ли import.

## Что не считается успехом

- просто абзац в чате;
- один файл вместо двух;
- слишком длинная архитектурная простыня;
- описание проекта как одной цифровой игры;
- описание `Меча Рима` как всего продукта.
