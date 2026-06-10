V2 ID: V2-20260609-121400

Ты в V2 External Senior Review.

## Required Central Rules
https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md

## Вопрос: несоответствие токенов в UI

Этап #9 — file_read. UI показывает:

```
app.js | read | Размер вывода: 2 889 | ~Токенов: ~722 | Доля: 50%
```

При этом AI-call #9 имеет:
```
Output: 149 | Reasoning: 79
```

Пользователь спрашивает: почему у файла ~722 токенов, а у AI output 149?

## Код
server.py: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/2584229a67b24f48b5fbe17795b73d3d2bf934d1/scripts/codex_token_monitor_server.py

Смотри `_make_context_contribution` (~1790) и `buildTimelineItemDetails` в app.js.

## Вопрос
Это баг (неправильный расчёт токенов) или корректное поведение (tool output chars ≠ model output tokens)? Объясни различие.

Формат: V2 ID / Context Readback / Provider / Answer / Nav Entry
