# Module Product UX Model

## Status

Planning artifact. Target UX model for the product as a whole.

## Purpose

Зафиксировать не отдельный editor surface, а полный пользовательский цикл:

- как дизайнер создаёт модуль;
- как он валидирует package;
- как запускает playtest;
- как возвращается в authoring;
- как работает с runtime save/snapshot;
- как доводит модуль от черновика до проверяемого состояния.

Этот документ не задаёт wireframes и не уходит в frontend implementation.
Он задаёт продуктовую UX-модель, режимы работы и границы между ними.

## Product Reading

Продукт должен читаться не как один экран, а как mode-based workflow:

- `authoring` для definitions и setup;
- `playtest preview` для runtime proof;
- `runtime session` для продолжения или просмотра состояния;
- `package/save workflow` для validation, save, fork и package lifecycle.

Пользователь должен всегда понимать:

- в каком он сейчас режиме;
- что именно изменяет текущее действие;
- какой артефакт получится на выходе.

## Core UX Modes

### 1. Authoring Mode

Назначение:

- редактирование module content;
- редактирование map/topology;
- редактирование pieces/factions;
- редактирование scenario setup;
- редактирование rules metadata.

Главный артефакт:

- canonical module package.

Пишет:

- `module.json`
- `map.json`
- `scenario.<scenarioId>.json`
- `rules.metadata.json`
- later other package content files.

### 2. Playtest Preview Mode

Назначение:

- быстро проверить модуль в действии;
- прогнать runtime loop;
- увидеть, как definitions и setup работают в sandbox.

Главный артефакт:

- short-lived runtime session over the current module package.

Пишет:

- runtime state;
- event log;
- optional runtime snapshot.

Не пишет:

- canonical definitions silently.

### 3. Runtime Session Mode

Назначение:

- открыть существующий runtime snapshot;
- продолжить или просмотреть состояние партии;
- проверять runtime behavior отдельно от authoring.

Главный артефакт:

- `savegame.json` and related runtime state.

Это не definitions editor и не должен им притворяться.

### 4. Package / Save Workflow

Назначение:

- validate module package;
- launch preview from valid content;
- save runtime snapshot;
- later fork runtime state into new scenario through explicit flow.

Это не отдельный content mode, а служебный workflow layer между режимами.

## Recommended UX Model

Safe default:

```text
one product shell
+ explicit mode switch
+ one Module Authoring Workspace
+ one Play Sandbox Preview path
+ one separate runtime/save flow
```

Не нужен ни один гигантский "do everything" экран, ни набор полностью
несвязанных приложений.

Нужен один продуктовый shell с явными режимами и понятными переходами.

## Daily Workflow Loop

Типичный day-to-day loop дизайнера:

1. Open or create module package.
2. Enter `authoring`.
3. Edit map, pieces, factions, scenario, module metadata.
4. Run validation.
5. Fix broken references or schema issues.
6. Launch `Play Sandbox Preview`.
7. Perform a small playtest action sequence.
8. Inspect runtime state and event log.
9. If the issue is in content/setup, return to `authoring`.
10. If the issue is in runtime behavior, keep it in playtest/runtime scope.
11. Save module package changes or save runtime snapshot explicitly.
12. Repeat until the module is stable enough for broader testing.

## Mode Map

### Central from the start

- `authoring`
- `validate package`
- `playtest preview`
- `save runtime snapshot`
- `return to authoring`

### Later

- playtest session manager;
- scenario fork from runtime snapshot;
- richer runtime inspection tools;
- package publishing/export workflows;
- more advanced runtime/session comparison.

## Mode Transitions

Transitions must be explicit:

- `authoring -> validate`
- `validate -> playtest preview`
- `playtest preview -> authoring`
- `playtest preview -> save snapshot`
- `runtime session -> inspect / continue`
- later `runtime snapshot -> create scenario fork`

The same click, drag, or drop must not silently switch between:

- changing a definition;
- changing scenario setup;
- changing current runtime state.

## Package And Save Separation

The user-facing model must preserve this distinction:

- module package = reusable canonical content;
- scenario setup = canonical starting arrangement;
- runtime save = current mutable state after play;
- event log = runtime history, not package content.

Practical rule:

- `Save module` and `Save runtime snapshot` are different actions with different
  outputs;
- later `Create scenario from snapshot` may exist, but only as explicit
  transformation, not as silent save behavior.

## Table Sandbox 0.1 Minimal UX Scope

For `0.1`, the product only needs a thin but coherent loop:

1. Open Module Authoring Workspace.
2. Edit a tiny module package.
3. Validate the package.
4. Launch Play Sandbox Preview.
5. Move one piece through the full runtime pipeline.
6. Inspect board refresh and event log.
7. Save runtime snapshot if needed.
8. Return to authoring for corrections.

`0.1` does not need:

- full runtime session manager;
- scenario fork tooling;
- rich branching/fork UX;
- sophisticated runtime undo/redo;
- publishing workflow;
- collaborative UX.

## Anti-Confusion Rules

1. Authoring changes and runtime changes must stay different user intents.
2. The same visual gesture must not silently write to different file classes.
3. `Play Sandbox Preview` proves runtime, but does not become a hidden editor of
   canonical definitions.
4. `savegame.json` must stay runtime-only in both data model and user mental model.
5. Sword of Rome-like content must remain a test lens, not the center of the UX.

## External Prototype Input

The external `table-map-editor-canvas-local-fixed` prototype is relevant mainly
to the future `Map Editor` surface inside the authoring shell.

Use it as:

- UX reference for map editing behavior;
- selective donor of interaction ideas;
- not a product-wide UX foundation;
- not a runtime/session model.

The main product UX must still be driven by the canonical mode split and package
lifecycle, not by the prototype's internal structure.

## Relation To Other Docs

Read together with:

- `module_authoring_workflow.md`
- `module_package_model.md`
- `table_sandbox_0_1_milestone_plan.md`
- `post_0_1_platform_roadmap.md`

Reading split:

- this file describes the whole product UX model;
- `module_authoring_workflow.md` describes the authoring-side slice;
- `module_package_model.md` describes the package as product artifact;
- `table_sandbox_0_1_milestone_plan.md` describes the first usable loop;
- `post_0_1_platform_roadmap.md` describes how the UX grows after `0.1`.

## Still Open

Still intentionally open:

- exact navigation chrome between modes;
- exact shape of future playtest session manager;
- exact relationship between runtime restart, replay, and snapshot compare;
- whether later runtime mode becomes distinct from preview mode in UI;
- how far scenario-fork tooling should go before `1.0`.
