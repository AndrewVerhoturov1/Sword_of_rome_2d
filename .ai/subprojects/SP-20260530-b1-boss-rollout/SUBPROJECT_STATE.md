# SUBPROJECT_STATE

Subproject ID: `SP-20260530-b1-boss-rollout`
Task Control Pack ID: `TCP-SP-20260530-b1-boss-rollout-v1`
Status: `closed_by_user`
Owner layer: `none`

> **Legacy/history only.** Эта папка — архив закрытой `B1/BOS/block-orchestration` системы. Не использовать как активный шаблон для новых подпроектов. Активный маршрут: `Planner -> Orc documentation-driven subproject execution`. Хранить для истории и аудита.

Closure mode:
Old `B1/BOS` rollout system is closed. Do not continue blocks, do not create new `B1` tasks, do not restart old hierarchy without new direct user instruction.

Goal:
Historical goal was to prove and harden `Subproject -> Boss -> B1` rollout in this repo without touching product code.

Scope:
- workflow and orchestration docs for first rollout slice;
- first docs-only smoke route;
- package gate, block report, boss review, human gate separation.

Out of scope:
- product code;
- `table-sandbox/**`;
- `arena-prototype-launcher/**`;
- broad central core promotion before proof;
- fake runtime/history placeholders.

Current phase: `closed`
Current rollout slice: `shutdown only`
Current block: `BLOCK-001-task-control-pack-smoke`
Nearest route: `none`

ID rule:
`BLOCK-NNN_slug` is canonical block ID; `B1` is layer label only.

Artifact timing rule:
Canonical docs may exist before execution. Runtime docs must appear only during or after real execution.

Package gate status: `not_started`
Pilot proof status: `cancelled_by_user`
Central promotion status: `blocked_until_two_pilots`

Canonical docs:
- `SHORT_PLAN.md`
- `TASK_CONTROL_PACK.md`
- `BOSS_BOOTSTRAP.md`
- `BLOCKS_INDEX.md`
- `blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md`
- `blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md`

Runtime docs:
- `blocks/BLOCK-001-task-control-pack-smoke/BLOCK_REPORT.md`

Human decision gate:
- user already decided to stop old rollout;
- no further `Boss review` or block continuation expected inside this archived system.

Next action:
- preserve artifacts as historical evidence only;
- do not continue old `B1/BOS` route.
