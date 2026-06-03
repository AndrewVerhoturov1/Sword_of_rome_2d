# Tokken Dashboard Decisions

Slug: `tokken_dashboard`  
Owner: `Orc`  
Status: `active`  
Last updated: `2026-06-03`  
Decision layer: `subproject-level accepted decisions`

## Quick Navigation

- [Purpose](#purpose)
- [Accepted Decisions](#accepted-decisions)
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
- Privacy rule: перед dashboard или долговременным хранением удалять минимум `user.email`, `user.account_id`, `conversation.id`, `prompt`, `prompt_length`.
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
