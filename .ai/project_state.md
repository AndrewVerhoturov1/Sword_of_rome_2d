# Project State

## Дата обновления

`2026-05-22`

## Текущий этап

`Bootstrap workflow + normalizing repository structure for future GitHub publication`

## Что уже сделано

- Разложен базовый публичный контекст по `canon/`, `references/`, `docs/`.
- Установлен workflow `Codex + Kilo Code` из central `ai-workflow-core`.
- Выделены local-only зоны: `arena-prototype-launcher/`, `_local/`, `output/Arena tests/`.

## Что внедряется сейчас

- Публичная навигация repo для внешних чатов.
- Подготовка репозитория к первой нормальной публикации в GitHub.

## Текущие риски

- Часть прототипов всё ещё лежит в `output/Arena tests/`; это локальный архив, не канон проекта.
- Архитектура самого игрового/editor runtime ещё не разложена на product-code модули, потому что repo пока содержит в основном контекст и прототипные материалы.

## Следующие задачи

1. Зафиксировать, какие материалы становятся каноном, а какие остаются идеями.
2. Инициализировать Git-репозиторий и опубликовать публичный слой.
3. Начать формировать первый product-code block для editor sandbox.
