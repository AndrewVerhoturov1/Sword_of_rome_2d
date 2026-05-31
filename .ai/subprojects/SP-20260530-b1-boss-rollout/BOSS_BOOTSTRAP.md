# BOSS_BOOTSTRAP

Subproject ID: `SP-20260530-b1-boss-rollout`
Boss Session ID: `BOSS-SP-20260530-b1-boss-rollout-S01`

## Boss Role

- own execution loop for `SP-20260530-b1-boss-rollout`;
- do not execute block work directly;
- enforce package gate before executor work;
- review `BLOCK_REPORT.md` before updating state;
- return human decision points in simple language.

## Required Inputs

- `SUBPROJECT_STATE.md`
- `SHORT_PLAN.md`
- `TASK_CONTROL_PACK.md`
- `BLOCKS_INDEX.md`
- `blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md`
- `blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md`

## Escalation-Only Inputs

Open only if blocked or review risk appears:

- `.ai/plans/implementation/boss_orchestrator_bootstrap.md`
- `.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md`
- `.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md`
- raw planning transcripts
- unrelated old runtime reports

## Hard Gates

- ID rule accepted: `BLOCK-NNN_slug` canonical, `B1` layer only.
- Canonical/runtime artifact split accepted.
- Package gate must return `approved`, `rejected`, `needs_clarification`, or `waived_by_human`.
- No executor handoff or executor package before package gate.
- Junior Orchestrator does not self-execute.
- Docs-only smoke does not equal full proof.
- Second non-trivial pilot required before central promotion.

## First Block

- `BLOCK-001-task-control-pack-smoke`

## Boss Operating Sequence

1. Read `SUBPROJECT_STATE.md` current phase and next action.
2. Read `BLOCKS_INDEX.md` current block status.
3. Read `TASK_CONTROL_PACK.md` for controlling scope.
4. Review current `BLOCK_PLAN.md` and `CONTEXT_PACK.md`.
5. Prepare or review `ORCHESTRATOR_PACKAGE.md`.
6. Apply package gate before any executor run.
7. After block return, read `BLOCK_REPORT.md`.
8. Write `Boss review`.
9. Update `SUBPROJECT_STATE.md`, `SHORT_PLAN.md`, and `BLOCKS_INDEX.md` only from evidence.

## After Each Block

- read block report;
- perform boss review;
- update state/index after evidence only;
- record only real decisions;
- return human gate if route continuation needs approval.

## Immediate Next Step

Prepare `ORCHESTRATOR_PACKAGE.md` for `BLOCK-001-task-control-pack-smoke` and do not skip package gate.
