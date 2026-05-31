# Ork Planner Full Plan

Slug: `ork_planner`  
Status: draft  
Last updated: 2026-05-31

<a id="purpose"></a>

## 1. Purpose

Создать новый подпроект `ork_planner` как documentation container в active системе `Planner -> Orc`.

Цель этого setup-шага: подготовить минимальный active documentation set для подпроекта и на этом остановиться, не переходя к execution work.

<a id="current-execution-model"></a>

## 2. Current Execution Model

Принятая схема для этого подпроекта:

- один Planning Chat;
- один будущий Execution Chat;
- context compaction;
- документация как внешняя память;
- V1/V2/V3/Kilo как внешние инструменты;
- без постоянных субагентов;
- без отдельных B1 block folders.

На текущем шаге Orc-mode не запускается.

<a id="documentation-structure"></a>

## 3. Documentation Structure

Подпроект в первой версии должен содержать только следующие документы:

- `ork_planner_readme.md`
- `ork_planner_navigation.md`
- `ork_planner_plan_full.md`
- `ork_planner_plan_index.md`
- `ork_planner_plan_active_1.md`
- `ork_planner_journal.md`
- `ork_planner_status.md`
- `ork_planner_decisions.md`

<a id="slug-naming-rule"></a>

### 3.1. Slug Naming Rule

Все документы подпроекта начинаются с `ork_planner_`.

<a id="required-files"></a>

### 3.2. Required Files

- `ork_planner_readme.md`
- `ork_planner_navigation.md`
- `ork_planner_plan_full.md`
- `ork_planner_plan_index.md`
- `ork_planner_plan_active_1.md`
- `ork_planner_journal.md`
- `ork_planner_status.md`
- `ork_planner_decisions.md`

<a id="optional-files"></a>

### 3.3. Optional Files

- `ork_planner_plan_active_2.md`
- `ork_planner_plan_active_3.md`
- `ork_planner_reports.md`

Эти файлы сейчас не создаются.

<a id="removed-files"></a>

### 3.4. Files We Do Not Use By Default

- `blocks/`
- `B1-*`
- `BOSS_*`
- `TASK_CONTROL_PACK*`
- `SUBPROJECT_STATE.md`
- `PLANNER_HANDOFF.md`
- `ORC_EXECUTION_LOG.md`
- `CHECKPOINTS.md`
- `CONTEXT_INDEX.md`

<a id="plan-index-rules"></a>

## 4. Plan Index Rules

- использовать semantic anchors;
- не использовать line ranges как основной механизм;
- держать anchors стабильными и понятными;
- обновлять index при существенных изменениях полного плана.

<a id="active-plan-rules"></a>

## 5. Active Plan Rules

`ork_planner_plan_active_1.md` описывает только setup-срез подпроекта:

- создать документационный каркас;
- не переходить к product-work;
- не запускать Orc;
- остановиться после bootstrap.

<a id="journal-rules"></a>

## 6. Journal Rules

`ork_planner_journal.md` фиксирует только фактически выполненные действия.

Для первой версии достаточно одной стартовой записи:

- подпроект создан;
- набор файлов создан;
- следующий шаг остаётся за человеком.

<a id="status-command"></a>

## 7. Status Command

`ork_planner_status.md` хранит ближайшее состояние подпроекта.

После этого setup-шагa статус должен показывать:

- текущий active plan = `ork_planner_plan_active_1.md`;
- текущий шаг = setup завершён;
- следующий шаг = человек открывает active plan и решает, когда передавать работу Orc.

<a id="decisions-policy"></a>

## 8. Decisions Policy

`ork_planner_decisions.md` фиксирует только важные решения.

Для первой версии обязательно зафиксировать:

- active route = `Planner -> Orc`;
- legacy `B1/BOS` не используется;
- текущий setup не запускает Orc-mode.

<a id="context-compaction"></a>

## 9. Context Compaction Workflow

После сжатия контекста продолжение должно идти так:

1. Прочитать `ork_planner_status.md`.
2. Прочитать `ork_planner_plan_active_1.md`.
3. При необходимости открыть `ork_planner_navigation.md`.
4. Продолжить только с следующего human-approved шага.

<a id="external-tool-usage"></a>

## 10. V1 / V2 / V3 / Kilo Usage

- `V1` допустим как внешний second opinion по planning-вопросам, когда человек считает это уместным.
- `V2` сейчас не нужен.
- `V3` сейчас не нужен.
- `Kilo` сейчас не нужен.

Этот план не встраивает конкретные `/v1` prompts внутрь repo-документации.

<a id="reports-policy"></a>

## 11. Reports Policy

`ork_planner_reports.md` считается optional и в первой версии не создаётся.

<a id="risks"></a>

## 12. Risks

- спутать planning setup с Orc bootstrap;
- случайно восстановить legacy `Boss / B1 / Junior Orchestrator`;
- раздуть подпроект лишними файлами;
- начать product-work вместо ограниченного setup-шагa;
- забыть, что global workflow docs в этой задаче менять нельзя.

<a id="acceptance-criteria"></a>

## 13. Acceptance Criteria

Подпроект считается успешно настроенным, если:

- создана папка `.ai/subprojects/ork_planner/`;
- внутри ровно 8 стартовых файлов;
- все имена имеют префикс `ork_planner_`;
- `ork_planner_plan_full.md` содержит semantic anchors;
- `ork_planner_plan_index.md` ссылается на anchors полного плана;
- `ork_planner_status.md` указывает на `ork_planner_plan_active_1.md` как текущий active plan;
- `ork_planner_reports.md` не создан;
- legacy B1/BOS артефакты не созданы;
- global workflow docs не менялись.
