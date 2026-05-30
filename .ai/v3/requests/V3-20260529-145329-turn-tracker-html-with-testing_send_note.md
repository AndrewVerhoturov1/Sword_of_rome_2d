# Send Note - V3 Turn Tracker HTML with Required Testing Prompt

Подготовлен новый V3 request для следующего живого test-cycle после внедрения лёгкого post-import testing layer.

Созданы файлы:

- [V3-20260529-145329-turn-tracker-html-with-testing_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-145329-turn-tracker-html-with-testing_request.md) — структурированный V3 request.
- [V3-20260529-145329-turn-tracker-html-with-testing_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-145329-turn-tracker-html-with-testing_prompt.md) — готовый copy-paste prompt для внешнего чата.

Что делать:

1. Открыть [V3-20260529-145329-turn-tracker-html-with-testing_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-145329-turn-tracker-html-with-testing_prompt.md).
2. Скопировать весь текст, начиная со строки `Ты участвуешь в V3 artifact-producing workflow.` и до конца файла.
3. Вставить этот текст во внешний V3-чат.
4. Дождаться ZIP package или ZIP-ready package representation.
5. Вернуть ответ сюда для review.

Что должно прийти в ответ:

- `manifest.yaml`
- `README_FOR_KILO.md`
- `README_FOR_CODEX.md`
- `checksums.sha256`
- `POST_IMPORT_TEST_PROMPT.md`
- `files/table-sandbox/v3-pilots/turn_tracker_russian.html`

Что особенно проверить потом:

- `POST_IMPORT_TEST_PROMPT.md` действительно есть;
- внутри него есть явный split:
  - `Machine checks`
  - `Human checks`
- package не утверждает, что repo уже изменён;
- package не включает лишние project files.
