# Ork Planner Request Ideas

Slug: `ork_planner`  
Status: active-planning  
Owner: `Planner`  
Last updated: 2026-06-01

## Quick Navigation

- [Purpose](#purpose)
- [How To Use](#how-to-use)
- [Statuses](#statuses)
- [Idea Backlog](#idea-backlog)

<a id="purpose"></a>

## Purpose

Planner-owned backlog для идей будущих запросов и routing-ходов:

- `/v1`
- `/v2`
- `/v3`
- `/kilo`
- mixed route ideas

Этот файл нужен, чтобы не терять хорошие идеи во время planning-чата.

Здесь хранятся только идеи и заготовки.  
Это не decision log и не execution handoff.

<a id="how-to-use"></a>

## How To Use

- Если во время planning-чата возникает хорошая идея для внешнего вопроса, Kilo run или смешанного route, Planner записывает её сюда.
- Если идея становится принятой частью стратегии, её нужно отдельно отразить в [ork_planner_plan_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md) или в будущем `ork_planner_plan_full.md`.
- Если идея превращается в реальный запуск, Orc потом делает уже свой operational artifact отдельно.

<a id="statuses"></a>

## Statuses

- `staged` — идея появилась, но ещё не утверждена как обязательный маршрут.
- `recommended` — Planner считает идею сильной и хочет вернуться к ней.
- `promoted` — идея уже встроена в основной план или отдельное принятое решение.
- `dropped` — идея признана лишней или неподходящей.

<a id="idea-backlog"></a>

## Idea Backlog

### I-001 — Planner discipline pack

- Status: `promoted`
- Route family: `Planner policy`
- Trigger: planning по high-impact workflow и role-boundary теме
- Idea:
- сделать для режима Planner обязательными три вещи:
- ведение backlog идей запросов;
- ведение decision log;
- активный stress-test через `grill-me`
- Why useful:
- меньше потерь контекста;
- меньше забытых `/v1` / `V3` / `kilo` идей;
- меньше слабых мест в большом плане.
- Resolution:
- обязательны `decision log` и backlog идей;
- `grill-me` остаётся user-invoked, не always-on.

### I-002 — Future `/v1` critique for battle-plan structure

- Status: `promoted`
- Route family: `/v1`
- Trigger: после импорта первого живого `ork_planner_plan_full.md`
- Idea:
- спросить внешний чат, достаточно ли жёстко Planner зафиксировал:
- `three hard phases`;
- strict template для `plan_active_N`;
- gate между local proof и repo-level alignment.
- Why useful:
- это узкий bounded second opinion по role-boundary и battle-plan design.
- Resolution:
- идея принята как следующий шаг после локального импорта первого `plan_full`;
- critique должен читать уже живой repo файл, а не сырой V3 ZIP.

### I-003 — Future V3 critique package for canonical planner docs

- Status: `staged`
- Route family: `V3`
- Trigger: когда будут готовы `plan_full`, `plan_navigation`, `plan_index`, `readme`
- Idea:
- собрать artifact package только для critique canonical planner docs, без запуска Orc execution layer.
- Why useful:
- можно проверить связность doc-set до начала живого Orc цикла.

### I-004 — First V3 draft package for `ork_planner_plan_full.md`

- Status: `promoted`
- Route family: `V3`
- Trigger: до появления первого живого `ork_planner_plan_full.md`
- Idea:
- использовать внешний `V3-Ревью` как источник сильного first draft только для `ork_planner_plan_full.md`;
- задать strict outline;
- попросить большой и подробный operational document;
- raw ZIP сначала держать в local-only holding area, не вести сразу в import lane.
- Why useful:
- меньше расход локального контекста;
- сильнее первый черновик большого workflow-doc;
- Planner остаётся review and acceptance layer, а не full-text drafter с нуля.
- Resolution:
- идея принята;
- request готовится как `V3-Ревью`, не как `/v3` import-entry route.
