# {Subproject Title} Battle Plan

Слаг: `{subproject_slug}`  
Владелец: `Orc`  
Статус: `draft / pending human approval / accepted / superseded`  
Дата: `YYYY-MM-DD`  
Основан на: `{subproject_slug}_plan_full.md`  
Active route: `Planner -> Orc`

## Назначение

Этот файл — сжатый исполнительный конспект принятого `{subproject_slug}_plan_full.md`.

Он берёт из полного плана **все оставшиеся шаги, которые ещё нужно выполнить**, и переписывает их для Орка в короткой, конкретной и исполняемой форме.

Главная идея:

```text
plan_full = полный стратегический план, объяснения, lifecycle, обоснования, scope, gates.
battle_plan = сокращённый план выполнения оставшихся шагов из plan_full для Orc.
```

Battle plan не является новой стратегией. Он не спорит с `plan_full` и не заменяет его. Он помогает Орку понять, **как выполнять уже принятый полный план**, не перечитывая каждый раз все подробные объяснения.

## Что обязательно сохраняется из plan_full

Battle plan должен сохранить:

- порядок оставшихся stages/steps;
- human gates;
- role boundaries;
- allowed paths;
- forbidden paths;
- verification requirements;
- stop rules;
- acceptance criteria;
- важные ограничения scope.

Если какой-то шаг из `plan_full` ещё не выполнен, он должен быть отражён в battle plan либо как explicit remaining step, либо как intentionally deferred/waived item с причиной.

## Что нужно убрать из plan_full при сжатии

Battle plan обычно убирает:

- длинные объяснения;
- исторические отступления;
- повторяющиеся обоснования;
- альтернативы, которые уже не выбраны;
- дискуссии и critique;
- подробные narrative sections;
- лишние описания, которые не помогают исполнению.

Вместо этого он оставляет:

```text
что сделать -> где сделать -> чем проверить -> где остановиться -> какой human gate нужен
```

## Границы

Этот battle plan не должен становиться:

- вторым `plan_full`;
- новым master plan;
- rewrite стратегии;
- списком идей;
- critique;
- journal;
- status snapshot;
- decisions log;
- разрешением обходить human gates.

Если Орк видит, что `plan_full` ошибочен или устарел, он не исправляет стратегию внутри battle plan молча. Он должен остановиться и запросить human decision или вернуть вопрос Planner, если это Planner-level issue.

## Human gate

Перед тем как использовать battle plan как рабочий документ исполнения, нужен verdict человека, если battle plan создаётся или существенно меняется.

Текущий verdict:

```text
pending / accepted / needs fixes / rejected
```

Agent recommendation не закрывает этот gate.

## Source mapping

Заполнить таблицу, чтобы было видно, что battle plan действительно построен из полного плана, а не придуман заново.

| Source section in `plan_full` | Remaining execution item in battle plan | Status |
|---|---|---|
| `<section / anchor>` | `<короткий исполняемый шаг>` | `remaining / done / deferred / waived` |

Если source section не читался, не заявлять, что он учтён.

## Remaining execution path

Это главный раздел battle plan.

Каждый stage/step должен быть коротким и исполняемым.

### Stage / Step `<N>` — `<название>`

Purpose:

```text
<зачем этот шаг нужен в выполнении полного плана>
```

Do:

1. `<конкретное действие>`
2. `<конкретное действие>`
3. `<конкретное действие>`

Allowed paths:

```text
<path 1>
<path 2>
```

Forbidden paths:

```text
<path 1>
<path 2>
```

Verification:

- `<что проверить>`
- `<что проверить>`

Human gate:

```text
none / required before start / required after completion / required before next stage
```

Stop rule:

```text
<когда Орк обязан остановиться>
```

Expected output:

```text
<какой результат должен появиться>
```

Status:

```text
not started / in progress / completed / blocked / deferred / superseded
```

## Current execution pointer

Этот раздел можно обновлять, но он не должен превращать battle plan в status file.

```text
Current remaining step: <Stage / Step ID>
Next allowed action: <одно ближайшее действие>
Current gate: <pending / accepted / blocked / none>
```

Полный live snapshot всё равно хранится в `{subproject_slug}_status.md`.

## Live artifact updates after each completed step

После выполнения шага Орк обновляет:

- `{subproject_slug}_journal.md` — factual entry о выполненном действии;
- `{subproject_slug}_status.md` — короткий свежий контекст;
- `{subproject_slug}_decisions.md` — только если появилось важное решение подпроекта;
- `{subproject_slug}_navigation.md` — только если изменился список документов, routes, canonical/non-canonical files.

Не записывать в `decisions` обычный выбор инструмента или route конкретного шага, если это не стало долгоживущим правилом подпроекта.

## Verification before marking a step complete

Проверить:

- step соответствует `plan_full`;
- не пропущены remaining items из полного плана;
- allowed paths не нарушены;
- forbidden paths не изменены;
- human gate не закрыт агентом;
- следующий stage не открыт молча;
- user-facing docs написаны на русском, кроме technical identifiers.

## Bugs and difficulties

Фиксировать только реальные проблемы:

- `<bug or difficulty 1>`
- `<bug or difficulty 2>`

Если проблем нет:

```text
none found
```

## Resume note

Если контекст потерян, не продолжать по памяти.

Сначала открыть:

1. `{subproject_slug}_status.md`
2. `{subproject_slug}_navigation.md`
3. этот battle plan
4. `{subproject_slug}_plan_full.md`
5. `{subproject_slug}_decisions.md`
6. последние записи `{subproject_slug}_journal.md`

Потом продолжать только с текущего remaining step и только в рамках human gates.
