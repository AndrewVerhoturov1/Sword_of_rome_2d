# Tokken Dashboard Decisions

Slug: `tokken_dashboard`  
Owner: `Orc`  
Status: `active`  
Last updated: `2026-06-07`
Decision layer: `subproject-level accepted decisions`

## Quick Navigation

- [Purpose](#purpose)
- [Accepted Decisions](#accepted-decisions)
- [D-20260604-002](#d-20260604-002)
- [D-20260604-003](#d-20260604-003)
- [D-20260604-004](#d-20260604-004)
- [D-20260604-005](#d-20260604-005)
- [D-20260604-006](#d-20260604-006)
- [D-20260604-007](#d-20260604-007)
- [D-20260604-008](#d-20260604-008)
- [D-20260604-009](#d-20260604-009)
- [D-20260605-001](#d-20260605-001)
- [D-20260605-004](#d-20260605-004)
- [D-20260606-001](#d-20260606-001)
- [D-20260607-001](#d-20260607-001)
- [D-20260607-002](#d-20260607-002)
- [D-20260607-003](#d-20260607-003)
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

<a id="d-20260604-007"></a>

### D-20260604-007 - Lean minimal runtime is the current working token baseline

- Status: `accepted`
- Source: `user instruction on 2026-06-04`
- Decision: for further token diagnostics, use the `lean minimal` runtime as the current working baseline when comparing models and reasoning levels.
- Reason: the lean minimal confirmation run reduced observed runtime inventory to `codex_apps` and `node_repl` and produced `18813` input tokens, which is lower than the earlier `20827` and `21698` lean/playwright-only baselines.
- Consequence: later model and reasoning comparisons should be interpreted relative to this lean baseline, not relative to the earlier `13 MCP` environment.
- Boundary: this does not mean internal Codex Desktop or system prompt overhead disappeared; it only means the runtime was narrowed to the smallest confirmed local working state so far.
- Human approval: `recorded`

<a id="d-20260604-008"></a>

### D-20260604-008 - Model-switch OTel tests must be captured sequentially, not in parallel

- Status: `accepted`
- Source: `user instruction on 2026-06-04`
- Decision: when a test changes model or reasoning effort inside or across threads, capture the modes sequentially: finish one mode, flush collector, save raw, then run the next mode.
- Reason: the parallel attempt made it harder to map OTel events to exact turns. The sequential rerun produced separate raw files for `A` and `B` and allowed clean recovery of `A1..A4` and `B1..B4`.
- Consequence: the sequential package becomes the canonical evidence for model-switch comparison, and the earlier parallel package is treated as non-canonical diagnostic scratch output.
- Boundary: this rule is specific to turn-level OTel diagnostics. It does not ban parallelism in unrelated engineering tasks.
- Human approval: `recorded`

<a id="d-20260604-009"></a>

### D-20260604-009 - Future token comparisons must use cache-adjusted metrics and estimated cost, not raw input alone

- Status: `accepted`
- Source: `user summary on 2026-06-04`
- Decision: future `tokken_dashboard` reports and comparisons must treat `input_tokens` as only one layer. Canonical comparison fields now include `cached_tokens`, `non_cached_input_tokens`, `cached_ratio`, `output_tokens`, `reasoning_tokens`, `tool_tokens`, model metadata, reasoning effort, environment-layer snapshot, and estimated token cost in USD.
- Pricing rule: estimated cost must be parameterized by per-model pricing table with `input price per 1M`, `cached input price per 1M`, and `output price per 1M`. Do not hardcode prices as permanent truth because pricing can change.
- First-turn rule: diagnostics must separate `first turn`, `second turn`, and later repeated turns because cache materially changes real cost and raw input alone is misleading.
- Model-switch rule: if model changes inside one thread, reports must mark the switch point and compare both `input delta` and `cached delta` after the switch. Do not compare mixed-model threads as if they were one stable baseline.
- Environment rule: each report must snapshot MCP, plugins, skills, global user instructions, repo context, and runtime/internal layers separately, because token overhead is multi-layered.
- Working hypothesis: current evidence suggests broad user MCP inventory and repo context are not the main source of high first-turn cost; the remaining overhead is more likely spread across plugins, global instructions, and internal Codex runtime/system preamble.
- Consequence: future baselines must be re-read through cache-adjusted and cost-adjusted metrics. A run is a real improvement when `non_cached_input_tokens` and/or `estimated_total_cost_usd` go down, or when `cached_ratio` rises without raising real total cost.
- Boundary: this decision updates the interpretation contract for future reports. It does not itself change parser code, telemetry config, or past raw evidence files.
- Human approval: `recorded`

<a id="d-20260605-001"></a>

### D-20260605-001 - Universal context-cost prompt scaffolds must be stored as reusable subproject templates

- Status: `accepted`
- Source: `user instruction on 2026-06-05`
- Decision: reusable prompt scaffolds for future Token Debugger context-cost experiments must be stored inside the `tokken_dashboard` subproject as stable markdown templates with anchors, instead of remaining only in ad hoc external files like `Downloads`.
- Template adopted: [tokken_dashboard_universal_context_cost_test_prompts_single_branch.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_universal_context_cost_test_prompts_single_branch.md)
- Reason: the user wants one canonical place for future context-cost test scaffolds. Keeping the template inside the subproject makes it easier to reuse, reference from journal/decisions, and compare later runs against the same prompt structure.
- Consequence: future prompt-only test scaffolds should be saved in the subproject first, then referenced from reports and test runbooks. If a scaffold becomes canonical, link it from `readme` and `navigation`.
- Boundary: this decision stores a reusable prompt template only. It does not create a new OTel run, does not change parser logic, and does not make the template itself a raw evidence artifact.
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

<a id="d-20260605-002"></a>

### D-20260605-002 - Token Cost Normalizer v1 is the canonical cache-adjusted cost layer

- Status: `accepted`
- Source: `V3-20260605-141503-token-cost-normalizer-v1 local apply/run`
- Decision: `scripts/codex_token_cost_normalizer.py` is the canonical local layer for converting sanitized parser outputs into cache-adjusted token cost artifacts.
- Reason: reports based only on raw `input_tokens` are misleading when cached input, model pricing, output tokens, reasoning tokens and model/reasoning switches matter.
- Consequence: future dashboard/report work should consume `token_cost_turns.jsonl`, `token_cost_sessions.json`, `token_cost_summary.json` and `token_cost_dashboard_data.json` instead of re-implementing cost formulas ad hoc.
- Boundary: pricing remains config-driven in `config/token_pricing.json`; unknown models must remain `pricing_unknown` with null estimated cost fields.
- Human approval: `pending local review`

<a id="d-20260605-003"></a>

### D-20260605-003 - Codex Token Monitor Server v1 is a local utility over normalized artifacts, not a new OTel experiment

- Status: `accepted`
- Source: `Handoff 0046 — Codex Token Monitor Server v1 implementation`
- Decision: `scripts/codex_token_monitor_server.py` is the canonical local layer for browsing normalized token-cost artifacts through a compact web UI. It is a static local utility, not a new telemetry collector, live config modifier, or dashboard redesign.
- Reason: existing normalized data from `Token Cost Normalizer v1` and local `_local/codex-token-debugger/` run-folders already contain enough information for human review. A local browser UI with session discovery, step cards, archive state, and refresh integration is the next practical layer.
- Consequence: monitor server must stay stdlib-only, use existing normalizer as subprocess, discover sessions by run-folder identity, and not modify live Codex config. UI must adopt the accepted compact prototype layout but consume only real API data.
- Boundary: this decision does not authorize new OTel runs, collector management, live config changes, or dashboard redesign outside the prototype-bound MVP.
- Human approval: `accepted after local review`

<a id="d-20260605-004"></a>

### D-20260605-004 - Codex Token Monitor v2 must separate real Codex chats from archival OTel runs

- Status: `accepted`
- Source: `user feedback on monitor v1 + local Codex review`
- Decision: the next monitor iteration must become a hybrid viewer with two explicit sources: `Реальные чаты Codex` from `C:/Users/andre/.codex/**` and `Архив тестов OTel` from `_local/codex-token-debugger/**`.
- Reason: monitor v1 truthfully reflected normalized test-run artifacts, but users naturally read it as a browser of current Codex chats. This caused misleading expectations around chat titles, prompt/answer visibility, model list, reasoning effort, and the absence of the current live thread.
- Consequence: live chat data must come from local Codex state (`state_5.sqlite`, `session_index.jsonl`, `sessions/**/rollout-*.jsonl`), while archival OTel runs remain available as a separate source with explicit `mixed/noisy/confirmed` semantics.
- UI rule: the monitor must show which source is active and must not present archive run-folders as if they were ordinary user chats.
- Boundary: this decision does not authorize live streaming, new OTel capture, collector work, or writes into `C:/Users/andre/.codex/**`; the live-chat adapter is read-only over already stored local Codex artifacts.
- Human approval: `recorded`

<a id="d-20260606-001"></a>

### D-20260606-001 - Live monitor must prefer request-local step data and rich exports over compact summaries

- Status: `accepted`
- Source: `user review of the live monitor on 2026-06-06`
- Decision: in `Реальные чаты Codex` mode, ordinary visible steps must show only request-local token/cost data. If a reliable per-step checkpoint is missing, monitor must show explicit absence instead of cumulative session totals or invented numbers.
- Decision: copy/export actions in the monitor must prioritize full useful detail over compact summaries. Single-step copy should include prompt, answer, model, reasoning, usage, cost breakdown, environment, warnings, and nearby compaction/timeline context when available.
- Decision: session-level and multi-step export should default to detailed step-by-step Markdown/JSON, not to short aggregate-only summaries.
- Reason: user review showed that cumulative totals make short prompts look absurdly expensive, and current copy/export output is too weak to use as a practical forensic tool.
- Consequence: live cache/cost interpretation must remain conservative; request-local usage stays nullable, and export payloads must preserve uncertainty notes instead of hiding them.
- Boundary: this decision does not authorize invented pricing, synthetic prompt reconstruction, or writes into `C:/Users/andre/.codex/**`.
- Human approval: `recorded`

<a id="d-20260607-001"></a>

### D-20260607-001 - Live cached-token spikes must be treated as first-visible-step semantics risk before they are treated as math failure

- Status: `accepted`
- Source: `external forensic audit V1-20260607-live-monitor-audit-r2 + local review`
- Decision: in live mode, a very short first visible prompt with high `cached_tokens` is not enough evidence of monitor math failure by itself. Accepted baseline is mixed-case live telemetry semantics: request-level `last_token_usage` may include hidden `system / developer / plugin / runtime` context that is not shown as the visible prompt text.
- Decision: UI and export must clearly separate `first visible step`, `request-level usage found`, `session cumulative totals`, and `estimated cost from local pricing`. These meanings must not collapse into one exact-looking label.
- Decision: if per-step display falls back to cumulative totals, that fallback must never be presented as confirmed per-step usage.
- Reason: external audit of forensic pack `live_monitor_audit_019e9d2a` leaned toward real telemetry semantics rather than a simple mapping bug, and identified semantic overconfidence as the main remaining monitor risk.
- Consequence: next safe monitor slice is semantic hardening and export honesty, not source-split redesign and not a new OTel experiment.
- Boundary: this decision keeps the accepted hybrid baseline, does not reopen live/archive split, does not change live Codex config, and does not authorize writes into `C:/Users/andre/.codex/**`.
- Human approval: `recorded`

<a id="d-20260607-002"></a>

### D-20260607-002 - Codex Token Monitor Audit must be implemented as a separate technical verification layer before honesty hardening

- Status: `accepted`
- Source: `external planning notebook V1-20260607-014953 + local orchestration review`
- Decision: the next monitor execution slice is `Codex Token Monitor Audit` as a separate verification layer over the accepted hybrid monitor baseline. This layer checks technical truth of source selection, session identity, step attribution, usage basis, fallback semantics, cost confidence and export completeness.
- Decision: `Audit` and `Honesty hardening` are different layers. `Audit` emits machine-readable verification results and human-readable audit reports. `Honesty hardening` remains a later follow-up that improves wording, badges, and explanatory UI text for humans.
- Decision: `Audit` must verify at least:
  - correct `source_kind` and `session_id`;
  - request-level `last_token_usage` versus cumulative `total_token_usage`;
  - that fallback is never shown as confirmed per-step usage;
  - that session summary basis does not silently pretend to equal visible-step sums;
  - that copy/export preserve warnings, basis fields, confirmation semantics and cost-confidence semantics.
- Decision: the next Kilo implementation run for this slice should target the audit layer first, not reopen source split and not start a broad UI wording pass.
- Reason: current accepted monitor baseline is technically useful, but the remaining risk is not only wording. We still need an explicit verification layer that can detect when monitor source/mapping/export behavior is wrong or looks more certain than the raw evidence allows.
- Consequence: implementation planning, tests, docs and handoff scope now center on an audit module, audit endpoint/action, audit JSON/MD artifacts and confidence/status model. Human-facing semantics polish remains out of scope for this run unless needed only to surface audit results.
- Boundary: this decision does not authorize a new OTel experiment, live Codex config changes, source-split redesign, writes into `C:/Users/andre/.codex/**`, or a full monitor UI rewrite.
- Human approval: `recorded`

<a id="d-20260607-003"></a>

### D-20260607-003 - Audit must verify monitor claims against upstream evidence and must downgrade confidence when that evidence is missing

- Status: `accepted`
- Source: `local review of Kilo run 0048 + forensic live thread 019e9d2a on 2026-06-07`
- Decision: `Codex Token Monitor Audit` is not allowed to mark a session or step as technically verified only because the current monitor already built a plausible `session detail` object. Audit must compare at least part of that object against evidence upstream from the UI/detail mapping.
- Decision: for live mode, strong statuses must not come only from `confirmation_status` fields already present in step payloads. Audit must verify enough source evidence to distinguish:
  - `request-level last_token_usage found`;
  - `cumulative total_token_usage`;
  - visible-step attribution uncertainty;
  - cumulative session basis versus visible-step basis.
- Decision: if upstream evidence is absent, incomplete, or outside the selected audit scope, audit must emit downgraded confidence such as `not_verified`, `warning`, `medium`, or repo-equivalent weaker status. It must not default to `ok`, `high`, or `per_step_estimated`.
- Decision: mandatory regression tests for this slice must include:
  - a live-like self-certification case where detail looks fully confirmed but evidence is still insufficient for `high`;
  - a cumulative summary cost case where visible steps look confirmed but session cost confidence must stay downgraded;
  - a selected-steps scope case where audit must expose narrowed scope explicitly.
- Reason: local review showed that run `0048_codex_token_monitor_audit` can self-certify the same mapping it is supposed to verify. On forensic live thread `019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f`, audit returned `ok / all_confirmed / high / per_step_estimated` even though the accepted unresolved risk is exactly step attribution and cumulative-vs-request confidence.
- Consequence: next Kilo correction slice is not honesty wording. It is audit-truth hardening plus regression tests around self-certification failure modes.
- Boundary: this decision still does not authorize a new OTel experiment, live Codex config changes, source-split redesign, or writes into `C:/Users/andre/.codex/**`.
- Human approval: `recorded`

## Maintenance rule

- Не превращать этот файл в журнал команд.
- Не записывать сюда каждую временную гипотезу.
- Добавлять сюда только то, что стало правилом, запретом, waiver или устойчивым baseline.
- Для новых устойчивых правил сначала обновлять `decisions`, потом добавлять запись или ссылку в `journal`.
- Если новый тест опровергнет текущий baseline, сначала зафиксировать факт в `journal`, затем обновить или исправить relevant decision.
