# Handoff 0046: Codex Token Monitor Server v1

## Статус

Готово для Kilo

## Рекомендуемый Kilo mode

kilo-handoff-runner

## Task role

Builder Agent

## Task profile

small-code

## Execution mandate

`agent-first`

## Primary execution path

`Kilo Code`

## Allowed agent kinds

- `Kilo Code`

## Default preference

Локальный implementation run через `Kilo Code`: нужны реальные file edits, новый stdlib server, static UI, config, tests и docs updates внутри repo.

## Exception status

`none`

## Minimum substantive agent work

Substantive run засчитывается только если Kilo реально:

- materialize-ит monitor MVP в repo, а не только пишет план или report;
- строит backend server + static UI + config + startup bat + tests;
- подключает UI к реальным local artifacts через JSON API;
- использует существующий `codex_token_cost_normalizer.py`, а не дублирует его логику;
- обновляет docs подпроекта под новый monitor layer;
- прогоняет проверки из handoff и честно фиксирует результат.

Одного анализа без изменения файлов недостаточно.

## Sequential agent policy

Только один run по этому handoff: один запуск -> report -> review Codex. Никаких параллельных агентов.

## If no agent path fits -> return escalation note

Если реализация упирается в неясность контракта или прототипа:

- не расширять scope самовольно;
- не изобретать новую архитектуру вместо сохраненного плана;
- зафиксировать blocker в report;
- предложить 2-4 узких candidate next steps.

## Session plan

[2026-06-05_codex_token_monitor_server_v1.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-06-05_codex_token_monitor_server_v1.md)

## Plan item

`P1: Materialize monitor MVP`

## Session run

`002`

## Рекомендуемый класс модели

fast_coding_model

## Default model

Qwen3 Coder 480B

## Fallback model или Candidate models

- Qwen3 Coder Next
- DeepSeek V4 Pro

## Когда эскалировать в strong_model

- если stdlib-only server contract начинает конфликтовать с реальной data-adapter логикой;
- если без архитектурного пересмотра нельзя совместить prototype UX и local artifact model;
- если task начинает требовать нового workflow/OTel experiment вместо local monitor utility;
- если fast_coding_model не справляется с целостной реализацией server + UI + tests.

## Уровень риска

Средний

## Цель

Реализовать `Codex Token Monitor Server v1` по сохраненному plan artifact как локальную MVP-утилиту поверх уже существующих `_local/codex-token-debugger/*` артефактов и `Token Cost Normalizer v1`.

Нужный итог:

- новый stdlib server [codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py);
- materialized static UI в `static/codex-token-monitor/`, максимально близкий к принятому prototype;
- project config [codex_token_monitor_projects.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/config/codex_token_monitor_projects.json);
- startup script [start_codex_token_monitor.bat](/D:/Codex+Kilocode/projects/sword-of-rome-web/start_codex_token_monitor.bat);
- unit test [test_codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py);
- docs updates в `tokken_dashboard`;
- без новых OTel запусков и без изменения live Codex config.

## Current state

Уже готово:

- planning artifact: [codex_token_monitor_server_v1_implementation_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/drafts/codex_token_monitor_server_v1_implementation_plan.md)
- normalizer baseline:
  - [codex_token_cost_normalizer.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_cost_normalizer.py)
  - [token_pricing.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/config/token_pricing.json)
  - [test_codex_token_cost_normalizer.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_cost_normalizer.py)
- prototype source of truth:
  - `C:/Users/andre/Downloads/codex_token_monitor_compact_archive_prototype.html`

Пока отсутствуют:

- monitor server;
- static monitor UI files;
- monitor project config;
- startup bat;
- monitor tests;
- docs updates про monitor MVP.

## Required Inputs

- [AGENTS.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/AGENTS.md)
- [codex_token_monitor_server_v1_implementation_plan.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/drafts/codex_token_monitor_server_v1_implementation_plan.md)
- [codex_token_cost_normalizer.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_cost_normalizer.py)
- [token_pricing.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/config/token_pricing.json)
- [test_codex_token_cost_normalizer.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_cost_normalizer.py)
- [tokken_dashboard_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md)
- [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md)
- [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md)
- [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md)
- sample normalized artifact:
  - [_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/token-cost-normalized/token_cost_dashboard_data.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/token-cost-normalized/token_cost_dashboard_data.json)
- sample parsed artifacts:
  - [_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/parsed/token_usage.jsonl](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/parsed/token_usage.jsonl)
  - [_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/parsed/session_summary.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/parsed/session_summary.json)
- prototype file:
  - `C:/Users/andre/Downloads/codex_token_monitor_compact_archive_prototype.html`

## Policy Inputs

- [.ai/policies/language_policy.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/policies/language_policy.md)
- [.ai/policies/human_review_policy.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/policies/human_review_policy.md)
- [.ai/policies/bug_tracking_policy.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/policies/bug_tracking_policy.md)
- [.ai/logs/bug_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/logs/bug_journal.md) if a repeatable bug/blocker appears

## Language Policy Expectation

- user-facing UI text на русском;
- internal technical identifiers на английском;
- JSON keys, ids, schema names, API fields only in English;
- не транслитерировать технические идентификаторы.

## Human Check Expectation

required

В конце report дай простую проверку для человека:

- запустить [start_codex_token_monitor.bat](/D:/Codex+Kilocode/projects/sword-of-rome-web/start_codex_token_monitor.bat);
- дождаться открытия локальной страницы monitor;
- убедиться, что слева виден список запусков, а справа открывается выбранная сессия;
- нажать кнопку архивации/разархивации для одной сессии, если она есть;
- нажать shutdown button и убедиться, что окно/сервер завершаются штатно;
- прислать ответ, что открылось и что не сработало, если что-то сломалось.

## Bug Tracking Expectation

- report must include `Баги и сложности`;
- перед отладкой повторяемой проблемы проверить [bug_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/logs/bug_journal.md);
- verification must be concrete;
- если human check потом провалится, считать это реальным follow-up bug.

## Required Report Sections

- `Краткий итог`
- `Что именно изменено`
- `Verification`
- `Human Check`
- `Баги и сложности`
- `Runtime metadata`

## Lookup Inputs

- [README.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/README.md)
- [.ai/repo_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/repo_navigation.md)
- [_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/token-cost-normalized/token_cost_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger/playwright-only-confirmation-20260604-072040/token-cost-normalized/token_cost_report.md)

## Do Not Read Unless Blocked

- `.ai/external_chats/**`
- `.ai/external_reviews/**`
- `src/**` product code unrelated to monitor utility
- `canon/**`
- `references/**`
- `docs/**`
- `output/**`
- bulk `_local/**` scanning beyond files directly needed for sample data and runtime discovery logic

## Context Budget

- Сначала прочитай planning artifact и normalizer files.
- Потом проверь prototype HTML и один-два sample artifact files.
- Не уходи в новый telemetry research.
- Не превращай monitor MVP в новый diagnostics framework.
- UI materialize-ить близко к prototype, но без demo data.

## Allowed Changes

- [codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- [codex_token_monitor_projects.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/config/codex_token_monitor_projects.json)
- [start_codex_token_monitor.bat](/D:/Codex+Kilocode/projects/sword-of-rome-web/start_codex_token_monitor.bat)
- `static/codex-token-monitor/**`
- [test_codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)
- [tokken_dashboard_readme.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md)
- [tokken_dashboard_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md)
- [tokken_dashboard_journal.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md)
- [tokken_dashboard_decisions.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md)
- один новый report:
  - [0046_codex_token_monitor_server_v1_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0046_codex_token_monitor_server_v1_report.md)

## Forbidden Changes

- не менять live Codex config в `C:/Users/andre/.codex/**`;
- не запускать новый OTel collector/run;
- не менять `_local/codex-token-debugger/**` артефакты, кроме допустимого runtime archive state в новом `_local/codex-token-monitor/`;
- не коммитить `_local/**` outputs;
- не трогать product code варгейма вне monitor utility;
- не делать dashboard redesign вне prototype-bound MVP;
- не добавлять новые Python dependencies;
- не писать UI на demo data;
- не делать commit/push.

## File writing policy

Используй нормальные file edits. Не записывай большие файлы через shell text dump.

## Точная задача

Реализуй `Codex Token Monitor Server v1` по сохраненному plan artifact.

### 1. Backend

Создай stdlib-only server с API:

- `GET /`
- `GET /api/status`
- `GET /api/projects`
- `GET /api/sessions?project_id=...`
- `GET /api/session?project_id=...&session_id=...`
- `POST /api/refresh`
- `POST /api/archive`
- `POST /api/unarchive`
- `POST /api/shutdown`

Используй `ThreadingHTTPServer`. Shutdown делай через delayed `server.shutdown()` после JSON response.

### 2. Discovery and refresh

- source of projects: `config/codex_token_monitor_projects.json`
- session identity = имя run-папки
- valid session если есть normalized dashboard data или хотя бы `parsed/token_usage.jsonl`
- refresh должен best-effort вызывать `scripts/codex_token_cost_normalizer.py`, если normalized output отсутствует или устарел
- archive state хранить в `_local/codex-token-monitor/archive_state.json`

### 3. UI adapter contract

Server должен возвращать session model с:

- metadata
- summary
- steps
- `user_prompt`
- `assistant_answer`
- `usage`
- `environment`
- `warnings`

Если prompt/answer недоступны, возвращай `available=false`, `text=""`. Ничего не выдумывай.

### 4. Static UI

Разбей prototype на:

- `static/codex-token-monitor/index.html`
- `static/codex-token-monitor/styles.css`
- `static/codex-token-monitor/app.js`

Сохрани layout и visual direction prototype максимально близко:

- compact dark style
- resizable split
- collapsible left block
- archived sessions
- step cards
- hidden prompt/answer by default
- shutdown button

UI должен работать только через API.

### 5. Startup and docs

- добавь `start_codex_token_monitor.bat`
- обнови 4 docs файла `tokken_dashboard`
- зафиксируй, что monitor MVP — local utility over normalized artifacts, не новый OTel experiment

### 6. Tests and verification

Добавь `tests/test_codex_token_monitor_server.py` и покрой минимум:

- project config loads
- invalid path warning without crash
- discovery prefers normalized data
- missing normalized output fallback without crash
- refresh stub
- archive/unarchive persistence
- archived hiding by default
- status payload shape
- absent prompt/answer contract
- shutdown endpoint behavior

Прогони:

```powershell
python -m unittest tests.test_codex_token_monitor_server tests.test_codex_token_cost_normalizer tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment
git diff --check
```

Если получится, сделай еще один local smoke check запуска server script без долгоживущего зависания и зафиксируй результат в report.

## Acceptance Criteria

- server script создан и отвечает по API contract;
- static UI materialized и не использует demo data;
- sessions строятся по run-folder identity;
- archive/unarchive работает через local state file;
- refresh интегрирован с existing normalizer;
- tests добавлены и проходят, либо честно зафиксирован точный blocker;
- docs обновлены;
- report написан по required sections;
- никаких новых OTel run и никаких изменений live Codex config.

## Report mode

`full`

## Куда записать report

[0046_codex_token_monitor_server_v1_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0046_codex_token_monitor_server_v1_report.md)
