# Notebook Entry

- External Question ID: `V1-20260523-055021-2`
- Entry status: `staged`
- Provider/Model: `not available (DeepSeek)`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-055021-2_domain-model-razdelyaet-immutable-definitions-mapdefinition-piecedefinition-scenariodefinition.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_brief.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/canon/context/sword_of_rome_web_project_context.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md`

## Candidate Navigation Entry

Topic: Domain model разделяет immutable definitions (MapDefinition, PieceDefinition, ScenarioDefinition) и mutable runtime state (PieceInstance, SaveGameState)
Summary: File contract включает project.json, module.manifest, map.json, scenario.json, savegame.json. Главные риски: смешение definition/instance, Phaser как источник истины, нарушение границ слоёв. Следующий шаг — Glossary + JSON Schema + Rules Hook Contract.

## Raw Response

## External Question ID
V1-20260523-055021-2

## Context Readback
- https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md: fully read
- https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md: fully read
- https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md: fully read
- https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_brief.md: fully read
- https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/project_state.md: fully read
- https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md: fully read
- https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md: fully read
- https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/canon/context/sword_of_rome_web_project_context.md: fully read
- https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/README.md: fully read

## Provider/Model
not available (DeepSeek)

## Answer

### Domain Framing
Проект — это **браузерная 2D-платформа для создания и запуска настольных/табличных сценариев** (authoring tool + runtime sandbox). Не одна игра, а инструмент, где модули (игровые системы, кампании, наборы правил) являются контентом.  
**Границы domain**:
- Authoring time: определение карт, фишек, стеков, сценариев, правил.
- Runtime time: исполнение сценария по правилам модуля, управление состоянием партии.
- Source of truth — JSON-модели (GameState, Action/Event log), Phaser — только визуализация.
- Модули изолированы через RulesHooksInterface; ядро не знает внутренней логики модуля.
- Состояние сохраняется в трёх типах файлов: статическая карта, сценарий (начальные условия + логика), сохранённая партия.

### Core Entities

| Сущность | Роль |
|----------|------|
| **Project** | Корневой контейнер всего содержимого редактора (набор модулей, карты, сценарии, настройки). |
| **Module** | Единица контента + правил. Имеет манифест, директорию content (определения) и rules (хуки). |
| **ModuleManifest** | Метаданные модуля: id, версия, зависимости, точки входа в RulesHooksInterface. |
| **MapDefinition** | Статическая топология (граф узлов/клеток, связи, типы тайлов). |
| **PieceDefinition** | Шаблон фишки (тип, внешний вид, свойства по умолчанию). Immutable. |
| **PieceInstance** | Экземпляр фишки в конкретной сессии (позиция, владелец, текущие модификаторы). |
| **ScenarioDefinition** | Начальное состояние партии: какие PieceInstance где лежат, стартовые параметры, привязка к MapDefinition и Module. |
| **SaveGameState** | Полный снапшот runtime-состояния: текущий ход, история действий, изменённые PieceInstance, флаги сценария. |
| **Action** | Намерение игрока/системы (переместить, взять, применить правило). Проходит валидацию через RulesHooksInterface. |
| **Event** | Факт, произошедший в рантайме (порождается действием или системой). Историчен, неизменяем. |
| **RulesHook** | Функция, реализуемая модулем и вызываемая ядром в строго определённых точках (см. RulesHooksInterface). |

### File Contract

| Файл | Purpose | Что хранится | Что **не** хранится | Owner layer |
|------|---------|--------------|---------------------|--------------|
| `project.json` | Манифест всего проекта | Список модулей (id, версии, активен ли), глобальные настройки редактора, ссылка на активную карту и сценарий по умолчанию | Состояние сессии, определения модулей (они в своих папках) | Layer 1 (Project/Data Model) |
| `modules/<module_id>/module.manifest` | Описание модуля | id, версия, dependencies, entry point для правил (rules.bundle.js), автор, лицензия | Контент модуля (карты, фишки) | Layer 4 (Module Package) |
| `modules/<module_id>/content/` | Определения модуля | PieceDefinition, кастомные ассеты, кастомные карты (если модуль расширяет картографию) | Правила, рантайм-состояние | Layer 4, Module Content |
| `modules/<module_id>/rules/` | Код/метаданные правил | RulesHooksInterface implementation, rules_config.json (опционально) | Определения контента | Layer 4, Module Rules |
| `maps/<map_id>.json` | Статическая карта | Узлы, рёбра, типы тайлов, размеры, мета-информация (автор, версия) | Позиции фишек, сценарные триггеры | Layer 1/2 (Project+Authoring) |
| `scenarios/<scenario_id>.json` | Начальное состояние сценария | Ссылка на map_id, список начальных PieceInstance (со ссылками на PieceDefinition), стартовые переменные, привязка к module_id | История действий, текущий ход | Layer 2 (Authoring) |
| `saves/<savegame_id>.json` | Сохранённая партия | Текущий GameState (позиции, модификаторы, очередь ходов, журнал событий), ссылка на scenario_id, дата, метаданные | Определения фишек (они в content) | Layer 3 (Runtime) |
| (optional) `rules_config.json` внутри `rules/` | Доп. метаданные для UI редактора | Какие действия разрешены в какой фазе, названия фаз, иконки для AuthoringTools | Логика валидации | Layer 4 Module Rules |

### Entity Ownership By Layer

- **Layer 1 (Core Infrastructure + Project/Data Model)**: Project, ModuleManifest (базовый контракт), ссылочная целостность между сущностями.
- **Layer 2 (Universal Authoring)**: MapDefinition, ScenarioDefinition, PieceDefinition (через AssetBoardModule), редактирование всех definition-сущностей.
- **Layer 3 (Universal Runtime)**: PieceInstance runtime state, SaveGameState, Action/Event журнал, текущий GameState.
- **Layer 4 (Module Package)**: Module content (конкретные PieceDefinition, кастомные карты) + Module rules (реализация хуков). Владеет только своими определениями, не владеет runtime-состоянием.

### Definitions vs Runtime State

| Immutable definitions | Mutable runtime state |
|-----------------------|------------------------|
| MapDefinition | PieceInstance (позиция, владелец, стек, current HP и т.п.) |
| PieceDefinition (тип фишки) | Scenario runtime variables (флаги, счётчики) |
| Module content (ассеты, шаблоны) | SaveGameState (включая журнал событий) |
| ScenarioDefinition (начальные условия как шаблон) | Текущий игрок, фаза, очередь действий |
| Project manifest | — |

**Важно**: PieceInstance в SaveGameState ссылается на PieceDefinition по id. Изменение PieceDefinition не должно ломать существующие сохранения (версионирование).

### Validation Rules And Invariants

1. **Unique ids глобально**: project-wide, но для PieceDefinition достаточно уникальности в рамках модуля (`module_id:def_id`).
2. **Reference integrity**: Каждый PieceInstance в scenario.json или savegame.json должен ссылаться на существующий PieceDefinition. Каждый scenario.json — на существующий map.json и module.
3. **Versioning**: Поля `schema_version` в каждом JSON-файле. При миграции — совместимость по major/minor.
4. **Layer ownership boundaries**:
   - Authoring layer не читает и не пишет savegame.json.
   - Runtime layer не изменяет definitions (map, piece definitions).
   - Module rules не имеют прямого доступа к DOM/Phaser, только к GameState через RulesHooksInterface.
5. **Action/Event separation**: Action всегда содержит `type`, `payload`, `source` (playerId/system). Event — action + `timestamp`, `result` (успех/неудача), `newStateHash` (опционально). Журнал событий append-only.
6. **Map consistency**: В map.json все рёбра ссылаются на существующие узлы. Граф должен быть связным (или допустимы изолированные области — оговаривается).
7. **Savegame snapshot**: Должен содержать полное состояние, чтобы не зависеть от оригинального scenario.json (который мог измениться после сохранения).

### Data Model Risks

1. **Смешивание definition и instance** — например, хранение позиции фишки в PieceDefinition. → Нарушит работу нескольких сценариев на одной карте.
2. **Нарушение source of truth (Phaser как истина)** — приведёт к рассинхрону JSON и отрисовки. Запрещено.
3. **Жёсткая связь модуля с глобальными типами действий** — модуль должен определять свои действия через хуки, а не жёсткие коды.
4. **Отсутствие хуков или неполный контракт** — сделает невозможным любую модульную логику побед/фаз/ограничений.
5. **Нарушение границ слоёв** — authoring инструменты, изменяющие runtime state, сломают предсказуемость.
6. **Избыточная нормализация** (например, отдельная таблица для каждого атрибута) — усложнит сохранение и отладку. JSON-документы допустимо денормализованы.
7. **Отсутствие версионирования** — сломает все сохранения при обновлении модуля.
8. **Сериализация функций/правил в JSON** — недопустимо. Правила живут как JS-бандлы, в JSON только метаданные.

### Recommended Next Planning Artifact

После этого domain/data contract следующим шагом должен быть **триплет документов**:

1. **Glossary** (термины: Piece, Stack, Node, Edge, Phase, Action, Event, Hook, Module, Sandbox) — единый язык для команды.
2. **JSON Schema спецификация** для каждого файла из File Contract (project.json, module.manifest, map.json, scenario.json, savegame.json) с примерами.
3. **Rules Hook Contract** — точная сигнатура и семантика каждой функции RulesHooksInterface (getAllowedActions, validateAction, onPhaseStart, checkWinCondition и др.), включая передаваемые объекты (GameState, Action, PlayerRef).

Альтернативно — **milestone breakdown**, но он будет сырым без этих спецификаций. Поэтому порядок: Glossary → Schemas → Hook Contract → Breakdown.

### Not available / not verified

- В явном виде не указано, поддерживаются ли **стеки фишек** и как именно их модель вписывается в PieceInstance (одна фишка vs стопка). Принято, что есть PiecesStacksModule, но детали стека (порядок, верхняя фишка) остаются открытыми. Рекомендуется добавить в PieceInstance поля `stackId` и `stackPosition`, либо сделать Stack сущностью первого класса.
- Не уточнён механизм **зависимостей между модулями** (может ли Module A расширять определения Module B). В манифесте нужно поле `dependencies`, но правила разрешения конфликтов (например, версий) пока не определены.
- Какой **формат action/event** для журнала — пока абстрактный. В следующем шаге (Hook Contract) это должно быть конкретизировано.

## Candidate Navigation Entry
Domain model разделяет immutable definitions (MapDefinition, PieceDefinition, ScenarioDefinition) и mutable runtime state (PieceInstance, SaveGameState). File contract включает project.json, module.manifest, map.json, scenario.json, savegame.json. Главные риски: смешение definition/instance, Phaser как источник истины, нарушение границ слоёв. Следующий шаг — Glossary + JSON Schema + Rules Hook Contract.
