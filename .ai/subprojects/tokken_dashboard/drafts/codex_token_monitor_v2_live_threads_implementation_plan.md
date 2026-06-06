# Codex Token Monitor v2: Real Codex Chats + Archive Test Runs

## Summary

Перевести монитор с режима `только _local/codex-token-debugger` на гибридную модель:

- основной источник: локальный архив реальных чатов Codex из `C:/Users/andre/.codex`;
- второй источник: существующий архив OTel/test-run из `_local/codex-token-debugger`;
- UI должен явно показывать активный источник и не маскировать архивный run-folder под обычный чат.

Решения уже приняты:

- режим: `hybrid`;
- prompt/answer: скрыты по умолчанию, с превью и раскрытием по клику;
- monitor server остается локальной read-only утилитой, без новых OTel-запусков и без записи в Codex state.

## Key Changes

### 1. Source-aware monitor

- Заменить misleading `projectSelect` на явный `sourceSelect`.
- Поддержать два источника:
  - `Реальные чаты Codex`
  - `Архив тестов OTel`
- При одном доступном проекте/профиле не показывать пустой dropdown как будто есть выбор.

### 2. Live Codex chat adapter

Использовать read-only локальные источники:

- `C:/Users/andre/.codex/state_5.sqlite`
- `C:/Users/andre/.codex/session_index.jsonl`
- `C:/Users/andre/.codex/sessions/**/rollout-*.jsonl`

Source of truth:

- chat list: `threads` table в `state_5.sqlite`;
- title: `threads.title`, затем `session_index.thread_name`, затем `thread.id`;
- model/reasoning: `threads.model`, `threads.reasoning_effort`, затем fallback из rollout;
- cwd/workdir: `threads.cwd`, затем `session_meta.payload.cwd`.

### 3. Step building for real chats

Строить шаги не по OTel normalizer, а по rollout-jsonl:

- user text из `response_item.role == "user"` или `event_msg.type == "user_message"`;
- assistant text из `response_item.role == "assistant"` и text/output_text content;
- turn id из `task_started`, `turn_context`, связанных message events;
- per-step usage best-effort по ближайшему следующему `token_count`.

Правило честности:

- если per-step usage mapping неоднозначен, ставить `usage.available = false`;
- не смешивать cumulative totals и fake per-step deltas.

Session totals для live chats:

- брать из последнего `token_count.info.total_token_usage`;
- cost считать через `config/token_pricing.json`.

### 4. Archive source semantics

Оставить current run-folder source, но исправить misleading display:

- title не должен слепо равняться имени папки, если доступен human label;
- при наличии `*_confirmation_summary.json` default detail = `selected/confirmed turn`;
- mixed/noisy confirmation-runs должны получать явные badges;
- архивный run не должен выглядеть как живой чат.

### 5. Prompt/answer visibility

Для обоих источников:

- schema fields всегда возвращаются;
- тексты скрыты по умолчанию;
- если текста нет, UI честно показывает `not available`.

### 6. Backend/API/config

Сохранить один server:

- `scripts/codex_token_monitor_server.py`

Добавить source-aware API:

- `GET /api/sources`
- `GET /api/sessions?source_id=...`
- `GET /api/session?source_id=...&session_id=...`

Расширить config:

- `config/codex_token_monitor_projects.json`

Минимальные sources:

- `codex_live_threads`
- `token_debugger_archive`

### 7. UI meaning

- Переименовать `Проект / рабочая папка` в `Источник / рабочая папка`.
- Live source должен показывать реальные названия чатов, модель, reasoning, cwd и updated time.
- Archive source должен показывать human label run, run id и source badges.

## Public Interfaces

### API

`GET /api/sources`
- `{ default_source_id, sources[] }`

`GET /api/sessions?source_id=...`
- список session cards для выбранного источника

`GET /api/session?source_id=...&session_id=...`
- detail для выбранной session

Каждый session detail обязан содержать:

- `source_kind`
- `id`
- `title`
- `date`
- `model`
- `reasoning`
- `workdir`
- `summary`
- `steps[]`

### Cost policy

- pricing source остается `config/token_pricing.json`;
- live chat adapter использует ту же pricing table, что и `codex_token_cost_normalizer.py`;
- если per-step usage unavailable, step cost не вычислять;
- session total cost для real chats считать по последнему `total_token_usage`.

## Test Plan

### Unit tests

Добавить/расширить tests так, чтобы покрыть:

- live chat source:
  - thread list из `state_5.sqlite`;
  - title из `threads.title`;
  - model/reasoning из live metadata;
  - prompt/answer extraction из rollout-jsonl;
  - honest handling of ambiguous token mapping;
- archive source:
  - confirmation-run prefers `selected_turn`;
  - mixed/noisy badges and warnings;
- UI semantics:
  - single-source/single-project mode не притворяется богатым выбором;
  - live source показывает human chat titles;
  - archive source не маскируется под live chat.

### Manual smoke checks

1. В режиме `Реальные чаты Codex` видны реальные русские названия чатов.
2. Текущий чат виден под человеческим названием, а не как run-folder.
3. В реальном чате показываются model и reasoning.
4. Prompt/answer для реальных чатов раскрываются.
5. В режиме `Архив тестов OTel` старые confirmation-runs остаются доступны.
6. `playwright-only-confirmation` не выглядит как один чистый чат, если artifact mixed/noisy.

## Constraints

- Не запускать новый OTel.
- Не менять live Codex config.
- Не писать в `C:/Users/andre/.codex/**`.
- Не трогать product code варгейма.
- `_local/**` не коммитить.
