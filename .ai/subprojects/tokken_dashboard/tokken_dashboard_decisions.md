# Tokken Dashboard Decisions

Slug: `tokken_dashboard`  
Owner: `Orc`  
Status: `active`  
Last updated: `2026-06-04`
Decision layer: `subproject-level accepted decisions`

## Quick Navigation

- [Purpose](#purpose)
- [Accepted Decisions](#accepted-decisions)
- [D-20260604-002](#d-20260604-002)
- [D-20260604-003](#d-20260604-003)
- [D-20260604-004](#d-20260604-004)
- [D-20260604-005](#d-20260604-005)
- [D-20260604-006](#d-20260604-006)
- [Corrected Decisions](#corrected-decisions)
- [Rejected Options](#rejected-options)
- [Waivers](#waivers)
- [Relation To Journal](#relation-to-journal)
- [Maintenance Rule](#maintenance-rule)

<a id="purpose"></a>

## Назначение

Этот файл хранит важные решения подпроекта `tokken_dashboard`.

Он нужен, чтобы быстро понять:

- какая локальная OTel-практика уже подтверждена;
- что не сработало и не должно считаться baseline;
- какие ограничения по безопасности уже обязательны;
- какой порядок ведения документации считается рабочим.

<a id="accepted-decisions"></a>

## Accepted subproject decisions

<a id="d-20260603-001"></a>

### D-20260603-001 - Подпроект ведется как локальный OTel-only baseline без облаков

- Status: `accepted`
- Source: `user request + smoke-test result`
- Decision: `tokken_dashboard` фиксирует только локальные способы получения OTel/telemetry данных от Codex без подключения внешних сервисов.
- Reason: цель подпроекта - сначала научиться безопасно получать сырые данные локально и не отправлять ничего наружу.
- Consequence: любые следующие шаги внутри baseline должны оставаться локальными, без Grafana Cloud, SigNoz Cloud, LangSmith или других внешних приемников.
- Boundary: это решение не разрешает сразу строить dashboard или включать постоянную telemetry без отдельного human решения.
- Human approval: `recorded`

<a id="d-20260603-002"></a>

### D-20260603-002 - Рабочий baseline для Codex OTel: localhost + local OpenTelemetry Collector

- Status: `accepted`
- Source: [J-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260603-002)
- Decision: для текущего smoke-test baseline рабочим считать конфиг Codex с endpoint-ами через `http://localhost:4318/v1/logs`, `http://localhost:4318/v1/traces`, `http://localhost:4318/v1/metrics` и локальным OpenTelemetry Collector как приемником.
- Reason: именно эта комбинация реально дала входящие `Logs`, `Traces` и `Metrics` от Codex.
- Consequence: при следующей локальной проверке сначала повторять эту рабочую схему, а не возвращаться к неподтвержденным гипотезам.
- Boundary: это решение не говорит, что любой другой runtime, адрес или exporter формат тоже гарантированно сработает.
- Human approval: `recorded`

<a id="d-20260603-003"></a>

### D-20260603-003 - `log_user_prompt` должен оставаться false для локальных тестов

- Status: `accepted`
- Source: `user request + executed smoke-test`
- Decision: в локальных telemetry проверках подпроекта `log_user_prompt = false` считать обязательным безопасным минимумом.
- Reason: тест должен быть максимально безопасным и не должен расширять объем отправляемых prompt-данных.
- Consequence: если telemetry временно включается для следующей локальной проверки, этот флаг нужно держать выключенным для prompt logging.
- Boundary: это решение не гарантирует отсутствие других чувствительных полей в raw telemetry.
- Human approval: `recorded`

<a id="d-20260603-004"></a>

### D-20260603-004 - После smoke-test config возвращается в безопасное состояние

- Status: `accepted`
- Source: [J-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260603-002)
- Decision: временный `[otel]` блок после теста нужно удалять, а backup конфига сохранять.
- Reason: telemetry не должна оставаться включенной случайно после разовой диагностики.
- Consequence: рабочее состояние подпроекта после smoke-test - telemetry выключена, backup сохранен.
- Boundary: это решение не запрещает следующий локальный тест, но требует нового временного включения и нового cleanup.
- Human approval: `recorded`

<a id="d-20260603-005"></a>

### D-20260603-005 - Raw OTel file capture можно использовать как parser baseline только после privacy check

- Status: `accepted`
- Source: [J-20260603-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260603-004)
- Decision: для следующего parser/dashboard исследования рабочим локальным входом считать файл [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json), созданный через OpenTelemetry Collector `file` exporter на `localhost`.
- Reason: этот файл реально содержит `logs`, `traces`, `metrics` и token usage поля, поэтому он достаточен для разработки локального parser.
- Confirmed token fields: `input_token_count`, `output_token_count`, `cached_token_count`, `reasoning_token_count`, `tool_token_count`, `codex.turn.token_usage.*`, `gen_ai.usage.*`, `codex.usage.*`, `token_type`.
- Privacy rule: перед dashboard или долговременным хранением удалять или маскировать минимум `user.email`, `user.account_id`, `conversation.id`, `host.name` и чувствительные `authorization/cookie/api-key/password/secret` поля. `prompt_length` можно сохранять как диагностический сигнал. `prompt` можно сохранять только если значение уже пустое или `[REDACTED]`, иначе значение нужно заменять на `[REDACTED]`.
- Consequence: raw-файл можно читать локальным parser-ом, но нельзя публиковать, коммитить или показывать в dashboard без redaction.
- Boundary: `log_user_prompt = false` остается обязательным, но не считается достаточной защитой.
- Human approval: `recorded`

<a id="d-20260603-006"></a>

### D-20260603-006 - Для устойчивых правил decisions являются первичным слоем, journal только ссылается на них

- Status: `accepted`
- Source: `user instruction on 2026-06-03`
- Decision: если появляется новое устойчивое правило, baseline, запрет или waiver, сначала оно фиксируется в `tokken_dashboard_decisions.md`, а затем `tokken_dashboard_journal.md` ссылается на соответствующий `D-*`, `S-*`, `R-*` или `W-*` anchor вместо повторного пересказа правила.
- Reason: так проще читать документы, меньше дублирования и легче поддерживать один canonical decision source.
- Consequence: journal остается factual log, а decisions становятся главным местом для рабочих правил.
- Boundary: это не отменяет того, что фактическое событие и проверка все равно должны быть зафиксированы в journal.
- Human approval: `recorded`

<a id="d-20260603-007"></a>

### D-20260603-007 - Следующий допустимый этап: локальный forensics parser раньше dashboard и раньше token optimization

- Status: `accepted`
- Source: `user instruction on 2026-06-03`
- Decision: следующий этап подпроекта `tokken_dashboard` ограничивается локальным `forensics parser` для raw OTel файла. Parser читает только локальный raw input и выпускает только очищенные локальные артефакты: `clean_events.jsonl`, `token_usage.jsonl`, `spans.jsonl`, `metrics.jsonl`, `sessions.jsonl` или `session_summary.json`, `warnings.jsonl`, `diagnostic_report.md`.
- Reason: уже подтверждено, что raw OTel содержит полезные `logs`, `traces`, `metrics` и token fields, но также содержит приватные поля. Значит сначала нужен слой local parsing + redaction, а не visualization и не optimization.
- Consequence: рабочей целью следующего шага считается forensic-разбор причин перерасхода токенов по sanitized data, а не построение dashboard и не изменение поведения Codex.
- Boundary: raw OTel file не публиковать, наружу не отправлять, код приложения не менять, telemetry optimization не делать на этом этапе. Dashboard может опираться только на sanitized outputs после отдельного решения.
- Human approval: `recorded`

<a id="d-20260604-001"></a>

### D-20260604-001 - Сравнение turn cost делать как A/B эксперимент из двух режимов по три сообщения в одной session

- Status: `accepted`
- Source: `user instruction on 2026-06-04`
- Decision: следующий turn-cost эксперимент для `tokken_dashboard` делать не как три изолированных одиночных run, а как два режима: `A-current-config` и `B-minimal-config`. В каждом режиме выполнять ровно три сообщения в одной и той же session/thread: первый short no-tool turn, второй short no-tool turn, третий safe tool turn.
- Same-session rule: внутри одного режима `A1 -> A2 -> A3` и `B1 -> B2 -> B3` нельзя менять config и нельзя перезапускать Codex. Между режимами разрешен только controlled config swap + fresh restart. После restore original config нужен отдельный fresh restart.
- Reason: только такой формат позволяет увидеть baseline overhead, cache effect второго сообщения и реальную стоимость turn с инструментом без смешивания разных session.
- Consequence: compare-артефакты должны хранить не только run-level summary, но и mode/turn структуру с `turn_index`, `tool_call_status`, `cached_tokens`, `tool_mcp_activity` и флагом `same_session_reliable`.
- Boundary: не делать вывод о точных токенах конкретного инструмента. OTel показывает token usage by turn и tool/MCP activity, но не гарантирует per-tool token accounting.
- Human approval: `recorded`

<a id="d-20260604-002"></a>

### D-20260604-002 - Tool/MCP Activity Inspector строится только поверх sanitized outputs и не утверждает per-tool tokens

- Status: `accepted`
- Source: `user instruction on 2026-06-04`
- Decision: следующий диагностический слой `Tool/MCP Activity Inspector` должен читать уже готовые sanitized parser outputs и `compare_summary.json`, нормализовать Tool/MCP activity records, привязывать их к `mode/turn` best-effort через окна `window_start/window_end`, и выпускать `tool_mcp_activity.jsonl`, `tool_mcp_activity_summary.json`, `tool_mcp_activity_report.md`.
- Reason: текущий A/B результат уже показывает token deltas по turn, но нужен отдельный forensic слой, который объясняет, какая Tool/MCP активность была рядом с дорогими ходами.
- Consequence: inspector может показывать activity, counts, spans, metrics, proximity и current-vs-minimal различия, но не должен утверждать точные токены конкретного tool или MCP server.
- Boundary: не запускать новые OTel-прогоны, не менять Codex config, не читать raw OTel без необходимости, не делать dashboard, не выводить приватные значения.
- Human approval: `recorded`

<a id="d-20260604-003"></a>

### D-20260604-003 - MCP Schema Inventory работает read-only и честно фиксирует `schema_unavailable`

- Status: `accepted`
- Source: `user instruction on 2026-06-04`
- Decision: `MCP Inventory / Schema Size Report` должен использовать только read-only config metadata, sanitized compare outputs и готовый Tool/MCP activity summary. Нельзя менять `config.toml`, перезапускать Codex, запускать новые OTel-прогоны, выполнять реальные tool calls, публиковать raw config или сохранять secret values.
- Reason: A/B compare уже показал стабильный `+10.1k` input-token overhead у current config, а сам safe tool-call добавил только около `+200`. Следующий полезный вопрос - может ли статический MCP/tool schema payload объяснить этот постоянный overhead.
- Consequence: если настоящие tool schemas недоступны безопасно, отчет должен писать `schema_unavailable`, а не имитировать точный schema/token size. В этом случае config/tool-count inventory является слабым сигналом, а следующий сильный шаг - MCP group attribution через контролируемые A/B micro-runs.
- Boundary: rough token estimate = `ceil(chars / 4)`. Это не официальный tokenizer OpenAI, не billing и не per-server token accounting.
- Human approval: `recorded`

<a id="d-20260604-004"></a>

### D-20260604-004 - Effective MCP inventory нужен перед group attribution

- Status: `accepted`
- Source: `user instruction on 2026-06-04`
- Decision: перед следующим `MCP group attribution experiment` нужно явно различать `configured MCP servers`, `effective enabled MCP servers`, `explicit disabled sections` и `telemetry observed MCP servers`. Для этого `mcp_schema_inventory.py` должен выпускать отдельный `Effective MCP Inventory` audit поверх read-only [config.toml](C:/Users/andre/.codex/config.toml) и старого [compare_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/compare_summary.json).
- Reason: старый compare видел `13` observed current MCP servers, но текущий config snapshot содержит несколько `enabled = false` sections. Без этого разделения легко спутать старый observed baseline с текущим effective baseline и неверно спланировать следующий experiment.
- Consequence: новый audit обязан хранить `config_present`, `enabled_raw`, `effective_enabled`, `enabled_source`, observed flags по current/minimal telemetry и `mismatch_flags`. Если mismatch есть, следующий безопасный шаг = сначала tiny confirmation run от текущего effective config, потом уже group attribution.
- Boundary: это read-only hardening. Нельзя менять live config, запускать новый OTel, запускать Codex, запускать MCP servers, делать dashboard или broad refactor.
- Human approval: `recorded`

<a id="d-20260604-005"></a>

### D-20260604-005 - Tool environment не равен только MCP servers

- Status: `accepted`
- Source: `user instruction on 2026-06-04`
- Decision: дальнейшая диагностика token overhead должна вести отдельный учет трех слоев: `MCP servers`, `plugins` и `runtime/internal tools`. Нельзя считать, что tool environment полностью описывается только `[mcp_servers.*]`.
- Reason: physical MCP removal уже уменьшил observed MCP inventory с `13` до `3`, но selected first-turn input tokens не снизились. Значит high input cost объясняется не только пользовательскими MCP sections.
- Consequence: read-only inventory и следующие тесты должны явно показывать enabled plugins, runtime/internal candidates вроде `codex_apps` и `node_repl`, и только потом предлагать следующий A/B шаг.
- Boundary: это не разрешение сразу делать новый token run. Сначала допустим read-only inventory; следующий run только как отдельный явно выбранный шаг.
- Human approval: `recorded`

<a id="d-20260604-006"></a>

### D-20260604-006 - High input cost may include skills, instructions and auto-loaded context

- Status: `accepted`
- Source: `user instruction on 2026-06-04`
- Decision: read-only inventory РґРѕР»Р¶РµРЅ С‡РµСЃС‚РЅРѕ С‡РµСЃС‚С‚СЊ `skills`, `AGENTS.md`, repo instruction files, `.ai/**/*.md` Рё РїРѕС…РѕР¶РёРµ auto-loaded context candidates, Р° РЅРµ СЃРІРѕРґРёС‚СЊ high input cost С‚РѕР»СЊРєРѕ Рє MCP/plugins/runtime tools.
- Reason: physical MCP removal already reduced observed MCP inventory `13 -> 3`, РЅРѕ selected first-turn input tokens РЅРµ СѓРїР°Р»Рё. Р—РЅР°С‡РёС‚ overhead РјРѕР¶РµС‚ РїСЂРёС…РѕРґРёС‚СЊ РёР· auto-loaded instruction/context layers.
- Consequence: `tool_environment_inventory_summary.json` РѕР±СЏР·Р°РЅ С…СЂР°РЅРёС‚СЊ Р±Р»РѕРє `skills_and_instructions` СЃ metadata only: configured skill candidates, repo instruction files, global instruction candidates, largest files, likely auto-loaded candidates Рё warnings. Report РѕР±СЏР·Р°РЅ РґР°РІР°С‚СЊ РєРѕСЂРѕС‚РєРёР№ РІС‹РІРѕРґ, РјРѕРіСѓС‚ Р»Рё large instructions explain part of input overhead.
- Boundary: СЌС‚Рѕ РЅРµ РѕР·РЅР°С‡Р°РµС‚ РіР»СѓР±РѕРєРёР№ docs audit, РЅРµ СЂР°Р·СЂРµС€Р°РµС‚ РЅРѕРІС‹Р№ OTel, Collector, Codex run РёР»Рё dashboard.
- Human approval: `recorded`

<a id="corrected-decisions"></a>

## Superseded or corrected decisions

<a id="s-20260603-001"></a>

### S-20260603-001 - Гипотеза про `127.0.0.1` как normal baseline отменена

- Status: `corrected`
- Old rule: `127.0.0.1:4318` можно считать нормальным baseline endpoint для Codex OTel smoke-test.
- New rule: для этого подпроекта baseline считать `localhost`, а не `127.0.0.1`, пока не появится отдельное объяснение и подтверждение обратного.
- Reason: на `127.0.0.1` Codex стабильно получал `502`, хотя ручные POST доходили до локального приемника.
- Evidence: [J-20260603-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260603-001), [J-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260603-002)

<a id="rejected-options"></a>

## Rejected options

<a id="r-20260604-001"></a>

### R-20260604-001 - Сравнивать turn cost по трем отдельным одиночным run

- Status: `rejected`
- Option: мерить baseline, second turn и tool turn через отдельные независимые запуски вместо одной session на режим.
- Reason: такой формат ломает session continuity и не дает чисто измерить cache effect и накопление history между первым, вторым и tool turn.
- Safe alternative: использовать двухрежимный A/B сценарий `A1 -> A2 -> A3` и `B1 -> B2 -> B3` с manual restart только между режимами и после restore.

<a id="r-20260603-001"></a>

### R-20260603-001 - Простой Python probe как основной приемник для Codex baseline

- Status: `rejected`
- Option: использовать только простой Python HTTP probe как достаточный приемник для smoke-test Codex OTel.
- Reason: probe был полезен как первичная проверка порта, но не подтвердил реальную доставку Codex OTel и не заменил Collector.
- Safe alternative: использовать локальный OpenTelemetry Collector с `otlp` receiver и `debug` exporter.

<a id="r-20260603-002"></a>

### R-20260603-002 - Постоянно включенная raw telemetry без фильтрации

- Status: `rejected`
- Option: оставить telemetry включенной после smoke-test и сразу собирать raw поток как есть.
- Reason: в сыром потоке уже замечены чувствительные поля уровня `user.email`, `user.account_id`, `conversation.id`.
- Safe alternative: перед постоянным сбором сделать локальную схему capture + redaction.

<a id="r-20260603-003"></a>

### R-20260603-003 - Сразу строить dashboard или делать token optimization поверх raw OTel

- Status: `rejected`
- Option: перейти сразу к dashboard, графикам или рекомендациям по оптимизации токенов без отдельного forensic parser и redaction слоя.
- Reason: raw поток пока небезопасен для прямого показа и еще не разложен в стабильные диагностические сущности уровня events, spans, metrics, sessions и warnings.
- Safe alternative: сначала локальный parser выпускает sanitized artifacts и только потом отдельно решается вопрос про dashboard или optimization workflow.

<a id="waivers"></a>

## Waivers

<a id="w-20260603-001"></a>

### W-20260603-001 - Упрощенный стартовый docset без `plan_full`, `plan_index` и `status`

- Status: `active`
- Waiver: подпроект стартует только с `readme`, `navigation`, `journal`, `decisions`.
- Reason: текущий запрос ограничен документированием уже полученного OTel baseline, без запуска большого planning/execution цикла.
- Remaining check: если подпроект пойдет в следующий этап, отдельно решить, нужен ли полный docset.
- Human approval: `recorded`

<a id="w-20260603-002"></a>

### W-20260603-002 - Локальный slug-format принят для этого подпроекта

- Status: `active`
- Waiver: внутри папки подпроекта используется canonical slug naming: `tokken_dashboard_*.md`.
- Reason: человек явно потребовал делать со слагом.
- Remaining check: при появлении новых файлов придерживаться того же naming.
- Human approval: `recorded`

<a id="relation-to-journal"></a>

## Relation to journal

Ключевые факты и проверка лежат в:

- [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries)

Этот файл хранит не историю команд, а только правила, запреты, waivers и рабочие baseline-решения.

<a id="maintenance-rule"></a>

## Maintenance rule

- Не превращать этот файл в журнал команд.
- Не записывать сюда каждую временную гипотезу.
- Добавлять сюда только то, что стало правилом, запретом, waiver или устойчивым baseline.
- Для новых устойчивых правил сначала обновлять `decisions`, потом добавлять запись или ссылку в `journal`.
- Если новый тест опровергнет текущий baseline, сначала зафиксировать факт в `journal`, затем обновить или исправить relevant decision.
