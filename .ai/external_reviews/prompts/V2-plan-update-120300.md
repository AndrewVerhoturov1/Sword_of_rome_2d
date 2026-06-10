V2 ID: V2-20260609-120300

Ты в V2 External Senior Review. Snapshot кода дан.

## Required Central Rules
https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md

## Проблема: plan_update explanation/items пустые

Этап #4 показывает "Обновил план работы" + note, но без explanation и plan items. Raw rollout содержит эти данные.

## Код

server.py snapshot: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/2584229a67b24f48b5fbe17795b73d3d2bf934d1/scripts/codex_token_monitor_server.py

Проверь цепочку передачи данных plan_update:

1. function_call parser (~3086): `pl.get("arguments")` → dict или строка? `isinstance(raw_args, dict)` проверка.
2. `_classify_service_call` (~1084): правильные ключи? `plan`/`items`/`plan_items`. Codex может использовать другой ключ.
3. `.update(classification)` на tool_event — все ли поля передаются?
4. Linker: `te_copy = dict(te)` сохраняет кастомные поля.
5. Enrichment (~1896): `te.get("plan_explanation")` в ev_map.

НАЙДИ ТОЧНЫЙ РАЗРЫВ. Ответ: V2 ID / Context Readback / Provider / Answer (location + cause + fix) / Nav Entry.
