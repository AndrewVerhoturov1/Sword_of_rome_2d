# Протокол V2 External Senior Review

## Статус

`draft` — первая реализация документации, не пилотирована

## Что такое V2

V2 — это строгий ручной протокол для внешнего senior review реального WIP-кода. В отличие от [`/v1`](../external_chats/external_chat_rules.md) (prompt-only вопрос), V2 даёт внешнему чату зафиксированный snapshot реального кода и контекст сравнения с base, чтобы получить bounded technical advice.

V2 не заменяет [`/v1`](../prompts/create_external_question_prompt.md) и [`/r1`](../prompts/create_external_chat_request.md). Это отдельный route для случая, когда нужно показать внешнему senior reviewer реальный код, а не только описание или план.

## Главное правило

**Внешний чат не получает repo authority.** V2 ответ — это planning/debug input, а не accepted fact. Любые выводы внешнего чата требуют локальной проверки Kilo/Codex перед использованием.

## Граница с другими маршрутами

| Маршрут | Назначение | Код виден? | Артефакты |
|---------|-----------|-----------|-----------|
| `/v1` | Prompt-only вопрос | Нет | Только notebook entry |
| `/r1` | Full external launch package | По published links | Published artifacts + recorder |
| `/v2` | Review WIP snapshot | Да, snapshot commit | Review branch + V2 artifacts |

## Команды V2 (manual Kilo protocol)

V2 — это ручной протокол. Ниже описаны команды как инструкции для Kilo, а не как реализованные CLI-команды. Первая версия не содержит automation scripts.

### `/v2` — подготовить external senior review snapshot

Kilo готовит WIP snapshot для внешнего review:

1. Определяет base commit и WIP snapshot commit.
2. Составляет inventory изменённых файлов.
3. Заполняет [`v2_request_template.md`](templates/v2_request_template.md).
4. Готовит safety-отчёт по [`v2_safety_checklist.md`](templates/v2_safety_checklist.md).
5. Показывает preview и ждёт human approval.
6. **Не делает commit и push без явного разрешения человека.**

### `/v2 preview` — показать, что попадёт в snapshot

Kilo показывает, но не публикует:

- review branch name;
- base branch и base commit;
- snapshot commit (если уже закоммичен локально);
- changed tracked files;
- untracked files;
- suspicious ignored files;
- blocked files;
- large/binary files;
- local-only path hits;
- exact files proposed for push;
- exact files excluded from push.

**Правило:** `/v2 preview` обязателен перед любым V2 push. Push запрещён, если preview не был показан человеку и явно им не принят.

### `/v2 ingest` — обработать внешний ответ

V2 ingest — полностью ручной. Два допустимых пути:

1. **Прямая вставка текста в ordinary Kilo run:**
   - Человек копирует raw external answer и вставляет его прямо в запуск Kilo (Handoff Runner или Debugger).
   - Kilo читает ответ и формулирует understanding summary по [`v2_ingest_summary_template.md`](templates/v2_ingest_summary_template.md).

2. **Через локально сохранённый V2 response file:**
   - Человек сохраняет raw external answer в локальный файл (например, `.ai/external_reviews/responses/V2-YYYYMMDD-HHMMSS_response.md` по [`v2_response_template.md`](templates/v2_response_template.md)).
   - Затем запускает ordinary Kilo run (Handoff Runner или Debugger), который читает этот файл и формулирует understanding summary.

Для V2 ingest используется только `kilo-handoff-runner` или `kilo-debugger`. `kilo-recorder` в первой версии V2 не используется. `kilo-notebook` остаётся `/v1-only` и не расширяется на V2.

### `/v2 status` — показать состояние текущего V2 request

Kilo показывает:

- текущий V2 ID (если есть активный request);
- статус по lifecycle;
- что уже сделано;
- что осталось.

### `/v2 cleanup` — провести cleanup после завершения review

Kilo проверяет и фиксирует:

- remote review branch удалена или явно оставлена;
- local review branch удалена или явно оставлена;
- [`V2_navigation.md`](V2_navigation.md) обновлён;
- финальный статус установлен в `cleaned`, `superseded` или `implemented`;
- raw V2 runtime artifacts не утекли в `main`;
- draft PR закрыт, помечен или подтверждён как отсутствующий.

## Жизненный цикл статусов V2

| Статус | Описание |
|--------|----------|
| `draft` | V2 request создан, но ещё не previewed |
| `previewed` | `/v2 preview` показан человеку |
| `awaiting_human_push_approval` | Preview принят, ждём разрешения на push |
| `snapshot_pushed` | Review branch запушина в public GitHub |
| `waiting_external_answer` | Snapshot отправлен внешнему чату, ждём ответ |
| `raw_response_captured` | Raw external answer записан (recording step) |
| `ingested` | Kilo understanding summary готов (interpretation step) |
| `implementation_planned` | Предложен план реализации по мотивам ответа |
| `implemented` | Изменения приняты и реализованы |
| `superseded` | Request перекрыт более новым V2 request |
| `cleaned` | Cleanup выполнен, ветки удалены |

## Классы артефактов и правила хранения

### Публичные и стабильные (tracked в `main`)

- `.ai/external_reviews/README.md` — этот файл
- `.ai/external_reviews/V2_navigation.md` — индекс V2 requests
- `.ai/external_reviews/templates/*` — шаблоны
- Sanitized accepted summaries — только после explicit human/Codex acceptance

### Runtime artifacts (в `review/v2/...` branch, не в `main`)

- V2 request report
- Generated V2 prompt
- Changed-file inventory
- Safety report
- Временные screenshots (только явно разрешённые для этого review)

### Raw response и ingest artifacts (не в `main` по умолчанию)

- Raw external answer
- Kilo understanding summary
- Draft implementation plan

**Правило по умолчанию:** Raw V2 runtime artifacts не трекаются в `main`. Они живут в `review/v2/...` branch или local-only до explicit решения о публикации sanitized summary.

### Sanitized accepted summary

Может быть поднят в `main` после explicit human/Codex acceptance и должен быть очищен от:

- raw external answer verbatim;
- приватных локальных путей;
- screenshots и binary artifacts (без отдельного одобрения);
- secrets и personal data;
- временных гипотез отладки, которые не были приняты;
- полного debug log.

## Review branch

- **Repo:** `AndrewVerhoturov1/Sword_of_rome_2d` (текущий GitHub repo)
- **Формат имени ветки:** `review/v2/YYYYMMDD-HHMMSS-short-topic`
- **Push gate:** Всегда требовать human confirmation перед V2 push

### Предупреждение о публичности

Push в public GitHub `review/v2/...` branch — это публикация. Даже после удаления ветки commit links могут остаться во внешних чатах, кэше, форках, локальных копиях, скриншотах и заметках. Если файл нельзя считать опубликованным, его нельзя пушить.

## Пакет подтверждения для human push gate

Перед V2 push Kilo обязан показать человеку **конкретный пакет**, а не расплывчатый вопрос «push?»:

- review branch name;
- base branch;
- base commit;
- changed tracked files;
- untracked files;
- suspicious ignored files;
- blocked files;
- large/binary files;
- local-only path hits;
- exact files that will be pushed;
- exact files excluded from push;
- простой yes/no вопрос на русском языке.

## Требования к внешнему чату в V2

V2 prompt должен требовать от внешнего чата:

1. Прочитать V2 request report первым.
2. Открыть WIP files на snapshot commit.
3. Сравнить их с base files на base commit.
4. Явно сохранять distinction между base и snapshot.
5. Предпочитать commit-pinned links; branch links допустимы только как дополнительный контекст.
6. Перечислить, что было прочитано, в `Context Readback`.
7. Отделять verified facts от hypotheses.
8. Не утверждать, что видел local runtime, tests, shell или git status.
9. Не писать patch так, как будто есть локальный repo access.
10. Давать bounded senior technical advice.
11. Явно говорить, чего не хватило и где граница уверенности.

### Обязательная форма ответа внешнего чата для V2

Внешний чат должен вернуть:

- `V2 ID`
- `Context Readback`
- `Provider/Model`
- `Answer`
- `Confirmed from central docs`
- `Confirmed from project docs`
- `Confirmed from WIP snapshot`
- `Confirmed from base comparison`
- `Not available / not verified`
- `Main assessment`
- `Root cause hypothesis`
- `Recommended correction path`
- `Risks`
- `Suggested implementation notes`
- `Questions back to Kilo/user, if any`
- `Candidate Navigation Entry`

## Требования безопасности

Перед любым V2 push Kilo обязан проверить:

- tracked changed files;
- untracked files;
- suspicious ignored files (если релевантны);
- secrets и private/local-only files (блокировать);
- large/binary files;
- local-only path hits.

### Примеры blocked или high-risk файлов

- `.env`, `.env.*`
- key/certificate/credential files
- файлы под `_local/`
- generated output и build artifacts
- private images/assets
- archives
- logs
- large binary files без отдельного разрешения

## Чего V2 НЕ делает

В первой версии V2:

- **Не добавляет новый Kilo mode.** V2 работает через существующие допустимые modes: `kilo-handoff-runner` для docs/protocol и `kilo-debugger` для stuck/debug cases.
- **Не использует `kilo-recorder`.** V2 ingest полностью ручной: raw external answer передаётся в ordinary Kilo run вручную (прямая вставка текста или локальный response-файл).
- **Не расширяет `kilo-notebook`.** `kilo-notebook` остаётся `/v1-only`.
- **Не добавляет helper scripts.** Все команды выполняются как manual Kilo instructions.
- **Не автоматизирует commit/push.** Push только после human confirmation.
- **Не трекает raw V2 runtime artifacts в `main` по умолчанию.**
- **Не заменяет `/v1` или `/r1`.**

## Связанные документы

- [V2_navigation.md](V2_navigation.md) — индекс V2 requests
- [v2_request_template.md](templates/v2_request_template.md) — шаблон V2 request
- [v2_prompt_template.md](templates/v2_prompt_template.md) — шаблон V2 prompt для внешнего чата
- [v2_response_template.md](templates/v2_response_template.md) — шаблон записи V2 response
- [v2_ingest_summary_template.md](templates/v2_ingest_summary_template.md) — шаблон Kilo understanding summary
- [v2_safety_checklist.md](templates/v2_safety_checklist.md) — safety checklist перед V2 push

## Ссылки на внешние контракты

- [`AGENTS.md`](../AGENTS.md) — workflow contract
- [`.ai/rules/agent_protocol.md`](../rules/agent_protocol.md) — агентный протокол
- [`.ai/rules/kilo_mode_contract.md`](../rules/kilo_mode_contract.md) — контракт Kilo modes
- [`.ai/external_chats/external_chat_rules.md`](../external_chats/external_chat_rules.md) — правила для внешнего чата
- [`.ai/policies/human_review_policy.md`](../policies/human_review_policy.md) — политика human review
- [`.ai/policies/bug_tracking_policy.md`](../policies/bug_tracking_policy.md) — политика bug tracking
- [`.ai/plans/master/v2_external_senior_review_system.md`](../plans/master/v2_external_senior_review_system.md) — master plan V2

## История

- 2026-05-26 — первая версия документации. Основана на master plan после внешней критики (V1-20260526-103939).
