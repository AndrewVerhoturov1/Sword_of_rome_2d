# {Subproject Title} Plan Index

Slug: `{subproject_slug}`  
Target file: `{subproject_slug}_plan_full.md`  
Owner: `Orc`  
Audience: agents  
Status: `draft`  
Last updated: `YYYY-MM-DD`

> Этот file — agent-oriented retrieval map. Он не является human README и не должен дублировать весь `plan_full`.

## Purpose

Помочь агенту быстро найти нужные anchors в `{subproject_slug}_plan_full.md`.

## Audience and non-goals

Audience:

```text
agents, reviewers, Orc execution sessions
```

Non-goals:

- не объяснять всё человеку простым языком;
- не заменять `readme`;
- не заменять `navigation`;
- не заменять `plan_full`;
- не становиться journal/status/decisions.

## Index rule

- Использовать semantic anchors, а не line numbers.
- Если anchor не проверен, помечать `provisional`.
- Если `plan_full` изменился, провести anchor audit.
- Не делать claims о sections, которые не были открыты/проверены.

## Fast anchor table

| Need | Anchor in `plan_full` | Status |
|---|---|---|
| Purpose | `#purpose` | `provisional` |
| Non-goals | `#non-goals-and-forbidden-drifts` | `provisional` |
| Source basis | `#source-basis-and-authority-order` | `provisional` |
| Role boundaries | `#role-boundaries` | `provisional` |
| Artifact model | `#artifact-model` | `provisional` |
| Lifecycle | `#lifecycle-overview` | `provisional` |
| Allowed writes | `#allowed-writes` | `provisional` |
| Forbidden writes | `#forbidden-writes` | `provisional` |
| Human gates | `#human-gates` | `provisional` |
| Acceptance criteria | `#acceptance-criteria` | `provisional` |

## Stage-to-anchor map

| Stage | Main anchor | Notes |
|---|---|---|
| Stage 1 | `#lifecycle-overview` | Planner review / base acceptance |
| Stage 2 | `#lifecycle-overview` | First Orc nav pass |
| Stage 3 | `#lifecycle-overview` | Battle plan and approval |
| Stage 4 | `#lifecycle-overview` | Local docs/execution slice |
| Stage 5 | `#lifecycle-overview` | Optional future proof/follow-up |
| Stage 6 | `#lifecycle-overview` | Optional repo-level alignment |

## Gate-to-anchor map

| Gate | Anchor | Human role |
|---|---|---|
| Plan accepted | `#human-gates` | approve or request edits |
| Orc start allowed | `#human-gates` | approve route |
| Execution slice accepted | `#acceptance-criteria` | accept or request fixes |
| Scope change | `#stop-rules` | decide |

## Role-boundary anchors

| Boundary | Anchor |
|---|---|
| Planner does strategy | `#role-boundaries` |
| Orc does execution evidence | `#role-boundaries` |
| Human approves gates | `#human-gates` |
| Agent recommendation != human approval | `#human-gates` |

## Maintenance rule

Update when `plan_full` anchors, lifecycle, gates or source sections change. Do not update this file as a substitute for changing `plan_full`.
