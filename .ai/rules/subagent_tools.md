# Subagent Tools

> **Legacy note:** Originally created for the closed `B1/BOS/block-orchestration` system (`Subproject -> Boss -> Block Orchestrator -> task planning`). The tool names themselves (`V1-Синтез`, `V3-Ревью`, `Kilo`, `Субагент-микро`) remain usable as optional tools for Planner or Orc, but the old block-orchestration framing is legacy/history only. Active route: `Planner -> Orc documentation-driven subproject execution`.

## Status

Optional tool reference for Planner/Orc subproject execution. Not a global routing document for the whole repo.

## Purpose

Defines a small named set of external tools that Planner or Orc can use when planning or executing subproject tasks. Use one explicit tool name per task instead of vague combinations.

## Scope

This rule applies to:

- Planner/Orc subproject task planning
- similar workflow docs where one concrete task needs one primary execution tool

This rule does not define the whole repo routing model. It is not tied to the old Boss/B1 hierarchy.

## Canonical Tool Set

Use exactly these four names for now:

1. `V1-Синтез`
2. `V3-Ревью`
3. `Kilo`
4. `Субагент-микро`

Do not add `V2` here yet.

## Classification

These are external tools usable by Planner or Orc.

Meaning:

- Planner or Orc selects tool per task;
- each task should have one primary tool;
- if no tool fits honestly, return `Blocked / Clarification Request`.

## Tool Definitions

### `V1-Синтез`

Short meaning:
external `V1` answer first, then subagent turns it into usable local output.

Use when:

- task is about naming;
- critique;
- documentation design;
- workflow clarity;
- second opinion;
- text structure or document draft shape.

Do not use when:

- local repo facts must be verified;
- files must be edited directly as main work;
- diff/test/debug is required;
- task depends on local authority.

Strengths:

- good for external thinking and critique;
- good for naming and structure;
- cheaper and lighter than artifact-heavy routes.

Limits:

- external answer is not repo authority;
- subagent must still verify and assemble result locally.

### `V3-Ревью`

Short meaning:
strong external draft or artifact first, then subagent verifies and makes only small local corrections.

Use when:

- document is important;
- strong first draft is valuable;
- artifact-style output is useful;
- subagent review should be verification-first, not full rewrite.

Do not use when:

- there is no external V3 draft/artifact yet;
- expected local rewrite is large;
- task is mainly debug/test/diff work;
- result cannot be verified after import or transfer.

Strengths:

- best baseline for important documentation;
- strong first-pass quality;
- good fit for artifact-producing workflows.

Limits:

- "minor fix" must stay minor;
- external artifact claims still need local verification;
- must not be confused with `/v3 import-entry route`.

### `Kilo`

Short meaning:
local repo-grounded executor.

Use when:

- local files must be read or changed;
- diff matters;
- tests matter;
- debug matters;
- local verification is required;
- runner/debugger/verifier behavior is needed.

Do not use when:

- task is mainly naming or external critique;
- there is no need for local repo authority;
- task is so small that tool overhead is bigger than the task itself.

Strengths:

- local repo authority;
- file edits;
- verification;
- debug/test flow.

Limits:

- heavier than tiny direct work;
- requires correct handoff/mode usage;
- do not confuse Kilo mode with task role.

### `Субагент-микро`

Short meaning:
tiny direct subagent work without calling a larger tool.

Use when:

- task is very small;
- repo risk is low;
- no tests are needed;
- no serious local verification is needed;
- separate tool overhead is larger than the work.

Examples:

- shorten one label;
- adjust one sentence;
- add one tiny table;
- normalize one already-understood wording;
- make one tiny documentation correction.

Do not use when:

- task is important;
- task changes risky repo state;
- local facts must be proven;
- tests/debug are needed;
- architectural choice is involved;
- direct work would become the default instead of an exception.

Strengths:

- fast;
- low overhead;
- useful for small safe edits.

Limits:

- weakest traceability;
- easiest tool to abuse;
- never use as default route.

## Selection Cheat Sheet

| Situation | Tool |
|---|---|
| Need external critique, naming, design help | `V1-Синтез` |
| Need important document or strong artifact draft | `V3-Ревью` |
| Need local repo work, diff, tests, verification | `Kilo` |
| Need very small safe direct edit | `Субагент-микро` |

## Required Task Field

Planner/Orc task docs should use this field:

```md
Subagent Tool: `V3-Ревью`
Reason: important workflow document; strong external draft useful; local pass should stay review-first
```

Allowed values are only:

- `V1-Синтез`
- `V3-Ревью`
- `Kilo`
- `Субагент-микро`

## V3 Distinction

### `V3-Ревью`

This is a planning/tool-selection label for a task:

- strong V3-produced draft or artifact;
- subagent verifies;
- subagent makes only limited local corrections.

### `/v3 import-entry route`

This is a workflow route:

- explicit `/v3` entry;
- existing V3 artifact package;
- import through `Kilo Notebook V3`;
- package/journal/import contract rules apply.

Rule:

Do not treat these as the same thing.

`V3-Ревью` describes how a task is executed conceptually.
`/v3 import-entry route` describes how a V3 package enters the repo workflow.

## Hard Boundaries

- Do not add new tools without explicit decision.
- Do not rename `Kilo`.
- Do not treat `Субагент-микро` as default route.
- Do not accept external answers as repo facts without local verification.
- Do not use this document as a global routing replacement for the whole repo.
- Do not choose multiple primary tools for one task unless a task is explicitly decomposed.

## Out Of Scope

This document does not yet define:

- full `/r1` published external route;
- full `/v2` external senior review;
- full V3 import contract;
- `Kilo Recorder`;
- `Kilo Notebook`;
- global repo-wide routing policy outside block task planning.
