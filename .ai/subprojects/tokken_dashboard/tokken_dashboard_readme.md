# Tokken Dashboard Readme

Slug: `tokken_dashboard`  
Owner: `Orc`  
Audience: human first  
Status: `draft`  
Lifecycle stage: `Stage 0 - local OTel baseline captured`  
Active route: `Planner -> Orc`

## Что это

`tokken_dashboard` - это подпроект для локального сбора и изучения сырых telemetry/OTel данных от Codex без облаков и без изменения кода приложения.

## Зачем он существует

Практическая польза подпроекта:

- зафиксировать, как безопасно получать сырые OTel-события локально;
- не потерять рабочую конфигурацию после разового smoke-test;
- отделить проверенную практику от гипотез и неудачных попыток;
- подготовить основу для следующего шага: локальный raw capture, а потом уже решение, нужен ли dashboard.

## Текущий статус простыми словами

Сейчас мы на этапе `Stage 0 - local OTel baseline captured`.

Уже подтверждено, что Codex читает `config.toml`, умеет включать OTel и реально отправляет локальные `logs`, `traces` и `metrics`, если endpoint задан через `localhost` и принимает их локальный OpenTelemetry Collector.

Также подтвержден локальный raw capture в файл через Collector `file` exporter:

- создан [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json);
- в файле есть `logs`, `traces`, `metrics`;
- найдены token usage поля;
- найдены чувствительные поля `user.email`, `user.account_id`, `conversation.id`, `prompt`, `prompt_length`.

Еще не принято:

- постоянное локальное хранилище сырых событий;
- безопасная фильтрация чувствительных полей;
- решение, нужен ли вообще dashboard на следующем шаге.

Следующий безопасный шаг - завести локальный raw capture без внешних сервисов и с явной маскировкой чувствительных полей.

## Что читать сначала

| Ситуация | Читать |
|---|---|
| Я человек и хочу быстро понять результат | `tokken_dashboard_readme.md`, потом `tokken_dashboard_navigation.md` |
| Я хочу увидеть факты теста | `tokken_dashboard_journal.md` |
| Я хочу увидеть, что теперь считается рабочим правилом | `tokken_dashboard_decisions.md` |
| Я агент и продолжаю работу | `tokken_dashboard_navigation.md` |

## Какие документы уже существуют

- `tokken_dashboard_readme.md` - human-first вход.
- `tokken_dashboard_navigation.md` - карта подпроекта.
- `tokken_dashboard_journal.md` - фактический журнал проверки.
- `tokken_dashboard_decisions.md` - важные решения и правила по OTel baseline.

## Чего еще нет

- нет `tokken_dashboard_plan_full.md`;
- нет `tokken_dashboard_plan_index.md`;
- нет `tokken_dashboard_status.md`;
- нет human acceptance по следующему этапу;
- нет локального постоянного файла с очищенным raw telemetry потоком.

## Current safe next step

```text
Сделать локальный parser для codex-otel.json и redaction слой, который удаляет user.email, user.account_id, conversation.id, prompt и prompt_length до любого dashboard.
```

## Role warning

- `Planner` отвечает за стратегию следующего этапа.
- `Orc` отвечает за execution evidence и локальные правила baseline.
- Человек утверждает, что делать дальше.
- Рекомендация агента не равна human approval.

## Non-canonical files

Сейчас нет отдельных legacy-файлов внутри `tokken_dashboard`.

Временные локальные артефакты smoke-test не считать активной документацией подпроекта:

- [collector.stderr.log](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/collector.stderr.log)
- [collector-config.yaml](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/collector-config.yaml)
- [config.toml.bak-otel-collector-smoke-20260603-211206](C:/Users/andre/.codex/config.toml.bak-otel-collector-smoke-20260603-211206)
- [collector-file-config.yaml](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/collector-file-config.yaml)
- [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json)
- [config.toml.bak-otel-file-smoke-20260603-214412](C:/Users/andre/.codex/config.toml.bak-otel-file-smoke-20260603-214412)

## Human check

1. Открой [tokken_dashboard_journal.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md).
2. Убедись, что там явно написано: `127.0.0.1` не сработал, а `localhost` сработал.
3. Открой [tokken_dashboard_decisions.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md).
4. Убедись, что рабочая практика описана как локальная, без облаков.
5. Если все верно, ответь: `tokken_dashboard docs accepted`.
6. Если не верно, напиши, что именно поправить.
