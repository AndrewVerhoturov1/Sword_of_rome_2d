# V3 Critique — ork_planner_journal

Reviewed source file: `.ai/subprojects/ork_planner/ork_planner_journal.md`
Review package: `V3-20260531-091439-ork-planner-doc-critique`
Review scope: one source document only; this file does not rewrite the source document.

## Severity

**Low to Medium.** The journal is concise and correctly records the initial bootstrap, but it is too light on verification details. The risk is not that the journal is wrong; the risk is that future readers cannot tell what was actually checked versus merely claimed.

## What is correct

- The file clearly says it records actual execution and is not the plan itself.
- It contains a dated entry for the initial subproject bootstrap.
- It links the entry to `ork_planner_plan_active_1.md / Step 001-003`.
- It records the action, result, changed files, related decisions, external tools used, next step, and notes.
- It correctly says Orc-mode was not launched.
- It correctly says no external tools were used for the original bootstrap.
- It does not copy a transcript or turn into a second full plan.

## Problems

1. **The plan reference is too broad.** `Step 001-003` is understandable, but the accepted journal template favors a specific plan reference. If one entry covers multiple steps, it should explicitly say it is a combined bootstrap entry.

2. **Claims are not separated from checks.** The journal says global workflow docs did not change and the eight files were created, but it does not record how this was verified. A journal should not be a full test report, but it should distinguish observed facts from unchecked assumptions.

3. **No `Checks / Verification` field.** Because this is a documentation-container setup, the relevant checks would be simple: file paths, forbidden paths, no global docs overwritten, anchor/index consistency. None are recorded.

4. **The journal will become stale after V3 critique import unless a new entry is added later.** The current entry says external tools used: `none`. That remains true for the bootstrap entry, but after this V3 package is imported, the journal should gain a separate entry recording the review package import/review result. The current journal has no hint that review entries should be added separately.

5. **No outcome status.** The entry says the subproject exists as an active documentation container, but does not mark whether the result is `accepted`, `pending review`, `pending human decision`, or `ready for Orc`.

6. **No relation to review folder.** After this package, review files exist outside the original eight docs. The journal should eventually record that as a new event without implying the original bootstrap used V3.

## White spots / missing areas

- No verification summary.
- No explicit `Status after entry`.
- No note that anchor correctness was not verified.
- No note that human acceptance is still pending.
- No template for future review-import journal entries.
- No record of who made the final decision or whether the human accepted the bootstrap as sufficient.

## Recommended fixes

1. Rewrite the plan reference line to be more explicit:

   ```markdown
   Plan reference: `ork_planner_plan_active_1.md / Step 001-003` (combined bootstrap entry)
   ```

2. Add a `Verification` field:

   ```markdown
   Verification:
   - File existence: claimed by bootstrap task; local git/file check still required after import.
   - Anchor/index consistency: not verified in this entry.
   - Forbidden paths: not verified in this entry.
   ```

3. Add `Status after entry`:

   ```markdown
   Status after entry: bootstrapped / pending human decision before Orc.
   ```

4. Add a future-entry convention for critique packages:

   ```markdown
   Future V3 critique import should be recorded as a separate journal entry and must not modify this original bootstrap entry retroactively.
   ```

5. When this review package is imported and accepted, add a new journal entry such as:
   - `J-002 — V3 critique package imported under reviews/`
   - list review files;
   - state that original `ork_planner_*.md` files were not overwritten;
   - link unresolved findings.

## Bottom line

The journal is clean and not bloated, which is good. Its weakness is traceability. A future reader can see what the bootstrap claimed to do, but not what was checked. Add verification/status fields and keep future critique/import events as separate journal entries.
