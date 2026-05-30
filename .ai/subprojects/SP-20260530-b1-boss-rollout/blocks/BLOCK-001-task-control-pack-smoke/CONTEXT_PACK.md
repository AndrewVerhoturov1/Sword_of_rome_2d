# Context Pack

## Block ID

`BLOCK-001-task-control-pack-smoke`

## Parent Chunk

`CHUNK-001-first-smoke-route`

## Master Artifacts

- Boss bootstrap baseline: `.ai/plans/implementation/boss_orchestrator_bootstrap.md`
- Working plan baseline: `.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md`
- Master rollout baseline: `.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md`

## Relevant Rules

- `AGENTS.md` — repo-level contracts, language policy, human review policy, bug tracking policy, agent-first mandate
- `.ai/rules/agent_protocol.md` — role split between Codex, Boss, Block Orchestrator, Kilo, human
- `.ai/rules/codex_orchestrator.md` — orchestration boundaries and review duty
- `.ai/rules/subagent_tools.md` — canonical names and selection rules for per-task subagent tools
- `.ai/templates/block_plan_template.md` — expected block-plan shape
- `.ai/templates/block_context_pack_template.md` — expected context-pack shape
- `.ai/templates/block_orchestrator_package_template.md` — required fields for package gate artifact
- `.ai/templates/block_report_template.md` — required report structure

## Accepted Decisions

- `SP-20260530-b1-boss-rollout` — recommended first subproject ID for this rollout slice
- `BLOCK-001-task-control-pack-smoke` — canonical first block ID
- `BLOCK-NNN_slug` — canonical block ID grammar
- `B1` — layer label only, not canonical ID
- runtime artifacts must not be pre-created as empty placeholders
- first block is `smoke only`, not full proof
- block decomposition is fixed as `2` subagent calls
- call 1 covers tasks `1-3`
- call 2 covers tasks `4-7`
- bugfixes and minor corrections inside a task stay inside that task, not new planned tasks
- Boss does not assign exact tools per task; Block Orchestrator decides that

## Block Plan Reference

`.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md`

## Context Notes

- Этот блок intentionally включает создание seed docs внутри своей работы.
- Поэтому отсутствие `SUBPROJECT_STATE.md`, `TASK_CONTROL_PACK.md` и других seed docs до запуска блока не считается ошибкой.
- Задача блока — вернуть seed + package + smoke result + block report.
- `Boss review` обязателен, но идет после возврата блока и не входит во внутренние subagent calls.
- До `Boss review` нельзя объявлять final accepted-state в `SUBPROJECT_STATE.md` и `BLOCKS_INDEX.md`.

## Do Not Include

- Полную историю planning chat
- Полные `V1` notebook entries
- Непринятые rejected alternatives
- Контекст будущего `BLOCK-002`, если он не нужен для текущего шага
- Product-code exploration
