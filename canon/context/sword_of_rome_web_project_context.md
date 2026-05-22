# Контекст проекта для Codex: Sword of Rome Web Vassal 0.1

Самое главное:
Я понял тебя так:

Ты делаешь **не цифровую версию “Меча Рима”**, а **конструктор / редактор / мастерскую для создания подобных варгеймов**.

“Меч Рима” в этой логике — не цель проекта, а **тестовый полигон**:

> У меня есть знакомая игра со сложной, понятной мне структурой. Я использую её как пример, чтобы проверить, что мой конструктор реально умеет собирать такие игры.

То есть правильный порядок разработки не такой:

> “Сделать карту Меча Рима → сделать фишки Меча Рима → сделать правила Меча Рима”

А такой:

> “Сделать инструмент для добавления карты → через него собрать карту Sword of Rome-like”
> “Сделать инструмент для создания фишек → через него создать римские/самнитские/греческие фишки”
> “Сделать редактор spaces/connections → через него разметить Италию”
> “Сделать редактор карт событий → через него собрать card-driven модуль”
> “Сделать сценарный редактор → через него собрать стартовую расстановку”

То есть каждый элемент должен сначала появляться как **универсальная возможность конструктора**, а уже потом применяться к конкретному модулю.

Я бы зафиксировал это как главный принцип:

**Мы строим не игру, а authoring tool для создания 2D counter-based варгеймов. Sword of Rome-like модуль — это первый тестовый проект внутри этого инструмента.**

Практически это меняет первый milestone. Он должен быть не просто `Table Sandbox 0.1`, а скорее:

**Developer Table Sandbox 0.1**

С фокусом на инструменты:

* добавить карту как объект на стол;
* менять размер карты;
* двигать карту;
* вращать карту, если нужно;
* закреплять / откреплять карту;
* добавлять spaces поверх карты;
* редактировать coordinates, radius, name, type;
* создавать connections;
* добавлять counters;
* двигать counters;
* сохранять всё в JSON;
* загружать обратно;
* затем на этом собрать маленький Sword of Rome-like пример.

То есть “Меч Рима” становится **не хардкодом**, а первым сохранённым проектом/модулем, созданным через редактор.



## 1. Что это за проект

Проект — браузерная 2D-платформа для разработки и плейтеста фишечных настольных варгеймов.

Первый практический модуль — веб-адаптация в духе **Sword of Rome / Меч Рима**, но в версии 0.1 это не полноценная автоматизированная цифровая игра, а **умный браузерный стол**: карта, точки, связи, фишки, стеки, режим разработчика, лог действий, сохранение/загрузка и подготовка к будущему онлайну.

Идея проекта не в том, чтобы сразу создать коммерческую или публичную цифровую версию чужой игры. Модуль Sword of Rome-like используется как **учебный и закрытый прототип**, потому что игра хорошо известна автору, имеет проверенную структуру и хороший набор механик для построения универсального движка: point-to-point карта, фракции, лидеры, контроль областей, города, лояльность, осады, карты, фазы, дипломатия, победные очки.

Долгосрочная цель — создать свой инструмент для разработки настольных варгеймов: нечто среднее между Vassal, Rally the Troops и лёгкой компьютерной игрой, где игроки сохраняют ручную свободу настольного стола, а компьютер постепенно берёт на себя рутину: подсчёты, проверки, логи, сохранения, подсказки, автоматизацию фаз и анализ плейтестов.

## 2. Главный milestone

Текущий утверждённый milestone:

**Sword of Rome Web Vassal 0.1 / Table Sandbox 0.1**

Фокус версии 0.1 — не карточный движок и не полные правила, а именно **2D-стол**:

- новая перерисованная карта в духе Sword of Rome;
- point-to-point spaces;
- off-map boxes, если они являются игровыми зонами;
- связи между spaces;
- фишки;
- стеки;
- drag-and-drop;
- примагничивание фишек к ближайшему space;
- контекстные меню;
- лог действий;
- режим разработчика;
- save/load состояния в JSON;
- архитектура, готовая к будущему серверу и онлайну.

Пока НЕ делаем:

- полную автоматизацию всех правил;
- карточный движок;
- боевой резолвер;
- ИИ;
- полноценный онлайн;
- публичный релиз с чужими ассетами;
- мобильную версию;
- сложный редактор всего на свете.

## 3. Почему сначала стол, а не карты

Изначально обсуждался карточный движок по примеру Twilight Struggle, но было принято решение начинать со стола.

Причина: для фишечного варгейма главный объект — состояние на карте:

- где стоят силы;
- кто контролирует пространства;
- какие пространства связаны;
- где находятся города;
- где возможны перемещения;
- где создаются стеки;
- какие точки являются родными для фракций;
- какие элементы можно выбрать и перетащить.

Карточный движок станет полезен только тогда, когда есть интерактивная карта, принимающая действия. Поэтому порядок разработки:

1. 2D table sandbox;
2. map data layer;
3. pieces and stacks;
4. save/load;
5. developer mode;
6. room sync / server later;
7. phase tracker later;
8. card engine later;
9. assisted rules later.

## 4. Основные референсы

Из всех обсуждённых референсов оставлены только два ключевых:

### 4.1. Twilight Struggle Digital

Полезно для будущего карточного движка:

- карта как основной экран;
- card-driven flow;
- у карты несколько способов использования;
- компактный лог;
- онлайн/асинхронность;
- понятный выбор действия при клике на карту.

Но это НЕ фокус версии 0.1.

### 4.2. Rally the Troops

Главный архитектурный референс на будущее:

- браузерный формат;
- игра по ссылке;
- сервер как источник истины;
- rules engine отдаёт игроку player-specific view;
- клиент показывает только разрешённые действия;
- action log как основа replay/undo/sync;
- async и live play.

В версии 0.1 сервер может ещё не существовать, но модель данных надо проектировать так, чтобы потом перейти к Rally-like архитектуре.

## 5. Технологический стек

Принятое решение:

```txt
Phaser 3 — игровой стол и runtime
React — внешний UI вокруг стола
TypeScript — основной язык
Vite — сборка
Zustand — client state / UI state
Zod — схемы и валидация JSON
позже Node.js/Fastify + WebSocket — онлайн-комнаты
```

Ранее рассматривался Konva.js. Konva хорош для canvas-редакторов, но автор уже делает браузерную RTS на Phaser, поэтому Phaser выбран как более практичный runtime-движок.

Главное правило: **Phaser не является источником истины**.

Истина живёт в `GameState`, JSON и событиях. Phaser только отображает состояние и превращает ввод пользователя в action/event.

Правильная модель:

```txt
GameState -> Phaser renders board
User input -> Action/Event -> GameState changes -> Phaser updates
```

Неправильная модель:

```txt
Phaser sprites сами хранят истинное состояние игры
```

## 6. Предлагаемая структура проекта

```txt
src/
  game/
    PhaserGame.ts
    scenes/
      BootScene.ts
      BoardScene.ts
    systems/
      CameraSystem.ts
      SelectionSystem.ts
      DragSystem.ts
      SnapSystem.ts
      StackSystem.ts
      OverlaySystem.ts
      LabelSystem.ts
      ConnectionSystem.ts
    objects/
      PieceSprite.ts
      SpaceMarker.ts
      ConnectionLine.ts

  state/
    gameStore.ts
    events.ts
    actions.ts

  data/
    schemas.ts
    sampleGame.json
    sampleMap.json
    sampleScenario.json

  ui/
    App.tsx
    RightPanel.tsx
    LogPanel.tsx
    ContextMenu.tsx
    StackViewer.tsx
    Toolbar.tsx
    DocumentWindow.tsx
    PinnedAidWindow.tsx

  types/
    game.ts
    map.ts
    pieces.ts
    events.ts
```

## 7. Визуальная модель: карта лежит на столе

Принята концепция: не бесконечная карта, а **карта-лист на цифровом столе**.

Визуально:

```txt
HTML/CSS table background
  -> Phaser transparent canvas
      -> map sheet shadow
      -> map sheet / border
      -> raster map image
      -> spaces / labels / connections
      -> pieces / markers / overlays
```

Зачем:

- игрок понимает, где заканчивается карта;
- камера может улетать за край карты;
- вокруг карты есть “стол” для воздуха и временного пространства;
- не нужно бесконечно дорисовывать море/сушу по краям;
- фон стола можно сделать лёгким CSS, а не огромным растром.

### 7.1. Стол

Стол вокруг карты лучше делать через HTML/CSS, а не большим изображением.

Варианты:

- CSS gradients;
- зелёное сукно;
- дерево;
- пергаментный стол;
- маленькая tileable noise texture 128–512 px;
- vignette через CSS.

Не надо делать `table_background_10000x14000.png`.

### 7.2. Что рисует Phaser

Phaser отвечает за всё, что должно двигаться и зумиться вместе с камерой:

- лист карты;
- тень листа;
- саму карту;
- точки/spaces;
- названия;
- связи;
- фишки;
- стеки;
- маркеры контроля;
- подсветки;
- off-map boxes, если они являются игровыми зонами.

### 7.3. Что рисует React/HTML

React/HTML отвечает за внешний интерфейс:

- toolbar;
- боковые панели;
- лог;
- модальные окна;
- окна правил и памяток;
- настройки;
- контекстные меню, если удобнее делать их HTML-слоем;
- pinned documents.

## 8. Арт-пайплайн карты

Оригинальную карту Sword of Rome не используем как финальный арт. Делается новая карта с нуля.

Принятый подход:

1. сгенерировать чистую основу карты в AI;
2. выбрать стиль;
3. при необходимости убрать/ослабить горы;
4. увеличить изображение локально через tiled upscale, например Flux;
5. доработать в Photoshop;
6. оставить карту как растровую high-res подложку;
7. игровые данные хранить отдельно в JSON и рисовать через Phaser.

Полная векторизация всей карты больше не считается обязательной. Для выбранного мягкого illustrated map style растровая карта может быть лучше, чем векторизация, потому что векторизация может испортить градиенты, мягкие берега, море и текстуры.

Принято:

```txt
растровая high-res карта = арт-подложка
JSON data layer = игровые точки, связи, боксы, города, контроль
Phaser overlay = визуализация игровых объектов
```

Векторными/программными должны быть:

- точки;
- связи;
- названия;
- иконки;
- маркеры;
- интерфейс;
- overlay-слои.

Растровыми могут быть:

- море;
- суша;
- текстуры;
- мягкий рельеф;
- декоративная подложка.

## 9. Карта: что запекать в изображение, а что рисовать программно

### 9.1. В base map raster запекаем

- географию;
- море;
- сушу;
- береговую линию;
- рельеф/текстуру;
- декоративную атмосферу.

Карта должна быть почти “немой”.

### 9.2. Через Phaser рисуем

- игровые точки / spaces;
- названия settlements/spaces;
- связи между spaces;
- home faction rings;
- current control markers;
- city icons;
- port icons;
- siege/rebel markers;
- hover/selection highlights;
- debug ids;
- координаты в Developer Mode;
- route overlays.

Почему не запекать названия и области в карту:

- проще локализация;
- можно менять язык;
- можно менять размер шрифта при зуме;
- можно включать/выключать labels;
- можно показывать debug ids;
- можно править названия без Photoshop;
- Play Mode и Designer Mode могут показывать разные слои.

Базовое правило:

**география запечена в карту, игровые данные рисуются Phaser-слоями.**

## 10. Spaces и point-to-point карта

Основной тип карты — point-to-point.

Все точки важны и должны быть размечены. На первом этапе не нужны провинции как большие окрашиваемые области. Нужны spaces, connections, control markers и stacks.

Пример структуры space:

```ts
type FactionId = "rome" | "greek" | "gaul" | "samnite" | "carthage" | "neutral";

type Space = {
  id: string;
  nameKey: string;
  x: number;
  y: number;
  radius: number;
  kind: "normal" | "city" | "walled_city" | "tribal" | "port" | "box";
  homeFaction?: FactionId;
  control?: FactionId;
  victorySpace?: boolean;
  port?: boolean;
  city?: CityState;
};
```

## 11. Home faction и current control

Очень важное решение: надо различать родную область и текущий контроль.

```ts
type Space = {
  homeFaction?: FactionId;
  control?: FactionId;
};
```

`homeFaction` — чья это родная область.

`control` — кто контролирует сейчас.

Потеря своей родной области даёт болезненный штраф/минус очки. Потеря чужой родной области не даёт такого штрафа.

Пример:

```json
{
  "id": "capua",
  "homeFaction": "rome",
  "control": "samnite"
}
```

Это значит:

- Capua — родная область Рима;
- сейчас её контролируют самниты;
- Рим получает штраф за потерю родной области;
- самниты не получают штраф за потерю Capua, потому что это не их родная область.

Визуально:

- outer ring / colored outline = home faction;
- small marker / flag / inner token = current control.

## 12. Connections

Связи между spaces должны храниться как отдельные объекты графа.

Пример:

```ts
type ConnectionKind =
  | "normal"
  | "rough"
  | "mountain"
  | "strait"
  | "appian_way"
  | "special";

type Connection = {
  id: string;
  from: string;
  to: string;
  kind: ConnectionKind;
};
```

Морские пути в первой версии не делаем. Всё кроме морского пути можно заложить уже сейчас как типы connections.

Даже если линии будут визуально нарисованы Phaser-слоем, логика движения использует `connections`, а не пиксели.

## 13. Города

Принята простая человеческая модель:

**Space — место, где стоят армии и фишки. City — состояние города внутри этого space.**

Город не обязательно отдельный space. Он может быть вложенным объектом в space.

```ts
type CityState = {
  loyalty: 1 | 2 | 3;
  wallLevel: 1 | 2 | 3;
  rebellious: boolean;
  besieged: boolean;
};
```

Пример:

```json
{
  "id": "rome",
  "kind": "city",
  "homeFaction": "rome",
  "control": "rome",
  "city": {
    "loyalty": 3,
    "wallLevel": 3,
    "rebellious": false,
    "besieged": false
  }
}
```

В UI это должно отображаться понятно:

- значок города;
- цифра 1/2/3;
- значок мятежа;
- значок осады;
- справа в inspector panel: loyalty, walls, rebellious, besieged.

## 14. Фишки и стеки

Фишка должна хранить не координаты как истину, а location.

```ts
type Piece = {
  id: string;
  type: "combat_unit" | "leader" | "marker" | "control" | "city";
  owner: FactionId;
  location: string; // spaceId or boxId
  faceUp: boolean;
  rotation?: number;
  selected?: boolean;
};
```

Неправильно:

```json
{ "pieceId": "rome_cu_1", "x": 642, "y": 1180 }
```

Правильно:

```json
{ "pieceId": "rome_cu_1", "location": "rome" }
```

Координаты нужны только для отрисовки. Если несколько фишек имеют один `location`, они формируют стек.

В версии 0.1 stacking limits не проверяем. Разработчик и игроки могут класть сколько угодно фишек в одно место. Ограничения появятся позже в Play Mode.

Визуализация стека в 0.1:

- несколько фишек в одной точке рисуются лесенкой/веером;
- клик по стеку открывает StackViewer;
- можно выбрать отдельную фишку;
- можно перетащить всю стопку или отдельную фишку — точное поведение можно уточнить при реализации.

## 15. Перемещение

В Table Sandbox 0.1:

- фишки можно свободно перетаскивать;
- по умолчанию drop примагничивается к ближайшему space;
- для разработчика нужен режим свободного размещения без snap;
- позже Play Mode будет проверять перемещение по правилам.

Варианты управления:

```txt
обычный drag -> snap к ближайшему space
Alt + drag -> free placement / no snap
Shift + click -> multi-select
right click -> context menu
```

Действие перемещения должно логироваться как event:

```ts
type PieceMovedEvent = {
  type: "piece_moved";
  pieceId: string;
  from: string;
  to: string;
  by?: string;
  timestamp: number;
};
```

## 16. Режимы работы

Нужно два режима:

### 16.1. Designer Mode

Режим разработчика/модератора. Можно делать всё:

- двигать любые фишки куда угодно;
- менять контроль;
- менять homeFaction;
- добавлять/удалять фишки;
- создавать/двигать spaces;
- создавать connections;
- редактировать города;
- менять параметры фишек;
- открывать скрытую информацию;
- откатывать действия;
- экспортировать JSON.

Table Sandbox 0.1 фактически делаем как Designer Mode + мягкие подсказки.

### 16.2. Play Mode

Будущий режим партии:

- действия ограничены текущей фазой;
- нельзя двигать чужие фишки;
- нельзя менять контроль без действия;
- нельзя нарушать правила движения;
- приватная информация скрыта;
- действия идут через allowed actions;
- сервер позже становится источником истины.

## 17. Developer Map Mode

Нужен встроенный dev-редактор карты, потому что координаты и связи будут постоянно уточняться.

Минимальные функции:

- загрузить карту;
- zoom/pan;
- показывать координаты курсора в map coordinates;
- Ctrl+click -> создать space;
- drag space -> изменить координаты;
- inspector для id/name/homeFaction/control/type;
- выбрать два spaces -> создать connection;
- выбрать тип connection;
- import/export map.json;
- включить debug ids;
- включить/выключить labels/connections/home/control overlays.

## 18. Импорт координат точек

Обсуждались три способа разметки точек.

### 18.1. Контрастные круги на изображении

Автор может в Photoshop нарисовать маленькие солидные круги контрастного цвета в центрах spaces.

Скрипт может найти центры таких кругов, если:

- цвет уникальный, например `#ff00ff`;
- круги не пересекаются;
- размер примерно одинаковый;
- на карте нет других похожих пятен.

Минус: скрипт найдёт координаты, но не поймёт названия. Потом в Developer Map Mode нужно вручную назначить id.

### 18.2. SVG/Figma/Inkscape слой

Лучший вариант для точности: отдельный слой circles, где каждый circle имеет id/name. Экспорт в SVG, скрипт читает `cx/cy/id`.

### 18.3. Встроенный редактор

Самый гибкий вариант: ставить и править точки прямо в приложении.

Предпочтительный pipeline:

```txt
новая карта -> быстрый импорт точек -> ручная правка в Developer Map Mode -> export map.json
```

## 19. Памятки, правила и документы

Таблицы и памятки не должны занимать место на карте. Всё это выносится в интерфейс.

Нужен UI-модуль документов:

- кнопка Rules;
- кнопка Player Aid;
- кнопка Tables;
- кнопка Cards Reference later;
- окно документа;
- возможность прикрепить документ “скрепкой”;
- pinned windows можно двигать, менять размер, сворачивать, закрывать;
- положения pinned windows сохраняются локально для игрока.

По умолчанию правила и памятки скрыты.

## 20. Action log

Лог действий нужен уже в Table Sandbox 0.1.

Минимальные события:

- piece_moved;
- piece_created;
- piece_deleted;
- control_changed;
- space_created;
- space_updated;
- connection_created;
- dice_rolled later;
- note_added later.

Пример:

```ts
type GameEvent =
  | { type: "piece_moved"; pieceId: string; from: string; to: string; timestamp: number }
  | { type: "control_changed"; spaceId: string; from: FactionId; to: FactionId; timestamp: number }
  | { type: "space_created"; spaceId: string; timestamp: number };
```

Лог должен быть не просто UI-историей, а будущей основой для:

- undo;
- replay;
- debugging;
- online sync;
- playtest analysis.

## 21. Save / Load

Состояние должно сохраняться в JSON.

Минимальная структура:

```ts
type GameState = {
  metadata: {
    gameId: string;
    version: string;
  };
  map: MapState;
  pieces: Record<string, Piece>;
  log: GameEvent[];
  mode: "designer" | "play";
};
```

`map.json` и `scenario.json` лучше разделить:

- `map.json` — постоянная структура карты: spaces, connections, базовые свойства;
- `scenario.json` — стартовая раскладка: фишки, контроль, стартовые состояния;
- `savegame.json` — конкретное состояние партии.

## 22. Будущая серверная архитектура

В версии 0.1 можно начать с локального single-page prototype. Но проектировать надо так, будто позже будет сервер.

Будущая модель:

```ts
getView(gameState, playerId) -> PlayerView
getAllowedActions(gameState, playerId) -> AllowedActions
applyAction(gameState, playerId, action) -> GameState
```

Клиент не должен сам решать правила. Клиент должен отправлять action request.

В будущем:

```txt
client action request
-> server validates
-> server updates state
-> server appends event log
-> server sends new player views
-> Phaser redraws board
```

## 23. Карточный движок позже

Карточный движок не входит в Table Sandbox 0.1, но надо помнить будущую модель.

Каждая карта должна быть объектом с несколькими режимами использования:

```ts
type CardMode =
  | "event"
  | "ops"
  | "political_support"
  | "reinforcement"
  | "response"
  | "discard";
```

Пример будущей карты:

```json
{
  "id": "rome_001",
  "faction": "rome",
  "title": "Example Card",
  "ops": 2,
  "type": "strategy",
  "timing": ["active_player_action"],
  "modes": ["event", "ops", "political_support", "reinforcement"],
  "responseWindow": null,
  "removeIfEvent": false,
  "automation": "manual",
  "tags": ["military"]
}
```

Но это позже.

## 24. Что можно прототипировать отдельно

Были предложены мини-прототипы, которые можно делать в сервисах вроде arena.ai или отдельно:

1. цифровой стол: CSS table + map sheet + panels;
2. drag/drop + snap + stacks;
3. Developer Map Mode;
4. context menu;
5. right-side inspector panel;
6. pinned player aid windows;
7. action log;
8. save/load JSON;
9. dynamic labels;
10. homeFaction vs currentControl visualization.

Это можно использовать как UX-референсы, но основной код проекта должен быть в нормальном репозитории.

## 25. Юридический и контентный подход

Важно не использовать публично оригинальные copyrighted assets без разрешения.

Принято:

- движок — наш;
- Sword of Rome-like module — закрытый прототип/учебный модуль;
- карта — новая, перерисованная с нуля;
- ассеты — временные или свои;
- публичная демонстрация — только на абстрактном sample game или после разрешения правообладателя.

## 26. Ближайший план работ для Codex

Первый набор задач:

### 26.1. Bootstrap

- создать Vite + React + TypeScript проект;
- подключить Phaser 3;
- встроить Phaser canvas в React layout;
- сделать CSS table background;
- сделать transparent Phaser canvas или корректную интеграцию canvas поверх HTML-фона.

### 26.2. BoardScene

- загрузить placeholder map image;
- отрисовать map sheet с тенью;
- реализовать camera zoom/pan;
- отображать координаты курсора в map coordinates.

### 26.3. Map data layer

- определить Zod-схемы для spaces/connections/map;
- загрузить sampleMap.json;
- отрисовать spaces как circles;
- отрисовать labels;
- отрисовать connections;
- добавить toggles для labels/connections/debug.

### 26.4. Pieces

- определить Piece type;
- загрузить sample pieces;
- отрисовать фишки как sprites/circles/placeholders;
- реализовать drag;
- реализовать snap to nearest space;
- логировать перемещение.

### 26.5. Stacks

- если несколько pieces в одном location, рисовать stack offset/fan;
- click stack -> открыть StackViewer;
- выбрать конкретную фишку.

### 26.6. UI

- toolbar: Designer Mode / Play Mode placeholder, Save, Load;
- right inspector panel;
- log panel;
- context menu for piece and space;
- pinned aid/document window placeholder.

### 26.7. Save/load

- export current GameState to JSON;
- import GameState from JSON;
- validate через Zod;
- show validation errors.

## 27. Критически важные правила реализации

1. Не хранить истину в Phaser sprites.
2. Не запекать игровые labels/spaces/connections в raster map.
3. Все игровые объекты должны иметь id.
4. Фишки стоят в `location`, а не просто в `x/y`.
5. UI действия должны превращаться в events/actions.
6. GameState должен быть сериализуемым в JSON.
7. Разделять `map`, `scenario` и `savegame`.
8. Designer Mode должен быть свободным.
9. Play Mode позже будет ограничивать действия правилами.
10. Архитектура должна быть готова к серверу, даже если сервер появится позже.

## 28. Короткое описание проекта одной фразой

**Браузерный Phaser + React инструмент для создания и плейтеста point-to-point фишечных варгеймов: сначала как ручной Vassal-like стол для Sword of Rome-like модуля, затем как полуавтоматический движок с правилами, картами, логом, онлайн-комнатами и редакторскими инструментами.**
