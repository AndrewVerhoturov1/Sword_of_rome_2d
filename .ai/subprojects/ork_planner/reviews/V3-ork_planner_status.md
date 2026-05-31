# V3 Critique — ork_planner_status

Reviewed source file: `.ai/subprojects/ork_planner/ork_planner_status.md`
Review package: `V3-20260531-091439-ork-planner-doc-critique`
Review scope: one source document only; this file does not rewrite the source document.

## Severity

**Medium.** The status file is short and useful, but it is not precise enough for safe resume after review. Its main flaw is that it points to a completed setup step as the current step instead of clearly saying the subproject is paused pending human decision and review resolution.

## What is correct

- The file contains the required status basics: last updated date, current active plan, current step, last completed action, next action, immediate risks, human decision, required files for resume, and resume instruction.
- It correctly identifies `ork_planner_plan_active_1.md` as the current active plan.
- It correctly says the documentation set has been created.
- It correctly warns against starting execution work too early and creating legacy-style files.
- It correctly leaves the next step to the human instead of silently starting Orc.

## Problems

1. **The “current step” is a completed step.** It says `Step 003 — Stop after bootstrap`. Since that step is done, this is not really a current execution step. A safer status would say `Current step: none / paused after Step 003` or `Current state: bootstrap complete; waiting for human decision`.

2. **The next action is too open-ended.** “Человек открывает active plan и решает...” is safe, but not operational enough. The user needs concrete choices: accept bootstrap as-is, import/read critique, revise docs, or start Orc.

3. **It does not account for review findings.** After this V3 package, the status should likely become `pending_review_resolution` or similar. The source status has no slot for unresolved review issues.

4. **Immediate risks are incomplete.** The two listed risks are valid, but the current docs also have anchor/index mismatch risk, role-boundary ambiguity, and possible confusion between eight core files and extra review files.

5. **Required files for resume omit `ork_planner_decisions.md`.** For a paused workflow with a human decision pending, the decisions file is essential. It should be in the required resume set.

6. **Required files for resume omit review files if present.** This is understandable before the review package, but once reviews exist, status should tell future readers whether reviews must be read before Orc starts.

7. **No clear acceptance gate.** The status says when to pass to Orc is a human decision, but it does not say what information the human should use to make that decision.

8. **No check state.** The status does not say whether anchors were checked, files were verified, or source docs are review-clean.

## White spots / missing areas

- No `Current state` field distinct from `Current step`.
- No `Review status` field.
- No `Ready for Orc` field.
- No list of unresolved blockers/findings.
- No required read of `ork_planner_decisions.md` before resume.
- No human decision options.
- No note that review files under `reviews/` are critique artifacts and not source docs.

## Recommended fixes

1. Replace the current step wording with:

   ```markdown
   ## Current state
   Bootstrap complete. Paused before Orc.

   ## Current active plan
   `ork_planner_plan_active_1.md` — completed bootstrap plan.

   ## Current step
   None. Waiting for human decision.
   ```

2. Add a `Review status` section:

   ```markdown
   ## Review status
   V3 critique package: pending import / imported / reviewed / resolved.
   High severity findings: pending / none / accepted risk.
   ```

3. Add concrete human decision options:

   ```markdown
   ## Human decision needed
   Choose one:
   1. Accept bootstrap docs as-is and allow Orc preparation.
   2. Revise source docs based on review findings first.
   3. Request another external review.
   4. Pause the subproject.
   ```

4. Expand `Required files for resume`:
   - `ork_planner_navigation.md`
   - `ork_planner_status.md`
   - `ork_planner_plan_active_1.md`
   - `ork_planner_plan_index.md`
   - `ork_planner_decisions.md`
   - `ork_planner_journal.md`
   - `reviews/` files if imported and unresolved.

5. Add `Ready for Orc`:

   ```markdown
   ## Ready for Orc
   No. Bootstrap is complete, but review findings should be checked before Orc starts.
   ```

6. Add immediate risks:
   - plan index anchors may not match full plan;
   - review files may be mistaken for core docs;
   - source docs may be treated as accepted without human review.

## Bottom line

The status file is useful but too optimistic. It should not present a completed step as the current step. After this critique package, it should clearly say: bootstrap is complete, review findings are pending, and Orc should not start until the human chooses the next route.
