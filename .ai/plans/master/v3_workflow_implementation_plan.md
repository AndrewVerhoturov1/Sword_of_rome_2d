# План внедрения V3 workflow и режима `Kilo Notebook V3`

Версия: 0.8
Статус: Phase 0 завершён, Phase 1 завершён (2026-05-27), Phase 2 завершён (2026-05-27), Phase 3 завершён (2026-05-27), Phase 4 завершён (2026-05-27), Phase 5A завершён (2026-05-28), Phase 5B завершён (2026-05-28), Phase 5C завершён (2026-05-28), Phase 5D import pilot выполнен (2026-05-28, human verdict pending)
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

### Phase 5D. Kilo Import Pilot ✅

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

- import pilot выполнен на package `V3-20260528-195750-phase5A-5C-deep-doc-pack`;
- 3 docs-файла импортированы в `.ai/v3/docs/`;
- journal draft создан;
- lifecycle entry обновлена;
- первый run записал результат не в workspace root, а во внешний `Documents` root, после чего import был восстановлен в правильный repo root;
- human verdict ещё pending.

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

## 9. Следующие substantive шаги после process fix

1. Получить human verdict по первому `Phase 5D` import pilot.
2. Ужесточить preset `Kilo Notebook V3`: относить все target paths только к current workspace root.
3. Убрать ambiguity между package-local scope и downstream import permission wording.
4. После этого решить, нужен ли второй clean import pilot уже без recovery.

---

## 10. Полезные выводы из первого внешнего V3 package cycle

Первый успешный цикл `V3-20260528-195750-phase5A-5C-deep-doc-pack` дал не только package, но и полезную process-подсветку:

- `5A`, `5B`, `5C` действительно нужно держать отдельными шагами;
- внешний чат способен вернуть не советы, а валидный artifact package;
- pre-Kilo review как отдельный gate оправдан и полезен;
- `5C` надо делать как живой UI-check, а не считать docs доказательством готового режима;
- до `5D` нельзя смешивать transport, import, journal и acceptance.
- preset `Kilo Notebook V3` обязан жёстко фиксировать current workspace root, иначе notebook может создать параллельную `.ai/` вне repo.

---

## 11. MVP boundary

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
- `scripts/v3/*` до Phase 7.

---

## 12. Главные риски

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

## 13. Итоговая формула

V3 надо внедрять не как один туманный pilot, а как staged subsystem:

- внешний package test;
- pre-Kilo review;
- UI setup;
- import pilot;
- review;
- verdict.

Главное правило:

> `Kilo Notebook V3` нельзя считать следующим шагом по умолчанию после получения ZIP. Сначала надо доказать, что package валиден, режим реально настроен, и текущая задача действительно вошла в import-stage.
