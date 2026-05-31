# V3 Critique — ork_planner_plan_full

Reviewed source file: `.ai/subprojects/ork_planner/ork_planner_plan_full.md`
Review package: `V3-20260531-091439-ork-planner-doc-critique`
Review scope: one source document only; this file does not rewrite the source document.

## Severity

**High.** The full plan is conceptually aligned with the intended `Planner -> Orc` route, but it has a structural navigation defect: the plan index references semantic anchors that are not explicitly present in the full plan. Because the full plan is supposed to be the strategic source for Orc, broken or ambiguous anchors are a serious documentation-quality issue.

## What is correct

- The file has the right role: it is the strategic “book of the plan,” not the active execution log.
- It correctly defines the subproject as a documentation container, not an Orc execution run.
- It clearly states that Orc-mode is not launched during the setup step.
- It lists exactly the eight core startup files and correctly avoids creating `reports` in the first version.
- It rejects legacy B1/BOS/block-style structures and other overbuilt files by default.
- It includes rules for plan index, active plan, journal, status, decisions, context compaction, external tools, reports, risks, and acceptance criteria.
- It correctly treats V1/V2/V3/Kilo as external tools, not permanent subagents.

## Problems

1. **The required semantic anchors are not explicit.** The acceptance criteria say the full plan contains semantic anchors. The plan index points to anchors like `#purpose`, `#current-execution-model`, and `#documentation-structure`. But the source headings are numbered, such as `## 1. Purpose` and `## 2. Current Execution Model`. On GitHub, automatic anchors for numbered headings are normally based on the full heading text, not the clean semantic IDs in the index. This means the index may not reliably jump to the intended sections.

2. **Some index anchors do not match the full plan headings.** The plan index includes `#removed-files`, but the full plan section is titled `Files We Do Not Use By Default`. Unless an explicit anchor is added, that link is broken or misleading.

3. **The plan says “inside exactly 8 startup files,” but future review files complicate this.** The current V3 task adds review files under `reviews/`. The full plan should distinguish “exactly 8 core startup docs at the subproject root” from “additional isolated review artifacts may exist under `reviews/`.” Without that distinction, future agents may incorrectly treat the review folder as a violation.

4. **The file status is `draft` while the setup is marked done elsewhere.** This may be intentional, but it should be explained. A plan can remain draft after bootstrap, but then status/active plan should not imply the strategic plan is fully accepted.

5. **The `Planner -> Orc` route is present but thin.** The plan says one Planning Chat and one future Execution Chat, but it does not explicitly bind `Orc` to that future execution role. The accepted source contains a richer distinction: Planner owns the full plan; Orc owns active plans and execution route. The full plan should capture that because this subproject is named `ork_planner`.

6. **Acceptance criteria include claims that require verification.** For example, “global workflow docs не менялись” and “legacy artifacts not created” are not self-verifying inside the full plan. The plan should say how those checks are verified or that they require Codex/Kilo/human review.

7. **The external tools section may become stale.** It says V3 is not needed “сейчас.” That is true for bootstrap, but this critique package is a V3 artifact. The full plan should distinguish initial bootstrap from later review/critique cycles.

8. **No explicit human review/check policy.** The repo contract expects human review sections for implementation results, and the accepted subproject system expects human final decisions. The full plan references a human-approved next step, but it does not define what the human checks before allowing Orc to proceed.

## White spots / missing areas

- No explicit `<a id="..."></a>` anchors or equivalent stable anchor declarations.
- No section explaining review artifacts and where they belong.
- No precise transition rule from `bootstrap complete` to `ready for Orc`.
- No source-basis table showing which higher-level docs this plan depends on.
- No verification method for “only allowed files were changed.”
- No policy for what to do if critique finds defects in the eight startup docs.
- No `Orc first run` checklist, even though the accepted design says Orc first transforms the full plan into active plans, navigation, journal, status, and decisions.
- No clear status taxonomy: `draft`, `bootstrapped`, `reviewed`, `accepted`, `ready_for_orc`, `active`, `done`.

## Recommended fixes

1. Add explicit semantic anchors before every section used by `ork_planner_plan_index.md`, for example:

   ```markdown
   <a id="purpose"></a>
   ## 1. Purpose
   ```

   Repeat for `current-execution-model`, `documentation-structure`, `slug-naming-rule`, `required-files`, `optional-files`, `removed-files`, `plan-index-rules`, `active-plan-rules`, `journal-rules`, `status-command`, `decisions-policy`, `context-compaction`, `external-tool-usage`, `reports-policy`, `risks`, and `acceptance-criteria`.

2. Update `Files We Do Not Use By Default` to include or be preceded by the explicit anchor `removed-files`.

3. Add a `Review Artifacts Policy` section:
   - review files live only under `reviews/`;
   - review files do not count as core startup docs;
   - review files do not overwrite source docs;
   - accepted fixes from review must be applied separately.

4. Add a `Bootstrap vs Ready for Orc` distinction:
   - `bootstrapped`: eight docs exist;
   - `reviewed`: critique has been read;
   - `ready_for_orc`: human accepts or resolves review findings.

5. Add a short `Human Check` section:
   - confirm that only the review folder is imported;
   - confirm original docs are untouched;
   - decide whether to revise source docs before Orc starts.

6. Add an `Orc first run checklist`:
   - read status;
   - read full plan;
   - validate anchors/index;
   - read review files if present;
   - propose source-doc fixes or create next active plan only after human approval.

7. Replace broad acceptance claims with verifiable checks, for example:
   - `Check: list files under .ai/subprojects/ork_planner/ and confirm root core docs remain exactly the expected eight.`

## Bottom line

The full plan is the strongest of the eight documents in content coverage, but it has the most important technical documentation defect: anchor mismatch. Until explicit anchors are added, the plan index is only aspirational. Fixing anchors and adding a review-artifact policy should happen before this subproject is treated as ready for Orc execution.
