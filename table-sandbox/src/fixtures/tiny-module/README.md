# Tiny Canonical Fixture Seed

Это крошечный canonical fixture seed для **Table Sandbox 0.1**.

Это **не** настоящий игровой модуль. Это минимальный data-only seed,
используемый следующим шагом `Runtime/Data Bootstrap` для загрузки
начального `GameState`.

## Структура

| Файл | Роль |
|------|------|
| `project.json` | Индекс workspace/project |
| `modules/tiny-module/module.json` | Manifest модуля + компактные `factions[]` и `pieceDefinitions[]` (временная политика `0.1`) |
| `modules/tiny-module/map.json` | Только topology карты (spaces, connections, zones) |
| `modules/tiny-module/scenario.basic.json` | Только initial setup (turnState, pieces, control, variables) |
| `modules/tiny-module/rules.metadata.json` | Только declarative metadata (поддерживаемые actions/events, фазы) |
| `saves/savegame.empty.json` | Runtime/save артефакт: зеркало initial setup + пустой `eventLog` |

## Границы

- **Definitions** (что это за модуль, карта, фишки, фракции) — в `module.json`, `map.json`.
- **Initial setup** (стартовая раскладка) — в `scenario.basic.json`.
- **Declarative rules metadata** (какие actions/events/phases поддерживаются) — в `rules.metadata.json`.
- **Runtime/save state** (текущее состояние партии, event log) — в `savegame.empty.json`.

`savegame.empty.json` не дублирует определения карты, фишек или фракций —
он содержит только runtime snapshot и ссылается на версии определений.

## Использование

Этот fixture seed загружается на следующем шаге `Runtime/Data Bootstrap`
для создания начального `GameState` и проверки цепочки
`Action -> Event -> GameState -> render -> save/load`.
