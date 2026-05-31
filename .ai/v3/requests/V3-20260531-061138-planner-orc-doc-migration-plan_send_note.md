# Send Note - V3 Planner Orc Documentation Migration Plan

Подготовлен новый V3 request для внешнего чата.

Цель: на основе [Report 0043](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0043_b1_bos_legacy_inventory_report.md), нового system document [subproject_single_execution_chat_documentation_system_v2.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/ideas/subproject_single_execution_chat_documentation_system_v2.md) и текущих docs проекта получить подробный migration plan документации от legacy `B1/BOS` к active `Planner -> Orc` системе.

Созданы файлы:

- [V3-20260531-061138-planner-orc-doc-migration-plan_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260531-061138-planner-orc-doc-migration-plan_request.md) — структурированный V3 request.
- [V3-20260531-061138-planner-orc-doc-migration-plan_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260531-061138-planner-orc-doc-migration-plan_prompt.md) — готовый copy-paste prompt для внешнего чата.

Что делать:

1. Открыть [V3-20260531-061138-planner-orc-doc-migration-plan_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260531-061138-planner-orc-doc-migration-plan_prompt.md).
2. Скопировать весь текст, начиная со строки `Ты участвуешь в V3 artifact-producing workflow.` и до конца файла.
3. Вставить этот текст во внешний V3-чат.
4. Дождаться ZIP package или ZIP-ready package representation.
5. Вернуть ответ сюда для review.

Что должно прийти в ответ:

- `manifest.yaml`
- `README_FOR_KILO.md`
- `README_FOR_CODEX.md`
- `checksums.sha256`
- `files/.ai/plans/implementation/planner_orc_documentation_migration_plan.md`

Что особенно проверить потом:

- это именно migration plan по документации, а не новый системный трактат;
- `Planner -> Orc` явно обозначен как active replacement system;
- legacy `B1/BOS` route явно не предлагается как active;
- есть file-level migration map;
- есть разделение `update / legacy / keep active / remove from required context / create new`;
- есть guidance по замене терминов и required-context cleanup;
- package не утверждает, что repo уже изменён.
