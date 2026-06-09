# V2 Preview: live_tool_events + human_timeline (handoff 0051)

## Status: preview (не push)

Это `/v2 preview` — snapshot текущего WIP для внешнего senior review.
Push в `review/v2/...` НЕ выполнялся. Жду явного подтверждения.

---

## Что сделано

Реализован захват `function_call`/`function_call_output` из raw rollout Codex и построение человеческой хронологии работы в Codex Token Monitor.

### Файлы этого slice (только мои правки)

| Файл | Строк изменено | Суть |
|---|---|---|
| [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | ~200 | `_classify_shell_command()`, захват в event loop, `live_tool_events`, `human_timeline`, `technical_ai_calls` |
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | ~60 | Хронология в popup, тех. AI-таблица, Markdown export |

### Что НЕ менялось

- `full_step_cost` / `full_step_usage` семантика
- Archive path
- Pricing
- Audit logic
- `index.html`, `styles.css`

---

## Проблема: «В мониторе нет этого»

Пользователь сообщает, что изменения не видны в интерфейсе монитора.

### Возможные причины

1. **Не перезапущен сервер** — `codex_token_monitor_server.py` читается при старте. Без рестарта backend-изменения не применяются.

2. **Кэш браузера** — `app.js` мог закэшироваться. Нужен hard reload (Ctrl+Shift+R) или очистка кэша.

3. **Структура raw rollout** — `function_call` события могут быть вложены иначе, чем ожидается в коде. Мой парсинг: `ev["payload"]["type"] == "function_call"`. Если реальная структура отличается, события не захватываются.

4. **`current_step is None`** в момент function_call — если событие приходит между `finalize_current_step` и созданием нового `current_step` (например, между task_complete и следующим task_started), оно теряется.

### Что нужно проверить внешнему ревьюверу

1. Корректен ли парсинг `response_item` с `payload.type == "function_call"` для формата Codex rollout?
2. Правильно ли выбрано место в event loop для захвата (после `is_user`/`is_assistant`, до token_count)?
3. Корректно ли связывание `tool_call → tool_output` по `call_id`?
4. Не теряет ли `current_step = None` события между шагами?
5. Правильно ли фронтенд читает `agent_timeline.items[].display_title_ru` (а не `action_title_ru`)?

---

## Ключевые точки в коде для ревью

### Backend: захват function_call

```python
# scripts/codex_token_monitor_server.py, event loop _build_live_steps()
is_function_call = (outer_type == "response_item" and pl.get("type") == "function_call")
is_function_output = (outer_type == "response_item" and pl.get("type") == "function_call_output")

if current_step and (is_function_call or is_function_output):
    tool_event = {
        "event_index": global_event_index,
        "timestamp": str(ev.get("timestamp", "")),
    }
    if is_function_call:
        tool_name = str(pl.get("name", ""))
        call_id = str(pl.get("call_id", ""))
        args_str = str(pl.get("arguments", "{}"))
        args = json.loads(args_str) if args_str.startswith("{") else {}
        command = str(args.get("command", ""))
        classification = _classify_shell_command(command)
        # ... fill tool_event
    else:
        call_id = str(pl.get("call_id", ""))
        output_text = str(pl.get("output", pl.get("text", pl.get("result", ""))))
        # ... fill tool_event
    current_step["_live_tool_events"].append(tool_event)
```

### Backend: классификатор shell_command

```python
def _classify_shell_command(command: str) -> dict:
    cmd_lower = command.strip().lower()
    if "get-content" in cmd_lower:
        return {"classified_action": "file_read", "title_ru": "Прочитал контекст проекта", ...}
    if any(kw in cmd_lower for kw in ("rg ", "select-string", ...)):
        return {"classified_action": "code_search", "title_ru": "Искал по коду", ...}
    if any(kw in cmd_lower for kw in ("python -m unittest", "pytest", ...)):
        return {"classified_action": "test_run", "title_ru": "Запустил тесты", ...}
```

### Backend: human_timeline builder

```python
# В _build_agent_activity():
# 1. Группировка tool events в batch по batch_group
# 2. Для каждого request_usage_item — поиск ближайшей предшествующей tool-группы
# 3. Построение human_timeline_items с типами: tool_with_cost, ai_call_only, action_only
# 4. Построение technical_ai_calls — отдельная таблица всех AI-обращений
```

### Frontend: рендеринг хронологии

```javascript
// В buildAgentActivityBlock():
tlItems.forEach(function(it) {
  var displayTitle = it.display_title_ru || it.recognized_action_ru || '—';
  var aiLabel = it.linked_model_request_index ? '#' + it.linked_model_request_index : '—';
  // ... рендеринг строки с колонками: #, Время, Действие, Объекты, AI, Cost, Нов. input, Output, Δt, Увер.
});
```

---

## Safety checklist

| Пункт | Статус |
|---|---|
| Тесты (109/109) | пройдены |
| `full_step_cost` не затронут | да |
| Archive path не затронут | да |
| Pricing не затронуто | да |
| `node --check app.js` | пройден |
| `python -c "import py_compile"` server.py | пройден |
| Push в GitHub | не выполнялся |
| Коммит | не выполнялся |

### Файлы, которые пойдут в review branch (если push одобрен)

```
scripts/codex_token_monitor_server.py   (только мои правки)
static/codex-token-monitor/app.js       (только мои правки)
```

### Файлы, которые НЕ пойдут

```
scripts/codex_token_monitor_audit.py    (чужие правки)
tests/*                                  (чужие правки)
.ai/subprojects/tokken_dashboard/*      (чужие правки)
.ai/logs/bug_journal.md                 (чужие правки)
.ai/plans/sessions/*                    (чужие правки)
```

---

## Вопросы к пользователю

1. Перезапускали ли вы сервер (`python scripts/codex_token_monitor_server.py`) после правок?
2. Делали ли hard reload браузера (Ctrl+Shift+R)?
3. Видите ли вы в консоли браузера (F12 → Console) ошибки JavaScript?
4. В ответе `/api/session` для 019e9d3e есть ли поле `live_tool_events` в шагах?

**Если ответы «да» на 1-2 и поле `live_tool_events` пустое** — проблема в backend-парсинге raw rollout.

**Если поле `live_tool_events` заполнено, но UI не показывает** — проблема во фронтенде (кэш, ошибка JS).

---

## /v2 push gate

Для push в `review/v2/handoff-0051-live-tool-events` нужно явное «да» от пользователя.

Пока: **preview only, push не выполнялся.**
