# Send Note - V3 Battle Status Dashboard HTML with Required Testing Prompt

Подготовлен новый V3 request для живого end-to-end test-cycle уже после закрытия `Phase 7`.

Созданы файлы:

- [V3-20260529-234145-battle-status-dashboard-html-with-testing_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-234145-battle-status-dashboard-html-with-testing_request.md) — структурированный V3 request.
- [V3-20260529-234145-battle-status-dashboard-html-with-testing_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-234145-battle-status-dashboard-html-with-testing_prompt.md) — готовый copy-paste prompt для внешнего чата.

Что делать:

1. Открыть [V3-20260529-234145-battle-status-dashboard-html-with-testing_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-234145-battle-status-dashboard-html-with-testing_prompt.md).
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
- `files/table-sandbox/v3-pilots/battle_status_dashboard_russian.html`

Что особенно проверить потом:

- `POST_IMPORT_TEST_PROMPT.md` действительно есть;
- внутри него есть все 4 секции:
  - `Execution split proposal`
  - `Machine checks`
  - `Human checks`
  - `Machine-check report output`
- package не утверждает, что repo уже изменён;
- package не включает лишние project files;
- canonical report path с exact `V3 ID` указан явно.
