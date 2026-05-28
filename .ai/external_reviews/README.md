# Протокол V2 External Senior Review

## Статус

`hardened` — доработан после первого реального V2 pilot (0026)

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

**Важно:** если WIP содержит new untracked files (только что созданные, ещё не закоммиченные), нельзя использовать обычный `git stash` без флага. Для V2 snapshot нужно использовать `git stash push --include-untracked`, иначе новые файлы будут потеряны при переключении на review-ветку.

1. Определяет base commit и WIP snapshot commit.
2. Составляет inventory изменённых файлов.
2a. **Корректно сохраняет untracked-файлы перед переключением на review-ветку:**
   - `git stash push --include-untracked -m "v2-snapshot-wip"` — флаг `--include-untracked` обязателен.
   - После создания review-ветки от base commit: `git stash pop`.
   - После восстановления обязательно проверяет `git status --short`: new files должны вернуться как `??`.
2b. **Central rules URL для V2 prompt:**
   - Правильный URL: `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
   - НЕ использовать `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/ai/external_chats/external_chat_rules.md` — этот URL возвращает 404.
3. Заполняет [`v2_request_template.md`](templates/v2_request_template.md).
4. Готовит safety-отчёт по [`v2_safety_checklist.md`](templates/v2_safety_checklist.md).
5. Показывает preview и ждёт human approval.
6. **Не делает commit и push без явного разрешения человека.**

#### Обязательная цепочка после push

После успешного V2 push Kilo обязан немедленно, до завершения run:

1. **Проверить commit-pinned ссылки** — убедиться, что snapshot commit, raw URL и compare link реально доступны.
2. **Финализировать request и safety artifacts** — после push проставить в request и safety реальный `Snapshot Commit`, заполнить compare/raw links, убрать `TBD` / `not yet committed`, обновить request как минимум до `snapshot_pushed`.
3. **Создать instantiated V2 prompt** — заполнить [`v2_prompt_template.md`](templates/v2_prompt_template.md) с реальными commit-pinned ссылками и сохранить в `.ai/external_reviews/prompts/V2-YYYYMMDD-HHMMSS_prompt.md`.
4. **Показать готовый copy-paste prompt человеку** — prompt должен быть готов к немедленной вставке во внешний чат.
5. **Перевести статус** — сначала в `prompt_ready` (prompt создан), затем, после показа prompt человеку, в `waiting_external_answer`.
6. **Не завершать run финальным report до этого шага.** Если prompt не может быть создан — остановиться с blocked-отчётом, объяснив причину.

Цепочка: `push → verify links → finalize request/safety → create prompt → prompt_ready → show human → waiting_external_answer`. Разрыв `push → prompt` или оставленные `TBD` в request/safety являются нарушением протокола.

#### Обязательный `restore-to-working-branch` step после V2 implementation

Если после V2 review Kilo сделал содержательные implementation-изменения не в исходной рабочей ветке, а внутри `review/v2/...`, он обязан до завершения run вернуть результат обратно в исходную рабочую ветку.

Обязательная последовательность:

1. **Явно вернуться в исходную рабочую ветку** — ту, из которой был вызван `/v2`.
2. **Перенести только content patch** — через `cherry-pick`, path-scoped restore или другой проверяемый git-механизм. Нельзя тащить обратно runtime artifacts из `.ai/external_reviews/`, если они не входят в scope основной задачи.
3. **Проверить branch state** — перед завершением run показать текущую ветку и убедиться, что она совпадает с исходной рабочей веткой, а не с `review/v2/...`.
4. **Проверить фактический diff на рабочей ветке** — `git status --short` и `git diff --name-only` должны подтверждать, что ожидаемые содержательные файлы уже существуют именно в рабочей ветке.
5. **Проверить отсутствие побочных V2-хвостов** — в рабочей ветке не должно появиться непредусмотренных изменений в `.ai/external_reviews/`.

**Правило приёмки:** если содержательный patch остался только в `review/v2/...`, а в исходной рабочей ветке его нет, V2 cycle считается незавершённым. Такой run нельзя объявлять completed, even if review artifacts, prompt и ingest уже готовы.

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

## `/v2` как interrupt-команда

`/v2` может быть вызван пользователем во время уже идущего Kilo run (например, посреди debug-задачи). Это **interrupt**, а не новый Kilo mode и не новый запуск.

### Контракт interrupt

Когда пользователь явно вводит `/v2` во время активного Kilo run:

1. Kilo **обязан поставить обычную задачу на паузу** — текущая debug/build попытка приостанавливается.
2. Kilo **кратко фиксирует текущее WIP state** — что уже сделано, что проверено, на каком шаге остановились.
3. Kilo **переходит в `/v2 preview`** — готовит inventory, safety checklist, ждёт human push approval.
4. После завершения V2-цикла (push → prompt → external answer → ingest → implementation) Kilo **возвращается к исходной задаче** через обязательный `restore-to-working-branch` step или завершает её по новому решению только после такого возврата.

### Отличие от `blocked-v2-recommended`

Это два разных trigger path:

| Путь | Триггер | Кто инициирует | Нужен ли blocked report |
|------|---------|---------------|------------------------|
| `blocked-v2-recommended` | Kilo достиг blocker на реальном WIP-коде | Kilo (автоматически) | Да, обязателен |
| Explicit user `/v2` | Пользователь ввёл `/v2` во время run | Человек (явно) | Нет, достаточно WIP summary |

При explicit user `/v2` Kilo **не обязан** сначала доказать три неудачные попытки или написать полный blocked report. Достаточно кратко зафиксировать WIP state и перейти к `/v2 preview`.

### `/v2 cleanup` — провести cleanup после завершения review

Cleanup ownership: **Codex-owned post-accept cleanup**, не Kilo-owned.

#### Модель владения

| Роль | Зона ответственности |
|------|---------------------|
| **Kilo** | Подготавливает cleanup preview: инспектирует состояние локальной и remote веток, перечисляет runtime artifacts, предлагает cleanup-действия, обновляет `V2_navigation.md` статусом до cleanup |
| **Человек** | Принимает необратимые решения: удалить/сохранить remote review branch, удалить/сохранить local review branch, сохранить/удалить raw response, поднимать ли sanitized summary в `main` |
| **Codex** | Выполняет post-accept cleanup review: проверяет, что `V2_navigation.md` обновлён, ветки удалены (или явно сохранены), raw V2 artifacts не утекли в `main`, результат implementation локально проверен, checkpoint готов |

#### Default cleanup policy

После принятого V2-result Codex обязан:

- удалить local `review/v2/...` branch;
- удалить remote `review/v2/...` branch;
- удалить temporary V2 runtime artifacts (request, prompt, safety, response, ingest);
- обновить `V2_navigation.md` до `cleaned`;
- проверить, что raw V2 artifacts не попали в `main`.

#### Human override policy

Если человек явно просит сохранить ветку или artifacts:

- ветка/артефакты **не удаляются**;
- в `V2_navigation.md` фиксируется `kept_by_decision` или `cleanup_pending`;
- причина сохранения кратко записывается.

Если человек ничего отдельно не сказал — действует default cleanup policy.

Kilo при подготовке cleanup preview проверяет и фиксирует:

- remote review branch удалена или явно оставлена;
- local review branch удалена или явно оставлена;
- [`V2_navigation.md`](V2_navigation.md) обновлён;
- финальный статус установлен в `cleaned`, `cleanup_pending`, `kept_by_decision` или `superseded`;
- в `V2_navigation.md` сохранены минимум: `V2 ID`, `base commit`, `snapshot commit`, `compare link`, итоговый статус, `Branch State` и `Cleanup Decision`;
- raw V2 runtime artifacts не утекли в `main`;
- draft PR закрыт, помечен или подтверждён как отсутствующий.

## Жизненный цикл статусов V2

| Статус | Описание |
|--------|----------|
| `draft` | V2 request создан, но ещё не previewed |
| `previewed` | `/v2 preview` показан человеку |
| `awaiting_human_push_approval` | Preview принят, ждём разрешения на push |
| `snapshot_pushed` | Review branch запушен в public GitHub |
| `prompt_ready` | Instantiated V2 prompt создан, но ещё не выдан человеку |
| `waiting_external_answer` | Prompt выдан человеку для внешнего чата, ждём ответ |
| `raw_response_captured` | Сырой ответ внешнего чата сохранён вручную |
| `ingested` | Kilo understanding summary готов после ручного ingest |
| `implementation_planned` | Предложен план реализации по мотивам ответа |
| `implemented` | Изменения приняты и реализованы |
| `superseded` | Request перекрыт более новым V2 request |
| `cleaned` | Cleanup выполнен, ветки удалены |
| `cleanup_pending` | Cleanup явно отложен человеком, ветки/артефакты сохранены |
| `kept_by_decision` | Ветка или артефакты сохранены по явному решению человека |

### Обязательная последовательность переходов

Каноническая цепочка статусов (нельзя проскочить `push → prompt`):

```text
draft
→ previewed
→ awaiting_human_push_approval
→ snapshot_pushed
→ prompt_ready
→ waiting_external_answer
→ raw_response_captured
→ ingested
→ implementation_planned
→ implemented
→ cleaned / cleanup_pending / kept_by_decision
```

`snapshot_pushed` без последующего `prompt_ready` или `waiting_external_answer` является нарушением протокола. Статус `waiting_external_answer` означает: «snapshot запушен + instantiated prompt создан + prompt передан человеку». Без prompt статус не должен продвигаться дальше `snapshot_pushed`.

`Snapshot Commit` — immutable review target. Это ровно тот commit, который был запушен в review-ветку и показан внешнему чату через commit-pinned links. Последующие implementation commits не заменяют `Snapshot Commit`; они живут отдельно в summary, implementation artifacts или product commits.

## Классы артефактов и правила хранения

### Публичные и стабильные (tracked в `main`)

- `.ai/external_reviews/README.md` — этот файл
- `.ai/external_reviews/V2_navigation.md` — индекс V2 requests
- `.ai/external_reviews/templates/*` — шаблоны
- `.ai/external_reviews/summaries/` — только sanitized accepted summaries и только после explicit human/Codex acceptance

### Runtime artifacts (в `review/v2/...` branch, не в `main`)

- `.ai/external_reviews/requests/` — V2 request reports
- `.ai/external_reviews/prompts/` — generated V2 prompts
- `.ai/external_reviews/safety/` — safety checklists и safety reports
- changed-file inventory
- временные screenshots (только явно разрешённые для этого review)

### Raw response и ingest artifacts (не в `main` по умолчанию)

- `.ai/external_reviews/responses/` — raw external answers
- `.ai/external_reviews/ingest_summaries/` — Kilo understanding summaries
- draft implementation plan

### Local-only runtime evidence, не для published external links

Следующие runtime paths не считаются published evidence для внешнего V2 review и не должны включаться в prompt как GitHub-readable source of truth:

- `.ai/reports/`
- `.ai/handoffs/`
- `.ai/plans/sessions/`

Причина:

- эти пути являются локальными Kilo/Codex runtime artifacts;
- часть из них игнорируется Git и не обязана существовать в GitHub;
- ссылки на них во внешнем prompt могут дать 404 и ломают traceability.

Для внешнего V2 review использовать только:

- committed protocol docs;
- `V2_navigation.md`;
- commit-pinned raw file links;
- compare links;
- request/prompt/safety artifacts, если они реально опубликованы и доступны по ссылке.

**Правило по умолчанию:** Raw V2 runtime artifacts не трекаются в `main`. Они живут в `review/v2/...` branch или local-only до explicit решения о публикации sanitized summary.

### Sanitized accepted summary

Может быть поднят в `main` после explicit human/Codex acceptance и должен быть очищен от:

- raw external answer verbatim;
- приватных локальных путей;
- screenshots и binary artifacts (без отдельного одобрения);
- secrets и personal data;
- временных гипотез отладки, которые не были приняты;
- полного debug log.

## Нормализованные runtime paths

Первая версия V2 использует следующие стандартные пути:

- `.ai/external_reviews/requests/` — request reports;
- `.ai/external_reviews/prompts/` — prompts для внешнего чата;
- `.ai/external_reviews/safety/` — safety checklist и safety reports;
- `.ai/external_reviews/responses/` — raw external answers;
- `.ai/external_reviews/ingest_summaries/` — Kilo understanding summaries;
- `.ai/external_reviews/summaries/` — sanitized accepted summaries.

Если конкретная V2-сессия использует другой путь, это нужно явно отметить в request и в `V2_navigation.md`.

## Минимальный обязательный набор runtime artifacts

Для каждого реального V2 run обязательно наличие следующих артефактов:

### До push (обязательно)

- **Request report** — заполненный [`v2_request_template.md`](templates/v2_request_template.md) в `.ai/external_reviews/requests/V2-YYYYMMDD-HHMMSS_request.md`
- **Safety report** — заполненный [`v2_safety_checklist.md`](templates/v2_safety_checklist.md) в `.ai/external_reviews/safety/V2-YYYYMMDD-HHMMSS_safety.md`
- **Review branch/snapshot metadata** — base commit, snapshot commit, compare link

### После push (обязательно)

- **Instantiated prompt** — заполненный [`v2_prompt_template.md`](templates/v2_prompt_template.md) с реальными commit-pinned ссылками в `.ai/external_reviews/prompts/V2-YYYYMMDD-HHMMSS_prompt.md`

### После внешнего ответа (обязательно)

Один из двух ingest-путей:

1. **Direct paste:** ответ вставлен в ordinary Kilo run. В этом случае:
   - `V2_navigation.md` должен содержать `Response Location: pasted directly into Kilo run; raw response not stored separately`
   - Ingest summary всё равно обязателен в `.ai/external_reviews/ingest_summaries/V2-YYYYMMDD-HHMMSS_ingest.md`
   
2. **Local response file:** ответ сохранён в `.ai/external_reviews/responses/V2-YYYYMMDD-HHMMSS_response.md`
   - `V2_navigation.md` содержит путь к response-файлу
   - Ingest summary обязателен

### После implementation (обязательно)

- **Финальное обновление `V2_navigation.md`** — статус, branch state, cleanup decision
- **Cleanup decision** — `cleaned`, `cleanup_pending` или `kept_by_decision`

### Legacy exception для первого реального pilot

Первый реальный V2 pilot (`V2-20260526-140000`) был завершён до полного ужесточения ingest-artifact discipline. Поэтому для него допускается legacy-исключение: ответ был ingest-нут без отдельно сохранённого ingest summary artifact.

Это не норма для будущих запусков.

Для всех следующих V2 runs правило жёсткое:

- direct paste разрешён;
- но ingest summary artifact всё равно обязан существовать.

## Path/write fallback

Если запись в `.ai/external_reviews/...` не удалась (path truncation, missing directory, tool error):

1. **Явно создать директорию** — `mkdir` для целевого пути, если её нет.
2. **Повторить запись** — использовать точный путь, проверить, что имя файла не обрезано.
3. **Проверить, что файл реально существует** — перечитать файл после записи, убедиться, что он не пустой.
4. **Если всё ещё не удалось** — не идти дальше молча. Завершить шаг как blocked process issue:
   - Статус: `blocked-no-source-of-truth` или `blocked-needs-human-decision`
   - Указать intended path
   - Не делать push, пока артефакт не создан
   - Объяснить человеку, что именно не получилось записать

Молчаливый пропуск артефакта из-за tool error является нарушением протокола.

## Template vs instantiated artifacts

Как и в `/v1`, V2 использует два разных слоя:

1. **Templates** в `.ai/external_reviews/templates/`
   - содержат placeholders;
   - объясняют структуру;
   - не обязаны содержать живые GitHub raw/blob URL.

2. **Instantiated artifacts** в runtime paths
   - создаются под конкретный `V2 ID`;
   - содержат уже реальные ссылки;
   - именно их человек показывает внешнему чату или использует для ingest.

Для первой версии V2 это значит:

- `templates/v2_request_template.md` — только шаблон;
- `templates/v2_prompt_template.md` — только шаблон;
- реальные ссылки должны появляться в instantiated файлах, например:
  - `.ai/external_reviews/requests/V2-YYYYMMDD-HHMMSS_request.md`
  - `.ai/external_reviews/prompts/V2-YYYYMMDD-HHMMSS_prompt.md`

Если в шаблоне виден `{{placeholder}}`, это не missing link и не ошибка публикации. Это признак template-layer. Проверять нужно уже instantiated request/prompt.

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

## YOLO Mode Interaction

V2 и YOLO-режим связаны через механизм остановки и эскалации:

- **V2 часто запускается после честной остановки Kilo.** Когда Kilo честно останавливается в статусе `blocked-v2-recommended`, следующим шагом может быть `/v2 preview` для внешнего senior review.
- **Kilo не должен бесконечно «додавливать» задачу.** YOLO Stop Gates требуют остановки при рискованных или бессмысленных действиях, а не бесконечных попыток.
- **После blocked report пользователь может:**
  - разрешить локально продолжить (например, если проблема оказалась проще);
  - попросить подготовить `/v2 preview` для внешнего senior review;
  - отменить часть изменений и вернуться к предыдущему состоянию;
  - передать вопрос Codex для перепланирования.

### YOLO + human push gate

`awaiting_human_push_approval` — **валидный stop-state даже в YOLO-режиме.** Kilo обязан остановиться на этом шаге и не продолжать автономно.

- YOLO не отменяет V2 push approval.
- Продолжение без явного human confirmation является нарушением протокола.
- Один короткий human approval step на push gate разрешён и обязателен.
- Если Kilo в YOLO не может использовать `ask_followup_question` для push gate, он должен явно написать в output: «Требуется human push approval. Разрешаю push review ветки [branch name] в GitHub?» и остановиться.

Полные правила YOLO Stop Gates, V2 Recommendation Gate и Blocked Report Contract описаны в [`AGENTS.md`](../../AGENTS.md).

## Связанные документы

- [V2_navigation.md](V2_navigation.md) — индекс V2 requests
- [v2_request_template.md](templates/v2_request_template.md) — шаблон V2 request
- [v2_prompt_template.md](templates/v2_prompt_template.md) — шаблон V2 prompt для внешнего чата
- [v2_response_template.md](templates/v2_response_template.md) — шаблон записи V2 response
- [v2_ingest_summary_template.md](templates/v2_ingest_summary_template.md) — шаблон Kilo understanding summary
- [v2_safety_checklist.md](templates/v2_safety_checklist.md) — safety checklist перед V2 push

## Ссылки на внешние контракты

- [`AGENTS.md`](../../AGENTS.md) — workflow contract
- [`.ai/rules/agent_protocol.md`](../rules/agent_protocol.md) — агентный протокол
- [`.ai/rules/kilo_mode_contract.md`](../rules/kilo_mode_contract.md) — контракт Kilo modes
- [`.ai/external_chats/external_chat_rules.md`](../external_chats/external_chat_rules.md) — правила для внешнего чата
- [`.ai/policies/human_review_policy.md`](../policies/human_review_policy.md) — политика human review
- [`.ai/policies/bug_tracking_policy.md`](../policies/bug_tracking_policy.md) — политика bug tracking
- [`.ai/plans/master/v2_external_senior_review_system.md`](../plans/master/v2_external_senior_review_system.md) — master plan V2

## История

- 2026-05-26 — первая версия документации. Основана на master plan после внешней критики (V1-20260526-103939).
- 2026-05-26 — hardening после первого реального V2 pilot (0026): добавлен обязательный post-push chain, `/v2` interrupt contract, Codex-owned cleanup, lifecycle hardening с `prompt_ready`/`cleanup_pending`/`kept_by_decision`, минимальный runtime artifact set, YOLO push-gate stop-state, path/write fallback. Основано на внешнем senior review (V1-20260526-213514).
- 2026-05-28 — добавлен обязательный `restore-to-working-branch` step после V2 implementation: содержательный patch не может считаться выполненным, пока он не возвращён из `review/v2/...` в исходную рабочую ветку и не подтверждён локальным diff.
