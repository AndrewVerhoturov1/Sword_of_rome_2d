# Архитектура

## Главный принцип

Сначала строим универсальные editor/runtime capabilities, потом через них собираем Sword of Rome-like тестовый модуль.

## Основные компоненты

- `Project context layer` — канон, референсы, workflow и решения в `canon/`, `references/`, `docs/`, `.ai/`.
- `Authoring/runtime layer` — будущий product code для карты, spaces, connections, counters, scenarios, JSON save/load.
- `Prototype layer` — локальные эксперименты в `arena-prototype-launcher/`, `_local/` и `output/Arena tests/`.

## Поток данных

1. Сначала фиксируем правила, контекст и принятые решения в публичном слое repo.
2. Затем реализуем editor/runtime capabilities как отдельные универсальные функции.
3. Потом собираем конкретный Sword of Rome-like модуль поверх этих capabilities.

## Архитектурные правила

- Не хардкодить проект как "одна игра"; держать фокус на reusable authoring tool.
- Публичный контекст должен быть удобен для внешнего чата и GitHub-навигации.
- Локальные прототипы и Kilo-runtime артефакты не смешивать с каноном и product-facing материалами.
