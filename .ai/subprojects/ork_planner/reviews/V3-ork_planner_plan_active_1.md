# V3 Critique — ork_planner_plan_active_1

Reviewed source file: `.ai/subprojects/ork_planner/ork_planner_plan_active_1.md`
Review package: `V3-20260531-091439-ork-planner-doc-critique`
Review scope: one source document only; this file does not rewrite the source document.

## Severity

**Medium.** The active plan is clear and correctly bounded, but it is now mostly an already-completed bootstrap record. It needs a stronger closure state and a safer bridge to the next active plan or Orc handoff.

## What is correct

- The file is short, operational, and not a duplicate of the full plan.
- It correctly names the setup goal: create the minimal documentation container and stop.
- The non-goals are appropriate: no Orc launch, no product-work, no legacy B1/BOS structure.
- The three steps match the actual bootstrap sequence: create folder, create required docs, stop after bootstrap.
- All steps are marked `done`, which matches the journal/status claim that the initial documentation set has been created.
- The completion criteria correctly focus on documentation setup and human-controlled next step.

## Problems

1. **The plan is marked done, but it does not state what replaces it.** A completed active plan should leave a clear next control object: either `ork_planner_plan_active_2.md`, an Orc preparation step, or a paused state awaiting human decision.

2. **The acceptance criteria are too shallow.** Step 002 only checks that files exist. It does not check that the files are internally consistent, that anchors work, that role boundaries are clear, or that forbidden paths were untouched. Existence is not enough for documentation quality.

3. **The active plan does not mention review findings.** This V3 task creates critique files. After import, the bootstrap plan should not simply remain “done” without acknowledging that the docs may need revision before Orc starts.

4. **No explicit handoff gate to Orc.** The plan says stop after bootstrap, but it does not define what must be true before Orc can start. The accepted design says Orc begins by turning the full plan into an executable system; here, that transition is not operationalized.

5. **Related full plan anchors may be broken.** The file references anchors such as `#documentation-structure`, `#status-command`, and `#journal-rules`. Those anchors are not explicitly present in the full plan, so the related anchor list may not work.

6. **No human check details.** The repo-level human review policy expects simple user-facing checks when human review is needed or suggested. This file says the next step is human-controlled but does not say what the human should inspect.

7. **No verification of forbidden paths.** The task’s boundary is “do not create legacy files / do not alter global docs.” The active plan should include a step or acceptance criterion for checking that.

## White spots / missing areas

- No `Closure state` section.
- No `Next active plan` or `No active execution plan yet` field.
- No quality checks for anchor/index consistency.
- No check that original files and global workflow docs were not overwritten.
- No instruction for handling V3 critique results.
- No explicit “ready for Orc” gate.
- No “blocked if review finds High severity issue” rule.

## Recommended fixes

1. Add a `Closure State` section:

   ```markdown
   ## Closure State
   Status: done_with_review_pending
   Bootstrap is complete, but source docs should not be treated as ready for Orc until review findings are accepted or resolved.
   ```

2. Strengthen Step 002 acceptance:
   - all eight files exist;
   - all filenames use `ork_planner_` prefix;
   - no forbidden legacy files exist;
   - full plan anchors match plan index;
   - status and journal agree;
   - decisions contain the mandatory active-route decisions.

3. Add a Step 004 if source docs are revised later:

   ```markdown
   ### Step 004 — Review bootstrap docs before Orc
   Status: todo / pending_human
   Action: Read review findings and decide whether source docs need fixes before Orc starts.
   Acceptance: Human either accepts current docs as-is or approves a focused revision task.
   ```

4. Add a `Ready for Orc Gate`:
   - no High severity review issues unresolved, or human explicitly accepts the risk;
   - status points to a concrete next action;
   - plan index anchors are verified;
   - decisions file contains route and no-legacy decisions.

5. Add human-check instructions in simple Russian:
   - open status;
   - open plan index and click anchors;
   - confirm the eight core files are not overwritten;
   - decide whether Orc may proceed.

## Bottom line

The active plan did its bootstrap job, but it should not be treated as sufficient for the next phase. It needs a closure/gate section so the process does not jump from “files exist” directly to “Orc may execute.”
