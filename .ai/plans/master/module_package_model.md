# Module Package Model

## Status

Planning artifact. Target product model for a mature `module package`.

## Purpose

Зафиксировать, какой должна стать зрелая модель `module package` как
продуктовой сущности:

- какие части package обязательны почти всегда;
- какие части optional;
- какие части относятся к content/data;
- какие части относятся к runtime/save;
- как package эволюционирует от compact `Table Sandbox 0.1` layout к зрелому
  multi-part format;
- как не дать одной reference game навязать shape всей платформе.

Этот документ не задаёт implementation. Он задаёт целевую package-модель и
путь взросления формата.

## Product Reading

`Module package` = не один файл, а согласованный набор частей, который описывает
один модуль как самостоятельный продукт:

- content;
- setup;
- rules metadata;
- rules boundary;
- optional rich content;
- packaging metadata.

`savegame.json` не является частью canonical module package content. Save
остается runtime artifact.

## Package Zones

### Core Required Files

Почти любому module package нужны:

- `module.json`
- `map.json`
- at least one `scenario.<scenarioId>.json`
- `rules.metadata.json`

Что они делают:

- `module.json` = entry manifest and package index;
- `map.json` = board/topology definition;
- `scenario.<scenarioId>.json` = initial setup over a map;
- `rules.metadata.json` = declarative rules capability metadata and hook
  contract info.

Что в них не должно жить:

- current runtime save state;
- executable rules code inside JSON metadata;
- event log as canonical content;
- hidden mutable state.

### Gameplay Content Files

Эти части описывают сам модуль как игру, но остаются данными, а не runtime:

- pieces;
- factions;
- cards;
- decks;
- scenarios;
- documents/player aids;
- assets references.

Правило:

- content files describe what exists;
- rules describe what can happen;
- runtime describes what currently happened.

### Optional Rich-Content Files

Optional и later-friendly части:

- `cards.json`
- `decks.json`
- `documents.json`
- `assets.json`
- later `prompts.json`, `conditions.json`, or other rich content files if the
  platform ever needs them.

Эти файлы не должны быть обязательными для `Table Sandbox 0.1`.

### Runtime / Save Files

Отдельно от canonical module content:

- `savegame.json`
- event log
- `GameState`

Правило:

- runtime files are loadable artifacts;
- they are not canonical package content;
- they must not redefine module definitions.

### Packaging / Publishing Metadata

Отдельный слой metadata может понадобиться позже:

- compatibility markers;
- content hashes;
- publication metadata;
- module package versioning;
- migration hints.

Для `0.1` это не нужно делать жирным слоем.

## Required vs Optional

### Required almost everywhere

- `module.json`
- `map.json`
- `rules.metadata.json`
- at least one `scenario.<scenarioId>.json`

### Required for most tabletop modules later

- `pieces.json`
- `factions.json`
- `documents.json` or docs-like registry
- `assets` references

### Optional by module type

- `cards.json`
- `decks.json`
- multiple scenarios
- player aids
- advanced publication metadata
- specialized scenario variants

### Not part of canonical module package content

- `savegame.json`
- transient runtime logs outside save/replay format;
- renderer state;
- UI-specific editor state.

## Evolution Path

### Compact `0.1` Layout

Safe default now:

- keep `pieces[]` and `factions[]` compact, possibly inline in `module.json`;
- keep rules as metadata + hooks boundary, not executable JSON code;
- keep save/runtime separate from content;
- keep one tiny test module readable by humans.

This is a milestone simplification, not the end state.

### Intermediate Package Format

When the module starts growing:

- move `PieceDefinition[]` and `FactionDefinition[]` out of `module.json`;
- split `cards`, `decks`, `documents`, `assets` into their own files if they are
  becoming non-trivial;
- keep a manifest that points to content files, not a dump of all content;
- keep preview/import/export validation package-oriented.

### Mature Package Format

Mature package should look like a product bundle with clear zones:

- core required files;
- gameplay content files;
- optional rich-content files;
- packaging/publishing metadata;
- runtime/save artifacts outside the package.

Mature package should let different module types share one common shape without
forcing every module to have every content type.

## Triggers For Splitting Files

Move content out of `module.json` when:

- `module.json` stops reading like a manifest and starts reading like content;
- pieces/factions become too many to scan comfortably;
- dedicated editor surfaces appear for that content;
- content needs reuse across multiple scenarios or modules;
- import/export validation becomes easier with explicit file boundaries.

Split package further when:

- cards/decks become a real subsystem;
- documents/player aids become first-class content;
- assets need their own registry or lifecycle;
- compatibility metadata becomes non-trivial.

## Boundary Rules

1. `module.json` is manifest, not content dump.
2. `map.json` is topology, not runtime.
3. `scenario` is initial setup, not play history.
4. `rules.metadata.json` is metadata, not executable rules.
5. `savegame.json` is runtime, not canonical content.
6. `rules hooks` are behavior boundary, not hidden content storage.

## Anti-Bloat Rules

- Do not force `cards`, `documents`, and `assets` into every module too early.
- Do not force `savegame` into canonical package model.
- Do not make `rules.metadata.json` a secret place for executable logic.
- Do not let Sword of Rome-like reference content decide universal package shape.
- Keep `0.1` compact only while the manifest still reads like a manifest.

## Relationship To Other Docs

This model should be read together with:

- `domain_schemas_contract.md`
- `minimal_canonical_file_schemas.md`
- `module_authoring_workflow.md`
- `post_0_1_platform_roadmap.md`

## Open Questions

Still intentionally open:

- exact packaging metadata shape;
- exact import/export format;
- exact content hash policy;
- exact migration/versioning policy for mature packages;
- how many optional content zones should become first-class before `1.0`.
