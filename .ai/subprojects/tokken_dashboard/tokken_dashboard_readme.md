# Tokken Dashboard Readme

Slug: `tokken_dashboard`  
Owner: `Orc`  
Audience: human first  
Status: `draft`  
Lifecycle stage: `Stage 1 - tool/MCP activity inspector working`
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

Сейчас мы на этапе `Stage 1 - local forensics parser working`.

Уже подтверждено, что Codex читает `config.toml`, умеет включать OTel и реально отправляет локальные `logs`, `traces` и `metrics`, если endpoint задан через `localhost` и принимает их локальный OpenTelemetry Collector.

Также подтвержден локальный raw capture в файл через Collector `file` exporter:

- создан [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json);
- в файле есть `logs`, `traces`, `metrics`;
- найдены token usage поля;
- найдены чувствительные поля `user.email`, `user.account_id`, `conversation.id` и prompt metadata (`prompt`, `prompt_length`).

Поверх этого raw-файла уже работает локальный parser:

- есть [codex_token_debugger.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_debugger.py);
- parser выпускает sanitized `clean_events.jsonl`, `token_usage.jsonl`, `spans.jsonl`, `metrics.jsonl`, `sessions.jsonl`, `session_summary.json`, `warnings.jsonl`, `diagnostic_report.md`;
- текущий проверочный прогон лежит в local-only папке [_local/codex-token-debugger/smoke-20260603-r2](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2);
- parser уже показал видимые причины дорогого хода: `high_input_low_output`, `many_mcp_servers`, `tool_or_mcp_activity_near_expensive_turn`, `prompt_metadata_present`.
- подготовлен и разобран A/B experiment package для сравнения `current config` vs `minimal/no MCP config` по схеме `A1 -> A2 -> A3` и `B1 -> B2 -> B3`: [_local/codex-token-debugger/ab-turn-cost-20260604-otab02](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02).
- построен Tool/MCP Activity Inspector по sanitized A/B outputs: [tool_mcp_activity_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity/tool_mcp_activity_report.md).

Главные рабочие правила вынесены в:

- [D-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-002)
- [D-20260603-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-003)
- [D-20260603-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-004)
- [D-20260603-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-005)
- [D-20260603-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-007)
- [D-20260604-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-001)
- [D-20260604-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-002)

Еще не принято:

- постоянное локальное хранилище сырых событий;
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
- нет устойчивой схемы sanitized session key для аккуратных aggregate-сводок;
- нет утвержденного whitelist полей для будущего dashboard.

<a id="safe-next-step"></a>

## Current safe next step

```text
Следующий безопасный шаг: MCP inventory / schema size report. Нужно измерить, сколько tools дает каждый MCP server, какой размер у tool descriptions/schemas, и какие servers дают самый тяжелый schema/context payload. Dashboard все еще не делать.
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
- [_local/codex-token-debugger/smoke-20260603-r2](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2)
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02)
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity)

<a id="human-check"></a>

## Human check

1. Открой [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions).
2. Проверь, что там есть отдельные якорные решения [D-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-002) и [D-20260603-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-006).
3. Открой [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries).
4. Проверь, что у записей журнала есть `Related decisions`, а не отдельный пересказ тех же правил.
5. Если все верно, ответь: `tokken_dashboard anchors accepted`.
6. Если не верно, напиши, какой файл или какая ссылка ведет не туда.
