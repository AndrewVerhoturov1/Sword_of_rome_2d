# V2 External Senior Review System Plan

## Status

`approved-for-planning`

## Created

2026-05-26

## Goal

Introduce a project-local `/v2` external senior review protocol for Kilo Code. The protocol lets Kilo prepare a safe GitHub-visible WIP snapshot, ask an external chat for grounded technical review, save the response, and propose next actions without letting the external chat edit code or become repo authority.

## Summary

V2 is a manual, strict protocol under `.ai/external_reviews/`.

First implementation is documentation and workflow only:

- no helper script;
- no automated push;
- no new Kilo mode;
- no direct code-fixing after external answer;
- tracked protocol/templates by default, but not raw V2 runtime artifacts in `main`;
- same GitHub repo review branches;
- mandatory human confirmation before every V2 push.

V2 is separate from `/v1`:

- `/v1` is prompt-only planning/critique route;
- `/v2` is WIP snapshot review route;
- `/v2` gives external chat pinned base/snapshot links and compare context;
- `/v2` requires stronger safety rules because it publishes working code.

## Fixed Decisions

| Topic | Decision |
|---|---|
| Storage | `.ai/external_reviews/` |
| First scope | docs/templates/rules only |
| Helper script | not included in first version |
| Kilo mode | no new Kilo mode |
| Typical Kilo mode | `Kilo Debugger` for stuck/debug cases, `Kilo Handoff Runner` for docs/protocol work |
| Artifact tracking | track protocol docs, templates, navigation, and sanitized accepted summaries in `main`; keep raw V2 runtime artifacts out of `main` by default |
| Review branch target | current repo `AndrewVerhoturov1/Sword_of_rome_2d` |
| Review branch format | `review/v2/YYYYMMDD-HHMMSS-short-topic` |
| Push gate | Kilo must always ask human confirmation before V2 push |
| External response authority | planning/debug input only, not accepted fact without local verification |
| Human review | required for every main V2 document before acceptance |

## Required Files

Create the project-local V2 area:

```text
.ai/
  external_reviews/
    README.md
    V2_navigation.md
    templates/
      v2_request_template.md
      v2_prompt_template.md
      v2_response_template.md
      v2_ingest_summary_template.md
      v2_safety_checklist.md
```

Update repo-level discovery and workflow rules:

- `AGENTS.md`
- `.ai/repo_navigation.md`
- `.ai/rules/agent_protocol.md`
- `.ai/rules/kilo_mode_contract.md`
- relevant `.ai/prompts/` files if they mention external routes, Kilo mode rules, or shortcut commands.

Do not create automation scripts in first implementation.

## Artifact Classes

V2 must distinguish artifact classes explicitly.

### Public and stable in `main`

- `.ai/external_reviews/README.md`
- `.ai/external_reviews/V2_navigation.md`
- `.ai/external_reviews/templates/*`
- sanitized accepted summaries, if the user decides they belong in project history

### Runtime artifacts for active V2 work

- request report
- generated prompt
- changed-file inventory
- safety report
- temporary screenshots approved for this review

Default rule:

- these may live in `review/v2/...` branch for the active review;
- they are not tracked in `main` by default.

### Raw response and ingest artifacts

- raw external answer
- Kilo understanding summary
- implementation-plan draft based on the answer

Default rule:

- raw response is not tracked in `main` by default;
- only sanitized accepted summary may be promoted later.

## V2 Protocol Requirements

V2 must define these user-facing commands or command-like instructions:

- `/v2` - prepare external senior review snapshot.
- `/v2 preview` - show what would be included, without commit or push.
- `/v2 ingest` - process an already-captured external answer and summarize Kilo understanding.
- `/v2 status` - show current V2 request state.
- `/v2 cleanup` - guide cleanup of temporary review branch after human approval.

First implementation may document these commands as manual Kilo protocol. It does not need to implement a CLI.

## V2 Status Lifecycle

V2 should define a compact status model:

- `draft`
- `previewed`
- `awaiting_human_push_approval`
- `snapshot_pushed`
- `waiting_external_answer`
- `raw_response_captured`
- `ingested`
- `implementation_planned`
- `implemented`
- `superseded`
- `cleaned`

`/v2 status` and `V2_navigation.md` should use the same vocabulary.

## Safety Requirements

Before any V2 push, Kilo must:

- inspect tracked changed files;
- inspect untracked files;
- inspect suspicious ignored files when relevant;
- block secrets and private/local-only files;
- report blocked files plainly;
- show files proposed for snapshot;
- show branch name, base branch, base commit, and exact files proposed for push;
- show large/binary file hits and local-only path hits;
- ask human confirmation even if safety-check is clean.

Default decision: do not publish risky files.

Human confirmation must not be a vague "push?" question. The confirmation packet must include:

- review branch name;
- base branch;
- base commit;
- changed tracked files;
- untracked files;
- suspicious ignored files;
- blocked files;
- large/binary files;
- local-only path hits;
- exact files that will be pushed;
- exact files excluded from push;
- a simple Russian yes/no decision prompt.

Blocked or high-risk examples:

- `.env`, `.env.*`
- key/certificate/credential files;
- files under `_local/`;
- generated output and build artifacts;
- private images/assets;
- archives;
- logs;
- large binary files unless explicitly approved.

## External Chat Requirements

The V2 prompt must require external chat to:

- read V2 request report first;
- inspect WIP files at snapshot commit;
- compare against base files at base commit;
- keep base/snapshot distinction explicit;
- prefer commit-pinned links; branch links are supplemental only;
- list what it read in `Context Readback`;
- separate verified facts from hypotheses;
- avoid claiming local runtime, tests, shell, or git status;
- avoid direct code patches as if it had local repo access;
- give bounded senior technical advice;
- state missing context and uncertainty.

Required response shape must include:

- `V2 ID`
- `Context Readback`
- `Provider/Model`
- `Answer`
- `Confirmed from central docs`
- `Confirmed from project docs`
- `Confirmed from WIP snapshot`
- `Confirmed from base comparison`
- `Not available / not verified`
- `Main assessment`
- `Root cause hypothesis`
- `Recommended correction path`
- `Risks`
- `Suggested implementation notes`
- `Questions back to Kilo/user, if any`
- `Candidate Navigation Entry`

## V2 Ingest Boundary

The first implementation must not blur `kilo-recorder` and ordinary interpretation work.

V2 default boundary:

1. raw external answer is captured first as a narrow recording step;
2. a separate ordinary Kilo continuation reads that captured response;
3. only that second step writes Kilo understanding and proposed implementation plan.

This keeps existing `kilo-recorder` contract intact. First implementation should document this split clearly instead of inventing a new Kilo mode.

## Implementation Sequence

### Step 0 - Tracker

Create this master plan document.

Expected output:

- `.ai/plans/master/v2_external_senior_review_system.md`

Human review: required.

### Step 1 - Revise Plan Before Implementation

Use the accepted external critique to tighten:

- artifact tracking policy;
- ingest/recorder boundary;
- push confirmation packet;
- commit-pinned link requirement;
- status lifecycle;
- cleanup expectations;
- rollout size.

### Step 2 - Kilo Docs Run

One medium-to-large Kilo Docs run through `strong_model`.

Scope:

- create V2 protocol docs;
- update repo-level rules for discoverability;
- define artifact classes and default storage rules;
- document that no new Kilo mode exists;
- document human push confirmation;
- document V2 as project-local first;
- document raw-response capture vs ingest summary split.

Recommended model class:

- `strong_model`

Default model:

- `DeepSeek V4 Pro`

Human review: required.

### Step 3 - Kilo Verifier Run

Read-only verification except report.

Scope:

- verify docs consistency;
- verify no new forbidden Kilo mode values were introduced;
- verify no helper script was created;
- verify `.gitignore` does not hide `.ai/external_reviews/`;
- verify templates contain required sections;
- verify V2 docs do not authorize push without human confirmation;
- verify raw V2 request/response artifacts are not tracked in `main` by default;
- verify V2 docs do not silently bypass existing recorder boundaries.

Recommended model class:

- `strong_model`

Default model:

- `Kimi K2.6`

Reason: executor and verifier should not use the same concrete model for an important workflow task.

### Step 4 - Human Review

Human review is required before acceptance of the docs patch. The review should check whether:

- `/v2`, `/v2 preview`, `/v2 ingest`, `/v2 status`, `/v2 cleanup` are understandable in simple Russian;
- the push gate is strict enough;
- the artifact storage rules are acceptable;
- the manual workflow is realistic without helper scripts.

### Step 5 - Codex Final Review

Codex verifies:

- Kilo reports;
- actual diff;
- file presence;
- rule consistency;
- search checks;
- `git status`;
- required `Human Check` and `Баги и сложности` sections.

Checkpoint commit only after accepted result.

### Step 6 - Low-Risk Manual Pilot

After docs acceptance, run one low-risk manual pilot:

- start with `/v2 preview`;
- use a non-secret issue only;
- push only after explicit human approval;
- capture what was awkward in the manual flow;
- decide after the pilot whether a tiny helper script is justified.

## Verification Commands

Run after implementation:

```powershell
git status --short --branch
rg -n "/v2|external_reviews|V2_navigation" AGENTS.md .ai
rg -n "kilo-v2|Kilo V2|kilo-builder|kilo-docs|kilo-tester|kilo-refactor" AGENTS.md .ai
```

Manual checks:

- `.gitignore` must not ignore `.ai/external_reviews/`.
- V2 templates must include `V2 ID`, base commit, snapshot commit, compare link, changed files, safety status, `Context Readback`, `Provider/Model`, and verified/not verified separation.
- V2 docs must state: no push without human confirmation, no secrets/private assets, no automatic fixes after external answer, no new Kilo mode, no helper script in first implementation.
- V2 docs must state that commit-pinned links are primary and branch links are supplemental only.
- V2 docs must distinguish public templates from raw V2 runtime artifacts.
- V2 docs must define the raw-response capture vs ingest-summary split.

## Human Review Points

Human review is required for:

- this master plan;
- V2 README/protocol;
- V2 external chat rules;
- V2 templates;
- any repo-level rules that change Kilo behavior;
- any future decision to add automation.

The user should check:

1. Does V2 match intended workflow?
2. Is the human push gate strict enough?
3. Are the `main` vs review-branch vs raw-response storage rules acceptable for this project?
4. Are Kilo instructions simple enough for manual use?
5. Are there missing safety risks around private images, local-only folders, or WIP branches?

## Out Of Scope For First Implementation

- CLI command for `/v2`.
- Automatic branch creation.
- Automatic commit/push.
- Automatic raw link generation.
- Automatic ingest parsing.
- Draft PR creation.
- Central workflow-core generalization.
- New Kilo mode or UI setup.
- Tracking raw V2 request/response artifacts in `main` by default.

## Acceptance Criteria

- Master plan exists and is reviewable.
- `.ai/external_reviews/` structure is defined.
- V2 protocol is discoverable from repo-level rules.
- V2 templates are complete enough for Kilo to use manually.
- Safety-check and always-confirm push gate are explicit.
- V2 prompt rules require honest external readback and base/snapshot separation.
- V2 artifact classes and default storage rules are explicit.
- V2 ingest boundary does not conflict silently with existing recorder contract.
- No helper script or automation is added.
- No new Kilo mode is introduced.
- Human review requirements are explicit.
