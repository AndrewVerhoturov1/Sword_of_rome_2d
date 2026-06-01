# {Subproject Title} Decisions

Слаг: `{subproject_slug}`  
Владелец: `Orc`  
Статус: `draft / active / pending review`  
Дата обновления: `YYYY-MM-DD`  
Decision layer: `subproject-level accepted decisions`

## Назначение

Этот файл хранит важные решения подпроекта.

Он нужен, чтобы будущий человек, Orc или Planner могли быстро понять:

- какие решения уже приняты;
- какие варианты отклонены;
- какие approvals были даны человеком;
- какие правила теперь обязательны для работы;
- какие решения принадлежат Planner, а какие — Orc/execution layer.

## Что сюда записывать

Записывать сюда только решения, которые важны дольше одной сессии:

- принятие или закрытие stage/gate;
- утверждение языка документации;
- утверждение active route;
- запрет на определённые действия;
- approved scope boundary;
- reusable process rule;
- отказ от legacy route;
- waiver, который влияет на дальнейшую работу;
- human approval или human correction request, если он меняет правила.

## Что сюда не записывать

Не записывать сюда обычный лог действий:

- какой tool был выбран в одной сессии;
- какие команды запускались;
- какие файлы были изменены в конкретном step;
- checksum output;
- import report;
- длинную историю чата;
- временную заметку для ближайшего продолжения.

Это относится к:

```text
{subproject_slug}_journal.md
{subproject_slug}_status.md
```

Главное различие:

```text
journal = что произошло;
decisions = какие важные решения теперь действуют;
status = самый свежий короткий контекст.
```

## Разделение decision layers

### Planner decisions

Planner-owned decisions живут в:

```text
{subproject_slug}_plan_decisions.md
```

Если такого файла нет, Planner decisions могут быть частью `{subproject_slug}_plan_full.md`.

Planner decisions отвечают за стратегию, lifecycle, причины архитектуры плана.

### Orc / subproject decisions

Orc-owned subproject decisions живут здесь:

```text
{subproject_slug}_decisions.md
```

Они отвечают за process/execution rules, которые действуют при исполнении принятого плана.

### Human approvals

Human approval не создаётся агентом.

Агент может написать:

```text
recommended
```

Но gate закрывается только после явного human verdict.

## Accepted subproject decisions

### D-YYYYMMDD-001 — <название решения>

- Status: `accepted / active / pending / superseded`
- Source: `<journal entry / human message / plan section / review>`
- Decision: `<что именно решено>`
- Reason: `<почему это важно>`
- Consequence: `<что теперь должен делать Orc/Planner/human>`
- Boundary: `<чего это решение не разрешает>`
- Human approval: `<accepted / pending / not required / recorded>`

## Superseded or corrected decisions

### S-YYYYMMDD-001 — <старое решение или ошибка draft>

- Status: `superseded / corrected / rejected`
- Old rule: `<что было раньше>`
- New rule: `<что действует теперь>`
- Reason: `<почему исправлено>`
- Evidence: `<human correction / review / journal entry>`

## Rejected options

### R-YYYYMMDD-001 — <отклонённый вариант>

- Status: `rejected`
- Option: `<что предлагалось>`
- Reason: `<почему нельзя или не нужно>`
- Safe alternative: `<что делать вместо этого>`

## Waivers

### W-YYYYMMDD-001 — <waiver>

- Status: `active / expired`
- Waiver: `<что пропускается или разрешается особым образом>`
- Reason: `<почему это безопасно>`
- Remaining check: `<какая проверка всё равно нужна>`
- Human approval: `<accepted / pending / recorded>`

## Human approvals

### HA-YYYYMMDD-001 — <approval>

- Status: `accepted / pending / rejected`
- Human verdict: `<exact wording if available>`
- Scope: `<что именно принято>`
- Boundary: `<что не принято>`
- Evidence: `<journal entry / user message / review report>`

## Relation to journal

Если важное решение сначала было записано в journal, потому что decisions file ещё не существовал, нужно:

1. оставить journal entry как factual history;
2. вынести само решение сюда;
3. в journal добавить короткую пометку:

```text
Decision mirror: reflected in {subproject_slug}_decisions.md
```

Так journal остаётся историей действий, а decisions становится памятью решений.

## Maintenance rule

- Не превращать этот файл в journal.
- Не записывать сюда каждую техническую операцию.
- Не подменять human approval агентским мнением.
- Не смешивать Planner decisions и Orc execution decisions.
- При споре route: Orc рекомендует, человек утверждает.
