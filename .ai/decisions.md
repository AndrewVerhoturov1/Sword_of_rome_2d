# Журнал решений

## `2026-05-22` — `Authoring tool first`

### Контекст

Проект легко спутать с веб-адаптацией Sword of Rome, но фактическая цель шире: создать редактор и рабочий стол для 2D counter-based варгеймов.

### Решение

Считать Sword of Rome-like модуль первым тестовым модулем внутри универсального authoring tool, а не единственным продуктом.

### Причины

- Это даёт правильный architectural focus на reusable capabilities.
- Это лучше согласуется с уже существующим контекстом и прототипами.

### Последствия

- Канон, архитектура и roadmap должны описывать editor/runtime platform, а не "одну игру".
- Конкретные игровые материалы держим как test module/reference layer.

### Статус

`Принято`

## `2026-05-22` — `Public repo with visible V1 history and hidden Kilo runtime`

### Контекст

Половина дальнейшей работы планируется через внешние чаты. Им нужна удобная GitHub-навигация и видимая история прошлых `/v1` вопросов. При этом Kilo runtime-мусор не должен попадать в публичную плоскость.

### Решение

Публиковать `.ai/external_chats/V1_navigation.md` и `.ai/external_chats/notebook/`, но не публиковать `.ai/handoffs/`, `.ai/reports/`, `.ai/plans/sessions/` и runtime-папки external route.

### Причины

- Внешнему чату нужен накопленный контекст.
- Внутренний execution noise мешает навигации и засоряет repo.

### Последствия

- `.gitignore` обязан жёстко разделять public и local-only workflow-слои.
- Repo navigation должен явно вести внешнего чата в V1 history.

### Статус

`Принято`

## `2026-05-23` — `4-layer product architecture with rules hook boundary`

### Контекст

После двух `/v1` second opinion по architectural decomposition (`V1-20260523-052756` и `V1-20260523-052757`) стало ясно, что грубая `2-layer` модель полезна только как стартовая интуиция, но недостаточна для product planning.

Главная проблема 2-layer framing:

- внутри `editor layer` смешиваются infrastructure, data model и authoring tools;
- внутри `project-specific layer` смешиваются content и rules;
- отсутствует явный universal runtime/play layer как буфер между editor и конкретной игрой.

### Решение

Для product code принять `4-layer` архитектуру:

1. `Core Infrastructure + Project/Data Model`
2. `Universal Authoring / Editor Capabilities`
3. `Universal Runtime / Play Sandbox`
4. `Module Package`

Внутри `Module Package` явно разделять:

- `Module Content`
- `Module Rules/Hooks`

Между universal runtime и module-specific rules ввести явный boundary-контракт:

`RulesHooksInterface`

Также явно держать разделение:

- `map.json`
- `scenario.json`
- `savegame.json`

### Причины

- Это не даёт Sword of Rome-like модулю превратиться в hardcoded центр всей платформы.
- Это сохраняет Phaser в роли renderer, а не source of truth.
- Это создаёт чистый шов между universal runtime и module-specific behavior.
- Это снижает риск смешивания editor-логики и play-логики.
- Это лучше готовит платформу к later server-authoritative architecture.

### Последствия

- `.ai/architecture.md` должен описывать именно `4-layer` модель и module boundaries.
- Первый product-code skeleton должен следовать этим слоям, а не начинаться как "одна игра".
- `RulesHooksInterface` нужно отдельно зафиксировать до начала substantive product-code implementation.
- `Table Sandbox 0.1` должен планироваться как набор universal modules, а не как первый hardcoded Sword of Rome runtime.

### Статус

`Принято`
