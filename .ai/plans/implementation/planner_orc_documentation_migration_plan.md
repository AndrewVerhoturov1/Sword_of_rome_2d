# Planner -> Orc Documentation Migration Plan

## Status

`draft_for_import`

This document is a migration plan only. It does not modify the repository by itself, does not claim that the migration has already been applied, and does not continue the old `B1/BOS/block-orchestration` hierarchy as an active route.

The active target system is:

```text
Subproject documentation
  <- prepared and maintained by Planner
  <- executed and updated by Orc
  <- supported by V1 / V2 / V3 / Kilo as tools only
```

The legacy source system is:

```text
Subproject -> Planning Chat -> Task Control Pack -> Boss Orchestrator -> B1 Block Chats -> Junior Orchestrators
```

## Intent

Migrate the documentation layer from the legacy `B1/BOS/block-orchestration` system to the accepted `Planner -> Orc` documentation-driven subproject execution system.

The migration must be file-level and operational:

- identify which existing files should be updated in place;
- identify which files should be marked as legacy/history;
- identify which files remain active;
- remove legacy Boss/B1 files from default required-reading routes;
- define the minimum new active documentation files needed for Planner -> Orc;
- replace old terminology in active workflow docs without rewriting historical archive content as if it never existed.

This plan intentionally does not perform product implementation work and does not create code tasks.

## Source Basis

This plan is based on the following repository context at commit `591e96190cb610779102e3122f887d64899998d9`.

### Primary source inventory

- `.ai/reports/0043_b1_bos_legacy_inventory_report.md`
  - Role in this migration: source inventory of old B1/BOS traces.
  - It identifies:
    - 11 direct legacy system files under `.ai/subprojects/SP-20260530-b1-boss-rollout/`;
    - 10 mention-only files that refer to the old system but are not themselves direct system artifacts;
    - the old system status as `closed_by_user`.
  - Important boundary: Report 0043 is not the migration plan. It is the map of legacy traces that this migration plan uses.

### Accepted replacement system

- `ideas/subproject_single_execution_chat_documentation_system_v2.md`
  - Role in this migration: accepted replacement model.
  - Key target idea: one subproject has one documentation folder and one main execution chat.
  - It explicitly rejects separate B1 block folders as the active route.
  - In this plan the roles are named:
    - `Planner` — prepares and maintains the planning/documentation route;
    - `Orc` — the single main execution chat that works through the subproject documentation.

### Legacy design source

- `ideas/hierarchical_ai_development_system_with_subproject.md`
  - Role in this migration: legacy idea/design source.
  - It should remain readable as history, but must not be used as the active workflow canon.

### Active repo workflow and navigation sources

- `AGENTS.md`
  - Role in this migration: repo-level workflow contract that currently contains block-orchestration wording and must be updated.
- `.ai/repo_navigation.md`
  - Role in this migration: repo reading route and navigation layer that currently exposes the old rollout slice as active-looking navigation.
- `.ai/project_state.md`
  - Role in this migration: project status surface that should eventually mention the workflow migration state after it is actually applied.
- `.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md`
  - Role in this migration: old master rollout plan for the legacy route.
- `.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md`
  - Role in this migration: old short working plan for the legacy route.
- `.ai/plans/implementation/boss_orchestrator_bootstrap.md`
  - Role in this migration: old Boss bootstrap document.
- `.ai/v3/V3_navigation.md`
  - Role in this migration: V3 lifecycle index only. It should not be edited by this package and should not be treated as the Planner -> Orc workflow source.

## Target Documentation Model

The target model is not a multi-level Boss/B1 hierarchy.

The target model is:

```text
Planner
  prepares the subproject documentation route
  defines scope, plan, context, checkpoints, and next execution step
  keeps required context small and explicit
  does not create B1 block folders as the normal execution unit

Orc
  is the one main execution chat for the subproject
  reads the current subproject docs
  performs the next approved execution slice
  updates progress/status through documentation
  calls Kilo, V1, V2, V3, or external review only as tools

Subproject documentation
  is the external memory of Planner and Orc
  stores current state, plan, context map, decisions, progress reports, and checkpoints
  replaces the old Boss/B1 execution tree as the active route
```

Practical target rule:

```text
One active subproject = one documentation folder + one main Orc execution route.
No active B1 block folder tree.
No active Boss layer above Orc.
No Junior Orchestrator layer as a default process.
```

## Migration Goals

1. Make `Planner -> Orc` the only active documentation-driven subproject execution route.
2. Preserve the old B1/BOS material as history, not as active workflow canon.
3. Remove old Boss/B1 files from default required context.
4. Keep Report 0043 as the inventory map for legacy traces.
5. Update active docs so future agents do not continue the closed B1/BOS route.
6. Avoid rewriting historical documents in a misleading way.
7. Avoid deleting legacy artifacts unless a later human-approved cleanup explicitly asks for deletion.
8. Keep migration limited to workflow documentation.
9. Keep V3 import mechanics separate from Planner -> Orc workflow mechanics.
10. Give Kilo/Codex/human reviewers concrete file-level checkpoints.

## File-by-File Migration Map

### Summary Table

| Path | Current role | Migration action | Notes |
|---|---|---|---|
| `.ai/plans/implementation/planner_orc_documentation_migration_plan.md` | New migration plan | Create | This file. It is the only project file in the V3 package. |
| `AGENTS.md` | Active repo workflow contract | Update existing file | Replace active block-orchestration contract with Planner -> Orc contract. Do not edit in this package. |
| `.ai/repo_navigation.md` | Active navigation / required reading map | Update existing file | Move old rollout slice to legacy/history wording; add Planner -> Orc active route after actual migration. |
| `.ai/project_state.md` | Active project status surface | Update existing file later | Add workflow migration status only after actual migration is applied. |
| `ideas/subproject_single_execution_chat_documentation_system_v2.md` | Accepted replacement idea | Keep active as source basis | Eventually promote/summarize into `.ai/` workflow docs; do not treat as legacy. |
| `ideas/hierarchical_ai_development_system_with_subproject.md` | Old B1/BOS idea design | Mark as legacy | Keep as historical design source, not required active context. |
| `.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md` | Old B1/BOS rollout master plan | Mark as legacy | Do not continue as active roadmap. |
| `.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md` | Old B1/BOS working plan | Mark as legacy | Superseded by Planner -> Orc migration and future active working docs. |
| `.ai/plans/implementation/boss_orchestrator_bootstrap.md` | Old Boss bootstrap | Mark as legacy | Remove from default inputs. |
| `.ai/reports/0043_b1_bos_legacy_inventory_report.md` | Legacy inventory report | Keep active as inventory source | It is evidence/inventory, not active workflow route. |
| `.ai/subprojects/SP-20260530-b1-boss-rollout/` | Direct legacy system artifacts | Mark as legacy/archive | Do not use as template for active subprojects. |
| `.ai/external_chats/V1_navigation.md` | V1 history index | Keep as history | Do not rewrite history; do not make it required context for Planner -> Orc. |
| `.ai/external_chats/notebook/...053908...md` | V1 historical synthesis | Keep as history | No active required context. |
| `.ai/external_chats/notebook/...214445...md` | V1 historical grounded design | Keep as history | No active required context. |
| `.ai/v3/V3_navigation.md` | V3 lifecycle index | Keep active for V3 only | Do not update in this package; update only when actual V3 import lifecycle requires it. |
| `.ai/rules/subagent_tools.md` | Block workflow tool naming doc, if present | Update or mark legacy depending on contents | Convert to Planner/Orc tool-use rules or mark old B1-only parts legacy. |
| `.ai/prompts/` entries that mention block orchestration | Prompt layer | Update existing files later | Remove Boss/B1 default route from active prompts. |
| `.ai/templates/` entries that mention block plan/report/package | Template layer | Update or mark legacy later | Do not use B1 templates for active Planner -> Orc subprojects. |

## Update Existing Files

These are files that should remain active, but need wording and required-context changes.

### 1. `AGENTS.md`

Current issue:

- Report 0043 identifies `AGENTS.md` as a mention-only file because it contains active-looking block orchestration sections such as:
  - `Role separation for block orchestration`;
  - `Runtime block orchestration operating contract`;
  - mentions of `Block Orchestrator Chat`;
  - mentions of `Block Orchestrator Package`.

Required migration action:

1. Add a short status note near the relevant workflow section:

   ```text
   Status: legacy B1/BOS block-orchestration route is closed and must not be used as the active execution route.
   Active route: Planner -> Orc documentation-driven subproject execution.
   ```

2. Replace active Boss/B1 role separation with Planner -> Orc role separation.

3. Replace any default instruction that tells an agent to launch a Boss, B1 Block Chat, Junior Orchestrator, Block Orchestrator Package, or Task Control Pack as the normal route.

4. Preserve historical references only if they are clearly labelled:

   ```text
   Legacy/history only: Boss/B1/block-orchestration artifacts from SP-20260530-b1-boss-rollout.
   ```

5. Add active contract text:

   ```text
   Planner prepares the subproject docs and next execution route.
   Orc is the single main execution chat for the subproject.
   V1/V2/V3/Kilo are tools, not permanent hierarchy layers.
   Required context must be explicit, small, and stored in the subproject docs.
   ```

6. Ensure `AGENTS.md` does not list the old Boss/B1 documents as default required inputs.

Suggested replacement section title:

```text
## Planner -> Orc documentation-driven subproject execution
```

Do not title the active section:

```text
## Runtime block orchestration operating contract
```

unless it is explicitly moved under legacy/history.

### 2. `.ai/repo_navigation.md`

Current issue:

- It contains a `Subproject Rollout Slice` that points to `SP-20260530-b1-boss-rollout` and its block artifacts.
- It also lists recent additions that frame `subagent_tools.md`, `boss_orchestrator_bootstrap.md`, and the old working plan as part of the active workflow layer.
- This can mislead new agents into continuing the old route.

Required migration action:

1. Add a new navigation subsection:

   ```text
   ## Planner -> Orc Active Workflow
   ```

2. Under that subsection, eventually link to:
   - the accepted replacement design source until promoted:
     - `ideas/subproject_single_execution_chat_documentation_system_v2.md`;
   - this migration plan:
     - `.ai/plans/implementation/planner_orc_documentation_migration_plan.md`;
   - any future canonical Planner/Orc workflow documents created by a later task.

3. Rename or move `Subproject Rollout Slice` under a clearly legacy section:

   ```text
   ## Legacy / Historical Workflow Experiments
   ```

4. Add a warning near `SP-20260530-b1-boss-rollout`:

   ```text
   Legacy only. Closed B1/BOS rollout artifact. Do not use as active subproject template.
   ```

5. Remove old Boss/B1 links from any "External Start Here", "Reading Order", or "Recent Additions" position that looks like required active context.

6. Keep V3 navigation separate. V3 is an artifact import workflow, not the Planner -> Orc execution model.

### 3. `.ai/project_state.md`

Current issue:

- The file is the high-level state surface.
- It should not claim migration completion until a later Kilo/Codex/human cycle actually applies the doc changes.

Required migration action after actual migration is applied:

1. Add a short workflow-state note:

   ```text
   Workflow documentation note:
   Legacy B1/BOS block-orchestration route is closed.
   Active subproject documentation route is Planner -> Orc.
   ```

2. Do not add this as completed until the active docs have actually been updated.

3. Do not mix this workflow migration with product-code status such as `table-sandbox/` implementation state.

### 4. `.ai/rules/subagent_tools.md` if present

Current issue:

- `.ai/repo_navigation.md` describes this file as a canonical per-task tool set for block workflow with `V1-Синтез`, `V3-Ревью`, `Kilo`, and `Субагент-микро`.
- If the file is still framed around B1/block workflow, it can keep the old hierarchy alive by terminology.

Required migration action:

1. If the tools are still useful, keep them as tools for Planner/Orc, not as B1 subagent hierarchy.
2. Replace framing such as:

   ```text
   tools used by B1 block orchestrator
   ```

   with:

   ```text
   optional external tools used by Planner or Orc
   ```

3. Preserve any useful distinction between V1/V2/V3/Kilo, but remove the claim that they belong to a default B1/Boss route.
4. If the whole file only makes sense for old block workflow, mark it legacy instead of updating.

### 5. `.ai/prompts/` active prompts that mention block orchestration

Current issue:

- `.ai/repo_navigation.md` describes `.ai/prompts/` as containing prompts for handoff, external request, and block orchestration.
- Active prompts must not keep producing Boss/B1 artifacts by default.

Required migration action:

1. Search active prompt files for:
   - `Boss Orchestrator`;
   - `B1`;
   - `Block Orchestrator`;
   - `block orchestration`;
   - `Task Control Pack`;
   - `BLOCK_PLAN`;
   - `BLOCK_REPORT`;
   - `ORCHESTRATOR_PACKAGE`;
   - `Junior Orchestrator`.

2. For each active prompt:
   - replace active Boss/B1 route with Planner -> Orc route;
   - keep old terms only in explicit legacy/history context;
   - ensure new V3 requests for workflow docs do not ask external chats to continue B1/BOS.

3. Do not edit `.ai/v3/prompts/` as part of this migration unless a separate V3 contract task explicitly asks for it. The current package forbids touching `.ai/v3/prompts/`.

### 6. `.ai/templates/` active templates that mention block artifacts

Current issue:

- Existing templates may produce block plans, block reports, or orchestrator packages for the old route.
- These templates should not remain the default for active Planner -> Orc work.

Required migration action:

1. Search active templates for:
   - `BLOCK_PLAN`;
   - `CONTEXT_PACK`;
   - `ORCHESTRATOR_PACKAGE`;
   - `BLOCK_ORCHESTRATOR_PROMPT`;
   - `BLOCK_REPORT`;
   - `TASK_CONTROL_PACK`;
   - `Boss`.

2. For each template:
   - mark old B1-only templates as legacy, or
   - create replacement Planner/Orc templates in a later task.

3. Do not delete templates during the first migration pass unless human explicitly approves cleanup.

## Mark as Legacy

These files should remain readable for audit/history, but must not be active required context.

### 1. Direct legacy system files from Report 0043

Mark all files under this legacy subproject as archive/history:

```text
.ai/subprojects/SP-20260530-b1-boss-rollout/SUBPROJECT_STATE.md
.ai/subprojects/SP-20260530-b1-boss-rollout/SHORT_PLAN.md
.ai/subprojects/SP-20260530-b1-boss-rollout/TASK_CONTROL_PACK.md
.ai/subprojects/SP-20260530-b1-boss-rollout/BOSS_BOOTSTRAP.md
.ai/subprojects/SP-20260530-b1-boss-rollout/BLOCKS_INDEX.md
.ai/subprojects/SP-20260530-b1-boss-rollout/SYSTEM_CLOSURE.md
.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md
.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md
.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/ORCHESTRATOR_PACKAGE.md
.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_ORCHESTRATOR_PROMPT.md
.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/BLOCK-001-task-control-pack-smoke/BLOCK_REPORT.md
```

Required legacy label:

```text
Legacy B1/BOS artifact.
Status: closed_by_user.
Do not use this file as the active Planner -> Orc template.
Kept for history, audit, and migration trace only.
```

Operational note:

- Do not rewrite all these files immediately if that creates too much churn.
- Minimum acceptable first pass: navigation and active required-context files must clearly mark the whole folder as legacy.
- A later cleanup pass may add file headers if human approves.

### 2. Old idea/design source

Path:

```text
ideas/hierarchical_ai_development_system_with_subproject.md
```

Required action:

- Mark as legacy idea/design source.
- Do not delete.
- Do not use as default context.
- Link to the accepted replacement system.

Suggested header if edited later:

```text
> Legacy note:
> This document describes the older Boss/B1 hierarchical workflow idea.
> It has been superseded as the active route by Planner -> Orc documentation-driven subproject execution.
> Keep for history only.
```

### 3. Old rollout master plan

Path:

```text
.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md
```

Required action:

- Mark as legacy rollout plan.
- Do not continue its phases as the active route.
- Keep it as historical context only.

Suggested status line if edited later:

```text
Status: legacy / superseded as active workflow route.
Superseded by: Planner -> Orc documentation-driven subproject execution.
```

### 4. Old short working plan

Path:

```text
.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md
```

Required action:

- Mark as legacy working plan.
- Do not use as current implementation plan.
- Keep as historical record of the old rollout attempt.

### 5. Old Boss bootstrap

Path:

```text
.ai/plans/implementation/boss_orchestrator_bootstrap.md
```

Required action:

- Mark as legacy.
- Remove from default input lists.
- Do not start new Boss sessions from it.

### 6. Mention-only V1 notebook entries

Paths from Report 0043:

```text
.ai/external_chats/V1_navigation.md
.ai/external_chats/notebook/2026-05-30_V1-20260530-053908_follow-up-synthesis-po-rollout-plan-v1-20260530.md
.ai/external_chats/notebook/2026-05-30_V1-20260530-214445_grounded-design-dlya-dokumenta-ob-instrumentah-subagenta-vnutri.md
```

Required action:

- Keep as history.
- Do not rewrite old notebook entries.
- Do not include them in active Planner -> Orc required context unless doing historical audit.

## Keep Active

These files or layers should remain active, with the boundaries below.

### 1. `ideas/subproject_single_execution_chat_documentation_system_v2.md`

Keep active as the accepted replacement design source.

Boundary:

- It is accepted design input.
- It is not yet the operational migration plan by itself.
- It should eventually be promoted or summarized into active `.ai/` workflow docs.

### 2. `.ai/reports/0043_b1_bos_legacy_inventory_report.md`

Keep active as inventory evidence.

Boundary:

- It is not a workflow route.
- It should be cited when explaining why specific old files are being marked legacy.
- It should not be used to launch new B1/BOS work.

### 3. `.ai/v3/` workflow

Keep active for V3 artifact package lifecycle only.

Boundary:

- V3 remains an artifact-producing/import workflow.
- V3 is not the Planner -> Orc execution model.
- This task does not update `.ai/v3/V3_navigation.md`, does not create a journal, and does not run Kilo import.

### 4. Repo project/product docs

Keep active and mostly untouched by this migration:

```text
README.md
canon/
references/
docs/
table-sandbox/
src/ if any
```

Boundary:

- This migration is workflow-docs only.
- Do not mix product roadmap or code implementation with the workflow migration.

## Remove from Required Context

The following should be removed from default required-reading routes for new active work.

### Remove from Planner -> Orc default context

```text
ideas/hierarchical_ai_development_system_with_subproject.md
.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md
.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md
.ai/plans/implementation/boss_orchestrator_bootstrap.md
.ai/subprojects/SP-20260530-b1-boss-rollout/
.ai/subprojects/SP-20260530-b1-boss-rollout/blocks/
```

These may be read only for:

- historical audit;
- migration validation;
- comparing old and new route;
- debugging a legacy reference.

### Remove from default agent startup

Do not tell new agents to start from:

```text
Boss Orchestrator Bootstrap
Task Control Pack
BLOCKS_INDEX
BLOCK_PLAN
CONTEXT_PACK
ORCHESTRATOR_PACKAGE
BLOCK_ORCHESTRATOR_PROMPT
BLOCK_REPORT
```

for active Planner -> Orc work.

### Keep in limited context only

`Report 0043` may remain in required context for this migration task, but not for every future Orc execution task.

Future active Orc tasks should usually read:

```text
AGENTS.md
.ai/repo_navigation.md
.ai/project_state.md
current subproject documentation folder
current Planner handoff / current execution plan
only the specific V1/V2/V3/Kilo artifacts needed for the current slice
```

## Create New Files

This V3 package creates only one project file:

```text
.ai/plans/implementation/planner_orc_documentation_migration_plan.md
```

That is intentional and required by the V3 request.

Later migration tasks may create additional files, but they must be separate tasks and should not be bundled into this package.

### Recommended future active Planner -> Orc files

A later Kilo task should create or update a minimal active documentation route. Suggested files:

```text
.ai/subprojects/<SP-ID>/SUBPROJECT_STATE.md
.ai/subprojects/<SP-ID>/PLANNER_HANDOFF.md
.ai/subprojects/<SP-ID>/ORC_EXECUTION_LOG.md
.ai/subprojects/<SP-ID>/CONTEXT_INDEX.md
.ai/subprojects/<SP-ID>/DECISIONS.md
.ai/subprojects/<SP-ID>/CHECKPOINTS.md
```

Alternative names are acceptable if the repo chooses a different naming convention, but the structure should preserve these functions:

| Needed function | Suggested file | Purpose |
|---|---|---|
| Current durable state | `SUBPROJECT_STATE.md` | ID, status, owner model, current phase, accepted route |
| Planner output | `PLANNER_HANDOFF.md` | Scope, next slice, allowed files, required context, gates |
| Orc progress memory | `ORC_EXECUTION_LOG.md` | Compact execution notes, reports, handbacks |
| Required context control | `CONTEXT_INDEX.md` | What to read by default vs escalation only |
| Decision memory | `DECISIONS.md` | Accepted/rejected decisions with dates |
| Human/Codex gates | `CHECKPOINTS.md` | Review points and pass/fail criteria |

Important:

- Do not create B1 block folders as the default structure.
- Do not create `BOSS_BOOTSTRAP.md` for active Planner -> Orc work.
- Do not create `BLOCKS_INDEX.md` for active Planner -> Orc work.
- Do not create `ORCHESTRATOR_PACKAGE.md` as the default handoff artifact.

## Terminology Replacements

Use this table when updating active workflow docs.

| Legacy term | Active replacement | Rule |
|---|---|---|
| `Boss Orchestrator` | `Orc` or `legacy Boss Orchestrator` | Use `Orc` for the active execution role. Use `legacy Boss Orchestrator` only when discussing old files. |
| `B1 Block Chat` | `Orc execution slice` | Do not create separate B1 chat/folder by default. |
| `Junior Orchestrator` | `optional external tool/reviewer` | Do not keep as a permanent hierarchy layer. |
| `Task Control Pack` | `Planner Handoff` or `Subproject Execution Handoff` | The Planner hands Orc a compact executable context. |
| `Block Plan` | `Execution slice plan` | A slice belongs inside the subproject docs, not a B1 block folder. |
| `Block Report` | `Orc execution report` | Report progress back into the subproject documentation. |
| `Block Orchestrator Package` | `Orc handoff package` | Only if packaging is needed; otherwise use current subproject docs. |
| `BLOCKS_INDEX.md` | `CHECKPOINTS.md` / `CONTEXT_INDEX.md` / `ORC_EXECUTION_LOG.md` | Split the useful functions without preserving B1 block-tree semantics. |
| `B1` as active layer | No active equivalent | Use only in legacy/history context. |
| `B1/BOS` | `legacy B1/BOS` | Never present as an active route. |
| `block orchestration` | `Planner -> Orc execution` | Use for active workflow. |
| `Subproject -> Boss -> B1` | `Subproject -> Planner -> Orc` | Canonical active route. |
| `subagent` as default execution unit | `tool call`, `external review`, or `helper process` | Only use if optional and explicitly bounded. |
| `package gate` in old B1 sense | `Planner handoff gate` or `human/Codex checkpoint` | Keep the quality-control idea, remove the B1 route. |

### Replacement examples

Legacy wording:

```text
The Boss Orchestrator creates a Task Control Pack and delegates B1 blocks to Junior Orchestrators.
```

Active wording:

```text
Planner prepares a compact handoff. Orc executes the next approved slice using the subproject documentation as external memory. V1/V2/V3/Kilo may be called as tools when explicitly needed.
```

Legacy wording:

```text
Create BLOCK-001 and launch a Block Orchestrator Chat.
```

Active wording:

```text
Add the next execution slice to the subproject docs and let Orc continue from the current Planner handoff.
```

Legacy wording:

```text
B1 is the active layer for block execution.
```

Active wording:

```text
The legacy B1 layer is closed. Active execution uses Planner -> Orc.
```

## Required Context Cleanup

The migration must clean not only files, but also reading routes.

### Current problem

The old system can remain alive accidentally if agents keep receiving old required context such as:

```text
hierarchical_ai_development_system_with_subproject.md
hierarchical_subproject_workflow_rollout_plan.md
hierarchical_subproject_workflow_work_plan.md
boss_orchestrator_bootstrap.md
SP-20260530-b1-boss-rollout/
BLOCK_PLAN.md
CONTEXT_PACK.md
ORCHESTRATOR_PACKAGE.md
BLOCK_ORCHESTRATOR_PROMPT.md
```

### Target required context for Planner

Planner should normally read:

```text
AGENTS.md
.ai/repo_navigation.md
.ai/project_state.md
ideas/subproject_single_execution_chat_documentation_system_v2.md
.ai/plans/implementation/planner_orc_documentation_migration_plan.md only while migration is in progress
current subproject docs
current user request / current task
```

Planner may read Report 0043 only when working on this migration or auditing legacy traces.

### Target required context for Orc

Orc should normally read:

```text
AGENTS.md
.ai/repo_navigation.md
.ai/project_state.md
current subproject/SUBPROJECT_STATE.md
current subproject/PLANNER_HANDOFF.md
current subproject/CONTEXT_INDEX.md
current subproject/CHECKPOINTS.md
only the specific files needed for the current execution slice
```

Orc should not read legacy B1/BOS files by default.

### Target required context for V3

V3 should remain separate:

```text
.ai/v3/contracts/
.ai/v3/templates/
.ai/v3/prompts/
.ai/v3/V3_navigation.md
```

Only use these when the task is specifically a V3 artifact workflow.

Do not confuse:

```text
V3 artifact-producing workflow
```

with:

```text
Planner -> Orc subproject execution workflow
```

## Migration Order

### Phase 0 — Import this migration plan

Goal:

- Add this single plan file to the repo through the V3 import route when the user explicitly runs Kilo import.

Allowed result:

```text
.ai/plans/implementation/planner_orc_documentation_migration_plan.md
```

Not allowed in this phase:

- editing `AGENTS.md`;
- editing `.ai/repo_navigation.md`;
- editing `.ai/v3/V3_navigation.md`;
- creating a journal inside this package;
- modifying product code;
- creating multiple project files.

### Phase 1 — Update active workflow contract first

Files:

```text
AGENTS.md
```

Actions:

1. Add Planner -> Orc as the active workflow route.
2. Mark B1/BOS block orchestration as legacy/closed.
3. Remove Boss/B1 documents from default required inputs.
4. Keep useful tool roles as optional tools, not hierarchy levels.

Gate:

- A new agent reading only `AGENTS.md` must not conclude that Boss/B1 is the active route.

### Phase 2 — Update navigation / reading route

Files:

```text
.ai/repo_navigation.md
```

Actions:

1. Add active Planner -> Orc navigation.
2. Move the old Subproject Rollout Slice to legacy/history.
3. Remove old Boss/B1 docs from active "Recent Additions" framing.
4. Keep V3 as V3 lifecycle only.

Gate:

- A new external chat reading `.ai/repo_navigation.md` must know that:
  - Planner -> Orc is active;
  - B1/BOS is legacy;
  - Report 0043 is inventory only.

### Phase 3 — Mark old plans and old idea docs as legacy

Files:

```text
ideas/hierarchical_ai_development_system_with_subproject.md
.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md
.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md
.ai/plans/implementation/boss_orchestrator_bootstrap.md
```

Actions:

1. Add short legacy/superseded headers.
2. Link to the active replacement route.
3. Do not rewrite historical content.
4. Do not delete.

Gate:

- Search results may still find old terms, but each active-looking old plan has a visible legacy warning.

### Phase 4 — Handle direct legacy subproject artifacts

Files/folder:

```text
.ai/subprojects/SP-20260530-b1-boss-rollout/
```

Actions:

1. At minimum, ensure navigation marks the folder as legacy.
2. Optionally add a top-level legacy note to `SUBPROJECT_STATE.md` or `SYSTEM_CLOSURE.md`.
3. Do not use the folder as the template for future active subprojects.
4. Do not create new B1 blocks inside it.

Gate:

- No future active task should point to this folder as default context.

### Phase 5 — Create/promote active Planner -> Orc docs

Files:

```text
.ai/subprojects/<SP-ID>/SUBPROJECT_STATE.md
.ai/subprojects/<SP-ID>/PLANNER_HANDOFF.md
.ai/subprojects/<SP-ID>/ORC_EXECUTION_LOG.md
.ai/subprojects/<SP-ID>/CONTEXT_INDEX.md
.ai/subprojects/<SP-ID>/DECISIONS.md
.ai/subprojects/<SP-ID>/CHECKPOINTS.md
```

Actions:

1. Choose the first real active Planner -> Orc subproject.
2. Create only the minimal docs needed.
3. Keep context compact.
4. Do not create `blocks/` as the default route.
5. Add clear human/Codex gates.

Gate:

- The first active subproject can run without Boss/B1 documents.

### Phase 6 — Clean prompt/template layer

Files:

```text
.ai/prompts/
.ai/templates/
.ai/rules/subagent_tools.md if present
```

Actions:

1. Search for old terms.
2. Convert active prompts/templates to Planner -> Orc.
3. Mark old block templates legacy if keeping them.
4. Avoid touching `.ai/v3/` unless a separate V3 contract task requires it.

Gate:

- New generated handoffs should not ask for Boss/B1 active route by default.

### Phase 7 — Verification pass

Run a read-only search after edits are actually made.

Search terms:

```text
B1/BOS
Boss Orchestrator
Block Orchestrator
block orchestration
Task Control Pack
B1 Block
Junior Orchestrator
SP-20260530-b1-boss-rollout
BLOCK-001-task-control-pack-smoke
ORCHESTRATOR_PACKAGE
BLOCK_ORCHESTRATOR_PROMPT
```

For each result classify:

```text
active-ok
legacy-ok
needs-fix
false-positive
```

Gate:

- No `needs-fix` result remains in active workflow required context.

### Phase 8 — Human acceptance

Human check should be in plain Russian.

Suggested human check:

```text
Проверь, пожалуйста:
1. В активных правилах больше не написано, что надо запускать Boss/B1 как основной маршрут.
2. В навигации старая папка SP-20260530-b1-boss-rollout видна только как legacy/history.
3. Новый активный маршрут называется Planner -> Orc.
4. Старые документы не удалены, но больше не выглядят как инструкция к продолжению работы.
Ответь: "миграция документации выглядит верно" или укажи, что осталось исправить.
```

## Checkpoints and Gates

### Gate A — Package integrity

Pass conditions:

- V3 package contains exactly one project file.
- Project file path is:

  ```text
  .ai/plans/implementation/planner_orc_documentation_migration_plan.md
  ```

- No `.ai/v3/` file is included in the package.
- No product code is included.

### Gate B — Contract clarity

Pass conditions after Phase 1:

- `AGENTS.md` names Planner -> Orc as active.
- `AGENTS.md` labels Boss/B1 as legacy.
- `AGENTS.md` does not make B1/BOS required default context.

### Gate C — Navigation clarity

Pass conditions after Phase 2:

- `.ai/repo_navigation.md` points to Planner -> Orc as active.
- The old rollout slice is under legacy/history wording.
- Report 0043 is described as inventory, not active workflow.

### Gate D — Legacy containment

Pass conditions after Phase 3/4:

- Old idea and rollout docs have visible legacy markers.
- Direct legacy subproject artifacts are not used as templates.
- Old notebook entries remain history only.

### Gate E — Active route exists

Pass conditions after Phase 5:

- A minimal active Planner -> Orc subproject documentation folder exists.
- It has state, handoff/context, progress/reporting, decision, and checkpoint functions.
- It does not use B1 block folders as the default structure.

### Gate F — Search verification

Pass conditions after Phase 7:

- All old terms in active docs are either:
  - converted to Planner -> Orc, or
  - explicitly labelled legacy/history.
- No required-reading route still instructs agents to continue Boss/B1.

### Gate G — Human acceptance

Pass conditions:

- Human confirms that the documentation layer no longer presents old B1/BOS as active.
- Human confirms Planner -> Orc is understandable as the new route.

## Immediate Next Step

After this V3 package is received, the immediate next step is not to run product work and not to continue B1/BOS.

The immediate next step is:

```text
Import this single migration-plan file through the V3/Kilo route when the user explicitly starts import.
Then create a separate Kilo documentation task to update AGENTS.md and .ai/repo_navigation.md according to Phase 1 and Phase 2.
```

Do not update `.ai/v3/V3_navigation.md` as part of this external package.

Do not create a V3 journal inside this package.

Do not claim the repository has already been migrated.

Do not create active Boss/B1 files.

## Final Operational Rule

For all future workflow-doc tasks until this migration is completed:

```text
Treat B1/BOS/Boss/block-orchestration as legacy/history.
Treat Planner -> Orc as the active documentation-driven subproject execution route.
Use Report 0043 only as inventory evidence.
Keep archive/history separate from active workflow canon.
```
