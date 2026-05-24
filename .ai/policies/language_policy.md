# Language Policy

## Main Rule

This project is user-facing Russian, but internally technical identifiers use English.

## English-Only Technical Layer

Use English for:

- folder names;
- file names;
- TypeScript identifiers;
- JSON keys;
- IDs;
- enum values;
- action types;
- event types;
- schema names;
- runtime/core terminology.

Examples:

- `GameState`
- `Action`
- `Event`
- `PieceDefinition`
- `PieceInstance`
- `MapDefinition`
- `ScenarioDefinition`
- `move_piece_requested`
- `piece_moved`
- `space-a`
- `piece-1`

## Russian User-Facing Layer

Use Russian for:

- UI labels;
- buttons;
- tooltips;
- user messages;
- visible names;
- help text;
- documentation for the Russian-speaking project owner.

Examples:

- `Карта`
- `Фишки`
- `Сценарий`
- `Журнал событий`
- `Фишка перемещена`

## JSON Rule

JSON keys and IDs must be English.

Display values may be Russian.

Good:

```json
{
  "spaceId": "space-a",
  "name": "Точка A"
}
```

Bad:

```json
{
  "идТочки": "точка-а"
}
```

## Documentation Rule

Existing Russian planning docs do not need mass translation.

New docs may be written in Russian, but canonical technical terms should be preserved in English when important.

Example:

Состояние игры (`GameState`) не должно храниться в Phaser.

## No Transliteration

Avoid mixed/transliterated names like:

- `tochka`
- `svyaz`
- `fishka`
- `karta`
- `move_fishka_requested`

Use canonical English terms instead:

- `space`
- `connection`
- `piece`
- `map`
- `move_piece_requested`

## Non-Goals

Do not mass-translate existing planning docs.

Do not rename existing files only for language cleanup.

Do not implement i18n/localization system in this policy step.
