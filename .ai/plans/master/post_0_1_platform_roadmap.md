# Post-0.1 Platform Roadmap

## Status

Planning artifact. Macro-roadmap after `Table Sandbox 0.1`.

## Purpose

Зафиксировать следующий крупный слой planning после `Table Sandbox 0.1`:

- как проект растёт дальше как platform-first product;
- какие milestones идут после `0.1`;
- что каждый milestone должен доказать;
- как не дать Sword of Rome-like test module превратить lower layers в hardcoded одну игру.

Этот документ не меняет уже принятый `0.1` scope. Он описывает, как двигаться дальше
после него.

## Roadmap Assumptions

Считаем уже принятым:

- `4-layer` product architecture;
- canonical split `definitions / runtime state / module rules`;
- canonical file set;
- `RulesHooksInterface` boundary;
- `Action / Event` backbone;
- safe default stack model for `0.1`;
- basic save compatibility policy for `0.1`;
- hybrid `Module Authoring Workspace` with specialized surfaces and explicit
  `Play Sandbox Preview`.

Главное следствие:

- следующий roadmap должен выращивать platform capabilities;
- Sword of Rome-like module должен оставаться reference/test module;
- нельзя делать следующий шаг как "теперь просто доделаем одну игру".

## Milestone 0.2 - Platform Hardening

### What It Must Prove

`Table Sandbox 0.1` не одноразовая демка, а стабильный фундамент:

- canonical files можно валидно загрузить;
- `GameState` стабильно собирается из module/scenario;
- save/load не ломает boundaries файлов;
- event log и runtime snapshot устойчивы;
- preview запускается только на валидном module package.

### New Platform Capabilities

- более строгая validation layer перед `Play Sandbox Preview`;
- понятные ошибки по ids и broken references;
- стабильный import/export canonical files;
- базовая save compatibility policy в действии;
- authoring undo/redo только для editor-side изменений;
- play sandbox restart/load/save без сложного runtime undo.

### Dependencies

- зависит от принятого `0.1` first slice;
- требует уже работающий `Action -> Event -> GameState -> log -> render`.

### Main Risks

Scope creep:

- начать тащить game-specific rules вместо укрепления foundation.

Architectural drift:

- копировать definitions в `savegame.json`;
- писать runtime state в `map.json`;
- обходить event pipeline ради "быстрого удобства".

## Milestone 0.3 - Authoring Workspace Expansion

### What It Must Prove

Дизайнер умеет не только гонять фишку в preview, но и собрать маленький валидный
module package через нормальный authoring workflow.

### New Platform Capabilities

- более полный `Module Authoring Workspace`;
- устойчивые surfaces для:
  - map;
  - pieces/factions;
  - scenario;
  - module settings;
  - rules metadata;
- отдельная команда "проверить модуль перед preview";
- при необходимости вынос `PieceDefinition[]` и `FactionDefinition[]` из
  `module.json` в отдельные content files;
- более зрелый authoring undo/redo.

### Dependencies

- требует стабильный file contract из `0.1` и hardening из `0.2`.

### Main Risks

Scope creep:

- превратить workspace в один огромный суперредактор без явных boundaries.

Architectural drift:

- размыть границу между authoring mode и play sandbox mode;
- начать смешивать definitions, scenario setup и runtime state.

## Milestone 0.4 - Assisted Runtime And Rules Hooks

### What It Must Prove

Runtime умеет не только вручную двигать объекты, но и получать structured
module-specific guidance через `RulesHooksInterface`, при этом universal runtime
всё ещё не знает конкретную игру изнутри.

### New Platform Capabilities

- устойчивый `resolveAction` в runtime flow;
- `validateAction` с warning/block semantics;
- `getAllowedActions` для UI hints;
- phase scaffold и phase metadata;
- первые assisted checks без full strict enforcement.

### Dependencies

- требует стабильные `Action/Event` contracts;
- требует, чтобы runtime оставался единственным коммиттером state changes.

### Main Risks

Scope creep:

- попытаться сразу сделать полные правила Sword of Rome-like игры.

Architectural drift:

- дать module rules напрямую менять `GameState` или renderer objects;
- вынести game-specific logic в lower layers вместо hooks boundary.

## Milestone 0.5 - Generic Cards And Documents

### What It Must Prove

Платформа может универсально поддерживать card-driven и document-heavy modules,
а не только map-and-counters sandbox.

### New Platform Capabilities

- generic card definitions;
- generic deck definitions;
- piles/hands/discard как runtime state;
- documents/player-aids registry;
- простые card actions вроде draw/discard/reveal/play-as-manual-event;
- cards/documents как часть module package, а не hardcoded game logic.

### Dependencies

- требует стабильный module package format;
- требует save/load boundaries, rules metadata и runtime state model.

### Main Risks

Scope creep:

- начать реализовывать card effects одной конкретной игры вместо generic layer.

Architectural drift:

- спрятать executable rules в JSON metadata;
- зашить game-specific card semantics в universal runtime.

## Milestone 1.0 - Modular Platform Alpha

### What It Must Prove

Это уже не proto одной карты, а ранняя modular platform:

- можно собрать, проверить, сохранить и запустить больше одного module package;
- Sword of Rome-like module остаётся reference/test module;
- lower layers не становятся branch под одну игру.

### New Platform Capabilities

- module package import/export;
- module validation report;
- version/reference compatibility rules;
- отдельные content files для pieces, factions, cards, documents, assets;
- минимум два test modules:
  - tiny generic test module;
  - Sword of Rome-like reference module;
- stable save/load boundaries;
- documented extension points and non-goals.

### Dependencies

- опирается на `0.2`, `0.3`, `0.4`;
- `0.5` нужен, если alpha уже должна поддерживать card-driven modules.

### Main Risks

Scope creep:

- назвать это "готовой игрой" и начать доделывать исторические детали вместо
  modular platform alpha.

Architectural drift:

- строить acceptance criteria только вокруг Sword of Rome-like module;
- добавлять universal fields и flows, нужные только одной игре.

## Universal Vs Module-Specific Vs Reference Module

### Universal Platform Growth

Сюда относится то, что нужно любому модулю:

- canonical file loading;
- validation;
- map/scenario/piece authoring;
- `Action/Event` pipeline;
- `GameState`;
- save/load;
- generic cards/decks later;
- documents/player aids;
- `RulesHooksInterface`;
- module package import/export.

### Module-Specific Growth

Сюда относится поведение конкретного module package:

- конкретные phases;
- конкретные movement restrictions;
- конкретные scoring rules;
- конкретные victory checks;
- конкретные card effects.

Это должно жить за hooks boundary, а не в lower layers.

### Sword Of Rome-Like Reference Growth

Сюда относится только reference/test content:

- конкретная карта;
- конкретные factions;
- конкретные pieces;
- конкретные scenarios;
- конкретные cards;
- конкретные hooks implementation.

Rule:

- если capability нужна только Sword of Rome-like module, она не должна
  попадать в Layer 1-3 без отдельного доказательства универсальности.

## Anti-Hardcoding Rules

Чтобы test module не превратил платформу в hardcoded игру:

1. Держать рядом tiny generic test module и Sword of Rome-like reference module.
2. Не добавлять в universal schema поля с названиями конкретной игры.
3. Все special rules держать только за `RulesHooksInterface`.
4. Жёстко разделять content и behavior.
5. Для каждого milestone писать platform acceptance criteria, а не
   "правильно разложили римские легионы".

## Deliberately Deferred Even After 0.1

Даже после `0.1` сознательно не тащить слишком рано:

- full strict rules enforcement;
- full Sword of Rome rules;
- combat resolver;
- full scoring/victory engine;
- hidden information;
- response/interrupt windows;
- online multiplayer;
- server-authoritative runtime;
- AI;
- full migration engine;
- advanced stack model as first-class `Stack`;
- polished publishing platform;
- module marketplace/library;
- collaborative authoring;
- full replay UI;
- rules scripting language.

Причина одна:

- это полезно later, но не должно идти раньше стабильных platform foundations.

## Safe Branch Vs Risky Branch

### Safe Branch

```text
0.1 sandbox loop
-> 0.2 hardening/validation/save compatibility
-> 0.3 authoring workspace expansion
-> 0.4 assisted runtime/rules hooks
-> 0.5 generic cards/documents
-> 1.0 modular platform alpha
```

Плюс:

- каждый milestone укрепляет foundation перед следующим слоем сложности.

### Risky Branch

```text
0.1 move-piece slice
-> сразу full Sword of Rome rules
-> сразу cards/combat/scoring
-> сразу detailed historical scenarios
-> потом попытка обобщить
```

Минус:

- lower layers почти наверняка станут "цифровой Sword of Rome", а не reusable
  authoring/runtime platform.

## Open Questions

Этот roadmap не закрывает автоматически:

- точную release numbering policy;
- exact acceptance criteria для каждого milestone;
- exact migration/versioning model after `0.2`;
- hidden info and server-authoritative path;
- AI scope.

## Recommended Use

Использовать этот документ как macro-roadmap над `Table Sandbox 0.1`, а не как
замену его milestone plan.

## Package Model Placement

`module_package_model.md` belongs to the post-`0.1` packaging track.

Use this roadmap to decide when package complexity should grow:

- `0.2` hardening validates the compact package;
- `0.3` authoring breadth often triggers first package splitting;
- `0.5` and `1.0` are where richer package zones become normal, not special.

## UX Model Placement

`module_product_ux_model.md` belongs to the post-`0.1` product-UX track.

Use this roadmap to decide when UX complexity should grow:

- `0.2` hardens the minimal user loop: validate, preview, restart, save, and
  return to authoring;
- `0.3` makes the Module Authoring Workspace feel like a coherent daily tool;
- `0.4` improves playtest feedback through assisted runtime while keeping mode
  boundaries explicit;
- `0.5` broadens UX to richer content flows such as cards/documents;
- `1.0` should read as one coherent authoring/runtime platform, not a loose
  pile of tools.

## Prototype Placement

External prototypes like `table-map-editor-canvas-local-fixed` belong on the
authoring-side growth line, mainly as reference material for the future Map
Editor surface.

They should not steer the roadmap toward a prototype-first foundation. The
roadmap remains platform-first, and the prototype is only a donor of specific
UX and interaction ideas.
