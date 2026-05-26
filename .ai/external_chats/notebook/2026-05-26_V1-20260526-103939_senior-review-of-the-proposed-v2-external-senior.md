# Notebook Entry

- External Question ID: `V1-20260526-103939`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-26_V1-20260526-103939_senior-review-of-the-proposed-v2-external-senior.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/AGENTS.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/project_state.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/plans/master/v2_external_senior_review_system.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/rules/agent_protocol.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/policies/bug_tracking_policy.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/policies/human_review_policy.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/rules/kilo_mode_contract.md`

## Candidate Navigation Entry

Topic: Senior review of the proposed V2 external senior review plan
Summary: Verdict: concept is strong, but implementation needs substantial revision before start. Main fixes: do not track raw V2 artifacts in main by default, resolve `/v2 ingest` vs `kilo-recorder` boundary, make the human push gate concrete, require pinned commit links, add status/cleanup rules, and use a leaner rollout: one docs run, one verifier run, human review, Codex checkpoint, then a low-risk manual pilot.

## Raw Response

# External Chat Raw Response

## External Question ID

V1-20260526-103939

## Context Readback

* `external_chat_rules.md`: fully read.
* Central `repo_navigation.md`: fully read.
* Project `V1_navigation.md`: partially read; visible entries showed `V1-20260526-000901` and `V1-20260525-063455`.
* Project `.ai/repo_navigation.md`: fully read.
* Project `AGENTS.md`: partially read; relevant workflow, Kilo mode, recorder/notebook, human review and bug reporting parts were visible.
* Project `.ai/project_state.md`: fully read.
* Project V2 plan `.ai/plans/master/v2_external_senior_review_system.md`: fully read.
* Session plan `2026-05-23_architecture_orchestration_v1_planning.md`: partially read; relevant recent run history and `0020` state were visible.
* Navigation-discovered project `.ai/rules/agent_protocol.md`: partially read; relevant agent roles, external chat, `/v1`, `/r1`, `kilo-recorder`, `kilo-notebook` and shortcut-command sections were visible.
* Navigation-discovered project `.ai/rules/kilo_mode_contract.md`: fully read.
* Navigation-discovered project `.ai/logs/bug_journal.md`: fully read.
* Navigation-discovered project `.ai/policies/human_review_policy.md`: fully read.
* Navigation-discovered project `.ai/policies/bug_tracking_policy.md`: fully read.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require exact `External Question ID`, honest `Context Readback`, source separation, and forbid claiming local git/runtime/test access unless it was actually provided. They also say external chat is not repo authority and must separate central-doc facts, provided context and unverified areas. ([GitHub][1])

Central `repo_navigation.md` says it is an allowed navigation target for central-core files, but it explicitly does not grant authority over consumer repo facts; consumer repo files must be provided separately. ([GitHub][2])

### Confirmed from provided excerpts

No separate `Context Excerpts` were provided in the prompt.

From the project-specific links: the project repo navigation says this repo is a browser-based editor / authoring tool for 2D counter-based wargames, that Sword of Rome-like materials are only first test/reference material, and that several runtime/workflow artifact folders are local-only and not public canon unless explicitly decided otherwise. ([GitHub][3])

`AGENTS.md` confirms the existing workflow split: Codex is orchestrator, Kilo is executor for small isolated tasks, External Web Chat is a separate agent kind, and external chat is not repo authority without local verification. It also fixes allowed Kilo modes and says `kilo-recorder` and `kilo-notebook` already have strict mode-specific contracts. ([GitHub][4])

`project_state.md` confirms the project is at `Table Sandbox 0.1: Play Sandbox Ready + Map Authoring 0.1 accepted baseline + 0020 checkpointed editor-growth state`, with `0020` checkpointed but not polished, and remaining large custom image / map-plane issues deferred to a next step. ([GitHub][5])

The V2 plan says it wants a project-local `/v2` protocol under `.ai/external_reviews/`, with no helper script, no automation, no new Kilo mode, tracked V2 artifacts by default, same-repo review branches, and mandatory human confirmation before every V2 push. ([GitHub][6])

### Not available / not verified

I did not inspect local git state, local `.gitignore`, uncommitted files, real Kilo UI setup, or whether the V2 plan file is already committed locally. I did not run scripts or verify actual branch/push behavior.

I did not fully read every historical `/v1` notebook entry. The visible V1 navigation entries were about editor map-plane advice and are not the main source for this workflow review. ([GitHub][7])

### Main assessment

The plan is directionally strong, but not ready as-is.

The biggest issue is not the idea of V2 itself. The idea is good: publish a safe WIP snapshot, let an external senior reviewer inspect pinned GitHub code, then bring the advice back into local Kilo work.

The weak point is that the current plan underestimates workflow-contract friction around three things:

1. **tracked V2 artifacts by default;**
2. **`/v2 ingest` recording and interpreting an external answer without conflicting with `kilo-recorder`;**
3. **manual first rollout being both heavy and error-prone without at least stricter templates/checklists.**

So my verdict is: **needs substantial revision before implementation**, but the revision is not a rewrite. It is mostly tightening boundaries.

### Flaws / gaps / risks

1. **Tracked V2 artifacts by default is too broad.**
   The plan says V2 request/prompt/response artifacts are tracked in GitHub by default. ([GitHub][6]) But repo navigation already treats many external-chat runtime artifacts as local-only, including requests, responses, tasks, recorder packages, notebook sources and notebook packages. ([GitHub][3])
   This is a direct policy tension. V2 may intentionally publish WIP code, but raw V2 responses and problem reports can contain accidental private context, screenshots descriptions, local paths, wrong hypotheses, or sensitive debugging details.

2. **`/v2 ingest` conflicts with the existing recorder/notebook boundary unless explicitly carved out.**
   Current contracts say `kilo-recorder` is for recording external chat responses only, is response-only, does not interpret the answer, does not create a report, and does not run git status. ([GitHub][8]) The V2 plan says `/v2 ingest` should save the external answer and summarize Kilo understanding. ([GitHub][6])
   That is useful, but it is not recorder behavior. The V2 docs must explicitly say whether V2 ingest is a new ordinary Kilo Debugger/Handoff Runner workflow, or whether raw recording and interpretation are split into two steps.

3. **Same repo + `review/v2/...` is practical, but privacy risk is permanent enough to require stronger warning.**
   Same-repo review branches are easy to diff and easy for external chats to open. But if the repo is public, a pushed review branch is public. Even deleted branches may have accessible commits for some time through links, caches, clones, or PR history. The plan says "mandatory human confirmation," but it needs a stronger "publishing is irreversible enough" warning.

4. **"Always ask human before every V2 push" is correct but underspecified.**
   The plan says Kilo must always ask human confirmation before V2 push. ([GitHub][6]) Good. But the human should not be asked a vague "push?" question. The confirmation packet must show: branch name, base commit, proposed files, untracked files, ignored suspicious files, large/binary files, local-only hits, and exact risk status.

5. **Manual rollout without helper script is okay, but the plan then needs stronger copy-paste command/checklist discipline.**
   The plan intentionally excludes helper scripts in first implementation. ([GitHub][6]) That is acceptable, but it makes mistakes more likely: wrong branch, wrong commit link, branch link instead of pinned commit link, forgetting safety output, or pushing extra files. The templates must compensate.

6. **The implementation sequence is heavier than necessary.**
   The plan proposes tracker, two `/v1` checks, two Kilo Docs runs, one verifier run and Codex final review. ([GitHub][6]) For a docs/templates-only protocol, that is too much ceremony. This very question already performs the main planning critique. One focused docs run plus one verifier run is enough if the plan is corrected first.

7. **V2 could accidentally become `/r1-lite`.**
   Existing agent protocol distinguishes `/v1` prompt-only, `/r1` full external launch package, recorder-ready capture, and published task bundle. ([GitHub][8]) V2 is different, but it uses published code and external review. The plan must explicitly state when to use V2 vs `/r1`, otherwise future agents may blur the two.

8. **No explicit status lifecycle is visible.**
   The plan mentions `V2_navigation.md`, `/v2 status`, and `/v2 cleanup`, but does not define clear statuses. A V2 request needs statuses like `draft`, `previewed`, `awaiting-human-push-approval`, `pushed`, `external-answer-received`, `ingested`, `implementation-planned`, `implemented`, `superseded`, `cleaned`.

9. **Cleanup policy is too soft.**
   `/v2 cleanup` is listed, but the plan needs exact cleanup outputs: delete local review branch, delete remote review branch or explain why kept, close draft PR if used, preserve pinned commit links in the request record, mark navigation entry status, and confirm no private artifacts remain.

10. **The plan does not clearly distinguish public-safe templates from runtime V2 artifacts.**
    I would track the protocol docs/templates/navigation. I would not track every raw request/response by default in the main branch. Keep raw V2 artifacts in the review branch or local-only until explicitly promoted/sanitized.

11. **Required docs list may be too broad for first implementation.**
    The plan wants updates to `AGENTS.md`, `.ai/repo_navigation.md`, `.ai/rules/agent_protocol.md`, `.ai/rules/kilo_mode_contract.md`, and relevant prompts. ([GitHub][6]) That is many workflow contract files. Because this touches workflow rules, it is high-risk and needs care, but the actual first change should be minimal: only update files that must know V2 exists.

12. **Bug/human-review policies should be referenced explicitly in V2 outputs.**
    V2 is often triggered by a bug or difficulty. Existing bug policy requires `Баги и сложности` and bug-journal checks for repeated issues. ([GitHub][9]) Human-review policy requires simple Russian human checks when visual/browser behavior matters. ([GitHub][10]) V2 templates should include these fields, especially for UI/debug cases.

### Keep as-is

Keep these parts:

1. **Separate V2 from `/v1`.**
   V2 is not just prompt-only; it includes WIP code visibility and base/snapshot comparison. This distinction is correct.

2. **No new Kilo mode in first implementation.**
   Existing contracts allow only fixed Kilo modes. Introducing a new `Kilo V2` mode would conflict with `kilo_mode_contract.md`. ([GitHub][11])

3. **Mandatory human confirmation before push.**
   This is essential. It just needs a stricter confirmation packet.

4. **Pinned base/snapshot commits and compare context.**
   This is one of the strongest ideas in the plan. External chat must inspect a stable snapshot, not a moving branch.

5. **External answer is advisory only.**
   The plan correctly says external response is planning/debug input, not accepted fact without local verification. ([GitHub][6]) This matches existing rules that external chat is not repo authority. ([GitHub][4])

6. **No automatic code-fixing after external answer.**
   Correct. Kilo should first summarize what it understood and propose a plan.

7. **No helper script in first implementation can be acceptable.**
   This is okay only if the templates are strong enough. Automation can come after one manual pilot.

### Must change before implementation

1. **Change "tracked V2 artifacts by default."**
   Better rule:

   ```text
   Track V2 protocol docs, templates, safety checklist and V2_navigation.
   Do not track raw V2 request/response artifacts in main by default.
   Raw WIP review artifacts may live in the review/v2 branch.
   Promote only sanitized summaries into main after human/Codex review.
   ```

2. **Define V2 artifact classes.**

   ```text
   Public/stable:
   - README
   - templates
   - safety checklist
   - V2_navigation

   Runtime/review snapshot:
   - request report
   - generated external prompt
   - changed-file inventory
   - safety report

   Response/ingest:
   - raw external answer
   - Kilo understanding summary
   - implementation plan
   ```

   Each class needs a default storage/tracking rule.

3. **Resolve the `kilo-recorder` conflict.**
   The plan must explicitly say one of these:

   Option A, cleaner:

   ```text
   /v2 ingest is not kilo-recorder.
   It is an ordinary Kilo Debugger/Handoff Runner continuation that both stores the response and summarizes it.
   Therefore V2 has its own narrow ingest contract.
   ```

   Option B, more compatible:

   ```text
   Raw response capture uses kilo-recorder only.
   A separate ordinary Kilo run then reads the recorded response and writes the understanding/implementation plan.
   ```

   Option B is cleaner with current contracts, but it adds one step. Option A is more user-friendly but requires an explicit exception in workflow docs.

4. **Make the human push gate concrete.**
   Before push, Kilo must show:

   ```text
   - branch name;
   - base branch;
   - base commit;
   - proposed snapshot commit if already committed locally;
   - git status summary;
   - changed tracked files;
   - untracked files;
   - suspicious ignored files;
   - large/binary files;
   - local-only path hits;
   - secret-risk hits;
   - exact files that will be pushed;
   - exact files blocked from publishing;
   - yes/no question in simple Russian.
   ```

5. **Require commit-pinned links, not branch-only links.**
   The external prompt should prefer raw/blob links at `snapshot commit`, plus a compare link from `base commit...snapshot commit`. Branch links are allowed only as supplemental.

6. **Add a V2 status lifecycle.**
   Without statuses, `/v2 status` and cleanup will be vague.

7. **Add cleanup acceptance criteria.**
   Cleanup must say what happened to remote branch, local branch, raw artifacts, navigation entry and any draft PR.

8. **Reduce implementation sequence.**
   Do not require two more `/v1` checks before docs implementation. This review already covers the major safety/workflow critique.

9. **Add explicit "do not use V2 for secrets/private assets" rule.**
   Existing AGENTS says External Web Chat is not first-choice for secrets and high-risk areas. ([GitHub][4]) V2 is even riskier because it can publish WIP code, so this must be prominent.

10. **Add relation to bug journal and human review.**
    V2 request template should include whether this relates to an open bug journal entry, and whether a human visual check is needed after implementation.

### Leaner alternative

A safer and smaller first rollout:

```text
V2 Manual Pilot Protocol 0.1
```

Scope:

```text
1. Create `.ai/external_reviews/README.md`.
2. Create templates:
   - v2_request_template.md
   - v2_prompt_template.md
   - v2_safety_checklist.md
   - v2_ingest_summary_template.md
3. Create `V2_navigation.md`.
4. Update `.ai/repo_navigation.md`.
5. Add a short V2 section to `AGENTS.md`.
6. Add only minimal notes to `agent_protocol.md` and `kilo_mode_contract.md` if needed.
```

Storage rule:

```text
Tracked in main:
- protocol docs;
- templates;
- navigation/index;
- sanitized accepted summaries only.

Not tracked in main by default:
- raw WIP request;
- raw external answer;
- screenshots;
- local logs;
- private assets.

Allowed in review branch:
- WIP code;
- V2 request report;
- generated prompt;
- safety report,
only after human push approval.
```

This keeps the same safety level, but avoids turning first rollout into a large workflow-system migration.

### Revised recommended sequence

1. **Revise the master V2 plan first.**
   Update the current plan to fix artifact tracking, ingest/recorder boundary, status lifecycle, cleanup and human push packet.

2. **One Kilo Docs run, not two.**
   Use `strong_model` because this changes workflow contracts. Scope: create V2 docs/templates and minimal repo-rule discovery updates.

3. **One Kilo Verifier run with a different concrete model.**
   Read-only except report. Verify:

   * no new Kilo mode;
   * no forbidden pseudo-mode values;
   * no helper script;
   * templates have safety gate;
   * templates require base/snapshot commit links;
   * no push without human confirmation;
   * raw artifacts are not tracked in main by default;
   * V2 does not silently bypass `kilo-recorder` without explicit rule.

4. **Human review.**
   The user checks whether `/v2`, `/v2 preview`, `/v2 ingest`, `/v2 status`, `/v2 cleanup` are understandable in simple practical terms.

5. **Codex final review and checkpoint.**
   Codex checks diff, reports, rule consistency, `rg` searches, and only then checkpoints.

6. **Manual pilot on a low-risk non-secret issue.**
   Do one real `/v2 preview` first, then one actual review branch only after human approval. Do not add automation until after the pilot exposes real friction.

7. **Only after the pilot, consider helper script.**
   If manual V2 is too error-prone, then add a small script for inventory/link generation. Do not automate push first.

### Final verdict

**needs substantial revision before implementation**

The plan is good in concept, but the first implementation should not proceed until three areas are corrected: public/tracked artifact policy, `/v2 ingest` vs `kilo-recorder` boundary, and the exact human push safety packet. Once those are fixed, the plan can be implemented as a lean manual pilot without two extra `/v1` checks and without a broad workflow rewrite.

## Candidate Navigation Entry

V1-20260526-103939: Senior review of the proposed V2 external senior review plan. Verdict: concept is strong, but implementation needs substantial revision before start. Main fixes: do not track raw V2 artifacts in main by default, resolve `/v2 ingest` vs `kilo-recorder` boundary, make the human push gate concrete, require pinned commit links, add status/cleanup rules, and use a leaner rollout: one docs run, one verifier run, human review, Codex checkpoint, then a low-risk manual pilot.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/repo_navigation.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/AGENTS.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/project_state.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/plans/master/v2_external_senior_review_system.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/rules/agent_protocol.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/policies/bug_tracking_policy.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/policies/human_review_policy.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/666c8d2f8e893919ca85ddc1b60fad129649f87b/.ai/rules/kilo_mode_contract.md "raw.githubusercontent.com"
