# V3 Critique — ork_planner_readme

Reviewed source file: `.ai/subprojects/ork_planner/ork_planner_readme.md`
Review package: `V3-20260531-091439-ork-planner-doc-critique`
Review scope: one source document only; this file does not rewrite the source document.

## Severity

**Medium.** The document is directionally correct and safe as an entry door, but it is too compressed to be a reliable long-term subproject README. The main risk is not catastrophic repo damage; the risk is that future Orc/Planner sessions will have to infer too much from other files.

## What is correct

- The source file uses the required slug prefix and names the slug explicitly: `ork_planner`.
- The owner model is correctly framed as `Planner -> Orc`, which matches the active route required by the current workflow direction.
- The purpose and main goal are bounded: create a starting documentation set and stop before execution work.
- The execution model correctly rejects permanent subagents as the main mechanism and treats V1/V2/V3/Kilo as external tools.
- The `Scope` and `Out of Scope` sections correctly prevent three common failure modes: starting Orc too early, doing product-work, and reviving the legacy `Boss / B1 / Junior Orchestrator` route.
- The file points to the current status file instead of trying to duplicate live state.

## Problems

1. **The README is too short for a stable entry door.** It says what the subproject is, but not enough about how a future reader should safely use it. For a subproject documentation container, the README should reduce ambiguity, not just list files.

2. **The `Planner -> Orc` boundary is stated but not explained.** The file says `Owner model: Planner -> Orc`, then says an `Execution Chat` will appear later. That is understandable to someone who already knows the system, but weaker for future recovery after context compaction. It should explicitly say whether `Orc` is the future execution chat role for this subproject.

3. **The README does not name the accepted design source.** It should mention that the structure follows `ideas/subproject_single_execution_chat_documentation_system_v2.md`. Without that, future agents may treat this as an ad hoc folder rather than an instance of the accepted subproject structure.

4. **It omits the source README itself from `Main Documents`.** The file lists the navigation, plan, index, active plan, journal, status, and decisions files, but not `ork_planner_readme.md`. That is small, but for a documentation entry point it is cleaner to include itself as the entry document.

5. **The scope wording mixes setup action and created state.** The file says the scope is “создать папку” and “создать 8 стартовых документов,” but by the time the README exists these actions are already done. This can confuse resume logic: is this a plan for creation, or a description of the created container?

6. **No explicit review/critique boundary.** The current V3 package adds review files under `reviews/`. The original README does not reserve or explain that review files are separate from the core eight startup documents. This matters because the full plan says the folder should contain exactly eight startup files; after review import, that statement can be misread as forbidding the `reviews/` subfolder.

7. **No human-readable “do not execute from here” warning.** The out-of-scope list says Orc is not launched, but the README should make this operational: this folder is a documentation container, not an execution instruction by itself.

## White spots / missing areas

- No “Source basis” section naming the active repo contract, Planner role contract, accepted subproject structure, and current project state.
- No short explanation of what `Orc` means in this subproject.
- No lifecycle status distinction between `planning`, `bootstrapped`, `reviewed`, `accepted`, and `ready_for_orc`.
- No explanation of where critique/review files belong.
- No “safe resume” mini-route for a reader who opens only the README first.
- No explicit note that the original `ork_planner_*.md` files must not be overwritten by critique files.

## Recommended fixes

1. Add a short `## Source Basis` section:
   - `AGENTS.md`
   - `.ai/rules/codex_role_planner.md`
   - `.ai/repo_navigation.md`
   - `.ai/project_state.md`
   - `ideas/subproject_single_execution_chat_documentation_system_v2.md`

2. Change the status wording from plain `planning` to something more precise, for example:
   - `Status: bootstrapped / awaiting human decision before Orc`

3. Add a one-sentence role clarification:
   - `Orc is the future execution-orchestration role for this subproject; Orc has not been started by this bootstrap.`

4. Add `ork_planner_readme.md` to the `Main Documents` list as the entry document.

5. Split the current `Scope` into:
   - `Bootstrap already created`
   - `Allowed next steps`
   - `Still out of scope`

6. Add a `Reviews` note:
   - review files, if imported, live only under `.ai/subprojects/ork_planner/reviews/` and do not replace the eight core `ork_planner_*.md` files.

7. Add a strong boundary sentence:
   - `This README does not authorize product work, Kilo work, or Orc execution by itself.`

## Bottom line

The README is safe and mostly aligned with the intended direction, but it is too minimal. It works as a bootstrap note, not yet as a durable entry point for a long-lived subproject. The most important fix is to clarify the `Planner -> Orc` boundary and explain that review artifacts are separate from the eight core startup documents.
