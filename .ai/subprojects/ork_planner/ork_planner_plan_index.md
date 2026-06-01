# Ork Planner Plan Index

Slug: `ork_planner`  
Target file: `ork_planner_plan_full.md`  
Owner: `Orc`  
Audience: agents  
Status: `active`  
Last updated: 2026-06-01

## Purpose

Agent-oriented index for [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md).

This file is for fast agent retrieval, not for human-first reading.

## Audience and non-goals

- Audience: Orc, Kilo, verifier-style agent runs, recovery after compaction.
- Non-goals:
  - not a human README;
  - not a journal;
  - not a status file;
  - not a replacement for `plan_full`.

## Index rule

- Use semantic anchors from `plan_full`, not line numbers.
- Prefer shortest route that answers current execution question.
- If `plan_full` anchor text changes later, this file must be audited before reuse.

## Fast anchor table

| Need | Anchor |
|---|---|
| Purpose of pilot | [`#mission-of-ork-planner`](#mission-of-ork-planner) |
| Forbidden drift / safety boundaries | [`#non-goals-and-forbidden-drifts`](#non-goals-and-forbidden-drifts) |
| Source authority order | [`#source-basis-and-source-authority-order`](#source-basis-and-source-authority-order) |
| Planner limits | [`#planner-role-boundaries`](#planner-role-boundaries) |
| Planner vs Orc ownership | [`#planner-owned-vs-orc-owned-artifacts`](#planner-owned-vs-orc-owned-artifacts) |
| Lifecycle overview | [`#lifecycle-overview`](#lifecycle-overview) |
| Tool route discipline | [`#v1-v3-kilo-usage-and-recommend-or-waive-rule`](#v1-v3-kilo-usage-and-recommend-or-waive-rule) |
| Stage 2 execution detail | [`#first-orc-nav-pass`](#first-orc-nav-pass) |
| Stage 3 battle plan detail | [`#one-battle-plan-and-approval-gate`](#one-battle-plan-and-approval-gate) |
| Hard phase boundaries | [`#three-hard-phases-of-the-pilot`](#three-hard-phases-of-the-pilot) |
| Future doc minimum blocks | [`#minimal-required-blocks-for-future-docs`](#minimal-required-blocks-for-future-docs) |
| Acceptance gates | [`#acceptance-gates`](#acceptance-gates) |

## Stage-to-anchor map

| Stage | Anchor | Use |
|---|---|---|
| Stage 1 | [`#stage-1-planner-review`](#stage-1-planner-review) | Planner-owned base rules |
| Stage 2 | [`#stage-2-first-orc-nav-pass`](#stage-2-first-orc-nav-pass) | Allowed writes, outputs, stop point |
| Stage 3 | [`#stage-3-one-battle-plan-human-approval`](#stage-3-one-battle-plan-human-approval) | One battle plan only |
| Stage 4 | [`#stage-4-remaining-local-docs`](#stage-4-remaining-local-docs) | Remaining local docs |
| Stage 5 | [`#stage-5-fresh-tiny-docs-only-pilot`](#stage-5-fresh-tiny-docs-only-pilot) | Fresh proof |
| Stage 6 | [`#stage-6-repo-level-alignment-wave`](#stage-6-repo-level-alignment-wave) | Fixed repo-level scope |

## Gate-to-anchor map

| Gate | Anchor | Check |
|---|---|---|
| Gate 1 | [`#gate-1-planner-base-accepted`](#gate-1-planner-base-accepted) | Planner base accepted |
| Gate 2 | [`#gate-2-grill-me-passed`](#gate-2-grill-me-passed) | Pre-Orc grill-me passed |
| Gate 3 | [`#gate-3-nav-pass-accepted`](#gate-3-nav-pass-accepted) | Stage 2 nav pass accepted |
| Gate 4 | [`#gate-4-battle-plan-approved`](#gate-4-battle-plan-approved) | Battle plan approved |
| Gate 5 | [`#gate-5-local-docs-accepted`](#gate-5-local-docs-accepted) | Local docs accepted |
| Gate 6 | [`#gate-6-fresh-pilot-accepted`](#gate-6-fresh-pilot-accepted) | Fresh tiny pilot accepted |
| Gate 7 | [`#gate-7-repo-alignment-accepted`](#gate-7-repo-alignment-accepted) | Repo-level alignment accepted |

## Role-boundary anchors

- Planner boundary: [`#planner-role-boundaries`](#planner-role-boundaries)
- Planner-owned vs Orc-owned artifacts: [`#planner-owned-vs-orc-owned-artifacts`](#planner-owned-vs-orc-owned-artifacts)
- Stage 2 allowed writes: [`#stage-2-allowed-writes`](#stage-2-allowed-writes)
- Stage 2 forbidden writes: [`#stage-2-forbidden-writes`](#stage-2-forbidden-writes)
- Mandatory grill-me gate: [`#mandatory-grill-me-gate`](#mandatory-grill-me-gate)
- Final operating rule: [`#final-operating-rule`](#final-operating-rule)

## Maintenance rule

- Keep this file short.
- Add anchors only when they materially improve retrieval.
- Do not mirror full prose from `plan_full`.
- If `plan_full` changes materially, re-audit this index before next Orc run.

## Last anchor audit

- Date: 2026-06-01
- Auditor: `Orc`
- Result: existing `plan_full` anchors, `Quick navigation`, and `Anchor map` were sufficient for `Stage 2`.
- `plan_full` edits needed: none.
