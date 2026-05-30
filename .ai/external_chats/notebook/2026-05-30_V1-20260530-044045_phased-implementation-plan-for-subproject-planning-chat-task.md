# Notebook Entry

- External Question ID: `V1-20260530-044045`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-30_V1-20260530-044045_phased-implementation-plan-for-subproject-planning-chat-task.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/prompts/create_block_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/prompts/create_block_orchestrator_package.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/prompts/review_block_report.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/README.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/templates/block_context_pack_template.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/rules/agent_protocol.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/templates/block_report_template.md`

## Candidate Navigation Entry

Topic: phased implementation plan for `Subproject -> Planning Chat -> Task Control Pack -> Boss -> B1 -> Junior -> Kilo/V1/V2/V3`
Summary: Вывод: в project repo уже есть сильный B1 scaffold, но rollout должен идти через project-local subproject/taskspace skeleton, Task Control Pack/Boss bootstrap, один docs-only B1 pilot с полным report/review, затем hardening и только потом promotion reusable parts в central core.

## Raw Response

## External Question ID

V1-20260530-044045

## Context Readback

* Central `external_chat_rules.md`: fully read
* Central `repo_navigation.md`: fully read
* Central navigation-discovered `README.md`: fully read
* Central navigation-discovered `prompts/create_block_plan.md`: fully read
* Central navigation-discovered `prompts/create_block_orchestrator_package.md`: fully read
* Central navigation-discovered `prompts/review_block_report.md`: fully read
* Central navigation-discovered `templates/block_plan_template.md`: fully read
* Central navigation-discovered `templates/block_context_pack_template.md`: fully read
* Central navigation-discovered `templates/block_report_template.md`: fully read
* Central navigation-discovered `templates/block_orchestrator_package_template.md`: fully read
* Project `.ai/repo_navigation.md`: fully read
* Project `README.md`: fully read
* Project `AGENTS.md`: fully read
* Project `.ai/README.md`: fully read
* Project `.ai/rules/agent_protocol.md`: fully read
* Project `.ai/rules/codex_orchestrator.md`: fully read
* Project `.ai/prompts/create_block_plan.md`: fully read
* Project `.ai/prompts/create_block_orchestrator_package.md`: fully read
* Project `.ai/prompts/review_block_report.md`: fully read
* Project `.ai/templates/block_plan_template.md`: fully read
* Project `.ai/templates/block_context_pack_template.md`: fully read
* Project `.ai/templates/block_report_template.md`: fully read
* Project `.ai/templates/block_orchestrator_package_template.md`: fully read
* Project V3 rollout precedent `.ai/plans/master/v3_workflow_implementation_plan.md`: not read — raw URL returned 404
* Project V3 contract precedent `.ai/plans/master/v3_artifact_producing_workflow_contract.md`: not read — raw URL returned 404
* Project `.ai/external_chats/V1_navigation.md`: fully read
* Uploaded idea file `hierarchical_ai_development_system_with_subproject(2).md`: fully read via uploaded file
* Uploaded B1 audit report `2026-05-30_V1-20260530-042120_audit-b1-block-orchestration-layer.md`: fully read via uploaded file
* Provided Context Excerpts: fully read

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require a grounded answer with honest readback, explicit separation between central docs, provided excerpts, and unverified areas; they also prohibit claiming local repo access, git checks, tests, or runtime verification unless those were actually provided. This answer follows that boundary: I am using opened raw links, uploaded files, and provided excerpts, not pretending to have local shell access to the repo. ([GitHub][1])

Central `repo_navigation.md` confirms that `ai-workflow-core` is the reusable core: it contains stable rules, prompts, templates, scripts, and external-chat materials, but not consumer repo runtime/history artifacts or project-specific state. So central core should be treated as reusable baseline, not as proof that the current consumer repo has already run B1/Boss/subproject workflow. ([GitHub][2])

Central core already has the important B1 primitives: `create_block_plan`, `create_block_orchestrator_package`, `review_block_report`, and block templates. The central `create_block_plan` defines `/b1` as planning-only, requires a Block Orchestrator Chat, 2–4 planned agent calls, separation between planned work and repair/contingency, and no execution before approval. ([GitHub][3])

Central and project versions of the Block Orchestrator Package contract both enforce the same key gate: Main Execution Orchestrator must not jump straight to Kilo handoff or external package; it must first create a `Block Orchestrator Package` and use it to hire the junior Block Orchestrator. ([GitHub][4])

Central `review_block_report.md` gives the review gate: Block Report must be checked against Block Plan, Context Pack, actual changed files, Kilo reports if any, allowed scope, acceptance criteria, agent-first evidence, and Block Orchestrator Package usage. That is already a strong reusable acceptance pattern for B1. ([GitHub][5])

### Confirmed from provided excerpts

The current project repo already has a strong B1 scaffold: project-local prompts, templates, role separation, package gate, and review prompt. The uploaded B1 audit says the missing part is not "write B1 from zero," but to prove it operationally: subproject/taskspace structure, Task Control Pack/Boss bootstrap, block index/status layer, real block reports/package examples, and ID linkage across B1 ↔ V1/V2/V3/Kilo artifacts.

The uploaded idea doc defines the target hierarchy as `Repository -> Subproject -> Planning Chat -> Task Control Pack -> Boss Orchestrator -> B1 Block Chats -> Junior Orchestrators -> Kilo / V1 / V2 / V3 / local checks`, and explains that a subproject is a long-lived operational container for related plans, chats, reports, decisions, and external materials.

Project `.ai/README.md` confirms the two-repo model: central core is canonical for shared reusable workflow, while consumer repos use raw references and local copies; it also says local copies of core rules/prompts/scripts can be synchronized into the consumer layout. This means the right rollout path is: prove project-local workflow first, then promote stable parts back to core. ([GitHub][6])

Project `AGENTS.md` and `.ai/rules/agent_protocol.md` already contain the operational B1/Boss boundaries: Block Orchestrator is orchestrator-only, execution goes through Kilo Code or External Web Chat, repo lookup/test discovery inside a block counts as substantive work and should go through Kilo, and the Block Orchestrator Package is mandatory before executor handoff. ([GitHub][7])

The V3 rollout/contract raw URLs from the prompt returned 404, so I cannot honestly cite those two files as read. I can still use the provided prompt/excerpts and your described V3 precedent as planning input, but not as verified opened source.

#### 1. Target-state summary

После rollout в этом repo система должна выглядеть так:

```text
.ai/subprojects/
  SP-YYYYMMDD-slug/
    SUBPROJECT_STATE.md
    FULL_PLAN.md
    SHORT_PLAN.md
    BLOCKS_INDEX.md
    DECISION_LOG.md
    SESSION_JOURNAL.md
    TASK_CONTROL_PACK.md или task_control_pack/
    BOSS_BOOTSTRAP.md
    blocks/
      B1-001_slug/
        HANDOFF.md
        BLOCK_PLAN.md
        CONTEXT_PACK.md
        ORCHESTRATOR_PACKAGE.md
        BLOCK_REPORT.md
        BOSS_REVIEW.md
    external/
      v1/
      v2/
      v3/
    kilo/
      reports/
    final/
      FINAL_REPORT.md
```

Главный смысл: **не заменить существующие B1 templates, а дать им "дом" уровня подпроекта**. Existing block templates остаются рабочими артефактами блока, а новый subproject/taskspace layer связывает их с Boss, planning, V1/V2/V3/Kilo reports, decisions и final report.

#### 2. Phase map

##### Phase 0 — Source boundary and rollout baseline

**Цель:** зафиксировать, от чего стартуем: B1 scaffold есть, реального доказанного B1-run нет.

**Почему сейчас:** без этого легко снова начать "аудит с нуля" или ошибочно считать scaffold уже рабочей системой.

**Deliverables:**

* `SP_ROLLOUT_BASELINE.md` или секция в будущем `FULL_PLAN.md`;
* список reused artifacts: existing B1 prompts/templates, agent protocol, Codex orchestrator rules;
* список gaps из B1 audit.

**Тип:** consumer repo + manual setup.

**Dependencies:** загруженный B1 audit, project `.ai/README.md`, `AGENTS.md`, `agent_protocol.md`.

**Acceptance gate:** есть короткая baseline-запись: "что уже есть / что scaffold-only / что не доказано".

**Risks / anti-patterns:**
Не делать новый большой audit. Не утверждать, что B1 proven. Не считать central core единственным источником правды.

---

##### Phase 1 — Minimal subproject/taskspace skeleton

**Цель:** создать операционный дом для одной большой работы.

**Почему здесь:** без `.ai/subprojects/...` или аналога все B1/V1/V2/V3/Kilo artifacts опять смешаются в общей `.ai`.

**Deliverables:**

* `.ai/subprojects/README.md`;
* `.ai/subprojects/SP-YYYYMMDD-b1-boss-orchestration-rollout/`;
* `SUBPROJECT_STATE.md`;
* `SHORT_PLAN.md`;
* `BLOCKS_INDEX.md`;
* `DECISION_LOG.md`;
* `SESSION_JOURNAL.md`.

**Тип:** consumer repo.

**Dependencies:** concept doc + B1 audit gaps.

**Acceptance gate:** новый чат может открыть только `SUBPROJECT_STATE.md`, `SHORT_PLAN.md`, `BLOCKS_INDEX.md` и понять текущий статус без чтения всего repo.

**Risks / anti-patterns:**
Не добавлять каждый runtime artifact в root `repo_navigation.md`: project `.ai/README.md` уже говорит, что временные workflow artifacts, включая B1 artifacts, не должны попадать в `repo_navigation.md` по умолчанию. ([GitHub][6])

---

##### Phase 2 — Task Control Pack minimal contract

**Цель:** оформить bridge между Planning Chat и Boss Orchestrator.

**Почему здесь:** existing B1 templates работают на уровне одного блока, но audit gap говорит, что нет целостного `Task Control Pack`/Boss bootstrap уровня большой задачи.

**Deliverables:**

* `TASK_CONTROL_PACK.md` или папка `task_control_pack/`;
* `FULL_PLAN.md`;
* `SHORT_PLAN.md`;
* `BLOCKS_INDEX.md`;
* `BOSS_BOOTSTRAP.md`;
* `blocks/B1-001.../HANDOFF.md`;
* начальный `SESSION_JOURNAL.md`.

**Тип:** consumer repo first; central core later.

**Dependencies:** Phase 1.

**Acceptance gate:** можно открыть новый Boss Chat, передать ему только `BOSS_BOOTSTRAP.md` + short docs, и он понимает: цель подпроекта, scope, первый блок, что читать, что не читать, что делать после block report.

**Risks / anti-patterns:**
Не превращать Task Control Pack в огромный dump planning chat. Context Pack template прямо запрещает включать полную историю planning chat, rejected decisions и контекст других блоков без необходимости. ([GitHub][8])

---

##### Phase 3 — Boss Orchestrator operating contract

**Цель:** формализовать, что Boss делает между блоками.

**Почему здесь:** B1 scaffold уже знает, как блок планировать и ревьюить, но Boss-level loop ещё не закреплён как рабочий процесс.

**Deliverables:**

* `BOSS_BOOTSTRAP.md`;
* секция `Boss Duties` в `SUBPROJECT_STATE.md` или отдельный `BOSS_OPERATING_NOTES.md`;
* правило обновления `SHORT_PLAN.md`, `BLOCKS_INDEX.md`, `SESSION_JOURNAL.md`, `DECISION_LOG.md`;
* format для `BOSS_REVIEW.md`.

**Тип:** consumer repo + manual setup.

**Dependencies:** Phase 2.

**Acceptance gate:** после каждого `BLOCK_REPORT.md` Boss обязан:

1. сверить report с plan/context;
2. принять / вернуть / заблокировать;
3. обновить `BLOCKS_INDEX.md`;
4. обновить `SESSION_JOURNAL.md`;
5. при изменении курса обновить `SHORT_PLAN.md` и `DECISION_LOG.md`.

**Risks / anti-patterns:**
Boss не должен автоматически доверять B1. Boss не должен становиться executor. Boss не должен сопровождать каждый внутренний шаг младшего оркестратора — project rules уже закрепляют senior non-interference и review-point подход. ([GitHub][9])

---

##### Phase 4 — B1 block integration with existing templates

**Цель:** встроить существующие B1 prompts/templates внутрь subproject structure.

**Почему здесь:** не нужно переписывать B1 scaffold; нужно связать его с `Subproject ID`, `Block ID`, Boss session и artifacts.

**Deliverables для каждого блока:**

* `BLOCK_PLAN.md` на базе existing `block_plan_template.md`;
* `CONTEXT_PACK.md`;
* `ORCHESTRATOR_PACKAGE.md`;
* `BLOCK_REPORT.md`;
* `BOSS_REVIEW.md`.

**Тип:** consumer repo.

**Dependencies:** Phase 1–3.

**Acceptance gate:** `BLOCK_PLAN.md` содержит allowed/forbidden files, required/lookup inputs, context budget, execution mandate, planned agent sequence, human checkpoints, stop conditions, report path. Existing template уже поддерживает эти поля. ([GitHub][10])

**Risks / anti-patterns:**
Не менять все templates сразу. Сначала добавить ID/linkage metadata поверх существующих templates. Не ломать текущий `BLOCK-NNN_short_name` формат без пилота.

---

##### Phase 5 — First real B1/Boss/subproject pilot

**Цель:** доказать, что система реально работает, а не только описана.

**Почему здесь:** audit прямо говорит, что published evidence реального B1-run не найдено; значит первый pilot — главный missing proof.

**Deliverables:**

* один реальный subproject folder;
* один `Task Control Pack`;
* один `BOSS_BOOTSTRAP.md`;
* один `B1-001` block;
* один `ORCHESTRATOR_PACKAGE.md`;
* один executor artifact: Kilo handoff или external request;
* один executor report;
* один `BLOCK_REPORT.md`;
* один `BOSS_REVIEW.md`;
* обновлённые `BLOCKS_INDEX.md`, `SESSION_JOURNAL.md`, `DECISION_LOG.md`.

**Тип:** pilot / verification / acceptance.

**Dependencies:** Phase 1–4.

**Acceptance gate:** можно показать цепочку доказательств:

```text
Subproject ID
→ Boss bootstrap
→ Block index
→ B1-001 handoff/plan/context
→ Block Orchestrator Package
→ executor run
→ executor report
→ Block Report
→ Boss Review
→ updated short plan/journal
```

**Risks / anti-patterns:**
Не выбирать product-code или UI-heavy block первым. Первый pilot лучше docs/workflow-only, чтобы проверять orchestration, а не отлаживать приложение.

---

##### Phase 6 — Post-pilot hardening

**Цель:** исправить то, что сломалось в первом реальном прогоне.

**Почему здесь:** до pilot нельзя точно знать, какие поля лишние, какие нужны, где человек путается, где Kilo забывает путь, где Boss слишком много читает.

**Deliverables:**

* `PILOT_RETROSPECTIVE.md`;
* обновлённые local templates;
* 1–2 example filled artifacts;
* checklist "before next B1 block";
* уточнённая navigation policy.

**Тип:** consumer repo + pilot acceptance.

**Dependencies:** Phase 5.

**Acceptance gate:** второй B1-block можно стартовать без переписывания правил вручную в prompt.

**Risks / anti-patterns:**
Не тащить в central core сырые lessons сразу. Сначала один исправленный локальный повтор или хотя бы local retrospective.

---

##### Phase 7 — V1/V2/V3/Kilo linkage layer

**Цель:** связать external/material artifacts с Subproject/Block IDs.

**Почему после pilot:** до первого pilot неясно, какие IDs реально удобны.

**Deliverables:**

* metadata block для V1/V2/V3/Kilo artifacts:

  * `Subproject ID`;
  * `Block ID`;
  * `Boss Session ID`;
  * `Source / downstream relation`;
  * `Status`;
* `external/v1/INDEX.md`;
* `external/v2/INDEX.md`;
* `external/v3/INDEX.md`;
* `kilo/reports/INDEX.md`.

**Тип:** consumer repo.

**Dependencies:** Phase 5–6.

**Acceptance gate:** по любому V1/V2/V3/Kilo report можно понять, к какому подпроекту и блоку он относится.

**Risks / anti-patterns:**
Не мигрировать всю старую историю задним числом. Старые материалы можно оставить как legacy, а linkage вводить для новых runs.

---

##### Phase 8 — Promote stable parts to central core

**Цель:** вынести повторно используемые элементы из consumer repo в `ai-workflow-core`.

**Почему только здесь:** core должен получать proven reusable contracts, а не сырые идеи.

**Deliverables in central core:**

* `templates/subproject_state_template.md`;
* `templates/task_control_pack_template.md`;
* `templates/boss_bootstrap_template.md`;
* `templates/blocks_index_template.md`;
* maybe `prompts/create_task_control_pack.md`;
* maybe `prompts/boss_review_block_report.md`.

**Тип:** central core changes.

**Dependencies:** successful pilot + hardening.

**Acceptance gate:** новые templates не содержат project-specific Sword_of_rome details and can be copied into another consumer repo.

**Risks / anti-patterns:**
Не переносить project-specific V2/V3 local behavior в central prematurely. Project `.ai/README.md` уже показывает, что central core и consumer repo имеют разные зоны ответственности. ([GitHub][6])

---

##### Phase 9 — Optional automation and validators

**Цель:** добавить лёгкую машинную проверку формы, но не заменить human/Boss review.

**Почему последним:** ранняя автоматизация закрепит неправильную структуру.

**Deliverables:**

* validator for required metadata fields;
* validator for `BLOCKS_INDEX.md` links;
* validator for missing `Subproject ID` / `Block ID`;
* optional script to create skeleton folder.

**Тип:** central core + consumer repo, after proof.

**Dependencies:** at least one successful pilot, preferably two.

**Acceptance gate:** validators catch missing IDs/links, but do not claim semantic acceptance.

**Risks / anti-patterns:**
Не делать automatic gate runner, который "принимает" блок. Central block plan explicitly says not to include validators or automatic gate runner in Block Plan. ([GitHub][3])

#### 3. First executable route

Самый маленький первый pilot:

```text
SP-20260530-b1-boss-orchestration-rollout
B1-001_task_control_pack_skeleton
```

**Задача pilot-а:** не писать product-code, а создать минимальный рабочий subproject/taskspace layer для самой B1/Boss системы.

**Artifacts before pilot:**

* `SUBPROJECT_STATE.md`
* `SHORT_PLAN.md`
* `BLOCKS_INDEX.md`
* `DECISION_LOG.md`
* `SESSION_JOURNAL.md`
* `BOSS_BOOTSTRAP.md`
* `blocks/B1-001_task_control_pack_skeleton/HANDOFF.md`
* `blocks/B1-001_task_control_pack_skeleton/BLOCK_PLAN.md`
* `blocks/B1-001_task_control_pack_skeleton/CONTEXT_PACK.md`

**Artifacts during pilot:**

* `ORCHESTRATOR_PACKAGE.md`
* Kilo handoff or External Web Chat package
* executor report
* `BLOCK_REPORT.md`

**Artifacts after pilot:**

* `BOSS_REVIEW.md`
* updated `BLOCKS_INDEX.md`
* updated `SESSION_JOURNAL.md`
* updated `SHORT_PLAN.md`
* `PILOT_RETROSPECTIVE.md`

**Success proof:**
B1/Boss/subproject layer считается реально заработавшим только если есть не просто созданные templates, а полный след выполнения:

```text
Boss запустил B1
→ B1 использовал Block Orchestrator Package
→ executor выполнил bounded work
→ B1 вернул Block Report
→ Boss не доверился автоматически, а проверил report
→ план/журнал/индекс обновлены
```

#### 4. Document architecture

**Minimal file set for subproject/taskspace:**

```text
SUBPROJECT_STATE.md
FULL_PLAN.md
SHORT_PLAN.md
BLOCKS_INDEX.md
DECISION_LOG.md
SESSION_JOURNAL.md
BOSS_BOOTSTRAP.md
blocks/B1-001/HANDOFF.md
blocks/B1-001/BLOCK_PLAN.md
blocks/B1-001/CONTEXT_PACK.md
blocks/B1-001/ORCHESTRATOR_PACKAGE.md
blocks/B1-001/BLOCK_REPORT.md
blocks/B1-001/BOSS_REVIEW.md
```

**Canonical working docs:**

* `SUBPROJECT_STATE.md` — главный короткий статус.
* `SHORT_PLAN.md` — живой управленческий план Boss.
* `BLOCKS_INDEX.md` — статусы блоков, зависимости, ссылки на handoff/report/review.
* `DECISION_LOG.md` — принятые решения.
* `BOSS_BOOTSTRAP.md` — стартовый документ Boss.
* `BLOCK_PLAN.md` / `CONTEXT_PACK.md` — canonical input для B1.

**Runtime/history only:**

* raw V1/V2/V3 answers;
* raw Kilo reports;
* individual executor handoffs;
* old block reports after block acceptance;
* session logs beyond current summary.

**Navigation-visible:**

* `.ai/subprojects/README.md`, if this layer becomes stable;
* maybe `.ai/subprojects/INDEX.md`;
* not every block report;
* not every Kilo/V1/V2/V3 raw artifact.

This matches the existing repo policy: temporary workflow artifacts are excluded from `repo_navigation.md`, while stable docs/templates/rules can be indexed. ([GitHub][6])

#### 5. ID and linkage model

Use a simple layered ID model:

```text
Subproject ID:
SP-20260530-b1-boss-orchestration-rollout

Task Control Pack ID:
TCP-SP-20260530-b1-boss-orchestration-rollout-v1

Boss Session ID:
BOSS-SP-20260530-b1-boss-orchestration-rollout-S01

Block ID:
BLOCK-001_task_control_pack_skeleton

Human alias:
B1-001

Block Orchestrator Package ID:
PACKAGE-BLOCK-001_task_control_pack_skeleton

Block Report ID:
BR-SP-20260530-b1-boss-orchestration-rollout-BLOCK-001-v1

Boss Review ID:
BOSSREVIEW-SP-20260530-b1-boss-orchestration-rollout-BLOCK-001-v1
```

Why keep both `BLOCK-001` and `B1-001`: existing templates already expect `BLOCK-NNN_short_name`; user-facing language prefers B1. Do not break existing templates before pilot.

Every artifact should include this header:

```md
Subproject ID:
Boss Session ID:
Block ID:
Block Alias:
Parent Task Control Pack:
Upstream Artifacts:
Downstream Artifacts:
Status:
```

For external modes:

```text
V1 ID: V1-YYYYMMDD-HHMMSS
V2 ID: V2-YYYYMMDD-HHMM-short
V3 ID: V3-YYYYMMDD-HHMM-short
Kilo Task ID: KILO-YYYYMMDD-NNN or existing repo task ID
```

Each V1/V2/V3/Kilo artifact should say:

```md
Belongs to Subproject:
Belongs to Block:
Used by:
Reviewed by:
Accepted / rejected / informational:
```

#### 6. Do not do yet

Do **not** build full automation before one real pilot.

Do **not** rewrite all B1 templates globally before testing the smallest working path.

Do **not** migrate all old V1/V2/V3/Kilo history into subprojects retroactively.

Do **not** put every runtime block artifact into `repo_navigation.md`.

Do **not** treat the 404 V3 rollout/contract links as verified source.

Do **not** make Boss execute code or repo reconnaissance directly.

Do **not** run multiple B1 chats in parallel at first.

Do **not** start with a product-code block. Start with docs/workflow-only, because the first goal is proving the orchestration layer.

Do **not** promote subproject templates into central core until at least one project-local pilot has produced real artifacts and a retrospective.

#### 7. Recommended order for first 3 real implementation chunks in this repo

**Chunk 1 — Consumer subproject skeleton.**
Create `.ai/subprojects/README.md`, one real `SP-...` folder, `SUBPROJECT_STATE.md`, `SHORT_PLAN.md`, `BLOCKS_INDEX.md`, `DECISION_LOG.md`, `SESSION_JOURNAL.md`, and `BOSS_BOOTSTRAP.md`.

**Chunk 2 — First Task Control Pack + B1-001 package.**
Instantiate the first `Task Control Pack` and one B1 block using existing block templates. Keep it docs/workflow-only: `B1-001_task_control_pack_skeleton`.

**Chunk 3 — Real B1 pilot + Boss review.**
Run the full chain once: Boss → Block Orchestrator Package → Junior/B1 → executor → Block Report → Boss Review → update short plan/journal/index → retrospective. Only after this decide what gets promoted to central core.

### Not available / not verified

I did not run local grep, git status, git diff, tests, or inspect unpublished local runtime folders.

The two V3 raw links in the prompt returned 404, so their exact contents are not verified.

I did not verify whether local untracked `.ai/subprojects/`, local Kilo reports, V2/V3 artifacts, or unpublished examples already exist outside the opened/public links and uploaded files.

The plan above is therefore a repo-grounded rollout plan from current verified scaffold + uploaded audit/idea docs, not proof that the full system already exists.

## Candidate Navigation Entry

V1-20260530-044045: phased implementation plan for `Subproject -> Planning Chat -> Task Control Pack -> Boss -> B1 -> Junior -> Kilo/V1/V2/V3`. Вывод: в project repo уже есть сильный B1 scaffold, но rollout должен идти через project-local subproject/taskspace skeleton, Task Control Pack/Boss bootstrap, один docs-only B1 pilot с полным report/review, затем hardening и только потом promotion reusable parts в central core.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/prompts/create_block_plan.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/prompts/create_block_orchestrator_package.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/prompts/review_block_report.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/README.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/templates/block_context_pack_template.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/rules/agent_protocol.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/templates/block_report_template.md "raw.githubusercontent.com"
