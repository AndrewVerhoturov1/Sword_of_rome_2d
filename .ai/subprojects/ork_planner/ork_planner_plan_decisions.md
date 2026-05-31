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
- создать `ork_planner_plan_navigation.md`;
- создать тонкий `ork_planner_plan_index.md`;
- создать `ork_planner_readme.md`;
- остановиться и вернуть report.

### D-007 — Два navigation-layer и отдельный plan index

- Должны существовать оба navigation-файла:
- `ork_planner_plan_navigation.md` — маршрут чтения большого плана;
- `ork_planner_navigation.md` — общая навигация подпроекта.
- `ork_planner_plan_index.md` тоже остаётся.
- Роли разделены так:
- `Quick Navigation` внутри `plan_full` — быстрый вход в самом файле;
- `plan_navigation` — human reading route большого плана;
- `plan_index` — тонкая anchor-map и cross-doc reference layer;
- `navigation` — общая навигация по подпроекту.

### D-008 — Общая subproject navigation появляется позже

- `ork_planner_navigation.md` не создаётся в первом nav pass.
- Она появляется во втором Orc шаге, после nav pass, после подготовки боевых планов и после human approval.

### D-009 — `readme` нужен сразу

- `ork_planner_readme.md` нужен уже в первом Orc nav pass.
- Но это не означает создание полного live execution layer в том же run.

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
- Первый реальный docs execution slice должен стартовать с:
- `codex_role_planner.md`
- `codex_role_orc.md`
- `codex_orchestrator.md`
- `.ai/repo_navigation.md`

### D-013 — Будущий live execution doc-set

- После approval Orc собирает минимальный live execution layer:
- `ork_planner_navigation.md`
- `ork_planner_plan_active_N.md`
- `ork_planner_status.md`
- `ork_planner_journal.md`
- `ork_planner_decisions.md`
- Отдельный `readme` уже существует раньше, с nav pass.

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
- `ork_planner_plan_navigation.md`
- `ork_planner_plan_index.md`
- `ork_planner_readme.md`
- `ork_planner_navigation.md`
- `ork_planner_plan_active_1.md` или последовательность `plan_active_N`
- `ork_planner_status.md`
- `ork_planner_journal.md`
- `ork_planner_decisions.md`

### D-022 — Planner фиксирует `three hard phases`, но не точное число `plan_active_N`

- Planner не оставляет Orc полную свободу в разрезке execution route.
- Нельзя смешивать три фазы:
- local live ops bootstrap;
- local docs execution + human acceptance;
- repo-level alignment.
- Orc может сам решить, будет ли это 3 или больше active plans, но границы фаз жёсткие.

### D-023 — Каждый `plan_active_N` должен иметь strict execution template

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
- `plan_navigation`
- `plan_index`
- `readme`
- `navigation`
- `status`
- `journal`
- `decisions`
- `plan_active_N`

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

<a id="execution-sequence"></a>

## Execution Sequence

Текущая принятая последовательность:

1. Planner подготавливает `V3-Ревью` request для первого драфта `ork_planner_plan_full.md`.
2. Внешний V3 возвращает raw draft package в local-only holding area.
3. Planner review-ит raw draft и только после этого собирает живой `ork_planner_plan_full.md`.
4. Orc через первый Kilo run делает nav pass:
- anchors
- `Quick Navigation`
- `ork_planner_plan_navigation.md`
- `ork_planner_plan_index.md`
- `ork_planner_readme.md`
5. Orc через отдельный Kilo run создаёт боевые планы.
6. Человек утверждает боевые планы.
7. Orc начинает первый local docs execution slice.
8. После local proof и human acceptance Orc может переходить к первому repo-level alignment wave:
- `.ai/rules/codex_role_planner.md`
- `.ai/rules/codex_role_orc.md`
- `.ai/rules/codex_orchestrator.md`
- `.ai/repo_navigation.md`
- `AGENTS.md`

<a id="open-notes"></a>

## Open Notes

- Этот файл фиксирует только уже принятые решения.
- Он не является полным `plan_full`.
- Идеи, гипотезы и будущие `v1/v2/v3/kilo` запросы надо держать отдельно от этого decision log.
