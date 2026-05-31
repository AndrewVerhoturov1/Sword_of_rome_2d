# Session: planner_orc_docs_migration

## Session ID

`2026-05-31_planner_orc_docs_migration`

## Status

in_progress

## Goal

Выполнить полную migration-задачу по documentation/workflow слою:

- убрать старую `B1/BOS/block-orchestration` систему из active route;
- перевести живые workflow docs на active route `Planner -> Orc`;
- пометить старые ключевые документы как `legacy/history`;
- очистить required context от старого маршрута;
- не создавать при этом новую active структуру подпроекта.

## Approved Plan

### P1: Full Planner Orc Docs Migration

- Status: ready.
- Использовать [planner_orc_documentation_migration_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/implementation/planner_orc_documentation_migration_plan.md) как главный execution guide.
- Обновить active contract и navigation layer.
- Обновить active rules/prompt/template слой там, где старая `B1/BOS` схема всё ещё выглядит как рабочий маршрут.
- Пометить ключевые старые документы как `legacy/history`.
- При необходимости добавить минимальную archive-note в старый rollout subproject, но не переписывать весь архив.
- Не создавать новую active Planner/Orc file-structure в этой задаче.
- Не трогать product-code.
- Не трогать `.ai/v3/**`, кроме уже существующих runtime artifacts этой задачи.
- Завершить repo-wide verification search после изменений.

## Active Plan Item

`P1: Full Planner Orc Docs Migration`

## Runs

- `Session run: 001` - prepare Kilo handoff for full docs migration from legacy `B1/BOS` to active `Planner -> Orc`.
- `Session review: 001` - Kilo result reviewed by Codex; not accepted yet due to remaining active old-route artifacts and inaccurate report claims.
- `Session review: 002` - correction run reviewed by Codex; accepted as docs-migration result within agreed scope.

## User Overrides

- Выполнить всю migration-задачу, а не только кусок.
- Новую active структуру пока не создавать.
- `Orc` — это управляющий execution-chat, который сам в основном маршрутизирует в инструменты.
- Смысл задачи: убрать старую систему как active route, а не строить новую структуру.
- Мелочи сейчас не полировать; править только существенные места.

## Checkpoint State

- [Report 0043](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0043_b1_bos_legacy_inventory_report.md) уже опубликован и является source inventory по legacy `B1/BOS` следам.
- [subproject_single_execution_chat_documentation_system_v2.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/ideas/subproject_single_execution_chat_documentation_system_v2.md) принят как новая active concept-model.
- [planner_orc_documentation_migration_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/implementation/planner_orc_documentation_migration_plan.md) уже импортирован из V3 и принят как migration guide.
- Обнаружено, что следы старой системы есть не только в `AGENTS.md` и `repo_navigation.md`, но и в `.ai/rules/`, `.ai/prompts/`, `.ai/templates/`.
- Первый Kilo migration run пока не принят:
  - в [AGENTS.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/AGENTS.md) всё ещё активен shortcut `/b1` с `Block Orchestrator Chat`;
  - в [.ai/rules/agent_protocol.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/agent_protocol.md) остались большие активные секции `Role separation for block orchestration` и `Runtime block orchestration operating contract`;
  - [0044_planner_orc_docs_migration_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0044_planner_orc_docs_migration_report.md) содержит неверное утверждение, что старые термины отсутствуют в active contract files / prompts / templates / rules.
- Correction run принят в рамках agreed scope:
  - `/b1` переведён в explicit legacy в [AGENTS.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/AGENTS.md), [.ai/rules/agent_protocol.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/agent_protocol.md) и [.ai/rules/codex_orchestrator.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/codex_orchestrator.md);
  - большие active-looking секции block orchestration в [.ai/rules/agent_protocol.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/agent_protocol.md) сведены к short legacy blocks;
  - prompts/templates с old body оставлены допустимо как historical helpers под явными legacy headers;
  - новая active структура подпроекта не создана.
