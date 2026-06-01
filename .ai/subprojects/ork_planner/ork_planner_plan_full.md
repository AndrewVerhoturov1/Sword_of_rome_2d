# ork_planner_plan_full.md — полный canonical plan подпроекта `ork_planner`

Slug: `ork_planner`  
Status: `accepted-planner-owned-base`  
Owner: `Planner`  
Target file: `.ai/subprojects/ork_planner/ork_planner_plan_full.md`  
Current lifecycle state: `Stage 1 accepted; pre-Orc grill-me gate`  
Language: Russian user-facing planning document; English identifiers remain English.  
Active route: `Planner -> Orc`.  

> Этот файл — canonical rewrite уже живого local planner document. Он не запускает Orc, не запускает `/v3 import-entry`, не запускает Kilo Notebook V3, не создаёт соседние документы и не утверждает, что repo уже изменён этим rewrite-ом. Он задаёт безопасный порядок, по которому будущий Orc сможет начать работу только после human approval и обязательного `grill-me` gate.

---

## 1. Title and document purpose {#title-and-document-purpose}

`ork_planner` — это pilot subproject для внедрения и проверки активной модели:

```text
Planner -> Orc
```

Назначение этого документа — быть большим, подробным и операционным master document для одного конкретного пилота. Он должен не просто красиво описать систему, а провести её через последовательные gates:

1. локальный Planner review этого `plan_full`;
2. первый узкий Orc navigation pass;
3. создание одного `ork_planner_battle_plan.md` и approval человеком;
4. создание оставшейся локальной документации самого `ork_planner`;
5. проверку техпроцесса на новом маленьком docs-only подпроекте с нуля;
6. только потом аккуратную repo-level alignment wave.

Этот документ нужен, потому что главный риск workflow не технический, а процессный: модель легко начинает смешивать роли. Planner может начать вести журнал и статус, Orc может начать переписывать стратегию, внешний V3-драфт может быть принят как repo truth, а старая многоагентная схема может вернуться под новыми именами. Этот файл должен зафиксировать простое правило:

```text
Planner creates and owns the full plan.
Orc executes the accepted plan.
Human approves gates.
```

Текущий файл является Planner-owned base. Он может быть принят человеком как основа для дальнейшего Orc run, но сам по себе не является Orc run и не создаёт execution evidence.

Главный практический результат этого документа: будущий Orc должен понять, что делать первым, где остановиться, какие файлы можно создавать на каждой стадии, какие файлы нельзя трогать, где нужен human approval, когда нужно рекомендовать V1/V3/Kilo, а когда честно написать waiver.

---

## 2. Quick navigation {#quick-navigation}

| Нужно понять | Читать |
|---|---|
| Что это за документ и зачем он нужен | [1. Title and document purpose](#title-and-document-purpose) |
| Зачем существует `ork_planner` | [3. Mission of ork_planner](#mission-of-ork-planner) |
| Что запрещено и куда нельзя дрейфовать | [4. Non-goals and forbidden drifts](#non-goals-and-forbidden-drifts) |
| Какие источники главнее других | [5. Source basis and source authority order](#source-basis-and-source-authority-order) |
| Где границы Planner-а | [6. Planner role boundaries](#planner-role-boundaries) |
| Чем отличаются Planner-owned и Orc-owned артефакты | [7. Planner-owned vs Orc-owned artifacts](#planner-owned-vs-orc-owned-artifacts) |
| Какая модель документов является canonical для пилота | [8. Canonical artifact model for this pilot](#canonical-artifact-model-for-this-pilot) |
| Какой полный lifecycle принят | [9. Lifecycle overview](#lifecycle-overview) |
| Как использовать V1/V3/Kilo и waiver | [10. V1 / V3 / Kilo usage and recommend-or-waive rule](#v1-v3-kilo-usage-and-recommend-or-waive-rule) |
| Откуда взялся первый V3 draft | [11. Provenance note for first V3 draft](#provenance-note-for-first-v3-draft) |
| Что делает первый Orc nav pass | [12. First Orc nav pass](#first-orc-nav-pass) |
| Что такое `ork_planner_battle_plan.md` | [13. One battle plan and approval gate](#one-battle-plan-and-approval-gate) |
| Какие три hard phases нельзя смешивать | [14. Three hard phases of the pilot](#three-hard-phases-of-the-pilot) |
| Что создаётся в remaining local docs wave | [15. Remaining local docs completion and human acceptance](#remaining-local-docs-completion-and-human-acceptance) |
| Зачем нужен свежий tiny docs-only pilot | [16. Fresh tiny docs-only pilot](#fresh-tiny-docs-only-pilot) |
| Когда можно трогать repo-level файлы | [17. Repo-level alignment wave after fresh proof](#repo-level-alignment-wave-after-fresh-proof) |
| Чем session отличается от journal | [18. Session binding and session != journal](#session-binding-and-session-not-journal) |
| Минимальные блоки будущих документов | [19. Minimal required blocks for future docs](#minimal-required-blocks-for-future-docs) |
| Какие acceptance gates должны закрыться | [20. Acceptance gates](#acceptance-gates) |
| Карта anchors этого файла | [21. Anchor map](#anchor-map) |

Quick navigation внутри `plan_full` — удобство чтения самого файла. Позже `ork_planner_plan_index.md` будет создан отдельно для агентов, а `ork_planner_navigation.md` — как общая карта подпроекта. Эти три вещи не заменяют друг друга.

---

## 3. Mission of ork_planner {#mission-of-ork-planner}

Миссия `ork_planner` — безопасно внедрить и доказать documentation-driven workflow `Planner -> Orc` на ограниченном подпроекте до того, как этот workflow будет закреплён в repo-level правилах.

Это не просто план «написать документы». Это pilot, который должен доказать, что новая модель реально работает:

```text
Planner думает и планирует.
Orc исполняет принятый план и ведёт live evidence.
Human принимает gates и выбирает route там, где выбор должен оставаться за человеком.
Документы подпроекта работают как внешняя память и защита от потери контекста.
```

`ork_planner` нужен по нескольким причинам.

Первая причина — граница ролей. В предыдущих подходах модель могла действовать как смесь планировщика, исполнителя, reviewer-а и владельца журнала. Это удобно на коротком участке, но опасно для большого workflow: потом невозможно понять, где был принят план, где началось выполнение, кто закрыл gate, почему появился тот или иной документ. `ork_planner` должен сделать границу явной: Planner-owned файлы не должны притворяться live execution docs, а Orc-owned файлы не должны появляться раньше Orc phase.

Вторая причина — управляемость для человека. Пользователь не должен быть вынужден читать огромный исторический контекст, чтобы понять, где процесс сейчас. Документация должна отвечать простыми вопросами:

- что сейчас принято;
- что ещё только proposed;
- какой следующий безопасный шаг;
- какие файлы являются source of truth;
- какой gate открыт;
- что должен проверить человек;
- какие старые идеи больше не являются active route.

Третья причина — отказ от старого active route. В этом пилоте нельзя возвращать legacy route через `Boss`, `B1`, `Junior Orchestrator` или похожую многоступенчатую иерархию как активную схему. Эти термины могут встречаться только как historical warning: так делать больше не надо. Активная модель одна:

```text
Planner -> Orc
```

Четвёртая причина — проверка документации как внешней памяти. Будущий Orc будет работать не «по памяти чата», а по принятому `plan_full`, `plan_index`, `navigation`, `journal`, `battle_plan`, `status`, `decisions` и README. Поэтому пилот должен проверить не только содержание документов, но и удобство восстановления после context compaction.

Практическая миссия `ork_planner` завершается не тогда, когда создан один красивый markdown-файл, а когда:

1. `plan_full` принят как Planner-owned base;
2. Orc прошёл первый nav pass и не вышел за scope;
3. один `ork_planner_battle_plan.md` создан и утверждён человеком;
4. remaining local docs system создана и проверена человеком;
5. новый маленький docs-only подпроект прошёл тот же цикл с нуля;
6. только после этого выполнена ограниченная repo-level alignment wave.

---

## 4. Non-goals and forbidden drifts {#non-goals-and-forbidden-drifts}

Этот раздел намеренно жёсткий. Он нужен не для теории, а для защиты от типовых ошибок workflow.

### 4.1. Non-goals текущего документа {#non-goals-current-document}

Этот `plan_full` не должен:

- запускать Orc;
- создавать `ork_planner_plan_index.md`;
- создавать `ork_planner_navigation.md`;
- создавать `ork_planner_journal.md`;
- создавать `ork_planner_battle_plan.md`;
- создавать `ork_planner_readme.md`;
- создавать `ork_planner_status.md`;
- создавать `ork_planner_decisions.md`;
- создавать `ork_planner_plan_navigation.md`;
- создавать `ork_planner_plan_active_1.md`;
- создавать или обновлять `.ai/v3/`;
- запускать `/v3 import-entry`;
- запускать Kilo Notebook V3;
- обновлять `.ai/rules/`;
- обновлять `.ai/repo_navigation.md`;
- обновлять `AGENTS.md`;
- обновлять `.ai/project_state.md`;
- делать repo-level alignment;
- утверждать, что Orc уже выполнил nav pass;
- утверждать, что execution evidence уже существует.

Этот документ может только описывать, что должно быть создано позже, кем, при каких gates и с какими allowed/forbidden paths.

### 4.2. Forbidden drift A — Planner начинает выполнять {#forbidden-drift-planner-executes}

Симптомы:

- Planner создаёт live `journal`, `status`, `decisions`;
- Planner записывает execution entries как будто действия уже выполнены;
- Planner создаёт `battle_plan` без explicit transition;
- Planner обновляет repo-level workflow files;
- Planner закрывает gates, которые должен закрывать человек или Orc report.

Правильная реакция:

```text
Остановиться. Вернуть работу в Planner review state. Явно сказать: это ещё не Orc execution.
```

### 4.3. Forbidden drift B — Orc появляется автоматически {#forbidden-drift-orc-auto-starts}

Симптомы:

- наличие хорошего `plan_full` трактуется как запуск Orc;
- агент пишет «Orc сделал» без фактического Orc run;
- nav pass считается выполненным до создания files и report;
- battle plan создаётся до принятия nav pass report;
- человеческое approval подменяется предположением модели.

Правильная реакция:

```text
Orc starts only after explicit human instruction and mandatory grill-me gate.
```

### 4.4. Forbidden drift C — legacy route возвращается как active route {#forbidden-drift-legacy-route}

Симптомы:

- появляются active terms `Boss`, `B1`, `Junior Orchestrator` как рабочие роли;
- создаются block folders как основная структура;
- subagents становятся постоянным execution layer;
- Planner/Orc подменяются старым многоуровневым деревом.

Правильная реакция:

```text
Legacy terms may be historical context only. Active route remains Planner -> Orc.
```

### 4.5. Forbidden drift D — V3 artifact путается с repo import {#forbidden-drift-v3-import}

Симптомы:

- внешний ZIP называется уже применённым repo change;
- наличие `manifest.yaml` трактуется как local import;
- Kilo Notebook V3 считается запущенным без evidence;
- `.ai/v3/` journaling описывается как уже выполненный;
- package lifecycle остаётся active lane внутри `plan_full`.

Правильная реакция:

```text
External V3 artifact generation is not repository import.
This rewritten plan treats the current file as local and live, not as an active package/import lane.
```

### 4.6. Forbidden drift E — `plan_active_N` становится canonical для `ork_planner` {#forbidden-drift-plan-active}

Для этого пилота canonical operational battle file — один:

```text
.ai/subprojects/ork_planner/ork_planner_battle_plan.md
```

`ork_planner_plan_active_1.md` не является canonical file для `ork_planner`. Его нельзя создавать как стандартный следующий шаг. Если когда-нибудь позже человек отдельно утвердит более сложную схему, это будет новое решение, а не default этого плана.

### 4.7. Forbidden drift F — создаётся `ork_planner_plan_navigation.md` {#forbidden-drift-plan-navigation}

`ork_planner_plan_navigation.md` не существует в новом каноне. Его нельзя создавать, ссылаться на него как на будущий обязательный файл или использовать как замену `ork_planner_plan_index.md`.

Новый канон:

```text
ork_planner_plan_index.md  -> agent-oriented index for plan_full
ork_planner_navigation.md  -> subproject-wide navigation
Quick Navigation in plan_full -> convenience links inside this file
```

---

## 5. Source basis and source authority order {#source-basis-and-source-authority-order}

Этот план основан на commit-pinned project context и локальных human clarifications, которые уже встроены в задачу rewrite. Порядок authority важен, потому что некоторые документы исторически содержат старые формулировки или ранние варианты.

### 5.1. Authority order {#authority-order}

Если источники конфликтуют, применять такой порядок:

1. **Явные human instructions в текущем rewrite request.**  
   Они имеют самый высокий приоритет для формы этого документа: 6 стадий, отсутствие active ZIP/import lane, отсутствие `Unresolved Decisions`, отсутствие `plan_navigation`, один `battle_plan`, mandatory `grill-me`, fixed Stage 6 scope.

2. **Planner decision log для `ork_planner`.**  
   Особенно решения D-044–D-050, где уже зафиксированы поздние уточнения: `grill-me`, сжатая provenance note, отсутствие unresolved tail, agent-only `plan_index`, fresh tiny pilot, fixed repo-level alignment scope, замена `plan_active_1` на `battle_plan`.

3. **Bounded V1 critique `V1-20260601-015836`.**  
   Он полезен как targeted critique уже imported `plan_full`, но не является repo authority сам по себе. Его выводы приняты здесь только там, где они согласуются с human clarifications.

4. **Active repo workflow contract: `AGENTS.md`.**  
   Он задаёт language policy, human review policy, bug/report discipline, V3 distinction, session contract и active repo workflow norms.

5. **Role contracts: `codex_role_planner.md` и `codex_role_orc.md`.**  
   Они разделяют planning и execution, Planner-owned и Orc-owned writes, route selection и stop/report discipline.

6. **`codex_orchestrator.md` и `subagent_tools.md`.**  
   Они задают tool categories, V1/V3/Kilo distinction, recommend/waive expectations и ограничивают legacy framing.

7. **Source idea document.**  
   Он объясняет исходную модель документации подпроекта и один execution chat, но в этом rewrite используется только в той части, которая не конфликтует с новым canonical lifecycle.

8. **Current imported `ork_planner_plan_full.md`.**  
   Это предыдущий draft, который переписывается. Он является source of problems and useful material, но не final authority.

### 5.2. Conflict handling {#conflict-handling}

Если старый документ говорит, что первый nav pass создаёт `readme` или `plan_navigation`, а новый request говорит, что Stage 2 создаёт ровно `plan_index`, `navigation`, `journal`, применяется новый request.

Если старые решения допускают `plan_active_N`, а позднее решение D-050 и текущий request говорят, что используется один `ork_planner_battle_plan.md`, применяется `battle_plan`.

Если source idea document описывает `_plan_active_1.md` как generic template для обычных подпроектов, это не применяется к пилоту `ork_planner`, потому что текущий pilot специально фиксирует другой canonical file.

Если V1 critique говорит, что readme в nav pass допустим, но текущий request говорит, что Stage 2 creates exactly plan_index + navigation + journal, применяется текущий request.

### 5.3. Source truth discipline {#source-truth-discipline}

Внешние ответы V1/V3 помогают думать и писать, но не доказывают локальное состояние repo. Будущий Orc должен проверять local files через local repo route, если утверждает, что файл создан, изменён, импортирован, проверен или принят.

Формула:

```text
External source can propose.
Planner can accept into plan.
Orc can execute after approval.
Repo truth requires local evidence.
```

---

## 6. Planner role boundaries {#planner-role-boundaries}

Planner отвечает на вопрос:

```text
What should be done, why, in what order, under which constraints, and with which gates?
```

Planner в этом подпроекте должен:

- понять цель `ork_planner`;
- читать relevant project context;
- отделять current live state от future execution;
- фиксировать scope и non-goals;
- описывать allowed/forbidden paths;
- планировать gates;
- задавать requirements к будущим Orc-owned documents;
- рекомендовать V1/V3/Kilo route или waiver;
- передать Orc-у достаточно ясный accepted plan;
- останавливаться перед execution.

Planner не должен:

- создавать live Orc docs раньше времени;
- вести journal;
- обновлять status;
- принимать execution evidence без Orc report;
- выбирать вместо человека финальный tool route, если план говорит, что человек выбирает;
- утверждать, что Kilo был запущен;
- утверждать, что repo-level docs обновлены;
- начинать repo-level alignment;
- переименовывать active route;
- возвращать legacy execution hierarchy.

### 6.1. Planner output complete {#planner-output-complete}

Фраза, которой должен завершаться Planner stage после принятия этого файла:

```text
Planner output complete: ork_planner_plan_full.md is ready for human review/acceptance. Orc has not started.
```

После human acceptance формула меняется только так:

```text
Planner base accepted. Orc is still not started until mandatory grill-me gate and explicit human execution instruction.
```

### 6.2. Planner can recommend; human chooses {#planner-can-recommend-human-chooses}

Planner может рекомендовать route, например:

```text
Stage 2 likely needs Kilo because local file creation and diff evidence are required.
```

Но Planner не должен подменять выбор человека. Для первого Orc run действует особое правило:

```text
Orc proposes the concrete tool route. Human chooses/approves the route before execution.
```

Это значит, что будущий Orc перед nav pass должен не просто начать работу, а сначала пройти `grill-me` gate и предложить route в понятной форме.

---

## 7. Planner-owned vs Orc-owned artifacts {#planner-owned-vs-orc-owned-artifacts}

Разделение ownership — один из главных safety mechanisms пилота.

### 7.1. Planner-owned artifacts {#planner-owned-artifacts}

Planner-owned support set для `ork_planner`:

```text
.ai/subprojects/ork_planner/ork_planner_plan_full.md
.ai/subprojects/ork_planner/ork_planner_plan_decisions.md
.ai/subprojects/ork_planner/ork_planner_planner_request_ideas.md
```

Назначение:

- `ork_planner_plan_full.md` — большой canonical plan;
- `ork_planner_plan_decisions.md` — planner-stage decision memory;
- `ork_planner_planner_request_ideas.md` — planner-only internal backlog идей для V1/V2/V3/Kilo или будущих route questions.

Эти файлы помогают Planner-у не потерять контекст. Они не являются live execution docs и не доказывают, что Orc что-то выполнил.

`ork_planner_planner_request_ideas.md` не входит в default starter pack для Orc и не должен даваться Orc без отдельного human decision.

### 7.2. Orc-owned artifacts {#orc-owned-artifacts}

Orc-owned live operational docs появляются только после explicit Orc phase. Для этого пилота canonical будущий набор:

```text
.ai/subprojects/ork_planner/ork_planner_plan_index.md
.ai/subprojects/ork_planner/ork_planner_navigation.md
.ai/subprojects/ork_planner/ork_planner_journal.md
.ai/subprojects/ork_planner/ork_planner_battle_plan.md
.ai/subprojects/ork_planner/ork_planner_readme.md
.ai/subprojects/ork_planner/ork_planner_status.md
.ai/subprojects/ork_planner/ork_planner_decisions.md
```

Эти файлы не должны существовать как «просто плановые черновики», если не помечены явно как temporary Planner scaffold. В текущем каноне они должны появляться только в своих стадиях lifecycle.

### 7.3. Ownership table {#ownership-table}

| Artifact | Owner | When appears | Purpose | Notes |
|---|---|---:|---|---|
| `ork_planner_plan_full.md` | Planner | Stage 1 | canonical full plan | Current rewrite target |
| `ork_planner_plan_decisions.md` | Planner | already exists | planning decisions | Not live execution decisions |
| `ork_planner_planner_request_ideas.md` | Planner | already exists | ideas backlog | Planner-only internal; not in default Orc pack |
| `ork_planner_plan_index.md` | Orc | Stage 2 | agent index for `plan_full` | For agents, not human readers |
| `ork_planner_navigation.md` | Orc | Stage 2 | subproject navigation | Created with index+journal |
| `ork_planner_journal.md` | Orc | Stage 2 | execution log starts | Must record nav pass evidence after creation |
| `ork_planner_battle_plan.md` | Orc | Stage 3 | one operational battle plan | Replaces `plan_active_1` for this pilot |
| `ork_planner_readme.md` | Orc | Stage 4 | human entry document | Not created in Stage 2 |
| `ork_planner_status.md` | Orc | Stage 4 | current live state | Not created before local docs wave |
| `ork_planner_decisions.md` | Orc | Stage 4 | execution decisions | Separate from planner decision log |

### 7.4. Files explicitly not canonical {#files-not-canonical}

The following are not canonical for this pilot:

```text
.ai/subprojects/ork_planner/ork_planner_plan_navigation.md
.ai/subprojects/ork_planner/ork_planner_plan_active_1.md
```

Do not create them in this lifecycle.

---

## 8. Canonical artifact model for this pilot {#canonical-artifact-model-for-this-pilot}

The canonical model is intentionally small and sequential. The pilot does not start by creating a full folder of docs. It starts with one accepted Planner base, then lets Orc build the operational layer in controlled stages.

### 8.1. Stage 1 artifact model {#stage-1-artifact-model}

Stage 1 has one active target:

```text
.ai/subprojects/ork_planner/ork_planner_plan_full.md
```

Planner-only support context may include:

```text
.ai/subprojects/ork_planner/ork_planner_plan_decisions.md
.ai/subprojects/ork_planner/ork_planner_planner_request_ideas.md
```

But this rewrite package itself contains only `ork_planner_plan_full.md` as project file.

For default Orc startup, `ork_planner_planner_request_ideas.md` stays out of scope unless human explicitly includes it.

### 8.2. Stage 2 artifact model {#stage-2-artifact-model}

Stage 2 creates exactly these three new docs:

```text
.ai/subprojects/ork_planner/ork_planner_plan_index.md
.ai/subprojects/ork_planner/ork_planner_navigation.md
.ai/subprojects/ork_planner/ork_planner_journal.md
```

Stage 2 may also apply limited edits to:

```text
.ai/subprojects/ork_planner/ork_planner_plan_full.md
```

Allowed `plan_full` edits in Stage 2:

- anchors;
- quick links;
- navigation clarity;
- typo-level fixes;
- tiny wording fixes needed to make links accurate.

Forbidden `plan_full` edits in Stage 2:

- rewriting strategy;
- changing lifecycle;
- changing ownership model;
- adding new stages;
- adding repo-level alignment actions;
- creating new unresolved tails;
- converting `battle_plan` back to `plan_active_N`.

### 8.3. Stage 3 artifact model {#stage-3-artifact-model}

Stage 3 creates one file:

```text
.ai/subprojects/ork_planner/ork_planner_battle_plan.md
```

No `plan_active_1`. No multiple battle files by default. One file is enough unless human explicitly changes the plan later.

### 8.4. Stage 4 artifact model {#stage-4-artifact-model}

Stage 4 creates remaining local docs for `ork_planner` and one reusable template layer for future subprojects, still without opening repo-level alignment. Minimum:

```text
.ai/subprojects/ork_planner/ork_planner_readme.md
.ai/subprojects/ork_planner/ork_planner_status.md
.ai/subprojects/ork_planner/ork_planner_decisions.md
.ai/subprojects/templates/subproject_plan_full_template.md
.ai/subprojects/templates/subproject_plan_index_template.md
.ai/subprojects/templates/subproject_navigation_template.md
.ai/subprojects/templates/subproject_journal_template.md
.ai/subprojects/templates/subproject_battle_plan_template.md
.ai/subprojects/templates/subproject_readme_template.md
.ai/subprojects/templates/subproject_status_template.md
.ai/subprojects/templates/subproject_decisions_template.md
.ai/subprojects/templates/subproject_templates_guide.md
```

Stage 4 may update Stage 2 and Stage 3 docs as part of local docs completion, but only inside `.ai/subprojects/ork_planner/` and `.ai/subprojects/templates/`, and only under approved `battle_plan` scope.

### 8.5. Stage 5 artifact model {#stage-5-artifact-model}

Stage 5 creates a new tiny docs-only subproject from scratch. This plan does not pre-name it. The future Planner/Orc must choose a small safe slug and task. The point is not the content of that tiny subproject, but proving the workflow on clean context.

Stage 5 must be tiny, fast, documentation-only, and reversible. It must not become a hidden repo-wide migration.

### 8.6. Stage 6 artifact model {#stage-6-artifact-model}

Stage 6 has fixed repo-level scope:

```text
.ai/rules/codex_role_planner.md
.ai/rules/codex_role_orc.md
.ai/rules/codex_orchestrator.md
.ai/repo_navigation.md
AGENTS.md
```

No other repo-level files are included by default.

---

## 9. Lifecycle overview {#lifecycle-overview}

The canonical lifecycle has exactly six stages.

```text
Stage 1 — Planner review
Stage 2 — First Orc nav pass
Stage 3 — One battle plan + human approval
Stage 4 — Remaining local docs system ork_planner
Stage 5 — Fresh tiny docs-only pilot subproject from scratch
Stage 6 — Repo-level alignment wave
```

### 9.1. Stage 1 — Planner review {#stage-1-planner-review}

Current stage.

Goal:

- rewrite and accept `ork_planner_plan_full.md` as Planner-owned base;
- remove stale active package/import wording;
- remove any dedicated unresolved-decision tail;
- replace old `plan_navigation` / `plan_active_1` assumptions;
- set six-stage lifecycle;
- keep Orc blocked until human approval and grill-me gate.

Allowed project path:

```text
.ai/subprojects/ork_planner/ork_planner_plan_full.md
```

Forbidden during Stage 1:

- creating sibling docs;
- changing repo-level files;
- claiming Kilo ran;
- claiming Orc ran;
- starting `/v3 import-entry`;
- writing journal/status/decisions.

Stage 1 exits only when human accepts this Planner-owned base or requests targeted edits.

### 9.2. Stage 2 — First Orc nav pass {#stage-2-first-orc-nav-pass}

Stage 2 starts only after all three conditions are true:

1. human accepted `plan_full` as Planner base;
2. mandatory `grill-me` gate completed;
3. human explicitly approved the first Orc run route.

Goal:

- make `plan_full` navigable for agents;
- create the initial subproject navigation layer;
- start factual journal only for the actual nav pass;
- stop and report.

Stage 2 creates exactly:

```text
.ai/subprojects/ork_planner/ork_planner_plan_index.md
.ai/subprojects/ork_planner/ork_planner_navigation.md
.ai/subprojects/ork_planner/ork_planner_journal.md
```

Stage 2 may touch `ork_planner_plan_full.md` only for anchors, quick links, navigation clarity, and typo-level fixes.

Stage 2 must not create:

```text
ork_planner_readme.md
ork_planner_status.md
ork_planner_decisions.md
ork_planner_battle_plan.md
ork_planner_plan_navigation.md
ork_planner_plan_active_1.md
```

Stage 2 exits with a report and human review. If the nav pass report is not accepted, Stage 3 is blocked.

### 9.3. Stage 3 — One battle plan + human approval {#stage-3-one-battle-plan-human-approval}

Stage 3 starts only after Stage 2 report is accepted.

Goal:

- create one practical battle plan for the rest of the local pilot;
- describe sequence, allowed writes, forbidden writes, evidence, checks, and gates;
- let human approve before local docs execution begins.

Stage 3 creates exactly one battle plan file:

```text
.ai/subprojects/ork_planner/ork_planner_battle_plan.md
```

This file replaces the old idea of `ork_planner_plan_active_1.md` for this pilot.

Stage 3 exits only after human approval. Without human approval, Stage 4 is blocked.

### 9.4. Stage 4 — Remaining local docs system ork_planner {#stage-4-remaining-local-docs}

Stage 4 starts only after the battle plan is approved.

Goal:

- complete the remaining local docs system for `ork_planner`;
- create reusable templates for the full `Planner -> Orc` doc set so future subprojects can start from a proven base;
- create one guide that explains how to use those templates and what each file is responsible for;
- prove that documentation supports continuation, status, journal, decisions, and human understanding;
- keep all work local to `.ai/subprojects/ork_planner/` and `.ai/subprojects/templates/`;
- avoid repo-level alignment until local docs are accepted.

Minimum new files:

```text
.ai/subprojects/ork_planner/ork_planner_readme.md
.ai/subprojects/ork_planner/ork_planner_status.md
.ai/subprojects/ork_planner/ork_planner_decisions.md
.ai/subprojects/templates/subproject_plan_full_template.md
.ai/subprojects/templates/subproject_plan_index_template.md
.ai/subprojects/templates/subproject_navigation_template.md
.ai/subprojects/templates/subproject_journal_template.md
.ai/subprojects/templates/subproject_battle_plan_template.md
.ai/subprojects/templates/subproject_readme_template.md
.ai/subprojects/templates/subproject_status_template.md
.ai/subprojects/templates/subproject_decisions_template.md
.ai/subprojects/templates/subproject_templates_guide.md
```

Stage 4 may update:

```text
ork_planner_plan_index.md
ork_planner_navigation.md
ork_planner_journal.md
ork_planner_battle_plan.md
ork_planner_plan_full.md
```

But `plan_full` updates remain limited unless human explicitly sends the work back to Planner for plan revision.

Stage 4 exits only after human acceptance that:

- the local `ork_planner` docs system is understandable and usable;
- the reusable template layer is understandable as a base for future subprojects;
- the guide clearly explains what each template file is for and how to use the set.

### 9.5. Stage 5 — Fresh tiny docs-only pilot subproject from scratch {#stage-5-fresh-tiny-docs-only-pilot}

Stage 5 starts only after Stage 4 local docs system is accepted.

Goal:

- create a new tiny docs-only subproject from scratch;
- run the full `Planner -> Orc` cycle on clean context;
- prove that the process works outside `ork_planner` itself;
- keep the task small enough that the process, not the content, is what gets tested.

The fresh pilot must be:

- tiny;
- documentation-only;
- fast;
- low-risk;
- self-contained;
- clear enough for human to review.

Example task shape, not a required exact task:

```text
Create a tiny docs-only subproject that documents one small naming convention or one small navigation cleanup rule.
```

Stage 5 must include at least:

- Planner base;
- Orc nav/battle/local execution equivalent appropriate to tiny scope;
- human acceptance;
- clear evidence that role boundaries were followed.

Stage 5 exits only after human confirms that the process worked on fresh context.

### 9.6. Stage 6 — Repo-level alignment wave {#stage-6-repo-level-alignment-wave}

Stage 6 starts only after Stage 5 fresh proof is accepted.

Fixed scope:

```text
.ai/rules/codex_role_planner.md
.ai/rules/codex_role_orc.md
.ai/rules/codex_orchestrator.md
.ai/repo_navigation.md
AGENTS.md
```

Goal:

- align repo-level workflow docs with the proven `Planner -> Orc` model;
- keep changes targeted;
- avoid broad rewrites;
- preserve project-specific context;
- explicitly retire legacy active route wording where it conflicts with the new model.

Stage 6 must not start from theory. It must use evidence from Stage 4 and Stage 5.

---

## 10. V1 / V3 / Kilo usage and recommend-or-waive rule {#v1-v3-kilo-usage-and-recommend-or-waive-rule}

V1, V3, and Kilo are tools. They are not active management roles and not hidden subagents.

### 10.1. Rule {#recommend-or-waive-rule}

For each major future step, Planner or Orc must do one of two things:

```text
Recommend a tool route with reason.
```

or

```text
Waive external/tool route with reason.
```

Silent omission is not allowed for high-impact planning/documentation workflow decisions.

Recommended field shape:

```md
Subagent Tool: `V3-Ревью`
Reason: important workflow document; strong external draft useful; local review remains source of acceptance.
```

Waiver shape:

```md
Subagent Tool: waived
Reason: this is a small docs-only correction; no external critique, local diff, or automated test evidence is needed.
```

### 10.2. V1-Синтез {#v1-synthesis}

Use V1 when:

- a bounded critique is useful;
- naming/structure needs second opinion;
- role-boundary risks need review;
- the question can be answered from provided context;
- no local repo truth is required.

Do not use V1 as proof that repo files were changed or verified.

For this pilot, V1 has already been useful as bounded critique of imported `plan_full`. Future V1 can be recommended if battle-plan structure or Stage 5 fresh pilot design needs outside review.

### 10.3. V3-Ревью {#v3-review}

Use V3 when:

- a strong artifact draft is useful;
- the output should be packaged;
- a large documentation rewrite benefits from external generation;
- the result will still be reviewed locally.

Do not confuse `V3-Ревью` with `/v3 import-entry`.

`V3-Ревью` means:

```text
External draft/artifact first, then local review.
```

`/v3 import-entry` means:

```text
There is an existing V3 package and the user explicitly wants import through the V3 import route.
```

This rewrite is V3 artifact generation, but the canonical lifecycle in this document no longer keeps package/import as an active lane.

### 10.4. Kilo {#kilo}

Use Kilo when:

- local files must be read or changed;
- a real diff matters;
- local evidence is required;
- tests or verification are needed;
- repo state must be confirmed.

Stage 2 likely requires Kilo because it creates local files and should return evidence. However, this document does not force a concrete Kilo mode. Future Orc must propose the tool route, explain it, pass the `grill-me` gate, and human must choose/approve.

### 10.5. Human-only checks {#human-only-checks}

Use human check when:

- wording must be understandable to the user;
- role-boundary clarity must be judged by a human;
- the process must feel controllable;
- acceptance depends on reading route, not automated tests.

For this pilot, human check is not optional at major gates.

---

## 11. Provenance note for first V3 draft {#provenance-note-for-first-v3-draft}

The first external V3 draft helped create an earlier version of this `plan_full`. That earlier draft was imported locally, critiqued, clarified by the human, and then replaced by this canonical rewrite.

This provenance note is historical only. It is not an active package/import lifecycle, not a `/v3 import-entry` instruction, not Kilo Notebook V3 evidence, and not a reason to write into `.ai/v3/`.

---

## 12. First Orc nav pass {#first-orc-nav-pass}

First Orc nav pass is the first real execution step of this pilot. It is intentionally narrow.

### 12.1. Preconditions {#first-orc-nav-pass-preconditions}

Before the first real Orc run, all conditions below must be true:

1. `ork_planner_plan_full.md` accepted by human as Planner-owned base.
2. Future Orc reads the accepted plan.
3. Mandatory `grill-me` gate is completed.
4. Orc proposes a concrete tool route.
5. Human chooses/approves the route.
6. Allowed and forbidden paths are restated.
7. Stop condition is clear.

### 12.2. Mandatory grill-me gate {#mandatory-grill-me-gate}

The `grill-me` gate is a stress test before Orc does real work. It should force Orc to prove that it understands:

- current stage;
- allowed writes;
- forbidden writes;
- role boundary;
- exact files to create;
- exact files not to create;
- whether `plan_full` may be edited;
- how tool route is selected;
- where it must stop;
- what report must include.

Minimum grill-me questions:

```text
1. Are you Planner or Orc in this run?
2. Has Orc already started before this run?
3. Which exact files may Stage 2 create?
4. Which tempting files are forbidden in Stage 2?
5. Can you create readme/status/decisions now?
6. Can you create battle_plan now?
7. Can you edit plan_full, and if yes, how narrowly?
8. Are you allowed to touch .ai/rules, AGENTS.md, .ai/repo_navigation.md, or .ai/v3?
9. Who chooses the concrete tool route?
10. Where must you stop?
```

Correct answers:

```text
1. Orc, but only after explicit human activation.
2. No.
3. plan_index, navigation, journal.
4. readme, status, decisions, battle_plan, plan_navigation, plan_active_1, repo-level files, .ai/v3.
5. No.
6. No.
7. Yes, only anchors, quick links, navigation clarity, typo-level fixes.
8. No.
9. Orc proposes; human chooses/approves.
10. After nav pass report; Stage 3 blocked until report accepted.
```

If Orc fails this gate, Stage 2 is blocked and the issue returns to Planner/human correction.

### 12.3. Stage 2 allowed writes {#stage-2-allowed-writes}

Stage 2 may create exactly:

```text
.ai/subprojects/ork_planner/ork_planner_plan_index.md
.ai/subprojects/ork_planner/ork_planner_navigation.md
.ai/subprojects/ork_planner/ork_planner_journal.md
```

Stage 2 may update:

```text
.ai/subprojects/ork_planner/ork_planner_plan_full.md
```

but only for:

- stable semantic anchors;
- Quick Navigation corrections;
- link target corrections;
- typo-level fixes;
- tiny navigation clarity notes.

### 12.4. Stage 2 forbidden writes {#stage-2-forbidden-writes}

Stage 2 must not create, update, or rename:

```text
.ai/subprojects/ork_planner/ork_planner_readme.md
.ai/subprojects/ork_planner/ork_planner_status.md
.ai/subprojects/ork_planner/ork_planner_decisions.md
.ai/subprojects/ork_planner/ork_planner_battle_plan.md
.ai/subprojects/ork_planner/ork_planner_plan_navigation.md
.ai/subprojects/ork_planner/ork_planner_plan_active_1.md
.ai/subprojects/ork_planner/reviews/
.ai/v3/
.ai/rules/
.ai/repo_navigation.md
.ai/project_state.md
AGENTS.md
ideas/
```

Stage 2 also must not update V1 notebook navigation, close future gates by assertion, or claim human approval that has not happened.

### 12.5. Required Stage 2 outputs {#required-stage-2-outputs}

#### `ork_planner_plan_index.md`

Purpose:

```text
Agent-oriented index for the large plan_full.
```

It is for agents, not for human readers. Human-facing entry comes later through `ork_planner_readme.md` and `ork_planner_navigation.md`.

The index should help agents find relevant anchors quickly and avoid rereading the whole plan every time.

#### `ork_planner_navigation.md`

Purpose:

```text
Subproject-wide navigation map.
```

It should list current docs, future docs, current stage, what exists, what does not exist yet, and what not to treat as active.

#### `ork_planner_journal.md`

Purpose:

```text
Factual execution log starting from the first real Orc run.
```

The first journal entry must not backfill fake history. It may summarize prior Planner stage as context, but journal entries must clearly distinguish:

```text
Historical context != Orc action.
```

### 12.6. Stage 2 report {#stage-2-report}

The Stage 2 report must include:

- actual role used;
- tool route proposed and approved;
- files created;
- files modified;
- confirmation that forbidden files were not touched;
- summary of `plan_full` edits;
- anchor/index/navigation status;
- journal initialization status;
- bugs and difficulties;
- verification performed;
- human check instructions;
- explicit stop statement.

Stop statement:

```text
Stage 2 nav pass complete/pending review. Stage 3 battle_plan creation is blocked until human accepts this report.
```

---

## 13. One battle plan and approval gate {#one-battle-plan-and-approval-gate}

Stage 3 creates one file:

```text
.ai/subprojects/ork_planner/ork_planner_battle_plan.md
```

It is the single operational plan for the remaining pilot path after accepted `Stage 2`. It replaces the older `plan_active_1` idea for this pilot.

### 13.1. Preconditions {#battle-plan-preconditions}

Before creating `ork_planner_battle_plan.md`:

1. Stage 2 nav pass report exists.
2. Human accepted Stage 2 report.
3. `plan_index`, `navigation`, and `journal` exist.
4. Any Stage 2 navigation blockers are resolved or explicitly carried as blockers.
5. Orc proposes route and human approves if a tool run is needed.

### 13.2. Purpose {#battle-plan-purpose}

The battle plan answers:

- what remains to be done in `Stage 4`, `Stage 5`, and `Stage 6`;
- what reusable documentation base must be produced for future subprojects;
- in what order;
- by which route;
- what each step may touch;
- what each step must not touch;
- what evidence must be produced;
- where human acceptance is required;
- when to stop;
- when to return to Planner.

### 13.3. Required battle plan blocks {#battle-plan-required-blocks-summary}

The file must contain at least:

- title and status;
- parent plan reference;
- current lifecycle stage;
- phase goal;
- scope;
- prerequisites;
- allowed writes;
- forbidden writes;
- source basis;
- step sequence;
- route recommendation/waiver per step;
- evidence and checks;
- human gates;
- bug/difficulty reporting rule;
- stop and escalation rules;
- acceptance criteria.

### 13.4. Approval gate {#battle-plan-approval-gate}

`ork_planner_battle_plan.md` does not authorize itself. After creation, Orc must stop.

Stage 4 starts only if human says, in effect:

```text
Боевой план принят. Можно выполнять Stage 4 по нему.
```

If human requests edits, Stage 3 remains open. If the requested edits change strategy, return to Planner. If they only clarify execution details, Orc may revise the battle plan within approved scope.

---

## 14. Three hard phases of the pilot {#three-hard-phases-of-the-pilot}

The six stages are the lifecycle. The three hard phases are safety groups that must not be mixed.

### 14.1. Hard Phase 1 — Local ork_planner proof {#hard-phase-1-local-proof}

Includes:

```text
Stage 1 — Planner review
Stage 2 — First Orc nav pass
Stage 3 — One battle plan + human approval
Stage 4 — Remaining local docs system ork_planner
```

Goal:

- prove the model inside `ork_planner` itself;
- build local docs system;
- keep repo-level files untouched;
- demonstrate that Planner and Orc boundaries work.

Hard rule:

```text
No repo-level alignment during Hard Phase 1.
```

### 14.2. Hard Phase 2 — Fresh tiny proof on clean context {#hard-phase-2-fresh-proof}

Includes:

```text
Stage 5 — Fresh tiny docs-only pilot subproject from scratch
```

Goal:

- prove the workflow is not overfitted to `ork_planner`;
- run a small clean cycle;
- check that docs are enough to guide a new subproject;
- keep it tiny and docs-only.

Hard rule:

```text
Do not skip fresh proof just because ork_planner local docs look good.
```

### 14.3. Hard Phase 3 — Repo-level alignment after proof {#hard-phase-3-repo-alignment}

Includes:

```text
Stage 6 — Repo-level alignment wave
```

Goal:

- update fixed repo-level docs only after evidence exists;
- make the repo rules match the proven route;
- avoid speculative broad rewrites.

Hard rule:

```text
Role docs, orchestrator docs, repo navigation, and AGENTS.md wait until after fresh proof.
```

---

## 15. Remaining local docs completion and human acceptance {#remaining-local-docs-completion-and-human-acceptance}

Stage 4 creates the remaining local docs system for `ork_planner`. This is where the pilot becomes usable as a local documentation structure.

### 15.1. Minimum Stage 4 outputs {#stage-4-minimum-outputs}

Stage 4 must create at least:

```text
.ai/subprojects/ork_planner/ork_planner_readme.md
.ai/subprojects/ork_planner/ork_planner_status.md
.ai/subprojects/ork_planner/ork_planner_decisions.md
.ai/subprojects/templates/subproject_plan_full_template.md
.ai/subprojects/templates/subproject_plan_index_template.md
.ai/subprojects/templates/subproject_navigation_template.md
.ai/subprojects/templates/subproject_journal_template.md
.ai/subprojects/templates/subproject_battle_plan_template.md
.ai/subprojects/templates/subproject_readme_template.md
.ai/subprojects/templates/subproject_status_template.md
.ai/subprojects/templates/subproject_decisions_template.md
.ai/subprojects/templates/subproject_templates_guide.md
```

It may update existing local docs:

```text
ork_planner_plan_index.md
ork_planner_navigation.md
ork_planner_journal.md
ork_planner_battle_plan.md
ork_planner_plan_full.md
```

But all updates must remain inside `.ai/subprojects/ork_planner/` and `.ai/subprojects/templates/` unless human explicitly returns the work to Planner and expands the plan. Stage 4 is not repo-level alignment.

### 15.2. What `readme` must do {#readme-purpose-stage-4}

`ork_planner_readme.md` is the human entry document. It should be short and understandable. It must not become status, journal, battle plan, or decision log.

It should answer:

- what is `ork_planner`;
- why it exists;
- what stage it is in;
- which docs exist;
- which docs to read first;
- what not to use;
- what the next safe step is;
- how human can check the process.

### 15.3. What `status` must do {#status-purpose-stage-4}

`ork_planner_status.md` is the current live state. It should be short. It must answer:

- current lifecycle stage;
- current owner role;
- active gate;
- last completed step;
- next allowed step;
- blockers;
- human action needed;
- last update.

It must not duplicate the journal.

### 15.4. What `decisions` must do {#decisions-purpose-stage-4}

`ork_planner_decisions.md` is Orc-owned execution decision log. It is separate from `ork_planner_plan_decisions.md`.

It should record decisions made during live execution, such as:

- route choice;
- accepted nav pass result;
- battle plan approval outcome;
- human scope changes;
- waivers;
- blockers;
- rejected alternatives.

It should not rewrite planner-stage history.

### 15.5. What Stage 4 reusable templates and guide must do {#stage-4-templates-guide}

The reusable template layer in `.ai/subprojects/templates/` must cover the full planned documentation set used by this pilot:

- `subproject_plan_full_template.md`
- `subproject_plan_index_template.md`
- `subproject_navigation_template.md`
- `subproject_journal_template.md`
- `subproject_battle_plan_template.md`
- `subproject_readme_template.md`
- `subproject_status_template.md`
- `subproject_decisions_template.md`

The guide file:

```text
.ai/subprojects/templates/subproject_templates_guide.md
```

must explain in plain Russian:

- when each template is used;
- who owns the corresponding document;
- what the file is for;
- what the file must not become;
- what should be created first in a new subproject;
- which files are human-first and which are agent-oriented;
- how the set supports `Planner -> Orc`.

The template layer must be reusable, not hard-coded only for `ork_planner`.

### 15.6. Human acceptance of Stage 4 {#stage-4-human-acceptance}

Stage 4 is accepted only if human can do a practical read-and-follow test:

1. Open `ork_planner_readme.md`.
2. Understand what `ork_planner` is.
3. Follow links to `navigation` and `status`.
4. Understand current stage and next step.
5. See what has been done in `journal`.
6. See what decisions are accepted in `decisions`.
7. Open `.ai/subprojects/templates/subproject_templates_guide.md`.
8. Understand what each reusable template is for and how a future subproject should use them.
9. Confirm that no repo-level alignment started early.
10. Confirm that no legacy active route returned.

If the human cannot understand the route, Stage 4 is not accepted even if all files exist.

---

## 16. Fresh tiny docs-only pilot {#fresh-tiny-docs-only-pilot}

Stage 5 is mandatory. It exists because `ork_planner` is a meta/workflow pilot and can accidentally pass by being over-explained. A fresh tiny docs-only subproject tests whether the process works on clean context.

### 16.1. Why fresh proof is required {#why-fresh-proof-required}

Without Stage 5, the repo-level alignment wave would be based only on `ork_planner`. That is not enough, because `ork_planner` has unusual context:

- it is about the workflow itself;
- it has many external critiques;
- it has long planner decisions;
- it has human clarifications;
- it has a history of V3 draft and rewrite.

A tiny fresh subproject proves that the documentation system is usable without all that special history.

### 16.2. Stage 5 constraints {#stage-5-constraints}

The fresh pilot must be:

- docs-only;
- very small;
- created from scratch;
- low-risk;
- not a source-code change;
- not a repo-level rules migration;
- not a hidden continuation of `ork_planner`;
- fast enough that human can review the whole thing.

### 16.3. Required process for fresh pilot {#fresh-pilot-required-process}

The fresh pilot must pass through the same conceptual route:

```text
Planner prepares small plan.
Human accepts.
Orc starts only after explicit signal.
Orc proposes route.
Human approves route where needed.
Orc creates minimal docs.
Journal/status/decisions appear only as live execution artifacts.
Human accepts result.
```

The exact document set may be smaller if the tiny task justifies it, but any reduction must be explicit and must not weaken role boundaries.

### 16.4. Acceptance of fresh pilot {#fresh-pilot-acceptance}

Stage 5 is accepted only if:

- the new subproject was created from scratch;
- it stayed docs-only;
- the route followed Planner -> Orc;
- human could understand and accept the result;
- no repo-level files were changed;
- no legacy route returned;
- documentation was sufficient to resume after context loss.

---

## 17. Repo-level alignment wave after fresh proof {#repo-level-alignment-wave-after-fresh-proof}

Stage 6 is the first repo-level alignment wave. It is deliberately delayed until after local `ork_planner` proof and fresh tiny proof.

### 17.1. Fixed scope {#repo-level-fixed-scope}

Stage 6 fixed scope:

```text
.ai/rules/codex_role_planner.md
.ai/rules/codex_role_orc.md
.ai/rules/codex_orchestrator.md
.ai/repo_navigation.md
AGENTS.md
```

No other repo-level files are in scope by default.

### 17.2. Purpose {#repo-level-purpose}

The purpose is targeted alignment, not broad rewrite.

Stage 6 should:

- align Planner role contract with proven pilot behavior;
- align Orc role contract with proven pilot behavior;
- align orchestrator rules with route choice and human gates;
- update repo navigation so future agents can find the new docs;
- update `AGENTS.md` only where needed to reference the accepted Planner -> Orc contract and gates.

### 17.3. What Stage 6 must not do {#repo-level-must-not-do}

Stage 6 must not:

- rewrite all repo workflow docs broadly;
- revive old active route terms;
- add new global tools without explicit decision;
- change source code;
- change `.ai/project_state.md` by default;
- change ideas docs by default;
- treat fresh pilot as optional;
- claim repo-level alignment before local evidence exists.

### 17.4. Stage 6 route discipline {#repo-level-route-discipline}

Because Stage 6 changes workflow rules, future Orc should strongly consider Kilo and/or bounded external review. But route remains a choice:

```text
Orc proposes route.
Human chooses/approves.
```

For each file in scope, Stage 6 should state:

- why it needs update;
- exact intended change type;
- forbidden expansions;
- verification method;
- human check.

---

## 18. Session binding and session != journal {#session-binding-and-session-not-journal}

Session and journal are related but not interchangeable.

### 18.1. Session {#session}

Session is the repo-level orchestration frame for a chat/run. It tracks:

- session ID;
- goal;
- approved plan;
- active plan item;
- runs;
- user overrides;
- checkpoint state;
- relation to Kilo or external tool runs.

A session belongs to the broader workflow. It may cover work across multiple files or stages.

### 18.2. Journal {#journal}

`ork_planner_journal.md` is subproject execution history. It tracks factual actions inside this subproject:

- what was done;
- when;
- by which role/tool route;
- which files changed;
- what evidence exists;
- what checks ran;
- what human verdict was given;
- what blockers remain.

Journal does not replace session. Session does not replace journal.

### 18.3. Binding rule {#session-journal-binding-rule}

When future Orc writes journal entries, each meaningful entry should reference the relevant session/run if available.

Recommended journal field:

```md
Session reference: `.ai/plans/sessions/YYYY-MM-DD_<session-id>.md`, run `00N` / `not available`
```

If session metadata is unavailable, journal must say so instead of inventing it.

### 18.4. Current state {#session-journal-current-state}

At Stage 1, this document does not create journal and does not create session entries. It only defines how future Orc should bind them.

---

## 19. Minimal required blocks for future docs {#minimal-required-blocks-for-future-docs}

This section gives minimum blocks for future docs. It does not create them now.

### 19.1. `ork_planner_plan_index.md` {#minimal-plan-index}

Purpose:

```text
Agent-oriented index for `ork_planner_plan_full.md`.
```

Important: this file is for agents, not for human readers.

Minimum blocks:

```md
# Ork Planner Plan Index

Slug: `ork_planner`
Target file: `ork_planner_plan_full.md`
Owner: `Orc`
Audience: agents
Status: `active` / `draft`
Last updated: YYYY-MM-DD

## Purpose
## Audience and non-goals
## Index rule
## Fast anchor table
## Stage-to-anchor map
## Gate-to-anchor map
## Role-boundary anchors
## Maintenance rule
## Last anchor audit
```

Rules:

- use stable semantic anchors;
- do not use line numbers as authority;
- mark anchors as audited or provisional;
- do not become human README;
- do not duplicate the whole plan.

### 19.2. `ork_planner_navigation.md` {#minimal-navigation}

Purpose:

```text
Subproject-wide navigation map.
```

Minimum blocks:

```md
# Ork Planner Navigation

Slug: `ork_planner`
Owner: `Orc`
Status: `active`
Last updated: YYYY-MM-DD

## Purpose
## Current lifecycle stage
## Start here
## Existing documents
## Planned documents not created yet
## Planner-owned documents
## Orc-owned documents
## Do not use / non-canonical files
## Reading routes
## Tool/external material references
## Maintenance rule
```

Rules:

- must say that `plan_index` is for agents;
- must say that human entry later comes through `readme`;
- must list `plan_navigation` and `plan_active_1` as non-canonical if they appear in old references;
- must not pretend future docs already exist.

### 19.3. `ork_planner_journal.md` {#minimal-journal}

Purpose:

```text
Factual execution log for Orc actions.
```

Minimum blocks:

```md
# Ork Planner Journal

Slug: `ork_planner`
Owner: `Orc`
Status: `active`
Started: YYYY-MM-DD

## Journal policy
## Entry format
## Historical context note
## Entries
## Bugs and difficulties
## Open follow-ups
```

Minimum entry format:

```md
### J-YYYYMMDD-001 — <short title>

- Lifecycle stage:
- Role:
- Tool route:
- Session reference:
- Files created:
- Files modified:
- Evidence:
- Verification:
- Human verdict:
- Bugs and difficulties:
- Next step:
```

Rules:

- factual entries only;
- no fake backfill;
- historical context must be labelled as context, not action;
- must include bugs/difficulties discipline.

### 19.4. `ork_planner_battle_plan.md` {#minimal-battle-plan}

Purpose:

```text
One operational battle plan for the remaining pilot path.
```

Minimum blocks:

```md
# Ork Planner Battle Plan

Slug: `ork_planner`
Owner: `Orc`
Parent plan: `ork_planner_plan_full.md`
Status: `draft` / `pending-human-approval` / `approved`
Lifecycle stage: `Stage 3`

## Purpose
## Preconditions
## Scope
## Non-goals
## Allowed writes
## Forbidden writes
## Source basis
## Step sequence
## Tool route recommendation or waiver per step
## Evidence and checks
## Human gates
## Stop rules
## Escalation rules
## Acceptance criteria
```

Rules:

- single file only;
- no `plan_active_1`;
- no Stage 4 execution before human approval;
- must include route choice and waivers;
- must include stop condition.

### 19.5. `ork_planner_readme.md` {#minimal-readme}

Purpose:

```text
Human entry door for the subproject.
```

Minimum blocks:

```md
# Ork Planner Readme

Slug: `ork_planner`
Owner: `Orc`
Audience: human first
Status: `active`

## What this is
## Why it exists
## Current plain-Russian status
## What to read first
## What exists now
## What does not exist yet
## Current safe next step
## Role warning
## Non-canonical files
## Human check
```

Rules:

- plain Russian;
- short;
- not journal;
- not status;
- not battle plan;
- not decision log.

### 19.6. `ork_planner_status.md` {#minimal-status}

Purpose:

```text
Current live state of the subproject.
```

Minimum blocks:

```md
# Ork Planner Status

Slug: `ork_planner`
Owner: `Orc`
Status updated: YYYY-MM-DD

## Current lifecycle stage
## Current owner role
## Current gate
## Last completed action
## Current active document
## Next allowed step
## Blockers
## Human action needed
## Verification state
## Resume instruction
```

Rules:

- short;
- updated at gates and before context compaction;
- does not duplicate journal;
- never claims acceptance without human verdict.

### 19.7. `ork_planner_decisions.md` {#minimal-decisions}

Purpose:

```text
Orc-owned execution decision log.
```

Minimum blocks:

```md
# Ork Planner Decisions

Slug: `ork_planner`
Owner: `Orc`
Status: `active`

## Decision policy
## Accepted execution decisions
## Superseded execution decisions
## Rejected options
## Waivers
## Human approvals
## Relation to planner decision log
```

Decision entry format:

```md
### OD-YYYYMMDD-001 — <decision title>

- Status:
- Decision:
- Reason:
- Consequence:
- Affected files:
- Evidence:
- Human approval:
```

Rules:

- separate from `ork_planner_plan_decisions.md`;
- records live execution decisions only;
- should not rewrite Planner decisions;
- can reference Planner decisions when they guide execution.

### 19.8. Reusable template layer for future subprojects {#minimal-reusable-template-layer}

Purpose:

```text
Reusable base for future Planner -> Orc subprojects.
```

Required files:

```text
.ai/subprojects/templates/subproject_plan_full_template.md
.ai/subprojects/templates/subproject_plan_index_template.md
.ai/subprojects/templates/subproject_navigation_template.md
.ai/subprojects/templates/subproject_journal_template.md
.ai/subprojects/templates/subproject_battle_plan_template.md
.ai/subprojects/templates/subproject_readme_template.md
.ai/subprojects/templates/subproject_status_template.md
.ai/subprojects/templates/subproject_decisions_template.md
.ai/subprojects/templates/subproject_templates_guide.md
```

Rules:

- file and folder names stay English;
- document bodies may be Russian;
- templates must be generic enough for future subprojects;
- templates must preserve role boundaries and human gates;
- the guide must explain order of use and file responsibility in simple Russian;
- `ork_planner` may be the proving ground, but the template layer must not be locked to `ork_planner` wording.

---

## 20. Acceptance gates {#acceptance-gates}

Acceptance gates are rewritten for the new lifecycle. They do not track package/import stages as active work.

### 20.1. Gate 1 — Planner base accepted {#gate-1-planner-base-accepted}

Required evidence:

- `ork_planner_plan_full.md` exists as rewritten canonical Planner base;
- six-stage lifecycle is present;
- no active package/import lane remains;
- Section 11 is only provenance note;
- no dedicated unresolved-decision section exists;
- `plan_navigation` is absent from canonical model;
- `plan_active_1` is not canonical;
- one `battle_plan` model is present;
- Stage 2 creates exactly `plan_index`, `navigation`, `journal`;
- human accepts or requests targeted edits.

Status at this document:

```text
Pending human acceptance.
```

### 20.2. Gate 2 — Pre-Orc grill-me passed {#gate-2-grill-me-passed}

Required evidence:

- Orc answers grill-me questions correctly;
- Orc restates allowed writes;
- Orc restates forbidden writes;
- Orc confirms it has not started before approval;
- Orc proposes concrete tool route;
- human chooses/approves route.

Blocks:

```text
Stage 2 cannot start until this gate is closed.
```

### 20.3. Gate 3 — First Orc nav pass accepted {#gate-3-nav-pass-accepted}

Required evidence:

- `ork_planner_plan_index.md` created;
- `ork_planner_navigation.md` created;
- `ork_planner_journal.md` created;
- `plan_full` edits, if any, limited to anchors/quick links/navigation clarity/typos;
- forbidden files not touched;
- journal contains factual Stage 2 entry;
- report returned;
- human accepts report.

Blocks:

```text
Stage 3 cannot start until this gate is closed.
```

### 20.4. Gate 4 — One battle plan approved {#gate-4-battle-plan-approved}

Required evidence:

- `ork_planner_battle_plan.md` created;
- no `plan_active_1` created;
- battle plan has required blocks;
- allowed/forbidden writes are clear;
- route recommendations or waivers are clear;
- human approves.

Blocks:

```text
Stage 4 cannot start until this gate is closed.
```

### 20.5. Gate 5 — Local ork_planner docs accepted {#gate-5-local-docs-accepted}

Required evidence:

- `ork_planner_readme.md` created;
- `ork_planner_status.md` created;
- `ork_planner_decisions.md` created;
- template layer created in `.ai/subprojects/templates/`;
- `subproject_templates_guide.md` created;
- `navigation` updated to include actual docs;
- `navigation` updated to include template layer;
- `journal` records Stage 4 actions;
- human can follow docs route;
- human can understand how the templates should be reused by future subprojects;
- no repo-level files touched;
- human accepts local docs system.

Blocks:

```text
Stage 5 cannot start until this gate is closed.
```

### 20.6. Gate 6 — Fresh tiny docs-only pilot accepted {#gate-6-fresh-pilot-accepted}

Required evidence:

- new tiny docs-only subproject created from scratch;
- Planner -> Orc route followed;
- task stayed small and docs-only;
- human accepted result;
- process worked on clean context;
- no repo-level alignment started early.

Blocks:

```text
Stage 6 cannot start until this gate is closed.
```

### 20.7. Gate 7 — Repo-level alignment accepted {#gate-7-repo-alignment-accepted}

Required evidence:

- changes limited to fixed scope;
- each file has targeted reason;
- no broad rewrite beyond approved scope;
- role docs align with proven lifecycle;
- `AGENTS.md` alignment is targeted;
- `.ai/repo_navigation.md` points to accepted docs;
- verification/report exists;
- human accepts.

This gate completes the first alignment wave, not the entire future evolution of the workflow.

---

## 21. Anchor map {#anchor-map}

This anchor map is part of `plan_full` itself. Stage 2 may audit and repair it.

| Section | Anchor | Purpose |
|---|---|---|
| 1. Title and document purpose | `#title-and-document-purpose` | Why this document exists |
| 2. Quick navigation | `#quick-navigation` | Fast links inside this file |
| 3. Mission of ork_planner | `#mission-of-ork-planner` | Why the pilot exists |
| 4. Non-goals and forbidden drifts | `#non-goals-and-forbidden-drifts` | Safety boundaries |
| 5. Source basis and authority | `#source-basis-and-source-authority-order` | Source priority |
| 6. Planner role boundaries | `#planner-role-boundaries` | Planner limits |
| 7. Planner-owned vs Orc-owned | `#planner-owned-vs-orc-owned-artifacts` | Artifact ownership |
| 8. Canonical artifact model | `#canonical-artifact-model-for-this-pilot` | File model by stage |
| 9. Lifecycle overview | `#lifecycle-overview` | Six stages |
| 10. V1/V3/Kilo usage | `#v1-v3-kilo-usage-and-recommend-or-waive-rule` | Tool route discipline |
| 11. Provenance note | `#provenance-note-for-first-v3-draft` | Historical V3 note only |
| 12. First Orc nav pass | `#first-orc-nav-pass` | Stage 2 detail |
| 13. One battle plan | `#one-battle-plan-and-approval-gate` | Stage 3 detail |
| 14. Three hard phases | `#three-hard-phases-of-the-pilot` | Safety grouping |
| 15. Remaining local docs | `#remaining-local-docs-completion-and-human-acceptance` | Stage 4 detail |
| 16. Fresh tiny pilot | `#fresh-tiny-docs-only-pilot` | Stage 5 detail |
| 17. Repo-level alignment | `#repo-level-alignment-wave-after-fresh-proof` | Stage 6 detail |
| 18. Session != journal | `#session-binding-and-session-not-journal` | State/evidence distinction |
| 19. Minimal doc blocks | `#minimal-required-blocks-for-future-docs` | Future templates |
| 20. Acceptance gates | `#acceptance-gates` | Gate model |
| 21. Anchor map | `#anchor-map` | Anchor overview |

---

## Final operating rule {#final-operating-rule}

The shortest safe summary of this whole plan:

```text
Accept plan_full first.
Run mandatory grill-me.
Orc proposes route; human chooses.
Stage 2 creates exactly plan_index + navigation + journal.
Stage 3 creates one battle_plan and stops for approval.
Stage 4 completes local ork_planner docs and creates reusable templates plus usage guide.
Stage 5 proves the workflow on a fresh tiny docs-only subproject.
Stage 6 aligns only the fixed repo-level files.
Planner -> Orc remains the only active route.
```
