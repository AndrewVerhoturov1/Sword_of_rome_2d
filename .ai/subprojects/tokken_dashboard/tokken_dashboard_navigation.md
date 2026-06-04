# Tokken Dashboard Navigation

Slug: `tokken_dashboard`  
Owner: `Orc`  
Status: `draft`  
Last updated: `2026-06-04`

## Quick Navigation

- [Purpose](#purpose)
- [Lifecycle Stage](#lifecycle-stage)
- [Start Here](#start-here)
- [Existing Documents](#existing-documents)
- [Planned Documents](#planned-documents)
- [Template Layer](#template-layer)
- [Local Evidence Files](#local-evidence-files)
- [Non-canonical Baseline](#non-canonical-baseline)
- [Reading Routes](#reading-routes)
- [Maintenance Rule](#maintenance-rule)

<a id="purpose"></a>

## Назначение

Карта подпроекта `tokken_dashboard`.

Здесь держим:

- ссылки на существующие документы подпроекта;
- текущий lifecycle stage;
- что читать человеку;
- что читать агенту;
- где лежат внешние локальные артефакты smoke-test;
- какие практики уже считаются рабочими;
- какие практики нельзя использовать как baseline.

Navigation не заменяет:

- `readme`;
- `journal`;
- `decisions`;
- будущий `plan_full`;
- будущий `status`.

<a id="lifecycle-stage"></a>

## Current lifecycle stage

```text
Stage 1 - tool environment + instruction inventory working
```

Gate state:

```text
Smoke-test подтвержден локально. Forensics parser работает. Tool/MCP Activity Inspector, MCP Schema Inventory, Effective MCP Inventory и Tool Environment Inventory разобрали sanitized A/B outputs/config metadata. Dashboard этап еще не утвержден человеком.
```

Stage warning:

```text
Не считать dashboard, постоянный telemetry pipeline или внешнюю интеграцию уже разрешенными. Сначала whitelist полей и sanitized schema.
```

## Active route

```text
Planner -> Orc
```

<a id="start-here"></a>

## Start here

### Human-first route

1. [tokken_dashboard_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md#purpose)
2. [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md#start-here)
3. [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions)
4. [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries)

### Agent route

1. [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md#reading-routes)
2. [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions)
3. [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries)
4. локальные smoke-test артефакты, если нужен raw evidence

### Planner route

1. [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions)
2. [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries)
3. локальные evidence-файлы smoke-test

<a id="existing-documents"></a>

## Existing documents

### Orc-owned documents

| File | Purpose | Audience |
|---|---|---|
| [tokken_dashboard_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md#purpose) | Human-first вход | human-first |
| [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md#purpose) | Карта подпроекта | human + agents |
| [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries) | Фактический журнал smoke-test | human + agents |
| [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions) | Важные решения и baseline rules | human + agents |

<a id="planned-documents"></a>

## Planned documents not created yet

| File | Planned stage | Notes |
|---|---|---|
| `tokken_dashboard_plan_full.md` | future planning stage | Нужен, если подпроект пойдет дальше baseline-docs |
| `tokken_dashboard_plan_index.md` | future planning stage | Нужен, если появится большой `plan_full` |
| `tokken_dashboard_status.md` | future execution stage | Нужен, если начнется живой многосеансовый execution цикл |

<a id="template-layer"></a>

## Reusable template layer

Template path:

```text
.ai/subprojects/templates/
```

Templates used as source:

- [subproject_readme_template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/templates/subproject_readme_template.md)
- [subproject_navigation_template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/templates/subproject_navigation_template.md)
- [subproject_journal_template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/templates/subproject_journal_template.md)
- [subproject_decisions_template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/templates/subproject_decisions_template.md)

Rule:

```text
Templates are reusable. Tokken_dashboard content should not rewrite template rules globally.
```

<a id="local-evidence-files"></a>

## Local evidence files

Collector and config evidence used by smoke-test:

- [config.toml](C:/Users/andre/.codex/config.toml)
- [config.toml.bak-otel-collector-smoke-20260603-211206](C:/Users/andre/.codex/config.toml.bak-otel-collector-smoke-20260603-211206)
- [collector-config.yaml](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/collector-config.yaml)
- [collector.stderr.log](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/collector.stderr.log)
- [run-127-separate-appserver.log](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/run-127-separate-appserver.log)
- [run-localhost-separate-appserver.log](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/run-localhost-separate-appserver.log)
- [run-localhost-separate-cli-exec.log](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/run-localhost-separate-cli-exec.log)
- [run-localhost-common-exporter-appserver.log](C:/Users/andre/.codex/tmp/otel-collector-smoke-20260603-210917/run-localhost-common-exporter-appserver.log)

Collector file exporter evidence:

- [collector-file-config.yaml](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/collector-file-config.yaml)
- [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json)
- [collector.stderr.log](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/collector.stderr.log)
- [config.toml.bak-otel-file-smoke-20260603-214412](C:/Users/andre/.codex/config.toml.bak-otel-file-smoke-20260603-214412)
- [_local/codex-token-debugger/smoke-20260603-r2](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/smoke-20260603-r2)
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02/experiment_manifest.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/experiment_manifest.json)
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02/runbook.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/runbook.md)
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/compare_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/compare_report.md)
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity/tool_mcp_activity_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity/tool_mcp_activity_report.md)
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/mcp_schema_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/mcp_schema_inventory_report.md)
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/effective_mcp_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/effective_mcp_inventory_report.md)
- [_local/codex-token-debugger/tool-environment-inventory-20260604-080502/reports/tool_environment_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080502/reports/tool_environment_inventory_report.md)
- [_local/codex-token-debugger/tool-environment-inventory-20260604-080635/reports/tool_environment_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080635/reports/tool_environment_inventory_report.md)
- [config.current-with-otel.toml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/config.current-with-otel.toml)
- [config.minimal-no-mcp-with-otel.toml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/config.minimal-no-mcp-with-otel.toml)
- [collector-A-current-config.yaml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/collector-A-current-config.yaml)
- [collector-B-minimal-config.yaml](C:/Users/andre/.codex/tmp/otel-ab-turn-cost-20260604-otab02/collector-B-minimal-config.yaml)
- [config.toml.bak-otel-ab-turn-cost-20260604-otab02](C:/Users/andre/.codex/config.toml.bak-otel-ab-turn-cost-20260604-otab02)

Important privacy finding:

```text
Raw OTel file contains token fields and sensitive fields. Treat codex-otel.json as local-only evidence.
Delete or mask user.email, user.account_id, conversation.id, host.name and sensitive authorization/cookie/api-key/password/secret fields before dashboard.
Keep prompt_length as diagnostic metadata. Keep prompt only when empty or already [REDACTED].
```

<a id="non-canonical-baseline"></a>

## Non-canonical / deprecated files

Не использовать как active baseline:

| File or practice | Why not canonical |
|---|---|
| `http://127.0.0.1:4318/v1/traces` | Давал `502`, Collector событий не получал |
| `http://127.0.0.1:4318/v1/logs` | Давал `502`, Collector событий не получал |
| Python probe как единственный приемник | Недостаточно для Codex smoke-test, потому что Codex ожидал поведение ближе к настоящему OTel Collector |
| Постоянно включенная telemetry после smoke-test | Не является safe default для этого подпроекта |

<a id="reading-routes"></a>

## Reading routes by need

| Need | Route |
|---|---|
| Быстро понять, что уже сработало | `readme` -> `decisions` |
| Проверить factual history | `journal` |
| Продолжить безопасную диагностику | `navigation` -> `decisions` -> `journal` -> local evidence files |
| Понять, почему `127.0.0.1` нельзя брать как baseline | [J-20260603-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260603-001) -> [S-20260603-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#s-20260603-001) |
| Строить parser/dashboard по raw OTel | [D-20260603-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-005) -> [J-20260603-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260603-004) -> [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json) |
| Продолжить A/B turn-cost experiment | [D-20260604-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-001) -> [J-20260604-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-001) -> [runbook.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/runbook.md) |
| Понять Tool/MCP activity в A/B results | [D-20260604-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-002) -> [J-20260604-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-002) -> [tool_mcp_activity_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/tool_mcp_activity/tool_mcp_activity_report.md) |
| Понять MCP schema inventory и ограничения schema size estimate | [D-20260604-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-003) -> [J-20260604-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-003) -> [mcp_schema_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/mcp_schema_inventory_report.md) |
| Проверить effective enabled MCP baseline перед group attribution | [D-20260604-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-004) -> [J-20260604-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-004) -> [effective_mcp_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/effective_mcp_inventory_report.md) |
| Отделить MCP servers от plugins и runtime/internal layers | [D-20260604-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-005) -> [J-20260604-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-005) -> [tool_environment_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080502/reports/tool_environment_inventory_report.md) |

| РџСЂРѕРІРµСЂРёС‚СЊ, РЅРµ Р»РµР¶РёС‚ Р»Рё overhead РІ skills/instructions/context | [D-20260604-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-006) -> [J-20260604-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-006) -> [tool_environment_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080635/reports/tool_environment_inventory_report.md) |

<a id="maintenance-rule"></a>

## Maintenance rule

- Обновлять `decisions`, когда временная находка становится рабочим правилом, запретом или waiver.
- После этого обновлять `journal`, если нужно зафиксировать конкретный факт, и ссылаться там на relevant decision anchor.
- Обновлять `navigation`, когда появляются новые canonical-файлы подпроекта или новые важные reading routes.
- Не считать внешние сервисы допустимыми, пока человек явно не разрешит это.
