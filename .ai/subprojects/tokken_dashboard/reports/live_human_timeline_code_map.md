# Live Human Timeline Code Map

## 1. Summary — Ключевая находка

Raw rollout содержит **435 `function_call` + 435 `function_call_output`** событий с полными данными (tool_name, command, call_id, workdir, exit_code), но [`_build_live_steps()`](scripts/codex_token_monitor_server.py:887) их **полностью игнорирует**, обрабатывая только `message` и `reasoning` типы.

**Статистика событий в сыром rollout (019e9d3e):**
| Тип события | Количество |
|---|---|
| response_item/function_call | 435 |
| response_item/function_call_output | 435 |
| event_msg/token_count | 240 |
| response_item/message | 217 |
| response_item/reasoning | 205 |
| response_item/custom_tool_call | 53 |
| response_item/custom_tool_call_output | 53 |
| event_msg/patch_apply_end | 32 |
| event_msg/context_compacted | 9 |

**Структура function_call:**
```json
{
  "timestamp": "2026-06-06T14:02:54.679Z",
  "type": "response_item",
  "payload": {
    "type": "function_call",
    "name": "shell_command",
    "arguments": "{\"command\":\"Get-Content -Raw 'C:\\\\...\\\\handoff-jkd38_r7.md'\",\"workdir\":\"D:\\\\...\",\"timeout_ms\":10000}",
    "call_id": "call_UJhcibqO3O7h2wVNT5BdB08a"
  }
}
```

---

## 2. Live source data flow

| Stage | File | Function | Input | Output |
|---|---|---|---|---|
| Config | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `load_config()` (108) | `config/codex_token_monitor_projects.json` | config dict |
| Threads | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_read_threads_from_sqlite()` (597) | `state_5.sqlite` | thread rows |
| Index | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_read_session_index()` (622) | `session_index.jsonl` | name map |
| Rollout paths | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_get_live_rollout_summaries()` (690) | `sessions/**/rollout-*.jsonl` | summaries dict |
| Raw events | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_read_rollout_jsonl()` (725) | rollout paths | `list[dict]` |
| Session detail | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `build_live_session_detail()` (750) | source + session_id | detail JSON |
| **Step building** | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | **`_build_live_steps()` (887)** | raw events | `(steps, timeline_events)` |
| API | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_handle_session()` (1345) | source_id + session_id | `/api/session` JSON |

---

## 3. Archive source data flow

| Stage | File | Function |
|---|---|---|
| Discovery | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `discover_archive_sessions()` (188) |
| Detail | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `build_archive_session_detail()` (339) |
| Step | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_build_step()` (463) |
| Archive state | [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `load_archive_state()` / `save_archive_state()` (158-168) |

---

## 4. Backend live functions — detailed

| File | Function | Line | Processes function_call? |
|---|---|---|---|
| [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_read_rollout_jsonl()` | 725 | Reads ALL — YES |
| [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_build_live_steps()` | 887 | **NO — skips function_call** |
| [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_classify_event()` | nested | **NO — only message/reasoning** |
| [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_classify_tool_use()` | nested | Never reached |
| [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_build_agent_activity()` | nested | Receives classified items |
| [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py) | `_extract_text_activity_items()` | nested | Only text |

### Почему _build_live_steps игнорирует function_call

В цикле событий проверяется `pl.get("role")` для определения `is_user`/`is_assistant`. `function_call` имеет `payload.type == "function_call"` но **не имеет `payload.role`**. Поэтому событие проходит цикл без обработки.

---

## 5. Frontend functions

| File | Function | Line |
|---|---|---|
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | `loadSessionDetail()` | ~138 |
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | `renderSteps()` | ~1862 |
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | `openStepPopup()` | ~1118 |
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | `buildPopupTimeline()` | ~1156 |
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | `buildStepExportData()` | ~835 |
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | `buildSessionExportJson()` | ~845 |
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | `buildSessionExportMarkdown()` | ~871 |
| [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js) | `buildAgentActivityMarkdown()` | ~780 |

---

## 6. Tests

| File | Test class |
|---|---|
| [`tests/test_codex_token_monitor_server.py`](tests/test_codex_token_monitor_server.py) | `TestLiveChatFixture`, `TestStepFullCostAccountingV21`, `TestAgentActivityBreakdownV22` |
| [`tests/test_codex_token_monitor_audit.py`](tests/test_codex_token_monitor_audit.py) | `TestRunAudit`, `TestAuditV21StepFullCostAccounting`, `TestTruthRegression` |

---

## 7. Tool event metadata audit

| Field | In raw rollout | Preserved in step JSON | Rendered in UI |
|---|---|---|---|
| `function_call.name` | YES (435) | **NO** | **NO** |
| `function_call.arguments` | YES | **NO** | **NO** |
| `function_call.call_id` | YES | **NO** | **NO** |
| `function_call_output` | YES (435) | **NO** | **NO** |
| `command` (shell) | In arguments | **NO** | Only text mining |
| `workdir` | In arguments | **NO** | Only env |
| `exit_code` | In output | **NO** | **NO** |
| `output_preview` | In output | **NO** | **NO** |
| `last_token_usage` | YES (240) | YES | YES |

---

## 8. Where data is lost

1. **`_build_live_steps()` event loop** — проверяет `pl.get("role")`; `function_call` не имеет role → пропускается
2. **`_classify_event()`** — не обрабатывает `function_call`/`function_call_output`
3. **`call_id` связь** — не используется для связи call→output
4. **Frontend** — получает только text-based activity, не получает tool events

---

## 9. Recommended next slice

1. Capture `function_call`/`function_call_output` в `_build_live_steps()` → `live_tool_events`
2. Classify: `Get-Content`→file_read, `python -m unittest`→test_run, `git`→git_operation
3. Link tool events to nearest `request_usage_item` via event_index
4. Build `human_timeline` from tool events + AI calls
5. Render in popup

---

## 10. Files to edit later

**Backend:** [`scripts/codex_token_monitor_server.py`](scripts/codex_token_monitor_server.py)
**Frontend:** [`static/codex-token-monitor/app.js`](static/codex-token-monitor/app.js)
**Tests:** [`tests/test_codex_token_monitor_server.py`](tests/test_codex_token_monitor_server.py)
**Docs:** [`.ai/subprojects/tokken_dashboard/`](.ai/subprojects/tokken_dashboard/)