# Master rollout plan: hierarchical subproject / Boss / B1 workflow system (legacy)

> **Legacy/history only.** Этот документ — старый master rollout plan для закрытой `B1/BOS/block-orchestration` системы (`SP-20260530-b1-boss-rollout`). Статус: `legacy / superseded as active workflow route`. Superseded by: `Planner -> Orc documentation-driven subproject execution`. Не продолжать его фазы как активный маршрут. Хранить только для истории.

> **Содержание (TOC) — для быстрой навигации агентов. Читай только нужные главы, не весь документ.**

| # | Глава | Строки | Описание |
|---|-------|--------|----------|
| 0 | **Source boundary and authority note** | 15–27 | Статус документа как planning/workflow artifact, три уровня утверждений (confirmed baseline / proposed target / recommended rollout), исходная позиция — B1 scaffold существует, но runtime-цикл ещё не доказан. |
| 1 | **Purpose and Scope** | 29–95 | Зачем нужен master plan (единый язык, порядок внедрения, gates, pilots), что регулирует (subproject / Boss / B1 / Task Control Pack / lifecycle), что не регулирует (product roadmap, table-sandbox, src/), почему это workflow_docs. |
| 2 | **Current Confirmed Baseline** | 97–165 | Что уже есть в repo: `.ai/` layer, agent roles, Kilo modes, V3, navigation boundaries; существующий B1 scaffold (prompts, templates, role separation); что ещё не доказано (8 пунктов); confirmed limitations (нет `.ai/subprojects/`, нет доказанного execution loop, нет accepted ID grammar). |
| 3 | **Target Operating Model** | 167–294 | Полная целевая иерархия (Repository → Subproject → Planning Chat → Boss → B1 → Junior → Executor), обоснование порядка слоёв, границы между Planning Chat и Boss, между Boss и B1, где вписываются Kilo/V1/V2/V3 и human gate. |
| 4 | **Design Principles** | 296–338 | 10 принципов: agent-first, package-before-execution, minimal canonical seed, no runtime prebuild, evidence-first hardening, no bureaucracy without proof, central promotion only after consumer proof, B1 как layer label, docs-only smoke ≠ full proof, human-readable + machine-linkable. |
| 5 | **Role and Responsibility Model** | 340–665 | 12 ролей: Repository, Subproject, Planning Chat, Task Control Pack, Boss Orchestrator, B1 Block Chat, Junior Orchestrator, Kilo, V1, V2, V3, Human — каждая с responsibility, allowed inputs, forbidden shortcuts, outputs. |
| 6 | **Subproject Model** | 668–756 | Что такое subproject (durable working area для одной инициативы), когда создавать (8 признаков), когда не создавать, сравнение с ordinary task, B1 block, Task Control Pack, V1/V2/V3, operational boundary. |
| 7 | **Document Architecture** | 758–877 | Четыре класса документов (canonical working / runtime / history / navigation), что создаётся immediately (Phase 1a seed), что только после первого pilot, что только во время execution, где живут файлы, naming rules, lifecycle rules по каждой группе документов. |
| 8 | **ID and Linkage Model** | 880–987 | Полная таблица ID-объектов (Subproject, TCP, Boss, Block, B1 Run, Package, Block Report, Boss Review, V1/V2/V3/Kilo), решение BLOCK-NNN_slug vs B1-001, формат linkage records и linkage header, V1/V2/V3/Kilo linkage, checkpoint commit linkage, правила избегания dual-ID chaos. |
| 9 | **Task Control Pack Model** | 989–1055 | Что входит в TASK_CONTROL_PACK.md (10+ полей), canonical source hierarchy, версионирование (v1 → v2), что Planning Chat передаёт Boss, что не включать в pack. |
| 10 | **Boss Bootstrap and Boss Lifecycle** | 1058–1181 | BOSS_BOOTSTRAP.md как cold-start документ, default inputs, escalation-only inputs, как Boss запускает блок (9 шагов), как обновляет state/plan/journal, как корректирует план (decision format), как закрывает блок (5 статусов), как закрывает subproject. |
| 11 | **B1 Block Lifecycle** | 1183–1283 | Один B1 чат = один блок, создание блока (5 шагов), mandatory inputs, decomposition в planned agent tasks (2–4), package gate внутри B1, Junior Orchestrators, review and return to Boss, invalid execution paths (8 примеров). |
| 12 | **Package Gate and Review Gates** | 1285–1399 | Package gate как реальный pass/fail (approved/rejected/needs_clarification/waived_by_human), required fields (18 полей), что блокирует execution, review gate после блока (10 пунктов), после pilot (7 вопросов), перед central promotion (8 условий), anti-fake signals. |
| 13 | **Phased Rollout Strategy** | 1401–1844 | 11 фаз: Phase 0 (ID decision gate), Phase 1a (minimal seed), Phase 1b (post-pilot expansion), Phase 2a (docs-only smoke), Phase 2b (non-trivial pilot), Phase 3 (evidence-based hardening), Phase 4 (linkage layer), Phase 5 (reusable extraction), Phase 6 (central promotion), Phase 7 (validators), Phase 8 (broader adoption), Phase 9 (retrospective), Phase 10 (automation). Каждая с goal, prerequisites, deliverables, owner, acceptance gate, failure signals, risks, what-not-to-do. |
| 14 | **First Executable Route** | 1846–1921 | Минимальный real route (Pre-phase → 1a → BLOCK-001 → Boss Review → BLOCK-002 → hardening), pre-phase ID decision, назначение docs-only smoke, recommended second pilot, что считается real proof. |
| 15 | **First Subproject Instantiation** | 1923–2036 | Рекомендуемый первый subproject (SP-20260530-b1-boss-rollout), первый блок (BLOCK-001-task-control-pack-smoke), второй блок (BLOCK-002-subproject-linkage-validator), docs до старта, runtime docs позже, пример двух циклов. |
| 16 | **Central Core vs Consumer Repo Split** | 2038–2100 | Что остаётся в consumer repo до proof, что не двигать в central рано, что может переехать после proof, 7 условий promotion, additive migration policy. |
| 17 | **Human / Manual / UI Setup Layer** | 2102–2179 | Что человек делает вручную (6 пунктов), какие новые чаты создавать, где нужен manual judgment, что не автоматизировать, UI conventions для инструкций (простой русский, exact files, expected result), как понять что система сошла с рельсов (8 warning signs). |
| 18 | **Navigation and Publication Policy** | 2181–2233 | Что в `.ai/repo_navigation.md`, что в subproject-local indexes, что в V1/V2/V3 navigation, что stays runtime/history only, publish rules. |
| 19 | **Governance, Change Control, and Decision Logging** | 2235–2303 | Формат decision records (DEC-YYYYMMDD-NNN), кто может менять план, как документируются corrections, как бороться с drift между canonical docs,如何处理 superseded plans, re-planning только на gates. |
| 20 | **Anti-Patterns and Do-Not-Do-Yet** | 2305–2379 | 12 анти-паттернов: bureaucracy-first, full architecture before proof, dual IDs, fake package gate, pre-created runtime docs, mass retroactive tagging, too-early centralization, docs-only pilot as proof, Boss as executor, Junior self-execution, V3 package = accepted, validators as semantic acceptors. |
| 21 | **First Three Implementation Chunks** | 2381–2451 | Chunk 1 (accept ID rules + minimal seed, 7 артефактов), Chunk 2 (BLOCK-001 smoke loop, 4 артефакта), Chunk 3 (BLOCK-002 non-trivial + hardening, 5 артефактов) — каждый с gate перед следующим. |
| 22 | **Acceptance Model for the Whole Rollout** | 2454–2518 | Четыре уровня зрелости: partially real (5 условий), usable (5 условий), broader adoption ready (6 условий), central promotion ready (5 условий), что остаётся optional, что должно stay manual. |
| 23 | **Appendices** | 2521–2802 | A — sample file tree, B — sample canonical IDs, C — sample linkage examples (Kilo/V1/V3), D — sample state/status progression, E — sample SUBPROJECT_STATE, F — sample BOSS_BOOTSTRAP, G — sample BLOCKS_INDEX, H — pilot evidence checklists (BLOCK-001 + BLOCK-002), I — minimal package gate checklist, J — minimal Boss Review checklist. |

Metadata:

| Field | Value |
|---|---|
| Document path | `.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md` |
| Scope | `workflow_docs` |
| Intended status | canonical master rollout plan, pending local import/review/human acceptance |
| V3 source request | `V3-20260530-055044-hierarchical-subproject-workflow-master-plan` |
| Project snapshot | `a33b142c19e94eae7a2c3bd087b26ecc49cb7de2` |
| Language | Russian prose with English technical identifiers |
| Product-code impact | none |

## 0. Source boundary and authority note

Этот документ создан как planning/workflow artifact. Он не утверждает, что локальный workspace был открыт, что `git status`, `git diff`, сборка, тесты или runtime были проверены. Основание документа — публичные commit-pinned GitHub sources, central workflow sources и свежая B1 planning chain, переданные во V3 request.

Документ различает три уровня утверждений:

1. **Confirmed current baseline** — то, что подтверждается открытыми project/core workflow files и опубликованными notebook entries.
2. **Proposed target state** — целевая модель, которую предлагается внедрять.
3. **Recommended rollout** — порядок внедрения, gates и anti-patterns.

Ключевая исходная позиция: в repo уже есть сильный B1 scaffold на уровне правил, prompts, templates и role separation, но нельзя писать, что полноценный B1/Boss/subproject runtime-cycle уже доказан. Пока доказательство должно быть получено через реальные pilots.

---

# 1. Purpose and Scope

## 1.1. Зачем нужен этот master plan

Этот master plan нужен, чтобы превратить идею иерархической AI-разработки из длинной обсуждательной схемы в управляемый rollout внутри repo. Система, которую нужно внедрить, выглядит так:

```text
Subproject
  -> Planning Chat
  -> Task Control Pack
  -> Boss Orchestrator
  -> B1 Block Chats
  -> Junior Orchestrators
  -> Kilo / V1 / V2 / V3 / local verification
```

Без такого master plan есть риск, что разные агенты будут использовать одинаковые слова по-разному:

- `B1` как режим, как ID блока, как чат или как слой;
- `Boss` как стратегический reviewer или как исполнитель;
- `Task Control Pack` как главный источник исполнения или как ещё один длинный план;
- `Subproject` как стабильная рабочая область или как временная папка;
- `Block Report` как реальный evidence или как пересказ Kilo report.

Этот документ задаёт общий язык, порядок внедрения, границы файлов, gates и первые pilots.

## 1.2. Что именно регулирует документ

Документ регулирует:

- модель `Subproject` как надстроечного контейнера над Boss/B1;
- разделение Planning Chat, Boss Orchestrator, B1 Block Chat, Junior Orchestrator и executor routes;
- минимальную document architecture;
- правила ID и linkage;
- модель Task Control Pack;
- lifecycle Boss и B1 block;
- package gate и review gates;
- phased rollout;
- first executable route;
- first subproject instantiation;
- разделение central core vs consumer repo;
- manual/human layer;
- navigation/publication policy;
- governance и change control;
- anti-patterns;
- first three implementation chunks;
- acceptance model для всего rollout.

## 1.3. Что документ не регулирует

Документ не регулирует product roadmap `table-sandbox`, rules engine, map editor, Phaser renderer, React UI или Sword of Rome-like module details. Он не назначает product features, не меняет архитектуру игры и не предлагает сразу править `src/`, `table-sandbox/` или product code.

Документ также не является:

- Kilo handoff;
- V1 prompt;
- V2 review request;
- V3 import package contract;
- validator specification;
- final accepted decision без local Codex/human review;
- доказательством, что B1 уже работает.

## 1.4. Почему это `workflow_docs`, а не product roadmap

Scope — `workflow_docs`, потому что результат влияет на способ организации AI-workflow, а не на функциональность продукта. Даже если позже B1 system будет использоваться для product-code blocks, текущий документ описывает route, roles, gates, artifacts и governance. Он должен жить в `.ai/plans/master/`, а не в product docs или source tree.

---

# 2. Current Confirmed Baseline

## 2.1. Что уже реально есть в repo как workflow baseline

По открытым project docs и navigation подтверждается, что repo уже имеет развитый `.ai/` workflow layer. В нём есть правила, prompts, templates, reports/reviews/navigation conventions, а также V1/V2/V3-related history и route contracts.

Подтверждённые элементы baseline:

| Area | Confirmed state | Operational meaning |
|---|---|---|
| Repo framing | Это browser-based authoring tool / tabletop sandbox для 2D counter-based wargames; Sword of Rome-like module — test/reference module, не весь продукт. | B1 rollout не должен превращаться в product roadmap. |
| `.ai/` layer | `.ai/` хранит workflow memory, rules, prompts, templates, reports, reviews, project state and route-specific materials. | Новый rollout должен интегрироваться в `.ai/`, а не создавать параллельную неуправляемую память. |
| Agent roles | Codex — orchestrator/reviewer; Kilo Code — исполнитель маленьких изолированных задач; External Web Chat — отдельный agent kind. | Boss/B1 должны наследовать agent-first модель и не превращаться в direct execution. |
| Kilo modes | Разрешены конкретные Kilo modes, включая `kilo-notebook-v3`; `/v2` не является Kilo mode. | В документах нельзя писать псевдо-mode вроде `kilo-builder` или путать mode/role. |
| Human review | Человек остаётся владельцем финального решения; human check обязателен там, где acceptance зависит от UI/runtime/text correctness. | Rollout gates должны явно показывать, где нужен человек. |
| Navigation boundaries | `repo_navigation.md` индексирует stable files, а runtime/history artifacts не должны массово попадать туда. | Subproject runtime docs нельзя автоматически публиковать как stable navigation. |
| V3 | V3 уже существует как artifact-producing workflow layer; ZIP/package сам по себе не равен import и import не равен acceptance. | Этот V3 package создаёт только один planning markdown и не утверждает repo write. |

## 2.2. Что уже есть как B1 scaffold/specification

У repo уже есть сильный B1/block orchestration scaffold:

| Existing scaffold | Current role |
|---|---|
| `.ai/prompts/create_block_plan.md` | Planning prompt for creating Block Plan + Context Pack. |
| `.ai/prompts/create_block_orchestrator_package.md` | Prompt for Main Execution Orchestrator to create Block Orchestrator Package before execution. |
| `.ai/prompts/review_block_report.md` | Prompt for reviewing Block Report against plan, context, scope, reports and changed files. |
| `.ai/templates/block_plan_template.md` | Template with allowed/forbidden files, context tiers, execution mandate, planned agent sequence, human checkpoints, stop conditions, report path. |
| `.ai/templates/block_context_pack_template.md` | Compact context carrier for one block. |
| `.ai/templates/block_report_template.md` | Evidence-focused block report template with bugs, human check, agent execution evidence, package verification, runtime contract verification. |
| `.ai/templates/block_orchestrator_package_template.md` | Template that turns package gate into an explicit artifact before Junior Orchestrator execution. |
| `AGENTS.md` / `.ai/README.md` role separation | Defines Strategist, Main Execution Orchestrator, Block Orchestrator Chat and Executor Run boundaries. |

This is not empty theory. The scaffolding is unusually strong: it already contains agent-first mandate, package gate, no self-execution rule, planned agent sequence, planned human checkpoints, senior non-interference, and block report review expectations.

## 2.3. What is not yet proven

Несмотря на scaffold, current evidence does not prove a full B1/Boss/subproject runtime loop. В свежей planning chain explicitly отмечено, что published evidence реального B1-run не найдено. Поэтому нельзя писать:

- “B1 system already works”;
- “Boss runtime cycle is proven”;
- “Subproject layer is accepted canonical structure”;
- “Package gate is proven under pressure”;
- “One docs-only pilot will prove the whole hierarchy”.

What remains unproven:

1. Может ли Boss cold-start с minimal Task Control Pack и реально управлять блоком.
2. Будет ли Package Gate настоящим pass/fail gate, а не ceremonial artifact.
3. Сможет ли Junior Orchestrator не делать substantive repo work сам.
4. Будет ли Block Report реально отличаться от Kilo report.
5. Сможет ли Boss review поймать scope drift, missing evidence or weak executor run.
6. Сможет ли subproject index/linkage не превратиться в тяжёлую бюрократию.
7. Можно ли масштабировать систему на второй non-trivial block.
8. Есть ли достаточно proof для central core promotion.

## 2.4. Confirmed current limitations

Current limitations для rollout:

- Нет подтверждённого `.ai/subprojects/` layer в pinned snapshot as accepted working system.
- Нет доказанного first real subproject execution cycle.
- Нет accepted canonical grammar for `Subproject ID`, `Block ID`, `Boss Review ID`, `B1 Run ID` в одной общей модели.
- Ранний rollout plan допускал confusion между `BLOCK-001` и `B1-001`; latest synthesis исправляет это, предлагая `BLOCK-NNN_slug` как canonical block ID.
- Ранний rollout plan смешивал canonical docs и runtime/history docs; latest critique требует развести creation timing.
- Docs-only pilot полезен, но не доказывает execution loop.
- Central promotion должна быть late, only after consumer proof.

---

# 3. Target Operating Model

## 3.1. Полная целевая иерархия

Целевая модель:

```text
Repository
  -> Subproject
      -> Planning Chat
          -> Task Control Pack
      -> Boss Orchestrator Chat
          -> B1 Block Chat / Block Orchestrator Chat
              -> Junior Orchestrator(s)
                  -> Executor Run(s)
                      -> Kilo Code
                      -> V1 External Web Chat
                      -> V2 External Senior Review
                      -> V3 Artifact-Producing Workflow
                      -> local verification / human checks
```

## 3.2. Почему порядок именно такой

Порядок слоёв нужен не ради красивой схемы, а ради снижения контекстного шума и сохранения ответственности.

| Layer | Why it exists | Why it is above/below neighbours |
|---|---|---|
| Repository | Технический контейнер проекта. | Содержит много unrelated initiatives; слишком широкий для одного Boss. |
| Subproject | Долгоживущая рабочая область одной крупной инициативы. | Уже, чем repo; шире, чем один block. |
| Planning Chat | Свободная зона исследования, synthesis, V1/V2/V3 planning. | До Boss, потому что Boss не должен читать всю сырую историю. |
| Task Control Pack | Сжатый управленческий пакет результата planning. | Передаёт только актуальное, не весь planning transcript. |
| Boss Orchestrator | Управляет execution loop внутри subproject. | Не исследует всё заново; не выполняет block work. |
| B1 Block Chat | Отдельный block-level orchestration context. | Получает bounded block scope, не весь subproject. |
| Junior Orchestrator | Делает выбор executor route and prepares executor artifact. | Не должен тащить целый Boss context. |
| Executor Run | Реальная работа: Kilo, External Web Chat, V3, verification. | Only layer allowed to perform substantive execution. |

## 3.3. Где заканчивается Planning Chat и начинается Boss

Planning Chat заканчивается там, где:

- сформирован target model на уровне подпроекта;
- выбраны initial phases;
- создан Task Control Pack;
- создан minimal Boss Bootstrap;
- создан minimal Blocks Index;
- первый Block Plan/Context Pack ready for package gate;
- дальнейшие decisions должны идти через controlled execution loop.

Planning Chat не должен:

- жить весь rollout как главный execution chat;
- запускать Kilo/V1/V2/V3 для конкретных блоков после передачи Boss;
- писать runtime reports за будущие блоки;
- pre-build пустые runtime docs;
- подменять Boss Review.

Boss начинается там, где:

- получает Task Control Pack;
- подтверждает ID/artifact timing rules;
- проверяет готовность current block;
- создаёт/reviews Block Orchestrator Package;
- после block execution reviews Block Report and updates state.

## 3.4. Где заканчивается Boss и начинается B1

Boss отвечает за subproject execution loop. B1 отвечает за один block.

Boss делает:

- выбирает next block из `BLOCKS_INDEX.md`;
- проверяет package readiness;
- создаёт или утверждает `Block Orchestrator Package`;
- получает `Block Report`;
- пишет `BOSS_REVIEW.md`;
- обновляет `SUBPROJECT_STATE.md`, `SHORT_PLAN.md`, `BLOCKS_INDEX.md`;
- решает: next block, repair, replan, stop.

Boss не делает:

- repo reconnaissance для block work;
- executor handoff напрямую, если нужен Junior/B1 package;
- product code changes;
- Kilo execution;
- replacement of B1 report.

B1 starts when:

- current `BLOCK_PLAN.md` and `CONTEXT_PACK.md` exist;
- `Block Orchestrator Package` exists and has passed package gate;
- Junior Orchestrator has bounded scope and stop conditions;
- executor path is chosen or chosen inside B1 according to package.

B1 ends when:

- executor evidence exists or block is blocked;
- `BLOCK_REPORT.md` is written;
- deviations/risks/checks are stated;
- Boss can review.

## 3.5. Where Kilo/V1/V2/V3 fit

Kilo/V1/V2/V3 are executor/support routes, not top-level owners.

| Route | Role inside B1 system | Important boundary |
|---|---|---|
| Kilo | File-system grounded executor for local repo tasks, code/docs/scripts/checks. | Kilo is not architecture owner and not final acceptor. |
| V1 | Prompt-only external analysis, critique, planning, second opinion. | V1 does not write files and does not prove local repo state. |
| V2 | Bounded external senior review of fixed WIP/snapshot. | V2 is not a Kilo mode and should not replace local verification. |
| V3 | External artifact package generation. | Package is not imported; imported is not accepted; human/Codex gates remain. |
| Local verification | Machine/manual checks after work. | Check reports are evidence, not automatic acceptance. |

## 3.6. Where human gate fits

Human gate exists at several levels:

- before accepting first subproject ID/artifact timing rule;
- before launching pilots that change files;
- before high-risk tasks;
- before accepting package gate exceptions;
- after UI/product visible changes;
- before central core promotion;
- when ambiguity requires a human decision.

Human is not expected to inspect every line of every runtime artifact. The system should tell the human exactly what to open, what to look for, and what answer to send back.

---

# 4. Design Principles

## 4.1. Agent-first, not Codex-as-worker

Substantive execution goes through agents: `Kilo Code` or `External Web Chat` routes. Direct Codex execution is allowed only with explicit pre-approved exception. This protects the main strategic context and makes execution evidence reviewable.

## 4.2. Package-before-execution

No B1 block execution starts before `Block Orchestrator Package` exists and passes a real package gate. The package is not decorative; it defines scope, boundary, recommended agent path, stop conditions, direct dependencies and expected outputs.

## 4.3. Minimal canonical seed before proof

Before first pilot, create only minimal canonical docs needed to start. Do not create a full subproject bureaucracy before the first loop proves what fields are actually useful.

## 4.4. No runtime prebuild

Runtime/history artifacts are created during or after real execution. Do not create empty `BLOCK_REPORT.md`, `BOSS_REVIEW.md`, `SESSION_JOURNAL.md`, `PILOT_RETROSPECTIVE.md` or `external/v1/INDEX.md` just to make a folder look complete.

## 4.5. Evidence-first hardening

Hardening must be based on real pilot findings. If a pilot reveals missing fields, confusing prompts or weak review gates, harden those exact parts. Do not harden imagined problems before proof.

## 4.6. No bureaucracy without proof

Every new required doc, field, index or gate must have operational value: it should prevent a real failure, preserve a decision, reduce context load, or make review possible. If it only makes the system look formal, defer it.

## 4.7. Central promotion only after consumer proof

Consumer repo is the experimental proving ground. Central core receives only stable, reusable patterns after at least two completed block cycles, including one non-trivial cycle.

## 4.8. B1 is layer label, not canonical block ID

`B1` names the layer/route. Canonical block IDs should use `BLOCK-NNN_slug`. Optional runtime attempt IDs can use `B1RUN-YYYYMMDD-NNN`, but should never replace `BLOCK-NNN_slug` in indexes or canonical docs.

## 4.9. Docs-only smoke is useful but insufficient

The first docs-only pilot is useful to test forms and package gate. It is not proof that execution logic works under pressure. A second non-trivial pilot is mandatory before hardening/promotion.

## 4.10. Human-readable, machine-linkable

Docs should be readable by the user in Russian, but identifiers, file paths, JSON/YAML keys and IDs must be English and stable.

---

# 5. Role and Responsibility Model

## 5.1. Repository / consumer repo

Responsibility:

- hosts project-specific workflow docs, rules copies, subproject artifacts and runtime history;
- is the first proving ground for B1/Boss/subproject rollout;
- keeps project-specific decisions separate from central core.

Allowed inputs:

- central core copies/references;
- project rules;
- accepted planning docs;
- human decisions;
- agent reports.

Forbidden shortcuts:

- blindly copying central core changes without local proof;
- treating historical notebook entries as accepted decisions automatically;
- indexing runtime artifacts in `repo_navigation.md` without stability.

Outputs:

- accepted project-local docs;
- subproject folders after rollout;
- pilot evidence;
- local template refinements;
- candidates for central promotion.

## 5.2. Subproject

Responsibility:

- provides bounded workspace for one large initiative;
- connects planning, Boss, B1 blocks, reports, external routes and decisions;
- preserves current status without dragging entire repo history.

Allowed inputs:

- Task Control Pack;
- short plan;
- block index;
- accepted decisions;
- block reports and Boss reviews.

Forbidden shortcuts:

- becoming a dump of every raw chat;
- pretending all runtime artifacts are stable canonical docs;
- mixing unrelated initiatives.

Outputs:

- `SUBPROJECT_STATE.md`;
- `SHORT_PLAN.md`;
- `TASK_CONTROL_PACK.md`;
- `BOSS_BOOTSTRAP.md`;
- `BLOCKS_INDEX.md`;
- runtime block artifacts created only when real runs happen.

## 5.3. Planning Chat

Responsibility:

- explores problem freely;
- uses V1/V2/V3 ideas as needed;
- produces Task Control Pack and minimal seed for Boss;
- resolves pre-phase decisions before document proliferation.

Allowed inputs:

- broad context;
- source idea docs;
- audit/critique/synthesis;
- repo rules;
- human preferences.

Forbidden shortcuts:

- executing blocks after Boss handoff;
- prebuilding runtime history;
- using vague IDs;
- hiding unresolved decisions in later phases.

Outputs:

- Task Control Pack;
- first subproject seed proposal;
- ID/linkage decision;
- first two block proposals.

## 5.4. Task Control Pack

Responsibility:

- cleanly transfers planning result into Boss context;
- defines scope, phases, blocks, gates and current next action.

Allowed inputs:

- approved planning conclusions;
- latest synthesis corrections;
- source constraints;
- current baseline.

Forbidden shortcuts:

- including full planning chat history;
- including rejected alternatives as if accepted;
- becoming a transcript archive.

Outputs:

- one compact canonical pack for Boss.

## 5.5. Boss Orchestrator

Responsibility:

- owns execution loop for the subproject;
- does not perform block work;
- creates/reviews block packages;
- reviews block reports;
- updates state and plan.

Allowed inputs:

- `TASK_CONTROL_PACK.md`;
- `BOSS_BOOTSTRAP.md`;
- `SUBPROJECT_STATE.md`;
- `BLOCKS_INDEX.md`;
- current `BLOCK_PLAN.md` and `CONTEXT_PACK.md`;
- completed block reports.

Forbidden shortcuts:

- direct executor handoff before package gate;
- doing repo reconnaissance for block work;
- trusting B1 report without review;
- updating state before evidence exists.

Outputs:

- package approval/rejection;
- Boss reviews;
- updated state/index/short plan;
- escalation decisions.

## 5.6. B1 Block Chat

Responsibility:

- manages one block;
- uses approved block plan/context;
- decomposes into 2–4 planned agent calls where appropriate;
- coordinates Junior Orchestrators/executor routes;
- returns Block Report.

Allowed inputs:

- `Block Orchestrator Package`;
- `BLOCK_PLAN.md`;
- `CONTEXT_PACK.md`;
- direct canonical dependencies allowed by package.

Forbidden shortcuts:

- taking entire subproject context;
- changing block scope silently;
- doing substantive repo work directly;
- skipping executor evidence;
- using Kilo report as block report.

Outputs:

- executor artifacts;
- block report;
- blocked/clarification notes.

## 5.7. Junior Orchestrator

Responsibility:

- prepares and routes executor work;
- chooses `Kilo Code`, `External Web Chat`, V1/V2/V3 or verification route inside block constraints;
- returns status to B1.

Allowed inputs:

- bounded block package;
- current agent path rules;
- explicit direct dependencies.

Forbidden shortcuts:

- running Kilo itself;
- inventing missing source truth;
- doing repo lookup if that lookup is substantive block work;
- bypassing human launch where required.

Outputs:

- Kilo handoff, external prompt/package, V3 request, verification prompt, or blocked note.

## 5.8. Kilo

Responsibility:

- performs local file/code/docs/check tasks with bounded scope;
- reports changed files, checks, bugs, human checks, runtime metadata.

Allowed inputs:

- one handoff/run package;
- allowed files;
- relevant rules;
- necessary context tiers.

Forbidden shortcuts:

- broad architecture ownership;
- ignoring mode/role contract;
- continuing when source of truth is missing;
- claiming unverified capabilities.

Outputs:

- changes;
- report;
- blocked report;
- machine evidence.

## 5.9. V1

Responsibility:

- prompt-only analysis, critique, brainstorming, planning second opinion.

Allowed inputs:

- explicit prompt with central and project links/excerpts.

Forbidden shortcuts:

- claiming local repo access;
- writing files;
- replacing Codex/local verification.

Outputs:

- answer with Context Readback, source boundary, candidate navigation entry.

## 5.10. V2

Responsibility:

- external senior review of bounded WIP/snapshot;
- useful for blockers, risky design, or quality review.

Allowed inputs:

- fixed snapshot, exact files, task, constraints.

Forbidden shortcuts:

- acting as Kilo mode;
- receiving unconstrained repo-wide task;
- replacing local workspace verification.

Outputs:

- bounded review, correction advice, risk notes.

## 5.11. V3

Responsibility:

- external artifact-producing package generation;
- creates ZIP package, not direct repo changes.

Allowed inputs:

- V3 request with allowed/forbidden paths, scope, expected files, acceptance criteria.

Forbidden shortcuts:

- claiming repo write;
- treating package as import;
- treating import as acceptance;
- creating files outside manifest.

Outputs:

- artifact package with manifest, README files, checksums and project target files.

## 5.12. Human

Responsibility:

- final decision owner;
- creates/manual-configures chats/modes where needed;
- performs UI/manual checks;
- decides when to accept, reject, revise or stop.

Allowed inputs:

- simple Russian instructions;
- exact files to open;
- clear verdict options.

Forbidden shortcuts:

- being forced to infer hidden process state;
- being asked to manually stage artifacts as default when the workflow has not reached that stage;
- accepting unclear outcomes.

Outputs:

- verdict;
- manual setup confirmation;
- clarifications;
- acceptance/rejection.

---

# 6. Subproject Model

## 6.1. What is a subproject

A `Subproject` is a durable working area inside repo for one large initiative. It is not the whole repository and not one small task. It answers the question:

```text
Which large initiative do these Planning Chat decisions, Boss actions, B1 blocks, V1/V2/V3 requests, Kilo reports and human decisions belong to?
```

A subproject is a context boundary. It reduces the need to reload unrelated repo history and prevents workflow artifacts from becoming an unstructured pile.

## 6.2. When to create a subproject

Create a subproject when a task has most of these traits:

- will take multiple blocks or days;
- needs planning separate from execution;
- has multiple agent routes;
- requires decision logs or repeated reviews;
- has high risk of context drift;
- touches workflow architecture or project architecture;
- will produce reusable patterns;
- needs Boss/B1 orchestration.

Examples:

- B1/Boss/subproject rollout itself;
- V3 workflow redesign;
- token diagnostics system;
- large map editor architecture evolution;
- module package import/export system;
- Obsidian-style graph memory workflow.

## 6.3. When not to create a subproject

Do not create a subproject for:

- one Kilo handoff;
- one docs typo;
- one bounded bugfix;
- one V1 second opinion;
- one V3 artifact package that does not create a long-lived initiative;
- a small task with no follow-up state.

If the overhead to create `SUBPROJECT_STATE`, `TASK_CONTROL_PACK`, `BOSS_BOOTSTRAP`, `BLOCKS_INDEX` is larger than the work, use ordinary Kilo/V1/V2/V3 route instead.

## 6.4. Subproject vs ordinary task

| Ordinary task | Subproject |
|---|---|
| One handoff/report/review can close it. | Multiple blocks and decisions are expected. |
| Scope is narrow and known. | Scope is broad but bounded by initiative. |
| No separate Boss needed. | Boss is needed to preserve continuity. |
| No subproject index needed. | Needs index/state/linkage. |

## 6.5. Subproject vs B1 block

| Subproject | B1 block |
|---|---|
| Long-lived initiative. | One bounded execution unit. |
| Contains many blocks. | Belongs to one subproject. |
| Has `SUBPROJECT_STATE.md`. | Has `BLOCK_PLAN.md`, `CONTEXT_PACK.md`, `BLOCK_REPORT.md`. |
| Boss owns it. | B1/Junior orchestrator executes it. |

## 6.6. Subproject vs Task Control Pack

`Task Control Pack` is not the subproject. It is the initial control bundle that bootstraps Boss for a subproject. The subproject is the living workspace; the pack is one canonical input document.

## 6.7. Subproject vs V1/V2/V3 route

V1/V2/V3 are routes that can be used inside a subproject. They are not subprojects. A V3 package can create subproject docs, but the accepted subproject exists only after import/review/human acceptance.

## 6.8. Operational boundary of a subproject

A subproject boundary includes:

- goal;
- out-of-scope topics;
- first and later block list;
- allowed artifact families;
- current Boss context;
- accepted decisions;
- runtime evidence;
- linkage to V1/V2/V3/Kilo runs.

A subproject boundary does not automatically include all related historical chats. Historical material must be linked only when needed.

---

# 7. Document Architecture

## 7.1. Document classes

Use four document classes:

| Class | Created when | Examples | Rule |
|---|---|---|---|
| Canonical working docs | Before execution, if needed to define current work | `SUBPROJECT_STATE.md`, `SHORT_PLAN.md`, `TASK_CONTROL_PACK.md`, `BOSS_BOOTSTRAP.md`, minimal `BLOCKS_INDEX.md`, current `BLOCK_PLAN.md`, `CONTEXT_PACK.md` | Allowed before pilot. Keep minimal. |
| Runtime docs | During/after actual runs | `ORCHESTRATOR_PACKAGE.md`, `EXECUTOR_HANDOFF.md`, `EXECUTOR_REPORT.md`, `BLOCK_REPORT.md`, `BOSS_REVIEW.md` | Never pre-build empty. |
| History docs | After cycles close | `PILOT_RETROSPECTIVE.md`, accepted/rejected external entries, old reports | Keep linked; do not put everything in stable navigation. |
| Navigation/index docs | When stable indexing is needed | subproject local `INDEX.md`, `BLOCKS_INDEX.md`, optional route indexes | Start minimal; expand after pilots. |

## 7.2. What is created immediately

Before first pilot, create only:

```text
.ai/subprojects/SP-20260530-b1-boss-rollout/
  SUBPROJECT_STATE.md
  SHORT_PLAN.md
  TASK_CONTROL_PACK.md
  BOSS_BOOTSTRAP.md
  BLOCKS_INDEX.md
  blocks/
    BLOCK-001-task-control-pack-smoke/
      BLOCK_PLAN.md
      CONTEXT_PACK.md
```

Optional:

```text
.ai/subprojects/README.md
```

Only create `.ai/subprojects/README.md` if the subproject layer itself is accepted as a stable entry point. It should not become a dump of runtime links.

## 7.3. What is created only after first pilot

After first pilot, if evidence supports it:

- `PILOT_RETROSPECTIVE.md`;
- `DECISION_LOG.md` only if real decisions occurred and need durable recording;
- `SESSION_JOURNAL.md` only if it records actual session events, not placeholders;
- refined local templates or filled examples;
- minimal post-pilot `BLOCKS_INDEX.md` updates with real paths.

## 7.4. What is created only during execution

During `BLOCK-001` execution:

```text
blocks/BLOCK-001-task-control-pack-smoke/ORCHESTRATOR_PACKAGE.md
blocks/BLOCK-001-task-control-pack-smoke/EXECUTOR_HANDOFF.md or EXTERNAL_REQUEST.md
blocks/BLOCK-001-task-control-pack-smoke/EXECUTOR_REPORT.md or EXTERNAL_RESPONSE_REF.md
blocks/BLOCK-001-task-control-pack-smoke/BLOCK_REPORT.md
blocks/BLOCK-001-task-control-pack-smoke/BOSS_REVIEW.md
```

If a file does not correspond to real execution evidence, do not create it.

## 7.5. Where subproject files should live

Recommended root:

```text
.ai/subprojects/
  README.md                    # optional stable entry
  SP-YYYYMMDD-slug/
    SUBPROJECT_STATE.md
    SHORT_PLAN.md
    TASK_CONTROL_PACK.md
    BOSS_BOOTSTRAP.md
    BLOCKS_INDEX.md
    DECISION_LOG.md             # create only after real decision or after pilot if needed
    SESSION_JOURNAL.md          # create only after real session event or after pilot if needed
    PILOT_RETROSPECTIVE.md      # after pilot
    blocks/
      BLOCK-NNN_slug/
        BLOCK_PLAN.md
        CONTEXT_PACK.md
        ORCHESTRATOR_PACKAGE.md # runtime
        EXECUTOR_HANDOFF.md     # runtime if Kilo
        EXTERNAL_REQUEST.md     # runtime if External Web Chat/V3
        EXECUTOR_REPORT.md      # runtime
        BLOCK_REPORT.md         # runtime
        BOSS_REVIEW.md          # runtime
    external/
      v1/INDEX.md               # after linkage layer, not before first proof
      v2/INDEX.md
      v3/INDEX.md
    kilo/
      reports/INDEX.md
```

## 7.6. Naming rules

- `Subproject ID`: `SP-YYYYMMDD-slug`
- `Block ID`: `BLOCK-NNN_slug`
- `B1 Run ID` optional runtime attempt: `B1RUN-YYYYMMDD-NNN`
- Folder names should match IDs exactly where possible.
- Use lowercase slugs with hyphens for subproject IDs, and lower snake/kebab style after block number only if already consistent. Recommended for block IDs: `BLOCK-001-task-control-pack-smoke`.
- Do not mix `B1-001` and `BLOCK-001` for the same canonical block.

## 7.7. Lifecycle rules by document group

| Document | Create | Update | Do not do |
|---|---|---|---|
| `SUBPROJECT_STATE.md` | Phase 1a | After each Boss decision/block review | Do not include raw transcripts. |
| `SHORT_PLAN.md` | Phase 1a | After replan/accepted block | Do not become full plan archive. |
| `TASK_CONTROL_PACK.md` | Phase 1a | Only by explicit replan/version | Do not mutate silently after Boss starts. |
| `BOSS_BOOTSTRAP.md` | Phase 1a | Rarely, only if bootstrap rule changes | Do not include full planning history. |
| `BLOCKS_INDEX.md` | Phase 1a minimal | After real block state changes | Do not link non-existing runtime reports. |
| `BLOCK_PLAN.md` | Before each block | Only before package gate or via controlled revision | Do not change during execution without recording deviation. |
| `CONTEXT_PACK.md` | Before each block | Only if missing context blocks execution | Do not add unrelated block context. |
| `ORCHESTRATOR_PACKAGE.md` | During package gate | Version/recreate if rejected | Do not prebuild. |
| `BLOCK_REPORT.md` | After block execution | Correct only by explicit revision | Do not replace with Kilo report. |
| `BOSS_REVIEW.md` | After report | Update only as review correction | Do not write before evidence. |

---

# 8. ID and Linkage Model

## 8.1. ID objects

| Object | Recommended grammar | Example |
|---|---|---|
| Subproject | `SP-YYYYMMDD-slug` | `SP-20260530-b1-boss-rollout` |
| Task Control Pack | `TCP-SP-YYYYMMDD-slug-vN` | `TCP-SP-20260530-b1-boss-rollout-v1` |
| Boss session | `BOSS-SP-YYYYMMDD-slug-SNN` | `BOSS-SP-20260530-b1-boss-rollout-S01` |
| Canonical block | `BLOCK-NNN_slug` or `BLOCK-NNN-slug` | `BLOCK-001-task-control-pack-smoke` |
| B1 runtime attempt | `B1RUN-YYYYMMDD-NNN` | `B1RUN-20260530-001` |
| Block package | `PACKAGE-BLOCK-NNN_slug-vN` | `PACKAGE-BLOCK-001-task-control-pack-smoke-v1` |
| Block report | `BR-SP-YYYYMMDD-slug-BLOCK-NNN-vN` | `BR-SP-20260530-b1-boss-rollout-BLOCK-001-v1` |
| Boss review | `BOSSREVIEW-SP-YYYYMMDD-slug-BLOCK-NNN-vN` | `BOSSREVIEW-SP-20260530-b1-boss-rollout-BLOCK-001-v1` |
| V1 | existing `V1-YYYYMMDD-HHMMSS` | `V1-20260530-053908` |
| V2 | existing project V2 ID | `V2-YYYYMMDD-HHMM-short` |
| V3 | existing `V3-YYYYMMDD-HHMMSS-slug` | `V3-20260530-055044-hierarchical-subproject-workflow-master-plan` |
| Kilo task | existing repo task/checkpoint ID | `0021` or `KILO-YYYYMMDD-NNN` if needed |

## 8.2. Exact decision: `BLOCK-001` vs `B1-001`

Decision:

```text
Canonical block ID: BLOCK-NNN_slug
B1: layer label / route label, not block ID
B1 Run ID: optional runtime attempt ID, never index key
```

Reason:

- Existing templates already use `BLOCK-NNN_short_name`.
- `B1-001` as equal ID would create dual-ID chaos.
- Indexes, report paths, Boss Review IDs and future validators need one canonical key.
- Humans can still say “B1 block”, but files must use `Block ID: BLOCK-...`.

Canonical header example:

```markdown
Subproject ID: SP-20260530-b1-boss-rollout
Layer: B1
Block ID: BLOCK-001-task-control-pack-smoke
B1 Run ID: B1RUN-20260530-001 # optional runtime attempt only
Boss Session ID: BOSS-SP-20260530-b1-boss-rollout-S01
Task Control Pack: TCP-SP-20260530-b1-boss-rollout-v1
Status: planned
```

## 8.3. Linkage records

Every relevant artifact should include a small linkage header:

```markdown
Subproject ID: SP-20260530-b1-boss-rollout
Boss Session ID: BOSS-SP-20260530-b1-boss-rollout-S01
Block ID: BLOCK-001-task-control-pack-smoke
Layer: B1
Parent Task Control Pack: TCP-SP-20260530-b1-boss-rollout-v1
Upstream Artifacts:
  - TASK_CONTROL_PACK.md
  - BLOCK_PLAN.md
  - CONTEXT_PACK.md
Downstream Artifacts:
  - ORCHESTRATOR_PACKAGE.md # when created
  - BLOCK_REPORT.md # when created
Status: planned | package_ready | running | blocked | review | accepted | accepted_with_warnings | needs_revision
```

## 8.4. V1/V2/V3/Kilo linkage

For external or executor artifacts inside a subproject:

```markdown
Route ID: V1-20260530-053908
Belongs to Subproject: SP-20260530-b1-boss-rollout
Belongs to Block: BLOCK-001-task-control-pack-smoke
Used by: Boss / B1 / Planning Chat
Reviewed by: Boss / Codex / Human
Status: informational | accepted_input | rejected | superseded
```

Do not retroactively tag all old history. New linkage starts from this subproject rollout onward.

## 8.5. Checkpoint commit linkage

If a checkpoint commit is created after a block or subproject step, use a linkage note:

```text
Checkpoint: Workflow: accept B1 block BLOCK-001-task-control-pack-smoke
Subproject: SP-20260530-b1-boss-rollout
Evidence: BLOCK_REPORT.md + BOSS_REVIEW.md + updated BLOCKS_INDEX.md
```

Exact commit hashes are verified by Git during local review, not guessed in planning docs.

## 8.6. How to avoid dual-ID chaos

Rules:

1. One canonical ID per entity.
2. Aliases are allowed only if marked as aliases.
3. `B1` cannot be both layer and ID prefix for canonical blocks.
4. Runtime attempt IDs never become index keys.
5. `BLOCKS_INDEX.md` uses only canonical `Block ID`.
6. File paths use canonical IDs, not aliases.
7. External routes keep their native IDs but link back to canonical `Subproject ID` and `Block ID`.

---

# 9. Task Control Pack Model

## 9.1. What belongs in the pack

`TASK_CONTROL_PACK.md` should contain:

- Subproject ID;
- goal;
- scope and out-of-scope;
- source baseline summary;
- target operating model summary;
- current rollout phase;
- accepted ID rule;
- canonical vs runtime artifact timing rule;
- first two blocks;
- package gate definition;
- pilot exit criteria;
- Boss Bootstrap link;
- Blocks Index link;
- known risks;
- next action.

## 9.2. What is the canonical source

For Boss startup, `TASK_CONTROL_PACK.md` plus `BOSS_BOOTSTRAP.md` are canonical. Boss should not require the full Planning Chat transcript.

If conflict exists:

1. Project `AGENTS.md` / active repo rules win.
2. `TASK_CONTROL_PACK.md` controls subproject-specific scope.
3. `BLOCK_PLAN.md` controls block-specific execution.
4. Runtime reports provide evidence but do not rewrite the pack automatically.

## 9.3. How pack updates work

The pack should be versioned logically:

- `TCP-...-v1`: initial pack.
- `TCP-...-v2`: after accepted replan if the scope/model changes.

Minor status updates belong in `SUBPROJECT_STATE.md` or `SHORT_PLAN.md`, not in the pack. The pack changes only when the controlling plan changes.

## 9.4. What Planning Chat passes to Boss

Planning Chat passes:

- `TASK_CONTROL_PACK.md`;
- `BOSS_BOOTSTRAP.md`;
- `SUBPROJECT_STATE.md`;
- `SHORT_PLAN.md`;
- minimal `BLOCKS_INDEX.md`;
- current block `BLOCK_PLAN.md`;
- current block `CONTEXT_PACK.md`;
- explicit note: no runtime reports exist yet.

## 9.5. What not to include in pack

Do not include:

- full planning transcript;
- long raw V1/V2/V3 responses;
- rejected alternatives unless they explain current decision;
- future runtime placeholders;
- product-code implementation details;
- every related repo link;
- model rankings unless task-specific.

---

# 10. Boss Bootstrap and Boss Lifecycle

## 10.1. What is Boss bootstrap

`BOSS_BOOTSTRAP.md` is the cold-start document for a new Boss Orchestrator Chat. It lets Boss start without reading the whole Planning Chat.

It should say:

```text
You are Boss Orchestrator for Subproject SP-20260530-b1-boss-rollout.
You own execution loop, not block work.
You must enforce package gate before execution.
You must review Block Report before updating state.
You must not create executor handoff directly when B1/Junior package is required.
You must update only real state based on evidence.
```

## 10.2. What Boss reads by default

Default Boss inputs:

- `SUBPROJECT_STATE.md`;
- `SHORT_PLAN.md`;
- `TASK_CONTROL_PACK.md`;
- `BOSS_BOOTSTRAP.md`;
- `BLOCKS_INDEX.md`;
- current `BLOCK_PLAN.md`;
- current `CONTEXT_PACK.md`.

## 10.3. What Boss reads only by escalation

Boss reads only if blocked or review requires it:

- raw planning chat transcript;
- full V1/V2/V3 notebook entries;
- old Kilo reports unrelated to current block;
- large architecture/product docs;
- older superseded plans;
- central core files not directly relevant.

## 10.4. How Boss starts a block

Before starting block:

1. Check `SUBPROJECT_STATE.md` current phase.
2. Check `BLOCKS_INDEX.md` current block status.
3. Read `BLOCK_PLAN.md` and `CONTEXT_PACK.md`.
4. Confirm ID rule is applied.
5. Confirm artifact timing rule: no runtime placeholders.
6. Create or review `Block Orchestrator Package`.
7. Apply package gate.
8. If approved, pass package to B1/Junior route.
9. If rejected, write rejection reason and return to Planning/Block Plan revision.

## 10.5. How Boss updates short plan, journal and state

After each block:

- read `BLOCK_REPORT.md`;
- run review checklist;
- write `BOSS_REVIEW.md`;
- update `BLOCKS_INDEX.md` with real status and paths;
- update `SUBPROJECT_STATE.md` with current phase and next action;
- update `SHORT_PLAN.md` if ordering/scope changes;
- write `DECISION_LOG.md` only if a real decision changed or clarified direction;
- write `SESSION_JOURNAL.md` only with actual session facts.

## 10.6. How Boss corrects plan

Boss can correct plan when:

- package gate failed;
- block report reveals scope issue;
- executor report shows source-of-truth missing;
- human gate changes direction;
- second pilot reveals structural issue;
- central promotion criteria are not met.

Correction format:

```markdown
Decision ID: DEC-YYYYMMDD-NNN
Subproject ID: ...
Block ID: ...
Old assumption: ...
New decision: ...
Reason/evidence: ...
Affected docs: ...
Status: accepted | pending human | superseded
```

## 10.7. How Boss closes block

A block can close as:

- `accepted`;
- `accepted_with_warnings`;
- `needs_revision`;
- `blocked`;
- `superseded`.

Required evidence for `accepted` or `accepted_with_warnings`:

- Block Plan existed before execution;
- Package Gate passed;
- executor evidence exists;
- Block Report exists;
- Boss Review exists;
- changed/created files are within scope;
- human check status is clear;
- open risks are listed.

## 10.8. How Boss closes subproject

Subproject can close only when:

- all required pilots completed or explicitly waived by human decision;
- acceptance criteria met;
- state/index reflect reality;
- central promotion decision recorded;
- runtime/history artifacts are linked but not over-published;
- final report states what remains manual and optional.

---

# 11. B1 Block Lifecycle

## 11.1. One B1 chat = one block

A B1 Block Chat should handle exactly one canonical block. It must not become a second Boss. It can coordinate multiple planned agent tasks inside one block, but the boundary remains `BLOCK-NNN_slug`.

## 11.2. How a block is created

Block creation requires:

1. entry in `BLOCKS_INDEX.md`;
2. `BLOCK_PLAN.md` based on template;
3. `CONTEXT_PACK.md`;
4. Boss selection of current block;
5. `Block Orchestrator Package` created at execution start.

## 11.3. Mandatory input docs

B1 receives:

- `Block Orchestrator Package`;
- `BLOCK_PLAN.md`;
- `CONTEXT_PACK.md`;
- direct canonical dependencies named in package;
- no full planning transcript by default.

## 11.4. How B1 decomposes

B1 decomposes into 2–4 planned agent tasks when the block is large enough. For first smoke pilot, decomposition may be very small, but it still must distinguish planned calls from contingency/repair.

Example:

```text
Planned Agent Sequence:
1. Junior Orchestrator prepares executor docs-only package/check.
2. Executor performs bounded docs/workflow action.
3. B1 reviews executor result and writes Block Report.
Contingency / Repair:
- If executor reports missing source-of-truth, return Blocked / Clarification Request.
```

## 11.5. How Package Gate works inside B1

The package gate checks:

- package has correct Subproject ID and Block ID;
- package references approved planning docs;
- block scope is clear;
- forbidden paths are listed;
- recommended agent path is justified;
- stop conditions are concrete;
- planned human checkpoints are present or explicitly `none` with reason;
- no executor handoff is created before package approval;
- Junior boundary is clear.

## 11.6. How B1 uses Junior Orchestrators

B1 can use Junior Orchestrators to:

- prepare Kilo handoff;
- prepare V1 prompt;
- prepare V2 request;
- prepare V3 request;
- prepare verification prompt;
- summarize executor report for block-level review.

Junior must not:

- run Kilo itself;
- do repo work itself;
- change files;
- bypass human launch;
- expand scope without returning blocked/escalation.

## 11.7. Review and return to Boss

At block end B1 returns:

- status;
- changed/created files;
- executor evidence;
- checks run;
- deviations;
- risks;
- human check status;
- blocked items;
- recommended Boss action.

## 11.8. Invalid B1 execution path

Invalid path examples:

- Boss creates Kilo handoff directly without Block Orchestrator Package.
- B1 starts work without `BLOCK_PLAN.md`.
- B1 does repo reconnaissance itself.
- `BLOCK_REPORT.md` is a copy of Kilo report with no block-level review.
- Runtime files were pre-created before actual run.
- `B1-001` is used as canonical ID while `BLOCK-001` also exists.
- Docs-only smoke pilot is declared as full proof.

---

# 12. Package Gate and Review Gates

## 12.1. Package gate as real pass/fail gate

Package gate result must be one of:

- `approved` — execution may start;
- `rejected` — execution blocked until package is revised;
- `needs_clarification` — Boss/Planning must resolve ambiguity;
- `waived_by_human` — only with explicit human decision and reason.

No `soft approved` by silence.

## 12.2. Required fields before block start

`Block Orchestrator Package` must include:

- Package ID;
- Parent Block ID;
- Subproject ID;
- Boss Session ID;
- Planning Document Reference;
- Block Plan Reference;
- Context Pack Reference;
- Block Scope;
- Block Boundary;
- Recommended Agent Path;
- Junior Execution Boundary;
- Planned Agent Sequence;
- Planned Human Checkpoints;
- Direct Canonical Dependencies;
- Stop Conditions;
- Workflow Canon Reference;
- Expected Outputs;
- Context Budget;
- Gate Confirmation.

## 12.3. What blocks execution

Execution is blocked if:

- no package exists;
- wrong or missing Subproject ID/Block ID;
- package references non-existing canonical docs;
- agent path unclear;
- forbidden paths missing for file-changing task;
- package asks Junior to do substantive repo work;
- package creates executor handoff before approval;
- human checkpoint missing for UI/runtime/high-risk task;
- scope is broader than block;
- conflict with repo rules.

## 12.4. Review gate after block

Boss Review must verify:

- package gate was applied;
- agent-first evidence exists;
- executor route was valid;
- files are within allowed scope;
- forbidden files untouched;
- block acceptance criteria met or not;
- report is not a raw Kilo report;
- human check status clear;
- risks and deviations explicit;
- state/index should or should not be updated.

## 12.5. Review gate after pilot

Pilot review must answer:

- Did the forms work?
- Did the package gate reject or approve something meaningful?
- Was there any correction/warning/lesson?
- Did Boss update state after evidence, not before?
- Did runtime artifact creation timing hold?
- What should be changed before next pilot?
- Was the pilot too trivial to prove anything beyond forms?

## 12.6. Review gate before central promotion

Central promotion is blocked until:

1. `BLOCK-001` docs-only smoke accepted as smoke only.
2. `BLOCK-002` non-trivial pilot accepted or accepted_with_warnings.
3. At least one real correction/lesson was processed or an explicit no-correction rationale was accepted.
4. Package gate applied before executor handoff in both cycles.
5. No dual-ID ambiguity remains.
6. Runtime placeholders were not prebuilt.
7. Human accepted promotion candidate.
8. Reusable parts are stripped of Sword_of_rome-specific details.

## 12.7. Anti-fake signals

Insufficient evidence:

- “The markdown file exists.”
- “Template was filled.”
- “Kilo report says done.”
- “No errors were reported.”
- “Docs-only smoke completed.”
- “V3 package exists.”
- “Import succeeded.”
- “Boss said accepted without checklist.”

Strong evidence:

- package was reviewed against pass/fail criteria;
- executor evidence exists;
- Block Report and Boss Review are separate;
- review found and handled real issues or explicitly justified no issues;
- state/index updated after facts;
- second non-trivial pilot survived correction pressure.

---

# 13. Phased Rollout Strategy

## Phase 0 — Source boundary and ID decision gate

Goal: Decide ID semantics and artifact timing before creating documents.

Why here: If ID ambiguity propagates into files, future indexes and validators become unreliable.

Prerequisites:

- read current B1 scaffold;
- accept that B1 runtime is not yet proven;
- human agrees to create subproject layer.

Deliverables:

- one recorded decision: `BLOCK-NNN_slug` is canonical block ID;
- `B1` is layer label;
- runtime artifacts are not prebuilt;
- docs-only pilot is smoke only.

Owner layer: mixed — Planning Chat + human decision.

Artifact impact:

- no runtime files;
- decision captured in first seed docs.

Acceptance gate:

- decision is visible in `TASK_CONTROL_PACK.md`, `SUBPROJECT_STATE.md`, `BOSS_BOOTSTRAP.md`, `BLOCKS_INDEX.md`.

Failure signals:

- both `B1-001` and `BLOCK-001` used as canonical IDs;
- empty runtime reports created;
- no explicit decision.

Main risks:

- “we will resolve IDs later” mindset.

What not to do:

- create full subproject tree before this decision.

## Phase 1a — Minimal subproject seed

Goal: Create only canonical docs needed for first smoke pilot.

Why here: The system needs enough structure to start, but not a full bureaucracy before proof.

Prerequisites:

- Phase 0 accepted.

Deliverables:

```text
.ai/subprojects/SP-20260530-b1-boss-rollout/
  SUBPROJECT_STATE.md
  SHORT_PLAN.md
  TASK_CONTROL_PACK.md
  BOSS_BOOTSTRAP.md
  BLOCKS_INDEX.md
  blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md
  blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md
```

Owner layer: consumer repo.

Artifact impact:

- creates minimal canonical docs only.

Acceptance gate:

- files include correct IDs;
- no runtime placeholders;
- `BLOCKS_INDEX.md` has only planned entries and no fake report paths.

Failure signals:

- `SESSION_JOURNAL.md`, `BLOCK_REPORT.md`, `BOSS_REVIEW.md` created empty;
- first block lacks stop conditions or package gate.

Risks:

- overbuilding folder structure.

What not to do:

- create `external/v1`, `external/v2`, `external/v3`, `kilo/reports` indexes yet.

## Phase 1b — Post-pilot expansion only if needed

Goal: Expand docs architecture only after first pilot reveals what is needed.

Why here: This prevents wrong structure from becoming pseudo-canonical.

Prerequisites:

- `BLOCK-001` smoke pilot completed and reviewed.

Deliverables:

- `PILOT_RETROSPECTIVE.md`;
- optional `DECISION_LOG.md` if real decision exists;
- optional `SESSION_JOURNAL.md` if real session facts need a journal;
- adjusted local templates if evidence supports changes.

Owner layer: consumer repo.

Acceptance gate:

- each new doc has a real reason.

Failure signals:

- expansion happens before pilot;
- docs added “because source idea had a big tree”.

What not to do:

- centralize anything yet.

## Phase 2a — Docs-only smoke pilot

Goal: Verify administrative loop: Block Plan -> Package Gate -> Executor -> Block Report -> Boss Review -> state update.

Why here: The audit found no evidence of a real B1 run, so a low-risk smoke test is useful.

Prerequisites:

- Phase 1a accepted.

Deliverables:

- real `ORCHESTRATOR_PACKAGE.md`;
- one bounded executor artifact/result;
- `BLOCK_REPORT.md`;
- `BOSS_REVIEW.md`;
- updated `BLOCKS_INDEX.md` and `SUBPROJECT_STATE.md`.

Owner layer: mixed — Boss/B1/Kilo or External Web Chat/human.

Acceptance gate:

- package gate was actually applied;
- Boss Review distinguishes smoke proof from system proof;
- state updated after evidence.

Failure signals:

- block accepted without package gate;
- no executor evidence;
- docs-only smoke declared full validation.

What not to do:

- use product-code task as first smoke;
- treat zero findings as proof of perfection.

## Phase 2b — Mandatory non-trivial pilot

Goal: Test loop under mild pressure with real checks/commands or non-trivial workflow support task.

Recommended block:

```text
BLOCK-002-subproject-linkage-validator
```

Why here: Forms can pass on a trivial docs-only block. The system must handle a task with some failure modes.

Prerequisites:

- `BLOCK-001` accepted as smoke only;
- Phase 2a findings reviewed.

Deliverables:

- new `BLOCK_PLAN.md`/`CONTEXT_PACK.md`;
- package gate;
- executor artifact;
- lightweight validator/check or concrete consistency review;
- block report;
- Boss review;
- updated state/index.

Owner layer: consumer repo; possibly Kilo for script/check if allowed.

Acceptance gate:

- real checks/evidence;
- at least one correction/warning/lesson or explicit rationale;
- no runtime placeholder violation.

Failure signals:

- second block is another purely administrative docs edit;
- no evidence beyond “file exists”.

What not to do:

- promote central core before this.

## Phase 3 — Evidence-based local hardening

Goal: Fix local docs/templates/prompts based only on two pilots.

Why here: Hardening without evidence is guessing.

Prerequisites:

- Phase 2a and 2b completed or blocked with documented reasons.

Deliverables:

- local template updates;
- simplified or tightened package gate;
- corrected ID/linkage fields;
- improved Boss Bootstrap;
- pilot retrospective.

Owner layer: consumer repo.

Acceptance gate:

- each change maps to a pilot finding.

Failure signals:

- broad rewrite not tied to evidence;
- new fields added without purpose.

What not to do:

- create automation that claims semantic acceptance.

## Phase 4 — Linkage layer for new artifacts

Goal: Add subproject-aware metadata/indexing for new V1/V2/V3/Kilo artifacts.

Why after pilots: Real artifact flow reveals which links matter.

Prerequisites:

- Phase 3 local hardening.

Deliverables:

- optional `external/v1/INDEX.md`;
- optional `external/v2/INDEX.md`;
- optional `external/v3/INDEX.md`;
- optional `kilo/reports/INDEX.md`;
- metadata header convention.

Owner layer: consumer repo.

Acceptance gate:

- new route artifacts can be traced to subproject/block;
- old history not mass-migrated.

Failure signals:

- indexing every raw artifact in stable repo navigation;
- retroactive tagging project history.

What not to do:

- touch `repo_navigation.md` for every runtime artifact.

## Phase 5 — Reusable extraction

Goal: Identify reusable pieces after local proof.

Prerequisites:

- two pilots and hardening;
- human agrees patterns are reusable.

Deliverables:

- list of candidate templates/prompts;
- central-neutral wording draft;
- migration notes.

Owner layer: mixed consumer/core planning.

Acceptance gate:

- candidates contain no Sword_of_rome-specific assumptions;
- local behavior is stable.

Failure signals:

- copy local subproject docs into central as-is.

What not to do:

- centralize project-specific V2/V3 local behavior prematurely.

## Phase 6 — Central core promotion

Goal: Move proven reusable contracts/templates/prompts to `ai-workflow-core`.

Prerequisites:

- two accepted block cycles including non-trivial;
- local hardening complete;
- promotion candidates reviewed.

Deliverables may include:

- `templates/subproject_state_template.md`;
- `templates/task_control_pack_template.md`;
- `templates/boss_bootstrap_template.md`;
- `templates/blocks_index_template.md`;
- `prompts/create_task_control_pack.md`;
- `prompts/boss_review_block_report.md`.

Owner layer: central core.

Acceptance gate:

- central docs are generic;
- consumer repo can sync without breaking local specifics.

Failure signals:

- one docs-only pilot treated as enough;
- central core gets experimental fields.

What not to do:

- rewrite consumer repo around central draft before sync path exists.

## Phase 7 — Optional validators

Goal: Add lightweight machine checks for form, not semantic acceptance.

Prerequisites:

- stable local fields;
- central promotion decision or local-only need.

Deliverables:

- ID/link check;
- missing placeholder/runtime artifact check;
- required field check;
- `BLOCKS_INDEX.md` consistency check.

Owner layer: consumer repo first, then maybe central.

Acceptance gate:

- validator catches structural issues but does not claim block accepted.

Failure signals:

- validator becomes automatic semantic gate.

What not to do:

- block humans from making decisions when context requires judgment.

## Phase 8 — Broader adoption in other subprojects

Goal: Use system beyond B1 rollout itself.

Prerequisites:

- accepted local hardening and maybe central reusable docs.

Deliverables:

- second real subproject in a different area;
- evidence of transferability.

Owner layer: consumer repo.

Acceptance gate:

- new subproject starts faster and with fewer corrections.

Failure signals:

- every new task forced into B1 hierarchy.

What not to do:

- use B1 for small one-shot tasks.

## Phase 9 — Retrospective and cleanup

Goal: Close rollout cleanly, archive superseded plans, clarify what stays manual.

Deliverables:

- final rollout report;
- superseded plan notes;
- manual setup checklist;
- list of remaining optional improvements.

Owner layer: Boss + human.

Acceptance gate:

- no ambiguity between accepted canonical docs and runtime/history artifacts.

Failure signals:

- stale plans left as if current.

## Phase 10 — Automation only after stability

Goal: Add helper scripts only where repeated manual work is stable and annoying.

Prerequisites:

- repeated successful cycles;
- stable file tree;
- stable ID grammar.

Deliverables:

- skeleton generator;
- link checker;
- package preflight tool.

Owner layer: consumer repo first.

Acceptance gate:

- automation reduces friction without making decisions.

Failure signals:

- automation creates fake reports or accepted states.

---

# 14. First Executable Route

## 14.1. Smallest real route

The smallest real route is:

```text
Pre-phase ID decision
  -> Phase 1a minimal seed
  -> BLOCK-001 docs-only smoke pilot
  -> Boss Review
  -> BLOCK-002 non-trivial linkage/check pilot
  -> evidence-based hardening
```

## 14.2. Pre-phase ID decision

Before creating files:

```text
Subproject ID: SP-20260530-b1-boss-rollout
Canonical Block ID: BLOCK-NNN_slug
B1: layer label, not canonical ID
Runtime attempt ID: optional B1RUN-YYYYMMDD-NNN
Runtime artifacts: created only during/after real runs
Docs-only smoke: smoke only, not full proof
```

## 14.3. Phase 1a minimal seed

Create only the minimal set listed earlier. This seed should be enough for Boss to start and for first Block Plan to exist. It should not include fake histories.

## 14.4. Docs-only smoke pilot

Purpose:

- verify templates can be filled;
- verify package gate can be applied;
- verify executor result can be captured;
- verify Block Report/Boss Review separation;
- verify state/index update after evidence.

Insufficient proof:

- no executor;
- no package gate;
- no Boss Review;
- no state update;
- declared “full system works”.

## 14.5. Second non-trivial pilot

Recommended purpose:

- create lightweight workflow-support consistency check for subproject artifacts.

Why:

- still safe;
- still workflow_docs/scripts-adjacent only if chosen carefully;
- introduces real validation pressure;
- can reveal ID/link/runtime-placeholder mistakes.

## 14.6. What counts as real proof

Real proof starts when:

- two block cycles completed;
- package gates actually applied;
- executor evidence exists;
- Block Report and Boss Review are separate;
- state/index updated after evidence;
- at least one correction/lesson processed;
- human accepts limited rollout status.

---

# 15. First Subproject Instantiation

## 15.1. Recommended first subproject

Adopt the latest synthesis recommendation:

```text
SP-20260530-b1-boss-rollout
Path: .ai/subprojects/SP-20260530-b1-boss-rollout/
```

Reason:

- it matches the actual rollout subject;
- it is short enough;
- it avoids mixing product code with workflow rollout;
- it follows `SP-YYYYMMDD-slug` grammar;
- it was explicitly recommended in the freshest synthesis chain.

Do not use `SP-20260530-b1-boss-orchestration-rollout` unless human prefers longer clarity. The shorter accepted path is better for file names and repeated references.

## 15.2. First block

```text
Block ID: BLOCK-001-task-control-pack-smoke
Layer: B1
Purpose: validate minimal Task Control Pack, Boss Bootstrap, Package Gate and report/review loop as smoke only.
```

Initial files before start:

```text
blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md
blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md
```

Runtime files later:

```text
ORCHESTRATOR_PACKAGE.md
EXECUTOR_HANDOFF.md or EXTERNAL_REQUEST.md
EXECUTOR_REPORT.md or EXTERNAL_RESPONSE_REF.md
BLOCK_REPORT.md
BOSS_REVIEW.md
```

## 15.3. Second block

```text
Block ID: BLOCK-002-subproject-linkage-validator
Layer: B1
Purpose: non-trivial pilot to test ID/linkage/runtime-placeholder consistency with actual evidence.
```

Possible scope:

- create a lightweight docs/checklist-based consistency check; or
- create a small script only if `scripts` scope is explicitly approved; or
- perform a Kilo-based file consistency review with exact checks.

Safer default: start with workflow docs/checklist and only escalate to script if human approves.

## 15.4. Docs that must exist before start

Before Boss starts first block:

- `SUBPROJECT_STATE.md`;
- `SHORT_PLAN.md`;
- `TASK_CONTROL_PACK.md`;
- `BOSS_BOOTSTRAP.md`;
- `BLOCKS_INDEX.md`;
- `blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md`;
- `blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md`.

## 15.5. Runtime docs that appear later

Not before execution:

- `ORCHESTRATOR_PACKAGE.md`;
- `EXECUTOR_HANDOFF.md`;
- `EXECUTOR_REPORT.md`;
- `BLOCK_REPORT.md`;
- `BOSS_REVIEW.md`;
- `SESSION_JOURNAL.md`;
- `DECISION_LOG.md` unless it records real pre-phase decision;
- `PILOT_RETROSPECTIVE.md`;
- external route indexes.

## 15.6. Example first two block cycles

### Cycle 1: `BLOCK-001-task-control-pack-smoke`

1. Boss reads seed docs.
2. Boss creates package or reviews prepared package.
3. Package gate returns `approved` or `rejected`.
4. If approved, Junior prepares executor route.
5. Executor performs bounded docs/workflow action.
6. B1 writes Block Report.
7. Boss writes Boss Review.
8. Boss updates state/index.
9. Boss marks pilot as `smoke_done`, not `system_proven`.

### Cycle 2: `BLOCK-002-subproject-linkage-validator`

1. Boss uses lessons from smoke.
2. New Block Plan defines consistency checks.
3. Package gate checks whether non-trivial evidence route is clear.
4. Executor runs actual checks/review.
5. Block Report includes findings/warnings.
6. Boss evaluates whether system handled pressure.
7. If accepted, local hardening begins.
8. If blocked, replan before central promotion.

---

# 16. Central Core vs Consumer Repo Split

## 16.1. What stays consumer repo first

Keep in consumer repo until proof:

- first subproject folder;
- first Task Control Pack;
- Boss Bootstrap;
- Blocks Index;
- filled block artifacts;
- pilot reports/reviews;
- local template refinements;
- subproject-specific decisions.

## 16.2. What not to move to central too early

Do not move:

- `SP-20260530-b1-boss-rollout` docs;
- pilot-specific folders;
- project-specific decisions;
- raw V1/V2/V3/Kilo linkage indexes;
- unproven ID grammar alternatives;
- scripts not proven on multiple cycles;
- validators that encode project-specific paths.

## 16.3. What can move after proof

Candidates after proof:

- generic `subproject_state_template.md`;
- generic `task_control_pack_template.md`;
- generic `boss_bootstrap_template.md`;
- generic `blocks_index_template.md`;
- prompt to create Task Control Pack;
- prompt to review Boss block report;
- lightweight ID/linkage validator, if stable.

## 16.4. Conditions before promotion

Promotion requires:

- two completed block cycles;
- one non-trivial pilot;
- accepted local hardening;
- no unresolved ID ambiguity;
- human approval;
- central-neutral wording;
- migration/sync notes.

## 16.5. Migration policy without huge rewrite

Use additive promotion:

1. Keep consumer repo docs as accepted local implementation.
2. Add central templates/prompts separately.
3. Sync only stable reusable files.
4. Do not rewrite history.
5. Mark older local docs as `project-local implementation` if they differ.
6. Update future subprojects gradually.

---

# 17. Human / Manual / UI Setup Layer

## 17.1. What human does manually

Human manually:

- approves first subproject creation;
- opens/creates Boss Chat;
- opens B1/Junior chat if internal subagent path is unavailable;
- launches Kilo runs;
- launches External Web Chat/V1/V2/V3 where needed;
- configures Kilo UI modes;
- checks UI/product results;
- decides acceptance/rejection.

## 17.2. New chats to create manually

For the first route:

1. Planning Chat — already represented by planning docs.
2. Boss Orchestrator Chat — new clean chat seeded with `BOSS_BOOTSTRAP.md` and Task Control Pack.
3. B1 Block Chat / Junior Orchestrator — per block, created via package or internal subagent if supported.
4. Kilo run — only after executor artifact exists.

## 17.3. Where manual judgment is needed

Manual judgment needed when:

- ID decision is accepted;
- package gate ambiguity exists;
- high-risk task appears;
- UI/runtime behavior must be judged;
- central promotion is considered;
- docs-only pilot produces no findings and may be too trivial;
- B1 attempts to broaden scope.

## 17.4. What not to automate at start

Do not automate:

- semantic acceptance;
- human verdict;
- central promotion;
- creation of runtime reports;
- auto-import of V3 package;
- auto-commit/push;
- package gate approval.

## 17.5. UI conventions for Boss/B1/subproject use

In user-facing instructions:

- write in simple Russian;
- always say what file to open;
- state expected result;
- offer exact verdict words;
- distinguish “подготовить”, “запустить”, “проверить”, “принять”.

Example human check:

```markdown
Human Check: suggested
Открой `BLOCKS_INDEX.md` и проверь, что у `BLOCK-001-task-control-pack-smoke` нет ссылок на отчёты до реального запуска. Если всё верно, ответь: `BLOCKS_INDEX выглядит правильно`.
```

## 17.6. How human knows system is off rails

Warning signs:

- agent says it ran git/tests without evidence;
- B1 starts editing files directly;
- Boss prepares Kilo handoff before package gate;
- report paths appear before run;
- `B1-001` and `BLOCK-001` both used as keys;
- docs-only smoke called full proof;
- central core promotion starts after one pilot.

---

# 18. Navigation and Publication Policy

## 18.1. What belongs in `.ai/repo_navigation.md`

Only stable important files after acceptance:

- `.ai/subprojects/README.md` if subproject layer becomes stable;
- this master plan after import/review acceptance;
- generic rules/templates/prompts if added and stable.

Do not add every runtime artifact.

## 18.2. What belongs in subproject-local indexes

`BLOCKS_INDEX.md` should contain:

- block ID;
- name;
- status;
- purpose;
- dependencies;
- canonical inputs;
- runtime outputs only after they exist;
- Boss review path after it exists.

Optional route indexes after Phase 4:

- external V1/V2/V3 IDs linked to blocks;
- Kilo reports linked to blocks.

## 18.3. What belongs only in V1/V2/V3 navigation

- V1 notebook entries stay in `V1_navigation.md`.
- V2 review entries stay in V2 navigation if present.
- V3 cycles stay in V3 navigation/lifecycle layer.

Subproject indexes may link to route entries, but should not duplicate full route navigation.

## 18.4. What stays runtime/history only

- raw Kilo reports;
- raw external responses;
- individual handoffs;
- block runtime reports;
- journal drafts;
- temporary package notes;
- failed package attempts.

## 18.5. Publish rules

Publish stable planning docs only after review. Runtime artifacts can remain local/history unless they become accepted examples. Do not publish placeholders.

---

# 19. Governance, Change Control, and Decision Logging

## 19.1. How decisions are recorded

Decision records should be small and real:

```markdown
Decision ID: DEC-20260530-001
Subproject ID: SP-20260530-b1-boss-rollout
Decision: Canonical block ID is `BLOCK-NNN_slug`; `B1` is layer label.
Reason: Prevent dual-ID chaos across indexes, reports and package gates.
Status: accepted
Made by: Human + Planning/Boss review
Affected docs: TASK_CONTROL_PACK.md, BOSS_BOOTSTRAP.md, BLOCKS_INDEX.md
```

## 19.2. Who may change the plan

- Planning Chat proposes initial plan.
- Boss updates operational plan after evidence.
- Human approves major changes.
- Kilo cannot change architecture or governance on its own.
- B1 can recommend changes via Block Report, not silently apply to subproject plan.

## 19.3. How corrections are documented

Every correction should say:

- trigger;
- evidence;
- old rule;
- new rule;
- affected files;
- whether it is local-only or candidate for central.

## 19.4. How to fight drift between canonical docs

Rules:

- one current state source: `SUBPROJECT_STATE.md`;
- one operational plan source: `SHORT_PLAN.md`;
- one controlling planning source: `TASK_CONTROL_PACK.md`;
- if pack changes, version it;
- if block plan changes after package gate, record deviation/revision.

## 19.5. How to handle superseded plans

Do not delete old planning docs. Mark them:

```markdown
Status: superseded
Superseded by: path/to/new_doc.md
Reason: pilot evidence / human decision / updated source chain
Do not use for new execution except historical context.
```

## 19.6. Re-planning without chaos

Re-plan only at gates:

- package rejected;
- block report blocked;
- pilot review fails;
- human changes priority;
- central promotion denied.

Do not re-plan in the middle of an executor run unless a stop condition triggers.

---

# 20. Anti-Patterns and Do-Not-Do-Yet

## 20.1. Bureaucracy-first rollout

Bad: create complete folder tree, empty logs, empty reports, indexes and placeholders before any pilot.

Good: create minimal canonical seed, then add runtime docs only when facts exist.

## 20.2. Full architecture before first proof

Bad: design every future subproject convention before first Boss/B1 loop.

Good: define enough to run smoke and learn.

## 20.3. Dual IDs without strict semantics

Bad: `B1-001` and `BLOCK-001` both mean the same block.

Good: `BLOCK-001...` is canonical; `B1` is layer; `B1RUN` is optional runtime attempt.

## 20.4. Fake package gate

Bad: package exists, therefore gate passed.

Good: package receives explicit `approved/rejected/needs_clarification` verdict.

## 20.5. Pre-created runtime folders/docs

Bad: empty `BLOCK_REPORT.md` before execution.

Good: create report only after execution or blocked outcome.

## 20.6. Mass retroactive tagging

Bad: reclassify all old V1/V2/V3/Kilo history into subprojects.

Good: start linkage from new rollout.

## 20.7. Too-early centralization

Bad: move local experiment to central core after one docs pilot.

Good: require two pilots including non-trivial.

## 20.8. Treating docs-only pilot as system proof

Bad: “smoke passed, B1 proven”.

Good: smoke validates forms only.

## 20.9. Boss as executor

Bad: Boss runs grep, prepares Kilo handoff, edits files.

Good: Boss reviews and routes; executor routes do work.

## 20.10. Junior self-execution

Bad: Junior does repo lookup and modifies files because “small task”.

Good: Junior prepares executor artifact or returns blocked.

## 20.11. V3 package equals accepted result

Bad: external package exists, so repo changed.

Good: package -> review -> import -> journal -> Codex review -> human verdict.

## 20.12. Validators as semantic acceptors

Bad: script says block accepted.

Good: script catches missing IDs/links; Boss/Human accept.

---

# 21. First Three Implementation Chunks

## Chunk 1 — Accept ID/artifact rules and create minimal subproject seed

Do first:

1. Accept `SP-20260530-b1-boss-rollout`.
2. Accept `BLOCK-NNN_slug` canonical block ID.
3. Create minimal seed docs.
4. Do not create runtime placeholders.

Artifacts left behind:

- `SUBPROJECT_STATE.md`;
- `SHORT_PLAN.md`;
- `TASK_CONTROL_PACK.md`;
- `BOSS_BOOTSTRAP.md`;
- `BLOCKS_INDEX.md`;
- first `BLOCK_PLAN.md`;
- first `CONTEXT_PACK.md`.

Gate before next chunk:

- human/Codex verifies no runtime placeholders and ID rule is consistent.

## Chunk 2 — Run `BLOCK-001` docs-only smoke through full loop

Do second:

1. Boss creates/reviews `ORCHESTRATOR_PACKAGE.md`.
2. Package gate gives verdict.
3. Junior/executor performs bounded docs/workflow action.
4. B1 writes Block Report.
5. Boss writes Boss Review.
6. Update state/index after evidence.

Artifacts left behind:

- package;
- executor artifact/report;
- block report;
- boss review;
- updated state/index.

Gate before next chunk:

- `BLOCK-001` accepted as smoke only;
- at least one lesson/correction captured or no-finding rationale accepted.

## Chunk 3 — Run `BLOCK-002` non-trivial pilot and harden locally

Do third:

1. Create `BLOCK-002-subproject-linkage-validator` plan/context.
2. Run package gate.
3. Perform real consistency check or lightweight validator task.
4. Review and update state.
5. Harden local templates based on findings.

Artifacts left behind:

- second block artifacts;
- evidence of checks;
- Block Report/Boss Review;
- `PILOT_RETROSPECTIVE.md`;
- local template/prompt refinements if needed.

Gate after chunk:

- decide whether system is ready for Phase 4 linkage and Phase 5 reusable extraction.

---

# 22. Acceptance Model for the Whole Rollout

## 22.1. What proves system is partially real

Partially real when:

- minimal subproject seed exists;
- first package gate executed;
- first Block Report and Boss Review exist;
- state/index updated from evidence;
- docs-only smoke clearly labeled as smoke.

## 22.2. What proves it is usable

Usable when:

- second non-trivial pilot completed;
- package gate worked under mild pressure;
- block report captured real checks/deviations;
- Boss review made a meaningful decision;
- user can understand current state from `SUBPROJECT_STATE.md` without reading transcripts.

## 22.3. What proves readiness for broader adoption

Ready for broader adoption when:

- at least two block cycles accepted;
- one non-trivial;
- local hardening complete;
- no unresolved ID/artifact timing issues;
- human is comfortable with manual flow;
- new subproject can be started with less confusion than the first.

## 22.4. What proves central promotion readiness

Central promotion ready when:

- consumer proof exists;
- reusable components are extracted;
- project-specific content removed;
- migration/sync plan exists;
- human/Codex approve.

## 22.5. What remains optional after proof

Even after proof, optional:

- validators;
- skeleton generator;
- automatic index updater;
- central core promotion of every local pattern;
- V3 artifact packaging for every planning doc;
- product-code B1 blocks.

## 22.6. What should stay manual

Should stay manual:

- final human verdict;
- high-risk escalation;
- Kilo UI mode setup;
- central promotion approval;
- semantic acceptance;
- decision to create a new subproject.

---

# 23. Appendices

## Appendix A — Sample subproject file tree

```text
.ai/subprojects/
  README.md                              # optional stable entry, only after subproject layer accepted
  SP-20260530-b1-boss-rollout/
    SUBPROJECT_STATE.md
    SHORT_PLAN.md
    TASK_CONTROL_PACK.md
    BOSS_BOOTSTRAP.md
    BLOCKS_INDEX.md
    DECISION_LOG.md                      # only after real decisions
    SESSION_JOURNAL.md                   # only after real session events
    PILOT_RETROSPECTIVE.md               # after pilot
    blocks/
      BLOCK-001-task-control-pack-smoke/
        BLOCK_PLAN.md
        CONTEXT_PACK.md
        ORCHESTRATOR_PACKAGE.md          # runtime
        EXECUTOR_HANDOFF.md              # runtime if Kilo
        EXTERNAL_REQUEST.md              # runtime if external route
        EXECUTOR_REPORT.md               # runtime
        BLOCK_REPORT.md                  # runtime
        BOSS_REVIEW.md                   # runtime
      BLOCK-002-subproject-linkage-validator/
        BLOCK_PLAN.md
        CONTEXT_PACK.md
        ...runtime files later...
    external/
      v1/INDEX.md                        # after Phase 4
      v2/INDEX.md
      v3/INDEX.md
    kilo/
      reports/INDEX.md
```

## Appendix B — Sample canonical IDs

```text
Subproject ID: SP-20260530-b1-boss-rollout
Task Control Pack ID: TCP-SP-20260530-b1-boss-rollout-v1
Boss Session ID: BOSS-SP-20260530-b1-boss-rollout-S01
Block ID: BLOCK-001-task-control-pack-smoke
Layer: B1
B1 Run ID: B1RUN-20260530-001
Package ID: PACKAGE-BLOCK-001-task-control-pack-smoke-v1
Block Report ID: BR-SP-20260530-b1-boss-rollout-BLOCK-001-v1
Boss Review ID: BOSSREVIEW-SP-20260530-b1-boss-rollout-BLOCK-001-v1
```

## Appendix C — Sample linkage examples

### Kilo report linkage

```markdown
Subproject ID: SP-20260530-b1-boss-rollout
Block ID: BLOCK-002-subproject-linkage-validator
Executor Route: Kilo Code
Kilo mode: kilo-handoff-runner
Task role: Tester Agent
Used by: B1 Block Chat
Reviewed by: Boss Orchestrator
Status: evidence_for_block_report
```

### V1 linkage

```markdown
V1 ID: V1-20260530-053908
Subproject ID: SP-20260530-b1-boss-rollout
Block ID: planning-level / no block
Used by: Planning Chat
Status: accepted_input_for_master_plan
```

### V3 linkage

```markdown
V3 ID: V3-20260530-055044-hierarchical-subproject-workflow-master-plan
Subproject ID: SP-20260530-b1-boss-rollout
Block ID: planning-level / no runtime block yet
Package status: external_artifact_generation_only
Import status: pending human/Kilo Notebook V3 route
Acceptance status: pending Codex/human review after import
```

## Appendix D — Sample state/status progression

```text
planning
  -> seed_ready
  -> pilot_1_package_gate
  -> pilot_1_running
  -> pilot_1_review
  -> smoke_done
  -> pilot_2_package_gate
  -> pilot_2_running
  -> pilot_2_review
  -> non_trivial_done
  -> local_hardening
  -> linkage_layer
  -> reusable_extraction
  -> central_promotion_candidate
  -> accepted
```

Blocked variants:

```text
blocked-id-ambiguity
blocked-package-rejected
blocked-missing-source-of-truth
blocked-human-decision-needed
blocked-runtime-placeholder-violation
blocked-second-pilot-required
```

## Appendix E — Sample minimal `SUBPROJECT_STATE` structure

```markdown
# SUBPROJECT_STATE

Subproject ID: SP-20260530-b1-boss-rollout
Status: planning
Owner layer: Boss Orchestrator after bootstrap
Goal: Prove and harden B1/Boss/subproject rollout in this repo.
Scope: workflow/orchestration only.
Out of scope: product code, table-sandbox changes, broad central core promotion before proof.

Current phase: Phase 1a minimal seed
Current block: BLOCK-001-task-control-pack-smoke
ID rule: `BLOCK-NNN_slug` is canonical block ID; `B1` is layer label.
Artifact timing rule: canonical docs before execution; runtime docs during/after execution only.

Package gate status: not_started
Pilot proof status: not_started
Central promotion status: blocked_until_two_pilots

Canonical docs:
- TASK_CONTROL_PACK.md
- BOSS_BOOTSTRAP.md
- BLOCKS_INDEX.md
- blocks/BLOCK-001-task-control-pack-smoke/BLOCK_PLAN.md
- blocks/BLOCK-001-task-control-pack-smoke/CONTEXT_PACK.md

Runtime docs:
- none yet

Next action:
- Boss must review/create Block Orchestrator Package for BLOCK-001.
```

## Appendix F — Sample minimal `BOSS_BOOTSTRAP` structure

```markdown
# BOSS_BOOTSTRAP

Boss role:
- Own execution loop for SP-20260530-b1-boss-rollout.
- Do not execute block work directly.
- Enforce package gate before executor work.
- Review Block Report before updating state.

Required inputs:
- SUBPROJECT_STATE.md
- SHORT_PLAN.md
- TASK_CONTROL_PACK.md
- BLOCKS_INDEX.md
- current BLOCK_PLAN.md
- current CONTEXT_PACK.md

Hard gates:
- ID rule accepted.
- Canonical/runtime artifact split accepted.
- Package gate must return approved/rejected/needs_clarification.
- No executor handoff before package approval.
- Junior Orchestrator does not self-execute.
- Docs-only smoke does not equal full proof.
- Second non-trivial pilot required before central promotion.

First block:
- BLOCK-001-task-control-pack-smoke

After each block:
- Read Block Report.
- Write Boss Review.
- Update SUBPROJECT_STATE.md and BLOCKS_INDEX.md after evidence.
- Record only real decisions.
```

## Appendix G — Sample minimal `BLOCKS_INDEX` structure

```markdown
# BLOCKS_INDEX

Subproject ID: SP-20260530-b1-boss-rollout
ID rule: canonical block IDs use `BLOCK-NNN_slug`; `B1` is layer label.

| Canonical Block ID | Name | Status | Purpose | Depends on | Canonical Inputs | Runtime Outputs |
|---|---|---|---|---|---|---|
| BLOCK-001-task-control-pack-smoke | Task Control Pack smoke | planned | Validate forms, package gate and report/review loop as smoke only | none | BLOCK_PLAN.md, CONTEXT_PACK.md | created during run |
| BLOCK-002-subproject-linkage-validator | Non-trivial linkage/check pilot | proposed | Test linkage and runtime-placeholder rules under mild pressure | BLOCK-001 accepted | TBD after pilot 1 | not created yet |
```

Do not add runtime output paths before files exist.

## Appendix H — Sample pilot evidence checklist

### `BLOCK-001` smoke checklist

- [ ] `BLOCK_PLAN.md` existed before package.
- [ ] `CONTEXT_PACK.md` existed before package.
- [ ] `ORCHESTRATOR_PACKAGE.md` created during execution, not before seed.
- [ ] Package Gate verdict recorded.
- [ ] Executor artifact/result exists.
- [ ] `BLOCK_REPORT.md` written by B1, not copied from Kilo report.
- [ ] `BOSS_REVIEW.md` written after report.
- [ ] `BLOCKS_INDEX.md` updated after evidence.
- [ ] `SUBPROJECT_STATE.md` updated after evidence.
- [ ] Smoke labelled as smoke only.

### `BLOCK-002` non-trivial checklist

- [ ] New Block Plan includes specific checks.
- [ ] Package Gate applied again.
- [ ] Executor evidence includes actual command/check/review output.
- [ ] At least one warning/correction/lesson exists or no-finding rationale accepted.
- [ ] Runtime placeholders not prebuilt.
- [ ] Boss Review evaluates whether system handled pressure.
- [ ] Central promotion remains blocked until review accepts proof.

## Appendix I — Minimal package gate checklist

```markdown
Package Gate for BLOCK-XXX

Verdict: approved | rejected | needs_clarification | waived_by_human
Reviewer: Boss Orchestrator

Required:
- [ ] Correct Subproject ID.
- [ ] Correct canonical Block ID.
- [ ] Planning Document Reference present.
- [ ] Block Plan and Context Pack references present.
- [ ] Scope and boundary clear.
- [ ] Recommended agent path justified.
- [ ] Junior does not self-execute.
- [ ] Stop conditions concrete.
- [ ] Human checkpoints present or explicitly none with reason.
- [ ] Expected outputs concrete.
- [ ] No executor handoff/package created before this verdict.

If rejected:
Reason:
Required correction:
Return to: Boss / Planning / Block Plan revision
```

## Appendix J — Minimal Boss Review checklist

```markdown
Boss Review for BLOCK-XXX

Verdict: accepted | accepted_with_warnings | needs_revision | blocked

Check:
- [ ] Package Gate was real and passed.
- [ ] Executor evidence exists.
- [ ] Agent-first mandate respected.
- [ ] Changed files are within allowed scope.
- [ ] Forbidden files untouched.
- [ ] Block Report is not raw Kilo report.
- [ ] Bugs/difficulties section present.
- [ ] Human Check status clear.
- [ ] Risks/deviations listed.
- [ ] State/index updates are based on evidence.

Required follow-up:
- none / repair block / replan / human decision / second pilot / central promotion blocked
```
