# TASK_CONTROL_PACK

Task Control Pack ID: `TCP-SP-20260530-b1-boss-rollout-v1`
Subproject ID: `SP-20260530-b1-boss-rollout`
Version: `v1`
Status: `archived_closed_by_user`

## Goal

Historical controlling plan for first rollout slice of `Subproject -> Boss -> B1` workflow in this repo.

## Closure Notice

Old `B1/BOS` system is closed by direct user decision. This pack remains as historical context only. Do not use it to start new `B1` work, new blocks, or old hierarchy runs unless user explicitly reopens that route.

## Scope

- create minimal subproject seed;
- run first docs-only smoke block through real orchestration path;
- preserve strict separation between package gate, block report, boss review, and human gate.

## Out of Scope

- product code changes;
- `table-sandbox/**`;
- runtime/history prebuild;
- broad central-core extraction before proof;
- declaring route fully proven after one smoke pass.

## Source Baseline Summary

- repo already has strong workflow canon for Boss, B1, Kilo, V1, V3, and report gates;
- full runtime proof for subproject/Boss/B1 loop does not exist yet;
- first safe proof step is a docs-only smoke block;
- planning artifacts already selected canonical first IDs:
  - `SP-20260530-b1-boss-rollout`
  - `BLOCK-001-task-control-pack-smoke`

## Target Operating Model Summary

Target route for this slice:

`Subproject -> Planning Chat -> Task Control Pack -> Boss Orchestrator -> B1 Block Chat -> Junior Orchestrator -> Kilo / V1 / V2 / V3 / local verification`

This pack only controls first practical rollout step, not full future expansion.

## Current Rollout Phase

`Phase 1a minimal seed`

## Accepted ID Rule

- `BLOCK-NNN_slug` is canonical block ID.
- `B1` is layer label only.
- Runtime attempts may get separate runtime IDs later, but not as block primary keys.

## Canonical vs Runtime Artifact Timing Rule

- canonical working docs may exist before execution;
- runtime docs must appear only during or after real execution;
- empty placeholders for reports, reviews, journals, and executor artifacts are forbidden.

## First Two Blocks

### Block 1

- ID: `BLOCK-001-task-control-pack-smoke`
- Purpose: validate seed docs, package gate, smoke execution route, and report/review separation
- Status meaning: `smoke only`

### Block 2

- ID: `BLOCK-002-subproject-linkage-validator`
- Purpose: non-trivial local proof for linkage and runtime-placeholder discipline
- Prerequisite: accepted review of `BLOCK-001`

## Package Gate Definition

Package gate must return exactly one explicit verdict:

- `approved`
- `rejected`
- `needs_clarification`
- `waived_by_human`

Package existence alone does not mean gate passed.

## Pilot Exit Criteria

For first smoke pilot to count as complete:

- package gate executed with explicit verdict;
- one bounded docs-only result exists inside allowed scope;
- `BLOCK_REPORT.md` exists and is not a raw executor report;
- `Boss review` happens before any human accept/reject decision;
- subproject state/index updates happen only from evidence.

## Canonical Source Hierarchy

If conflict exists:

1. `AGENTS.md` and active repo rules win.
2. `TASK_CONTROL_PACK.md` controls subproject-specific scope.
3. `BLOCK_PLAN.md` controls block-specific execution.
4. Runtime evidence may inform review, but does not silently rewrite this pack.

## Canonical Links

- Boss bootstrap: `BOSS_BOOTSTRAP.md`
- Blocks index: `BLOCKS_INDEX.md`
- Current block plan: `blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md`
- Current context pack: `blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md`

## Known Risks

- route may be heavier than useful work;
- package gate may become ceremonial if not reviewed strictly;
- docs-only smoke may create false confidence if misread as full proof;
- state/index drift may appear if updates happen before evidence.

## Next Action

No active next action. Historical pack only.
