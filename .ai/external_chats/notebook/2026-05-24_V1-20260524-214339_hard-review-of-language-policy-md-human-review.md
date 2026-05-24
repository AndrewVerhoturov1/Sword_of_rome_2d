# Notebook Entry

- External Question ID: `V1-20260524-214339`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-24_V1-20260524-214339_hard-review-of-language-policy-md-human-review.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/implementation/first_product_code_block.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/policies/language_policy.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/policies/human_review_policy.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/policies/bug_tracking_policy.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/logs/bug_journal.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`

## Candidate Navigation Entry

Topic: Hard review of `language_policy.md`, `human_review_policy.md`, and `bug_tracking_policy.md`
Summary: Verdict: policy layer is useful and well-aligned, but should be tightened with small changes: require checking bug journal before debugging, make verification concrete, clarify failed human-check handling, clarify human-check vs bug-journal boundary, and cover language gray zones without adding heavy bureaucracy.

## Raw Response

# Raw External Response

## External Question ID

V1-20260524-214339

## Context Readback

* Uploaded prompt / `Вставленный текст(22).txt`: fully read. 
* `external_chat_rules.md`: fully read. ([GitHub][1])
* Central `repo_navigation.md`: fully read. ([GitHub][2])
* Project `README.md`: fully read. ([GitHub][3])
* Project `AGENTS.md`: fully read. ([GitHub][4])
* Project `.ai/repo_navigation.md`: fully read. ([GitHub][5])
* Project `.ai/plans/implementation/first_product_code_block.md`: fully read. ([GitHub][6])
* Project `.ai/policies/language_policy.md`: fully read. ([GitHub][7])
* Project `.ai/policies/human_review_policy.md`: fully read. ([GitHub][8])
* Project `.ai/policies/bug_tracking_policy.md`: fully read. ([GitHub][9])
* Project `.ai/logs/bug_journal.md`: fully read. ([GitHub][10])
* Project `.ai/external_chats/V1_navigation.md`: fully read. ([GitHub][11])
* Navigation-discovered central links: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

`external_chat_rules.md` requires exact `External Question ID`, honest `Context Readback`, source separation, and no unsupported claims about local repo/runtime/tests. It also requires the answer to separate central-doc conclusions, provided/project conclusions, and not-verified items. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation does not authorize claims about the consumer repo unless those project files are explicitly provided. Here, the policy files and related project docs were explicitly provided and opened. ([GitHub][2])

### Confirmed from provided excerpts

The project has added three policy files: `language_policy.md`, `human_review_policy.md`, and `bug_tracking_policy.md`, plus links from `AGENTS.md`, `.ai/repo_navigation.md`, and the first implementation brief. `AGENTS.md` now tells agents to use English technical identifiers, Russian user-facing UI/docs, include a `Human Check` section, and include a `Баги и сложности` section in implementation/QA/Codex/Kilo reports. ([GitHub][4])

`language_policy.md` already gives the core split: English for folder/file names, TypeScript identifiers, JSON keys, IDs, enum values, action/event types, schema names and runtime/core terminology; Russian for UI labels, buttons, tooltips, user messages, visible names, help text, and docs for the Russian-speaking project owner. It also explicitly forbids transliteration and says not to mass-translate old docs. ([GitHub][7])

`human_review_policy.md` already defines required/suggested/not-needed human review, requires simple Russian, gives a template, and says work needing human review should be marked `pending human check` until the user confirms it. ([GitHub][8])

`bug_tracking_policy.md` already requires every implementation/QA/Kilo/Codex report to include `Баги и сложности`, defines report statuses, gives a bug journal format, requires simple Russian, and connects visible/UI bugs to the human review policy. ([GitHub][9])

`bug_journal.md` is not just empty: it already contains a useful real entry about the Phaser canvas disappearing under React StrictMode double-mount, including symptoms, cause, fix, verification, human check status, related files, and notes for future agents. ([GitHub][10])

### Not available / not verified

I did not run local validators, inspect git diff, execute Codex/Kilo flows, or verify whether future handoff/report templates already enforce these sections automatically. I also did not inspect every workflow template under `.ai/templates/` or `.ai/prompts/`, so template-level coverage is not verified.

### Main assessment

The policy layer is **good and already useful**, especially for the project's current maturity. It correctly covers the three biggest workflow risks: mixed Russian/English technical naming, silent skipping of human visual checks, and lost debugging knowledge.

The main weakness is not the intent. The intent is strong. The weak point is **enforcement consistency**: agents can still produce formally compliant but low-value reports unless the policies add a few sharper rules about verification details, journal lookup, and failed human checks.

### Strong parts

1. **The three policies are conceptually well separated.**
   Language policy governs naming and text language. Human review policy governs when the human must look at visible/browser/UX results. Bug tracking policy governs how problems are reported and when they go into the journal. This is a clean split. ([GitHub][7])

2. **They are linked from the right high-level places.**
   `AGENTS.md` includes all three policy concepts, and `.ai/repo_navigation.md` lists the policy files and bug journal under the workflow layer. That makes them discoverable for future agents. ([GitHub][4])

3. **They protect the user's real needs.**
   Human review instructions must be in simple Russian, and bug reports must avoid developer jargon. That directly matches the user's requirement that agents explain checks and problems plainly. ([GitHub][8])

4. **The first implementation brief already applies the policies to the current block.**
   `first_product_code_block.md` has sections for language, human check, and bug tracking, including examples and first-block-specific risks such as Phaser visibility, double boot, layout, input, JSON fixture consistency, and GameState/Action/Event boundaries. ([GitHub][6])

5. **The bug journal already proves the idea works.**
   The existing `BUG-20260524-001` entry is exactly the kind of practical memory future agents need: symptom, cause, fix, verification, related files, and future-agent note. ([GitHub][10])

### Weak spots / gaps

1. **Bug journal lookup is not mandatory yet.**
   The bug policy says important/repeatable problems must be recorded, but it does not explicitly say: before debugging a problem, search or inspect `.ai/logs/bug_journal.md` for similar symptoms. That was one of the user's goals: future agents should be able to find repeated solutions. Without a "check the journal first" rule, agents may keep adding fixes without learning from old entries.

2. **Verification can be too vague.**
   The bug report template has `Verification: [чем проверено]`, but it does not forbid useless text like "checked" or "seems fine." This can become formal compliance with no real value. It should require either actual commands/checks, human check status, or an explicit "not run / not checked".

3. **Human review and bug tracking overlap, but the failure path is not explicit enough.**
   Bug policy points to human review when a bug affects visible UI, and human review says pending confirmation blocks full acceptance. But neither policy clearly says: if the user reports that the human check failed, the agent must treat that as a bug/difficulty and record it in the task report, and possibly in the bug journal.

4. **The language policy does not explicitly cover comments/debug text/test names.**
   It covers technical identifiers and user-facing text well, but common gray zones remain: code comments, console/debug labels, test titles, commit-like report names, and fixture `name`/`description` fields. The first implementation brief partly covers user-facing debug labels, but the policy itself could be clearer. ([GitHub][7])

5. **The human review policy may be too broad around Russian text.**
   It says human review is required for user-facing Russian labels/messages/tooltips. That is correct for app UI, but if every small docs copy change or README wording triggers required human check, agents may overuse it. The policy needs one line clarifying that app-visible/user-facing product text is required; ordinary docs wording is usually suggested or not needed unless acceptance depends on the wording.

6. **Bug journal entry IDs can collide.**
   `BUG-YYYYMMDD-NNN` is good, but the policy does not say how to choose the next `NNN` when multiple agents work on the same day. It should say: inspect existing entries for that date and use the next available number; never renumber older entries.

### Conflicts / ambiguities

1. **`Human Check` status vs `Баги и сложности` status use overlapping states.**
   Human review uses `required / suggested / not needed`, while bug tracking uses `none / fixed / open / pending human check`. This is not a conflict, but agents may confuse the two. A report can have `Human Check: required` and `Баги и сложности: none`, or `Human Check: pending human check` and `Баги и сложности: pending human check`. The difference should be clarified: one is about human validation, the other is about problems encountered.

2. **Human check does not always mean bug journal.**
   Bug policy says journal when a human had to verify the fix, but human review policy makes many visual changes require human review. If interpreted literally, this could flood the bug journal. Better wording: human verification alone does not require a journal entry; journal entry is needed when the issue was non-obvious, repeated, fixed with a workaround, or useful for future debugging.

3. **Docs-only changes are "usually not needed" for human review, but language policy cares about readable Russian.**
   This is okay, but the boundary should be explicit: docs-only Russian text generally does not need mandatory human check unless it is user-facing instructions, acceptance-critical wording, or the user specifically asked to review wording.

4. **Policies are strong, but report templates may not enforce them.**
   I did not verify `.ai/templates/` or report-generation prompts. If agents use older templates without the required sections, the policies may be forgotten despite being correct.

### Must-fix now

These are small wording changes, not a new process.

1. **Add "check bug journal before debugging" to `bug_tracking_policy.md`.**
   Suggested rule: before working on a bug or recurring difficulty, inspect `.ai/logs/bug_journal.md` for similar symptoms, especially for Phaser/React, layout, build/typecheck, fixture/JSON, and workflow issues.

2. **Strengthen `Verification` wording in `bug_tracking_policy.md`.**
   Require concrete verification: command names, test names, browser/manual check, human check status, or explicit `not run / not verified`. Forbid vague "checked" without details.

3. **Clarify failed human check path.**
   Add to both human/bug policies or just bug policy: if the user reports a failed human check, treat it as `Баги и сложности: open` or `fixed` after correction; if repeatable/non-obvious, add or update bug journal.

4. **Clarify human-check vs journal boundary.**
   Add: human check alone does not automatically require bug journal. Journal is for important/repeated/non-obvious problems or useful fixes.

5. **Clarify language gray zones.**
   Add one compact paragraph: code comments may be Russian if explanatory, but public technical names stay English; fixture `name`/`title`/`description` display fields may be Russian; test names should prefer English technical terms plus Russian description only if useful.

### Nice-to-have later

1. Add the required `Human Check` and `Баги и сложности` sections to any Kilo/Codex report templates, if they are not already there.

2. Add a tiny "policy compliance checklist" to future handoff templates: language policy observed, human check section included, bugs/difficulties section included, bug journal checked/updated if relevant.

3. Add a short "known bug lookup" heading at the top of `bug_journal.md`, with areas/tags like `Phaser`, `React StrictMode`, `layout`, `fixtures`, `JSON`, `workflow`.

4. Add examples of good/bad `Баги и сложности` sections, similar to the examples already in the human review and bug policies.

### What Codex should change now

1. In `.ai/policies/bug_tracking_policy.md`, add a rule: before debugging or investigating a repeated problem, check `.ai/logs/bug_journal.md` for similar symptoms.

2. In `.ai/policies/bug_tracking_policy.md`, strengthen `Verification`: it must list actual commands/checks/human confirmation, or explicitly say `not run / not verified`.

3. In `.ai/policies/bug_tracking_policy.md`, clarify: failed human check must be treated as a bug/difficulty; but human check alone does not automatically require a bug journal entry.

4. In `.ai/policies/language_policy.md`, add gray-zone guidance for comments, fixture display fields, debug labels, and test names.

5. In `.ai/policies/human_review_policy.md`, clarify that required human review for Russian text means app-visible/user-facing product text; ordinary docs-only wording is usually suggested/not needed unless acceptance depends on it.

### What not to overdo

Do not create a heavy governance system. Do not force every small typo into the bug journal. Do not require human review for every docs-only or JSON-only task. Do not mass-translate old Russian planning docs. Do not add a big QA database or issue tracker before the project needs it. Do not make agents spend more time filling forms than doing the small Kilo task.

The current policy layer is already strong enough to use. It only needs sharper wording in a few places so agents cannot "technically comply" while producing useless reports.

## Candidate Navigation Entry

V1-20260524-214339: Hard review of `language_policy.md`, `human_review_policy.md`, and `bug_tracking_policy.md`. Verdict: policy layer is useful and well-aligned, but should be tightened with small changes: require checking bug journal before debugging, make verification concrete, clarify failed human-check handling, clarify human-check vs bug-journal boundary, and cover language gray zones without adding heavy bureaucracy.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/implementation/first_product_code_block.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/policies/language_policy.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/policies/human_review_policy.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/policies/bug_tracking_policy.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/logs/bug_journal.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
