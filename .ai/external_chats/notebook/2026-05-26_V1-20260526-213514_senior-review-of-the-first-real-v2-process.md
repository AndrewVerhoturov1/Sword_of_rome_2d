# Notebook Entry

- External Question ID: `V1-20260526-213514`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-26_V1-20260526-213514_senior-review-of-the-first-real-v2-process.md`

## Context Links

- `нет`

## Candidate Navigation Entry

Topic: Senior review of the first real V2 process after the underlay alignment case
Summary: Verdict: `good with targeted corrections`; V2 worked technically and produced a successful fix, but docs need lifecycle hardening: mandatory `push -> instantiated prompt`, explicit `/v2` interrupt contract, clear `V2_navigation` updates, hybrid cleanup ownership, runtime artifact minimum set, YOLO push-gate stop rule, and path/write fallback.

## Raw Response

# Raw External Response

## External Question ID

V1-20260526-213514

## Context Readback

* `external_chat_rules.md`: fully read. ([GitHub][1])
* Central `repo_navigation.md`: fully read. ([GitHub][2])
* Project `V1_navigation.md`: partially read; visible entries included V2-related records `V1-20260526-135600`, `V1-20260526-123133`. ([GitHub][3])
* Project `.ai/repo_navigation.md`: partially read; relevant public/local-only and reading-order lines were visible. ([GitHub][4])
* Project `AGENTS.md`: partially read; relevant project context, local-only, human review and bug tracking sections were visible. ([GitHub][5])
* `agent_protocol.md`: partially read; relevant Codex/Kilo roles, Kilo modes, recorder/notebook, external chat, sequence and shortcut-command sections were visible. ([GitHub][6])
* `kilo_mode_contract.md`: fully read for available content. ([GitHub][7])
* V2 README: fully read for available content. ([GitHub][8]) ([GitHub][8])
* `V2_navigation.md`: fully read; it currently says there are no active V2 requests. ([GitHub][9])
* V2 master plan: fully read for available content. ([GitHub][10]) ([GitHub][10])
* External chats manual: fully read for available content. ([GitHub][11])
* Bug journal: fully read for available content. ([GitHub][12])
* Published V2 compare `89fabf...318094d`: partially read; GitHub page opened, but full diff content was not useful in returned view. ([GitHub][13])
* Snapshot `EditorSurface.tsx` at `318094d`: partially read; relevant underlay/editor code was visible, but raw file is compacted. ([GitHub][14])
* Snapshot `MapDraft.ts` at `318094d`: partially read; relevant underlay/map-local state comments and types were visible. ([GitHub][15])
* Base `EditorSurface.tsx` at `89fabf...`: partially read; opened, but not enough useful rendered content for detailed comparison. ([GitHub][16])
* Base `MapDraft.ts` at `89fabf...`: partially read; opened, but not enough useful rendered content for detailed comparison. ([GitHub][17])
* Historical V1 review `V1-20260526-103939`: partially read; relevant planning review and recommended V2 fixes were visible. ([GitHub][18])
* Historical V1 review `V1-20260526-123133`: partially read; relevant audit summary and must-fix themes were visible. ([GitHub][19])
* Historical V1 review `V1-20260526-135600`: partially read; relevant YOLO/V2 stop-gate review summary was visible. ([GitHub][20])

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central rules require honest readback, source separation, exact external question ID, and no claims about local git/runtime/tests unless that access was explicitly provided. They also require opened navigation-discovered links to appear in `Context Readback`. ([GitHub][1])

Central navigation explicitly says it does not authorize claims about the consumer repo; consumer repo facts require project-specific links or excerpts. ([GitHub][2])

### Confirmed from project docs

The accepted V2 docs define V2 as a manual protocol for external senior review of real WIP code through a GitHub-visible snapshot. V2 is separate from `/v1` and `/r1`, does not add a new Kilo mode, requires `/v2 preview` before push, and treats public `review/v2/...` branch push as publication. ([GitHub][8])

The V2 docs already define a lifecycle with statuses such as `draft`, `previewed`, `awaiting_human_push_approval`, `snapshot_pushed`, `waiting_external_answer`, `ingested`, `implemented`, `superseded`, and `cleaned`. They also define `/v2 cleanup` as checking branch fate, `V2_navigation.md`, final status, raw artifact leakage, and draft PR state. ([GitHub][8])

The V2 master plan says the first implementation intentionally has no helper script, no automatic push, no new Kilo mode, no automatic code fixing after external answer, and requires human confirmation before every V2 push. ([GitHub][10])

The Kilo mode contract confirms V2 is not a new Kilo mode, uses existing `kilo-handoff-runner` / `kilo-debugger`, and V2 ingest is manual without `kilo-recorder`; `kilo-notebook` remains `/v1-only`. ([GitHub][7])

The external chats manual also says V2 is separate from `/r1`, does not use the published-artifact route, requires `/v2 preview`, treats public review branch push as publication, and uses manual ingest rather than `kilo-recorder`. ([GitHub][11])

The bug journal records the editor map-plane / large image geometry drift as an open issue, with human check suggested on a live large custom map. ([GitHub][12])

### Confirmed from published V2 snapshot

The snapshot code at `318094d` contains the underlay/map-plane work: `MapDraft.ts` describes separate authoring state, `UnderlayState`, `EditorSettings`, map-plane transform model, and undo/redo snapshot types. ([GitHub][15])

Snapshot `EditorSurface.tsx` shows the V2-reviewed WIP was real editor code, not an empty process test: it contains underlay state usage, image loading, active draft coordinate size, underlay move/scale/rotate handlers, grid/snap, undo/redo, and one SVG map-plane group for underlay, grid, connections, spaces and handles. ([GitHub][14])

The compare URL opened, but the returned GitHub page did not provide a useful full diff in this environment, so I treat raw base/snapshot files and the provided runtime excerpts as stronger sources. ([GitHub][13])

### Confirmed from current excerpts

The real V2 cycle was successful technically: Kilo reached `/v2 preview`, gathered inventory, got human approval, pushed `review/v2/20260526-140000-underlay-alignment`, an external chat gave useful technical review, Kilo applied three editor fixes, and the user manually confirmed that the map now moves correctly.

The main process failure was not technical review quality, but lifecycle bookkeeping: after push, Kilo did not immediately create the instantiated V2 prompt and tried to go to final report until the human reminded it.

The current observed state has inconsistencies: `V2_navigation.md` still says there are no active V2 requests, the local and remote review branches still exist, a local instantiated prompt exists, but the normalized runtime artifact set is incomplete or not visible under `requests`, `safety`, `responses`, and `ingest_summaries`.

The observed frictions were: weak `push -> prompt` contract, weak `/v2` as interrupt-command contract, YOLO vs human push gate friction, and a tool-level path writing issue for `.ai/external_reviews/prompts/...`.

### Not available / not verified

I did not inspect local branches, local runtime artifacts, local `git status`, local filesystem, Kilo reports, shell logs, actual prompt file, actual request/safety files, response/ingest files, or branch deletion permissions.

The facts about Kilo needing manual reminder after push, local/remote branch existence, missing artifacts, and user's successful manual check are taken from the provided excerpts, not independently verified.

### Main assessment

The real V2 process is **working but not yet smooth**.

The important part succeeded: V2 solved the exact problem it was created for. A real WIP snapshot was published, an external senior review looked at the code, the advice was useful, Kilo applied fixes, and the user confirmed the editor behavior improved.

The weak part is the lifecycle contract around the review. The docs describe the pieces, but the actual process showed that Kilo can complete the "push" part and then forget the next required step: creating the instantiated prompt, handing it to the human, waiting for the external answer, ingesting it, updating navigation, and cleaning up.

So the answer is not "redesign V2." The answer is: **tighten V2 as a state machine.** The next V2 run should not rely on the human remembering the next step.

### What already works well

The review-branch idea worked. The external reviewer had real code at pinned commits, and the snapshot files were accessible. That is the core purpose of V2.

The human push gate worked in principle: Kilo reached preview, collected inventory, asked for approval, and only then pushed. That is exactly the safety model the V2 docs require. ([GitHub][8])

The manual external review loop produced useful engineering advice, and the result was actually applied and human-checked. This proves V2 is not just documentation overhead; it materially improved the editor.

The separation from `/v1`, `/r1`, `kilo-recorder`, and `kilo-notebook` is still the right design. The existing contracts say V2 is manual, not a new Kilo mode, not recorder, not notebook, and not `/r1`. Keep that. ([GitHub][7])

The "public branch = publication" warning is correct and should remain strict. ([GitHub][8])

### Process gaps

1. **`push -> prompt` gap**

   This is the most important gap. Current docs say `/v2` prepares a snapshot, shows preview, asks approval, and pushes. They also define `snapshot_pushed` and `waiting_external_answer`, but they do not make "create instantiated prompt immediately after push" feel like a mandatory next action. ([GitHub][8])

   Recommended fix: after successful push, Kilo must not write final report yet. It must immediately create the instantiated prompt, verify that it uses commit-pinned links, print the copy-paste prompt for the human, and only then move status to `waiting_external_answer`.

   I would define:

   ```text
   snapshot_pushed = branch exists, but prompt may not yet be ready
   prompt_ready = instantiated prompt exists and was shown to human
   waiting_external_answer = human has been given the prompt / external chat is expected
   ```

   If you do not want a new status, then at least redefine `waiting_external_answer` to mean: "snapshot pushed + instantiated prompt created + prompt handed to human." Without prompt, status must not advance.

2. **`/v2` as interrupt-command is underdescribed**

   Current docs cover the case where Kilo naturally reaches `blocked-v2-recommended`. The observed real case also includes a human explicitly invoking `/v2` during an ongoing debug run. The docs should say what happens then.

   Recommended contract:

   ```text
   If user invokes `/v2` during an active Kilo debug run, Kilo must pause normal debugging, summarize current WIP state, run `/v2 preview`, and ask for human push approval.
   ```

   This is not the same as a blocker. It is a user-requested escalation. It should not require Kilo to first prove three failed attempts or write a full blocked report.

3. **YOLO vs human gate friction**

   V2 push approval must remain a hard human gate even in YOLO mode. The docs already say push requires explicit human confirmation, but the runtime observation shows Kilo in YOLO can still "flow past" ask/follow-up behavior.

   Add an explicit sentence:

   ```text
   In YOLO mode, reaching `awaiting_human_push_approval` is a valid final state for the current attempt. Kilo must stop and wait; continuing without approval is a protocol violation.
   ```

4. **Navigation was not updated**

   `V2_navigation.md` currently says there are no active V2 requests, even though the real process produced a pushed branch and useful external review. The file itself says records should appear after the first manual pilot and should include request location and branch state. ([GitHub][9])

   This is a bookkeeping failure. `V2_navigation.md` must be updated at least at two points: after prompt creation and after cleanup.

5. **Runtime artifact ownership is unclear**

   The docs list normalized paths for requests, prompts, safety, responses, ingest summaries and sanitized summaries. ([GitHub][8]) But the observed run ended with only a prompt clearly visible locally and missing or unclear request/safety/response/ingest artifacts.

   The docs need a clear minimum artifact set for a real V2 run:

   ```text
   Required before push:
   - request report
   - safety report
   - changed-file inventory, if separate
   - review branch/snapshot metadata

   Required after push:
   - instantiated prompt

   Required after external answer:
   - either response file or note that answer was pasted directly
   - ingest summary / Kilo understanding summary

   Required after implementation:
   - final V2_navigation update
   - cleanup decision
   ```

6. **Path/write issue needs a documented fallback**

   The observed path issue matters because V2 relies on correct artifact paths. Add a small fallback rule:

   ```text
   If writing to `.ai/external_reviews/...` fails or the tool truncates path, Kilo must stop artifact creation, create/check the directory explicitly, retry with exact path, then verify the file exists. If still blocked, report `blocked-no-source-of-truth` or `blocked-needs-human-decision` with the intended path and no push.
   ```

7. **Cleanup is documented but not owned**

   `/v2 cleanup` exists in the docs, but the observed state shows nobody clearly "owns" it. The result: remote branch remains, local branch remains, nav remains stale, and runtime artifacts are inconsistent.

   The docs should state cleanup is not optional. It can leave branches intentionally, but only with an explicit recorded decision.

### Cleanup ownership model

Use a **hybrid model**, not purely Kilo-owned, Codex-owned, or human-owned.

#### Kilo owns operational cleanup preparation and execution

Kilo should:

```text
- inspect current V2 state;
- list local review branch state;
- list remote review branch state;
- list runtime artifacts under `.ai/external_reviews/*`;
- propose cleanup action;
- update `V2_navigation.md`;
- delete local/remote review branch only after human approval;
- verify that raw artifacts did not enter `main`;
- write final cleanup summary.
```

If Kilo cannot safely delete a branch or cannot confirm remote state, it must produce exact manual instructions and mark cleanup as pending.

#### Human owns irreversible decisions

The human should decide:

```text
- delete or keep remote review branch;
- delete or keep local review branch;
- keep raw response locally or discard it;
- promote sanitized accepted summary to main or not;
- approve any publication-sensitive action.
```

Branch deletion is safer than branch retention by default, but retention can be valid if the branch is still useful for follow-up.

#### Codex owns final acceptance/checkpoint review

Codex should not be the routine cleanup executor. Codex should verify after Kilo cleanup:

```text
- `V2_navigation.md` has the final status;
- branch fate is recorded;
- accepted workflow docs remain consistent;
- no raw V2 runtime artifacts leaked into main;
- implementation result was locally reviewed;
- checkpoint can proceed.
```

#### Recommended cleanup lifecycle

```text
1. Kilo performs `/v2 cleanup preview`.
2. Human chooses: delete / keep / defer.
3. Kilo executes allowed cleanup or gives manual commands if blocked.
4. Kilo updates V2_navigation.
5. Codex verifies final state during checkpoint review.
```

This is the cleanest ownership model because Kilo has local repo context, human controls publication/destructive actions, and Codex verifies the workflow state.

### Must-fix doc changes

1. **Add mandatory post-push checklist**

   In V2 README under `/v2` and `/v2 preview`, add:

   ```text
   After successful V2 push, Kilo must immediately:
   - verify snapshot commit/raw links are reachable;
   - create instantiated prompt in `.ai/external_reviews/prompts/`;
   - include request report, base/snapshot links, compare link, and project docs;
   - show the full copy-paste prompt to the human;
   - update V2 status to `prompt_ready` or `waiting_external_answer`;
   - not finish the run until the prompt is created or a blocked report explains why.
   ```

2. **Add `/v2` interrupt contract**

   Add a section:

   ```text
   `/v2` can be invoked by the user during an active Kilo run.
   This is an interrupt, not a new Kilo mode.
   Kilo must pause normal work, summarize current WIP, run V2 preview, and wait for human approval.
   ```

   This should explicitly differ from `blocked-v2-recommended`.

3. **Clarify state transitions**

   Document the canonical sequence:

   ```text
   draft
   -> previewed
   -> awaiting_human_push_approval
   -> snapshot_pushed
   -> prompt_ready / waiting_external_answer
   -> raw_response_captured or external_answer_pasted
   -> ingested
   -> implementation_planned
   -> implemented
   -> cleaned / kept_by_decision
   ```

   If you do not want new statuses, define the existing statuses more strictly.

4. **Update cleanup contract with ownership**

   Add table:

   ```text
   Kilo: prepares cleanup preview, updates V2_navigation, performs approved deletion.
   Human: approves deletion/retention/publication decisions.
   Codex: verifies cleanup and checkpoints.
   ```

5. **Make `V2_navigation.md` update mandatory**

   Add rules:

   ```text
   After prompt creation: add or update V2 entry.
   After ingest: update status and response/ingest location.
   After implementation: update outcome.
   After cleanup: update branch state and final status.
   ```

6. **Add runtime artifact minimum set**

   Define which artifacts are mandatory and which are optional. For direct-paste external answer, allow:

   ```text
   Response Location: pasted into Kilo run; raw response not stored.
   ```

   But then `ingest_summary` should still exist, or the final report must explicitly say why it does not.

7. **Add path/write fallback**

   Add the tool-level fallback rule for `.ai/external_reviews/...` paths: create directories first, verify exact path, retry safely, and block instead of silently dropping artifacts.

8. **Clarify YOLO gate**

   Add:

   ```text
   `awaiting_human_push_approval` is a valid stop state in YOLO mode.
   Kilo must stop there and not attempt to continue autonomously.
   ```

### Nice-to-have improvements

1. Add a small lifecycle diagram to V2 README.

2. Add `/v2 post-push` as a named checklist, even if it is not a real command.

3. Add `/v2 cleanup preview` as a named checklist before actual deletion.

4. Add `branch_state` allowed values to `V2_navigation.md`:

   ```text
   active
   deleted
   kept_by_decision
   cleanup_pending
   unknown
   ```

5. Add `response_location` and `ingest_location` columns to `V2_navigation.md`.

6. Add one example filled V2 navigation row based on the first real pilot, but only after local review decides what should remain public.

7. Consider a tiny future helper script later, but not now. The current gap can be fixed with docs/checklists first.

### Final verdict

`good with targeted corrections`

V2 is now proven useful: it handled a real editor underlay problem and produced a successful technical outcome. The remaining weakness is not the concept; it is lifecycle discipline. Add a mandatory post-push prompt step, define `/v2` as an interrupt, make navigation and cleanup ownership explicit, and document the runtime artifact minimum set. After those targeted corrections, this V2 process can be considered production-worthy for this workflow, still with manual human gates for publication and cleanup.

## Candidate Navigation Entry

V1-20260526-213514: Senior review of the first real V2 process after the underlay alignment case. Verdict: `good with targeted corrections`; V2 worked technically and produced a successful fix, but docs need lifecycle hardening: mandatory `push -> instantiated prompt`, explicit `/v2` interrupt contract, clear `V2_navigation` updates, hybrid cleanup ownership, runtime artifact minimum set, YOLO push-gate stop rule, and path/write fallback.
