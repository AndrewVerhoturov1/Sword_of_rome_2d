# Ork Planner Full Plan

Slug: `ork_planner`  
Status: draft_v1  
Last updated: 2026-05-31

<a id="purpose"></a>

## 1. Purpose

Создать новый подпроект `ork_planner` как planning-first documentation container в active системе `Planner -> Orc`.

Этот первый план не запускает Orc-mode, не открывает execution slice и не создаёт legacy B1/BOS-структуру. Его задача — зафиксировать безопасную стартовую рамку подпроекта и подготовить следующие решения человека.

<a id="current-execution-model"></a>

## 2. Current Execution Model

- текущая роль: `Planner`;
- active route проекта: `Planner -> Orc`;
- этот шаг создаёт только planning artifact;
- Orc пока не запускается;
- `V1` может использоваться как внешний second opinion для усиления плана;
- `V2`, `V3`, `Kilo` на этом шаге не обязательны.

<a id="scope"></a>

## 3. Scope Of This First Version

В scope первой версии:

- создать папку подпроекта `ork_planner`;
- записать первый полный planning-документ;
- зафиксировать границы подпроекта;
- предложить точечные `/v1` вопросы, которые могут улучшить дальнейший план.

Вне scope первой версии:

- запуск Orc;
- создание execution logs, reports или B1-like артефактов;
- product-code work;
- изменение global workflow docs;
- утверждение окончательной структуры downstream execution-файлов без дополнительной проверки.

<a id="subproject-boundary"></a>

## 4. Subproject Boundary

`ork_planner` трактуется как подпроект для planning/documentation работы вокруг роли Planner и её рабочего маршрута внутри active repo workflow.

Подпроект пока не объявляется большим program-level migration stream. На этой стадии он остаётся узким контейнером для:

- уточнения обязанностей Planner;
- подготовки безопасного handoff в Orc только тогда, когда человек сочтёт это уместным;
- накопления решений по planning-side workflow без возврата к legacy `Boss / B1 / Junior Orchestrator`.

<a id="initial-structure"></a>

## 5. Initial Structure

Первая версия intentionally минимальна:

```text
.ai/subprojects/ork_planner/
  ork_planner_plan_full.md
```

Следующие документы считаются вероятными кандидатами для следующего шага, но сейчас не создаются автоматически:

- `ork_planner_readme.md`
- `ork_planner_navigation.md`
- `ork_planner_plan_index.md`
- `ork_planner_plan_active_1.md`
- `ork_planner_status.md`
- `ork_planner_decisions.md`
- `ork_planner_journal.md`

Причина: для роли `Planner` важнее сначала зафиксировать первый полный план и проверить его человеком, чем сразу раздувать execution-pack.

<a id="role-rules"></a>

## 6. Planner Rules For This Subproject

- Planner не должен молча становиться Orc.
- Planner обязан советоваться с человеком на важных развилках.
- Planner должен предлагать внешний чат, когда нужен bounded second opinion по planning/design вопросам.
- Planner не должен реанимировать legacy `Boss / B1 / Junior Orchestrator`.
- Planner не должен создавать лишнюю иерархию до подтверждения, что она реально нужна.

<a id="suggested-v1-questions"></a>

## 7. Suggested `/v1` Questions

Ниже три точечных `/v1` вопроса, которые могут улучшить следующий шаг плана.

### V1-Question 1 — minimal subproject artifact set

Цель: проверить, какой минимальный набор документов действительно нужен именно для Planner-first старта подпроекта, не смешивая его с Orc bootstrap.

Короткая формулировка вопроса:

```text
Нужен grounded second opinion: для нового subproject `ork_planner` в active route `Planner -> Orc` какой минимальный стартовый documentation set логичнее создать сразу, если текущая роль = Planner, а Orc ещё не запускается? Сравни варианты: только `plan_full`, `plan_full + readme`, полный minimal pack. Дай recommendation с аргументами за минимальность, clarity и non-legacy safety.
```

### V1-Question 2 — граница Planner vs Orc

Цель: уточнить, какие planning artifacts должен подготовить Planner до handoff, а какие должны впервые появляться уже в первом Orc-шаге.

Короткая формулировка вопроса:

```text
Нужен grounded second opinion: в active workflow `Planner -> Orc` где лучше провести границу между Planner artifacts и first Orc bootstrap? Какие документы Planner должен создавать сам, а какие лучше отложить до первого Orc step, чтобы не смешивать planning и execution?
```

### V1-Question 3 — naming and file contract

Цель: проверить, не конфликтует ли текущая идея `ork_planner_plan_full.md` с accepted design source и migration notes, и какой naming safest для active подпроекта.

Короткая формулировка вопроса:

```text
Нужен grounded second opinion: для нового active subproject `ork_planner` какой naming/file contract safest с учётом accepted design source про slug-prefixed files и migration notes про Planner -> Orc? Проверь, достаточно ли старта с `ork_planner_plan_full.md`, или safer добавить ещё один companion file сразу.
```

<a id="human-checkpoints"></a>

## 8. Planned Human Checkpoints

- Человек смотрит, согласен ли он с тем, что первая версия подпроекта пока состоит только из `plan_full`.
- Человек выбирает, какой из трёх `/v1` вопросов запускать первым, если внешний second opinion нужен сейчас.
- Только после этого решается, надо ли расширять подпроект до `readme/navigation/status/decisions` или передавать следующий шаг Orc.

<a id="risks"></a>

## 9. Risks

- Слишком раннее создание полного documentation-pack может незаметно включить Orc bootstrap раньше времени.
- Слишком маленький старт может оказаться неудобным для resume/navigation.
- Без внешнего second opinion можно слишком быстро принять локальное naming/structure решение, которое потом придётся корректировать.
- Есть риск по инерции повторить legacy-паттерны из старых rollout-артефактов.

<a id="acceptance-criteria"></a>

## 10. Acceptance Criteria

Первая версия плана считается созданной, если:

- существует папка `.ai/subprojects/ork_planner/`;
- в ней есть `ork_planner_plan_full.md`;
- план явно фиксирует active route `Planner -> Orc`;
- план явно запрещает возврат к legacy `Boss / B1 / Junior Orchestrator`;
- план содержит 3 точечных `/v1` вопроса для улучшения следующего шага;
- план не запускает Orc и не создаёт legacy/execution дерево.

<a id="next-step"></a>

## 11. Next Step

Ближайший следующий шаг после review человеком:

1. Выбрать, нужен ли сейчас один из трёх `/v1` вопросов.
2. Если нужен — подготовить конкретный `/v1` prompt по repo template.
3. Если не нужен — решить, расширять ли подпроект до compact Planner pack (`readme/navigation/status/decisions`) или оставить только `plan_full` до первого Orc handoff.
