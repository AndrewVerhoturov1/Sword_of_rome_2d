# Send Note - V3 Planner Orc Role Rules Split

Подготовлен V3 request под фактический split-результат.

Цель:

- получить отдельный canon rules-файл для `Planner`;
- получить отдельный canon rules-файл для `Orc`;
- не возвращаться к single-file варианту;
- не возрождать legacy `Boss / B1` маршрут.

Созданы файлы:

- [V3-20260531-072402-planner-orc-role-rules-split_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260531-072402-planner-orc-role-rules-split_request.md)
- [V3-20260531-072402-planner-orc-role-rules-split_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260531-072402-planner-orc-role-rules-split_prompt.md)

Что должен вернуть внешний чат:

- `manifest.yaml`
- `README_FOR_KILO.md`
- `README_FOR_CODEX.md`
- `checksums.sha256`
- `files/.ai/rules/codex_role_planner.md`
- `files/.ai/rules/codex_role_orc.md`

Что потом особенно проверить:

- `Planner` и `Orc` разведены по двум отдельным файлам;
- `Planner` не превращён в execution role по умолчанию;
- `Orc` описан как execution orchestrator, который в основном маршрутизирует в инструменты;
- нет возврата к `Boss / B1` как к active route.
