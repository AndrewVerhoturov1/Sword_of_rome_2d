# V3 Critique — ork_planner_plan_index

Reviewed source file: `.ai/subprojects/ork_planner/ork_planner_plan_index.md`
Review package: `V3-20260531-091439-ork-planner-doc-critique`
Review scope: one source document only; this file does not rewrite the source document.

## Severity

**High.** The file is structurally the right kind of document, but its main function depends on anchors that do not appear explicitly in the target full plan. A broken index is not a cosmetic problem; it undermines the chosen anchor-based navigation system.

## What is correct

- The file names its target file: `ork_planner_plan_full.md`.
- It correctly states that stable semantic anchors, not line ranges, are the navigation mechanism.
- It provides a fast index with priorities, section names, anchors, and “use when” guidance.
- It includes a detailed documentation subsection and several reading routes.
- It avoids line ranges, which matches the accepted subproject design.
- It is short enough to serve as a practical map rather than duplicating the full plan.

## Problems

1. **The index likely points to non-existent anchors.** The index uses anchors like `#purpose` and `#current-execution-model`, but the full plan headings are numbered. Without explicit anchor tags in the full plan, GitHub-style generated anchors will likely be different. The index therefore cannot be trusted as a working navigation tool.

2. **`#removed-files` is especially mismatched.** The detailed index points to `#removed-files`, while the full plan section is titled `Files We Do Not Use By Default`. This is a concrete mismatch, not just a general anchor risk.

3. **No validation status per anchor.** The index does not say whether each anchor has been checked against the actual full plan. For an anchor-driven system, the index should include a small validation note or at least a `Last anchor check` field.

4. **It does not cover review artifacts.** After this V3 critique package, the subproject will have review files under `reviews/`. The plan index should either ignore them deliberately or include a separate route: “When reviewing critique findings, read review files first, then open the relevant full plan anchors.”

5. **The reading routes are useful but incomplete.** There is no route for “decide whether this subproject is ready for Orc,” which is the most important next decision after bootstrap.

6. **The file does not expose source-basis anchors.** The plan full references repo-level workflow, active route, and external tool usage, but the index does not help a reader find the parts that connect to `AGENTS.md`, Planner role, or the accepted design source.

7. **The index is fragile because it is not tied to a maintenance rule.** It says line ranges are not authoritative, but it does not say what must happen when the full plan changes. The accepted design expects plan index updates after major plan changes.

## White spots / missing areas

- No `Anchor check status` field.
- No route for `Review critique package`.
- No route for `Prepare Orc start`.
- No route for `Resolve broken anchors`.
- No mapping from review files to the full plan sections they affect.
- No warning that default GitHub anchors for numbered headings may differ from the intended semantic anchors.
- No `Last updated because` or `Last synchronized with target` note.

## Recommended fixes

1. Add explicit anchor tags to `ork_planner_plan_full.md`, then update this index only after verifying them.

2. Add a top-level status block:

   ```markdown
   ## Index Status
   Target file: `ork_planner_plan_full.md`
   Last updated: 2026-05-31
   Last anchor check: pending / passed / failed
   Known broken anchors: ...
   ```

3. Add a maintenance rule:
   - when `plan_full` headings change, update `plan_index` in the same change;
   - do not add index anchors until the full plan contains matching explicit anchors.

4. Add a review route:

   ```markdown
   ### Review V3 critique findings
   1. Read files under `reviews/`.
   2. For each finding, open the related `plan_full` anchor.
   3. Decide whether to revise source docs before Orc starts.
   ```

5. Add a route for preparing Orc:

   ```markdown
   ### Prepare Orc start
   1. Read `ork_planner_status.md`.
   2. Read `ork_planner_decisions.md`.
   3. Check unresolved review findings.
   4. Open `#active-plan-rules` and `#context-compaction`.
   5. Create or approve the next active plan only after human decision.
   ```

6. Correct `#removed-files` by either changing the full plan heading/anchor or changing the index anchor to match an explicit anchor in the full plan.

## Bottom line

The plan index is conceptually right, but it is not yet reliable. Its main job is to make the full plan navigable, and that job fails if anchors do not resolve. The first fix should not be adding more content; it should be making the current anchors real and verified.
