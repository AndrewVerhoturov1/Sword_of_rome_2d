# Tokken Dashboard Journal

Slug: `tokken_dashboard`  
Owner: `Orc`  
Status: `active`  
Started: `2026-06-03`

## Назначение

Этот файл фиксирует фактические действия и результаты по локальной OTel-проверке для `tokken_dashboard`.

Журнал отвечает на вопрос:

```text
Что реально было проверено и что реально сработало?
```

Для долгоживущих правил и решений есть:

```text
tokken_dashboard_decisions.md
```

## Записи

### J-20260603-001 - Первый локальный probe подтвердил проблему baseline

- Этап жизненного цикла: `Stage 0 - local OTel baseline search`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
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

### J-20260603-002 - Локальный OpenTelemetry Collector подтвердил рабочий путь через localhost

- Этап жизненного цикла: `Stage 0 - local OTel baseline captured`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
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

Decision mirror:

```text
Рабочая практика и запреты из этого результата отражены в tokken_dashboard_decisions.md.
```

### J-20260603-003 - Создан базовый docset подпроекта tokken_dashboard

- Этап жизненного цикла: `Stage 0 - local OTel baseline documented`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
- Созданные файлы:
  - [tokken_dashboard_readme.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md)
  - [tokken_dashboard_navigation.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md)
  - [tokken_dashboard_journal.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md)
  - [tokken_dashboard_decisions.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md)
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

### J-20260603-004 - Collector file exporter подтвердил raw OTel capture в локальный файл

- Этап жизненного цикла: `Stage 0 - local raw OTel file capture confirmed`
- Роль: `Orc`
- Маршрут выполнения: `direct`
- Ссылка на сессию: `not available`
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
  - `prompt` и `prompt_length` тоже найдены, поэтому считаются чувствительными для parser/dashboard pipeline.
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
  - dashboard разрешать только после redaction слоя, который удаляет минимум `user.email`, `user.account_id`, `conversation.id`, `prompt`, `prompt_length`.

## Bugs and difficulties

Текущий статус:

```text
found and fixed partly
```

Повторяющиеся process issues:

- `127.0.0.1` нельзя считать рабочим baseline для Codex OTel только потому, что ручной POST доходит;
- raw telemetry нельзя включать надолго без решения по чувствительным полям.

## Open follow-ups

- Если подпроект пойдет дальше, завести безопасный локальный file capture для сырого потока.
- Отдельно решить, какие поля маскировать до любого постоянного сбора.
- Не включать dashboard-этап, пока нет решения по raw capture и privacy.
