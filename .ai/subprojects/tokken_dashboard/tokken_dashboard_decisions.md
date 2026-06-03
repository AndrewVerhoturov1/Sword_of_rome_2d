# Tokken Dashboard Decisions

Slug: `tokken_dashboard`  
Owner: `Orc`  
Status: `active`  
Last updated: `2026-06-03`  
Decision layer: `subproject-level accepted decisions`

## Назначение

Этот файл хранит важные решения подпроекта `tokken_dashboard`.

Он нужен, чтобы быстро понять:

- какая локальная OTel-практика уже подтверждена;
- что не сработало и не должно считаться baseline;
- какие ограничения по безопасности уже обязательны;
- какие упрощения сделаны в текущем docs-only старте подпроекта.

## Accepted subproject decisions

### D-20260603-001 - Подпроект ведется как локальный OTel-only baseline без облаков

- Status: `accepted`
- Source: `user request + smoke-test result`
- Decision: `tokken_dashboard` фиксирует только локальные способы получения OTel/telemetry данных от Codex без подключения внешних сервисов.
- Reason: цель подпроекта - сначала научиться безопасно получать сырые данные локально и не отправлять ничего наружу.
- Consequence: любые следующие шаги внутри baseline должны оставаться локальными, без Grafana Cloud, SigNoz Cloud, LangSmith или других внешних приемников.
- Boundary: это решение не разрешает сразу строить dashboard или включать постоянную telemetry без отдельного human решения.
- Human approval: `recorded`

### D-20260603-002 - Рабочий baseline для Codex OTel: localhost + local OpenTelemetry Collector

- Status: `accepted`
- Source: `J-20260603-002`
- Decision: для текущего smoke-test baseline рабочим считать конфиг Codex с endpoint-ами через `http://localhost:4318/v1/logs`, `http://localhost:4318/v1/traces`, `http://localhost:4318/v1/metrics` и локальным OpenTelemetry Collector как приемником.
- Reason: именно эта комбинация реально дала входящие `Logs`, `Traces` и `Metrics` от Codex.
- Consequence: при следующей локальной проверке сначала повторять эту рабочую схему, а не возвращаться к неподтвержденным гипотезам.
- Boundary: это решение не говорит, что любой другой runtime, адрес или exporter формат тоже гарантированно сработает.
- Human approval: `recorded`

### D-20260603-003 - log_user_prompt должен оставаться false для локальных тестов

- Status: `accepted`
- Source: `user request + executed smoke-test`
- Decision: в локальных telemetry проверках подпроекта `log_user_prompt = false` считать обязательным безопасным минимумом.
- Reason: тест должен быть максимально безопасным и не должен расширять объем отправляемых prompt-данных.
- Consequence: если telemetry временно включается для следующей локальной проверки, этот флаг нужно держать выключенным для prompt logging.
- Boundary: это решение не гарантирует отсутствие других чувствительных полей в raw telemetry.
- Human approval: `recorded`

### D-20260603-004 - После smoke-test config возвращается в безопасное состояние

- Status: `accepted`
- Source: `J-20260603-002`
- Decision: временный `[otel]` блок после теста нужно удалять, а backup конфига сохранять.
- Reason: telemetry не должна оставаться включенной случайно после разовой диагностики.
- Consequence: рабочее состояние подпроекта после smoke-test - telemetry выключена, backup сохранен.
- Boundary: это решение не запрещает следующий локальный тест, но требует нового временного включения и нового cleanup.
- Human approval: `recorded`

## Superseded or corrected decisions

### S-20260603-001 - Гипотеза про 127.0.0.1 как normal baseline отменена

- Status: `corrected`
- Old rule: `127.0.0.1:4318` можно считать нормальным baseline endpoint для Codex OTel smoke-test.
- New rule: для этого подпроекта baseline считать `localhost`, а не `127.0.0.1`, пока не появится отдельное объяснение и подтверждение обратного.
- Reason: на `127.0.0.1` Codex стабильно получал `502`, хотя ручные POST доходили до локального приемника.
- Evidence: `J-20260603-001`, `J-20260603-002`

## Rejected options

### R-20260603-001 - Простой Python probe как основной приемник для Codex baseline

- Status: `rejected`
- Option: использовать только простой Python HTTP probe как достаточный приемник для smoke-test Codex OTel.
- Reason: probe был полезен как первичная проверка порта, но не подтвердил реальную доставку Codex OTel и не заменил Collector.
- Safe alternative: использовать локальный OpenTelemetry Collector с `otlp` receiver и `debug` exporter.

### R-20260603-002 - Постоянно включенная raw telemetry без фильтрации

- Status: `rejected`
- Option: оставить telemetry включенной после smoke-test и сразу собирать raw поток как есть.
- Reason: в сыром потоке уже замечены чувствительные поля уровня `user.email`, `user.account_id`, `conversation.id`.
- Safe alternative: перед постоянным сбором сделать локальную схему capture + redaction.

## Waivers

### W-20260603-001 - Упрощенный стартовый docset без plan_full, plan_index и status

- Status: `active`
- Waiver: подпроект стартует только с `readme`, `navigation`, `journal`, `decisions`.
- Reason: текущий запрос ограничен документированием уже полученного OTel baseline, без запуска большого planning/execution цикла.
- Remaining check: если подпроект пойдет в следующий этап, отдельно решить, нужен ли полный docset.
- Human approval: `recorded`

### W-20260603-002 - Локальный slug-format принят для этого подпроекта

- Status: `active`
- Waiver: внутри папки подпроекта используется canonical slug naming: `tokken_dashboard_*.md`.
- Reason: человек явно потребовал делать со слагом.
- Remaining check: при появлении новых файлов придерживаться того же naming.
- Human approval: `recorded`

## Relation to journal

Ключевые факты и проверка лежат в:

- [tokken_dashboard_journal.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md)

Этот файл хранит не историю команд, а только правила и решения, которые теперь считаются рабочими для подпроекта.

## Maintenance rule

- Не превращать этот файл в журнал команд.
- Не записывать сюда каждую временную гипотезу.
- Добавлять сюда только то, что стало правилом, запретом, waiver или устойчивым baseline.
- Если новый тест опровергнет текущий baseline, сначала зафиксировать факт в journal, потом обновить decision.
