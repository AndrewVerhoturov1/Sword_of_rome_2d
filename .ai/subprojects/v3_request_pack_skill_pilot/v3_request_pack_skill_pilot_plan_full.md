# План подпроекта `v3_request_pack_skill_pilot`

Статус: baseline draft  
Владелец плана: `Planner`  
Маршрут: `Planner -> Orc`

## Назначение документа

Этот файл фиксирует исходный `plan_full` для первого `Stage 5` pilot после `ork_planner`.

Пилот нужен не ради ещё одного docs-only слоя сам по себе. Он нужен, чтобы спланировать и затем безопасно проверить узкий skill для Codex, который помогает готовить `V3 request pack` для внешнего чата и доводить flow до получения годного внешнего `V3 artifact package`.

Этот документ пока не запускает execution. Он задаёт рамку, scope, gates, stop rules и proof bar.

## Быстрый итог

- Новый подпроект живёт в `.ai/subprojects/v3_request_pack_skill_pilot/`.
- Proposed skill home до отдельного capability-sensitive human gate: `C:\Users\andre\.codex\skills\v3-request-pack-prep\`.
- Сам подпроект остаётся repo-local и docs-only.
- Первый proof идёт на узком `workflow_docs`-профиле.
- Полезность skill должна быть доказана не только сборкой request pack, но и получением по нему годного внешнего `V3 artifact package`.
- Допустим только один узкий helper script-класс: `request-pack preflight`, и только по отдельному human decision.
- `Stage 6` этим планом не открыт.
- Human approval ничем не подменяется.

## Source of Truth и порядок чтения

Для этого подпроекта authoritative basis такой:

1. `AGENTS.md`
2. `.ai/subprojects/ork_planner/ork_planner_stage5_first_pilot_bridge.md`
3. связанные docs `ork_planner`
4. `.ai/subprojects/templates/subproject_templates_guide.md`
5. `.ai/v3/contracts/v3_request_contract.md`
6. `.ai/v3/contracts/v3_artifact_package_contract.md`
7. session artifact `2026-06-02_stage5_v3_request_pack_skill_pilot.md`

Если документы расходятся, приоритет у более нового локального human-approved слоя. Для этого пилота нельзя молча возвращать legacy route или открывать repo-level rollout заранее.

## Папка подпроекта и canonical file set

Папка подпроекта:

`D:\Codex+Kilocode\projects\sword-of-rome-web\.ai\subprojects\v3_request_pack_skill_pilot\`

Canonical baseline file этого planning шага:

- `v3_request_pack_skill_pilot_plan_full.md`

Reduced docs set для первого прохода подпроекта:

- `v3_request_pack_skill_pilot_plan_full.md`
- `v3_request_pack_skill_pilot_battle_plan.md`
- `v3_request_pack_skill_pilot_readme.md`
- `v3_request_pack_skill_pilot_status.md`
- `v3_request_pack_skill_pilot_navigation.md`
- `v3_request_pack_skill_pilot_journal.md`
- `v3_request_pack_skill_pilot_decisions.md`

Waiver:

- `v3_request_pack_skill_pilot_plan_index.md` можно временно не создавать, пока `plan_full` остаётся коротким и читаемым.

Причина, почему `decisions.md` не waived: уже есть долгоживущие решения по skill home, proof bar, gates и stop rules.

## Scope пилота

### Внутри scope

- спланировать первый `Stage 5` pilot как новый tiny docs-only подпроект;
- зафиксировать цель skill и узкий первый proof profile;
- определить docs set подпроекта;
- определить lifecycle, gates и stop rules;
- определить, каким образом пилот доказывает полезность skill;
- при необходимости готовить внешний `V3 request` на draft planning docs.

### Вне scope

- писать сам skill;
- запускать import через `Kilo Notebook V3`;
- считать `Stage 6` начатым;
- заранее проектировать repo-level promotion;
- возвращать legacy route;
- подменять human approval агентным решением;
- расширять первый proof до `scripts`, `schemas` или `product_code`.

## Целевой skill и его границы

Рабочее имя skill:

`v3-request-pack-prep`

Proposed skill home до отдельного capability-sensitive human gate:

`C:\Users\andre\.codex\skills\v3-request-pack-prep\`

Skill version 1 должен уметь:

- помогать собирать `V3 request pack` для внешнего чата;
- удерживать обязательные поля `v3_request_contract.md`;
- удерживать GitHub-first rule;
- удерживать границу `request != package != import`;
- помогать собирать `allowed_paths`, `forbidden_paths`, `expected_files`, `acceptance_criteria`, `known_risks`;
- помогать выбирать безопасный proof task под первый внешний прогон.

Skill version 1 не должен:

- сам импортировать package;
- писать repo files напрямую;
- выполнять post-import testing;
- расширяться за пределы `workflow_docs` без нового planner/human gate.

## Authorization boundary

Принятие этого `plan_full` разрешает только:

- уточнять и пересматривать локальные planning docs подпроекта;
- готовить следующий human decision point;
- при отдельном решении человека готовить узкий `V3 request` на внешний draft planning docs.

Принятие этого `plan_full` не разрешает:

- materialize global skill;
- запускать внешний proof автоматически;
- импортировать какой-либо package;
- обновлять repo-level workflow docs как promoted standard;
- открывать `Stage 6`;
- писать scripts, кроме отдельно одобренного узкого preflight helper.

### Что skill version 1 должен предотвращать

Skill version 1 должен активно удерживать от типичных ошибок:

- внешнему чату переданы только локальные пути вместо commit-pinned GitHub raw URLs;
- raw URLs не pinned к конкретному commit;
- `allowed_paths` слишком широкие, `forbidden_paths` пропущены;
- external chat попросили писать в repo напрямую;
- `current_stage` не указан или неверен;
- `post_import_testing.mode` пропущен;
- human approval ослаблен или заменён;
- scope расширен до scripts/product code без нового gate;
- proof остановился на request pack, внешний package не проверен.

## Proof profile для первого пилота

Первый proof task должен быть маленьким и проверяемым.

Базовый профиль:

- `action = create`
- `scope = workflow_docs`
- `current_stage = external_artifact_generation_only`
- `post_import_testing.mode = waived`
- target task = 1-2 markdown-файла под `.ai/` или `docs/`
- без кода
- без scripts

### First proof must be boring

Первый proof должен быть намеренно скучным и узким:

- один внешний чат;
- один `V3 request pack`;
- один returned package;
- один create-only markdown target;
- без overwrite;
- без import;
- без `schemas`;
- без `product_code`.

### Candidate boring proof task

Базовый кандидат для первого proof:

- создать один короткий markdown-файл:
  - `.ai/subprojects/v3_request_pack_skill_pilot/examples/example_v3_request_pack_checklist.md`
- `scope = workflow_docs`
- `action = create`
- `post_import_testing.mode = waived`
- `allowed_paths` ограничить:
  - `.ai/subprojects/v3_request_pack_skill_pilot/examples/`
- `forbidden_paths` явно включить:
  - `AGENTS.md`
  - `.ai/repo_navigation.md`
  - `.ai/v3/contracts/`
  - `.ai/rules/`
  - `scripts/`
  - `src/`
  - `package.json`

### Full V3 request checklist

Первый proof request pack должен явно покрывать все обязательные поля контракта:

- `v3_id`
- `task_title`
- `generated_by`
- `action`
- `scope`
- `current_stage`
- `context_summary`
- `task_description`
- `allowed_paths`
- `forbidden_paths`
- `expected_files`
- `package_format`
- `acceptance_criteria`
- `known_risks`
- `post_import_testing`
- `no_repo_access_statement`

### Request-pack-only proof недостаточен

Proof должен дойти до реального внешнего `V3 artifact package`, а не остановиться на красивом request pack. Request pack — необходимый, но не достаточный шаг. Полезность skill считается доказанной только если flow доходит до годного внешнего package.

### Evidence layers

Proof должен давать четыре слоя evidence:

**Evidence A — Request pack quality.** Реальный request pack с обязательными полями `v3_request_contract.md`, commit-pinned raw URLs, allowed/forbidden paths, expected files, acceptance criteria, чёткой границей `request != package != import`.

**Evidence B — External package quality.** Внешний чат возвращает реальный ZIP artifact package (не только советы). Пакет содержит `manifest.yaml`, `README_FOR_KILO.md`, `README_FOR_CODEX.md`, `checksums.sha256`, `files/`.

**Evidence C — Package-only review.** Пакет проверяется без импорта. Review подтверждает: manifest существует, файлы совпадают со списком, хэши сходятся, пути внутри `allowed_paths`, вне `forbidden_paths`, scope остаётся `workflow_docs`, пакет не утверждает, что repo изменён.

**Evidence D — Human gate preservation.** Review явно фиксирует: human approval всё ещё обязателен, import-stage не начат, Stage 6 не начат.

### Минимальный proof bar

1. skill помогает собрать один реальный `V3 request pack`;
2. по этому pack внешний чат возвращает один реальный `V3 artifact package`;
3. package проходит package-only review как годный для своей стадии.

## Lifecycle и gates

### Stage 5 pilot lifecycle

Operational detail держать в `battle_plan`. Сам `plan_full` фиксирует только крупные gates и границы.

1. `Planner phase`
   Зафиксировать `plan_full`, folder, target skill path, scope, proof profile и waivers.
2. `Human gate A`
   Человек явно принимает `plan_full`.
3. `Orc phase 1`
   Создать `battle_plan`.
4. `Human gate B`
   Человек явно принимает `battle_plan`.
5. `Orc phase 2`
   Создать remaining docs set подпроекта и вести `journal`/`decisions`.
6. `Human gate C`
   Человек принимает docs-system подпроекта как пригодный для продолжения.
7. `Capability-sensitive gate`
   Отдельный human signal на создание глобального skill вне repo.
8. `Skill build phase`
   Только после gate можно materialize минимальный bundle skill.
9. `Proof phase A`
   Применить skill к одной реальной маленькой `workflow_docs` задаче и собрать request pack.
10. `Human gate D`
   Человек явно разрешает внешний прогон request pack.
11. `Proof phase B`
   Внешний чат возвращает реальный `V3 artifact package`.
12. `Human gate E`
   Человек подтверждает, что returned package годный для своей стадии.
13. `Final verdict`
   `accepted`, `needs revision` или `rejected`.

### Жёсткие правила lifecycle

- Пока не закрыт текущий human gate, следующий execution step не стартует.
- Package generation не равен import-stage.
- Годный внешний package не равен accepted repo result.
- Package-only review — обязательный шаг перед любым решением об импорте.
- Package-only review не открывает import-stage автоматически.
- Принятый `Stage 5` pilot не равен началу `Stage 6`.

## Package-only review

Package-only review — это проверка полученного внешнего `V3 artifact package` без его импорта в репозиторий. Review подтверждает:

- ZIP содержит один root folder формата `V3-YYYYMMDD-HHMMSS-short-topic/`, а не россыпь файлов в корне;
- `manifest.yaml` существует, файлы совпадают со списком;
- SHA-256 хэши из `checksums.sha256` сходятся;
- все target paths внутри `allowed_paths`, ни один не в `forbidden_paths`;
- scope остаётся `workflow_docs`, action остаётся `create`;
- пакет не утверждает, что repo уже изменён;
- пакет не заявляет, что результат accepted или импортирован.

Package-only review — это gate перед любым решением об импорте. Он не открывает import-stage и не является human verdict.

## Как пилот докажет полезность skill

Пилот должен доказать не абстрактную "интересность", а реальную операционную пользу.

Польза считается доказанной, если одновременно выполнено всё ниже:

- skill помогает собрать request pack без путаницы между request/package/import;
- request pack содержит обязательные поля контракта;
- request pack удерживает GitHub-first context mode;
- request pack не допускает forbidden-path drift;
- внешний чат по этому request pack возвращает годный `V3 artifact package`, а не только советы;
- package проходит package-only review (без импорта);
- человеку понятно, что со skill flow стал чище, быстрее или стабильнее, чем ручная сборка.

Returned package считать годным только если:

- это реальный ZIP artifact package;
- структура соответствует `v3_artifact_package_contract.md`;
- есть `manifest.yaml`;
- есть `README_FOR_KILO.md`;
- есть `README_FOR_CODEX.md`;
- есть `checksums.sha256`;
- project files лежат только под `files/`;
- package не заявляет, что repo уже изменён;
- package остаётся внутри `workflow_docs` scope;
- scope не расширился до scripts/product code без нового gate.

Даже успешный pilot даёт только `candidate skill/process evidence`. Он не даёт автоматического разрешения на repo-level promotion, import-stage или `Stage 6`.

## Automation policy

Для этого pilot допустим только один automation-класс:

- узкий `request-pack preflight helper`

Его цель:

- быстро проверить draft `V3 request pack` перед отправкой во внешний чат;
- поймать пропущенные обязательные поля;
- поймать неполные `allowed_paths` / `forbidden_paths`;
- поймать raw GitHub URLs, которые не pinned к commit;
- поймать drift между `expected_files`, `allowed_paths` и `forbidden_paths`.

Этот helper не должен:

- сам писать request pack вместо человека;
- генерировать ZIP package;
- импортировать package;
- писать repo files по умолчанию;
- обновлять repo-level docs;
- подменять human approval;
- открывать `Stage 6`.

Этот helper допустим только по отдельному human decision. Для текущего pilot это узкое исключение, а не расширение первого proof до scripts/product code.

## Stop rules

Нужно остановиться и вернуть вопрос человеку, если:

- scope хочет выйти за `workflow_docs`;
- появляется желание добавить automation шире, чем узкий `request-pack preflight helper`;
- proof требует repo-level writes;
- кто-то пытается считать package import-stage результатом или accepted результатом без package-only review;
- возникает попытка импортировать package без package-only review;
- возникает попытка открыть `Stage 6` без принятого `Stage 5`;
- возникает попытка трактовать успешный pilot как разрешение на repo-level promotion;
- становится неясно, должен ли skill жить глобально или repo-local;
- для безопасного решения не хватает важной информации.

## Success criteria

Пилот можно считать успешным только если одновременно выполнено всё ниже:

- новый подпроект создан и остаётся docs-only;
- canonical route везде остаётся `Planner -> Orc`;
- human gates были явными;
- итоговый skill materialized только после отдельного human signal;
- skill version 1 остаётся узким и не выходит за `workflow_docs`;
- собран один реальный `V3 request pack`;
- по нему получен один реальный годный внешний `V3 artifact package`;
- package проходит package-only review;
- `Stage 6` не объявлен начатым;
- repo-level promotion заранее не заявлен.

## Ближайший безопасный следующий шаг

Следующий безопасный шаг зависит от выбора человека:

- либо уточнять и усиливать локальный `plan_full`;
- либо готовить `V3 request` на внешний draft planning docs;
- но не переходить к skill execution без отдельного разрешения.
