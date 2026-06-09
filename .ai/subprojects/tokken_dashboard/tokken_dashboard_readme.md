# Tokken Dashboard Readme

Slug: `tokken_dashboard`  
Owner: `Orc`  
Audience: human first  
Status: `draft`  
Lifecycle stage: `Stage 1 - hybrid monitor baseline accepted; audit truth-fix accepted; audit cumulative-accounting expansion pending`
Active route: `Planner -> Orc`

## Quick Navigation

- [Purpose](#purpose)
- [Why It Exists](#why-it-exists)
- [Current Status](#current-status)
- [Read First](#read-first)
- [Existing Documents](#existing-documents)
- [Reusable Template](#reusable-template)
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
- построен MCP Schema Inventory read-only по config metadata: [mcp_schema_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/mcp_schema_inventory_report.md). Настоящие tool schemas безопасно получить не удалось, поэтому `schema_available_server_count = 0`.
- построен Effective MCP Inventory audit: [effective_mcp_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory/effective_mcp_inventory_report.md). Он показал `12` configured sections, `6` effective enabled servers, `6` explicit disabled servers и `7` mismatch против старой current telemetry.
- построен Tool Environment Inventory: [tool_environment_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080502/reports/tool_environment_inventory_report.md). Physical MCP removal reduced observed MCP inventory from `13` to `3`, but did not reduce selected first-turn input tokens; diagnostics now must distinguish MCP servers, plugins, and runtime/internal tools.

Главные рабочие правила вынесены в:

- [D-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-002)
- [D-20260603-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-003)
- [D-20260603-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-004)
- [D-20260603-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-005)
- [D-20260603-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-007)
- [D-20260604-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-001)
- [D-20260604-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-002)
- [D-20260604-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-003)
- [D-20260604-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-004)
- [D-20260604-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-005)
- [D-20260604-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-006)
- [D-20260604-007](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-007)
- [D-20260604-008](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-008)

Еще не принято:

- постоянное локальное хранилище сырых событий;
- решение, нужен ли вообще dashboard на следующем шаге.

- РїРѕСЃС‚СЂРѕРµРЅ extended Tool Environment Inventory with skills/instructions metadata: [tool_environment_inventory_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/tool-environment-inventory-20260604-080635/reports/tool_environment_inventory_report.md). Inventory now also tracks `skills.config`, root `AGENTS.md`, root `README.md`, `.ai/**/*.md` and likely auto-loaded context candidates.
- [D-20260604-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-006)

Новые локальные контрольные артефакты этой серии:

- lean minimal baseline: [lean_minimal_confirmation_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/lean-minimal-confirmation-20260604-225228/reports/lean_minimal_confirmation_report.md)
- sequential model switch compare: [model_switch_sequential_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/model-switch-sequential-20260604-232818/reports/model_switch_sequential_report.md)
- local bundle of recent test packages: [codex-token-debugger-tests-from-lean-minimal-20260604.zip](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/bundles/codex-token-debugger-tests-from-lean-minimal-20260604.zip)
- future comparisons must use cache-adjusted and cost-aware reporting, not raw `input_tokens` alone: [D-20260604-009](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260604-009)

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

<a id="reusable-template"></a>

## Reusable template

- [tokken_dashboard_universal_context_cost_test_prompts_single_branch.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_universal_context_cost_test_prompts_single_branch.md#purpose) - canonical single-branch context-cost prompt scaffold for future tests.

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
Следующий безопасный шаг: не запускать новый OTel и не трогать source split. Сначала реализовать `Codex Token Monitor Audit` как отдельный verification layer: проверить source/session/step/usage/export truth, научиться явно помечать fallback и confidence, и только потом переходить к отдельному slice `Honesty hardening`.
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
- [_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/ab-turn-cost-20260604-otab02/compare/mcp_schema_inventory)

<a id="human-check"></a>

<a id="codex-token-monitor-server-v1"></a>

## Codex Token Monitor Server v1

`Codex Token Monitor Server v1` is the local browser UI layer for browsing normalized token-cost artifacts.

It provides:

- local web server on `127.0.0.1:8765` (stdlib-only, no extra dependencies);
- session discovery by run-folder identity in `_local/codex-token-debugger/`;
- compact dark UI with resizable split, collapsible left panel, step cards, archive/unarchive and shutdown;
- refresh integrated with `Token Cost Normalizer v1` as subprocess;
- archive state persisted in `_local/codex-token-monitor/archive_state.json`.

Start with [start_codex_token_monitor.bat](/D:/Codex+Kilocode/projects/sword-of-rome-web/start_codex_token_monitor.bat).

Monitor MVP is a local utility over normalized local artifacts, not a new OTel experiment. It does not manage collector lifecycle, does not modify live Codex config, and does not run new OTel captures.

Prompt/answer texts are currently unavailable in normalized artifacts — UI shows `not available` explicitly.

See [D-20260605-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-003) and [J-20260605-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260605-003).

<a id="codex-token-monitor-v2-next-step"></a>

## Codex Token Monitor v2 next step

`Codex Token Monitor v1` turned out to be a correct archive viewer, but not a browser of current live Codex chats.

Approved next route:

- keep v1 archive behavior for `_local/codex-token-debugger/**`;
- add a second explicit source for real Codex chats from `C:/Users/andre/.codex/**`;
- keep prompt/answer hidden by default, but show real text when it exists in local Codex artifacts;
- never present archive run-folders as if they were ordinary live chats.

Planning and routing artifacts:

- decision: [D-20260605-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260605-004)
- journal note: [J-20260605-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260605-004)
- implementation plan: [codex_token_monitor_v2_live_threads_implementation_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/drafts/codex_token_monitor_v2_live_threads_implementation_plan.md)

<a id="codex-token-monitor-current-state"></a>

## Codex Token Monitor current state

Current accepted baseline:

- monitor is now a hybrid local viewer with explicit `live` and `archive` sources;
- live timeline hides obvious technical synthetic prompts from the default user-facing step list;
- context compaction is visible in the live timeline as its own event;
- per-step live usage stays conservative: if request-local usage is not confirmed, monitor should show explicit absence rather than cumulative totals.

Current open follow-up:

- accepted `Codex Token Monitor Audit` truth layer is now in place;
- main audit truth gap is closed: fake verified evidence without explicit note is blocked;
- accepted cumulative-accounting layer is now also in place;
- next separate slice is still inside `Audit`: correct visible-step full-cost semantics so request cost is no longer confused with full visible-step cost;
- only after that move to `Honesty hardening` for human-facing wording, badges and explanation quality;
- optional later integration follow-up: ordinary UI/API request path may still be wired to provide `evidence_note` if the verified-evidence path needs to be reachable outside forensic/manual flows.

Current audit-expansion target:

- preserve the accepted truth layer, evidence-basis model, and cumulative-accounting layer;
- add per visible step:
  - `request_usage_items`
  - `full_step_usage`
  - `full_step_cost`
  - `primary_request_usage`
  - `cost_scope`
- reconcile:
  - full visible-step sums
  - latest cumulative session total
  - unmapped/internal usage
- verify that JSON/Markdown exports keep these fields together with `source_kind`, basis fields, warnings, confirmation semantics, and cumulative before/after fields.

External forensic audit update:

- current accepted interpretation is mixed-case, leaning real telemetry semantics, not a simple mapping bug;
- a very short first visible live prompt may still show large `cached_tokens`, because the request-level boundary can include hidden `system / developer / plugin / runtime` context before that visible prompt;
- the biggest remaining risk is not fake arithmetic by itself, but labels/export that look more certain than the underlying live evidence really is;
- accepted rich export direction:
  - `Copy` of one step = full step export;
  - `Session` = detailed session export;
  - `Selected JSON` = detailed selected-step JSON;
  - `Selected MD` = detailed selected-step Markdown.

See [D-20260606-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260606-001) and [J-20260606-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260606-001).
See also [D-20260607-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-001), [J-20260607-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260607-001), and [BUG-20260607-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/logs/bug_journal.md).
Implementation planning baseline for the next slice:
- [D-20260607-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-002)
- [D-20260607-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-003)
- [D-20260607-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-004)
- [D-20260607-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260607-005)
- [D-20260608-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260608-001)
- [J-20260607-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260607-002)
- [J-20260607-003](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260607-003)
- [J-20260607-004](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260607-004)
- [J-20260607-005](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260607-005)
- [J-20260608-001](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#j-20260608-001)
- [2026-06-07_V1-20260607-014953_detailed-implementation-plan-for-codex-token-monitor-audit.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_chats/notebook/2026-06-07_V1-20260607-014953_detailed-implementation-plan-for-codex-token-monitor-audit.md)

<a id="token-cost-normalizer-v1"></a>

## Token Cost Normalizer v1

`Token Cost Normalizer v1` is the next local layer after the sanitized Codex token parser and comparison tools.

It reads parsed artifacts such as:

- `parsed/token_usage.jsonl`
- `parsed/session_summary.json`
- `parsed/sessions.jsonl`
- optional nearby compare/confirmation summary JSON files

It writes cache-adjusted cost artifacts:

- `token_cost_turns.jsonl`
- `token_cost_sessions.json`
- `token_cost_summary.json`
- `token_cost_report.md`
- `token_cost_dashboard_data.json`

Important interpretation rule: future token comparisons must not use raw `input_tokens` alone. They must check `cached_tokens`, `non_cached_input_tokens`, `cached_ratio`, output/reasoning/tool tokens, model/reasoning switches and estimated cost from `config/token_pricing.json`.

Unknown model pricing is intentionally left unknown. The normalizer must not invent prices.

## Human check

1. Открой [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#accepted-decisions).
2. Проверь, что там есть отдельные якорные решения [D-20260603-002](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-002) и [D-20260603-006](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md#d-20260603-006).
3. Открой [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md#entries).
4. Проверь, что у записей журнала есть `Related decisions`, а не отдельный пересказ тех же правил.
5. Если все верно, ответь: `tokken_dashboard anchors accepted`.
6. Если не верно, напиши, какой файл или какая ссылка ведет не туда.
