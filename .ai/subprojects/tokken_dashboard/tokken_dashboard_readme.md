# Tokken Dashboard Readme

Slug: `tokken_dashboard`  
Owner: `Orc`  
Audience: human first  
Status: `draft`  
Lifecycle stage: `Stage 0 - local OTel baseline captured`  
Active route: `Planner -> Orc`

## Quick Navigation

- [Purpose](#purpose)
- [Why It Exists](#why-it-exists)
- [Current Status](#current-status)
- [Read First](#read-first)
- [Existing Documents](#existing-documents)
- [Missing Pieces](#missing-pieces)
- [Safe Next Step](#safe-next-step)
- [Role Warning](#role-warning)
- [Human Check](#human-check)

<a id="purpose"></a>

## Что это

`tokken_dashboard` - это подпроект для локального сбора и изучения сырых telemetry/OTel данных от Codex без облаков и без изменения кода приложения.

<a id="why-it-exists"></a>

## Зачем он существует

Практическая польза подпроекта:

- зафиксировать, как безопасно получать сырые OTel-события локально;
- не потерять рабочую конфигурацию после разового smoke-test;
- отделить проверенную практику от гипотез и неудачных попыток;
- подготовить основу для следующего шага: локальный raw capture, а потом уже решение, нужен ли dashboard.

<a id="current-status"></a>

## Текущий статус простыми словами

Сейчас мы на этапе `Stage 0 - local OTel baseline captured`.

Уже подтверждено, что Codex читает `config.toml`, умеет включать OTel и реально отправляет локальные `logs`, `traces` и `metrics`, если endpoint задан через `localhost` и принимает их локальный OpenTelemetry Collector.

Также подтвержден локальный raw capture в файл через Collector `file` exporter:

- создан [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json);
- в файле есть `logs`, `traces`, `metrics`;
- найдены token usage поля;
- найдены чувствительные поля `user.email`, `user.account_id`, `conversation.id`, `prompt`, `prompt_length`.

Главные рабочие правила вынесены в:

- [D-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-002)
- [D-20260603-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-003)
- [D-20260603-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-004)
- [D-20260603-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-005)

Еще не принято:

- постоянное локальное хранилище сырых событий;
- безопасная фильтрация чувствительных полей;
- решение, нужен ли вообще dashboard на следующем шаге.

<a id="read-first"></a>

## Что читать сначала

| Ситуация | Читать |
|---|---|
| Я человек и хочу быстро понять результат | [tokken_dashboard_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md#current-status), потом [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md#start-here) |
| Я хочу увидеть факты теста | [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries) |
| Я хочу увидеть, что теперь считается рабочим правилом | [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions) |
| Я агент и продолжаю работу | [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md#reading-routes) |

<a id="existing-documents"></a>

## Какие документы уже существуют

- [tokken_dashboard_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md#purpose) - human-first вход.
- [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md#purpose) - карта подпроекта.
- [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries) - фактический журнал проверки.
- [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions) - важные решения и правила по OTel baseline.

<a id="missing-pieces"></a>

## Чего еще нет

- нет `tokken_dashboard_plan_full.md`;
- нет `tokken_dashboard_plan_index.md`;
- нет `tokken_dashboard_status.md`;
- нет human acceptance по следующему этапу;
- нет локального постоянного файла с очищенным raw telemetry потоком.

<a id="safe-next-step"></a>

## Current safe next step

```text
Сделать локальный parser для codex-otel.json и redaction слой, который удаляет user.email, user.account_id, conversation.id, prompt и prompt_length до любого dashboard.
```

<a id="role-warning"></a>

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

<a id="human-check"></a>

## Human check

1. Открой [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions).
2. Проверь, что там есть отдельные якорные решения [D-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-002) и [D-20260603-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-006).
3. Открой [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries).
4. Проверь, что у записей журнала есть `Related decisions`, а не отдельный пересказ тех же правил.
5. Если все верно, ответь: `tokken_dashboard anchors accepted`.
6. Если не верно, напиши, какой файл или какая ссылка ведет не туда.
