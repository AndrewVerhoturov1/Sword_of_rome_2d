# Block Plan

## Block ID

`BLOCK-001-task-control-pack-smoke`

## Block Name

Task Control Pack smoke

## Parent Chunk

`CHUNK-001-first-smoke-route`

## Goal

Подготовить и провести первый управляемый docs-only smoke-блок для rollout-системы `Subproject -> Boss -> B1`.

Этот блок должен:

- создать минимальный subproject seed как часть работы блока;
- зафиксировать block-level orchestration artifacts;
- довести блок до `ORCHESTRATOR_PACKAGE.md`;
- пройти реальный package gate;
- провести один bounded docs-only smoke execution;
- вернуть `BLOCK_REPORT.md` для последующего `Boss review`.

Этот блок не доказывает зрелость всей системы. Его статусный смысл: `smoke only`.

## Allowed Files

- `.ai/subprojects/SP-20260530-b1-boss-rollout/SUBPROJECT_STATE.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/SHORT_PLAN.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/TASK_CONTROL_PACK.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/BOSS_BOOTSTRAP.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/BLOCKS_INDEX.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/ORCHESTRATOR_PACKAGE.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_REPORT.md`

## Forbidden Files

- `table-sandbox/**`
- `arena-prototype-launcher/**`
- `canon/**`
- `references/**`
- `docs/**`
- `.ai/plans/master/**`
- `.ai/plans/implementation/**`
- `.ai/repo_navigation.md`
- `.ai/project_state.md`
- любые runtime/history files вне scope текущего блока

## Context Tiers

- **Tier 0:** только этот `BLOCK_PLAN.md`
- **Tier 1:** `BLOCK_PLAN.md` + `CONTEXT_PACK.md` + `ORCHESTRATOR_PACKAGE.md`
- **Tier 2:** нужные rule/master docs, на которые прямо ссылается `CONTEXT_PACK.md`
- **Tier 3-4:** не использовать без блокировки или review-risk

## Required Inputs

- `.ai/plans/implementation/boss_orchestrator_bootstrap.md`
- `.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md`
- `.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md`
- `.ai/rules/agent_protocol.md`
- `.ai/rules/codex_orchestrator.md`
- `AGENTS.md`
- `.ai/templates/block_plan_template.md`
- `.ai/templates/block_context_pack_template.md`
- `.ai/templates/block_orchestrator_package_template.md`
- `.ai/templates/block_report_template.md`

## Lookup Inputs

- `ideas/hierarchical_ai_development_system_with_subproject.md`
- `.ai/prompts/create_block_orchestrator_package.md`
- `.ai/prompts/review_block_report.md`

## Do Not Read Unless Blocked

- полные `V1` notebook entries
- старые Kilo reports вне текущего шага
- большие runtime logs
- старые superseded plans

## Context Budget

Читать только те разделы master rollout plan, которые нужны для:

- ID rule;
- first subproject instantiation;
- docs-only smoke;
- package gate;
- block report / boss review separation.

Не перечитывать весь master plan целиком.

## Execution Mandate

`agent-first`

Содержательное выполнение внутри блока идет через вызовы субагента-младшего оркестратора.
Баги, мелкие исправления и доработки по ходу не считаются отдельными planned tasks, а входят в ту задачу, внутри которой возникли.

## Block Orchestrator Role

`Block Orchestrator Chat`:

- не перепридумывает цель блока;
- не меняет decomposition `2 calls / 7 tasks`;
- сам выбирает конкретный инструмент для каждой задачи внутри вызова;
- сам проводит package gate и внутреннюю проверку;
- возвращает `BLOCK_REPORT.md`;
- не объявляет итог блока принятым вместо `Boss review`.

## Primary Execution Path

`delegated by Block Orchestrator per task`

Boss не фиксирует инструмент заранее.
Block Orchestrator сам решает, что именно использовать внутри каждой задачи: `Kilo`, `V1`, `V2`, `V3` или допустимую bounded-работу младшего оркестратора.

## Allowed Agent Kinds

- `Kilo Code`
- `External Web Chat`
- `V1`
- `V2`
- `V3`
- `bounded junior-orchestrator direct work`

## Exception Status

`none`

## Planned Agent Sequence

Обязательная структура этого блока — ровно `2` вызова субагента-младшего оркестратора.

### Subagent Call 1

#### Task 1. Create minimal subproject entity

Собрать стартовую сущность подпроекта как рабочую единицу:

- определить `subproject_id`;
- зафиксировать название, цель, `scope / out of scope`;
- зафиксировать текущий rollout-slice;
- зафиксировать ближайший route `Boss -> BLOCK-001 -> report -> Boss review -> human gate`.

Goal:
получить минимальный subproject container, от которого можно честно запустить первый `Boss -> Block` route.

Success Criteria:
появилась одна согласованная subproject-сущность с `subproject_id`, целью, границами, текущим slice и ближайшим route без fake accepted-state.

Subagent Tool:
`V3-Ревью`

Reason:
это важный workflow-doc artifact. Нужен сильный первый draft для структуры subproject entity, после чего допустима только локальная проверка и небольшая доводка.

#### Task 2. Create seed docs

Подготовить и согласованно заполнить:

- `SUBPROJECT_STATE.md`
- `SHORT_PLAN.md`
- `TASK_CONTROL_PACK.md`
- `BOSS_BOOTSTRAP.md`
- минимальный `BLOCKS_INDEX.md`

Seed docs не должны содержать:

- full-history dump;
- fake runtime paths;
- пустые history placeholders;
- объявление `accepted` без evidence.

Goal:
создать минимальный набор seed docs, достаточный для первого управляемого smoke-route без разрастания бюрократии.

Success Criteria:
созданы все пять seed docs; они согласованы между собой; в них нет fake runtime/history placeholders и нет premature accepted-state.

Subagent Tool:
`V3-Ревью`

Reason:
это основной пакет важной документации внутри блока. По пользовательскому правилу baseline для важной документации = `V3`; subagent после этого должен только проверить и слегка довести результат.

#### Task 3. Create block start package

Подготовить или довести до согласованного состояния:

- `BLOCK_PLAN.md`
- `CONTEXT_PACK.md`

В этих docs должно быть явно зафиксировано:

- цель smoke-блока;
- allowed / forbidden boundary;
- expected outputs;
- stop conditions;
- human decision point после `Boss review`;
- правило ID: `BLOCK-NNN_slug` — canonical, `B1` — только layer label;
- текущий блок = smoke only, не proof всей системы.

Goal:
довести block-start artifacts до состояния, в котором их можно использовать как честный execution boundary для первого smoke-блока.

Success Criteria:
`BLOCK_PLAN.md` и `CONTEXT_PACK.md` согласованы между собой, явно фиксируют scope/boundary/outputs/stop conditions и не противоречат canonical ID rules.

Subagent Tool:
`Kilo`

Reason:
задача repo-grounded и проверочная. Здесь важнее локальная валидация уже существующих файлов и точное согласование артефактов, чем внешний draft.

### Subagent Call 2

#### Task 4. Prepare `ORCHESTRATOR_PACKAGE.md`

Собрать рабочий package для запуска блока как orchestration-единицы:

- ссылки на planning/source artifacts;
- scope и boundary;
- expected outputs;
- escalation path;
- внутренняя карта `2 calls / 7 tasks`.

Goal:
собрать рабочий package artifact, по которому младший оркестратор сможет запускать блок без пересборки контекста с нуля.

Success Criteria:
`ORCHESTRATOR_PACKAGE.md` содержит ссылки на source artifacts, scope/boundary, expected outputs, escalation path и карту `2 calls / 7 tasks` без scope drift.

Subagent Tool:
`V3-Ревью`

Reason:
это важный orchestration-doc. Пользовательский baseline для важной документации = `V3`, а локальная работа после внешнего draft должна оставаться review-first.

#### Task 5. Apply real package gate

Вынести один явный verdict:

- `approved`
- `rejected`
- `needs_clarification`
- `waived_by_human`

Если gate не пройден, это фиксируется как реальный outcome блока без fake partial success.

Goal:
вынести честный gate verdict на основе фактического состояния package artifacts, а не на основе деклараций.

Success Criteria:
есть ровно один явный verdict; он обоснован содержимым файлов; при неуспехе outcome зафиксирован без fake partial success.

Subagent Tool:
`Kilo`

Reason:
package gate требует локальной проверки фактических файлов и repo-grounded verdict. Внешний reasoning здесь не заменяет локальную верификацию.

#### Task 6. Run bounded docs-only smoke execution

Провести один реальный исполнительный цикл в пределах workflow-docs:

- есть фактический результат;
- product code не затронут;
- результат проверяем по файлам, а не по декларации.

Goal:
показать один реальный docs-only execution cycle внутри разрешённого scope, чтобы блок вернул не только планы, но и evidence.

Success Criteria:
есть наблюдаемый файловый результат, product code не затронут, проверка опирается на фактические файлы и действия, а не на декларацию.

Subagent Tool:
`Kilo`

Reason:
это реальный execution cycle внутри repo. Нужен локальный исполнительный и проверочный путь, а не внешний draft route.

#### Task 7. Prepare `BLOCK_REPORT.md`

Собрать итоговый отчет блока и review bundle для Boss:

- `Status`
- `Changed Files`
- `Created Files`
- `Checks Run`
- `Баги и сложности`
- `Human Check`
- `Agent Execution Evidence`
- `Block Orchestrator Package Verification`
- `Deviations from Block Plan`
- `Blocked Items`
- `Required Lead Action`

Goal:
собрать итоговый block report, пригодный для `Boss review`, с evidence, verdict и открытыми вопросами.

Success Criteria:
`BLOCK_REPORT.md` заполнен по required sections, опирается на реальные результаты блока и не подменяет собой `Boss review`.

Subagent Tool:
`Kilo`

Reason:
report должен собираться из локального evidence: changed files, checks, verdict, blocked items. Для этого нужен repo-grounded путь.

## Planned Human Checkpoints

`none`

Обоснование:
этот блок целиком про workflow-docs. Human gate нужен после `Boss review`, а не внутри вызовов субагента.

## Expected Outputs

- `.ai/subprojects/SP-20260530-b1-boss-rollout/SUBPROJECT_STATE.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/SHORT_PLAN.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/TASK_CONTROL_PACK.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/BOSS_BOOTSTRAP.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/BLOCKS_INDEX.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/ORCHESTRATOR_PACKAGE.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_REPORT.md`

## Stop Conditions

- Block Orchestrator пытается переписать decomposition блока вместо исполнения утвержденного плана.
- Для завершения задачи требуется править forbidden files или product code.
- Возникает необходимость придумывать новый ID grammar.
- Невозможно вынести честный package gate verdict.
- Невозможно показать фактический docs-only result.
- Отчет нельзя собрать без фиктивных claims.

## Acceptance Criteria

- [ ] Структура блока = ровно `2` вызова субагента.
- [ ] Вызов 1 покрывает задачи `1-3`.
- [ ] Вызов 2 покрывает задачи `4-7`.
- [ ] Seed docs созданы как часть работы блока, не заранее.
- [ ] Есть реальный package gate verdict.
- [ ] Есть bounded docs-only smoke result.
- [ ] `BLOCK_REPORT.md` собран и пригоден для `Boss review`.
- [ ] Финальный accepted-state не объявлен до `Boss review`.

## Block Report Path

`.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_REPORT.md`
