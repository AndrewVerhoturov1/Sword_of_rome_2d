# Tokken Dashboard Navigation

Slug: `tokken_dashboard`  
Owner: `Orc`  
Status: `draft`  
Last updated: `2026-06-07`

## Quick Navigation

- [Purpose](#purpose)
- [Lifecycle Stage](#lifecycle-stage)
- [Start Here](#start-here)
- [Existing Documents](#existing-documents)
- [Planned Documents](#planned-documents)
- [Reusable Test Templates](#reusable-test-templates)
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
Stage 1 - hybrid monitor baseline accepted; audit implementation pending; honesty hardening deferred
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
| [public_forensics/live_monitor_audit_019e9d2a/README.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/README.md) | Publishable forensic-pack for live monitor audit thread `019e9d2a...` | external chats + agents |
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

<a id="reusable-test-templates"></a>

## Reusable test templates

- [tokken_dashboard_universal_context_cost_test_prompts_single_branch.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_universal_context_cost_test_prompts_single_branch.md)

Rule:

```text
Canonical reusable prompt scaffolds for Token Debugger context-cost experiments should live inside the subproject and be linked from navigation, not left only in ad hoc external folders.
```

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

| Lean minimal baseline for current token diagnostics | [D-20260604-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-007) -> [J-20260604-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-007) -> [lean_minimal_confirmation_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/lean-minimal-confirmation-20260604-225228/reports/lean_minimal_confirmation_report.md) |
| Sequential model-switch compare after rejecting the parallel attempt | [D-20260604-008](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-008) -> [J-20260604-008](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-008) -> [model_switch_sequential_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/model-switch-sequential-20260604-232818/reports/model_switch_sequential_report.md) |
| Перейти от raw input к cache-adjusted и cost-aware token comparisons | [D-20260604-009](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-009) -> [J-20260604-009](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-009) -> [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-009) |
| Local bundle of test artifacts starting from lean minimal | [J-20260604-008](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260604-008) -> [codex-token-debugger-tests-from-lean-minimal-20260604.zip](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/bundles/codex-token-debugger-tests-from-lean-minimal-20260604.zip) |

Additional route:

- Open the canonical reusable scaffold for future single-branch context-cost tests:
  [D-20260605-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-001) ->
  [J-20260605-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260605-001) ->
  [tokken_dashboard_universal_context_cost_test_prompts_single_branch.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_universal_context_cost_test_prompts_single_branch.md#purpose)

- Open the publishable live-monitor forensic pack for external audit:
  [README.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/README.md) ->
  [manifest.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/manifest.json) ->
  [live_rollout_redacted.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/live_rollout_redacted.jsonl) ->
  [live_session_detail.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/live_session_detail.json) ->
  [live_session_export.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/live_session_export.md) ->
  [2026-06-07_V1-20260607-live-monitor-audit-r2_forensic-audit-of-live-token-monitor.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_chats/notebook/2026-06-07_V1-20260607-live-monitor-audit-r2_forensic-audit-of-live-token-monitor.md)

<a id="maintenance-rule"></a>

<a id="token-cost-normalizer-v1"></a>

## Token Cost Normalizer v1

- Draft implementation pack: [token_cost_normalizer_v1_implementation_pack.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/drafts/token_cost_normalizer_v1_implementation_pack.md)
- Live script: [codex_token_cost_normalizer.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_cost_normalizer.py)
- Live pricing config: [token_pricing.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/config/token_pricing.json)
- Live test: [test_codex_token_cost_normalizer.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_cost_normalizer.py)
- Example smoke-run output: [_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/token-cost-normalized](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/token-cost-normalized)

Purpose: cache-adjusted token and estimated-cost normalization over sanitized parser outputs.

<a id="codex-token-monitor-server-v1"></a>

## Codex Token Monitor Server v1

- Implementation plan: [codex_token_monitor_server_v1_implementation_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/drafts/codex_token_monitor_server_v1_implementation_plan.md)
- Live server: [codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- Static UI: [static/codex-token-monitor/](/D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/)
- Project config: [codex_token_monitor_projects.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/config/codex_token_monitor_projects.json)
- Startup: [start_codex_token_monitor.bat](/D:/Codex+Kilocode/projects/sword-of-rome-web/start_codex_token_monitor.bat)
- Live test: [test_codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)
- Archive state: `_local/codex-token-monitor/archive_state.json`

Purpose: local browser UI over normalized token-cost artifacts. Session discovery by run-folder identity, step cards, archive/unarchive, refresh via existing normalizer.

Route: Open the monitor: [D-20260605-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-003) -> [J-20260605-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260605-003) -> [start_codex_token_monitor.bat](/D:/Codex+Kilocode/projects/sword-of-rome-web/start_codex_token_monitor.bat)

## Codex Token Monitor v2 planning route

- Decision: [D-20260605-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-004)
- Journal: [J-20260605-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260605-004)
- Implementation plan: [codex_token_monitor_v2_live_threads_implementation_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/drafts/codex_token_monitor_v2_live_threads_implementation_plan.md)
- Session plan: [2026-06-05_codex_token_monitor_v2_live_threads.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-06-05_codex_token_monitor_v2_live_threads.md)
- Kilo handoff: [0047_codex_token_monitor_v2_live_threads.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/handoffs/0047_codex_token_monitor_v2_live_threads.md)

Current approved route:

```text
Keep v1 as the archive viewer. Build v2 as a hybrid monitor with two explicit sources: real Codex chats from C:/Users/andre/.codex and archival OTel test runs from _local/codex-token-debugger.
```

## Codex Token Monitor next follow-up

- Decision: [D-20260606-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260606-001)
- Journal: [J-20260606-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260606-001)
- Current live server: [codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- Current UI: [static/codex-token-monitor/](/D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/)
- Current test: [test_codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

Focused next route:

```text
Do not reopen the source split. The next execution slice is Codex Token Monitor Audit: keep the hybrid baseline, verify source/session/step/usage/export truth, and emit audit statuses/artifacts before any wider honesty-hardening pass.
```

New safe reading route:

```text
Read D-20260606-001 -> D-20260607-001 -> D-20260607-002 -> J-20260607-002 -> V1-20260607-014953 notebook entry -> BUG-20260607-001 before implementing the audit layer.
```

Additional planning route:

```text
If task is "implement Audit", use the notebook entry V1-20260607-014953 as planning baseline, then local repo files as source of truth for exact file placement, API shape and tests.
```

## Maintenance rule

- Обновлять `decisions`, когда временная находка становится рабочим правилом, запретом или waiver.
- После этого обновлять `journal`, если нужно зафиксировать конкретный факт, и ссылаться там на relevant decision anchor.
- Обновлять `navigation`, когда появляются новые canonical-файлы подпроекта или новые важные reading routes.
- Не считать внешние сервисы допустимыми, пока человек явно не разрешит это.
