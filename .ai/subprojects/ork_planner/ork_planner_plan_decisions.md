# Ork Planner Plan Decisions

Slug: `ork_planner`  
Status: active-planning  
Owner: `Planner`  
Last updated: 2026-06-01

## Quick Navigation

- [Purpose](#purpose)
- [Role And Goal](#role-and-goal)
- [Accepted Decisions](#accepted-decisions)
- [Execution Sequence](#execution-sequence)
- [Open Notes](#open-notes)

<a id="purpose"></a>

## Purpose

Фиксация важных решений, принятых в planning-чате по новому старту `ork_planner`.

Документ нужен как memory layer на случай compaction.

Это planner-owned artifact.  
Он не заменяет будущие Orc-owned operational docs.

<a id="role-and-goal"></a>

## Role And Goal

- Текущий чат работает как `Planner`, не как `Orc`.
- Новый старт `ork_planner` должен быть `one-file first`.
- Главный читатель нового `ork_planner_plan_full.md` — человек.
- Главная цель подпроекта `ork_planner` — внедрить всю систему `Planner -> Orc`, а не просто написать один красивый документ.
- `ork_planner` — pilot subproject: мы создаём документацию и стараемся сразу ей следовать.

<a id="accepted-decisions"></a>

## Accepted Decisions

### D-001 — Новый старт остаётся planner-first

- Живой старт подпроекта не должен сразу превращаться в полный Orc-pack.
- Новый старт начинается с `ork_planner_plan_full.md`.
- Planner не должен заново создавать live `journal`, `status`, `decisions`, `plan_active_*` до явного Orc-phase.

### D-002 — План должен доводить до первого реального Orc run

- Горизонт большого плана — не только handoff boundary.
- `ork_planner_plan_full.md` должен довести систему до первого реального Orc run и проверки, что модель работает.

### D-003 — `ork_planner` = pilot, не control center

- Подпроект не становится meta-штабом над всем repo.
- Он используется как первый безопасный pilot новой модели `Planner -> Orc`.

### D-004 — После пилота Orc делает не только subproject docs

- Реальная задача Orc после planning-stage:
- собрать docs самого `ork_planner`;
- обновить минимально нужный repo-level workflow layer.
- Scope первого внедрения не ограничивается только подпроектной папкой.

### D-005 — Минимальный repo-level scope первого внедрения

- Обязательный минимум:
- `.ai/rules/codex_role_planner.md`
- `.ai/rules/codex_role_orc.md`
- `.ai/rules/codex_orchestrator.md`
- `.ai/repo_navigation.md`
- `project_state` сейчас не обязателен в первом docs-slice.

### D-006 — Первый Orc шаг = узкий nav pass

- Первый Orc run не делает полный execution setup.
- Он должен быть узким safety-gate шагом.
- Его задача:
- прочитать `ork_planner_plan_full.md`;
- расставить и/или починить anchors в `plan_full`;
- добавить короткий `Quick Navigation` внутрь `plan_full`;
- создать `ork_planner_plan_index.md`;
- создать `ork_planner_navigation.md`;
- создать `ork_planner_journal.md`;
- остановиться и вернуть report.

### D-007 — `plan_index` остаётся, `plan_navigation` убирается

- `ork_planner_plan_navigation.md` не нужен.
- Для большого плана остаётся только `ork_planner_plan_index.md`.
- Общая навигация подпроекта живёт в `ork_planner_navigation.md`.
- Роли разделены так:
- `Quick Navigation` внутри `plan_full` — быстрый вход в самом файле;
- `plan_index` — агентный маршрут чтения и рабочий index большого плана;
- `navigation` — общая навигация по подпроекту.

### D-008 — Общая subproject navigation появляется сразу

- `ork_planner_navigation.md` создаётся уже в первом nav pass.
- Это часть минимального nav/bootstrap слоя перед дальнейшей работой Orc.

### D-009 — `readme` переносится в Stage 4

- `ork_planner_readme.md` не создаётся в первом Orc nav pass.
- Он создаётся позже, когда Orc после battle-plan approval пишет весь оставшийся local docs layer.

### D-010 — Боевые планы отделены от nav pass

- После первого nav pass Orc не должен сразу переходить к реальному docs execution.
- Сначала Orc отдельным шагом готовит боевые планы.
- Боевые планы — это руководство к действию по выполнению большого `plan_full`.

### D-011 — Боевые планы делаются отдельным Kilo run

- Nav pass = один Kilo run.
- Создание боевых планов = отдельный Kilo run.
- После этого нужен human approval.

### D-012 — Первый docs execution slice идёт только после approval

- Только после утверждения боевых планов Orc начинает реальную работу подпроекта.
- Это решение в ранней формулировке больше не читается как старт с repo-level files.
- Актуальная трактовка после D-019 и D-020:
- первый реальный docs execution slice остаётся local-first внутри `.ai/subprojects/ork_planner/`;
- repo-level файлы вроде `codex_role_planner.md`, `codex_role_orc.md`, `codex_orchestrator.md`, `.ai/repo_navigation.md` и `AGENTS.md` относятся к отдельной future alignment wave после полного local cycle.

### D-013 — Будущий live execution doc-set

- После approval Orc собирает минимальный live execution layer:
- уже существующие после nav pass:
- `ork_planner_navigation.md`
- `ork_planner_journal.md`
- уже существующий после отдельного шага battle-plan:
- `ork_planner_battle_plan.md`
- создаваемые в remaining local docs wave:
- `ork_planner_readme.md`
- `ork_planner_status.md`
- `ork_planner_decisions.md`

### D-014 — Kilo route первого nav pass заранее не фиксируется жёстко

- В плане надо зафиксировать, что первый nav pass идёт через Kilo.
- Но конкретный Kilo route/mode для этого шага оставляется на решение будущего Orc после чтения `plan_full`.

### D-015 — Acceptance пилота

- Пилот считается доказанным не по факту создания файлов.
- Минимальное доказательство:
- nav pass выполнен;
- боевые планы созданы;
- боевые планы утверждены человеком;
- первый docs execution slice выполнен;
- человек принял результат.

### D-016 — Legacy route не возвращаем

- Нельзя возвращаться к `Boss / B1 / Junior Orchestrator`.
- Новый план должен явно избегать role drift в legacy execution tree.

### D-017 — В этом planning-чате Planner должен активнее предлагать `/v1` и `V3`

- Это не отдельная обязанность будущего Orc.
- Это ожидание от текущего Planner-поведения в этом чате:
- чаще вскрывать развилки;
- предлагать `/v1` и `V3`, когда они реально полезны;
- не ждать, пока человек сам напомнит про эти инструменты.

### D-018 — `plan_full` строится `lifecycle first`

- Главный каркас большого плана — путь системы во времени.
- Порядок чтения должен вести от Planner contract к nav pass, боевым планам, локальному доказательству и только потом к repo-level alignment.
- При этом главная цель подпроекта не меняется: мы внедряем документационную систему `Planner -> Orc`.

### D-019 — Local docs system делается с нуля, repo-level patching потом

- Документация самого техпроцесса `ork_planner` должна собираться как новый local pilot layer.
- Общие repo-level файлы вроде `AGENTS.md` и `.ai/rules/*` не являются первой целью пилота.
- Их можно точечно править только после доказанной работоспособности local `ork_planner` docs.

### D-020 — Gate перехода к repo-level patching = полный local cycle

- Недостаточно только nav pass или утверждённых боевых планов.
- Минимальное доказательство:
- nav pass;
- боевые планы;
- human approval боевых планов;
- первый local docs execution slice внутри `ork_planner`;
- human acceptance результата.

### D-021 — Первый полный local cycle должен дать `core + live ops`

- Одних canonical docs недостаточно.
- После первого полного цикла внутри `ork_planner` должны быть:
- `ork_planner_plan_full.md`
- `ork_planner_plan_index.md`
- `ork_planner_navigation.md`
- `ork_planner_journal.md`
- `ork_planner_battle_plan.md`
- `ork_planner_readme.md`
- `ork_planner_status.md`
- `ork_planner_decisions.md`

### D-022 — Planner фиксирует `three hard phases`, но не раздувает battle-layer

- Planner не оставляет Orc полную свободу в разрезке execution route.
- Нельзя смешивать три фазы:
- local live ops bootstrap;
- local docs execution + human acceptance;
- repo-level alignment.
- По умолчанию достаточно одного `ork_planner_battle_plan.md`, если человек не утвердил более сложную схему отдельно.

### D-023 — `battle_plan` должен иметь strict execution template

- Боевой план не должен быть свободной запиской.
- Минимум обязательных блоков:
- phase goal;
- scope;
- prerequisites;
- allowed writes;
- forbidden writes;
- step sequence;
- evidence and checks;
- human gate;
- stop and escalation rules.

### D-024 — Planner-норма для `ork_planner` = mandatory `decisions` + mandatory `ideas`

- Для нетривиального planning по `ork_planner` обязательны два planner-owned support файла:
- `ork_planner_plan_decisions.md`
- `ork_planner_planner_request_ideas.md`
- `grill-me` не становится always-on нормой и включается человеком явно.

### D-025 — Первый repo-level alignment wave включает и `AGENTS.md`

- После доказанного local pilot первая repo-level wave не ограничивается только `.ai/rules/*` и `.ai/repo_navigation.md`.
- В этот же первый alignment wave входит [AGENTS.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/AGENTS.md).

### D-026 — Первая правка `AGENTS.md` должна быть targeted alignment

- Первая wave не должна широко переписывать весь repo contract.
- Допустимы только точечные правки под новый `Planner -> Orc` contract:
- роль Planner;
- роль Orc;
- порядок перехода;
- базовые gates;
- ссылки на новые rule docs.

### D-027 — Human acceptance local pilot = `read + follow test`

- Для local proof недостаточно просто наличия файлов или operational evidence.
- Человек должен суметь:
- понять маршрут по документации;
- проверить навигацию;
- подтвердить, что цикл Orc проходит без неясных скачков между Planner и Orc.

### D-028 — Для `/v1` и `V3` действует правило `recommend or waive`

- В будущем `ork_planner_plan_full.md` Planner и Orc не должны молча забывать про внешний critique.
- Для high-impact planning и doc-architecture развилок надо:
- либо рекомендовать уместный `/v1` или `V3`;
- либо явно записывать короткий waiver, почему внешний critique сейчас не нужен.
- Это не означает автозапуск внешнего маршрута без решения человека.

### D-029 — Planner-owned support files входят в явный artifact set

- `ork_planner_plan_full.md` должен явно описывать planner-owned support set, а не считать его неформальной привычкой.
- Минимальный набор:
- `ork_planner_plan_full.md`
- `ork_planner_plan_decisions.md`
- `ork_planner_planner_request_ideas.md`

### D-030 — `plan_full` должен давать minimal templates для key docs

- Большой план не ограничивается только описанием ролей документов.
- Для key docs нужно задать минимальные обязательные блоки, но не превращать план в полный template pack.
- Это относится как минимум к:
- `plan_index`
- `readme`
- `navigation`
- `status`
- `journal`
- `decisions`
- `battle_plan`

### D-031 — В `plan_full` нужна compact migration map

- Кроме `lifecycle first`, план должен коротко показывать migration route:
- что уже есть в repo;
- что создаётся заново в `ork_planner`;
- что доказывается локально;
- что и когда поднимается в repo-level docs.

### D-032 — Historical scaffold = reference-only, non-authoritative

- Archived scaffold в `drafts/` можно читать только как historical reference и postmortem material.
- Его нельзя использовать как active source, template base или partial bootstrap нового старта.

### D-033 — `ork_planner` pilot должен быть явно привязан к repo session contract

- Будущие Orc-run'ы по `ork_planner` не должны жить как отдельный неформальный поток.
- Их надо увязывать с `.ai/plans/sessions/...`:
- plan item;
- run numbering;
- gates;
- checkpoint state.

### D-034 — `session` и `journal` не одно и то же

- `session` = repo-level рамка чата, approved plan, run history и checkpoint state.
- `journal` = subproject execution log внутри `ork_planner`.
- `journal` должен ссылаться на relevant session run, но не заменяет `session`.
- Planner в `plan_full` только описывает это разделение и не создаёт Orc-owned `journal`.

### D-035 — Первый драфт `ork_planner_plan_full.md` заказывается через `V3-Ревью`

- Для первого сильного черновика `plan_full` выбран tool route `V3-Ревью`.
- Это не `/v3` import-entry route и не `Kilo Notebook V3`.
- Внешний V3 нужен как сильный first draft, а не как source of truth.
- Финальный shape и принятие содержания остаются у Planner.

### D-036 — Первый V3-драфт обязан идти по strict outline

- Внешнему чату нельзя отдавать свободную структуру.
- Planner должен заранее задать жёсткий skeleton разделов и boundaries.
- Внутри первого драфта обязательны:
- основной `plan_full`;
- `unresolved decisions`;
- `acceptance gates`;
- `anchor map`.

### D-037 — V3 input pack должен включать published context + planner-owned local context

- Для published repo docs используется GitHub-first чтение по commit-pinned ссылкам.
- Для новых planner-owned артефактов используются сами planner files как context source.
- Минимум это:
- исходный idea file;
- active role/orchestrator docs;
- `ork_planner_plan_decisions.md`;
- `ork_planner_planner_request_ideas.md`.

### D-038 — Historical scaffold можно давать V3 только как reference-only

- Historical scaffold допустим в input pack только с жёстким дисклеймером.
- Его нельзя трактовать как canonical template или source base.
- Его роль = показать прошлую ошибочную форму и что именно не надо копировать.

### D-039 — Сырой V3 output сначала идёт в local-only holding area

- Первый V3 ZIP нельзя сразу вести в Kilo import lane.
- Сначала raw draft ложится в local-only holding area.
- Для этого pilot разрешена папка `_local/v3_drafts/ork_planner/`.
- Только после local Planner review решается, что попадёт в живой repo doc-set.

### D-040 — Первый V3 запрос должен просить большой и подробный `plan_full`

- Внешний чат не должен возвращать короткий summary или outline.
- Нужен один большой operational document, пригодный как сильный первый черновик.
- Если есть развилка между краткостью и полнотой, для этого запроса выбирается полнота.

### D-041 — Если planner files ещё не опубликованы, V3 request использует fallback local context

- Пока planner-owned файлы не видны через GitHub, request не должен делать вид, что весь source pack published.
- Допустим fallback:
- человек прикладывает planner-owned файлы вручную;
- или их содержимое явно вкладывается в prompt package.
- После публикации этих файлов GitHub-first снова становится основным режимом.

### D-042 — Первый V3 ZIP для `ork_planner_plan_full.md` импортируется вручную после local review

- Для первого драфта выбран local route:
- raw ZIP хранится в `_local/v3_drafts/ork_planner/`;
- Planner локально проверяет package structure и содержимое;
- затем один файл `ork_planner_plan_full.md` вручную вытаскивается в живой repo path.
- Это не `/v3 import-entry` и не `Kilo Notebook V3`.

### D-043 — После импорта первого `plan_full` нужен bounded `/v1` critique

- Следующий внешний шаг = prompt-only `/v1` review уже живого `ork_planner_plan_full.md`.
- Цель review:
- найти contradictions;
- проверить role boundaries;
- проверить lifecycle/gates/nav pass/battle-plan logic;
- не переписывать план с нуля.
- Это critique imported planner artifact, не новый first-draft generation route.
- `2026-06-01`: critique получен через `V1-20260601-015836`.
- Следующий локальный шаг после этого critique: targeted Planner cleanup и human acceptance decision по `plan_full`.

<a id="execution-sequence"></a>

## Execution Sequence

Текущая принятая последовательность:

1. Planner подготавливает `V3-Ревью` request для первого драфта `ork_planner_plan_full.md`.
2. Внешний V3 возвращает raw draft package в local-only holding area.
3. Planner review-ит raw draft и только после этого собирает живой `ork_planner_plan_full.md`.
4. Orc через первый Kilo run делает nav pass:
- anchors
- `Quick Navigation`
- `ork_planner_plan_index.md`
- `ork_planner_navigation.md`
- `ork_planner_journal.md`
5. Перед первым реальным Orc run человек прогоняет Orc через `grill-me` в plan mode.
6. Orc через отдельный Kilo run создаёт `ork_planner_battle_plan.md`.
7. Человек утверждает боевой план.
8. Orc создаёт весь оставшийся local docs layer `ork_planner`, кроме глобальных repo-level файлов.
9. После этого создаётся новый маленький docs-only подпроект с нуля и на нём проходится весь цикл `Planner -> Orc`.
10. Только после успешного fresh pilot и human acceptance Orc может переходить к первому repo-level alignment wave:
- `.ai/rules/codex_role_planner.md`
- `.ai/rules/codex_role_orc.md`
- `.ai/rules/codex_orchestrator.md`
- `.ai/repo_navigation.md`
- `AGENTS.md`

### D-044 — Перед первым Orc run обязателен `grill-me` gate

- До первого реального Orc запуска человек прогоняет Orc через `grill-me` в plan mode.
- Только после этого даётся команда на живой Orc run.

### D-045 — `Section 11` в rewritten `plan_full` сжимается до provenance note

- История первого V3 package может остаться только как краткая provenance note.
- Она не должна оставаться частью активного lifecycle.
- В rewritten `plan_full` не должно быть route-описания распаковки, import-stage и package-lane как текущей работы.

### D-046 — `Unresolved Decisions` убираются из rewritten `plan_full`

- К моменту нового rewrite `plan_full` должен быть decision-complete.
- Отдельный раздел `Unresolved Decisions` в конце файла не нужен.
- Нерешённые поздние вещи не должны оставаться как хвосты в canonical plan.

### D-047 — `ork_planner_plan_index.md` нужен для агентов, не для человека

- Это не human reading guide.
- Это агентный index и рабочий маршрут чтения большого `plan_full`.
- Для человека главным входом позже остаются `readme` и общая `navigation`.

### D-048 — После local ork_planner cycle обязателен fresh tiny docs-only pilot

- До repo-level alignment нужен новый маленький подпроект, созданный с нуля.
- На нём должен быть пройден полный цикл `Planner -> Orc`.
- Задача должна быть маленькой и быстрой, чтобы проверять именно техпроцесс на чистом контексте.

### D-049 — Первая repo-level alignment wave имеет фиксированный scope

- Scope первой wave:
- `codex_role_planner.md`
- `codex_role_orc.md`
- `codex_orchestrator.md`
- `.ai/repo_navigation.md`
- `AGENTS.md`
- Role docs не правятся раньше успешного fresh pilot.

### D-050 — `ork_planner_battle_plan.md` заменяет `plan_active_1` в этом подпроекте

- `ork_planner_plan_active_1.md` не является canonical operational file для `ork_planner`.
- Вместо него используется один понятный `ork_planner_battle_plan.md`.
- Только если позже человек отдельно утвердит более сложную схему, можно обсуждать дополнительные battle files.

<a id="open-notes"></a>

## Open Notes

- Этот файл фиксирует только уже принятые решения.
- Он не является полным `plan_full`.
- Идеи, гипотезы и будущие `v1/v2/v3/kilo` запросы надо держать отдельно от этого decision log.
