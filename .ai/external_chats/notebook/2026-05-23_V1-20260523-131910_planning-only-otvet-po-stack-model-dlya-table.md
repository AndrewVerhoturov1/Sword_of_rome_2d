# Notebook Entry

- External Question ID: `V1-20260523-131910`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-131910_planning-only-otvet-po-stack-model-dlya-table.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-055021_domain-data-contract-proposal-for-the-2d-counter.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-055021-2_domain-model-razdelyaet-immutable-definitions-mapdefinition-piecedefinition-scenariodefinition.md`

## Candidate Navigation Entry

Topic: Planning-only ответ по stack model для `Table Sandbox 0.1`
Summary: Рекомендация: safe default now — выводить stack из общего `locationId` у `PieceInstance`, не вводить отдельную сущность `Stack` и не добавлять обязательные `stackId/stackPosition` в первый save format; это сохраняет простой first slice `move_piece_requested -> piece_moved -> GameState -> log -> render` и оставляет путь к advanced stack model later.

## Raw Response

## External Question ID

V1-20260523-131910

## Context Readback

* `external_chat_rules.md` — fully read. ([GitHub][1])
* `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — fully read. ([GitHub][4])
* `domain_schemas_contract.md` — fully read. ([GitHub][5])
* `rules_hooks_interface.md` — fully read. ([GitHub][6])
* `action_event_contract.md` — fully read. ([GitHub][7])
* `first_milestone_runtime_skeleton.md` — fully read. ([GitHub][8])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][9])
* `first_vertical_slice_spec.md` — fully read. ([GitHub][10])
* `minimal_canonical_file_schemas.md` — fully read. ([GitHub][11])
* Project `V1_navigation.md` — fully read. ([GitHub][12])
* V1-navigation-discovered `V1-20260523-124734` notebook entry — fully read. ([GitHub][13])
* V1-navigation-discovered `V1-20260523-062449` notebook entry — partially read. ([GitHub][14])
* V1-navigation-discovered `V1-20260523-055021` notebook entry — partially read. ([GitHub][15])
* V1-navigation-discovered `V1-20260523-055021-2` notebook entry — partially read. ([GitHub][16])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond the required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` contract требует честный `Context Readback`, запрещает писать `fully read` для неоткрытых ссылок и требует разделять выводы из central docs, project-specific context и not verified. Для этого вопроса central docs подтверждают именно workflow-границу ответа, а не саму stack model. ([GitHub][1])

Central `repo_navigation.md` подтверждает, что central navigation — это closed set allowed navigation targets для `ai-workflow-core`; он не даёт права делать claims о consumer repo без явно переданных project-specific links/excerpts. ([GitHub][2])

### Confirmed from provided excerpts

Project-specific документы уже фиксируют важную базу: проект — это универсальная browser-based 2D authoring/runtime platform, а Sword of Rome-like модуль — test module, который не должен превращать lower layers в hardcoded одну игру. Принята 4-layer architecture, где Layer 3 содержит universal runtime/play sandbox, а Layer 4 содержит module content и module rules/hooks. ([GitHub][3])

Также уже принят canonical split: `definitions`, `runtime state`, `module rules`; `PieceDefinition` и `PieceInstance` разделены; `MapDefinition`, `ScenarioState` и `SaveGameState` разделены; `Action` и `Event` разделены. Stack model при этом прямо помечена как open question, то есть она ещё не была зафиксирована как принятое решение. ([GitHub][5])

Для `Table Sandbox 0.1` уже зафиксирован порядок: canonical files → `GameState` bootstrap → Action/Event backbone → permissive RulesHooks → первый thin vertical slice. Первый slice — перемещение одной фишки между двумя spaces через полный pipeline `move_piece_requested -> piece_moved -> GameState -> log -> render`. ([GitHub][8])

**Рекомендация:** для `Table Sandbox 0.1` лучший safe default — **не вводить отдельную сущность `Stack` и не добавлять `stackId` / `stackPosition` в `PieceInstance` как обязательную модель**. Стек на раннем milestone лучше **выводить из общего `locationId`**: все `PieceInstance`, у которых одинаковый `locationId`, считаются находящимися в одной stack group. Это самый простой вариант, он лучше всего поддерживает первый thin vertical slice и не перегружает `savegame.json` ранней сложностью. Такой подход соответствует уже принятому правилу, что `PieceInstance.locationId` — mutable runtime field, а state changes должны идти через committed events. ([GitHub][5])

#### Сравнение трёх вариантов

| Вариант                                       | Оценка для `Table Sandbox 0.1`                           | Почему                                                                                                                                         |
| --------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Стек выводится из общего `locationId`         | **Лучший safe default now**                              | Минимум новых полей, простой save/load, хорошо ложится на `move_piece_requested -> piece_moved`, не заставляет заранее решать stack ordering   |
| Отдельная сущность `Stack`                    | Слишком рано                                             | Добавляет новый lifecycle: создать stack, удалить stack, переместить stack, split/merge stack; это рано для первого vertical slice             |
| `stackId` + `stackPosition` в `PieceInstance` | Компромисс на будущее, но рано как обязательный контракт | Полезно later для ordered stacks, hidden/revealed stacks, trays, partial movement, но сейчас создаёт преждевременную сложность и риск миграций |

#### Почему derived-from-location лучше именно сейчас

Для первого milestone важно доказать не полноценную stack UX, а runtime backbone. Документы уже говорят, что sophisticated/advanced stack model отложена после `0.1`, а первый slice должен быть простым перемещением одной фишки через canonical pipeline. ([GitHub][9])

Derived stack даёт простое правило:

```text
stack at location X = all pieces where piece.locationId == X
```

То есть stack пока не отдельная canonical entity, а **derived view / derived grouping** поверх `GameState`.

#### Как это влияет на `PieceInstance`

Для `Table Sandbox 0.1` `PieceInstance` должен оставаться минимальным:

```text
pieceId
pieceDefId
locationId
ownerId
status
```

Можно добавить later optional поля, но не делать их обязательными сейчас:

```text
displayOrder
faceUp
rotation
selected
```

Safe default now:

```text
У фишки есть locationId.
Если несколько фишек имеют одинаковый locationId, UI/runtime может показывать их как стек.
```

Не добавлять сейчас:

```text
stackId
stackPosition
stackMembership
stackOwner
```

Это сохраняет простую связь `PieceInstance -> locationId`, которая уже есть в schema planning: piece location должен ссылаться на existing `spaceId` или `zoneId`. ([GitHub][11])

#### Как это влияет на `move_piece_requested`

Для первого slice action payload должен оставаться простым:

```text
actionId
type: move_piece_requested
actorId
payload:
  pieceId
  fromLocationId
  toLocationId
```

Safe default now: action двигает **одну конкретную фишку**, а не стек. Если в `fromLocationId` было несколько фишек, выбранная фишка просто уходит из derived group; если в `toLocationId` уже есть фишки, она автоматически оказывается в derived stack по общему `locationId`.

Later extension:

```text
move_stack_requested
split_stack_requested
merge_stack_requested
move_pieces_requested
```

Но эти action types уже стоит оставить после `0.1`, потому что `action_event_contract.md` прямо помечает `split_stack_requested` и `merge_stack_requested` как possible later manual actions, а не first-set required actions. ([GitHub][7])

#### Как это влияет на `piece_moved`

Для первого slice event payload тоже должен быть простым:

```text
eventId
seq
type: piece_moved
causedByActionId
payload:
  pieceId
  fromLocationId
  toLocationId
```

Reducer делает только одно canonical изменение:

```text
piecesById[pieceId].locationId = toLocationId
```

Никаких `stackId` он не пересчитывает и не сохраняет. Stack display после этого пересчитывается как derived grouping из `piecesById`.

Это хорошо сохраняет главный invariant: только committed events меняют `GameState`, а renderer только перерисовывает derived view. ([GitHub][7])

#### Как это влияет на `GameState`

В `GameState` для `0.1` не нужен отдельный `stacksById`.

Достаточно:

```text
gameState:
  piecesById:
    piece-1:
      pieceId
      pieceDefId
      locationId
      ownerId
      status
```

Derived stack можно получить так:

```text
group piecesById by locationId
```

Если очень нужно для UI, можно иметь transient derived selector/view:

```text
derivedStacksByLocation
```

Но это не canonical state и не часть save format. Это вычисляемое представление.

#### Как это влияет на `savegame.json`

`savegame.json` должен хранить `GameState`, event log и mutable piece/control/variable state, но не должен заново определять canonical definitions. В этой модели save хранит только `piecesById[*].locationId`; отдельный `stacks[]` в save не нужен. ([GitHub][5])

Минимально:

```text
savegame.json:
  gameState:
    piecesById:
      piece-1:
        pieceId: piece-1
        pieceDefId: roman-cu
        locationId: space-rome
        ownerId: faction-rome
        status: normal
  eventLog:
    - type: piece_moved
      payload:
        pieceId: piece-1
        fromLocationId: space-capua
        toLocationId: space-rome
```

Не хранить сейчас:

```text
stacks:
  stack-1:
    locationId
    pieceIds[]
```

И не хранить сейчас:

```text
piece.stackId
piece.stackPosition
```

Причина: иначе save format начнёт фиксировать модель, которую проект ещё не решил окончательно. Это прямо важно, потому что stack model в доменном контракте пока open question. ([GitHub][5])

#### Как это влияет на первый thin vertical slice

Первый slice остаётся очень чистым:

```text
1. В scenario есть две или больше фишек.
2. Каждая фишка имеет locationId.
3. Runtime группирует фишки по locationId для отображения.
4. Пользователь перетаскивает одну фишку из space A в space B.
5. Runtime создаёт move_piece_requested.
6. RulesHooks permissive validate/resolve.
7. Runtime commits piece_moved.
8. Reducer меняет только locationId этой фишки.
9. Event log получает событие.
10. Render заново показывает derived stack по новому locationId.
```

Это не ломает путь `Action -> validation -> resolveAction -> Event -> GameState -> log -> render`, который уже зафиксирован как смысл первого vertical slice. ([GitHub][10])

#### Safe default for now

Safe default for `Table Sandbox 0.1`:

```text
Stack = derived group of PieceInstance by locationId.
```

Минимальные правила:

* если одна фишка в location — это single piece;
* если несколько фишек в location — это derived stack;
* stack не имеет собственного id;
* stack не сохраняется в `savegame.json`;
* порядок внутри stack в 0.1 не является rules-critical;
* move action двигает одну выбранную фишку;
* stack UI может показывать count или небольшое смещение, но это view concern, не canonical data.

#### Later extension

Later можно добавить один из двух путей:

**Путь A — мягкое расширение без first-class Stack:**

```text
PieceInstance.displayOrder
PieceInstance.stackPosition
```

Это даст controlled ordering внутри location, но всё ещё без отдельной `Stack` entity.

**Путь B — first-class Stack entity:**

```text
Stack:
  stackId
  locationId
  pieceIds[]
  ownerId?
  visibility?
  stackType?
```

Это имеет смысл позже, если появятся:

* move whole stack;
* split/merge stack;
* hidden stack;
* stack ownership;
* trays/reserves;
* card-like piles;
* strict stacking limits;
* server-authoritative hidden info.

Для `0.1` это не нужно.

#### Риски проигравших вариантов

**Риск отдельной сущности `Stack`:**

* появится новый lifecycle, который надо валидировать;
* нужно решать, что происходит с empty stack;
* нужно синхронизировать `Stack.pieceIds[]` и `PieceInstance.locationId`;
* легко получить два источника истины;
* savegame начнёт хранить сложную структуру раньше, чем она реально нужна;
* первый vertical slice станет не "move one piece", а "обнови piece, stack A, stack B, ordering and log".

Главный риск: отдельный `Stack` может нарушить простоту `PieceInstance.locationId` как текущей позиции фишки.

**Риск `stackId` + `stackPosition` у `PieceInstance`:**

* выглядит проще, чем отдельная `Stack`, но всё равно создаёт второй слой истины;
* нужно решать, может ли `stackId` существовать без `locationId`;
* нужно валидировать, что все pieces в одном `stackId` имеют один location;
* move одной фишки требует решать, создаётся ли новый `stackId`;
* stack ordering станет обязательной проблемой уже в 0.1;
* save format может зацементировать раннее решение.

Главный риск: это преждевременно превращает stack model в обязательный canonical contract.

#### Рекомендуемый компромисс

Лучший компромисс:

```text
0.1:
  canonical = locationId only
  stack = derived by locationId
  optional UI ordering = transient only

later:
  если нужно — добавить displayOrder или stackPosition
  ещё позже — first-class Stack только при реальной необходимости
```

То есть проект не закрывает дверь для advanced stacks, но не платит за них в первом milestone.

#### Что должно остаться явно open

Открытыми нужно оставить:

* нужен ли stack ordering как canonical state;
* будут ли hidden stacks;
* будет ли move whole stack;
* нужны ли split/merge stack actions;
* будут ли stacking limits в assisted/strict rules;
* будет ли first-class `Stack` entity после `0.1`;
* как future stack model мигрирует старые saves, где stack выводился только из `locationId`.

Эти вопросы не надо маскировать как уже принятые решения. Сейчас принимается только safe default для раннего milestone.

### Not available / not verified

* Локальный репозиторий, product-code skeleton, runtime, tests, build и фактические JSON-файлы не проверялись.
* Не проверено, есть ли уже локальная реализация `PiecesStacksModule`.
* Точный UI/UX стеков не рассматривался.
* Точный TypeScript/Zod contract не фиксировался.
* Точный future migration path для перехода от derived stacks к `stackId` или first-class `Stack` пока не зафиксирован.
* Этот ответ — planning-only recommendation, а не accepted local decision.

## Candidate Navigation Entry

V1-20260523-131910: Planning-only ответ по stack model для `Table Sandbox 0.1`. Рекомендация: safe default now — выводить stack из общего `locationId` у `PieceInstance`, не вводить отдельную сущность `Stack` и не добавлять обязательные `stackId/stackPosition` в первый save format; это сохраняет простой first slice `move_piece_requested -> piece_moved -> GameState -> log -> render` и оставляет путь к advanced stack model later.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-062449_ruleshooksinterface-second-opinion-for-the-universal-2d-counter.md "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-055021_domain-data-contract-proposal-for-the-2d-counter.md "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-055021-2_domain-model-razdelyaet-immutable-definitions-mapdefinition-piecedefinition-scenariodefinition.md "raw.githubusercontent.com"
