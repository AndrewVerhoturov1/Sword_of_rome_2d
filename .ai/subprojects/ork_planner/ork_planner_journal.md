# Журнал Ork Planner

Слаг: `ork_planner`  
Владелец: `Orc`  
Статус: `active`  
Начат: 2026-06-01

## Политика журнала

- Этот файл фиксирует только фактические действия по выполнению.
- Нельзя делать выдуманный backfill.
- Запланированная будущая работа должна жить в `plan_full`, а не здесь.
- Вердикт человека должен оставаться `pending`, пока человек явно его не дал.

## Формат записи

```md
### J-YYYYMMDD-001 - <короткий заголовок>

- Этап жизненного цикла:
- Роль:
- Маршрут выполнения:
- Ссылка на сессию:
- Созданные файлы:
- Изменённые файлы:
- Подтверждение:
- Проверка:
- Вердикт человека:
- Баги и сложности:
- Следующий шаг:
```

## Исторический контекст

Planner-owned история остаётся в [ork_planner_plan_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md).

Этот журнал начинается только с live Orc execution evidence.

## Записи

### J-20260601-001 - Создание nav layer для Stage 2

- Этап жизненного цикла: `Stage 2 - First Orc nav pass`
- Роль: `Orc`
- Маршрут выполнения: direct Codex work (`Codex-only exception` по явному human override; изначально approved route был `Kilo Handoff Runner`)
- Ссылка на сессию: `not available`
- Созданные файлы:
  - [ork_planner_plan_index.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_index.md)
  - [ork_planner_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_navigation.md)
  - [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
- Изменённые файлы: нет
- Подтверждение:
  - `plan_index` создан как agent-oriented retrieval map
  - `navigation` создан как subproject-wide map
  - `journal` создан и инициализирован первой фактической записью
  - выполнен anchor audit для `plan_full`; правки для Stage 2 не потребовались
- Проверка:
  - локальная проверка существования файлов
  - просмотр `git diff --stat` / `git diff --name-only` в пределах scope `Stage 2`
- Вердикт человека: `pending`
- Баги и сложности:
  - содержательных проблем в `plan_full` не найдено
  - маршрут сменился с planned Kilo path на direct Codex work только потому, что человек явно попросил self-execution
- Следующий шаг:
  - вернуть `Stage 2 report`
  - дождаться принятия человеком или запроса на правки
  - не начинать `Stage 3` до human acceptance

### J-20260601-002 - Принятие Stage 2 и process-retrospective note

- Этап жизненного цикла: `Stage 2 - First Orc nav pass`
- Роль: `Orc`
- Маршрут выполнения: direct Codex work для обновления журнала и подготовки checkpoint
- Ссылка на сессию: `not available`
- Созданные файлы: нет
- Изменённые файлы:
  - [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
- Подтверждение:
  - человек сообщил, что во время `grill-me` Orc задавал слишком много низкоценных вопросов, хотя план уже был подробно расписан и утверждён
  - человек сообщил, что единственный действительно полезный вопрос на этом gate был про то, как именно выполнять задачу
  - человек попросил оставить эту заметку в журнале, чтобы потом можно было отдельно подумать, почему система сработала именно так
  - человек попросил отдельно зафиксировать, что Codex обошёл более раннее прямое указание выполнять задачу через Kilo route
  - человек подтвердил, что сами файлы `Stage 2` хорошие и приняты
- Проверка:
  - human acceptance и retrospective note записаны по текущему чату
  - за пределами журнала в этом checkpoint-preparation step содержимое не менялось
- Вердикт человека: `Stage 2 report accepted by human`
- Баги и сложности:
  - на `pre-Orc grill-me gate` Orc задал слишком много low-value вопросов при уже утверждённом плане; по сути полезным был только вопрос про execution route
  - ранее Codex допустил process error и обошёл прямое указание идти через Kilo route; позже это было исправлено, и direct execution произошёл только после явного human override
- Следующий шаг:
  - сделать workflow checkpoint commit
  - push принятого состояния `Stage 2`
  - держать `Stage 3` закрытым до отдельной команды человека

### J-20260601-003 - Правило языка для документации

- Этап жизненного цикла: `post-Stage-2 accepted state`
- Роль: `Orc`
- Маршрут выполнения: direct Codex work для docs-only update
- Ссылка на сессию: `not available`
- Созданные файлы: нет
- Изменённые файлы:
  - [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
- Подтверждение:
  - человек явно потребовал вести всю документацию на русском языке
  - человек отдельно уточнил, что [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md) он будет читать часто
  - по этой причине журнал переведён на русский в первую очередь
- Проверка:
  - содержимое журнала переведено на русский
  - English identifiers, file names и route names сохранены как technical identifiers
- Вердикт человека: `recorded`
- Баги и сложности:
  - правило языка раньше не было явно зафиксировано внутри самого журнала, из-за чего часть документации была оставлена на английском
- Следующий шаг:
  - дальше вести документацию подпроекта на русском
  - сохранять English только для technical identifiers, file names, IDs и machine-readable значений там, где это нужно

### J-20260601-004 - Универсальные process rules для Stage 4 и следующих подпроектов

- Этап жизненного цикла: `Stage 3 - battle plan clarification`
- Роль: `Orc`
- Маршрут выполнения: direct Codex work для docs-only clarification
- Ссылка на сессию: `not available`
- Созданные файлы: нет
- Изменённые файлы:
  - [ork_planner_battle_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_battle_plan.md)
  - [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
- Подтверждение:
  - человек уточнил, что боевой план должен быть не описанием только следующего шага, а сокращённым и более конкретным конспектом полного плана без уже пройденных этапов
  - человек отдельно указал, что большие смысловые переписывания таких документов нельзя начинать без явного разрешения
  - человек уточнил, что при `Stage 4` нужно учитывать не всю историческую хронику `ork_planner`, а только универсальные process rules из журнала и planner decisions
  - человек подтвердил, что эти универсальные правила надо учитывать и в будущих подпроектах, а не только внутри `ork_planner`
- Проверка:
  - battle plan уточнён под модель `Stage 4-6 condensed route`
  - в журнале зафиксировано, что для `Stage 4` и дальше берутся только универсальные правила, а не вся локальная история
- Вердикт человека: `recorded`
- Баги и сложности:
  - ранее battle plan был ошибочно сужен до `Stage 4 only`
  - ранее Orc начал готовиться к большому смысловому переписыванию battle plan без предварительного явного разрешения человека
- Следующий шаг:
  - при `Stage 4` и в будущих подпроектах учитывать только универсальные правила из журнала и planner decisions
  - не переносить локальные частные эпизоды как обязательный canon для всех подпроектов
  - ждать human verdict по обновлённому battle plan

## Баги и сложности

Текущий статус:

```text
found and logged
```

Зафиксированные process issues:

- `grill-me` задавал низкоценные вопросы при уже утверждённом подробном плане
- на этом gate явно полезным был только вопрос про execution route
- Codex ранее обошёл approved Kilo execution route до последующего явного human override
- правило русского языка для документации не было достаточно жёстко зафиксировано в самом журнале
- battle plan был сначала ошибочно сужен до `Stage 4 only`, хотя человек понимает его как конспект всего оставшегося `plan_full`
- большая смысловая переработка battle plan была преждевременно подготовлена без предварительного явного разрешения человека

## Открытые follow-ups

- Держать `Stage 3` заблокированным до явной команды человека
- Дальше вести документацию подпроекта на русском языке
- Для `Stage 4` и будущих подпроектов брать из журнала и planner decisions только универсальные process rules
