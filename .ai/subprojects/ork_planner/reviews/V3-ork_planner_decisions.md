# V3 Critique — ork_planner_decisions

Reviewed source file: `.ai/subprojects/ork_planner/ork_planner_decisions.md`
Review package: `V3-20260531-091439-ork-planner-doc-critique`
Review scope: one source document only; this file does not rewrite the source document.

## Severity

**Medium to High.** The decisions file captures two important decisions, but it misses at least one mandatory decision from the full plan: legacy B1/BOS is not used. It also inherits the anchor mismatch problem through related document links.

## What is correct

- The file uses the required slug prefix and decision ID format.
- D-001 correctly records the active route: `Planner -> Orc`.
- D-002 correctly records that the first version stops before Orc execution.
- Both decisions include date, status, decision, reason, consequences, and related documents.
- The decisions are concise and do not become a general plan.
- The file correctly frames the next step as requiring a separate human decision.

## Problems

1. **The no-legacy decision is only a consequence, not a decision.** The full plan says the first version must record that legacy `B1/BOS` is not used. In the decisions file, this appears only as a consequence of D-001. That is weaker than a standalone decision and easier to miss.

2. **No decision about semantic anchors.** The accepted subproject design treats semantic anchors as important, and the plan/index rely on them. Because anchor navigation is central, there should be a decision or at least an accepted policy entry for semantic anchors over line ranges.

3. **No decision about review files.** This V3 task creates review files under `reviews/`. The decisions file currently has no policy that critique files are isolated and do not overwrite source docs. That decision matters because it prevents review artifacts from being mixed with the core eight documents.

4. **Related document anchors may not work.** D-001 points to `ork_planner_plan_full.md#current-execution-model`; D-002 points to `#acceptance-criteria`. Those semantic anchors are not explicitly present in the full plan. The links may be broken.

5. **Reasons are too thin.** D-001 says the active route matches current workflow and Planner role contract, but does not name source basis. A decision file should be strong enough to prevent later re-litigation.

6. **No decision lifecycle mechanism.** The file has accepted decisions, but no instructions for `proposed`, `superseded`, or `rejected` entries. That may be acceptable for a tiny file, but this subproject is supposed to support long-lived controlled execution.

7. **No human acceptance evidence.** The decisions say `accepted`, but do not indicate whether accepted by the human, by Planner setup, or by imported docs. That matters in this workflow where final acceptance belongs to the human.

## White spots / missing areas

- Missing D-003: do not use legacy `Boss / B1 / Junior Orchestrator` as active route.
- Missing D-004: use semantic anchors rather than line ranges.
- Missing D-005: review files are isolated under `reviews/` and do not overwrite source docs.
- Missing decision lifecycle notes.
- Missing source-basis references for each decision.
- Missing check that related anchors resolve.
- Missing relation to status: which decisions must be read before Orc starts.

## Recommended fixes

1. Add a standalone no-legacy decision:

   ```markdown
   ## D-003 — Do not use legacy B1/BOS route for ork_planner
   Date: 2026-05-31
   Status: accepted

   ### Decision
   `Boss / B1 / Junior Orchestrator` and block-style subfolders are not the active route for this subproject.

   ### Reason
   The accepted subproject model uses one future Orc execution chat with documentation as external memory.

   ### Consequences
   Use `ork_planner_plan_active_N.md`, `ork_planner_journal.md`, `ork_planner_status.md`, and `ork_planner_decisions.md` instead of B1/block artifacts.
   ```

2. Add a semantic-anchor decision:

   ```markdown
   ## D-004 — Use explicit semantic anchors
   Status: proposed / accepted after fix
   Decision: `ork_planner_plan_full.md` must contain explicit anchors matching `ork_planner_plan_index.md`.
   ```

3. Add a review-isolation decision:

   ```markdown
   ## D-005 — Keep critique files isolated
   Decision: V3 critique files live only under `reviews/` and do not overwrite core `ork_planner_*.md` files.
   ```

4. Replace related document links with verified anchors after the full plan is fixed. Until then, mark them as `anchor pending verification`.

5. Add a small `Decision status rules` section:
   - `proposed` = suggested but not accepted;
   - `accepted` = accepted by human or explicitly accepted workflow source;
   - `superseded` = replaced by later decision;
   - `rejected` = considered but not used.

6. For accepted decisions, add `Accepted by:` or `Acceptance source:` where possible.

## Bottom line

The decisions file has the right shape but not enough coverage. It records the route and bootstrap stop, but misses the no-legacy decision as a first-class decision and lacks policies for anchors and review-file isolation. These omissions should be fixed before Orc uses the decisions file as a stable source of truth.
