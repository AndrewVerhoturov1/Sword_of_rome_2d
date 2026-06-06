# Bug Journal

This journal records important, repeated, or non-obvious bugs and difficulties found during project work.

Use it so future agents can check whether a similar issue already happened and how it was solved.

Do not record every tiny typo. Record issues that may help future debugging.

## Entries

### BUG-20260607-001 - Live monitor may overstate certainty for cached tokens and step attribution

Status: open

Area:
`scripts/codex_token_monitor_server.py`, `static/codex-token-monitor/app.js`, live monitor semantics/export

Symptoms:
- короткий первый видимый шаг live-чата может показывать очень большой `Cached` и `Cache ratio`, как будто кэш относится только к видимому prompt;
- summary и шаги выглядят одинаково точными, хотя у них разная semantic basis;
- подписи вроде `confirmed_request_usage` и `Cost confirmed: yes` могут звучать сильнее, чем реально позволяет live telemetry.

Observed recurrence:
- confirmed on forensic thread `019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f`;
- external audit notebook entry `V1-20260607-live-monitor-audit-r2` classified this as mixed case leaning real telemetry semantics, not simple mapping bug.

Cause:
- live per-step usage для видимого шага берётся из request-level `last_token_usage`, и это похоже на реальную telemetry semantics;
- первый видимый шаг не равен cold-start request: в live rollout перед видимым prompt есть большой скрытый `system / developer / plugin / runtime` context;
- monitor всё ещё может выглядеть слишком уверенно, потому что UI/export не везде ясно отделяют:
  - `first visible step` от полного provider request;
  - `request-level usage found` от точной привязки всех токенов к видимой карточке;
  - `usage source confirmed` от `cost estimated from local pricing`;
  - `session cumulative totals` от `visible step totals`.

Fix:
- not fixed yet;
- next implementation slice should build `Codex Token Monitor Audit` first, so monitor can verify source/session/step/usage/export truth before wider human-facing wording changes;
- future fix should keep current live/archive split, but make semantics more explicit in UI/export;
- especially important:
  - label first live step as first visible step, not implicit cold start;
  - warn that cached input may include hidden/system/runtime context;
  - never present cumulative fallback as confirmed per-step usage;
  - separate confirmed usage source from estimated cost wording;
  - fix export warning mojibake if still present.

Verification:
- external audit reviewed published forensic pack and recorded verdict in:
  - [2026-06-07_V1-20260607-live-monitor-audit-r2_forensic-audit-of-live-token-monitor.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_chats/notebook/2026-06-07_V1-20260607-live-monitor-audit-r2_forensic-audit-of-live-token-monitor.md)
- local published artifacts referenced by that audit:
  - [README.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/README.md)
  - [live_rollout_redacted.jsonl](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/live_rollout_redacted.jsonl)
  - [live_session_detail.json](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/public_forensics/live_monitor_audit_019e9d2a/live_session_detail.json)
- tests not run for this journal-only update.

Human check:
not needed

Related files:
- [bug_journal.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/logs/bug_journal.md)
- [codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- [app.js](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/app.js)
- [2026-06-07_V1-20260607-live-monitor-audit-r2_forensic-audit-of-live-token-monitor.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_chats/notebook/2026-06-07_V1-20260607-live-monitor-audit-r2_forensic-audit-of-live-token-monitor.md)

Notes for future agents:
- `cached_tokens` on first visible live step is not enough evidence of mapping bug by itself;
- treat this as semantics/communication risk first, arithmetic bug second;
- if a later fix changes wording or confidence flags, verify both UI and export, not only backend JSON.

### BUG-20260606-009 - Monitor defaulted to empty live chat and showed infinite loading instead of honest no-steps state

Status: fixed

Area:
`static/codex-token-monitor/app.js`

Symptoms:
- после открытия монитора мог автоматически выбраться самый свежий live-чат без распарсенных шагов;
- справа висело `Загрузка шагов...`, хотя запрос уже завершился и шагов для этой сессии просто не было;
- пользователю казалось, что чат не открывается вообще.

Observed recurrence:
- повторилось на `http://127.0.0.1:8765/` после фикса списка сессий, когда вверху live-ленты были чаты со `step_count = null`.

Cause:
- стартовый выбор брал просто первую сессию из списка, даже если у неё не было шагов;
- UI не отличал состояние `detail ещё грузится` от состояния `detail загружен, но steps пусты`.

Fix:
- добавлен `preferredSessionId(...)`, который по умолчанию предпочитает сессию с `step_count > 0`;
- для смены фильтров и клика по карточке добавлен явный loading-state;
- пустой detail теперь показывает честный текст `Для этой сессии шаги пока не найдены`, а не бесконечную загрузку.

Verification:
- `python -m unittest tests.test_codex_token_monitor_server`
- browser smoke на `http://127.0.0.1:8765/` показал много live-сессий вместо одной;
- API для первой видимой пустой сессии вернул `steps = 0`, что подтвердило именно UX-проблему, а не зависший запрос.

Human check:
required - обновить монитор и убедиться, что по умолчанию открывается чат со шагами, а для пустого чата справа честно написано, что шаги не найдены.

Related files:
- [app.js](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/app.js)
- [test_codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

### BUG-20260606-008 - Session list render crashed because step timeline code leaked into renderSessions

Status: fixed

Area:
`static/codex-token-monitor/app.js`

Symptoms:
- в левой колонке мог показываться только один чат, хотя API возвращал много сессий;
- при клике по единственной карточке справа оставалось `Выберите сессию слева` или шаги не открывались;
- источник и фильтры выглядели живыми, но detail не догружался.

Observed recurrence:
- повторилось на live monitor `http://127.0.0.1:8765/` после добавления timeline-событий сжатия контекста.

Cause:
- в `renderSessions()` случайно остался кусок кода из `renderSteps()`;
- список сессий пытался читать `timelineByStep` и `idx`, которых в этом scope нет;
- после первого `root.appendChild(el)` происходил `ReferenceError`, и рендер обрывался на первой карточке.

Fix:
- удалён stray timeline-render block из `renderSessions()`;
- добавлен frontend contract test, чтобы `renderSessions()` больше не зависел от step timeline state.

Verification:
- `python -m unittest tests.test_codex_token_monitor_server`
- `node --check static/codex-token-monitor/app.js`
- live API smoke показывал много сессий, а после refresh UI снова мог открыть detail выбранного чата.

Human check:
required - обновить монитор, убедиться что слева виден не один чат, а список, и что клик по карточке реально открывает шаги справа.

Related files:
- [app.js](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/app.js)
- [test_codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

### BUG-20260606-007 - Live step lost valid last_token_usage because step closed after compaction cycle

Status: fixed

Area:
`scripts/codex_token_monitor_server.py`, `static/codex-token-monitor/app.js`

Symptoms:
- some real live chat steps showed `no confirmed last_token_usage for this step` even though rollout contained valid `last_token_usage` during the same visible turn;
- after context compaction the monitor did not show where compaction happened;
- user could not see whether the missing usage came from true interruption or from monitor mis-grouping.

Observed recurrence:
- repeated on live thread `019e8e29-ed90-71d3-86b0-90bb7a3c4d00`, especially around visible `Step 4`.

Cause:
- live step stayed open until the next visible user message;
- rollout could emit `task_complete`, then a separate compaction mini-cycle with zero `last_token_usage`, then `context_compacted`, and only after that another user prompt;
- the zero compaction-cycle usage overwrote the real request usage of the previous visible step.

Fix:
- visible live step now finalizes on `task_complete`, not only on the next visible user prompt;
- `context_compacted` is exposed as a dedicated timeline event after the previous visible step;
- previous step gets a badge `контекст сжат после этого хода`;
- compaction event includes available task/turn identifiers from rollout.

Verification:
- `python -m unittest tests.test_codex_token_monitor_server`
- live rollout inspection around visible `Step 4` showed valid `last_token_usage`, then `task_complete`, then separate `context_compacted` cycle with zero usage.

Human check:
required - open the same live chat and verify:
- the previously missing step now has token/cost data if rollout had valid `last_token_usage`;
- after a compaction point there is a separate `Сжатие контекста` event in the timeline;
- the previous step shows badge `контекст сжат после этого хода`.

Related files:
- [codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- [app.js](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/app.js)
- [styles.css](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/styles.css)
- [test_codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

### BUG-20260606-006 - Live monitor used session totals instead of request usage for visible step cost

Status: fixed

Area:
`scripts/codex_token_monitor_server.py`

Symptoms:
- a very short live message such as `все хорошо` could show millions of input tokens on a single visible step;
- step cost looked like cost of a huge hidden chain, not cost of the concrete user-visible request;
- the session summary looked plausible, but per-step live numbers were wildly inflated.

Observed recurrence:
- reproduced on the live thread `019e8e29-ed90-71d3-86b0-90bb7a3c4d00` in Codex Token Monitor.

Cause:
- live step builder was reading `event_msg.payload.info.total_token_usage` for the step;
- `total_token_usage` is cumulative for the whole thread/session state, not request-local usage for one request cycle;
- after hiding synthetic internal prompts, the delta between visible steps could still absorb a large hidden execution tail and make a short human message look absurdly expensive.

Fix:
- live step builder now prefers `event_msg.payload.info.last_token_usage` for visible step usage;
- if confirmed `last_token_usage` is absent, the step stays unavailable instead of reusing cumulative totals;
- tests now cover the realistic case where `total_token_usage` is huge but `last_token_usage` for the concrete step is small.

Verification:
- `python -m unittest tests.test_codex_token_monitor_server`
- live rollout inspection showed:
  - `total_token_usage` around millions on late turns;
  - `last_token_usage` around the actual request-sized numbers for the concrete step.

Human check:
required - reopen the same live chat in the monitor and confirm that a short message no longer shows multi-million input tokens for the visible step. If the step has no confirmed `last_token_usage`, it should show `—` instead of a fake giant number.

Related files:
- [codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- [test_codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

### BUG-20260606-005 - Live monitor mixed technical synthetic turns with real user chat steps

Status: fixed

Area:
`scripts/codex_token_monitor_server.py`

Symptoms:
- live chat steps included internal prompts like `PLEASE IMPLEMENT THIS PLAN:` and `<turn_aborted>` as if they were normal user messages;
- this made the visible step list look wrong even when token deltas themselves were technically derived from real rollout checkpoints;
- user-facing step numbering no longer matched the human chat history.

Observed recurrence:
- repeated on the live thread `019e8e29-ed90-71d3-86b0-90bb7a3c4d00` in Codex Token Monitor.

Cause:
- live step builder treated every `response_item role=user` as a visible chat step;
- Codex rollout stores some internal workflow/control prompts with the same low-level `user` role.

Fix:
- added `_is_internal_live_user_prompt(...)` classification for synthetic/internal live prompts;
- excluded internal prompts from both:
  - live detail step builder;
  - fast rollout summary step counter used by session cards.

Verification:
- `python -m unittest tests.test_codex_token_monitor_server`
- direct real-chat smoke on `019e8e29-ed90-71d3-86b0-90bb7a3c4d00`:
  - visible first steps became:
    - `Задача: проверить...`
    - `Продолжай`
    - `Я оборвал тебя, продолжи`
  - synthetic `PLEASE IMPLEMENT THIS PLAN:` and `<turn_aborted>` no longer appeared as ordinary live steps.

Human check:
required - open the same live chat in the monitor and confirm that technical control prompts no longer appear as separate steps in the default view.

Related files:
- [codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- [test_codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

### BUG-20260606-004 - Live Token Monitor showed cumulative totals as if they were per-step tokens

Status: fixed

Area:
`scripts/codex_token_monitor_server.py`, `static/codex-token-monitor/app.js`

Symptoms:
- in live chat mode a late step could show huge `Input / Cached / Output` values that matched the whole accumulated conversation, not the concrete step;
- step cost could stay empty or meaningless because live step usage was taken from cumulative `token_count` totals;
- unavailable live per-step usage looked like zeros in detailed token and cost boxes.

Observed recurrence:
- repeated in monitor checks on `127.0.0.1:8765` after opening long live Codex chats with many previous turns.

Cause:
- rollout `token_count` events store cumulative totals for the thread, not direct per-step deltas;
- monitor attached the latest cumulative totals to the current step without subtracting the previous finalized step totals;
- frontend rendered unavailable live step usage as numeric zero-like fields instead of explicit absence.

Fix:
- live step builder now stores the last cumulative totals for each step and computes a delta against the previous finalized step;
- confirmed per-step delta now gets its own token counts and per-step price from `config/token_pricing.json`;
- if per-step delta cannot be trusted, frontend shows `—` and a warning instead of raw cumulative totals or fake zeros.

Verification:
- `python -m unittest tests.test_codex_token_monitor_server`
- direct live fixture check:
  - step 1 delta = `1200 / 1000 / 200`;
  - step 2 delta = `600 / 400 / 200`;
  - both steps have non-null per-step cost.

Human check:
required - open a long live chat in the monitor and confirm that a late step no longer shows giant accumulated totals from the whole conversation, but only the cost and tokens of that specific step.

Related files:
- [codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- [app.js](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/app.js)
- [test_codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

### BUG-20260606-003 - Token Monitor lost session detail after filter changes and had no project/workdir navigation

Status: fixed

Area:
`static/codex-token-monitor/app.js`, `static/codex-token-monitor/index.html`

Symptoms:
- right pane could stay on `Выберите сессию` or `Нет данных по шагам` even when session cards were visible on the left;
- live/archive source list had no separate project or workdir filter, so the user could not narrow chats to a repo like `sword-of-rome-web`;
- step count badge in session cards could render `null` instead of `—`.

Observed recurrence:
- repeated during live monitor manual checks on `127.0.0.1:8765` after adding hybrid sources and date sorting.

Cause:
- frontend changed `currentSessionId` during filtered list rendering, but did not always reload session detail for the new active card;
- monitor had only `sourceSelect`, but no UI filter built from `session.workdir`;
- card badge used raw `s.step_count` instead of the already-sanitized display value.

Fix:
- added `applySessionFilters()` to reload detail whenever the active card changes after filtering;
- added `workdirFilter` built from normalized `session.workdir` values, with human labels based on folder names;
- source path display and `Path` copy action now respect the selected workdir filter;
- session badge uses display-safe `stepText`.

Verification:
- `python -m unittest tests.test_codex_token_monitor_server`
- browser smoke on `http://127.0.0.1:8765/`:
  - `workdirFilter` appeared;
  - selecting `D:\\Codex+Kilocode\\projects\\sword-of-rome-web` reduced the list to `2/386`;
  - the right pane stayed on the selected session and showed live steps.

Human check:
required - refresh the monitor page, choose `sword-of-rome-web` in the new project/workdir filter, and confirm that the session list narrows and the right pane still shows steps.

Related files:
- [app.js](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/app.js)
- [index.html](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/index.html)
- [test_codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

### BUG-20260606-002 - Token Monitor live chats mixed composed prompt with real history and scanned rollout archive too slowly

Status: fixed

Area:
`codex_token_monitor_server.py`, live chat adapter, monitor UI summary semantics

Symptoms:
- live session list could hang or take minutes on real `C:\Users\andre\.codex` data;
- first visible live step could be internal composed prompt with `AGENTS.md`, not real user message;
- top summary cards in UI could show zeros because they were summed from ambiguous per-step usage instead of `session.summary`.

Observed recurrence:
- `0047` review cycle: repeated on real local `.codex` state during multiple verifier passes.

Cause:
- `discover_live_sessions()` scanned every rollout file for every thread (`N_threads × N_files`);
- `_build_live_steps()` kept composed/system prompt as ordinary `Step 1`;
- frontend header used `totals(s.steps)` even when live step usage was intentionally marked `available = false`.

Fix:
- added cached rollout summary index with one-pass scan of `sessions/**/rollout-*.jsonl`;
- live list now reads `step_count` and token totals from cached rollout summaries;
- composed/system prompt is filtered out of normal live steps, so first visible step is real user message;
- header metrics now use `session.summary` via frontend helper instead of ambiguous per-step sums.

Verification:
- `python -m unittest tests.test_codex_token_monitor_server`
- direct smoke on real `.codex` profile:
  - `discover_live_sessions()` returned `386` sessions in about `16s`;
  - `build_live_session_detail()` returned non-zero totals;
  - first step kind became `user_message`, not `system_composed`.

Human check:
suggested - open the monitor, switch to live chats, and confirm that the first visible step is the real chat message and top totals are non-zero.

Related files:
- [codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)
- [app.js](D:/Codex+Kilocode/projects/sword-of-rome-web/static/codex-token-monitor/app.js)
- [test_codex_token_monitor_server.py](D:/Codex+Kilocode/projects/sword-of-rome-web/tests/test_codex_token_monitor_server.py)

### BUG-20260603-001 - Codex OTel raw file contains sensitive fields despite `log_user_prompt = false`

Status: open

Area:
Codex OTel local telemetry, `tokken_dashboard`, privacy/redaction

Symptoms:
Local OpenTelemetry Collector `file` exporter successfully writes Codex `logs`, `traces`, and `metrics` to [codex-otel.json](C:/Users/andre/.codex/tmp/otel-file-smoke-20260603-214412/codex-otel.json), but raw output includes sensitive identity/session fields.

Observed recurrence:
- `J-20260603-004`: raw OTel file contained `user.email`, `user.account_id`, `conversation.id`, `prompt`, and `prompt_length`.

Cause:
`log_user_prompt = false` reduces prompt logging but does not delete all sensitive telemetry attributes from Codex OTel payloads. Identity/session metadata and prompt-related fields can still appear in exported raw telemetry.

Current mitigation:
- keep OTel endpoint local-only through `localhost`;
- disable telemetry after each smoke-test;
- treat raw OTel files as local-only evidence;
- before any parser/dashboard storage or display, delete at least `user.email`, `user.account_id`, `conversation.id`, `prompt`, and `prompt_length`.

Verification:
- local Collector file exporter produced `logs`, `traces`, `metrics`;
- raw-file search confirmed token fields and sensitive fields;
- temporary `[otel]` block was removed after test;
- backup [config.toml.bak-otel-file-smoke-20260603-214412](C:/Users/andre/.codex/config.toml.bak-otel-file-smoke-20260603-214412) exists.

Human check:
suggested - do not publish raw OTel files; use only local parser/redaction experiments.

Related files:
- [tokken_dashboard_journal.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md)
- [tokken_dashboard_decisions.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md)

### BUG-20260530-007 - Kilo Notebook V3 leaves tester prompt in staging and does not return clickable prompt link

Status: open

Area:
V3 post-import testing flow, `kilo-notebook-v3`, tester prompt handoff

Symptoms:
Import-run succeeds, journal and `V3_navigation.md` are created, but canonical tester prompt copy is missing from `.ai/v3/test_prompts/`. Instead, prompt may remain only in `.ai/v3/staging/`, and the user may receive only a plain text path or summary instead of a clickable markdown link.

Observed recurrence:
- `V3-20260529-234145-battle-status-dashboard-html-with-testing`: machine-check report exists and import succeeded, but canonical tester prompt file was absent from `.ai/v3/test_prompts/`; only staging copy existed at `.ai/v3/staging/V3-20260529-234145-battle-status-dashboard-html-with-testing_POST_IMPORT_TEST_PROMPT.md`.

Cause:
Runtime behavior of live `Kilo Notebook V3` does not fully follow Phase 7 canon. Prompt handling still treats staging as usable final location and does not enforce clickable link output as part of tester prompt handoff.

Current mitigation:
- recover tester prompt manually from staging into `.ai/v3/test_prompts/<V3-ID>_post_import_test_prompt.md`;
- use that recovered file as source for ordinary Kilo code run;
- tighten canon wording so notebook must return a clickable markdown link, not just a plain path.

Required durable fix:
- `Kilo Notebook V3` must always persist tester prompt copy to `.ai/v3/test_prompts/<V3-ID>_post_import_test_prompt.md`;
- staging copy must not count as final success;
- notebook final response must include clickable markdown link to the canonical tester prompt file;
- if canonical file is missing or link is not returned, run should be treated as `blocked`.

Verification:
- `Test-Path '.ai\\v3\\test_prompts\\<V3-ID>_post_import_test_prompt.md'`
- `Get-ChildItem '.ai\\v3\\staging'`
- manual comparison of staging copy vs canonical test_prompts copy
- review of notebook final response for clickable markdown link

Human check:
suggested

Related files:
- [kilo_notebook_v3_mode_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/prompts/kilo_notebook_v3_mode_prompt.md)
- [v3_storage_policy.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/contracts/v3_storage_policy.md)
- [v3_artifact_package_contract.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/contracts/v3_artifact_package_contract.md)
- [test_prompts/README.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/test_prompts/README.md)
- [V3-20260529-234145-battle-status-dashboard-html-with-testing_journal.yaml](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/journals/drafts/V3-20260529-234145-battle-status-dashboard-html-with-testing_journal.yaml)

Notes for future agents:
If import looks successful but tester prompt is hard to find, first check `.ai/v3/test_prompts/`. If file is missing, inspect `.ai/v3/staging/` for a stray `*_POST_IMPORT_TEST_PROMPT.md` copy. Do not treat staging-only prompt as canon-complete success.

### BUG-20260528-006 - Kilo Notebook V3 resolves relative target paths against wrong root

Status: still open

Area:
V3 import workflow, `kilo-notebook-v3`, repeated in multiple pilots

Symptoms:
Notebook report may claim successful import into repo-relative paths, but actual writes happen under wrong filesystem root.

Observed recurrences:
- first Phase 5D docs pilot wrote `.ai/v3/...` into `C:\Users\andre\Documents\.ai\v3\...` instead of active repo `D:\Codex+Kilocode\projects\sword-of-rome-web`;
- later pink calculator pilot again used wrong workspace/root logic on first attempt and required correction before final file ended up in repo.

Cause:
Mode instructions still do not force a hard repo-root detection step before any file write. Notebook can resolve relative paths against VS Code workspace, user documents, or another external root instead of actual git repo root.

Current mitigation:
- imported artifacts can be recovered into real repo root after the fact;
- journal and lifecycle entry can then be recreated or corrected in repo.

Required durable fix:
- mode instructions must explicitly require `git rev-parse --show-toplevel` before any file write;
- all relative target paths are resolved against current workspace root;
- never create or use a parallel `.ai/` tree near archive source or inside user documents;
- if current workspace root is unclear, stop with `blocked`.

Verification:
- `Get-ChildItem 'C:\\Users\\andre\\Documents\\.ai\\v3' -Recurse`
- `Get-ChildItem '.ai\\v3' -Recurse`
- `Test-Path` for expected repo files before and after recovery
- manual comparison of shadow-root files vs recovered repo files
- repeated repro during `V3-20260529-000139-pink-calculator-html-pilot`

Human check:
suggested

Related files:
- [V3_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/V3_navigation.md)
- [V3-20260528-195750-phase5A-5C-deep-doc-pack_journal.yaml](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/journals/drafts/V3-20260528-195750-phase5A-5C-deep-doc-pack_journal.yaml)
- [manual_kilo_notebook_v3_setup.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/docs/manual_kilo_notebook_v3_setup.md)
- [V3-20260529-000139-pink-calculator-html-pilot_journal.yaml](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/journals/drafts/V3-20260529-000139-pink-calculator-html-pilot_journal.yaml)

Notes for future agents:
If notebook says import succeeded but repo files are missing, immediately search for stray `.ai/v3/` trees outside workspace root. First suspect: path resolution against user documents or archive-adjacent folder.

### BUG-20260607-002 - Codex Token Monitor Server: старый процесс блокирует порт при повторном запуске

Status: fixed

Area:
`start_codex_token_monitor.bat`

Symptoms:
- После нажатия «Остановить монитор» процесс Python мог остаться висеть
- Повторный запуск `start_codex_token_monitor.bat` не убивал старый процесс
- Браузер подключался к старому серверу без новых изменений
- Новый endpoint `/api/audit_session` возвращал 404

Cause:
`start_codex_token_monitor.bat` запускал `python scripts/codex_token_monitor_server.py` без предварительной проверки занятости порта. Если старый процесс уже слушал `127.0.0.1:8765`, новый процесс падал с `Address already in use`, а старый продолжал отвечать.

Fix:
Добавлен блок в bat-файл:
```
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8765.*LISTENING"') do (
    taskkill /PID %%a /F
)
```

Verification:
- `netstat -ano | findstr ":8765"` показал два процесса LISTENING (PID 19500, 18560) до фикса
- После `taskkill` оба процесса убиты
- `start_codex_token_monitor.bat` запустился успешно
- `/api/audit_session` начал отвечать 200

Human check:
suggested — при обновлении монитора обращать внимание, не открывается ли старая версия. Если кнопка «Аудит» не появляется — проверить, не висит ли старый процесс на порту.

Related files:
- [start_codex_token_monitor.bat](/D:/Codex+Kilocode/projects/sword-of-rome-web/start_codex_token_monitor.bat)
- [codex_token_monitor_server.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/codex_token_monitor_server.py)

Notes for future agents:
- Если новый endpoint возвращает 404, первым делом проверить `netstat -ano | findstr ":8765"` — если есть LISTENING PID, убить.
- Баталка авто-убивает PID при запуске, но если сервер стартует не через bat — нужно убивать вручную.

### BUG-20260528-005 - V2 cycle: содержательный patch остаётся в review-ветке и не возвращается в рабочую ветку

Status: fixed

Area:
V2 external review workflow, branch choreography, Handoff 0034

Symptoms:
После V2 snapshot/review содержательные Phase 4 изменения оказались в `review/v2/20260527-210800-v3-phase4-runtime`, но не были возвращены в рабочую ветку `codex/editor-play-visual-continuity-plan`. На рабочей ветке `git status` был чистым, хотя Kilo report утверждал, что Phase 4 выполнен.

Cause:
В протоколе V2 не был жёстко зафиксирован обязательный post-review шаг возврата content patch из `review/v2/...` обратно в исходную рабочую ветку. В результате review-ветка использовалась не только как временный snapshot/runtime слой, но и как место, где фактически осталась реализация.

Fix:
В [`.ai/external_reviews/README.md`](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/README.md) добавлен обязательный `restore-to-working-branch` step. Теперь после V2 implementation Kilo обязан:
- явно вернуться в исходную рабочую ветку;
- перенести обратно только content patch;
- проверить `git status --short` и `git diff --name-only` уже на рабочей ветке;
- убедиться, что непредусмотренные `.ai/external_reviews/` изменения не попали в рабочую ветку.

Verification:
- `git reflog --date=iso -n 30`
- `git log --oneline --decorate review/v2/20260527-210800-v3-phase4-runtime -n 8`
- `git diff --name-only 51458eb..review/v2/20260527-210800-v3-phase4-runtime`
- ручная проверка, что Phase 4 patch присутствовал только в review-ветке

Human check:
not needed

Related files:
- [`.ai/external_reviews/README.md`](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/README.md)
- [0034_v3_phase4_runtime_mode_integration_report.md](D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0034_v3_phase4_runtime_mode_integration_report.md)

Notes for future agents:
`review/v2/...` — временная review-площадка, а не финальное место реализации. Если содержательный patch есть только там, задача не завершена. Перед финальным report нужно проверить, что expected diff существует именно в исходной рабочей ветке.

### BUG-20260527-004 — V2 snapshot: потеря untracked-файлов при git stash без --include-untracked

Status: fixed

Area:
V2 external review workflow, git, Handoff 0031

Symptoms:
При подготовке V2 review-ветки `git stash` (без `--include-untracked`) потерял untracked-файлы `.ai/v3/`. После `git checkout -b review/v2/...` от base commit и `git stash pop` новые untracked-файлы не восстановились. `git status --short` показал только modified tracked-файлы; папка `.ai/v3/` исчезла.

Cause:
`git stash` по умолчанию сохраняет только tracked modified-файлы. Untracked-файлы (только что созданные, никогда не коммиченные) не попадают в stash. При переключении ветки они теряются безвозвратно.

Fix:
Файлы `.ai/v3/` восстановлены повторным созданием через `edit_file`. V2 snapshot успешно запушен. Рекомендована правка протокола: в [`.ai/external_reviews/README.md`](.ai/external_reviews/README.md:29), секция `/v2` (шаг 2), добавить явное требование `git stash push --include-untracked` и проверку восстановления untracked-файлов после `git stash pop`.

Verification:
- `git status --short` подтверждает наличие всех 6 файлов `.ai/v3/`
- V2 snapshot `dd0d195` запушен, review пройден, внешний reviewer подтвердил корректность

Human check:
not needed

Related files:
- [`.ai/external_reviews/README.md`](.ai/external_reviews/README.md:29) — требует правки инструкции
- [`.ai/reports/0031_v3_phase1_docs_foundation_report.md`](.ai/reports/0031_v3_phase1_docs_foundation_report.md)

Notes for future agents:
При V2 snapshot всегда использовать `git stash push --include-untracked`. Без этого флага `git stash` сохраняет только tracked-файлы, и новые untracked-файлы будут безвозвратно потеряны при переключении ветки. После `git stash pop` проверять восстановление через `git status --short`.

### BUG-20260527-003 - Kilo workflow report overclaims file changes and verification

Status: open

Area:
workflow docs/rules, Kilo reporting integrity, Handoff 0030

Symptoms:
Kilo report for Phase 0 claims broader success than repo actually contains:
- report says multiple canon files changed, but `git diff` shows only partial subset;
- report says `python scripts/validate_kilo_contract.py repo` passed, but local rerun fails;
- report marks task accepted/completed even though key acceptance items remain unmet.

Cause:
Unknown executor/reporting gap. Most likely report assembled from intended change list rather than final filesystem state and real command results.

Current state:
Not accepted by Codex. Push blocked. Needs correction run with strict requirement to report only actual modified files and real validator output.

Fix direction:
1. Review actual dirty files before writing report.
2. Re-run required verification commands and copy truthful status.
3. Do not mark Phase 0 accepted until canon files, validator, and required checks all align.

Verification:
- `git diff --stat`
- `git diff`
- `python scripts/validate_kilo_contract.py repo`
- manual comparison of report vs actual changed files

Human check:
not needed

Related files:
- [0030_v3_phase0_contract_alignment_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0030_v3_phase0_contract_alignment_report.md)
- [0030_v3_phase0_contract_alignment.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/handoffs/0030_v3_phase0_contract_alignment.md)
- [validate_kilo_contract.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/validate_kilo_contract.py)

### BUG-20260527-001 — Play/test spaces/connections render без underlay transform (coordinate misalignment)

Status: fixed

Area:
table-sandbox, Phaser scene, Editor → Play continuity, Handoff 0029, Map Plane Alignment 0.1

Symptoms:
После Handoff 0029 (MapRenderModel Contract Wire-Up) в play/test mode mapVisual debug bounds и underlay bounds видны, но spaces, connections и pieces визуально не совпадают с ними по расположению относительно редактора. Точки и связи выглядят так, как будто рисуются в другой системе координат.

Cause:
`phaserScene.ts` рисовал spaces/connections/pieces по координатам `space.x`, `space.y` напрямую — в raw map-local координатах. Редактор (`EditorSurface.tsx`) применяет `mapLocalToWorld(space.x, space.y, underlay)` — center-based offset+scale+rotation transform — ко всем объектам. Без этого transform в play/test объекты оказывались в другом месте относительно map/underlay bounds.

Fix:
1. Добавлен `mapLocalToWorld()` helper в [`MapRenderModel.ts`](table-sandbox/src/map/MapRenderModel.ts:53) — работает только с `MapRenderUnderlay`, не тянет `MapDraft` в renderer.
2. В [`phaserScene.ts`](table-sandbox/src/renderer/phaserScene.ts) добавлено поле `currentUnderlay`, сохраняемое из `mapVisual.underlay` в `updateFromState`.
3. Transform применён единообразно в `drawSpaces`, `drawConnections`, `drawPieces`, `drawMapVisualDebug`.
4. Hit-test (`cachedSpaces`, `cachedPieceBoxes`) теперь в world-координатах — корректно, т.к. pointer input тоже в world.
5. [P1 correction] Map bounds AABB исправлен с 2-углового (`strokeRect(tl.x, tl.y, br.x - tl.x, br.y - tl.y)`) на 4-угловой (min/max по всем transformed corners), идентично underlay bounds. Для rotated карт 2-угловой подход давал неверные размеры.

Дополнительно в рамках этого же цикла:
- V2 external review (GPT-5.5 Thinking) нашёл неявный debug depth (0/1) — исправлен на `DEBUG_DEPTH = -20`.
- Ложное V2 срабатывание: `useState(null)` без generic — не подтвердилось, generic уже был в коде.
- Path truncation в `write_to_file` при создании V2 артефактов — обойдено через `edit_file`.
- Потеря working tree после V2 push/review-branch — восстановлено cherry-pick.

Verification:
- `npm run typecheck` — passes
- `npm run build` — passes
- Browser check: не проводился, делегирован человеку

Human check:
suggested — `table-sandbox/Запуск.bat` → Editor → Preview → точки/связи должны совпадать с map/underlay bounds. Сброс/загрузка чистят debug-слой.

Related files:
- [`table-sandbox/src/map/MapRenderModel.ts`](table-sandbox/src/map/MapRenderModel.ts)
- [`table-sandbox/src/renderer/phaserScene.ts`](table-sandbox/src/renderer/phaserScene.ts)
- [`table-sandbox/src/editor/MapDraft.ts`](table-sandbox/src/editor/MapDraft.ts) (read-only reference)
- [`.ai/reports/0029_map_plane_alignment_play_preview_0_1_report.md`](.ai/reports/0029_map_plane_alignment_play_preview_0_1_report.md)

### BUG-20260526-002 — Editor map-plane / large image geometry drift

Status: open

Area:
editor branch, `0020`, underlay, map-plane geometry

Symptoms:
При загрузке большой custom map image карта может вести себя не как реальная рабочая плоскость редактора: раньше были drift image vs points, странное движение при scale/move, ощущение что весь editor world всё ещё равен tiny fixture sheet.

Cause:
Проблема оказалась не в одной подложке, а в editor geometry model:
- fixed tiny plane долго оставался implicit source of truth;
- underlay, grid, pointer conversion и map-local coordinates расходились по смыслу;
- large image edge cases начали проявляться сильнее tiny-fixture сценария.

Current state:
В `0020` и correction-pass большая часть модели уже переделана:
- active draft size снова идёт из реального `coordinateSystem`, а не из forced `6000x4000`;
- build/typecheck проходят;
- но текущий checkpoint всё ещё допускает, что на живой большой карте могут остаться browser-level edge cases.

Fix direction:
Следующий узкий шаг должен проверять и добивать только large custom image / map-plane ergonomics поверх текущего checkpoint, без wholesale editor redesign.

Verification:
- `npm run typecheck`
- `npm run build`
- Codex code review of [`MapDraft.ts`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/MapDraft.ts) and [`EditorSurface.tsx`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/EditorSurface.tsx)

Human check:
suggested — на живой большой custom карте проверить move / scale / rotate / space placement / preview.

Related files:
- [`table-sandbox/src/editor/MapDraft.ts`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/MapDraft.ts)
- [`table-sandbox/src/editor/EditorSurface.tsx`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/EditorSurface.tsx)
- [`table-sandbox/src/editor/Editor.css`](D:/Codex+Kilocode/projects/sword-of-rome-web/table-sandbox/src/editor/Editor.css)

### BUG-20260524-001 — Phaser canvas исчезает при StrictMode double-mount

Status: fixed

Area:
table-sandbox, Phaser, React StrictMode

Symptoms:
Зелёный Phaser-холст не отображается. В консоли видно `Phaser v3.90.0 (WebGL | Web Audio)`, но `canvasCount: 0`. Пользователь видит страницу без поля для кликов.

Cause:
React 18 StrictMode (в [`main.tsx`](table-sandbox/src/main.tsx)) делает double-mount. [`PhaserStage.tsx`](table-sandbox/src/renderer/PhaserStage.tsx) в `useEffect` создавал `new Phaser.Game(config)`. StrictMode: mount → эффект → cleanup (`game.destroy(true)`) → mount → эффект. `game.destroy(true)` удаляет canvas **асинхронно**. Второй mount проверял `container.querySelector("canvas")` — видел ещё не удалённый canvas от первой игры → скипал создание. Потом destroy заканчивал удаление → холст исчезал.

Fix:
Заменить хрупкий DOM-based guard на синхронную очистку: перед созданием игры всегда удалять предыдущий `gameRef.current`, затем синхронно удалять любой оставшийся canvas через `leftoverCanvas.remove()`. Файл: [`PhaserStage.tsx`](table-sandbox/src/renderer/PhaserStage.tsx:23-31).

Verification:
- Playwright: `canvasCount: 1`, `canvasWidth: 800`, `canvasHeight: 500`
- `npx tsc --noEmit` — 0 ошибок
- `npx vite build` — 40 modules, built 8.26s

Human check:
suggested — открыть страницу, убедиться что зелёное поле с сеткой видно, кликнуть и проверить координаты в DebugPanel.

Related files:
- [`table-sandbox/src/renderer/PhaserStage.tsx`](table-sandbox/src/renderer/PhaserStage.tsx)
- [`table-sandbox/src/main.tsx`](table-sandbox/src/main.tsx) (StrictMode — не менялся, но влияет)

Notes for future agents:
При работе с Phaser + React 18 StrictMode нельзя полагаться на DOM-проверки (`querySelector`) для защиты от double-mount. `game.destroy(true)` асинхронный — canvas может оставаться в DOM после вызова. Нужно синхронно удалять canvas до создания нового экземпляра. Либо рассмотреть отказ от StrictMode для Phaser-компонентов.
