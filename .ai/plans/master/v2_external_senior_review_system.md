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
- tracked V2 artifacts by default;
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
| Artifact tracking | V2 request/prompt/response tracked in GitHub by default |
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

## V2 Protocol Requirements

V2 must define these user-facing commands or command-like instructions:

- `/v2` - prepare external senior review snapshot.
- `/v2 preview` - show what would be included, without commit or push.
- `/v2 ingest` - save external answer and summarize Kilo understanding.
- `/v2 status` - show current V2 request state.
- `/v2 cleanup` - guide cleanup of temporary review branch after human approval.

First implementation may document these commands as manual Kilo protocol. It does not need to implement a CLI.

## Safety Requirements

Before any V2 push, Kilo must:

- inspect tracked changed files;
- inspect untracked files;
- inspect suspicious ignored files when relevant;
- block secrets and private/local-only files;
- report blocked files plainly;
- show files proposed for snapshot;
- ask human confirmation even if safety-check is clean.

Default decision: do not publish risky files.

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

## Implementation Sequence

### Step 0 - Tracker

Create this master plan document.

Expected output:

- `.ai/plans/master/v2_external_senior_review_system.md`

Human review: required.

### Step 1 - Two `/v1` External Checks

Prepare two `/v1` prompts before implementation:

1. Safety/privacy/push-gate review.
2. Kilo usability/workflow clarity review.

Each response must be saved through `Kilo Notebook` into:

- `.ai/external_chats/notebook/`
- `.ai/external_chats/V1_navigation.md`

Codex must review both responses locally before treating anything as planning input.

### Step 2 - Kilo Docs Run 1

Medium Kilo Docs run through `strong_model`.

Scope:

- create V2 protocol docs;
- update repo-level rules for discoverability;
- document that no new Kilo mode exists;
- document human push confirmation;
- document V2 as project-local first.

Recommended model class:

- `strong_model`

Default model:

- `DeepSeek V4 Pro`

Human review: required.

### Step 3 - Kilo Docs Run 2

Medium Kilo Docs run through `strong_model`.

Scope:

- create templates;
- create `V2_navigation.md`;
- ensure templates contain required safety, context, commit, compare, and ingest sections;
- keep helper script out of scope.

Recommended model class:

- `strong_model`

Default model:

- `DeepSeek V4 Pro`

Human review: required.

### Step 4 - Kilo Verifier Run

Read-only verification except report.

Scope:

- verify docs consistency;
- verify no new forbidden Kilo mode values were introduced;
- verify no helper script was created;
- verify `.gitignore` does not hide `.ai/external_reviews/`;
- verify templates contain required sections;
- verify V2 docs do not authorize push without human confirmation.

Recommended model class:

- `strong_model`

Default model:

- `Kimi K2.6`

Reason: executor and verifier should not use the same concrete model for an important workflow task.

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
3. Are tracked V2 artifacts acceptable for this project?
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

## Acceptance Criteria

- Master plan exists and is reviewable.
- `.ai/external_reviews/` structure is defined.
- V2 protocol is discoverable from repo-level rules.
- V2 templates are complete enough for Kilo to use manually.
- Safety-check and always-confirm push gate are explicit.
- V2 prompt rules require honest external readback and base/snapshot separation.
- No helper script or automation is added.
- No new Kilo mode is introduced.
- Human review requirements are explicit.

