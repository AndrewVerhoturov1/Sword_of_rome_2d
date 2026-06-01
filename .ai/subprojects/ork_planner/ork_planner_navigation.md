# Ork Planner Navigation

Slug: `ork_planner`  
Owner: `Orc`  
Status: `active`  
Last updated: 2026-06-01

## Purpose

Subproject-wide navigation map for `ork_planner`.

This file is shared orientation. It is broader than `plan_index` and narrower than the full plan.

## Current lifecycle stage

Current execution stage:

```text
Stage 2 — First Orc nav pass
```

Current gate state:

```text
Nav layer created; Stage 2 report pending human review.
```

## Start here

- Human-first strategic source: [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md)
- Agent-first retrieval index: [ork_planner_plan_index.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_index.md)
- Factual execution log: [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
- Planner decision memory: [ork_planner_plan_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md)

## Existing documents

- [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md)
  Purpose: canonical Planner-owned base.
- [ork_planner_plan_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md)
  Purpose: Planner-owned decision memory.
- [ork_planner_planner_request_ideas.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_planner_request_ideas.md)
  Purpose: Planner support artifact only; not part of active Orc route.
- [ork_planner_plan_index.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_index.md)
  Purpose: agent reading index for `plan_full`.
- [ork_planner_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_navigation.md)
  Purpose: shared navigation map.
- [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
  Purpose: factual execution log.

## Planned documents not created yet

- `ork_planner_battle_plan.md`
  Planned stage: `Stage 3`
- `ork_planner_readme.md`
  Planned stage: `Stage 4`
- `ork_planner_status.md`
  Planned stage: `Stage 4`
- `ork_planner_decisions.md`
  Planned stage: `Stage 4`

## Planner-owned documents

- [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md)
- [ork_planner_plan_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md)
- [ork_planner_planner_request_ideas.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_planner_request_ideas.md)

## Orc-owned documents

- [ork_planner_plan_index.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_index.md)
- [ork_planner_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_navigation.md)
- [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)

Human entry later should come through `readme`, not through `plan_index`.

## Do not use / non-canonical files

- `ork_planner_plan_navigation.md`
  Non-canonical in new route.
- `ork_planner_plan_active_1.md`
  Replaced by single `ork_planner_battle_plan.md`.
- `Boss / B1 / Junior Orchestrator`
  Legacy/history only, not active route.

## Reading routes

- Human wanting big picture:
  [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md) -> this file -> journal
- Agent wanting exact execution rules:
  [ork_planner_plan_index.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_index.md) -> `plan_full` anchors -> journal
- Planner wanting prior decisions:
  [ork_planner_plan_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md) -> `plan_full`

## Tool/external material references

- Approved historical Stage 2 route before explicit override:
  `Kilo Handoff Runner`
- Actual Stage 2 implementation route for this run:
  direct Codex work by explicit human override
- Relevant repo-level role rules:
  [codex_role_orc.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/codex_role_orc.md)
  [codex_role_planner.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/codex_role_planner.md)
  [codex_orchestrator.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/codex_orchestrator.md)

## Maintenance rule

- Keep this map factual.
- Add future docs only after they really exist.
- Do not pretend planned docs already exist.
- If lifecycle stage changes, update this file together with journal and later status docs.
