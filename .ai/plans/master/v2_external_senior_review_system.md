# План системы V2 External Senior Review

## Статус

`approved-for-docs-implementation`

## Дата создания

2026-05-26

## Цель

Внедрить project-local протокол `/v2` для внешнего senior review поверх Kilo Code.

Смысл V2:

- Kilo готовит безопасный GitHub-видимый WIP snapshot;
- внешний чат смотрит pinned snapshot и сравнивает его с base;
- внешний чат даёт технический совет;
- Kilo сохраняет ответ, формулирует своё понимание и предлагает следующий шаг;
- внешний чат не получает repo authority и не превращается в исполнителя кода.

## Краткое описание

V2 — это строгий ручной протокол в `.ai/external_reviews/`.

Первая реализация включает только документацию и workflow-правила:

- без helper script;
- без автоматического push;
- без нового Kilo mode;
- без автоматического исправления кода после внешнего ответа;
- с tracked protocol/templates по умолчанию, но без raw V2 runtime artifacts в `main`;
- с review-ветками в текущем GitHub repo;
- с обязательным human confirmation перед каждым V2 push.

V2 отделяется от `/v1`:

- `/v1` — prompt-only route для planning/critique;
- `/v2` — route для review реального WIP snapshot;
- `/v2` даёт внешнему чату base/snapshot distinction и compare context;
- `/v2` требует более жёсткой safety-модели, потому что публикует рабочий код.

## Язык документов V2

Основные V2-документы и шаблоны должны быть написаны по-русски, чтобы пользователь мог их читать и проверять без дополнительного перевода.

Английский остаётся только там, где этого требует project policy:

- code identifiers;
- file/folder names;
- status values;
- branch names;
- JSON keys;
- machine-readable поля и технические идентификаторы.

## Зафиксированные решения

| Тема | Решение |
|---|---|
| Storage | `.ai/external_reviews/` |
| First scope | только docs/templates/rules |
| Helper script | не входит в первую версию |
| Kilo mode | новый режим не создаём |
| Typical Kilo mode | `Kilo Debugger` для stuck/debug cases, `Kilo Handoff Runner` для docs/protocol work |
| Artifact tracking | в `main` трекаем protocol docs, templates, navigation и sanitized accepted summaries; raw V2 runtime artifacts в `main` по умолчанию не трекаем |
| Review branch target | текущий repo `AndrewVerhoturov1/Sword_of_rome_2d` |
| Review branch format | `review/v2/YYYYMMDD-HHMMSS-short-topic` |
| Push gate | Kilo всегда спрашивает человека перед V2 push |
| External response authority | внешний ответ = planning/debug input, а не accepted fact без локальной проверки |
| Human review | обязателен для всех основных V2 документов |

## Обязательные файлы

Нужно создать project-local V2 area:

```text
.ai/
  external_reviews/
    README.md
    V2_navigation.md
    templates/
      v2_request_template.md
      v2_prompt_template.md
      v2_response_template.md
      v2_ingest_summary_template.md
      v2_safety_checklist.md
```

Нужно обновить repo-level discovery и workflow rules:

- `AGENTS.md`
- `.ai/repo_navigation.md`
- `.ai/rules/agent_protocol.md`
- `.ai/rules/kilo_mode_contract.md`
- relevant `.ai/prompts/` files, если они затрагивают external routes, Kilo mode rules или shortcut commands.

В первой версии не создавать automation scripts.

## Классы артефактов

V2 должен явно различать классы артефактов.

### Публичные и стабильные в `main`

- `.ai/external_reviews/README.md`
- `.ai/external_reviews/V2_navigation.md`
- `.ai/external_reviews/templates/*`
- sanitized accepted summaries, если пользователь решил, что они должны остаться в публичной истории проекта

### Runtime artifacts для активной V2 работы

- request report
- generated prompt
- changed-file inventory
- safety report
- временные screenshots, отдельно разрешённые для этого review

Правило по умолчанию:

- они могут жить в `review/v2/...` branch для активного review;
- в `main` по умолчанию не трекаются;
- всё, что ушло в public `review/v2/...` branch, надо считать опубликованным, даже если ветка потом удалена.

### Raw response и ingest artifacts

- raw external answer
- Kilo understanding summary
- draft implementation plan по мотивам внешнего ответа

Правило по умолчанию:

- raw response в `main` по умолчанию не трекается;
- позже можно поднять только sanitized accepted summary.

`Sanitized accepted summary` означает:

- без raw external answer;
- без приватных локальных путей;
- без screenshots и binary artifacts, если они отдельно не одобрены для публикации;
- без secrets и personal data;
- без временных гипотез отладки, которые не были приняты;
- без полного debug log.

Правило публикации:

- sanitized accepted summary можно публиковать только после explicit human/Codex acceptance.

## Требования к V2 протоколу

V2 должен описывать такие user-facing commands или command-like instructions:

- `/v2` — подготовить external senior review snapshot;
- `/v2 preview` — показать, что попадёт в snapshot, но не делать commit/push;
- `/v2 ingest` — обработать уже сохранённый внешний ответ и сформулировать Kilo understanding;
- `/v2 status` — показать состояние текущего V2 request;
- `/v2 cleanup` — провести cleanup временной review-ветки после human approval.

В первой версии это может быть задокументировано как manual Kilo protocol. CLI реализовывать не нужно.

### Правило preview

- `/v2 preview` обязателен перед любым V2 push;
- V2 push запрещён, если preview не был показан человеку и явно им не принят.

## Жизненный цикл статусов V2

V2 должен использовать компактный набор статусов:

- `draft`
- `previewed`
- `awaiting_human_push_approval`
- `snapshot_pushed`
- `waiting_external_answer`
- `raw_response_captured`
- `ingested`
- `implementation_planned`
- `implemented`
- `superseded`
- `cleaned`

`/v2 status` и `V2_navigation.md` должны использовать одну и ту же терминологию.

## Требования по безопасности

Перед любым V2 push Kilo обязан:

- проверить tracked changed files;
- проверить untracked files;
- проверить suspicious ignored files, если они релевантны;
- блокировать secrets и private/local-only files;
- явно показывать blocked files;
- явно показывать files proposed for snapshot;
- показывать branch name, base branch, base commit и exact files proposed for push;
- показывать large/binary hits и local-only path hits;
- спрашивать человека даже если safety-check чистый.

Правило по умолчанию:

- risky files не публикуются.

Human confirmation не должен быть расплывчатым вопросом “push?”. Пакет подтверждения должен содержать:

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
- простой yes/no prompt на русском языке.

### Предупреждение о публичности ветки

- push в public GitHub `review/v2/...` branch — это публикация;
- даже после удаления ветки commit links могут остаться во внешних чатах, кэше, форках, локальных копиях, скриншотах и заметках;
- если файл нельзя считать опубликованным, его нельзя пушить.

Примеры blocked или high-risk файлов:

- `.env`, `.env.*`
- key/certificate/credential files
- файлы под `_local/`
- generated output и build artifacts
- private images/assets
- archives
- logs
- large binary files без отдельного разрешения

## Требования к внешнему чату

V2 prompt должен требовать от внешнего чата:

- сначала прочитать V2 request report;
- открыть WIP files на snapshot commit;
- сравнить их с base files на base commit;
- явно сохранять distinction между base и snapshot;
- предпочитать commit-pinned links; branch links допустимы только как дополнительный контекст;
- перечислить, что было прочитано, в `Context Readback`;
- отделять verified facts от hypotheses;
- не утверждать, что он видел local runtime, tests, shell или git status;
- не писать patch так, как будто у него есть локальный repo access;
- давать bounded senior technical advice;
- явно говорить, чего не хватило и где граница уверенности.

Обязательная форма ответа должна включать:

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

## Граница V2 ingest

Первая версия не должна смешивать `kilo-recorder` и обычную интерпретацию ответа.

Базовая граница V2:

1. raw external answer сначала захватывается как узкий recording step;
2. отдельное обычное продолжение Kilo читает этот захваченный ответ;
3. только второй шаг пишет Kilo understanding и proposed implementation plan.

Так мы не ломаем существующий контракт `kilo-recorder`. В первой версии эту границу нужно описать явно, без изобретения нового Kilo mode.

## Требования к cleanup

`/v2 cleanup` должен проверять и фиксировать:

- remote review branch удалена или явно оставлена;
- local review branch удалена или явно оставлена;
- `V2_navigation.md` обновлён;
- финальный status установлен в `cleaned`, `superseded` или `implemented`;
- raw V2 runtime artifacts не утекли в `main`;
- draft PR закрыт, помечен или подтверждён как отсутствующий.

## Последовательность внедрения

### Шаг 0 — Tracker

Создать этот master plan.

Ожидаемый результат:

- `.ai/plans/master/v2_external_senior_review_system.md`

Human review: required.

### Шаг 1 — Уточнение плана перед реализацией

Использовать уже полученную внешнюю критику, чтобы ужесточить:

- artifact tracking policy;
- ingest/recorder boundary;
- push confirmation packet;
- commit-pinned link requirement;
- status lifecycle;
- cleanup expectations;
- rollout size.

Этот шаг уже отражён в текущем состоянии документа. Он остаётся как первый implementation checkpoint, а не как приглашение заново открыть широкое планирование.

### Шаг 2 — Kilo Docs Run

Один medium-to-large Kilo Docs run через `strong_model`.

Scope:

- создать V2 protocol docs;
- обновить repo-level rules для discoverability;
- зафиксировать artifact classes и default storage rules;
- зафиксировать, что новый Kilo mode не создаётся;
- зафиксировать human push confirmation;
- зафиксировать, что V2 сначала живёт только в этом repo;
- зафиксировать split между raw-response capture и ingest summary.

Рекомендуемый класс модели:

- `strong_model`

Default model:

- `DeepSeek V4 Pro`

Human review: required.

### Шаг 3 — Kilo Verifier Run

Read-only verification, кроме report.

Scope:

- проверить consistency docs;
- проверить, что не появились запрещённые Kilo mode values;
- проверить, что helper script не создан;
- проверить, что `.gitignore` не скрывает `.ai/external_reviews/`;
- проверить, что templates содержат обязательные секции;
- проверить, что V2 docs не разрешают push без human confirmation;
- проверить, что raw V2 request/response artifacts по умолчанию не трекаются в `main`;
- проверить, что V2 docs не обходят молча существующую recorder boundary.

Рекомендуемый класс модели:

- `strong_model`

Default model:

- `Kimi K2.6`

Причина:

- executor и verifier не должны использовать одну и ту же concrete model для важной workflow-задачи.

### Шаг 4 — Human Review

Human review обязателен до принятия docs patch.

Нужно проверить:

- понятны ли `/v2`, `/v2 preview`, `/v2 ingest`, `/v2 status`, `/v2 cleanup` простым русским языком;
- достаточно ли строгий push gate;
- устраивают ли правила хранения артефактов;
- реалистичен ли manual workflow без helper scripts.

### Шаг 5 — Codex Final Review

Codex проверяет:

- Kilo reports;
- фактический diff;
- наличие нужных файлов;
- consistency rule layer;
- search checks;
- `git status`;
- обязательные секции `Human Check` и `Баги и сложности`.

Checkpoint commit делать только после принятого результата.

### Шаг 6 — Low-Risk Manual Pilot

После принятия docs patch провести один low-risk manual pilot:

- начать с `/v2 preview`;
- использовать только non-secret issue;
- пушить только после explicit human approval;
- зафиксировать, что оказалось неудобным в ручном flow;
- уже после пилота решить, нужен ли tiny helper script.

## Проверки

Команды после реализации:

```powershell
git status --short --branch
rg -n "/v2|external_reviews|V2_navigation" AGENTS.md .ai
rg -n "kilo-v2|Kilo V2|kilo-builder|kilo-docs|kilo-tester|kilo-refactor" AGENTS.md .ai
```

Ручные проверки:

- `.gitignore` не должен скрывать `.ai/external_reviews/`;
- V2 templates должны включать `V2 ID`, base commit, snapshot commit, compare link, changed files, safety status, `Context Readback`, `Provider/Model` и verified/not verified separation;
- V2 docs должны явно говорить: no push without human confirmation, no secrets/private assets, no automatic fixes after external answer, no new Kilo mode, no helper script in first implementation;
- V2 docs должны явно говорить, что commit-pinned links — основной формат, branch links — только дополнительный;
- V2 docs должны различать public templates и raw V2 runtime artifacts;
- V2 docs должны явно описывать split между raw-response capture и ingest-summary.

## Точки human review

Human review обязателен для:

- этого master plan;
- V2 README/protocol;
- V2 external chat rules;
- V2 templates;
- любых repo-level rules, которые меняют поведение Kilo;
- любого будущего решения добавить automation.

Пользователь должен проверить:

1. Совпадает ли V2 с желаемым workflow.
2. Достаточно ли строг human push gate.
3. Приемлемы ли правила хранения `main` vs review-branch vs raw-response artifacts.
4. Достаточно ли просты Kilo instructions для ручного использования.
5. Не пропущены ли safety-risks вокруг private images, local-only folders и WIP branches.

## Что вне scope первой версии

- CLI implementation для `/v2`
- automatic branch creation
- automatic commit/push
- automatic raw link generation
- automatic ingest parsing
- draft PR creation
- generalization в central workflow core
- новый Kilo mode или UI setup
- tracking raw V2 request/response artifacts в `main` по умолчанию

## Критерии приёмки

- master plan существует и пригоден для review;
- структура `.ai/external_reviews/` определена;
- V2 protocol discoverable из repo-level rules;
- V2 templates достаточно полны для ручной работы Kilo;
- safety-check и always-confirm push gate описаны явно;
- V2 prompt rules требуют honest external readback и base/snapshot separation;
- artifact classes и default storage rules описаны явно;
- V2 ingest boundary не конфликтует молча с существующим recorder contract;
- helper script и automation не добавлены;
- новый Kilo mode не введён;
- требования human review описаны явно.

