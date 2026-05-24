# Handoff 0009: Canonical Fixture Seed

## Статус

Готово для Kilo

## Рекомендуемый Kilo mode

kilo-handoff-runner

## Task role

Builder Agent

## Task profile

small-code

## Execution mandate

`agent-first`

## Primary execution path

`Kilo Code`

## Allowed agent kinds

- `Kilo Code`

## Default preference

Работать только внутри:

- [sword-of-rome-web](/D:/Codex+Kilocode/projects/sword-of-rome-web)

## Exception status

`none`

## Minimum substantive agent work

Создать самый маленький canonical fixture seed для следующего runtime шага.

Нужен только data-only scope:

1. создать папку `table-sandbox/src/fixtures/tiny-module/`;
2. создать внутри неё минимальный набор fixture-файлов:
   - `project.json`
   - `modules/tiny-module/module.json`
   - `modules/tiny-module/map.json`
   - `modules/tiny-module/scenario.basic.json`
   - `modules/tiny-module/rules.metadata.json`
   - `saves/savegame.empty.json`
   - `README.md`
3. сделать fixture нейтральным, маленьким и внутренне согласованным;
4. не лезть в loader, runtime bootstrap, Phaser rendering, prototype migration.

Это fixture-задача, не runtime-задача.

## Sequential agent policy

Только один run в рамках этого handoff: один запуск -> report -> review Codex.

## If no agent path fits -> return escalation note

Если упрёшься в schema-detail развилку, не расширяй scope. Выбери самый узкий рабочий вариант, совместимый с canon и с этим handoff, и зафиксируй выбор в report. Если без этого задача превращается в loader/runtime design, верни `Blocked`.

## Session plan

[2026-05-23_architecture_orchestration_v1_planning.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-05-23_architecture_orchestration_v1_planning.md)

## Plan item

`P3: Consolidate Architecture And Next Steps`

## Session run

`002`

## Рекомендуемый класс модели

fast_coding_model

## Default model

Qwen3 Coder 480B

## Fallback model или Candidate models

- Qwen3 Coder Next
- DeepSeek V4 Pro

## Когда эскалировать в strong_model

- если задача начинает расползаться из fixture seed в runtime/data architecture;
- если без широкой schema-переработки нельзя принять ни один компактный вариант;
- если модель начинает тащить в handoff loader, validator framework или prototype migration.

## Уровень риска

Низкий

## Цель

Получить tiny canonical data seed, который:

- лежит рядом с новым `table-sandbox`;
- задаёт минимальные canonical definitions и runtime/save boundary;
- готовит следующий шаг `Runtime/Data Bootstrap`;
- не смешивает definitions, initial setup, rules metadata и runtime snapshot.

## Контекст проекта

- `0008` уже принят как узкий `Phase 1 - Technical Bootstrap`.
- Следующий принятый узкий шаг по `V1-20260524-184203` = `Canonical Fixture Seed`.
- Принята временная compact `0.1` политика:
  - маленькие `factions[]` и `pieceDefinitions[]` пока допустимы внутри `module.json`;
  - `map.json` = topology only;
  - `scenario.basic.json` = initial setup only;
  - `rules.metadata.json` = declarative metadata only;
  - `savegame.empty.json` = runtime/save artifact only.
- Этот handoff не открывает новую архитектурную фазу. Он только создаёт tiny fixture set для следующего run.

## Required Inputs

- [AGENTS.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/AGENTS.md)
- [README.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/README.md)
- [repo_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/repo_navigation.md)
- [2026-05-23_architecture_orchestration_v1_planning.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-05-23_architecture_orchestration_v1_planning.md)
- [pre_code_closure_and_first_execution_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/master/pre_code_closure_and_first_execution_plan.md)
- [first_product_code_block.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/implementation/first_product_code_block.md)
- [2026-05-24_V1-20260524-184203_detailed-decomposition-of-the-next-narrow-step-canonical.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_chats/notebook/2026-05-24_V1-20260524-184203_detailed-decomposition-of-the-next-narrow-step-canonical.md)

## Lookup Inputs

- [minimal_canonical_file_schemas.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/master/minimal_canonical_file_schemas.md)
- [first_vertical_slice_spec.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/master/first_vertical_slice_spec.md)
- [action_event_contract.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/master/action_event_contract.md)
- [2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md)

## Context Budget

- Фокус только на tiny fixture data.
- Не делать loader.
- Не делать runtime `GameState` expansion.
- Не делать Phaser changes.
- Не делать `move_piece_requested -> piece_moved` implementation.
- Не делать schema library, validator framework, Zod generation.
- Не делать prototype migration.

## Do Not Read Unless Blocked

- другие `.ai/external_chats/**`, кроме явно указанных выше notebook entry
- `_local/**`
- `arena-prototype-launcher/**`
- `references/**`
- старые handoff/report, не связанные с `0008`/`0009`

## Implementation Constraints

- Fixture path зафиксирован:
  - `table-sandbox/src/fixtures/tiny-module/`
- Используй нейтральные tiny IDs:
  - `tiny-project`
  - `tiny-module`
  - `tiny-map`
  - `basic`
  - `tiny-empty-save`
  - `tiny-red`
  - `tiny-blue`
  - `infantry`
  - `piece-1`
  - `space-a`
  - `space-b`
  - `connection-a-b`
  - `manual`
- Минимальный fixture content:
  - 1 project
  - 1 module
  - 1 map
  - 2 spaces
  - 1 connection
  - 1 scenario
  - 2 factions
  - 1 piece definition
  - 1 piece instance
  - 1 manual phase
  - supported action `move_piece_requested`
  - supported event `piece_moved`
- `module.json` может временно содержать compact `factions[]` и `pieceDefinitions[]`.
- `savegame.empty.json` должен быть маленьким runtime snapshot artifact с пустым `eventLog`.
- Все JSON должны быть читаемыми людьми и парситься.

## File Role Contract

### `project.json`

Должен содержать только workspace/project-level index:

- `schemaVersion`
- `projectId`
- `name`
- `activeModuleId`
- `modules[]`

Не должен содержать карту, сценарий setup, event log, runtime state.

### `module.json`

Должен содержать manifest-level данные плюс compact `0.1` content:

- `schemaVersion`
- `moduleId`
- `name`
- `version`
- `engineCompatibility`
- `defaultMapId`
- `defaultScenarioId`
- `files`
- `rules`
- `factions[]`
- `pieceDefinitions[]`

Не должен содержать topology, piece instances, event log, save state, executable rules.

### `map.json`

Должен содержать только topology:

- `schemaVersion`
- `mapId`
- `moduleId`
- `version`
- `name`
- `coordinateSystem`
- `spaces[]`
- `connections[]`
- `zones[]`

Не должен содержать pieces, control state, turn state, save state, rules logic.

### `scenario.basic.json`

Должен содержать только initial setup:

- `schemaVersion`
- `scenarioId`
- `moduleId`
- `mapId`
- `name`
- `version`
- `setup`

`setup` должен включать:

- `turnState`
- `pieces`
- `controlBySpace`
- `variables`

Не должен содержать topology, definitions, event log, save snapshots.

### `rules.metadata.json`

Должен содержать только declarative metadata:

- `schemaVersion`
- `rulesVersion`
- `hookContractVersion`
- `automationLevel`
- `supportedActionTypes[]`
- `supportedEventTypes[]`
- `phases[]`

Не должен содержать executable rule functions, runtime state, event log, Phaser/DOM details.

### `savegame.empty.json`

Должен содержать только runtime/save artifact:

- `schemaVersion`
- `saveId`
- `engineVersion`
- `moduleId`
- `moduleVersion`
- `mapId`
- `mapVersion`
- `scenarioId`
- `scenarioVersion`
- `gameState`
- `eventLog[]`

`gameState` можно сделать как маленькое ручное зеркало initial setup. `eventLog` должен быть `[]`.

Не должен дублировать full module definitions, map topology или piece definitions.

### `README.md`

Коротко объясни роль fixture seed и границу между definitions, setup и save.

## Cross-File Consistency Requirements

Нужно обеспечить:

- `project.activeModuleId == module.moduleId`
- `project.modules[0].moduleId == module.moduleId`
- `module.defaultMapId == map.mapId`
- `module.defaultScenarioId == scenario.scenarioId`
- `scenario.moduleId == module.moduleId`
- `scenario.mapId == map.mapId`
- `map.moduleId == module.moduleId`
- `connection.fromSpaceId` и `connection.toSpaceId` существуют в `map.spaces`
- `scenario.setup.pieces[0].pieceDefId` существует в `module.pieceDefinitions`
- `scenario.setup.pieces[0].locationId` существует в `map.spaces` или `map.zones`
- `scenario.setup.pieces[0].ownerId` существует в `module.factions`
- `scenario.setup.turnState.phaseId` существует в `rules.metadata.phases`
- `rules.supportedActionTypes` включает `move_piece_requested`
- `rules.supportedEventTypes` включает `piece_moved`
- `savegame` ids/versions совпадают с fixture files
- `savegame.eventLog` равен `[]`

## Allowed Changes

- `table-sandbox/src/fixtures/tiny-module/**`
- новый report по пути ниже

## Forbidden Changes

- не менять `table-sandbox/src/**`, кроме fixture path
- не менять Phaser renderer
- не добавлять loader/runtime code
- не добавлять validator framework
- не трогать `arena-prototype-launcher/**`
- не трогать `canon/**`, `references/**`, `docs/**`
- не создавать новые handoff/session files

## Verification Requirements

Минимум:

1. все requested files созданы;
2. все JSON парсятся;
3. IDs и cross-file references внутренне согласованы;
4. file roles не смешаны;
5. `map.json` содержит topology only;
6. `scenario.basic.json` содержит initial setup only;
7. `rules.metadata.json` содержит metadata only;
8. `savegame.empty.json` не дублирует canonical definitions;
9. в repo нет scope creep в runtime/Phaser/prototype.

Если есть дешёвый способ, добавь короткую verification command для JSON parse/check consistency. Не пиши полноценный validator subsystem.

## Acceptance Shape

Результат считается годным, если после review видно:

- tiny fixture tree создан в правильном path;
- definitions / setup / rules metadata / save artifact разделены;
- IDs скучные, стабильные, нейтральные;
- fixture уже готов для следующего handoff `Runtime/Data Bootstrap`;
- runtime code и Phaser layer не были задеты.

## Stop Conditions

- без loader/runtime кода нельзя честно завершить задачу;
- для согласованности данных внезапно требуется broad schema redesign;
- модель начинает тащить Sword-specific content вместо neutral tiny fixture;
- появляется желание добавить ещё карты, сценарии, фазы, actions сверх минимума.

## Критерии приёмки

- [ ] создан `table-sandbox/src/fixtures/tiny-module/`
- [ ] созданы все 7 requested files
- [ ] JSON files парсятся
- [ ] `project.json` = project index only
- [ ] `module.json` = manifest + compact `factions[]`/`pieceDefinitions[]`
- [ ] `map.json` = topology only
- [ ] `scenario.basic.json` = initial setup only
- [ ] `rules.metadata.json` = declarative metadata only
- [ ] `savegame.empty.json` = runtime/save artifact only
- [ ] `supportedActionTypes` содержит `move_piece_requested`
- [ ] `supportedEventTypes` содержит `piece_moved`
- [ ] `phaseId: manual` согласован между scenario и rules metadata
- [ ] нет loader/runtime/Phaser/prototype scope creep
- [ ] report содержит file tree, verification и список changed files

## Report mode

full

## Куда записать report

[0009_canonical_fixture_seed_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0009_canonical_fixture_seed_report.md)

## Что вернуть после запуска

- путь к report
- список локально изменённых и созданных файлов
- краткий итог:
  - `fixture seed done`
  - или `Blocked`
- какие команды проверки реально запускались
- был ли выбран exact fixture path из handoff без отклонений
