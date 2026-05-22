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
