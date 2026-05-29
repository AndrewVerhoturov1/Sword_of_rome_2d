# План внедрения V3 workflow и режима `Kilo Notebook V3`

Версия: 0.12
Статус: Phase 0 завершён, Phase 1 завершён (2026-05-27), Phase 2 завершён (2026-05-27), Phase 3 завершён (2026-05-27), Phase 4 завершён (2026-05-27), Phase 5 полностью завершён и практически доказан (2026-05-29). Post-import testing correction layer внедрён (2026-05-29). Post-import testing flow hardened (2026-05-29). Phase 6 завершён (lifecycle cleanup/hardening). Phase 7 foundation запущен (2026-05-29): scripted support foundation создан (`scripts/v3/` helper layer).
Назначение: зафиксировать repo-grounded план внедрения V3 как отдельного workflow route и отдельного Kilo mode для artifact-producing задач.

---

## 1. Входные источники

План опирается на:

1. V1-ответ [`V1-20260527-181041`](../../external_chats/notebook/2026-05-27_V1-20260527-181041_plan-vnedreniya-v3-artifact-producing-workflow-v-tekuschuyu.md).
2. Root-cause analysis [`V1-20260528-031912`](../../external_chats/notebook/2026-05-28_V1-20260528-031912_updated-root-cause-analysis-after-user-clarified-that.md).
3. Draft-contract [`v3_artifact_producing_workflow_contract.md`](v3_artifact_producing_workflow_contract.md).
4. Repo-level workflow rules в [`../../../AGENTS.md`](../../../AGENTS.md) и `.ai/rules/*`.

---

## 2. Что фиксируем как целевое решение

### 2.1. V3 остаётся отдельным workflow route

- V1 = внешний prompt-only анализ.
- V2 = внешний senior review зафиксированного WIP/snapshot.
- V3 = внешний artifact-producing workflow.

### 2.2. Для V3 создаётся отдельный Kilo mode

- внутреннее mode-значение: `kilo-notebook-v3`;
- UI-значение: `Kilo Notebook V3`;
- task role: `Notebook Agent`.

Важно:

- `kilo-notebook` остаётся `/v1-only`;
- `kilo-recorder` остаётся `/r1-only`;
- V3 не подменяет `kilo-notebook`;
- setup guide не равен факту, что режим уже настроен в живом UI.

### 2.3. V3 не равен немедленному import-stage

После root-cause анализа фиксируем важную поправку:

```text
V3 route в целом включает import-stage,
но текущий rollout должен различать:
external artifact generation,
pre-Kilo package review,
Kilo UI setup,
Kilo import.
```

Нельзя считать, что получение ZIP автоматически означает готовность к Kilo import.

---

## 3. Целевое состояние V3 в этом repo

После rollout в repo должны существовать:

- отдельный `.ai/v3/` workflow-слой;
- отдельный lifecycle `request -> external package -> import -> journal -> Codex review -> human verdict`;
- mode-specific contract для `kilo-notebook-v3`;
- отдельная V3 navigation;
- request/prompt/template layer;
- setup guide;
- validator/staging support;
- явные process gates между pre-Kilo и import-stage.

---

## 4. Роль V1, V2 и Kilo в rollout

### 4.1. V1

V1 нужен для:

- critique contracts/prompts;
- process root-cause analysis;
- review rollout wording и phase split.

### 4.2. V2

V2 нужен позже:

- для bounded review risky validator/staging logic;
- для review scripted support;
- для review расширения в более сильные scopes.

### 4.3. Kilo

Kilo делает substantive execution только там, где шаг уже реально вошёл в его lane.

Критично:

- Kilo не должен появляться слишком рано как будто import-stage уже доступен;
- substantive run для `kilo-notebook-v3` допустим только после выполнения import gates.

---

## 5. Завершённые фазы

### Phase 0. Contract Alignment ✅

Узаконен сам факт режима `kilo-notebook-v3`.

### Phase 1. V3 Docs Foundation ✅

Создан `.ai/v3/` foundation layer.

### Phase 2. Contract Pack ✅

Создано 9 V3-контрактов.

### Phase 3. Prompt and Template Layer ✅

Создан prompt/template layer.

### Phase 4. Runtime Mode Integration ✅

Создан setup guide и synced docs для ручной настройки режима.

Важно: завершение Phase 4 не означает, что import pilot уже можно запускать автоматически.

---

## 6. Phase 5 - Safe Pilot (split after root-cause analysis)

Старое описание `Phase 5 = первый живой V3-cycle` было слишком грубым. Теперь делим его на четыре явные подфазы.

### Phase 5A. External Artifact Generation Pilot ✅

Цель:

- проверить, что внешний чат умеет читать commit-pinned GitHub links;
- проверить, что он умеет собрать валидный V3 artifact package;
- не трогать Kilo import.

Ограничения:

- scope: безопасный docs-layer, для текущего цикла `workflow_docs`;
- один узкий package test;
- без Kilo import;
- без manual staging как обязательства для человека;
- без заявлений, что repo уже изменён.

Выход:

- внешний ZIP/package реально существует;
- package можно review-ить;
- package ещё не imported.

Фактический результат:

- цикл `V3-20260528-195750-phase5A-5C-deep-doc-pack` вернул валидный ZIP package;
- package содержит 3 больших русскоязычных `.md`-файла по `5A`, `5B`, `5C`;
- package не делает ложных claims про repo write, import, journal или update navigation.

### Phase 5B. Pre-Kilo Package Review ✅

Цель:

- проверить ZIP, manifest, checksums, список файлов, allowed/forbidden paths;
- отделить качество package от готовности import-stage.

Проверяется:

- структура ZIP;
- совпадает ли набор `expected files`;
- валиден ли manifest;
- совпадают ли hashes;
- нет ли scope drift.

Выход:

- `external_package_received`;
- `pre_kilo_package_review`;
- package либо `valid_for_future_import`, либо `needs_revision`.

Фактический результат:

- ZIP проверен по структуре, manifest, checksums и содержанию файлов;
- критичных проблем не найдено;
- pre-Kilo verdict: `valid_for_future_import`;
- import-stage ещё не начат.

### Phase 5C. Kilo Notebook V3 UI Setup ✅

Цель:

- реально настроить `Kilo Notebook V3` в живом UI;
- зафиксировать, что режим существует не только в docs.

Проверки:

- режим виден в UI;
- выбран правильный mode name;
- если UI поддерживает mode prompt, он связан с V3-specific prompt;
- человек подтверждает дату/факт настройки.

Выход:

- `kilo_mode_configured`;
- import-stage теперь теоретически возможен, но ещё не выполнен.

Фактический результат:

- режим `Kilo Notebook V3` создан в UI;
- режим пережил restart VS Code;
- `Kilo Notebook V3` отделён от старого `Kilo Notebook`.

### Phase 5D. Kilo Import Pilot ✅ (практически доказан)

Цель:

- дать уже проверенный package в `Kilo Notebook V3`;
- пройти import/check/write/journal flow;
- потом перейти к Codex review и human verdict.

Только здесь допустимы:

- реальный import-run через `Kilo Notebook V3`;
- package source для raw input;
- staging/inbox, если он выбран как текущий transport path;
- реальный journal draft.

Фактический результат:

- import pilot впервые выполнен на package `V3-20260528-195750-phase5A-5C-deep-doc-pack`;
- 3 docs-файла импортированы в `.ai/v3/docs/`;
- journal draft создан;
- lifecycle entry обновлена;
- первый run записал результат не в workspace root, а во внешний `Documents` root, после чего import был восстановлен в правильный repo root;
- позже чистый docs-only цикл `V3-20260529-040855-project-and-sword-of-rome-briefs` прошёл уже напрямую в правильном repo без shadow-write в `Documents`;
- это подтверждает, что при совпадении workspace root и repo root базовый import/check/write/journal flow работает штатно.

**Verdict: Phase 5 практически доказан.** Два успешных import-цикла (один с recovery, один чистый) подтверждают, что базовый import/check/write/journal flow работает. Главный вопрос «работает ли вообще import» больше не является текущим blocker.


---

## 7. Hard gates before import-stage

Запуск `Kilo Notebook V3` нельзя делать, пока одновременно не выполнены все условия:

1. Реальный external package уже получен.
2. Package прошёл pre-Kilo review или хотя бы признан пригодным к import-test.
3. `Kilo Notebook V3` реально настроен в UI.
4. Явно выбран transport method.
5. Человек подтвердил, что сейчас тестируется import-stage, а не только artifact generation.

Если хотя бы один gate не выполнен, статус должен оставаться в одном из pre-Kilo состояний:

- `waiting_external_package`
- `external_package_received`
- `pre_kilo_package_review`
- `kilo_mode_not_configured`

---

## 8. Transport policy for current system state

До scripted support нельзя притворяться, что transport уже canonically solved.

Для текущего состояния системы правильно так:

- внешний чат возвращает package;
- человек может хранить ZIP локально;
- Codex/человек могут review-ить package до import-stage;
- `.ai/v3/staging/` используется только если уже начался import-stage и выбран repo-local staging fallback;
- человек не обязан заранее руками раскладывать ZIP по repo-paths до explicit import-stage.

---

## 9. Post-import testing correction layer (внедрён 2026-05-29, hardened 2026-05-29)

После доказанного import flow в Phase 5D в V3 workflow внедрён лёгкий post-import testing layer, а затем усилен через flow hardening.

### 9.1. Модель

```text
V3 external artifact generation is not testing.
Kilo Notebook V3 import is not testing.
Post-import testing is a lightweight separate step:
- notebook auto-emits POST_IMPORT_TEST_PROMPT.md после импорта (без ожидания вопроса),
- ordinary Kilo code run сначала показывает Execution split proposal человеку,
- человек согласует split (может перераспределить),
- Kilo code run выполняет Machine checks,
- Kilo code run пишет machine-check report в canonical file .ai/v3/test_reports/<V3-ID>_machine_check_report.md,
- human checks via manual review,
- Codex читает machine-check report как главный источник результатов.
```

### 9.2. Ключевые сущности

- `POST_IMPORT_TEST_PROMPT.md` — опциональный root-level control file V3 package. Не project target file. Следует строгой четырёхсекционной структуре:
  1. `Execution split proposal` (tester-first negotiation);
  2. `Machine checks`;
  3. `Human checks`;
  4. `Machine-check report output`.
- `manifest.post_import_testing` block — `mode: required | optional | waived`. Трёхрежимная модель:
  - `required` — prompt обязателен, notebook auto-emit жёстко обязателен, testing gate активен;
  - `optional` — prompt опционален, если есть — auto-emit показывается, но acceptance не блокирует;
  - `waived` — testing не требуется (default для чистого docs_only).
- `Kilo Notebook V3` **всегда** auto-emit-ит prompt после импорта при mode ≠ waived и наличии prompt. Ждать вопрос пользователя запрещено. При `mode = required` и отсутствии prompt — `blocked`.
- Machine-check report пишется в canonical file: `.ai/v3/test_reports/<V3-ID>_machine_check_report.md`. Не journal, не lifecycle registry. Codex читает этот файл как главный источник machine-check результатов.
- Codex review и acceptance policy учитывают testing gate: для `mode = required` нужен machine-check report в `.ai/v3/test_reports/` или testing waiver.

### 9.3. Что не изменилось

- Новые Kilo mode не введены.
- Handoff между `Kilo Notebook V3` и обычным код-режимом не создан.
- Новые статусы в `V3_navigation.md` не добавлены.
- Отдельный test journal не создан.
- Lifecycle model не раздут.

### 9.4. File-by-file coverage

Correction + hardening протянут через следующие файлы:

| Файл | Что добавлено/усилено |
|------|----------------------|
| `v3_artifact_package_contract.md` | `POST_IMPORT_TEST_PROMPT.md` как root-level control file, 4-секционная структура, canonical output path |
| `v3_manifest_contract.md` | Блок `post_import_testing`, правила required/optional |
| `v3_manifest_template.yaml` | `post_import_testing` block с комментариями |
| `v3_request_contract.md` | Post-import testing в request, Execution split proposal требования |
| `create_v3_request_prompt.md` | Инструкция требовать `POST_IMPORT_TEST_PROMPT.md` с 4 секциями |
| `v3_request_template.md` | Секция `Post-Import Testing` с новой структурой |
| `kilo_notebook_v3_mode_prompt.md` | **Hardened auto-emit**: всегда показывать prompt, blocked при mode=required без prompt |
| `v3_codex_review_contract.md` | Testing gate, canonical report path, Codex читает report первым |
| `v3_acceptance_policy.md` | Testing gate с canonical report path, waiver mechanism |
| `v3_codex_review_template.md` | `machine_check_report_ref` с canonical путём |
| `v3_storage_policy.md` | Machine-check reports в `.ai/v3/test_reports/` |
| `v3/README.md` | Process model с hardened flow |
| `codex_v3_review_prompt.md` | Шаг 4: проверить post-import testing, читать report file |

### 9.5. Практический flow для человека

1. Package импортируется через `Kilo Notebook V3`.
2. В конце `Kilo Notebook V3` **автоматически** выводит полный `POST_IMPORT_TEST_PROMPT.md` (без ожидания вопроса).
3. Человек копирует prompt в обычный Kilo code run.
4. Обычный Kilo code run **сначала** показывает `Execution split proposal` — человек согласует распределение проверок.
5. Kilo code run выполняет назначенные ему Machine checks.
6. Kilo code run пишет machine-check report в `.ai/v3/test_reports/<V3-ID>_machine_check_report.md`.
7. Человек делает manual Human checks.
8. Человек приносит результат в Codex.
9. Codex читает machine-check report из `.ai/v3/test_reports/` как главный источник, а не требует длинный pasted summary.
10. Codex даёт финальный verdict с учётом testing status.

## 10. Process clarification: external chat access wording (2026-05-29)

После реальных V3-циклов уточнена модель доступа внешнего чата во всей V3-системе:

- внешний чат может читать публичный GitHub-контекст по ссылкам из prompt;
- внешний чат не имеет прямого repo write access и не имеет локального filesystem-доступа к workspace;
- внешний чат создаёт ZIP artifact package, а не делает прямой repo write.

Старая грубая формулировка «нет доступа к репозиторию» заменена на точное разведение read/write/filesystem semantics во всех V3 canon-файлах, шаблонах и prompt-слое. Исторические request-файлы прошлых циклов не переписывались.

## 11. Phase 6 — Lifecycle Cleanup and Hardening (текущая фаза)

После того как Phase 5 практически доказан, следующий шаг — не scripted support и не новый pilot. Нужно закрыть ambiguity в lifecycle rules.

### 11.1. Что такое Phase 6

Phase 6 — это не новый import pilot и не scripted support. Это узкий, но жёсткий lifecycle hardening:

- формализовать closure rules: что происходит с imported cycle до и после human verdict;
- убрать ambiguity вокруг статуса tester prompt, machine-check report и journal draft;
- зафиксировать, что `imported != accepted`;
- описать accepted journal policy;
- создать минимальные локальные README для runtime-папок (`test_prompts/`, `test_reports/`);
- синхронизировать review/acceptance слой.

### 11.2. Ключевое правило

```text
imported != accepted
```

Импортированный цикл ещё не равен финальному accepted результату. После импорта могут идти:

- tester prompt handoff в обычный Kilo code run;
- machine-check report;
- human checks;
- Codex review;
- human verdict.

Только после этого цикл может стать `accepted`, `revision_requested` или `rejected`.

### 11.3. Границы Phase 6

Phase 6 не затрагивает:

- `V3_navigation.md` (новые статусы не вводятся);
- текущие imported cycles (victory-points и другие активные циклы);
- scripted support (`scripts/v3/*`);
- новые Kilo mode;
- новый lifecycle status;
- process gates между pre-Kilo и import-stage (они уже описаны в Phase 5).

### 11.4. Что остаётся на Phase 7

Phase 7 foundation создан (2026-05-29): `scripts/v3/` helper layer существует (validate, stage, journal draft). Оставшаяся часть Phase 7:

- дальнейшее расширение helper layer (если нужно);
- `/v3` shortcut активация (позже).
- `apply_v3_package.py` не создан и не планируется в текущем scope.


---

## 12. Полезные выводы из первого внешнего V3 package cycle

Первый успешный цикл `V3-20260528-195750-phase5A-5C-deep-doc-pack` дал не только package, но и полезную process-подсветку:

- `5A`, `5B`, `5C` действительно нужно держать отдельными шагами;
- внешний чат способен вернуть не советы, а валидный artifact package;
- pre-Kilo review как отдельный gate оправдан и полезен;
- `5C` надо делать как живой UI-check, а не считать docs доказательством готового режима;
- до `5D` нельзя смешивать transport, import, journal и acceptance.
- preset `Kilo Notebook V3` обязан жёстко фиксировать current workspace root, иначе notebook может создать параллельную `.ai/` вне repo;
- чистый цикл `V3-20260529-040855-project-and-sword-of-rome-briefs` показал, что root-issue не является неизбежным свойством режима: при правильном workspace binding импорт уже проходит без recovery.

---

## 13. MVP boundary

V3 MVP в текущем понимании достигается не тогда, когда просто есть mode prompt, а когда одновременно есть:

- canonically разрешённый режим;
- setup guide;
- request/prompt/template/contracts layer;
- хотя бы один успешный `Phase 5A` package test;
- хотя бы один `Phase 5B` package review;
- подтверждённый `Kilo Notebook V3` UI setup;
- хотя бы один `Phase 5D` import pilot;
- journal;
- Codex review;
- human verdict.

MVP не требует:

- product-code pilot;
- auto-apply;
- auto-commit/push;
- `/v3` shortcut;
- `scripts/v3/*` созданы в Phase 7 foundation.

Практическая поправка после цикла `V3-20260529-040855-project-and-sword-of-rome-briefs`:

- docs-only MVP-флоу уже доказан практически;
- следующий выбор теперь не между `работает ли вообще import`, а между `закрываем Phase 5 verdict/hardening` и `идём в scripted support`.

---

## 14. Главные риски

### Риск 1. Смешать target-state и current-state

Контрмера:

- явно различать pre-Kilo и import-stage;
- писать operational status отдельным блоком.

### Риск 2. Считать setup guide доказательством готового режима

Контрмера:

- требовать явный UI confirmation gate.

### Риск 3. Навесить на человека manual staging как будто это canon

Контрмера:

- staging включать только как selected transport method внутри import-stage.

### Риск 4. Считать валидный ZIP доказательством рабочего import flow

Контрмера:

- package quality и import readiness review-ить отдельно.

---

## 15. Итоговая формула

V3 надо внедрять не как один туманный pilot, а как staged subsystem:

- внешний package test;
- pre-Kilo review;
- UI setup;
- import pilot;
- review;
- verdict.

Главное правило:

> `Kilo Notebook V3` нельзя считать следующим шагом по умолчанию после получения ZIP. Сначала надо доказать, что package валиден, режим реально настроен, и текущая задача действительно вошла в import-stage.
