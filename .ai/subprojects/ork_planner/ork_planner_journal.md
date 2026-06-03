# Журнал Ork Planner

Слаг: `ork_planner`  
Владелец: `Orc`  
Статус: `active-draft-pending-local-review`  
Начат: `2026-06-01`

## Политика журнала

- Этот файл фиксирует фактические действия по выполнению.
- Журнал не является главным хранилищем решений подпроекта.
- Если важное решение временно зафиксировано в журнале, оно должно быть также отражено в `ork_planner_decisions.md`.
- Выбор инструмента/route конкретного действия фиксируется здесь, если это нужно для evidence.
- Долгоживущие решения подпроекта фиксируются в `ork_planner_decisions.md`.
- Самый свежий короткий контекст фиксируется в `ork_planner_status.md`.
- Нельзя делать выдуманный backfill.
- Вердикт человека должен оставаться `pending`, пока человек явно его не дал.
- Для будущих подпроектов из этого журнала можно брать только универсальные process rules, а не всю локальную историю `ork_planner`.

## Формат записи

```md
### J-YYYYMMDD-001 — <короткий заголовок>

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

## Записи

### J-20260601-002 — Принятие Stage 2 и process-retrospective note

- Этап жизненного цикла: `Stage 2 — First Orc nav pass`
- Роль: `Orc`
- Маршрут выполнения: direct Codex work для обновления журнала и подготовки checkpoint.
- Ссылка на сессию: `not available`
- Созданные файлы: `none`
- Изменённые файлы:
  - `ork_planner_journal.md`
- Подтверждение:
  - человек сообщил, что во время `grill-me` было слишком много низкоценных вопросов;
  - полезным был вопрос про execution route;
  - человек попросил зафиксировать process issue;
  - человек подтвердил, что сами файлы Stage 2 хорошие и приняты.
- Проверка:
  - human acceptance и retrospective note recorded.
- Вердикт человека: `Stage 2 report accepted by human`
- Баги и сложности:
  - `grill-me` был чрезмерно подробным при уже утверждённом плане;
  - earlier process error: approved Kilo route был обойдён до последующего explicit human override.
- Следующий шаг:
  - сделать workflow checkpoint;
  - держать Stage 3 closed до отдельной команды человека.

Decision mirror:

```text
Ключевые решения из этой записи отражены в ork_planner_decisions.md.
```

### J-20260601-003 — Правило языка для документации

- Этап жизненного цикла: `post-Stage-2 accepted state`
- Роль: `Orc`
- Маршрут выполнения: direct Codex work для docs-only update.
- Ссылка на сессию: `not available`
- Созданные файлы: `none`
- Изменённые файлы:
  - `ork_planner_journal.md`
- Подтверждение:
  - человек явно потребовал вести документацию на русском языке;
  - человек уточнил, что `ork_planner_journal.md` будет читаться часто;
  - English остаётся для technical identifiers, file names, IDs, route names и machine-readable значений.
- Проверка:
  - language rule recorded.
- Вердикт человека: `recorded`
- Баги и сложности:
  - правило языка раньше не было достаточно явно закреплено в самом журнале.
- Следующий шаг:
  - дальше вести user-facing документацию подпроекта на русском.

Decision mirror:

```text
Ключевое решение из этой записи отражено в ork_planner_decisions.md.
```

### J-20260601-004 — Универсальные process rules для Stage 4 и следующих подпроектов

- Этап жизненного цикла: `Stage 3 — battle plan clarification`
- Роль: `Orc`
- Маршрут выполнения: direct Codex work для docs-only clarification.
- Ссылка на сессию: `not available`
- Созданные файлы: `none`
- Изменённые файлы:
  - `ork_planner_battle_plan.md`
  - `ork_planner_journal.md`
- Подтверждение:
  - человек уточнил, что battle plan — это сокращённый operational-конспект оставшегося пути, а не только Stage 4;
  - человек указал, что большие смысловые переписывания existing docs нельзя начинать без explicit permission;
  - для Stage 4 нужно брать из `journal` и `plan_decisions` только универсальные process rules;
  - универсальные правила должны работать и для будущих подпроектов.
- Проверка:
  - clarification recorded.
- Вердикт человека: `recorded`
- Баги и сложности:
  - battle plan сначала был ошибочно сужен до `Stage 4 only`;
  - большая смысловая переработка была преждевременно подготовлена без явного разрешения.
- Следующий шаг:
  - учитывать только универсальные rules;
  - ждать human verdict по обновлённому battle plan.

Decision mirror:

```text
Ключевые решения из этой записи отражены в ork_planner_decisions.md.
```

### J-20260601-005 — External V3 draft package для Stage 4 docs slice

- Этап жизненного цикла: `Stage 4 — local docs system + reusable template layer`
- Роль: `external V3 artifact producer`
- Маршрут выполнения: external V3 ZIP draft; без `/v3 import-entry`; без Kilo Notebook V3; без direct repo write.
- Ссылка на сессию: `V3-20260601-200210-ork-planner-stage4-doc-system`
- Созданные файлы в package:
  - `ork_planner_readme.md`
  - `ork_planner_status.md`
  - `ork_planner_decisions.md`
  - `subproject_plan_full_template.md`
  - `subproject_plan_index_template.md`
  - `subproject_navigation_template.md`
  - `subproject_journal_template.md`
  - `subproject_battle_plan_template.md`
  - `subproject_readme_template.md`
  - `subproject_status_template.md`
  - `subproject_decisions_template.md`
  - `subproject_templates_guide.md`
- Обновлённые файлы в package:
  - `ork_planner_navigation.md`
  - `ork_planner_journal.md`
- Подтверждение:
  - package создан как внешний draft;
  - repo не изменён;
  - Stage 5 и Stage 6 не начаты;
  - human acceptance Stage 4 docs не заявлен.
- Проверка:
  - package structure/checksums prepared in artifact package.
- Вердикт человека: `pending`
- Баги и сложности:
  - first draft смешал `decisions` и `journal`;
  - first draft сделал `status` слишком широким;
  - часть template bodies была на английском;
  - guide оказался недостаточно подробным.
- Следующий шаг:
  - подготовить correction package по human feedback.

### J-20260601-006 — Human-requested correction of Stage 4 draft

- Этап жизненного цикла: `Stage 4 — correction before local acceptance`
- Роль: `external V3 artifact producer`
- Маршрут выполнения: revise ZIP artifact package after explicit human correction request.
- Ссылка на сессию: `V3-20260601-200210-ork-planner-stage4-doc-system revised draft`
- Созданные файлы: `none beyond allowed Stage 4 package files`
- Изменённые файлы in revised package:
  - `ork_planner_decisions.md`
  - `ork_planner_status.md`
  - `ork_planner_journal.md`
  - `subproject_battle_plan_template.md`
  - `subproject_decisions_template.md`
  - `subproject_journal_template.md`
  - `subproject_navigation_template.md`
  - `subproject_templates_guide.md`
  - package metadata/checksums
- Подтверждение:
  - человек прямо указал, что `decisions` должен хранить важные решения подпроекта, а не выбор инструмента Орка;
  - человек указал, что `status` должен быть коротким live snapshot ближайшего контекста;
  - человек потребовал сильнее раскрыть `subproject_templates_guide.md`;
  - человек указал, что четыре template bodies были написаны по-английски и должны быть по-русски;
  - человек попросил пометить, что эти правки requested by human.
- Проверка:
  - revised package preserves 14 allowed project files;
  - forbidden paths remain excluded;
  - Stage 5/6 remain not started;
  - Stage 4 human acceptance remains pending.
- Вердикт человека: `pending`
- Баги и сложности:
  - first draft layer separation was not strict enough;
  - corrected by moving important decisions into `ork_planner_decisions.md` and keeping tool/route evidence in journal.
- Следующий шаг:
  - local review/import revised package;
  - ask human for Stage 4 verdict;
  - do not start Stage 5 before explicit acceptance.

## Открытые follow-ups

- Локально проверить revised package и diff.
- После review получить human verdict по Stage 4 docs.
- Если будут правки, фиксировать их как Stage 4 corrections, не открывая Stage 5.

### J-20260601-006 — Human-requested уточнение semantics для `battle_plan` в template layer

- Этап жизненного цикла: `Stage 4 — local docs system draft correction`
- Роль: `Orc`
- Маршрут выполнения: external V3 artifact revision по прямому запросу человека.
- Ссылка на сессию: `not available`
- Созданные файлы: `none`
- Изменённые файлы:
  - `ork_planner_decisions.md`
  - `ork_planner_navigation.md`
  - `ork_planner_readme.md`
  - `ork_planner_journal.md`
  - `subproject_battle_plan_template.md`
  - `subproject_templates_guide.md`
  - `subproject_navigation_template.md`
  - `subproject_plan_full_template.md`
  - `subproject_readme_template.md`
- Подтверждение:
  - человек уточнил, что `battle_plan` — это сжатый исполнительный конспект оставшихся шагов из полного плана для Орка;
  - `battle_plan` не должен быть отдельным мини-планом, списком идей или только ближайшим slice;
  - шаблоны должны объяснять это так, чтобы новый Орк правильно составил battle plan.
- Проверка:
  - template-layer mentions of `battle_plan` updated;
  - local docs references aligned;
  - Stage 5/6 не объявлены начатыми.
- Вердикт человека: `pending local review`
- Баги и сложности:
  - previous template wording could make a new Orc treat battle plan as too narrow or too generic.
- Следующий шаг:
  - local Codex/human review revised package;
  - не начинать Stage 5 без отдельного explicit approval.

### J-20260602-001 - Human accepted temporary Stage 5 bridge direction

- Этап жизненного цикла: `между Stage 4 accepted и Stage 5 preparation`
- Роль: `Orc`
- Маршрут выполнения: `/v1` grounded second opinion -> human acceptance -> journal capture
- Ссылка на внешний вопрос: `V1-20260602-061552`
- Подтверждение:
  - человек принял идею одного временного bridge-документа для первого `Stage 5` tiny docs-only pilot;
  - bridge не считается repo-level standard и нужен только как временный переходник до `Stage 6`;
  - рекомендуемый путь bridge-документа принят человеком: `.ai/subprojects/ork_planner/ork_planner_stage5_first_pilot_bridge.md`;
  - для первого `Stage 5` pilot принят reduced set из 6 обязательных файлов:
    - `{stage5_slug}_plan_full.md`
    - `{stage5_slug}_battle_plan.md`
    - `{stage5_slug}_readme.md`
    - `{stage5_slug}_status.md`
    - `{stage5_slug}_navigation.md`
    - `{stage5_slug}_journal.md`
  - `plan_index` и `decisions` допустимо waive-нуть для первого tiny pilot, если не появится явная причина их заводить;
  - сам bridge-документ сейчас не пишется; человек отдельно указал, что позже его должен написать `Kilo`;
  - `Stage 5` execution этим решением не начат.
- Проверка:
  - прочитан notebook entry `.ai/external_chats/notebook/2026-06-02_V1-20260602-061552_grounded-second-opinion-po-stage-5-bridge.md`;
  - подтверждено human сообщение: `Принимаю. Пока ничего не делай. Сам файл позже напишет кило, ты только запиши в журнал, запуш все`.
- Вердикт человека: `accepted`
- Баги и сложности:
  - notebook entry содержит сломанные по кодировке русские фрагменты;
  - смысл ответа читается и был отдельно подтверждён человеком;
  - до отдельного запуска `Kilo` bridge-файл не создавать.
- Следующий шаг:
  - при отдельной команде человека подготовить/запустить `Kilo` на написание `ork_planner_stage5_first_pilot_bridge.md`;
  - не начинать `Stage 5` без отдельного human сигнала.

### J-20260602-002 - Process bug: pilot planner слишком рано свёл старт к battle plan

- Этап жизненного цикла: `Stage 5 preparation`
- Роль: `Orc`
- Маршрут выполнения: local retrospective note по human feedback.
- Ссылка на сессию: `not available`
- Созданные файлы: `none`
- Изменённые файлы:
  - `ork_planner_journal.md`
- Подтверждение:
  - человек заметил, что pilot planner интерпретировал первый шаг Орка как немедленное написание `battle_plan`;
  - человек отдельно уточнил, что для нового пилота нужно не автоматически разворачивать полный doc-set и не начинать с `battle_plan` по умолчанию;
  - сначала нужно определить, какая часть документации реально нужна для конкретного пилота.
- Проверка:
  - process note recorded.
- Вердикт человека: `recorded`
- Баги и сложности:
  - planner слишком рано зафиксировал execution shape;
  - `battle_plan` был не туда поставлен по порядку работ;
  - риск: новый подпроект может получить лишние документы до того, как будет понятен минимальный scope.
- Следующий шаг:
  - для нового пилота сначала определить папку подпроекта и минимально нужный docs slice;
  - не считать `battle_plan` автоматическим первым артефактом;
  - создавать не весь doc-set сразу, а только доказанно нужную часть под конкретный pilot scope.

Decision mirror:

```text
Ключевое правило про универсальный стартовый минимум вынесено в ork_planner_decisions.md.
```

### J-20260602-003 - Human fixed universal startup doc minimum for future subprojects

- Этап жизненного цикла: `Stage 5 preparation`
- Роль: `Orc`
- Маршрут выполнения: local rule capture по прямому human instruction.
- Ссылка на сессию: `not available`
- Созданные файлы:
  - `ork_planner_stage5_minimal_docset_prompt.md`
- Изменённые файлы:
  - `ork_planner_journal.md`
  - `ork_planner_decisions.md`
- Подтверждение:
  - человек явно указал, что универсальный стартовый минимум для нового подпроекта должен состоять из:
    - `*_readme.md`
    - `*_decisions.md`
    - `*_plan_index.md`
    - `*_journal.md`
    - `*_navigation.md`
  - человек попросил также сделать короткий prompt для другого чата с этим правилом.
- Проверка:
  - rule recorded;
  - short prompt created.
- Вердикт человека: `recorded`
- Баги и сложности:
  - новое universal rule отличается от более ранней рабочей гипотезы Орка;
  - дальше при старте новых подпроектов нужно опираться на human-fixed minimum, а не на старую гипотезу.
- Следующий шаг:
  - использовать этот минимум как базовое правило для новых подпроектов;
  - при необходимости человек может отдельно расширить его для конкретного pilot scope.
