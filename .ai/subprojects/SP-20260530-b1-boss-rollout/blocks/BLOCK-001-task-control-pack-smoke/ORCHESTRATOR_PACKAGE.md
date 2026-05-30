# Block Orchestrator Package

## Package ID

`PACKAGE-BLOCK-001-task-control-pack-smoke-v1`

## Parent Block

`BLOCK-001-task-control-pack-smoke`

## Created By

`Boss / Main Execution Orchestrator`

## Recipient

`Block Orchestrator Chat`

## Planning Document Reference

- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md`

## Block Artifacts Reference

- Block Plan: `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md`
- Context Pack: `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md`

## Block Scope

Запустить и довести до reviewable result первый docs-only smoke block для rollout-системы.

Обязательный результат блока:

- создать minimal subproject seed;
- собрать block-level artifacts;
- подготовить `ORCHESTRATOR_PACKAGE.md`;
- пройти реальный package gate;
- провести один bounded docs-only smoke execution;
- собрать `BLOCK_REPORT.md`.

## Block Boundary

Вне scope:

- product code;
- `table-sandbox/**`;
- broad rewrite master plans;
- расширение в `BLOCK-002`;
- pre-creating fake runtime/history docs;
- объявление route fully proven.

## Agent Path Policy

Boss не назначает конкретный инструмент по задачам заранее.

Block Orchestrator обязан:

- для каждой задачи внутри вызова сам выбрать точный путь исполнения;
- использовать только допустимые routes;
- не менять decomposition `2 calls / 7 tasks`;
- не превращать bugfixes в новые planned tasks.

## Junior Execution Boundary

Младший оркестратор:

- выполняет уже запланированные задачи блока;
- сам выбирает конкретный инструмент внутри разрешенного пути;
- сам проверяет результат задачи;
- не меняет цель блока;
- не добавляет новые planned tasks;
- не объявляет accepted-state вместо Boss.

## Allowed Agent Kinds

- `Kilo Code`
- `External Web Chat`
- `V1`
- `V2`
- `V3`
- `bounded junior-orchestrator direct work`

## Planned Agent Sequence

### Subagent Call 1

- Task 1: create minimal subproject entity
  - Goal: produce one minimal subproject container for first `Boss -> Block` route
  - Success Criteria: subproject entity fixes id, purpose, scope and nearest route without fake accepted-state
  - Subagent Tool: `V3-Ревью`
  - Reason: important workflow-doc artifact; strong draft first, then local verify/minor fix
- Task 2: create seed docs
  - Goal: create minimal seed doc set for first smoke route
  - Success Criteria: five seed docs exist, are mutually consistent and contain no fake placeholders
  - Subagent Tool: `V3-Ревью`
  - Reason: important documentation package; user preference = V3 baseline for important docs
- Task 3: create block start package
  - Goal: finalize `BLOCK_PLAN.md` and `CONTEXT_PACK.md` as real execution boundary
  - Success Criteria: both files are locally validated, aligned and consistent with block rules
  - Subagent Tool: `Kilo`
  - Reason: repo-grounded validation/finalization of existing local files

### Subagent Call 2

- Task 4: prepare `ORCHESTRATOR_PACKAGE.md`
  - Goal: assemble working orchestration package for block launch
  - Success Criteria: package contains artifacts, boundaries, expected outputs, escalation path and `2 calls / 7 tasks`
  - Subagent Tool: `V3-Ревью`
  - Reason: important orchestration document; strong draft first, then local verify/minor fix
- Task 5: apply real package gate
  - Goal: return one honest gate verdict from actual files
  - Success Criteria: exactly one explicit verdict grounded in local artifact state
  - Subagent Tool: `Kilo`
  - Reason: gate verdict requires local file verification
- Task 6: run bounded docs-only smoke execution
  - Goal: produce one real docs-only execution result inside allowed scope
  - Success Criteria: observable file-based result, no product-code touch, evidence-based verification
  - Subagent Tool: `Kilo`
  - Reason: real repo-grounded execution and verification path
- Task 7: prepare `BLOCK_REPORT.md`
  - Goal: assemble Boss-reviewable final report
  - Success Criteria: report covers required sections and is grounded in local evidence
  - Subagent Tool: `Kilo`
  - Reason: report must be built from actual changed files, checks and verdicts

Правило:
minor fixes, found bugs and small corrections stay inside the task where they appear.

## Planned Human Checkpoints

`none`

Human gate остается после `Boss review`.

## Direct Canonical Dependencies

Разрешено открывать только:

- `.ai/plans/implementation/boss_orchestrator_bootstrap.md`
- `.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md`
- `.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md`
- `.ai/rules/agent_protocol.md`
- `.ai/rules/codex_orchestrator.md`
- `AGENTS.md`
- template/prompt files, прямо названные в `CONTEXT_PACK.md`

Если нужен другой file outside this set:
вернуть `Blocked / Clarification Request`.

## Default Escalation Path

При ambiguity, missing dependency, scope conflict или невозможности честно выбрать execution path:

- не домысливать;
- не расширять scope;
- вернуть `Blocked / Clarification Request`.

## Expected Outputs

- `.ai/subprojects/SP-20260530-b1-boss-rollout/SUBPROJECT_STATE.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/SHORT_PLAN.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/TASK_CONTROL_PACK.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/BOSS_BOOTSTRAP.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/BLOCKS_INDEX.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/ORCHESTRATOR_PACKAGE.md`
- `.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_REPORT.md`

## Context Budget

Read only direct dependencies.
Do not open full history unless blocked.

## Stop Conditions

- Нужен выход в forbidden files
- Нужен новый ID grammar
- Нельзя вынести package gate verdict
- Нельзя показать фактический smoke result
- Для завершения блока пришлось бы добавить новые planned tasks вне `1-7`

## Gate Confirmation

- [x] Boss не назначил конкретный инструмент для задач заранее
- [x] decomposition блока зафиксирован как `2 calls / 7 tasks`
- [x] seed docs должны быть созданы внутри блока, а не считаются предварительно готовыми
- [x] `Boss review` идет после возврата блока
