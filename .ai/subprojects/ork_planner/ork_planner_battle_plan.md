# Боевой план Ork Planner

Слаг: `ork_planner`  
Владелец: `Orc`  
Родительский план: [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md)  
Статус: `draft`  
Этап жизненного цикла: `Stage 3`

## Purpose

Этот файл не описывает только следующий execution chunk.

Для `ork_planner` боевой план означает:

- сжатый operational-конспект уже принятого [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md);
- более короткую и более конкретную карту оставшегося пути;
- один документ, по которому человек и Orc видят, что именно осталось сделать после уже принятого `Stage 2`;
- понятные gates, scope, allowed writes и stop rules для `Stage 4`, `Stage 5` и `Stage 6`.

Этот файл не заменяет `plan_full` как source of truth. Он упрощает его до рабочего конспекта без лишней воды и без повторного разворачивания уже пройденных этапов как активной работы.

## Preconditions

Перед использованием этого battle plan должны быть верны все пункты:

- `Stage 2` принят человеком;
- существуют:
  - [ork_planner_plan_index.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_index.md)
  - [ork_planner_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_navigation.md)
  - [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
- [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md) остаётся canonical source of truth;
- active route остаётся `Planner -> Orc`;
- этот battle plan должен быть отдельно принят человеком до старта `Stage 4`.

## Scope

Этот battle plan покрывает весь оставшийся путь текущего пилота после уже закрытых `Stage 1` и `Stage 2`:

```text
Stage 4 - Remaining local docs system for ork_planner
Stage 5 - Fresh tiny docs-only pilot subproject from scratch
Stage 6 - Repo-level alignment wave
```

Это значит:

- `Stage 4` описывается как локальная docs-wave для `ork_planner` плюс reusable template-layer в `.ai/subprojects/templates/`;
- `Stage 5` описывается как обязательное доказательство на новом маленьком docs-only подпроекте;
- `Stage 6` описывается как отложенная repo-level alignment wave с фиксированным scope;
- уже пройденные `Stage 1` и `Stage 2` не повторяются здесь как активные задачи.

## Non-goals

Этот battle plan не должен:

- заново пересказывать весь `plan_full` раздел за разделом;
- притворяться, что `Stage 4`, `Stage 5` или `Stage 6` уже выполняются;
- автоматически разрешать старт следующего этапа без явного human gate;
- возвращать `ork_planner_plan_active_1.md`;
- возвращать `ork_planner_plan_navigation.md`;
- подменять собой Planner-owned канон;
- переписывать lifecycle strategy без отдельного возврата в Planner.

## Allowed writes

Разрешённые записи зависят от этапа.

### `Stage 4`

```text
.ai/subprojects/ork_planner/ork_planner_readme.md
.ai/subprojects/ork_planner/ork_planner_status.md
.ai/subprojects/ork_planner/ork_planner_decisions.md
.ai/subprojects/ork_planner/ork_planner_navigation.md
.ai/subprojects/ork_planner/ork_planner_journal.md
.ai/subprojects/templates/subproject_plan_full_template.md
.ai/subprojects/templates/subproject_plan_index_template.md
.ai/subprojects/templates/subproject_navigation_template.md
.ai/subprojects/templates/subproject_journal_template.md
.ai/subprojects/templates/subproject_battle_plan_template.md
.ai/subprojects/templates/subproject_readme_template.md
.ai/subprojects/templates/subproject_status_template.md
.ai/subprojects/templates/subproject_decisions_template.md
.ai/subprojects/templates/subproject_templates_guide.md
```

Режим:

- `readme`, `status`, `decisions` создаются;
- `navigation` и `journal` обновляются точечно;
- reusable templates и guide создаются в `.ai/subprojects/templates/`;
- правки должны оставаться внутри `.ai/subprojects/ork_planner/` и `.ai/subprojects/templates/`.

### `Stage 5`

`Stage 5` не имеет заранее названного slug в этом battle plan.

Разрешённый принцип такой:

- создать новый маленький docs-only подпроект с нуля;
- писать только в его локальный подпроектный слой;
- не трогать repo-level files;
- не превращать `Stage 5` в скрытое продолжение `ork_planner`.

Точный список путей для `Stage 5` должен быть отдельно назван Orc и принят человеком в момент старта этого этапа.

### `Stage 6`

```text
.ai/rules/codex_role_planner.md
.ai/rules/codex_role_orc.md
.ai/rules/codex_orchestrator.md
.ai/repo_navigation.md
AGENTS.md
```

`Stage 6` допускается только после принятого `Stage 5`.

## Forbidden writes

Вне зависимости от этапа запрещено:

```text
.ai/subprojects/ork_planner/ork_planner_plan_active_1.md
.ai/subprojects/ork_planner/ork_planner_plan_navigation.md
.ai/subprojects/ork_planner/reviews/
.ai/v3/
ideas/
scripts/
src/
```

Дополнительно:

- в `Stage 4` нельзя трогать repo-level files вне `.ai/subprojects/ork_planner/` и `.ai/subprojects/templates/`;
- в `Stage 5` нельзя делать repo-level alignment;
- в `Stage 6` нельзя расширять fixed scope без отдельного human decision;
- нельзя возвращать legacy route `Boss / B1 / Junior Orchestrator`.

## Source basis

При конфликте источников применять такой порядок:

1. [ork_planner_plan_full.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_full.md)
2. [ork_planner_plan_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md)
3. [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
4. [AGENTS.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/AGENTS.md)
5. [codex_role_orc.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/codex_role_orc.md), [codex_role_planner.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/codex_role_planner.md), [codex_orchestrator.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/codex_orchestrator.md)

Если конфликт не снимается, Orc должен остановиться и запросить решение человека.

## Step sequence

Оставшийся путь пилота выглядит так:

1. Получить human approval этого battle plan.
2. Выполнить `Stage 4`: собрать remaining local docs system для `ork_planner` и reusable template-layer для будущих подпроектов.
3. Получить human acceptance по `Stage 4`.
4. Выполнить `Stage 5`: провести fresh tiny docs-only pilot на новом чистом подпроекте.
5. Получить human acceptance по `Stage 5`.
6. Выполнить `Stage 6`: сделать repo-level alignment wave в фиксированном scope.
7. Получить human acceptance по `Stage 6`.

Внутренний смысл этапов:

### `Stage 4`

- создать [ork_planner_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_readme.md)
- создать [ork_planner_status.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_status.md)
- создать [ork_planner_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_decisions.md)
- создать reusable template-layer в `.ai/subprojects/templates/` для полного doc-set `Planner -> Orc`
- создать [subproject_templates_guide.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/templates/subproject_templates_guide.md) с объяснением, как пользоваться шаблонами и за что отвечает каждый файл
- обновить [ork_planner_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_navigation.md)
- занести template-layer в navigation как отдельный reusable layer
- обновить [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md)
- при разработке документации учитывать универсальные process rules из [ork_planner_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_journal.md) и [ork_planner_plan_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md)
- не переносить в новые документы всю локальную историю чата; брать только правила, годные для любого подпроекта

### `Stage 5`

- выбрать новый маленький docs-only подпроект;
- не брать скрытое продолжение `ork_planner`;
- пройти чистый `Planner -> Orc` цикл с нуля;
- доказать, что процесс работает не только на мета-подпроекте.

### `Stage 6`

- обновить только fixed repo-level scope;
- опираться на evidence из `Stage 4` и `Stage 5`;
- не делать broad rewrite;
- не менять source code.

## Tool route recommendation or waiver per step

Рекомендации по маршруту:

### `Stage 4`

- основной вариант: `Kilo Handoff Runner`
- роль: `Docs Agent`
- direct Codex execution: только по отдельному human override

Почему:

- docs-only scope;
- локальные file writes и один shared template layer;
- нужен аккуратный report и human check.

### `Stage 5`

- route не фиксировать заранее;
- Orc должен сначала предложить конкретный route после выбора tiny pilot scope;
- при равной пригодности можно рекомендовать `Kilo Handoff Runner` или bounded external critique, но решение утверждает человек.

Почему:

- новый подпроект ещё не назван;
- конкретный scope пока не определён;
- battle plan должен сохранить gate, а не симулировать уже сделанный выбор.

### `Stage 6`

- strongly consider `Kilo` и/или bounded external review;
- финальный route утверждает человек;
- direct Codex execution по умолчанию не считать базовым вариантом.

Почему:

- меняются repo-level workflow files;
- риск ошибки выше, чем на local docs wave;
- нужен более строгий review discipline.

## Evidence and checks

Минимальные проверки по этапам:

### `Stage 4`

- existence check трёх новых local docs;
- existence check полного template-layer в `.ai/subprojects/templates/`;
- проверка, что `navigation` и `journal` обновлены;
- проверка, что `navigation` явно ссылается на template-layer;
- `git status --short`;
- `git diff --stat`;
- визуальная проверка, что документы на русском и понятны человеку.

### `Stage 5`

- existence check нового tiny subproject docs set;
- проверка, что route шёл через `Planner -> Orc`;
- подтверждение, что repo-level files не менялись;
- проверка, что документация позволяет восстановиться после потери контекста.

### `Stage 6`

- `git diff --name-only` должен оставаться в fixed scope;
- каждый изменённый repo-level файл должен иметь точечную причину;
- broad rewrite без отдельного решения недопустим;
- нужен явный `Human Check`.

Каждый итоговый report должен содержать:

- route;
- какие файлы созданы;
- какие файлы обновлены;
- verification;
- `Human Check`;
- `Баги и сложности`;
- explicit stop statement.

## Human gates

Для старта `Stage 4` нужна явная фраза человека:

```text
Боевой план принят. Можно выполнять Stage 4 по нему.
```

Для закрытия `Stage 4` нужна явная фраза человека:

```text
Stage 4 local docs accepted
```

Для старта `Stage 5` нужна явная команда человека после принятия `Stage 4`.

Для закрытия `Stage 5` нужна явная фраза человека о принятии fresh tiny pilot.

Для старта `Stage 6` нужна явная команда человека после принятия `Stage 5`.

Для закрытия `Stage 6` нужна явная фраза человека о принятии repo-level alignment wave.

Без этих gates Orc не должен двигаться дальше.

## Stop rules

Orc обязан остановиться, если:

- нет явного human approval для следующего этапа;
- нужно выйти за allowed writes текущего этапа;
- battle plan начинает расходиться с `plan_full`;
- route спорный и человек его не утвердил;
- попытка большого смыслового переписывания документа делается без явного разрешения человека;
- `Stage 5` пытаются пропустить;
- `Stage 6` пытаются начать до доказанного fresh proof.

Формат остановки:

```text
Остановлено. Нужен human decision: <что именно решить>.
```

## Escalation rules

Вернуть вопрос человеку нужно, если:

- требуется route override;
- нужно назвать точный scope и slug для `Stage 5`;
- нужен выход за fixed repo-level scope `Stage 6`;
- человек хочет смысловую переработку battle plan или другой большой документации;
- внешний draft или Kilo report противоречит локальным source-of-truth файлам.

Вернуть работу в Planner нужно, если:

- меняется сама lifecycle strategy;
- меняется fixed scope `Stage 6`;
- `battle plan` перестаёт быть condensed operational summary и снова становится отдельной конкурирующей стратегией.

## Acceptance criteria

Этот battle plan можно считать принятым, если человек видит, что:

- файл один и это именно [ork_planner_battle_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_battle_plan.md);
- `Stage 2` явно считается уже закрытым;
- battle plan покрывает оставшийся путь `Stage 4-6`, а не только следующий шаг;
- он короче и конкретнее `plan_full`, но не спорит с ним;
- `Stage 4`, `Stage 5` и `Stage 6` имеют понятные gates;
- `Stage 4` явно включает reusable template-layer и guide для будущих подпроектов;
- `plan_active_1` не возвращён;
- journal и planner decisions явно признаны источником только универсальных process rules для дальнейшей документации;
- route recommendation дана, но human approval не подменён;
- после battle plan нет самозапуска следующего этапа.
