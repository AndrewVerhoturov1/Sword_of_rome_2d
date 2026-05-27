# План внедрения V3 workflow и режима `Kilo Notebook V3`

Версия: 0.5
Статус: Phase 0 завершён, Phase 1 завершён (2026-05-27), Phase 2 завершён (2026-05-27), Phase 3 завершён (2026-05-27), Phase 4 завершён (2026-05-27)
Назначение: зафиксировать repo-grounded план внедрения V3 как третьего workflow route и как отдельного Kilo mode для artifact-producing задач.

---

## 1. Входные источники

План опирается на четыре слоя:

1. V1-ответ [`V1-20260527-181041`](../../external_chats/notebook/2026-05-27_V1-20260527-181041_plan-vnedreniya-v3-artifact-producing-workflow-v-tekuschuyu.md).
2. Текущий draft-contract [`v3_artifact_producing_workflow_contract.md`](v3_artifact_producing_workflow_contract.md).
3. Текущий V2 protocol [`../../external_reviews/README.md`](../../external_reviews/README.md).
4. Текущие repo-ограничения по mode/role в [`../../../AGENTS.md`](../../../AGENTS.md), [`../../README.md`](../../README.md), [`../../rules/agent_protocol.md`](../../rules/agent_protocol.md), [`../../rules/kilo_mode_contract.md`](../../rules/kilo_mode_contract.md), [`../../../scripts/validate_kilo_contract.py`](../../../scripts/validate_kilo_contract.py).

---

## 2. Что фиксируем как целевое решение

### 2.1. V3 остается отдельным workflow route

Финальная формула остается такой:

- V1 = внешний prompt-only анализ.
- V2 = внешний senior review зафиксированного WIP/snapshot.
- V3 = внешний artifact-producing workflow.

### 2.2. Для V3 создается отдельный Kilo mode

Это решение зафиксировано отдельно и не считается optional:

- внутреннее mode-значение: `kilo-notebook-v3`;
- UI-значение: `Kilo Notebook V3`;
- основная роль: `Notebook Agent`.

Важно:

- существующий `kilo-notebook` остается строго `/v1-only`;
- существующий `kilo-recorder` остается строго `/r1-only`;
- V3 не должен перегружать или переопределять `kilo-notebook`;
- для V3 нужен собственный mode-specific contract, а не скрытый reuse старого notebook flow.

### 2.3. V3 не вводит глобический запрет на product code

Здесь принимается ключевая мысль из V1:

- V3 core не запрещает `product_code` навсегда;
- scope задается в каждом конкретном V3 request;
- но MVP и первый pilot идут в безопасном режиме `docs_only` / `workflow_docs` / `schemas`.

---

## 3. Repo-specific поправка к V1

V1 правильно описывает целевую архитектуру, но в текущем repo есть важное ограничение: новый режим нельзя считать существующим, пока он не проведен через canon и tooling.

Сейчас в repo:

- допустимые `Kilo mode` перечислены явно;
- `kilo-notebook` закреплен как `/v1-only`;
- `kilo-recorder` закреплен как `/r1-only`;
- список mode-значений зашит не только в docs, но и в validator/script layer.

Следствие:

1. Внедрение V3 надо начинать не с ZIP-автоматики, а с contract alignment.
2. `Kilo Notebook V3` должен появиться одновременно в правилах, навигации, шаблонах, валидаторах и bootstrap-подсказках.
3. Без этого получится декоративный режим, который описан в тексте, но ломается в validator/preflight.

---

## 4. Целевое состояние V3 в этом repo

После внедрения в repo должны существовать:

- отдельный workflow-слой `.ai/v3/`;
- отдельный жизненный цикл V3 request -> external artifact package -> V3 import -> journal -> Codex review -> human verdict;
- отдельный mode-specific contract для `kilo-notebook-v3`;
- отдельная навигация `V3_navigation.md`;
- отдельные шаблоны request/manifest/journal/review/revision;
- отдельный manual setup для `Kilo Notebook V3`;
- отдельный validator/staging слой для V3 packages;
- отдельные acceptance gates для docs/script/product-code scopes.

---

## 5. Роль V1, V2 и Kilo в rollout

### 5.1. Как использовать V1

V1 здесь нужен не для исполнения, а для внешней критики и refinement:

- review структуры V3 contracts;
- review wording для external prompts;
- review package schema и review gates;
- critique пилотного процесса до hardening.

### 5.2. Как использовать V2

V2 нужен не в начале, а после появления реальных V3 scripts/rules diff:

- bounded review validator/staging scripts;
- review safety логики импортера;
- review narrow product-code expansion rules;
- review risky workflow-rule changes на живом branch snapshot.

### 5.3. Как использовать Kilo

Основная substantive работа идет через последовательные Kilo-задачи:

- docs/rules sync;
- prompt/template layer;
- validator/script layer;
- pilot import;
- hardening после внешнего review.

---

## 6. Фазы внедрения

## Phase 0. Contract Alignment ✅ (завершён — 2026-05-27)

Цель: узаконить сам факт нового режима `kilo-notebook-v3`.

Нужно сделать:

- добавить `kilo-notebook-v3` и `Kilo Notebook V3` в canon-списки допустимых mode-значений;
- зафиксировать, что `kilo-notebook` остается `/v1-only`;
- ввести mode-specific contract для `kilo-notebook-v3`;
- зафиксировать границу между `kilo-notebook-v3`, `kilo-notebook`, `kilo-recorder`, `kilo-handoff-runner`;
- решить, нужен ли отдельный shortcut `/v3` сейчас или это более поздний слой.

Файлы impact surface минимум:

- [`../../../AGENTS.md`](../../../AGENTS.md)
- [`../../README.md`](../../README.md)
- [`../../rules/agent_protocol.md`](../../rules/agent_protocol.md)
- [`../../rules/codex_orchestrator.md`](../../rules/codex_orchestrator.md)
- [`../../rules/kilo_mode_contract.md`](../../rules/kilo_mode_contract.md)
- [`../../rules/model_roster.md`](../../rules/model_roster.md)
- [`../../../scripts/validate_kilo_contract.py`](../../../scripts/validate_kilo_contract.py)

Выход фазы:

- новый режим canonically разрешен;
- validator/preflight знает про него;
- mode naming и role naming больше не конфликтуют.

## Phase 1. V3 Docs Foundation ✅ (завершён — 2026-05-27)

Цель: сделать V3 discoverable как самостоятельный workflow layer.

Создано:

- [`.ai/v3/README.md`](../../v3/README.md)
- [`.ai/v3/V3_navigation.md`](../../v3/V3_navigation.md)
- [`.ai/v3/contracts/README.md`](../../v3/contracts/README.md)
- [`.ai/v3/templates/README.md`](../../v3/templates/README.md)
- [`.ai/v3/prompts/README.md`](../../v3/prompts/README.md)
- [`.ai/v3/docs/README.md`](../../v3/docs/README.md)

Обновлено:

- [`../../repo_navigation.md`](../../repo_navigation.md) — секция V3 расширена, добавлены ссылки на foundation layer.

Выполнено через Kilo handoff [`0031_v3_phase1_docs_foundation`](../../handoffs/0031_v3_phase1_docs_foundation.md), report [`0031_v3_phase1_docs_foundation_report.md`](../../reports/0031_v3_phase1_docs_foundation_report.md).

Выход фазы:

- V3 виден в repo navigation;
- любой новый оркестратор понимает, где лежит V3 canon;
- foundation layer создан, но без operational обещаний.

## Phase 2. Contract Pack ✅ (завершён — 2026-05-27)

Цель: описать V3 как формальный процесс, а не как идею.

Создано:

- [`v3_request_contract.md`](../../v3/contracts/v3_request_contract.md)
- [`v3_artifact_package_contract.md`](../../v3/contracts/v3_artifact_package_contract.md)
- [`v3_manifest_contract.md`](../../v3/contracts/v3_manifest_contract.md)
- [`v3_journal_contract.md`](../../v3/contracts/v3_journal_contract.md)
- [`v3_codex_review_contract.md`](../../v3/contracts/v3_codex_review_contract.md)
- [`v3_revision_contract.md`](../../v3/contracts/v3_revision_contract.md)
- [`v3_storage_policy.md`](../../v3/contracts/v3_storage_policy.md)
- [`v3_scope_policy.md`](../../v3/contracts/v3_scope_policy.md)
- [`v3_acceptance_policy.md`](../../v3/contracts/v3_acceptance_policy.md)

Обновлено:

- [`../../v3/README.md`](../../v3/README.md) — статус Phase 2
- [`../../v3/V3_navigation.md`](../../v3/V3_navigation.md) — contracts отметка
- [`../../v3/contracts/README.md`](../../v3/contracts/README.md) — полный список
- [`../../repo_navigation.md`](../../repo_navigation.md) — статус Phase 2

Выполнено через Kilo handoff [`0032_v3_phase2_contract_pack`](../../handoffs/0032_v3_phase2_contract_pack.md), report — [`0032_v3_phase2_contract_pack_report.md`](../../reports/0032_v3_phase2_contract_pack_report.md).

Ключевые решения этой фазы:

- поддерживать `scope` как поле запроса;
- MVP ограничить `action: create`;
- raw ZIP и staging хранить local-only по умолчанию;
- stable docs/contracts/templates хранить tracked.

## Phase 3. Prompt and Template Layer ✅ (завершён — 2026-05-27)

Цель: дать рабочие заготовки для каждого шага V3.

Создано:

- [`create_v3_request_prompt.md`](../../v3/prompts/create_v3_request_prompt.md)
- [`kilo_notebook_v3_mode_prompt.md`](../../v3/prompts/kilo_notebook_v3_mode_prompt.md)
- [`codex_v3_review_prompt.md`](../../v3/prompts/codex_v3_review_prompt.md)
- [`v3_revision_request_prompt.md`](../../v3/prompts/v3_revision_request_prompt.md)
- [`v3_request_template.md`](../../v3/templates/v3_request_template.md)
- [`v3_manifest_template.yaml`](../../v3/templates/v3_manifest_template.yaml)
- [`v3_journal_template.yaml`](../../v3/templates/v3_journal_template.yaml)
- [`v3_codex_review_template.md`](../../v3/templates/v3_codex_review_template.md)
- [`v3_revision_request_template.md`](../../v3/templates/v3_revision_request_template.md)

Обновлено:

- [`../../v3/prompts/README.md`](../../v3/prompts/README.md) — статус Phase 3, полный список.
- [`../../v3/templates/README.md`](../../v3/templates/README.md) — статус Phase 3, полный список.
- [`../../v3/README.md`](../../v3/README.md) — статус Phase 3.
- [`../../v3/V3_navigation.md`](../../v3/V3_navigation.md) — prompt/template layer, закрыта future additions секция для Phase 3.
- [`../../repo_navigation.md`](../../repo_navigation.md) — статус Phase 3, добавлены ссылки на prompts/templates.
- [`v3_workflow_implementation_plan.md`](v3_workflow_implementation_plan.md) — Phase 3 отмечен завершённым.

Выполнено через Kilo handoff [`0033_v3_phase3_prompt_and_template_layer`](../../handoffs/0033_v3_phase3_prompt_and_template_layer.md), report — [`0033_v3_phase3_prompt_and_template_layer_report.md`](../../reports/0033_v3_phase3_prompt_and_template_layer_report.md).

Ключевые решения этой фазы:

- Узаконен 5-template pack (v3_revision_request_template.md добавлен как обязательный).
- Template count inconsistency между plan (4) и navigation/docs (5) закрыта в пользу 5-template pack.
- Prompt для внешнего чата требует artifact package, а не совет.
- Prompt для `Kilo Notebook V3` описывает безопасный import flow без обещания готового runtime.
- Prompt для Codex review проверяет journal и реальные файлы, использует нормализованный verdict enum.

## Phase 4. Runtime Mode Integration ✅ (завершён — 2026-05-27)

Цель: сделать новый режим реально запускаемым, а не только описанным.

Выполнено:

- Создан setup guide [`../v3/docs/manual_kilo_notebook_v3_setup.md`](../v3/docs/manual_kilo_notebook_v3_setup.md).
- Обновлены portable bootstrap docs (manual_setup_checklist.md, verification_checklist.md) — добавлен шестой режим `Kilo Notebook V3`.
- Синхронизирован V3 docs layer (README.md, V3_navigation.md, docs/README.md).
- Обновлены global rules: AGENTS.md, .ai/README.md, agent_protocol.md, kilo_mode_contract.md — убран stale Phase 0 wording, зафиксирован актуальный статус.
- Обновлён repo_navigation.md (фаза V3, добавлена ссылка на setup guide).
- Синхронизирован prompt wording в kilo_notebook_v3_mode_prompt.md (версия 0.1 → 0.2).

Выполнено через Kilo handoff [`0034_v3_phase4_runtime_mode_integration`](../../handoffs/0034_v3_phase4_runtime_mode_integration.md), report — [`0034_v3_phase4_runtime_mode_integration_report.md`](../../reports/0034_v3_phase4_runtime_mode_integration_report.md).

Ключевые решения этой фазы:

- Setup guide описывает ручную настройку режима без scripted support.
- Bootstrap portable docs честно указывают, что V3 mode требует ручной настройки в UI.
- Global rules синхронизированы: больше нет утверждений, что `.ai/v3/` subsystem «ещё не создана».
- Phase 4 не включает `/v3` shortcut, не создаёт `scripts/v3/*`, не запускает pilot.

Выход фазы:

- новый режим имеет manual setup guide;
- bootstrap/docs знают о ручной настройке шестого режима;
- global/runtime docs больше не отстают от факта существования `.ai/v3/` слоя и prompt/template layer.

## Phase 5. Safe Pilot

Цель: провести первый живой V3-cycle в безопасной зоне.

Ограничения первого pilot:

- scope: `docs_only` или `workflow_docs`;
- allowed paths: только `.ai/v3/` и при необходимости `.ai/` workflow-слой;
- без product code;
- без overwrite существующих product files;
- без auto-execution scripts;
- с обязательным journal и `V3_navigation.md`.

Первый pilot должен доказать:

- внешний чат может стабильно собирать package нужной структуры;
- `Kilo Notebook V3` может его безопасно импортировать;
- Codex может проверить результат по реальным файлам;
- человек может дать понятный verdict.

## Phase 6. External Hardening

Цель: не доверять первому working варианту слишком рано.

Нужны два review-круга:

- V1-круг для critique contracts/prompts/manual flow;
- V2-круг для review реального validator/stager diff и safety logic.

После review:

- исправить rules;
- исправить prompts/templates;
- исправить validator/stager;
- обновить `V3_navigation.md` и master docs.

## Phase 7. Scripted Support

Цель: убрать ручную рутину там, где это уже безопасно.

Кандидаты на scripts:

- `scripts/v3/validate_v3_package.py`
- `scripts/v3/stage_v3_package.py`
- `scripts/v3/write_v3_journal.py`

Что не делать раньше времени:

- `apply_v3_package.py` с агрессивной автозаписью;
- авто-commit/push;
- broad import в product paths;
- сложный schema stack до подтверждения реальной полезности MVP.

## Phase 8. Expansion to Product-Code Scopes

Цель: допустить V3 к более сильным задачам только после доказанного безопасного MVP.

Условия входа:

- хотя бы один успешный docs-only pilot;
- отработанный journal flow;
- V2 review validator/stager logic;
- понятные overwrite и rollback rules;
- явные acceptance gates для product-code scope.

Для `product_code` обязательно:

- узкий `allowed_paths`;
- expected diff;
- forbidden paths;
- explicit overwrite policy;
- test/verification plan;
- Codex review;
- human review;
- при крупных изменениях рекомендуется V2 review до принятия.

---

## 7. Последовательность Kilo-задач

Ниже не один шаг, а рекомендуемая полная последовательность rollout.

1. Kilo Task A: обновить canon и mode-contract под `kilo-notebook-v3`.
2. Kilo Task B: создать `.ai/v3/` foundation и `V3_navigation.md`.
3. Kilo Task C: создать contracts/templates/prompts pack.
4. V1 Round 1: отдать эти материалы на внешний critique и собрать замечания.
5. Kilo Task D: встроить принятые V1 замечания.
6. Kilo Task E: обновить validators/bootstrap/prompt helpers под новый mode.
7. Kilo Task F: создать V3 validator/staging scripts draft.
8. V2 Round 1: провести bounded review scripts и risky workflow diff.
9. Kilo Task G: исправить замечания после V2.
10. Kilo Task H: провести первый docs-only pilot через `Kilo Notebook V3`.
11. Kilo Task I: зафиксировать итоги pilot в V3 docs/navigation и принять решение о расширении scope.

Все эти задачи должны идти последовательно: один запуск -> review -> следующий запуск.

---

## 8. MVP boundary

MVP V3 считается достигнутым, когда одновременно есть:

- разрешенный в canon режим `kilo-notebook-v3`;
- UI-имя `Kilo Notebook V3`;
- `.ai/v3/README.md`;
- `.ai/v3/V3_navigation.md`;
- contracts/templates/prompts для V3;
- manual setup guide для нового режима;
- рабочий validator/staging минимум;
- первый docs-only package;
- первый V3 journal;
- первый Codex review;
- первый human verdict.

MVP не требует:

- product-code pilot;
- auto-apply;
- auto-commit/push;
- переноса V3 в central core;
- shortcut `/v3`, если mode уже можно использовать вручную.

---

## 9. Основные риски

### Риск 1. Новый mode будет описан в тексте, но не проведен через tooling

Это даст ложную готовность.

Контрмера:

- считать Phase 0 и Phase 4 обязательными;
- не объявлять режим готовым, пока validator/preflight не знают про него.

### Риск 2. V3 начнет подменять Codex decision layer

Контрмера:

- внешний чат только генерирует package;
- `Kilo Notebook V3` только импортирует по правилам;
- Codex делает review;
- человек принимает решение.

### Риск 3. Слишком рано открыть product-code scope

Контрмера:

- docs-only MVP;
- V2 hardening перед расширением;
- отдельные gates для product code.

### Риск 4. Перегрузить V3 лишней автоматизацией в самом начале

Контрмера:

- сначала contracts, prompts, journal, validator;
- потом staged scripts;
- auto-apply и push только после доказанной зрелости.

---

## 10. Acceptance gates

Минимальные gates для внедрения самого V3 режима:

1. Canon gate: новый mode добавлен во все обязательные rule files и validator lists.
2. Discoverability gate: `.ai/v3/` и `V3_navigation.md` видны в navigation.
3. Prompt gate: есть рабочий request/template layer.
4. Runtime gate: `Kilo Notebook V3` имеет явный contract и setup guide.
5. Safety gate: есть manifest/journal/storage policy.
6. Review gate: есть Codex review template и реальный review flow.
7. Pilot gate: пройден хотя бы один docs-only pilot.
8. Human gate: человек подтверждает, что процесс понятен и воспроизводим.

---

## 11. Итоговая формула внедрения

V3 в этом repo надо внедрять не как одну фичу и не как один prompt, а как отдельный workflow subsystem:

- с собственным режимом `kilo-notebook-v3`;
- с собственным `.ai/v3/` слоем;
- с собственными contracts/templates/prompts/navigation;
- с обязательным journal и Codex review;
- с V1 как внешним critique-инструментом;
- с V2 как hardening/review-инструментом;
- с поэтапным переходом от docs-only pilot к более сильным scope.

Главное правило:

> `Kilo Notebook V3` должен появиться не номинально, а как полностью проведенный через canon, tooling и pilot workflow отдельный режим.
