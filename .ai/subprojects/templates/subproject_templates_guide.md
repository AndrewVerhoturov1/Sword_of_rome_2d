# Subproject Templates Guide

Owner: `Orc`  
Audience: человек + agents  
Status: `draft-pending-local-review`  
Template layer path: `.ai/subprojects/templates/`  
Active route supported: `Planner -> Orc`

## Зачем нужен этот набор

Этот набор шаблонов нужен, чтобы будущие подпроекты создавались одинаково, понятно и без потери границ ролей.

Главная идея:

```text
Planner делает большой план.
Human принимает важные gates.
Orc исполняет принятый план и ведёт live artifacts.
```

Шаблоны не нужны ради бюрократии. Они нужны, чтобы в новом подпроекте сразу было понятно:

- где стратегия;
- где сжатый исполнительный конспект оставшихся шагов из `plan_full`;
- где текущий статус;
- где фактический журнал;
- где важные решения;
- где карта документов;
- что должен читать человек;
- что должен читать агент;
- какие gates ещё не закрыты.

## Главное правило набора

Не смешивать разные типы документов.

```text
plan_full != battle_plan
journal != status
journal != decisions
navigation != readme
planner-owned plan_decisions != Orc-owned decisions
human approval != agent recommendation
```

Если агент смешивает эти слои, подпроект быстро становится непонятным: невозможно понять, что уже принято, что только предложено, что реально сделано, а что является планом на будущее.

## Язык документов

User-facing prose пишется на русском языке.

English допустим для:

- file names;
- technical identifiers;
- route names;
- IDs;
- machine-readable values;
- code-like snippets.

Пример нормального смешения:

```text
Файл `{subproject_slug}_status.md` хранит короткий live snapshot.
```

Пример плохого варианта:

```text
This file tracks operational state and current execution layer...
```

Такой текст нужно писать по-русски, если он предназначен для человека.

## Базовая последовательность создания подпроекта

Обычный порядок для нового подпроекта:

### 1. Создать большой план

Шаблон:

```text
subproject_plan_full_template.md
```

Будущий файл:

```text
{subproject_slug}_plan_full.md
```

Владелец: `Planner`.

Это основа подпроекта. Здесь описываются цель, scope, stages, gates, constraints, allowed/forbidden areas, risks, verification, human checks.

После создания большой план должен пройти human review.

### 2. Создать agent-oriented index

Шаблон:

```text
subproject_plan_index_template.md
```

Будущий файл:

```text
{subproject_slug}_plan_index.md
```

Владелец: обычно `Orc`, но он индексирует Planner-owned plan.

Этот файл нужен агентам, чтобы быстро находить sections/anchors в `plan_full`. Он не должен пересказывать весь план заново.

### 3. Создать navigation

Шаблон:

```text
subproject_navigation_template.md
```

Будущий файл:

```text
{subproject_slug}_navigation.md
```

Владелец: `Orc`.

Это карта подпроекта: какие документы есть, что canonical, что deprecated, что читать человеку, что читать агенту.

### 4. Создать journal

Шаблон:

```text
subproject_journal_template.md
```

Будущий файл:

```text
{subproject_slug}_journal.md
```

Владелец: `Orc`.

Journal фиксирует фактические действия. Он начинается с реальных действий, а не с придуманного backfill.

### 5. Создать battle plan

Шаблон:

```text
subproject_battle_plan_template.md
```

Будущий файл:

```text
{subproject_slug}_battle_plan.md
```

Владелец: `Orc`.

Battle plan — это не отдельный мини-план и не новая стратегия. Это сжатый исполнительный конспект **оставшихся шагов из принятого `{subproject_slug}_plan_full.md`**, переписанный для Орка в конкретную форму выполнения.

Он отвечает:

```text
какие шаги из полного плана ещё не сделаны;
в каком порядке Орк их выполняет;
какие paths можно трогать;
какие paths нельзя трогать;
как проверять каждый шаг;
где Орк обязан остановиться;
где нужен human gate.
```

Из battle plan убираются длинные объяснения, обоснования, повторы и уходы в сторону. Но сами remaining steps из `plan_full` не должны исчезать без явной причины.

Перед использованием battle plan нужен human gate, если он создаётся, существенно меняется или меняет порядок выполнения принятого плана.

### 6. Создать readme

Шаблон:

```text
subproject_readme_template.md
```

Будущий файл:

```text
{subproject_slug}_readme.md
```

Владелец: `Orc`.

Readme — human-first entry door. Это первый файл для человека, который не хочет читать сразу весь план.

### 7. Создать status

Шаблон:

```text
subproject_status_template.md
```

Будущий файл:

```text
{subproject_slug}_status.md
```

Владелец: `Orc`.

Status — короткий live snapshot. Он может часто перезаписываться. В нём только самый близкий контекст: где мы сейчас, что последнее сделано, какой gate открыт, что можно делать дальше.

### 8. Создать decisions

Шаблон:

```text
subproject_decisions_template.md
```

Будущий файл:

```text
{subproject_slug}_decisions.md
```

Владелец: `Orc` for subproject execution decisions.

Decisions хранит важные решения подпроекта, а не обычный лог действий.

### 9. Поддерживать guide

Шаблон/документ:

```text
subproject_templates_guide.md
```

Guide объясняет, как пользоваться всем набором. Его не нужно копировать в каждый подпроект, если общий template layer уже существует.

## Кто владеет какими файлами

| Template | Future file | Owner | Main audience | Коротко |
|---|---|---|---|---|
| `subproject_plan_full_template.md` | `{slug}_plan_full.md` | `Planner` | human + agents | Большая стратегия |
| `subproject_plan_index_template.md` | `{slug}_plan_index.md` | `Orc` | agents | Навигация по большому плану |
| `subproject_navigation_template.md` | `{slug}_navigation.md` | `Orc` | human + agents | Карта документов |
| `subproject_journal_template.md` | `{slug}_journal.md` | `Orc` | human + agents | Фактические действия |
| `subproject_battle_plan_template.md` | `{slug}_battle_plan.md` | `Orc` | human + Orc | Сжатый исполнительный конспект оставшихся шагов из `plan_full` |
| `subproject_readme_template.md` | `{slug}_readme.md` | `Orc` | human-first | Вход для человека |
| `subproject_status_template.md` | `{slug}_status.md` | `Orc` | human + agents | Ближайший live context |
| `subproject_decisions_template.md` | `{slug}_decisions.md` | `Orc` | human + agents | Важные решения подпроекта |

## Human-first файлы

Human-first значит: человек может открыть файл и быстро понять, что происходит, без погружения в детали работы агентов.

Human-first files:

1. `{slug}_readme.md`
2. `{slug}_status.md`
3. `{slug}_navigation.md`
4. `{slug}_decisions.md`, если нужно понять решения
5. `{slug}_journal.md`, если нужно проверить историю

Самый удобный старт для человека:

```text
readme -> status -> navigation
```

Если человек проверяет, почему что-то было решено:

```text
decisions -> journal -> plan_full / plan_decisions
```

## Agent-oriented файлы

Agent-oriented значит: файл помогает агенту быстро работать, но не обязан быть первым файлом для человека.

Agent-oriented files:

1. `{slug}_plan_index.md`
2. anchors внутри `{slug}_plan_full.md`
3. `{slug}_battle_plan.md`
4. `{slug}_navigation.md`
5. `{slug}_status.md`
6. latest entries in `{slug}_journal.md`

Agent route обычно такой:

```text
navigation -> status -> plan_index -> battle_plan -> decisions -> latest journal
```

## Подробно по каждому шаблону

### `subproject_plan_full_template.md`

Для чего:

- описывает цель подпроекта;
- задаёт scope;
- задаёт stages;
- задаёт gates;
- объясняет, почему работа устроена именно так;
- фиксирует allowed/forbidden areas;
- описывает risks and verification.

Не должен становиться:

- журналом действий;
- сжатым battle plan, который показывает оставшиеся шаги выполнения `plan_full`;
- текущим status;
- отчётом о выполнении;
- списком всех мелких команд.

Кто пишет:

```text
Planner
```

Кто принимает:

```text
Human
```

Когда обновлять:

- при стратегическом изменении;
- при изменении lifecycle;
- при изменении scope;
- только с пониманием, что это большой документ.

### `subproject_plan_index_template.md`

Для чего:

- помогает агенту быстро найти нужные sections в `plan_full`;
- даёт короткую карту anchors;
- снижает риск, что агент будет перечитывать и переинтерпретировать весь план.

Не должен становиться:

- новым plan_full;
- readme для человека;
- journal;
- status;
- decisions.

Кто пишет:

```text
Orc, но индексирует Planner-owned plan
```

Важно:

```text
plan_index is agent-oriented, not human-first entry.
```

### `subproject_navigation_template.md`

Для чего:

- показывает все документы подпроекта;
- разделяет existing/planned/non-canonical;
- показывает reading routes;
- отмечает template layer, если он используется;
- помогает восстановиться после потери контекста.

Не должен становиться:

- README;
- журналом;
- decisions;
- status;
- rewrite плана.

Кто пишет:

```text
Orc
```

Когда обновлять:

- появился новый документ;
- документ стал deprecated;
- изменился lifecycle stage;
- изменились reading routes;
- появился reusable template layer.

### `subproject_journal_template.md`

Для чего:

- фиксирует, что реально произошло;
- фиксирует route/tool для evidence;
- фиксирует created/modified files;
- фиксирует verification;
- фиксирует bugs and difficulties;
- фиксирует human verdict, если он действительно был.

Не должен становиться:

- хранилищем всех решений;
- full plan;
- status;
- battle plan;
- transcript чата;
- fake backfill.

Кто пишет:

```text
Orc
```

Особое правило:

Если в journal временно попало важное решение, потому что decisions file ещё не существовал, решение нужно вынести в `{slug}_decisions.md`, а в journal оставить factual entry и пометку:

```text
Decision mirror: reflected in {slug}_decisions.md
```

### `subproject_battle_plan_template.md`

Для чего:

- берёт принятый `plan_full` как источник истины;
- выделяет из него все оставшиеся шаги, которые ещё нужно выполнить;
- переписывает эти шаги коротко и конкретно для Орка;
- показывает порядок выполнения;
- показывает allowed/forbidden paths;
- показывает verification для каждого шага;
- показывает stop rules и human gates;
- помогает Орку выполнять полный план, а не заново его планировать.

Не должен становиться:

- вторым `plan_full` с длинными объяснениями;
- новым master plan;
- списком идей;
- спором со стратегией;
- открытием следующего stage без gate;
- journal;
- status;
- decisions.

Кто пишет:

```text
Orc after accepted Planner plan exists
```

Кто утверждает:

```text
Human, если battle plan создаётся, существенно меняется или меняет порядок выполнения принятого плана
```

Важно:

Battle plan может описывать будущие stages как remaining path, но это не значит, что эти stages уже начаты. Начинается только тот stage/step, gate которого закрыт человеком или явно разрешён процессом.

Если шаг из `plan_full` ещё не выполнен, он должен быть в battle plan как remaining item, deferred item или waiver. Нельзя просто потерять его при сжатии.

### `subproject_readme_template.md`

Для чего:

- объясняет человеку, что это за подпроект;
- зачем он существует;
- где сейчас работа;
- что читать первым;
- чего ещё нет;
- какой safe next step.

Не должен становиться:

- полным планом;
- журналом;
- status history;
- decisions log;
- техническим import report.

Кто пишет:

```text
Orc
```

Когда обновлять:

- когда изменился entry point;
- когда появились новые документы;
- когда human-first explanation устарела.

### `subproject_status_template.md`

Для чего:

- хранит самый свежий короткий operational state;
- помогает продолжить работу после паузы;
- показывает current stage, current gate, last action, next allowed step, blockers.

Не должен становиться:

- длинной историей;
- журналом;
- decision log;
- battle plan;
- README.

Кто пишет:

```text
Orc
```

Ключевое правило:

```text
status may be rewritten frequently.
```

Если нужен полный history — читать journal, а не status.

### `subproject_decisions_template.md`

Для чего:

- хранит важные решения подпроекта;
- разделяет Planner decisions, Orc/subproject decisions и Human approvals;
- фиксирует rejected options and waivers;
- помогает не повторять уже решённые споры.

Не должен становиться:

- журналом;
- списком инструментов;
- status;
- import report;
- заменой human approval.

Кто пишет:

```text
Orc for subproject execution decisions
```

Кто закрывает gates:

```text
Human
```

Важно:

Выбор tool/route конкретного действия обычно относится к journal. В decisions он попадает только если становится долгоживущим правилом подпроекта.

## Как набор поддерживает `Planner -> Orc`

Шаблоны держат роли раздельно:

```text
Planner:
- создаёт/обновляет plan_full;
- фиксирует Planner-level decisions;
- не ведёт journal как исполнитель.

Orc:
- строит navigation;
- ведёт journal;
- держит status свежим;
- готовит `battle_plan` как сжатый исполнительный конспект оставшихся шагов из принятого `plan_full`;
- фиксирует execution/subproject decisions;
- не переписывает стратегию без разрешения.

Human:
- принимает gates;
- утверждает спорные routes;
- принимает или отклоняет docs slices;
- даёт permission на крупные rewrite.
```

Это защищает процесс от типичных ошибок:

- Planner начинает исполнять вместо Orc;
- Orc переписывает стратегию вместо выполнения;
- agent recommendation выдаётся за human approval;
- journal превращается в decisions;
- status превращается в историю;
- navigation превращается в README;
- `battle_plan` превращается во второй full plan или, наоборот, теряет связь с remaining steps из `plan_full`.

## Human gates

Human gates должны быть явными.

Плохой вариант:

```text
The agent considers this accepted.
```

Хороший вариант:

```text
Human verdict: pending
```

или:

```text
Human verdict: accepted, exact wording: "Stage 4 local docs accepted"
```

Если точной формулировки нет, лучше написать `pending` или `recorded`, но не `accepted`.

## Route decisions

Если route спорный:

```text
Orc recommends.
Human approves.
```

Пример:

```text
Orc recommends V3 external artifact route for this docs-only slice.
Human approval: pending.
```

Нельзя писать:

```text
Route approved
```

если человек не утвердил route явно.

## Как не смешивать файлы

### `plan_full != battle_plan`

`plan_full` объясняет всю стратегию и lifecycle.

`battle_plan` даёт Орку сжатый исполнительный конспект оставшихся шагов из принятого `plan_full`: что сделать, где сделать, как проверить и где остановиться.

Если battle plan начинает спорить с `plan_full`, пропускает оставшиеся шаги без причины или придумывает новую стратегию, нужно остановиться.

### `journal != status`

`journal` — история фактов.

`status` — текущий ближайший snapshot.

Status можно часто перезаписывать. Journal должен сохранять историю.

### `journal != decisions`

`journal` говорит: что произошло.

`decisions` говорит: какое важное решение теперь действует.

Если решение временно записали в journal, потом вынеси его в decisions.

### `navigation != readme`

`navigation` — карта документов и routes.

`readme` — простое объяснение для человека.

Navigation может быть таблицей. Readme должен быть входной дверью.

### `planner-owned plan_decisions != Orc-owned decisions`

`plan_decisions` объясняет стратегические решения Planner.

`decisions` объясняет важные execution/subproject decisions Орка.

Нельзя сливать их без явного решения.

### `human approval != agent recommendation`

Агент может предложить.

Человек утверждает.

Если approval нет, писать:

```text
pending
```

## Минимальный набор для маленького подпроекта

Для совсем маленького docs-only подпроекта можно начать с:

1. `{slug}_plan_full.md`
2. `{slug}_battle_plan.md`
3. `{slug}_status.md`
4. `{slug}_journal.md`
5. `{slug}_readme.md`

Но если появляются важные решения, нужен `{slug}_decisions.md`.

Если появляется много документов, нужен `{slug}_navigation.md`.

Если план большой, нужен `{slug}_plan_index.md`.

Любое сокращение должно быть записано как waiver:

```text
Waiver: <какой файл временно не создаём>
Reason: <почему безопасно>
Human gate: <pending / accepted>
```

## Практический пример начала нового подпроекта

Допустим, есть новый подпроект:

```text
slug: example_subproject
```

Создать:

```text
.ai/subprojects/example_subproject/example_subproject_plan_full.md
.ai/subprojects/example_subproject/example_subproject_plan_index.md
.ai/subprojects/example_subproject/example_subproject_navigation.md
.ai/subprojects/example_subproject/example_subproject_journal.md
.ai/subprojects/example_subproject/example_subproject_battle_plan.md
.ai/subprojects/example_subproject/example_subproject_readme.md
.ai/subprojects/example_subproject/example_subproject_status.md
.ai/subprojects/example_subproject/example_subproject_decisions.md
```

Порядок чтения для человека:

```text
readme -> status -> navigation -> decisions if needed
```

Порядок чтения для Orc:

```text
navigation -> status -> plan_index -> plan_full -> battle_plan -> decisions -> journal
```

## Проверка качества шаблонного подпроекта

Перед human review проверить:

- все user-facing explanations на русском;
- file names and IDs остались technical English;
- `plan_full` не превратился в journal;
- `battle_plan` не переписывает стратегию и не теряет связь с оставшимися шагами из `plan_full`;
- `status` короткий и свежий;
- `journal` factual, без fake backfill;
- `decisions` хранит важные решения, а не список tool choices;
- `navigation` показывает existing docs and routes;
- human gates не закрыты без human verdict;
- legacy route не возвращён как active route без approval.

## Как обновлять набор со временем

Когда процесс меняется, обновлять нужно не все файлы подряд, а только нужный слой:

- изменился current state -> `status`;
- выполнен шаг -> `journal`;
- принято важное решение -> `decisions`;
- появился/исчез документ -> `navigation`;
- человеку стало непонятно, с чего начать -> `readme`;
- изменилась стратегия -> `plan_full` with Planner/human gate;
- изменился порядок выполнения оставшихся шагов из `plan_full` -> `battle_plan` with gate if needed.

## Stop rules

Остановиться и не продолжать автоматически, если:

- нужен human approval;
- route спорный;
- требуется крупный rewrite existing docs;
- обнаружен forbidden path;
- next stage ещё не открыт;
- agent не уверен, какой layer нужно обновлять;
- пользователь прямо просит сначала объяснить суть.

## Короткая памятка

```text
Readme — объяснить человеку.
Status — ближайшее состояние.
Navigation — карта документов.
Journal — что произошло.
Decisions — что решено.
Plan full — большая стратегия.
Plan index — быстрые anchors для агента.
Battle plan — короткие шаги выполнения.
Human gate — только человек закрывает gate.
```
