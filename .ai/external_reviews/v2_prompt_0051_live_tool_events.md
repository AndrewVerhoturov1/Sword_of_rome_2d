# V2 External Review Prompt — handoff 0051

## Контекст

Ты делаешь code review для Codex Token Monitor — browser-based инструмента, который парсит raw rollout-логи Codex и показывает cost/usage сессий.

## Задача этого slice

Реализован захват `function_call`/`function_call_output` из raw rollout Codex и построение человеческой хронологии работы. Раньше монитор показывал только «Скрытое обращение Codex к AI #N», теперь должен показывать реальные действия: «Прочитал контекст проекта», «Запустил тесты», «Проверил изменения в Git».

## Review branch

https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/tree/review/v2/handoff-0051-live-tool-events

## Файлы для ревью (только 2)

1. [`scripts/codex_token_monitor_server.py`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/blob/review/v2/handoff-0051-live-tool-events/scripts/codex_token_monitor_server.py) — backend
2. [`static/codex-token-monitor/app.js`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/blob/review/v2/handoff-0051-live-tool-events/static/codex-token-monitor/app.js) — frontend

Коммит: `5664bb8`

## Что изменилось

### Backend (`_build_live_steps()`)

Добавлен захват событий `response_item` с `payload.type == "function_call"` и `"function_call_output"`, которые раньше полностью игнорировались (event loop смотрел только на `payload.role`).

Новая функция `_classify_shell_command()` классифицирует shell-команды:
- `Get-Content` → `file_read` / `file_read_batch`
- `rg`, `Select-String` → `code_search`
- `python -m unittest` → `test_run`
- `git status/diff` → `git_operation`
- `node --check` → `syntax_check`

Захваченные события попадают в `step.live_tool_events`. Затем в `_build_agent_activity()` строится `human_timeline`:
- tool-события группируются в batch (несколько чтений файлов → одна группа)
- каждая группа привязывается к ближайшему последующему AI-обращению
- стоимость не дублируется
- AI-обращения без tool-событий получают fallback «Осмыслил промежуточный контекст»
- Техническая таблица `technical_ai_calls` содержит все AI-обращения отдельно

### Frontend (`buildAgentActivityBlock()`)

- Таблица хронологии переименована: «Хронология работы»
- Добавлена колонка «AI» с номером привязанного обращения
- Исправлен баг: использовалось `action_title_ru` (несуществующее поле), теперь `display_title_ru`
- Добавлена сворачиваемая таблица «Технические AI-обращения»
- Обновлён Markdown export: секции «Человеческая хронология работы», «Что означает AI #», «Технические AI-обращения»

## Проблема

Пользователь сообщает: «В мониторе нет этого» — изменения не видны в интерфейсе.

## Что нужно проверить

1. **Парсинг function_call**: корректен ли `ev["payload"]["type"] == "function_call"` для реального формата Codex rollout? Может ли `function_call` быть вложен иначе?

2. **Место в event loop**: не теряются ли события из-за `current_step is None`? Между `finalize_current_step` и созданием нового шага есть окно. Между `task_complete` и `task_started` тоже.

3. **Связывание call_id**: tool_call и tool_output связываются по `call_id`. Всегда ли он присутствует и совпадает?

4. **Batch-группировка**: несколько `Get-Content` перед одним AI-вызовом объединяются эвристически по `batch_group = "project_context"`. Достаточно ли этого? Не теряются ли одиночные чтения?

5. **Фронтенд**: правильно ли читается `display_title_ru` из JSON? Не кэшируется ли старый `app.js`?

6. **Общая архитектура**: правильный ли подход — захват function_call в том же event loop, где обрабатываются message/reasoning/token_count?

## Ожидаемый ответ

Развёрнутое code review с конкретными замечаниями по каждому из 6 пунктов. Если находишь баг — укажи точную строку и предложи исправление.
