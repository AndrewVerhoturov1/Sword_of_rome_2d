# Notebook Entry

- External Question ID: `V1-20260525-005823`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-25_V1-20260525-005823_next-step-advice-after-accepted-minimal-runtime-snapshot.md`

## Context Links

- `нет`

## Candidate Navigation Entry

Topic: Next-step advice after accepted minimal runtime snapshot
Summary: Updated recommendation: instead of a single `change_control` slice, the next meaningful step should be `Manual Sandbox Action Pack 1`: create piece, delete piece, change control, selected object panel, human-readable validation messages, and save/load verification for all new runtime state changes.

## Raw Response

## External Question ID

V1-20260525-005823

## Context Readback

Текущий baseline я понимаю так:

* уже есть рабочий `table-sandbox`;
* `GameState` живёт вне Phaser;
* Phaser остаётся только слоем отображения и ввода;
* fixture-данные загружаются в runtime;
* фишка уже двигается через схему `Action → RulesHooks → Event → reducer → GameState → event log → render`;
* move validation уже проверяет карту: есть ли точки и связь между ними;
* minimal save/load snapshot уже принят: `Сохранить` / `Загрузить` сохраняют и восстанавливают `GameState + eventLog` через `localStorage`;
* пользователь визуально подтвердил, что save/load работает;
* сейчас нужен следующий **значимый**, но всё ещё контролируемый product-code шаг. 

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Нужно честно отделять проверенные факты от того, что известно из контекста. Я не должен заявлять, что сам локально запускал проект или видел браузерный результат, если это было подтверждено через отчёт пользователя/локального агента.

### Confirmed from provided excerpts

Из предоставленного контекста подтверждается, что после `0014` уже есть первый законченный runtime loop:

```text id="8s3g9g"
fixture data
→ GameState
→ move_piece_requested
→ RulesHooks validation/resolution
→ piece_moved
→ reducer
→ updated GameState
→ event log
→ render
→ save/load snapshot
```

Также подтверждается, что сейчас не нужен новый roadmap, не нужна миграция старого prototype editor, не нужна большая save-система и не нужен полный rules engine. Нужен следующий практический product-code шаг. 

### Not available / not verified

Я сам не запускал проект локально после `0014`.

Не проверял лично:

```text id="35rv6r"
npm run build
npm run typecheck
browser behavior
localStorage behavior
git diff
текущий main/local sync
```

Поэтому техническую готовность `0014` принимаю из твоего контекста и отчёта.

### Main assessment

После save/load проект уже не стоит дальше двигать "по одной микрофункции". Следующий шаг лучше сделать заметным: не только `change_control`, а первый полноценный набор ручных действий для песочницы.

Оптимальный следующий этап:

```text id="m5pcwn"
Manual Sandbox Action Pack 1
```

По-русски:

```text id="g1xp7m"
Первый набор ручных действий песочницы
```

Это хороший шаг, потому что он превращает текущий прототип из технического теста "одна фишка ходит" в маленький рабочий tabletop sandbox.

### Best next step

Лучший следующий шаг:

```text id="zx9un9"
Manual Sandbox Action Pack 1
```

Состав шага:

```text id="hpbr5r"
1. create_piece_requested → piece_created
2. delete_piece_requested → piece_deleted
3. change_control_requested → control_changed
4. простая панель выбранного объекта
5. понятные сообщения validation для пользователя
6. проверка, что save/load сохраняет новые изменения
```

Это один значимый product-code пакет, но без прыжка в большой редактор или полные правила игры.

### Why this step now

Сейчас уже есть основа:

```text id="w17pl2"
GameState
Action/Event
RulesHooks
event log
renderer redraw
save/load
```

Но пока продукт умеет в основном одно: двигать уже существующую фишку.

Следующий шаг должен добавить несколько базовых ручных операций, чтобы пользователь мог реально менять состояние стола:

```text id="np0kq3"
поставить новую фишку
убрать фишку
поменять контроль точки
увидеть выбранный объект
понять, почему действие запрещено
сохранить и загрузить всё это обратно
```

Это лучше, чем делать только `change_control`, потому что одна смена контроля слишком маленькая и не даст ощущения серьёзного продвижения.

Это лучше, чем продолжать save/load, потому что minimal snapshot уже принят. Сейчас важнее проверить, что save/load держит не только перемещение, но и несколько разных типов изменений.

Это лучше, чем full rules engine, потому что пока нужен ручной sandbox, а не строгая игра по правилам.

Это лучше, чем prototype migration, потому что старый map editor пока лучше держать как reference/donor, а не тянуть его в runtime раньше времени.

### Recommended scope

#### 1. Создание фишки

Добавить действие:

```text id="leofbr"
create_piece_requested → piece_created
```

Минимальный смысл:

```text id="l4prcu"
выбрана точка
выбран тип фишки
выбран владелец
создаётся новая фишка
она появляется на карте
событие попадает в журнал
save/load сохраняет результат
```

На первом этапе не нужен полноценный редактор фишек.

Достаточно:

```text id="7mhfo6"
тип: infantry
владелец: tiny-red / tiny-blue
локация: выбранный space
id: автоматически piece-2, piece-3, piece-4...
```

Важно не смешать:

```text id="8zbvq1"
PieceDefinition — описание типа фишки
PieceInstance — конкретная фишка на столе
```

Создавать нужно именно `PieceInstance`.

---

#### 2. Удаление фишки

Добавить действие:

```text id="mfa1ip"
delete_piece_requested → piece_deleted
```

Минимальный смысл:

```text id="a8pqud"
выбрана фишка
пользователь удаляет её
фишка исчезает из GameState
событие попадает в журнал
после save/load удалённая фишка не возвращается
```

Это нужно для ручной песочницы, потому что пользователь должен уметь исправлять состояние стола.

---

#### 3. Смена контроля точки

Добавить действие:

```text id="yy50ow"
change_control_requested → control_changed
```

Минимальный смысл:

```text id="gydcwj"
выбрана точка
пользователь выбирает контроль
контроль меняется
событие попадает в журнал
save/load сохраняет результат
```

Возможные значения:

```text id="b9w4pz"
tiny-red
tiny-blue
null / none
```

В интерфейсе это можно показывать по-русски:

```text id="8zjqmw"
Красная сторона
Синяя сторона
Нет контроля
```

Но технические ID должны оставаться английскими.

---

#### 4. Простая панель выбранного объекта

Нужна не большая property panel, а маленькая понятная панель.

Если выбрана фишка:

```text id="e6r4gn"
Фишка: piece-1
Тип: infantry
Владелец: tiny-red
Позиция: space-b
```

Если выбрана точка:

```text id="44td4x"
Точка: space-a
Контроль: tiny-red
```

Эта панель важна, потому что без неё пользователь не понимает, что именно сейчас выбрано и какие действия доступны.

---

#### 5. Понятные сообщения validation

Сейчас технические ошибки могут выглядеть как:

```text id="rbswb0"
move_piece_requested_no_connection
```

Для человека нужно показывать простые сообщения:

```text id="9jxqxn"
Нельзя переместить фишку: между этими точками нет связи.
```

Для новых действий тоже нужны понятные сообщения:

```text id="ndmneo"
Нельзя создать фишку: не выбрана точка.
Нельзя удалить фишку: фишка не выбрана.
Нельзя поменять контроль: точка не выбрана.
```

Технические `reasonCode` можно оставить английскими, но видимый текст должен быть русским.

---

#### 6. Save/load должен сохранять весь новый state

После этого пакета save/load должен восстанавливать:

```text id="fd3fnq"
перемещённые фишки
созданные фишки
удалённые фишки
изменённый контроль точек
event log
```

Это важная проверка: snapshot должен работать не только с одним `piece_moved`, а с несколькими типами событий и изменений.

### Candidate alternatives

#### Альтернатива 1: только `change_control`

Слишком маленький шаг. Полезно, но не даёт достаточного ощущения прогресса.

#### Альтернатива 2: только `create_piece`

Полезно, но без удаления и панели выбора будет неудобно. Пользователь сможет поставить фишку, но не сможет нормально управлять состоянием.

#### Альтернатива 3: идти в map editor integration

Пока рано. Это большой скачок. Лучше сначала укрепить ручную runtime-песочницу.

### Risks before next step

#### 1. Создание фишки может расползтись

Самый опасный элемент пакета — `create_piece`.

Он может потянуть за собой:

```text id="t9jafe"
редактор типов фишек
полноценный faction editor
сложную генерацию ID
формы свойств
изображения counters
```

На этом этапе это не нужно.

Ограничение:

```text id="nrgfct"
создаём только infantry
только tiny-red / tiny-blue
только на выбранный space
id генерируется просто: piece-2, piece-3...
```

---

#### 2. Можно смешать scenario setup и runtime state

Новые созданные фишки не должны записываться обратно в scenario fixture как будто это исходная расстановка.

Они должны жить в текущем `GameState` и save snapshot.

---

#### 3. Можно смешать map definition и control state

Контроль точки — это не свойство карты.

Карта описывает topology:

```text id="baypvo"
spaces
connections
zones
```

А контроль — это состояние партии:

```text id="indavz"
controlBySpace
```

Поэтому контроль должен жить в `GameState` / scenario setup / snapshot, а не в `map.json`.

---

#### 4. Event id / seq после load

После save/load и добавления новых event types важно, чтобы новые события не получали повторяющиеся номера.

Нужно проверить:

```text id="5ke5sg"
создал фишку
сохранил
обновил страницу
загрузил
сделал новое действие
новое событие получило корректный следующий seq
```

---

#### 5. UI может стать хаотичным

Не стоит делать большой красивый интерфейс.

Достаточно простой панели и простых кнопок:

```text id="xjz0ws"
Создать фишку
Удалить фишку
Контроль: Красная / Синяя / Нет
```

Главное — не UI-polish, а правильный runtime pipeline.

### Acceptance checks

Шаг можно считать успешным, если работает такой набор:

```text id="iccb8f"
1. Можно выбрать точку.
2. Можно создать на ней новую фишку.
3. Создание проходит через Action/Event.
4. Новая фишка появляется на карте.
5. Создание записывается в event log.

6. Можно выбрать фишку.
7. Можно удалить выбранную фишку.
8. Удаление проходит через Action/Event.
9. Фишка исчезает с карты.
10. Удаление записывается в event log.

11. Можно выбрать точку.
12. Можно поменять её контроль.
13. Смена контроля проходит через Action/Event.
14. Новый контроль виден в UI/debug.
15. Смена контроля записывается в event log.

16. Есть простая панель выбранного объекта.
17. Ошибки validation показываются человеку понятным русским текстом.
18. Save/load восстанавливает созданные фишки.
19. Save/load сохраняет удаление фишек.
20. Save/load восстанавливает контроль точек.
21. Event log восстанавливается.
22. После загрузки новые события не ломают seq/id.
23. Старое движение фишки продолжает работать.
24. Phaser остаётся только renderer/input.
25. GameState остаётся source of truth.
```

### Human Check

Status: required

Причина: этот шаг меняет видимое поведение приложения. Нужно проверить глазами в браузере, что пользователь действительно может создать фишку, удалить фишку, поменять контроль точки, увидеть выбранный объект, сохранить и загрузить результат.

Проверка человеком должна быть простой:

```text id="n8p5y4"
1. Открыть приложение.
2. Выбрать точку.
3. Создать новую фишку.
4. Проверить, что она появилась.
5. Выбрать фишку.
6. Удалить её.
7. Проверить, что она исчезла.
8. Выбрать точку.
9. Поменять контроль.
10. Проверить, что контроль отображается.
11. Сохранить.
12. Обновить страницу.
13. Загрузить.
14. Проверить, что состояние восстановилось правильно.
```

Ожидаемый результат:

```text id="orf7q9"
созданные фишки сохраняются
удалённые фишки не возвращаются
контроль точек сохраняется
event log восстанавливается
старое движение фишек работает
```

### Баги и сложности

Status: expected risk

Пока баг не заявлен, но заранее видны рискованные места:

```text id="ql9dso"
генерация новых pieceId
сохранение новых pieces в snapshot
удаление pieces без поломки selection
controlBySpace как runtime state
event seq/id после загрузки
понятные сообщения validation
```

Если на этом шаге появится повторяемая проблема, её нужно будет записать в bug journal.

## Candidate Navigation Entry

V1-20260525-005823: Next-step advice after accepted minimal runtime snapshot. Updated recommendation: instead of a single `change_control` slice, the next meaningful step should be `Manual Sandbox Action Pack 1`: create piece, delete piece, change control, selected object panel, human-readable validation messages, and save/load verification for all new runtime state changes.
