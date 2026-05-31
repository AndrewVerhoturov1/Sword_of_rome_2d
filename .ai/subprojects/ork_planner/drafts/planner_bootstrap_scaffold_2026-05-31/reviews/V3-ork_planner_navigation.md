# V3 Critique — ork_planner_navigation

Reviewed source file: `.ai/subprojects/ork_planner/ork_planner_navigation.md`
Review package: `V3-20260531-091439-ork-planner-doc-critique`
Review scope: one source document only; this file does not rewrite the source document.

## Severity

**Medium.** The navigation file is usable for the initial bootstrap, but it is incomplete as the main map of the subproject. Its biggest weakness is that it does not preserve enough source basis and future review/import context for safe continuation.

## What is correct

- It provides a clear `Start Here` route and correctly prioritizes `ork_planner_status.md`, the active setup plan, the plan index, and decisions.
- It lists all eight core documents and gives each a practical purpose.
- It correctly marks `ork_planner_plan_active_1.md` as the active setup plan.
- It includes required repo context rather than pretending the subproject is self-contained.
- It explicitly deprecates the legacy `Boss / B1 / Junior Orchestrator` active route and block-style subfolders.
- It gives three useful reading routes: resume after compaction, understand the whole subproject, and continue setup work.

## Problems

1. **Required context is incomplete.** The navigation names `AGENTS.md`, `.ai/repo_navigation.md`, and the accepted design source, but omits `.ai/rules/codex_role_planner.md` even though this subproject is explicitly about the `Planner -> Orc` route. It also omits `.ai/project_state.md`, which is part of the prompt context and helps prevent confusion between workflow docs and product-code status.

2. **The navigation does not include the Planner role boundary.** It says the active route is not legacy B1/Boss, but it does not tell a reader where to read the Planner-specific role contract. That makes it easier for future sessions to blur Planner and Orc.

3. **The V1/V2/V3/Kilo table is too static.** It says all are `none` or `not used`. That was true at bootstrap, but this critique package is itself a V3 artifact package. After import, navigation should have a way to record “V3 review package exists under reviews/” without mixing review files into the core eight documents.

4. **No `reviews/` section.** The task explicitly requires critique files to live in `.ai/subprojects/ork_planner/reviews/` and not mix with the main files. The current navigation has no place for such isolated review artifacts.

5. **The deprecated section is too narrow.** It mentions `Boss / B1 / Junior Orchestrator` and block-style subfolders, but not other known forbidden/legacy-style files from the full plan such as `BOSS_*`, `TASK_CONTROL_PACK*`, `SUBPROJECT_STATE.md`, `PLANNER_HANDOFF.md`, `ORC_EXECUTION_LOG.md`, `CHECKPOINTS.md`, and `CONTEXT_INDEX.md`.

6. **Reading order slightly conflicts with the “navigation as map” idea.** The file itself is the map, but `Start Here` begins with status. That is acceptable for a resume route, but the navigation should distinguish “if you are already in this file” from “after compaction, read status first.”

7. **No freshness or maintenance rule.** The file says `Last updated: 2026-05-31`, but does not say what kinds of events require updating navigation. The accepted source says navigation must be updated when new important files, V1/V2/V3/Kilo materials, or deprecated materials appear.

## White spots / missing areas

- No direct mention of `.ai/rules/codex_role_planner.md`.
- No direct mention of `.ai/project_state.md`.
- No section for review artifacts under `reviews/`.
- No “after importing a V3 critique package” reading route.
- No rule for keeping navigation synchronized with new review files, external packages, reports, or accepted decisions.
- No warning that review files are not replacements for original `ork_planner_*.md` files.
- No separation between core docs, optional docs, review docs, and forbidden docs.

## Recommended fixes

1. Add these to `Required Repo Context`:
   - `.ai/rules/codex_role_planner.md` — Planner role boundary for `Planner -> Orc`.
   - `.ai/project_state.md` — current project maturity and practical next step.

2. Add a `Review Materials` section:
   - `reviews/V3-ork_planner_readme.md`
   - `reviews/V3-ork_planner_navigation.md`
   - `reviews/V3-ork_planner_plan_full.md`
   - `reviews/V3-ork_planner_plan_index.md`
   - `reviews/V3-ork_planner_plan_active_1.md`
   - `reviews/V3-ork_planner_journal.md`
   - `reviews/V3-ork_planner_status.md`
   - `reviews/V3-ork_planner_decisions.md`

3. Mark review files as **non-core**:
   - they are critique artifacts;
   - they do not overwrite source docs;
   - they should be read before deciding whether to revise the core docs.

4. Expand `Deprecated / Do Not Use` with the forbidden legacy-style names already listed in the full plan.

5. Add a `Navigation Maintenance Rule`:
   - update navigation when a new active plan, review package, external response, Kilo report, decision, or deprecated file appears.

6. Split reading routes into:
   - `Resume after context compaction`
   - `Review this subproject after V3 critique import`
   - `Prepare Orc handoff`
   - `Understand source basis`

## Bottom line

The navigation file is a good first map, but it is not yet robust enough for future workflow use. Its most important missing piece is a dedicated review-artifact section, because this V3 critique package intentionally adds files that must stay separate from the eight core `ork_planner_*.md` documents.
