# Tokken Dashboard Journal

Slug: `tokken_dashboard`  
Owner: `Orc`  
Status: `active`  
Started: `2026-06-03`

## Quick Navigation

- [Purpose](#purpose)
- [Entries](#entries)
- [J-20260603-001](#j-20260603-001)
- [J-20260603-002](#j-20260603-002)
- [J-20260603-003](#j-20260603-003)
- [J-20260603-004](#j-20260603-004)
- [J-20260603-005](#j-20260603-005)
- [J-20260604-001](#j-20260604-001)
- [J-20260604-002](#j-20260604-002)
- [J-20260604-003](#j-20260604-003)
- [J-20260604-004](#j-20260604-004)
- [J-20260604-005](#j-20260604-005)
- [J-20260604-006](#j-20260604-006)
- [J-20260604-007](#j-20260604-007)
- [J-20260604-008](#j-20260604-008)
- [J-20260604-009](#j-20260604-009)
- [J-20260605-001](#j-20260605-001)
- [Bugs And Difficulties](#bugs-and-difficulties)
- [Open Follow-ups](#open-follow-ups)

<a id="purpose"></a>

## Назначение

Этот файл фиксирует фактические действия и результаты по локальной OTel-проверке для `tokken_dashboard`.

Журнал отвечает на вопрос:

```text
Что реально было проверено и что реально сработало?
```

Для долгоживущих правил и решений есть:

- [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions)

<a id="entries"></a>

## Записи

<a id="j-20260603-001"></a>

### J-20260603-001 - Первый локальный probe подтвердил проблему baseline

- Этап жизненного цикла: `Stage 0 - local OTel baseline search`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [S-20260603-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#s-20260603-001), [R-20260603-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#r-20260603-001)
- Созданные файлы:
  - [otel_probe.py](C:/Users/andre/.codex/tmp/otel-smoke-20260603-205139/otel_probe.py)
- Измененные файлы:
  - [config.toml](C:/Users/andre/.codex/config.toml)
- Подтверждение:
  - найден рабочий конфиг Codex: [config.toml](C:/Users/andre/.codex/config.toml);
  - сделан backup: [config.toml.bak-otel-smoke-20260603-205139](C:/Users/andre/.codex/config.toml.bak-otel-smoke-20260603-205139);
  - простой Python probe слушал `127.0.0.1:4318`;
  - обычный локальный POST до probe доходил;
  - Codex при endpoint на `127.0.0.1` давал `502`, а probe POST от Codex не получал.
- Проверка:
  - локальный self-test probe вернул `200`;
  - проверка Codex на `/v1/traces` и `/v1/logs` не дала входящих запросов в probe.
- Вердикт человека: `not applicable`
- Баги и сложности:
  - простой probe оказался недостаточным для подтверждения реального OTel-пути Codex;
  - `127.0.0.1` выглядел рабочим для ручного POST, но не для Codex.
- Следующий шаг:
  - проверить не probe, а настоящий локальный OpenTelemetry Collector.

<a id="j-20260603-002"></a>

### J-20260603-002 - Локальный OpenTelemetry Collector подтвердил рабочий путь через localhost

- Этап жизненного цикла: `Stage 0 - local OTel baseline captured`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-002), [D-20260603-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-003), [D-20260603-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-004), [S-20260603-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#s-20260603-001), [R-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#r-20260603-002)
- Созданные файлы:
  - [collector-config.yaml](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/collector-config.yaml)
  - [collector.stderr.log](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/collector.stderr.log)
- Измененные файлы:
  - [config.toml](C:/Users/andre/.codex/config.toml)
- Подтверждение:
  - скачан и запущен локальный `otelcol v0.153.0`;
  - Collector слушал `127.0.0.1:4318` для HTTP и `127.0.0.1:4317` для gRPC;
  - ручные POST на `/v1/traces`, `/v1/logs`, `/v1/metrics` доходили до Collector;
  - при конфиге Codex с `127.0.0.1` снова были `502`, а Collector сигналов от Codex не увидел;
  - при конфиге Codex с `localhost` Collector получил реальные `Traces`, `Logs` и `Metrics`;
  - service names в raw output включали `codex-app-server`, `codex-app-server-test-client`, `Codex Desktop`;
  - для `codex exec` Collector получил сырые log-события ответа и usage-метрики;
  - в raw output были чувствительные поля уровня `user.email`, `user.account_id`, `conversation.id`.
- Проверка:
  - Collector config прошел validate;
  - `codex debug app-server send-message-v2 "ответь коротко: test"` дал сигналы в Collector при `localhost`;
  - `codex exec "ответь коротко: test"` тоже дал сигналы в Collector при `localhost`;
  - telemetry block затем удален из [config.toml](C:/Users/andre/.codex/config.toml), Collector остановлен, порты освобождены.
- Вердикт человека: `not applicable`
- Баги и сложности:
  - `127.0.0.1` стабильно давал `502` именно для Codex OTel-пути;
  - interactive CLI полноценно не проверился в non-TTY среде;
  - raw telemetry содержит чувствительные поля, поэтому постоянный режим без фильтрации опасен.
- Следующий шаг:
  - если нужен следующий этап, делать только локальный raw capture с маскировкой чувствительных полей.

<a id="j-20260603-003"></a>

### J-20260603-003 - Создан базовый docset подпроекта `tokken_dashboard`

- Этап жизненного цикла: `Stage 0 - local OTel baseline documented`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [W-20260603-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#w-20260603-001), [W-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#w-20260603-002)
- Созданные файлы:
  - [tokken_dashboard_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md)
  - [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md)
  - [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md)
  - [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md)
- Измененные файлы:
  - `none`
- Подтверждение:
  - подпроект оформлен в slug-формате;
  - journal зафиксировал и неудачный baseline на `127.0.0.1`, и удачный baseline на `localhost`;
  - рабочая практика вынесена в отдельный `decisions` файл.
- Проверка:
  - файлы созданы в `.ai/subprojects/tokken_dashboard/`.
- Вердикт человека: `pending`
- Баги и сложности:
  - `tokken_dashboard` пока не имеет `plan_full`, `plan_index`, `status`;
  - это сознательно оставлено за пределами текущего запроса.
- Следующий шаг:
  - получить human verdict по docset или расширить подпроект до следующего execution этапа.

<a id="j-20260603-004"></a>

### J-20260603-004 - Collector `file` exporter подтвердил raw OTel capture в локальный файл

- Этап жизненного цикла: `Stage 0 - local raw OTel file capture confirmed`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260603-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-003), [D-20260603-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-004), [D-20260603-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-005)
- Созданные файлы:
  - [collector-file-config.yaml](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/collector-file-config.yaml)
  - [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json)
  - [collector.stderr.log](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/collector.stderr.log)
  - [config.toml.bak-otel-file-smoke-20260603-214412](C:/Users/andre/.codex/config.toml.bak-otel-file-smoke-20260603-214412)
- Измененные файлы:
  - [config.toml](C:/Users/andre/.codex/config.toml) был временно изменен и затем возвращен в исходное состояние.
- Подтверждение:
  - использован локальный `otelcol v0.153.0` с `otlp` receiver и `file` exporter;
  - Codex endpoint-ы были только через `localhost`: `/v1/logs`, `/v1/traces`, `/v1/metrics`;
  - `log_user_prompt = false` был включен в временном `[otel]` блоке;
  - создан локальный raw-файл [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json) размером `152576` байт;
  - Collector получил `logs`, `traces` и `metrics`;
  - итоговый подсчет в файле: `resourceLogs=7`, `logRecords=19`, `resourceSpans=5`, `spans=80`, `resourceMetrics=1`, `metrics=26`.
- Token fields:
  - найдены `input_token_count`, `output_token_count`, `cached_token_count`, `reasoning_token_count`, `tool_token_count`;
  - найдены `codex.turn.token_usage.input_tokens`, `codex.turn.token_usage.cached_input_tokens`, `codex.turn.token_usage.non_cached_input_tokens`, `codex.turn.token_usage.output_tokens`, `codex.turn.token_usage.reasoning_output_tokens`, `codex.turn.token_usage.total_tokens`;
  - найдены `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.cache_read.input_tokens`;
  - найдены `codex.usage.total_tokens`, `codex.usage.reasoning_output_tokens`, `token_type`.
- Privacy fields:
  - `user.email` найден;
  - `user.account_id` найден;
  - `conversation.id` найден;
  - `prompt` и `prompt_length` тоже найдены как prompt metadata; для будущего parser/dashboard pipeline нужен отдельный policy-layer по их сохранению или маскированию.
- Проверка cleanup:
  - временный `[otel]` блок удален из [config.toml](C:/Users/andre/.codex/config.toml);
  - SHA256 текущего [config.toml](C:/Users/andre/.codex/config.toml) совпал с backup [config.toml.bak-otel-file-smoke-20260603-214412](C:/Users/andre/.codex/config.toml.bak-otel-file-smoke-20260603-214412);
  - Collector остановлен;
  - порты `4317` и `4318` освобождены;
  - `git status --short` был чистым до документирования результата.
- Вердикт человека: `not applicable`
- Баги и сложности:
  - `log_user_prompt = false` не является достаточным privacy-фильтром: raw telemetry все равно содержит чувствительные поля;
  - во время `codex exec` обычный Codex runtime пытался обращаться к внешним MCP/analytics endpoint из существующего config; OTel наружу не отправлялся, но для полностью изолированного будущего теста нужен временный config с отключенными внешними MCP/analytics.
- Следующий шаг:
  - строить parser можно на локальном raw-файле;
  - dashboard разрешать только после redaction слоя, который удаляет или маскирует минимум `user.email`, `user.account_id`, `conversation.id`, `host.name` и чувствительные auth/header поля.

<a id="j-20260603-005"></a>

### J-20260603-005 - Локальный forensics parser выпустил sanitized OTel artifacts для token diagnostics

- Этап жизненного цикла: `Stage 1 - local forensics parser working`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260603-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-007), [R-20260603-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#r-20260603-003)
- Созданные файлы:
  - [codex_token_debugger.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_debugger.py)
  - [test_codex_token_debugger.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_debugger.py)
  - [codex_otel_sample.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/fixtures/codex_otel_sample.jsonl)
- Локальные output artifacts:
  - [clean_events.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2/clean_events.jsonl)
  - [token_usage.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2/token_usage.jsonl)
  - [spans.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2/spans.jsonl)
  - [metrics.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2/metrics.jsonl)
  - [sessions.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2/sessions.jsonl)
  - [session_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2/session_summary.json)
  - [warnings.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2/warnings.jsonl)
  - [diagnostic_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2/diagnostic_report.md)
- Подтверждение:
  - parser читает локальный raw OTel `json/jsonl` и пишет набор sanitized artifacts без внешних endpoint-ов;
  - unit test `python -m unittest tests.test_codex_token_debugger` прошел;
  - реальный запуск на [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json) создал `clean_events=36`, `token_usage=6`, `spans=80`, `metrics=49`, `sessions=27`, `warnings=5`;
  - в `clean_events.jsonl`, `token_usage.jsonl`, `spans.jsonl`, `metrics.jsonl`, `sessions.jsonl` не найдено `user.email`, `user.account_id`, `conversation.id`;
  - `prompt_length` в sanitized outputs сохраняется как диагностический сигнал, а `prompt` сохраняется только если уже пустой или `[REDACTED]`;
  - parser автоматически поднял предупреждения `many_mcp_servers`, `prompt_metadata_present`, `high_input_low_output`, `tool_or_mcp_activity_near_expensive_turn`, `private_fields_detected_in_raw`;
  - token fields из raw подтверждены и вынесены в `token_usage.jsonl` и `session_summary.json`.
- Проверка:
  - `python -m unittest tests.test_codex_token_debugger`
  - `python scripts\codex_token_debugger.py --input C:\Users\andre\.codex\tmp\otel-file-smoke-20260603-214412\codex-otel.json --output-dir D:\Codex+Kilocode\projects\sword-of-rome-web\_local\codex-token-debugger\smoke-20260603-r2`
  - `rg -n -F 'user.email' ...`, `rg -n -F 'user.account_id' ...`, `rg -n -F 'conversation.id' ...` по основным sanitized JSONL-файлам вернули пустой результат.
- Вердикт человека: `not applicable`
- Баги и сложности:
  - warning `private_fields_detected_in_raw` сначала терял список полей из-за слишком агрессивной sanitization логики, затем это исправлено;
  - `session_summary.json` пока агрегирует часть записей грубо и может давать дублирующиеся session-подобные срезы для `service/model`, если raw не несет одного стабильного sanitized session id;
  - консоль PowerShell в текущей среде показывает UTF-8 русский текст с кракозябрами, но сами файлы пишутся в UTF-8.
- Следующий шаг:
  - отдельно решить, какой sanitized session key и какой whitelist полей нужны для будущего dashboard/parser schema;
  - не переходить к dashboard до отдельного решения по allowed fields.

<a id="j-20260604-001"></a>

### J-20260604-001 - Подготовлен A/B turn-cost experiment package с current и minimal/no MCP режимами

- Этап жизненного цикла: `Stage 1 - turn-cost A/B experiment prepared`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-002), [D-20260603-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-003), [D-20260603-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-004), [D-20260603-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-005), [D-20260603-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-006), [D-20260604-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-001), [R-20260604-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#r-20260604-001)
- Созданные файлы:
  - [codex_otel_ab_experiment.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_otel_ab_experiment.py)
  - [test_codex_otel_ab_experiment.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_otel_ab_experiment.py)
- Локальные runtime artifacts:
  - [experiment_manifest.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/experiment_manifest.json)
  - [runbook.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/runbook.md)
  - [compare_summary.template.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/compare_summary.template.json)
  - [compare_report.template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/compare_report.template.md)
  - [config.current-with-otel.toml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/config.current-with-otel.toml)
  - [config.minimal-no-mcp-with-otel.toml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/config.minimal-no-mcp-with-otel.toml)
  - [config.original.toml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/config.original.toml)
  - [collector-A-current-config.yaml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/collector-A-current-config.yaml)
  - [collector-B-minimal-config.yaml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/collector-B-minimal-config.yaml)
  - [apply-current-config.ps1](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/apply-current-config.ps1)
  - [apply-minimal-config.ps1](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/apply-minimal-config.ps1)
  - [restore-original-config.ps1](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/restore-original-config.ps1)
  - [config.toml.bak-otel-ab-turn-cost-20260604-otab02](C:/Users/andre/.codex/config.toml.bak-otel-ab-turn-cost-20260604-otab02)
- Подтверждение:
  - подготовлен отдельный experiment package для двухрежимного сценария `A-current-config` vs `B-minimal-config`;
  - `current` variant сохраняет MCP окружение и добавляет только локальный `[otel]` блок на `localhost`;
  - `minimal/no MCP` variant удаляет все `[mcp_servers.*]` секции и добавляет тот же локальный `[otel]` блок;
  - compare template уже хранит mode/turn структуру `A1/A2/A3` и `B1/B2/B3`, а также поля `same_session_reliable`, `tool_call_status`, `tool_mcp_activity`;
  - backup [config.toml.bak-otel-ab-turn-cost-20260604-otab02](C:/Users/andre/.codex/config.toml.bak-otel-ab-turn-cost-20260604-otab02) и [config.original.toml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/config.original.toml) byte-identical текущему live [config.toml](C:/Users/andre/.codex/config.toml);
  - live [config.toml](C:/Users/andre/.codex/config.toml) на этом шаге не менялся.
- Проверка:
  - `python -m unittest tests.test_codex_otel_ab_experiment`
  - `python -m unittest tests.test_codex_token_debugger`
  - `Get-FileHash -Algorithm SHA256 config.toml, backup, config.original.toml`
- Вердикт человека: `not applicable`
- Баги и сложности:
  - первый вариант prep-script портил точный SHA256 backup из-за записи через `write_text`; это исправлено, теперь backup и `config.original.toml` сохраняются byte-identical;
  - A/B run пока еще не выполнялся, потому что дальше нужен ручной restart между stop points.
- Следующий шаг:
  - это `STOP POINT 1`: backup/config/collector prepared;
  - дальше по команде человека перейти к записи current config и ждать ручной restart для `continue A run`.

<a id="j-20260604-002"></a>

### J-20260604-002 - Tool/MCP Activity Inspector построил forensic-отчет по sanitized A/B outputs

- Этап жизненного цикла: `Stage 1 - tool/MCP activity inspector working`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260604-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-002)
- Созданные файлы:
  - [tool_mcp_activity_inspector.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/tool_mcp_activity_inspector.py)
  - [test_tool_mcp_activity_inspector.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_tool_mcp_activity_inspector.py)
- Локальные output artifacts:
  - [tool_mcp_activity.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity/tool_mcp_activity.jsonl)
  - [tool_mcp_activity_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity/tool_mcp_activity_summary.json)
  - [tool_mcp_activity_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity/tool_mcp_activity_report.md)
- Подтверждение:
  - inspector использует sanitized outputs из `A-current-config-rerun/parsed`, `B-minimal-config/parsed` и [compare_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/compare_summary.json);
  - raw OTel не читался;
  - Codex config не менялся;
  - новых OTel-прогонов не запускалось;
  - найдено `1222` Tool/MCP activity records;
  - основные activity types: `mcp_server_inventory`, `mcp_init`, `mcp_tool_discovery`, `mcp_transport`, `tool_call_build`, `tool_call_metric`, `tool_call_duration_metric`, `tool_related_span`, `mcp_related_span`;
  - `current config` имеет `681` activity records, `minimal/no MCP` имеет `541`;
  - вывод по token overhead остается из `compare_summary.json`: current примерно на `+10.1k` input tokens дороже minimal, tool-turn добавляет около `+200` input tokens.
- Проверка:
  - `python -m unittest tests.test_tool_mcp_activity_inspector`
  - `python scripts\tool_mcp_activity_inspector.py --compare-summary _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\compare_summary.json --a-parsed _local\codex-token-debugger\ab-turn-cost-20260604-otab02\A-current-config-rerun\parsed --b-parsed _local\codex-token-debugger\ab-turn-cost-20260604-otab02\B-minimal-config\parsed --output-dir _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\tool_mcp_activity`
  - `rg -n "user\.email|user\.account_id|conversation\.id|host\.name|authorization|cookie|access_token|refresh_token|id_token" _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\tool_mcp_activity` вернул пустой результат.
- Вердикт человека: `pending`
- Баги и сложности:
  - часть tool/MCP metrics видна на mode-level, но не попадает в короткие turn windows по timestamp, поэтому для таких записей используется `mode_level` или limitation в отчете;
  - OTel не дает точный per-tool token accounting, поэтому inspector не делает выводов вида "этот tool съел X tokens".
- Следующий шаг:
  - если диагностику продолжать, делать `MCP inventory / schema size report`: количество tools на MCP server, размеры descriptions/schemas и rough token estimate schema payload.

<a id="j-20260604-003"></a>

### J-20260604-003 - MCP Schema Inventory создал read-only отчет по config metadata

- Этап жизненного цикла: `Stage 1 - MCP schema inventory complete`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260604-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-003)
- Созданные файлы:
  - [mcp_schema_inventory.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/mcp_schema_inventory.py)
  - [test_mcp_schema_inventory.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_mcp_schema_inventory.py)
- Локальные output artifacts:
  - [mcp_schema_inventory.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/mcp_schema_inventory.jsonl)
  - [mcp_schema_inventory_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/mcp_schema_inventory_summary.json)
  - [mcp_schema_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/mcp_schema_inventory_report.md)
  - [mcp_schema_inventory_warnings.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/mcp_schema_inventory_warnings.jsonl)
  - [config.mcp_sections.sanitized.toml](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/config.mcp_sections.sanitized.toml)
- Подтверждение:
  - script читает live [config.toml](C:/Users/andre/.codex/config.toml) только read-only;
  - `config.toml` не менялся;
  - новые OTel-прогоны не запускались;
  - реальные tool calls не выполнялись;
  - найдено `13` current MCP servers и `2` minimal MCP servers из [compare_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/compare_summary.json);
  - в current config metadata найдено `15` tool override names, но настоящие JSON schemas безопасно получить не удалось;
  - `schema_available_server_count = 0`;
  - все `13` current servers получили warning `schema_unavailable`;
  - rough schema token estimate для current config равен `0`, потому что настоящие schemas недоступны, а tool override names не считаются schema payload.
- Проверка:
  - `python -m unittest tests.test_mcp_schema_inventory`
  - `python scripts\mcp_schema_inventory.py --config C:\Users\andre\.codex\config.toml --compare-summary _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\compare_summary.json --activity-summary _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\tool_mcp_activity\tool_mcp_activity_summary.json --output-dir _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\mcp_schema_inventory`
  - privacy grep по output artifacts не нашел secret values, cookies, access tokens, auth headers или реальные email values; env key names сохранены только как names.
- Вердикт человека: `pending`
- Баги и сложности:
  - безопасный read-only путь не дал настоящие tool schemas;
  - поэтому этот отчет не может объяснить `+10.1k` через schema size и не ранжирует servers по настоящему schema token payload;
  - следующий сильный диагностический шаг - MCP group attribution experiment, если человек разрешит новые controlled A/B micro-runs.
- Следующий шаг:
  - не делать dashboard;
  - если продолжать диагностику, спланировать группы MCP servers и измерить token delta по группам.

<a id="j-20260604-004"></a>

### J-20260604-004 - Effective MCP Inventory отделил configured, effective enabled и observed MCP servers

- Этап жизненного цикла: `Stage 1 - effective MCP inventory hardened`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260604-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-004)
- Измененные файлы:
  - [mcp_schema_inventory.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/mcp_schema_inventory.py)
  - [test_mcp_schema_inventory.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_mcp_schema_inventory.py)
- Локальные output artifacts:
  - [effective_mcp_inventory_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/effective_mcp_inventory_summary.json)
  - [effective_mcp_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/effective_mcp_inventory_report.md)
- Подтверждение:
  - script по-прежнему читает live [config.toml](C:/Users/andre/.codex/config.toml) только read-only;
  - raw OTel не читался;
  - новые OTel/Collector/Codex run не запускались;
  - current snapshot содержит `12` configured MCP sections;
  - effective enabled по config semantics = `6`;
  - explicit disabled = `6`;
  - old current telemetry observed = `13`;
  - old minimal telemetry observed = `2`;
  - mismatch count = `7`;
  - mismatch есть у `codex_apps`, `figma`, `google_workspace`, `obsidian`, `obsidian_tasks`, `paper`, `semgrep`.
- Проверка:
  - `python -m unittest tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment`
  - `python scripts\mcp_schema_inventory.py --config C:\Users\andre\.codex\config.toml --compare-summary _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\compare_summary.json --activity-summary _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\tool_mcp_activity\tool_mcp_activity_summary.json --output-dir _local\codex-token-debugger\ab-turn-cost-20260604-otab02\compare\mcp_schema_inventory`
  - `git diff --check`
- Вердикт человека: `pending`
- Баги и сложности:
  - old telemetry и current config snapshot расходятся, поэтому старый `+10.1k` overhead нельзя автоматически считать overhead именно текущего effective config;
  - следующий безопасный шаг теперь сужен: сначала tiny confirmation run от текущего effective baseline, потом MCP group attribution.
- Следующий шаг:
  - не делать dashboard;
  - перед group attribution сделать confirmation run для current effective config.

<a id="j-20260604-005"></a>

### J-20260604-005 - Tool Environment Inventory отделил MCP, plugins и runtime/internal layers

- Этап жизненного цикла: `Stage 1 - tool environment inventory working`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260604-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-005)
- Измененные файлы:
  - [mcp_schema_inventory.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/mcp_schema_inventory.py)
  - [test_mcp_schema_inventory.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_mcp_schema_inventory.py)
- Локальные output artifacts:
  - [tool_environment_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080502/reports/tool_environment_inventory_report.md)
  - [tool_environment_inventory_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080502/reports/tool_environment_inventory_summary.json)
  - [config_tool_environment_sanitized.toml](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080502/configs/config_tool_environment_sanitized.toml)
- Подтверждение:
  - physical MCP removal reduced observed MCP inventory from `13` to `3`;
  - selected first-turn input tokens did not go down: `21177` -> `21698`;
  - current live config still has enabled plugins, including `github@openai-curated`, `superpowers@openai-curated`, `vercel@openai-curated`, `netlify@openai-curated`, `browser@openai-bundled`;
  - current MCP sections visible in config are `playwright` and `node_repl`;
  - runtime/internal candidates remain `codex_apps` and `node_repl`.
- Проверка:
  - `python -m unittest tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment`
  - `git diff --check`
  - privacy grep по new local outputs не нашел real email, secret values или query string.
- Вердикт человека: `pending`
- Баги и сложности:
  - inventory не доказывает точный token вклад конкретного plugin или runtime layer;
  - следующий сильный тест теперь логично отделять plugins от runtime/internal слоя.
- Следующий шаг:
  - не делать dashboard;
  - если продолжать диагностику, следующим маленьким run должен быть `no-plugin/no-extra-tools`, потому что plugins сейчас включены.

<a id="j-20260604-006"></a>

### J-20260604-006 - Tool Environment Inventory added skills and auto-loaded instruction candidates

- Р­С‚Р°Рї Р¶РёР·РЅРµРЅРЅРѕРіРѕ С†РёРєР»Р°: `Stage 1 - tool environment + instruction inventory working`
- Р РѕР»СЊ: `Orc`
- РњР°СЂС€СЂСѓС‚ РІС‹РїРѕР»РЅРµРЅРёСЏ: `direct`
- РЎСЃС‹Р»РєР° РЅР° СЃРµСЃСЃРёСЋ: `not available`
- Related decisions: [D-20260604-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-005), [D-20260604-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-006)
- РР·РјРµРЅРµРЅРЅС‹Рµ С„Р°Р№Р»С‹:
  - [mcp_schema_inventory.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/mcp_schema_inventory.py)
  - [test_mcp_schema_inventory.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_mcp_schema_inventory.py)
- Р›РѕРєР°Р»СЊРЅС‹Рµ output artifacts:
  - [tool_environment_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080635/reports/tool_environment_inventory_report.md)
  - [tool_environment_inventory_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080635/reports/tool_environment_inventory_summary.json)
  - [config_tool_environment_sanitized.toml](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080635/configs/config_tool_environment_sanitized.toml)
- РџРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ:
  - live config still has `2` MCP sections, `6` plugins, `5` enabled plugins;
  - `skills.config` in live config contains `11` configured skill candidates and they are currently disabled;
  - root [AGENTS.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/AGENTS.md) is large: about `58.7 KB / 14.7k tokens`;
  - repo inventory found `410` markdown instruction candidates including `.ai/**/*.md`;
  - report now separates MCP/plugins/runtime from skills/instructions/auto-loaded context layer.
- РџСЂРѕРІРµСЂРєР°:
  - `python -m unittest tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment`
  - `python scripts\\mcp_schema_inventory.py --mode tool-environment --config C:\\Users\\andre\\.codex\\config.toml --output-dir _local\\codex-token-debugger\\tool-environment-inventory-20260604-080635 --before-after-summary _local\\codex-token-debugger\\after-4-mcp-ui-compare-20260604-062149\\compare\\before_vs_after_4_mcp_summary.json --playwright-summary _local\\codex-token-debugger\\playwright-only-confirmation-20260604-072040\\reports\\playwright_only_confirmation_summary.json --effective-summary _local\\codex-token-debugger\\ab-turn-cost-20260604-otab02\\compare\\mcp_schema_inventory\\effective_mcp_inventory_summary.json --before-after-report _local\\codex-token-debugger\\after-4-mcp-ui-compare-20260604-062149\\compare\\before_vs_after_4_mcp_report.md --playwright-report _local\\codex-token-debugger\\playwright-only-confirmation-20260604-072040\\reports\\playwright_only_confirmation_report.md --effective-report _local\\codex-token-debugger\\ab-turn-cost-20260604-otab02\\compare\\mcp_schema_inventory\\effective_mcp_inventory_report.md`
  - privacy grep РїРѕ new local outputs РЅРµ РЅР°С€РµР» real email, token values РёЛЃ URL query strings.
- Р’РµСЂРґРёРєС‚ С‡РµР»РѕРІРµРєР°: `pending`
- Р‘Р°РіРё Рё СЃР»РѕР¶РЅРѕСЃС‚Рё:
  - inventory still does not prove exact prompt composition;
  - `likely_auto_loaded` is best-effort classification, not hard runtime truth;
  - current result only says this layer is large enough to remain a plausible part of high input cost.
- РЎР»РµРґСѓСЋС‰РёР№ С€Р°Рі:
  - РЅРµ РґРµР»Р°С‚СЊ dashboard;
  - РµСЃР»Рё РїСЂРѕРґРѕР»Р¶Р°С‚СЊ РґРёР°РіРЅРѕСЃС‚РёРєСѓ, following smallest run should still isolate plugins before broader runtime conclusions.

<a id="j-20260604-007"></a>

### J-20260604-007 - Lean minimal confirmation established the current working low-overhead runtime baseline

- Этап жизненного цикла: `Stage 1 - lean minimal baseline confirmed`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260604-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-007)
- Локальные output artifacts:
  - [lean_minimal_confirmation_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/lean-minimal-confirmation-20260604-225228/reports/lean_minimal_confirmation_report.md)
  - [lean_minimal_confirmation_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/lean-minimal-confirmation-20260604-225228/reports/lean_minimal_confirmation_summary.json)
- Подтверждение:
  - lean minimal run дал `18813` input tokens;
  - observed runtime inventory сузился до `codex_apps` и `node_repl`;
  - это оказалось дешевле предыдущего no-plugins/no-user-instructions результата `20827` и playwright-only repo run `21698`;
  - значит `playwright` и связанный tool layer реально давали заметный overhead, но большой остаток стоимости все еще остается в internal runtime/system layer.
- Проверка:
  - локальный OTel confirmation run;
  - review summary/report files в `_local/codex-token-debugger/lean-minimal-confirmation-20260604-225228/`.
- Вердикт человека: `pending`
- Баги и сложности:
  - markdown report сначала страдал от проблем с русской кодировкой в Windows;
  - итоговый report пришлось отдельно переписать в `UTF-8 with BOM`.
- Следующий шаг:
  - использовать lean minimal как рабочую baseline-среду для сравнений моделей и reasoning levels.

<a id="j-20260604-008"></a>

### J-20260604-008 - Sequential model-switch compare replaced the parallel attempt

- Этап жизненного цикла: `Stage 1 - sequential model switch comparison captured`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260604-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-007), [D-20260604-008](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-008)
- Локальные output artifacts:
  - [model_switch_sequential_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/model-switch-sequential-20260604-232818/reports/model_switch_sequential_report.md)
  - [model_switch_sequential_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/model-switch-sequential-20260604-232818/reports/model_switch_sequential_summary.json)
  - [codex-token-debugger-tests-from-lean-minimal-20260604.zip](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/bundles/codex-token-debugger-tests-from-lean-minimal-20260604.zip)
- Подтверждение:
  - режим `A` снят как `gpt-5.4-mini/low -> gpt-5.5/high` в одном чате;
  - режим `B` снят как четыре последовательных хода на `gpt-5.5/high`;
  - `A1=16618`, `A2=16696`, `A3=21361`, `A4=21440`;
  - `B1=18355`, `B2=18433`, `B3=18512`, `B4=18591`;
  - switch `A2 -> A3` дал jump `+4665` input tokens, тогда как в `B` рост между соседними ходами остался маленьким, около `+78/+79`.
- Проверка:
  - раздельный capture raw для `A` и `B`;
  - выделение target completions по `conversation.id` и окнам времени;
  - итоговый compare report сохранен в `_local`.
- Вердикт человека: `pending`
- Баги и сложности:
  - параллельный запуск оказался неканоничным для такой диагностики и был отброшен;
  - при копировании raw по длинным путям `PowerShell Copy-Item` сбоил, поэтому raw фиксировался через прямой `System.IO.File.Copy`.
- Следующий шаг:
  - если продолжать серию, новые model/reasoning tests снимать только последовательно.

<a id="j-20260604-009"></a>

### J-20260604-009 - Token Debugger reporting rules were tightened to cache-adjusted and cost-aware comparisons

- Этап жизненного цикла: `Stage 1 - reporting contract tightened`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Related decisions: [D-20260604-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-007), [D-20260604-008](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-008), [D-20260604-009](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-009)
- Подтверждение:
  - для следующих сравнений больше недостаточно смотреть только на `input_tokens`;
  - canonical fields теперь включают `cached_tokens`, `non_cached_input_tokens`, `cached_ratio`, `output_tokens`, `reasoning_tokens`, `tool_tokens`;
  - future reports должны хранить model metadata, reasoning effort, environment-layer snapshot и estimated USD cost по parameterized pricing table;
  - first-turn, second-turn и repeated-turn comparisons теперь считаются разными диагностическими случаями;
  - mixed-model threads требуют отдельной пометки про switch point и cache/input deltas после switch;
  - сохранены рабочие ориентиры для сверки: `21177/13`, `19024/13`, `21698/3`, `21738/3`, `20827/3`, lean minimal `18813/2`, lean model comparison around `18.3k`, `17.0k`, `16.6k`.
- Проверка:
  - rules summary прочитан из user-provided note и перенесен в `decisions`, `journal`, `navigation`, `readme`;
  - код parser-а и raw artifacts в этом шаге не менялись.
- Вердикт человека: `pending`
- Баги и сложности:
  - rules note пришел во вложении с битой Windows-кодировкой, поэтому перенос делался по смыслу, а не verbatim-copy;
  - старые markdown-файлы уже частично содержат mojibake, поэтому новую запись безопаснее было добавить как отдельный anchor-block, не переписывая старые разделы.
- Следующий шаг:
  - при следующем runtime test or compare report уже считать canonical метриками `non_cached_input_tokens`, `cached_ratio` и `estimated_total_cost_usd`, а headline `input_tokens` использовать только вместе с cache context.

<a id="bugs-and-difficulties"></a>

<a id="j-20260605-001"></a>

### J-20260605-001 - Universal single-branch context-cost prompt scaffold was copied into the subproject

- Stage: `Stage 1 - reusable test scaffold documented`
- Role: `Orc`
- Execution route: `direct`
- Session link: `not available`
- Related decisions: [D-20260605-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-001)
- Created files:
  - [tokken_dashboard_universal_context_cost_test_prompts_single_branch.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_universal_context_cost_test_prompts_single_branch.md)
- Source file:
  - [universal_context_cost_test_prompts_single_branch.md](C:/Users/andre/Downloads/universal_context_cost_test_prompts_single_branch.md)
- Confirmed:
  - the imported source file decoded correctly as UTF-8;
  - the scaffold contains one large shared fixture plus `A1 -> A4` prompt steps;
  - the subproject copy now has stable anchors and can be referenced as the canonical reusable prompt template for future context-cost tests.
- Verification:
  - source bytes were checked against UTF-8 decoding;
  - local subproject file created with anchors and preserved prompt structure;
  - `readme` and `navigation` linked to the new template.
- Human verdict: `pending`
- Bugs and difficulties:
  - the first shell read of the Downloads file showed mojibake because PowerShell rendered UTF-8 badly in console output;
  - the actual source bytes were valid UTF-8, so the template itself was recovered cleanly before saving into the subproject.
- Next step:
  - reuse this scaffold for later model/context-cost runs instead of rebuilding the same prompt chain from scratch.

<a id="bugs-and-difficulties"></a>

<a id="j-20260605-002"></a>

### J-20260605-002 - Token Cost Normalizer v1 materialized and smoke-tested

- Stage: `Stage 1 - cache-adjusted cost normalization`
- Role: `Orc`
- Execution route: `direct`
- Source package: `V3-20260605-141503-token-cost-normalizer-v1`
- Related decisions:
  - [D-20260604-009](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-009)
  - [D-20260605-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-002)
- Created files:
  - [codex_token_cost_normalizer.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_cost_normalizer.py)
  - [token_pricing.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/config/token_pricing.json)
  - [test_codex_token_cost_normalizer.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_cost_normalizer.py)
- Updated files:
  - [token_cost_normalizer_v1_implementation_pack.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/drafts/token_cost_normalizer_v1_implementation_pack.md)
- Verification:
  - `python -m unittest tests.test_codex_token_cost_normalizer`
  - `python -m unittest tests.test_codex_token_cost_normalizer tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment`
  - `python scripts/codex_token_cost_normalizer.py --input-dir _local/codex-token-debugger/playwright-only-confirmation-20260604-072040 --out-dir _local/codex-token-debugger/playwright-only-confirmation-20260604-072040/token-cost-normalized --pricing config/token_pricing.json`
  - `git diff --check`
- Result:
  - added cache-adjusted normalization over sanitized parser outputs;
  - cost formulas now split non-cached input, cached input and output cost;
  - unknown model pricing stays explicit instead of being invented;
  - real smoke-run produced `token_cost_turns.jsonl`, `token_cost_sessions.json`, `token_cost_summary.json`, `token_cost_report.md` and `token_cost_dashboard_data.json`.
- Bugs and difficulties:
  - V3 draft test had a Python 3.14 compatibility bug around `importlib` + `dataclass`; fixed in both live test and implementation pack by registering the module in `sys.modules` before `exec_module`;
  - the draft markdown still contains mojibake in some Russian explanatory sections, but code/config/test extraction remained usable.
- Human verdict: `pending`

<a id="j-20260605-003"></a>

### J-20260605-003 - Codex Token Monitor Server v1 реализован, перепроверен и принят

- Этап жизненного цикла: `Stage 1 — token monitor MVP materialized`
- Роль: `Kilo Handoff Runner`
- Маршрут выполнения: `Handoff 0046`
- Ссылка на сессию: `2026-06-05_codex_token_monitor_server_v1`
- Related decisions: [D-20260605-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-003), [D-20260605-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-002)
- Созданные файлы:
  - [codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
  - [static/codex-token-monitor/index.html](/D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/index.html)
  - [static/codex-token-monitor/styles.css](/D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/styles.css)
  - [static/codex-token-monitor/app.js](/D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/app.js)
  - [codex_token_monitor_projects.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/config/codex_token_monitor_projects.json)
  - [start_codex_token_monitor.bat](/D:/Codex+Kilocode/projects/sword-of-rome-web/start_codex_token_monitor.bat)
  - [test_codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)
- Подтверждение:
  - реализован stdlib-only monitor server на `ThreadingHTTPServer` с API: `/api/status`, `/api/projects`, `/api/sessions`, `/api/session`, `/api/refresh`, `/api/archive`, `/api/unarchive`, `/api/shutdown`;
  - discovery сессий по run-папкам в `_local/codex-token-debugger/`, prefer normalized `token_cost_dashboard_data.json`;
  - static UI materialized как три файла, сохраняет compact dark layout prototype, работает только через API без demo data;
  - archive state хранится в `_local/codex-token-monitor/archive_state.json`;
  - refresh integrated с существующим `codex_token_cost_normalizer.py` как subprocess;
  - prompt/answer всегда возвращают `available=false` (тексты недоступны в normalized artifacts).
- Проверка:
  - `python -m unittest tests.test_codex_token_monitor_server tests.test_codex_token_cost_normalizer tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment` — 36 tests OK;
  - `git diff --check` — clean.
- Вердикт человека: `accepted after Codex review + local browser verification`
- Баги и сложности:
  - prompt/answer тексты недоступны в текущих normalized artifacts — это ожидаемое ограничение, а не баг;
  - monitor server не управляет OTel collector lifecycle — это best-effort status field в MVP.
- Следующий шаг:
  - использовать monitor как локальный слой просмотра нормализованных token-cost artifacts без новых OTel запусков.

## Bugs and difficulties

Текущий статус:

```text
found and fixed partly
```

Повторяющиеся process issues:

- `127.0.0.1` нельзя считать рабочим baseline для Codex OTel только потому, что ручной POST доходит;
- raw telemetry нельзя включать надолго без решения по чувствительным полям.

<a id="open-follow-ups"></a>

## Open follow-ups

- Если подпроект пойдет дальше, завести безопасный локальный file capture для сырого потока.
- Отдельно решить, какие поля маскировать до любого постоянного сбора.
- Не включать dashboard-этап, пока нет решения по raw capture и privacy.
