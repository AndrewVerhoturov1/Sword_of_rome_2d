# Notebook Entry

- External Question ID: `V1-20260523-052757`
- Entry status: `staged`
- Provider/Model: `Anthropic / Claude Sonnet 4.6`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-052757_architectural-second-opinion-po-dekompozitsii-produkta-browser-based.md`

## Context Links

- `нет`

## Candidate Navigation Entry

Topic: Architectural second opinion по декомпозиции продукта (browser-based 2D wargame authoring tool)
Summary: Вывод: 2-layer модель недостаточна; рекомендована 4-layer модель (Core Infrastructure → Universal Authoring → Runtime/Play Engine → Module Layer). Ключевой промежуточный слой — Runtime/Play Engine с `RulesHooksInterface` как буферным швом между universal и module-specific. Перечислены 14 модулей верхнего уровня, 8 архитектурных рисков и 7 planning steps в правильном порядке.

## Raw Response

## External Question ID

V1-20260523-052757

---

## Context Readback

- `external_chat_rules.md` (raw URL, central core): fully read
- `repo_navigation.md` (raw URL, central core): fully read
- `project_brief.md` (project-specific, raw URL): fully read
- `architecture.md` (project-specific, raw URL): fully read
- `project_state.md` (project-specific, raw URL): fully read
- `decisions.md` (project-specific, raw URL): fully read
- `sword_of_rome_web_project_context.md` (project-specific, raw URL): fully read
- `repo_navigation.md` (project-specific, Sword_of_rome_2d): **not read** — ссылка передана в prompt, но не открывалась отдельно, так как project brief и architecture уже дали достаточно контекста
- `README.md` (project-specific, Sword_of_rome_2d): **not read** — не открывался, достаточного контекста получено из других файлов
- Context Excerpts (inline в prompt): fully read

---

## Provider/Model

Anthropic / Claude Sonnet 4.6

---

## Answer

### Confirmed from provided excerpts + project-specific documents

*(Следующий раздел опирается на project_brief.md, architecture.md, project_state.md, decisions.md и sword_of_rome_web_project_context.md — все прочитаны полностью.)*

---

### Problem Framing

Продукт — браузерный 2D authoring tool для создания и плейтеста counter-based варгеймов с point-to-point картой. Sword of Rome-like модуль — первый тестовый проект внутри инструмента, а не сам инструмент. Архитектурная задача: правильно разделить universal capabilities (reusable на любой модуль) и module-specific layer (контент и правила конкретной игры), не перепутав их на старте, пока product code ещё не написан.

Из canon уже зафиксировано: tech stack Phaser 3 + React + TypeScript + Zustand + Zod, два режима (Designer / Play Mode), модель «GameState как источник истины — Phaser только рендерит», три типа файлов (map.json / scenario.json / savegame.json), будущая серверная модель getView / getAllowedActions / applyAction.

---

### Recommended Layer Stack

**Нужна 4-layer модель, а не 2-layer.**

Гипотеза из двух слоёв правильна по направлению, но смешивает внутри «editor layer» две разные вещи, а внутри «project layer» — ещё две. Как только начнётся реализация Play Mode или правил, швы сразу дадут о себе знать.

Правильный разрез — 4 слоя:

```
Layer 4 │ Module Content + Module Rules
        │  (game-specific data + game-specific logic)
────────┼──────────────────────────────────────────────
Layer 3 │ Runtime / Play Engine
        │  (game-agnostic execution infrastructure)
────────┼──────────────────────────────────────────────
Layer 2 │ Universal Authoring / Editor Capabilities
        │  (creation + editing tools, game-agnostic)
────────┼──────────────────────────────────────────────
Layer 1 │ Core Infrastructure
        │  (engine integration, event bus, persistence)
```

Два внутренних слоя (1 и 2) вместе образуют то, что ты назвал «universal editor layer». Их надо разделить, потому что Layer 1 — это платформа без предметной логики, а Layer 2 — это уже authoring-инструменты с понятиями «пространство», «фишка», «deck». Это разные уровни абстракции.

Layer 3 (Runtime) — это **промежуточный слой, которого нет в 2-layer модели, но он критичен**. Без него нет чистого способа отделить «инфраструктуру исполнения» от «правил конкретной игры». Если его пропустить, правила Sword of Rome начнут просачиваться в GameState и ActionModule.

---

### Module Breakdown

**Layer 1 — Core Infrastructure** *(universal)*

| Модуль | Purpose | Owns | Dependencies | Universal? |
|---|---|---|---|---|
| `RenderEngine` | Phaser-React интеграция, camera, canvas | Phaser scene lifecycle, BoardScene, camera | — | universal |
| `InputPipeline` | Drag/drop, snap, click, multi-select, pan/zoom | Input events, snap logic, selection state | RenderEngine | universal |
| `EventBus` | Внутренняя шина событий между слоями | Typed event stream | — | universal |
| `PersistenceModule` | Save/load, JSON schemas, validation | Zod schemas, import/export, versioning | GameState (Layer 3) | universal |

**Layer 2 — Universal Authoring Capabilities** *(universal)*

| Модуль | Purpose | Owns | Dependencies | Universal? |
|---|---|---|---|---|
| `MapAuthoringModule` | Создание и редактирование карт, spaces, connections | Space graph, connection graph, map metadata | Layer 1 | universal |
| `PieceAuthoringModule` | Определение типов фишек, размещение, стеки | Piece definitions, piece instances, stack logic | MapAuthoringModule | universal |
| `DeckAuthoringModule` | Создание колод и карт событий | Card definitions, deck definitions, hand state | — | universal |
| `ScenarioAuthoringModule` | Начальные расстановки, стартовые состояния | Scenario files, initial placement | Map + Piece + Deck modules | universal |
| `DesignerModeTools` | Свободная манипуляция всем, Developer Map Mode | Dev-time overlays, coordinate editor, debug tools | все authoring modules | universal |
| `DocumentsModule` | Правила, памятки, pinned windows | Document registry, pin state, window positions | — | universal |

**Layer 3 — Runtime / Play Engine** *(universal infrastructure)*

| Модуль | Purpose | Owns | Dependencies | Universal? |
|---|---|---|---|---|
| `GameStateModule` | Авторитетное состояние игры | GameState, state transitions | Layer 1 | universal |
| `ActionModule` | Диспетчер действий, action log, event stream | Action types, action log, undo/replay basis | GameState | universal |
| `RulesHooksInterface` | **Абстрактный интерфейс** для правил модуля | `getAllowedActions()`, `validateMove()`, `checkWinCondition()`, `getPhaseActions()` — stub/noop по умолчанию | GameState, ActionModule | universal (interface) |
| `PhaseTrackerModule` | Фреймворк фаз и ходов | Phase sequence framework, current phase state | GameState, RulesHooksInterface | universal (framework) |
| `PlayModeEnforcer` | Ограничение действий в Play Mode | Mode state, action gating | GameState, RulesHooksInterface | universal |
| `ServerBridgeStub` | Заготовка под future server | `getView()`, `applyAction()` signatures | GameState | universal |

**Layer 4 — Module Layer** *(project-specific)*

| Модуль | Purpose | Owns | Dependencies | Universal? |
|---|---|---|---|---|
| `[ModuleName]Content` | Игровые данные конкретного модуля | map.json, scenario.json, piece definitions, faction definitions, card data | все universal modules | **project-specific** |
| `[ModuleName]Rules` | Реализация правил конкретного модуля | Имплементация `RulesHooksInterface`: movement constraints, combat resolver, win conditions, phase sequence, faction hooks | `RulesHooksInterface` (Layer 3) | **project-specific** |

Для Sword of Rome-like: `SwordOfRomeContent` + `SwordOfRomeRules`.

---

### Universal vs Project-Specific Split

**Universal (Layers 1–3 + RulesHooksInterface):**
- Вся платформа рендеринга и ввода
- Все authoring tools (map editor, piece editor, deck editor, scenario editor)
- Designer Mode как таковой
- GameState model + ActionModule + ActionLog
- Phase tracker framework (без конкретной sequence)
- Save/load + Zod schemas
- Интерфейс правил (пустые хуки по умолчанию)
- Documents/windows система

**Project-specific (Layer 4):**
- Конкретные JSON-данные: map.json, scenario.json, piece/faction definitions
- Конкретные ассеты (карта Италии, графика фишек)
- Имплементация `RulesHooksInterface`: правила движения, боевая механика, фазовая последовательность, victory conditions
- Модульные UI-расширения (если нужны faction-specific панели)
- Карточные эффекты и event card logic

**Граница:** `RulesHooksInterface` — это буферный шов между слоями 3 и 4. Всё, что ниже интерфейса — universal. Всё, что его реализует — module-specific. Это граница должна быть явно задокументирована до начала кода.

---

### Нужен ли промежуточный слой между Editor и Specific Project?

**Да, Layer 3 (Runtime / Play Engine) — именно он.**

Без него: все правила, проверки и фазы начнут просачиваться в GameState или в authoring tools. Designer Mode и Play Mode превратятся в одну свалку с нарастающими `if (mode === 'play')` проверками везде.

С ним: editor (Layer 2) знает только как **создавать** объекты; runtime (Layer 3) знает только как **исполнять** действия в рамках any interface; rules (Layer 4) знают только **правила конкретной игры**.

---

### Architectural Risks

**1. Editor/Runtime blur (главный риск).** Play Mode logic окажется в Designer Mode tools или наоборот. Без явного разделения Layer 2 / Layer 3 это происходит незаметно, через `if (isPlayMode)` внутри authoring tools.

**2. Phaser как источник истины.** Уже зафиксировано в canon, но риск остаётся при реализации: удобно хранить gameObject.data прямо в Phaser sprite. Этот паттерн разрушает всю архитектуру при первой же попытке sync/undo.

**3. Hardcoded Sword of Rome в universal modules.** Конкретные faction IDs («rome», «samnite»), типы connection («appian_way»), типы пространств попадут в универсальные схемы как «временно хардкод». Это прорастёт везде.

**4. Отсутствие RulesHooksInterface на старте.** Если не определить пустой интерфейс сразу, первые же правила Sword of Rome будут написаны прямо в GameStateModule или ActionModule, и выдернуть их оттуда потом очень дорого.

**5. Schema drift без версионирования.** GameState.version не ставят на старте, думая «разберёмся потом». После первых же save файлов становится невозможно их читать при изменении схемы.

**6. Over-engineering editor в v0.1.** Попытка сделать «полноценный universal editor» до первого модуля. Правило: editor capabilities строятся ровно настолько, насколько нужно для Table Sandbox 0.1 плюс один шаг вперёд.

**7. Фазовая логика просочилась в client.** AllowedActions начинают проверяться на клиенте напрямую, без абстракции. Когда появится сервер, вся эта логика окажется в двух местах.

**8. Смешение map.json и scenario.json.** Если пространства и стартовая расстановка фишек оказались в одном файле — при смене карты или сценария всё нужно переписывать.

---

### Recommended Next Planning Steps

1. **Зафиксировать 4-layer модель в `architecture.md`** — добавить Layer 1–4 с описанием responsibilities. Не код, только текст.

2. **Определить `RulesHooksInterface` в `architecture.md` или отдельном doc** — список методов-заглушек (`getAllowedActions`, `validateMove`, `onPhaseStart`, `checkWin`). Даже пустой stub как контракт.

3. **Задокументировать Module Boundaries** — для каждого модуля: что он owns, что ему запрещено знать (explicit «NOT IN scope»). Это предотвращает erosion границ.

4. **Зафиксировать схемы данных для v0.1**: `GameState`, `map.json`, `scenario.json`, `savegame.json` — структуры, обязательные поля, версия. Это через Zod.

5. **Определить объём Table Sandbox 0.1** — явный список: какие модули из breakdown входят в первый milestone, какие нет. Сейчас scope v0.1 описан в контексте, но не отражён в architecture.md как module-level boundary.

6. **Инициализировать product-code структуру (src/)** — skeleton папок под модули без реализации. Только структура, достаточная для первого authoring block.

7. **Первый product-code block: Layer 1 + MapAuthoringModule skeleton** — Phaser scene bootstrap, camera, map image loading, space rendering из sampleMap.json.

---

### Not available / not verified

- `repo_navigation.md` (project-specific, Sword_of_rome_2d) — не читался отдельно; навигация по project repo не проверялась.
- `README.md` (project-specific) — не читался; возможно содержит дополнительный контекст по структуре папок.
- Текущее состояние product code — per `project_state.md`, его практически нет; architectural proposal опирается на это допущение. Если уже есть prototip код в `arena-prototype-launcher/` с другими решениями — это может скорректировать слои.
- Детали card-driven mechanics для будущего карточного движка не анализировались — это Layer 4 territory, за горизонтом v0.1.

---

## Candidate Navigation Entry

V1-20260523-052757: Architectural second opinion по декомпозиции продукта (browser-based 2D wargame authoring tool). Вывод: 2-layer модель недостаточна; рекомендована 4-layer модель (Core Infrastructure → Universal Authoring → Runtime/Play Engine → Module Layer). Ключевой промежуточный слой — Runtime/Play Engine с `RulesHooksInterface` как буферным швом между universal и module-specific. Перечислены 14 модулей верхнего уровня, 8 архитектурных рисков и 7 planning steps в правильном порядке.
