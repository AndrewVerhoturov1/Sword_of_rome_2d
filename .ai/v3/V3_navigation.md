# V3 Navigation

Индекс V3 artifact-producing cycles для проекта `sword-of-rome-web`.

`V3_navigation.md` — это operational lifecycle index, как в `V1` и `V2`. Он нужен не только как справка по слою `.ai/v3/`, но и как живой журнал V3-циклов: что запросили у внешнего чата, какой пакет получили, что импортировал `Kilo Notebook V3`, какие файлы были созданы и чем цикл закончился.

## Текущий статус

**Phase 5 завершён, Phase 6 завершён, Phase 7 завершён (2026-05-29):** `/v3` shortcut активирован как explicit V3 import-entry mode, канонический шаблон создан, `scripts/v3/*` helper layer существует. Auto-apply запрещён.

### Operational status

- `Kilo Notebook V3` canonically разрешён.
- Setup guide существует.
- `/v3` shortcut активирован (Phase 7).
- `scripts/v3/*` созданы: validate, stage, journal helpers. `apply_v3_package.py` не создан.
- Живой UI-режим `Kilo Notebook V3`: `verified by human on 2026-05-28`.
- ZIP import capability в живом Kilo: `verified in one pilot on 2026-05-28`.
- External artifact generation и pre-Kilo package review уже подтверждены на одном цикле.
- Несколько успешных import-циклов подтвердили базовый flow.

### Current Phase 5 split

```text
Phase 5A - External Artifact Generation Pilot
Phase 5B - Pre-Kilo Package Review
Phase 5C - Kilo Notebook V3 UI Setup
Phase 5D - Kilo Import Pilot
```

Критическое правило:

```text
external_package_received != import_ready
```

## Обязательные точки обновления

| Этап | Когда | Что обновить |
|---|---|---|
| **Request creation** | После подготовки V3 request/prompt | Создать или обновить запись: `V3 ID`, дата, статус `request_prepared`, `Request Location`, `Prompt Location` |
| **Package received / reviewed** | После ответа внешнего чата и pre-Kilo review | Обновить статус (`external_package_received` или `package_reviewed`), `Package Source`, краткую `Summary` того, что сделал внешний чат |
| **Import** | После запуска `Kilo Notebook V3` | Обновить статус (`imported` или `import_blocked`), `Journal Location`, `Created Files` |
| **Verdict** | После Codex review и human verdict | Обновить статус (`accepted`, `revision_requested`, `rejected`) и итоговую `Summary` |

## Формат записи

| V3 ID | Date | Status | Topic | Request Location | Prompt Location | Package Source | Journal Location | Created Files | Summary |
|---|---|---|---|---|---|---|---|---|---|

### Допустимые значения полей

**Status:** `request_prepared`, `waiting_external_package`, `external_package_received`, `package_reviewed`, `kilo_mode_not_configured`, `import_blocked`, `imported`, `accepted`, `revision_requested`, `rejected`

**Request Location:** путь к V3 request-файлу, обычно `.ai/v3/requests/...`

**Prompt Location:** путь к prompt-файлу для внешнего чата, обычно `.ai/v3/requests/...`

**Package Source:** `human-provided archive link`, `local-only zip path`, `not stored in repo`, или другой явно понятный источник пакета

**Journal Location:** путь к journal draft или accepted journal entry. Если импорта ещё не было — `—`

**Created Files:** список реально созданных project files. До импорта — `—`

**Summary:** краткая суть того, что сделал внешний чат или что сделал `Kilo Notebook V3`

Важно:

- `V3_navigation.md` не хранит подробный технический trace import-run;
- подробности проверки, skipped reasons и source-package block живут в journal.

## Статусы

Статусы отражают жизненный цикл V3:

- `request_prepared` — request/prompt уже созданы
- `waiting_external_package` — prompt отдан человеку, ждём пакет
- `external_package_received` — внешний чат вернул архив или ссылку на архив
- `package_reviewed` — пакет проверен до Kilo import
- `kilo_mode_not_configured` — пакет есть, но `Kilo Notebook V3` ещё не подтверждён в UI
- `import_blocked` — import-run пытались начать, но он остановился по контракту
- `imported` — `Kilo Notebook V3` записал разрешённые файлы и создал journal
- `accepted` — цикл принят
- `revision_requested` — нужна доработка внешнего пакета
- `rejected` — пакет или import-run отклонён

## Записи

| V3 ID | Date | Status | Topic | Request Location | Prompt Location | Package Source | Journal Location | Created Files | Summary |
|---|---|---|---|---|---|---|---|---|---|
| V3-20260528-195750-phase5A-5C-deep-doc-pack | 2026-05-28 | `imported` | Большой русскоязычный V3 doc-package по `Phase 5A`, `Phase 5B` и `Phase 5C` | `.ai/v3/requests/V3-20260528-195750-phase5A-5C-deep-doc-pack_request.md` | `.ai/v3/requests/V3-20260528-195750-phase5A-5C-deep-doc-pack_prompt.md` | `local-only zip path: C:/Users/andre/Downloads/V3-20260528-195750-phase5A-5C-deep-doc-pack.zip` | `.ai/v3/journals/drafts/V3-20260528-195750-phase5A-5C-deep-doc-pack_journal.yaml` | `.ai/v3/docs/phase5A_external_artifact_generation_pilot_detailed_implementation.md, .ai/v3/docs/phase5B_pre_kilo_package_review_detailed_implementation.md, .ai/v3/docs/phase5C_kilo_notebook_v3_ui_setup_detailed_implementation.md` | Package imported into repo docs layer. Original notebook run resolved paths against external Documents root, then import result was recovered into current workspace and verified against manifest and hashes. Human verdict still pending. |
| V3-20260529-000139-pink-calculator-html-pilot | 2026-05-29 | `imported` | Узкий standalone product-code stress test: один розовый HTML-калькулятор без интеграции в текущее приложение | `.ai/v3/requests/V3-20260529-000139-pink-calculator-html-pilot_request.md` | `.ai/v3/requests/V3-20260529-000139-pink-calculator-html-pilot_prompt.md` | `local-only zip path: C:/Users/andre/Downloads/V3-20260529-000139-pink-calculator-html-pilot.zip` | `.ai/v3/journals/drafts/V3-20260529-000139-pink-calculator-html-pilot_journal.yaml` | `table-sandbox/v3-pilots/pink_calculator.html` | Standalone pink calculator HTML pilot imported into repo. First write went to wrong workspace root (Documents), corrected to actual repo (D:\\Codex+Kilocode\\projects\\sword-of-rome-web). SHA256 verified. Codex review and human acceptance still pending. |
| V3-20260529-032915-d6-dice-roller-pseudo3d | 2026-05-29 | `imported` | Узкий standalone product-code stress test: псевдо-3D имитация броска D6 на чистом 2D, с количеством и цветом кубиков | `.ai/v3/requests/V3-20260529-032915-d6-dice-roller-pseudo3d_request.md` | `.ai/v3/requests/V3-20260529-032915-d6-dice-roller-pseudo3d_prompt.md` | `local-only zip path: D:\Codex+Kilocode\projects\sword-of-rome-web\V3-20260529-032915-d6-dice-roller-pseudo3d_from_text2.zip` | `.ai/v3/journals/drafts/V3-20260529-032915-d6-dice-roller-pseudo3d_journal.yaml` | `table-sandbox/v3-pilots/d6_dice_roller_pseudo3d.html` | Standalone D6 Dice Roller pseudo-3D HTML pilot imported. Pure CSS 3D transforms, no external dependencies, inline CSS/JS, Russian UI. SHA256 verified. Journal draft created. Codex review and human acceptance still pending. |
| V3-20260529-040855-project-and-sword-of-rome-briefs | 2026-05-29 | `request_prepared` | Короткий docs-only пакет: отдельное описание проекта и отдельное описание модуля `Меч Рима` | `.ai/v3/requests/V3-20260529-040855-project-and-sword-of-rome-briefs_request.md` | `.ai/v3/requests/V3-20260529-040855-project-and-sword-of-rome-briefs_prompt.md` | `—` | `—` | `—` | External chat is asked to create two short Russian markdown briefs: one for the whole 2D wargame constructor project, one for Sword of Rome-like as the first test module. |
| V3-20260529-145329-turn-tracker-html-with-testing | 2026-05-29 | `imported` | Первый живой V3 request после внедрения post-import testing layer: standalone HTML tracker хода/раунда с обязательным `POST_IMPORT_TEST_PROMPT.md` | `.ai/v3/requests/V3-20260529-145329-turn-tracker-html-with-testing_request.md` | `.ai/v3/requests/V3-20260529-145329-turn-tracker-html-with-testing_prompt.md` | `local-only zip path: C:/Users/andre/Downloads/V3-20260529-145329-turn-tracker-html-with-testing.zip` | `.ai/v3/journals/drafts/V3-20260529-145329-turn-tracker-html-with-testing_journal.yaml` | `table-sandbox/v3-pilots/turn_tracker_russian.html` | Standalone Russian turn tracker HTML imported. Inline CSS/JS, no external deps. Post-import testing prompt included. SHA256 verified. Journal draft created. Codex review and human acceptance still pending. |
| V3-20260529-160218-victory-points-tracker-html-with-testing | 2026-05-29 | `imported` | Узкий standalone product-code test: русский HTML-трекер очков победы двух сторон с обязательным 4-секционным `POST_IMPORT_TEST_PROMPT.md` | `.ai/v3/requests/V3-20260529-160218-victory-points-tracker-html-with-testing_request.md` | `.ai/v3/requests/V3-20260529-160218-victory-points-tracker-html-with-testing_prompt.md` | `local-only zip path: C:/Users/andre/Downloads/V3-20260529-160218-victory-points-tracker-html-with-testing.zip` | `.ai/v3/journals/drafts/V3-20260529-160218-victory-points-tracker-html-with-testing_journal.yaml` | `table-sandbox/v3-pilots/victory_points_tracker_russian.html` | Standalone Russian victory-points tracker HTML imported. Inline CSS/JS, no external deps. Post-import testing required. SHA256 verified after binary copy. Journal draft created. Codex review and human acceptance still pending. |
| V3-20260529-234145-battle-status-dashboard-html-with-testing | 2026-05-29 | `imported` | Новый живой V3 end-to-end test: standalone русский dashboard статуса партии с раундом, фазой, инициативой и двумя группами счётчиков | `.ai/v3/requests/V3-20260529-234145-battle-status-dashboard-html-with-testing_request.md` | `.ai/v3/requests/V3-20260529-234145-battle-status-dashboard-html-with-testing_prompt.md` | `local-only zip path: C:/Users/andre/Downloads/V3-20260529-234145-battle-status-dashboard-html-with-testing.zip` | `.ai/v3/journals/drafts/V3-20260529-234145-battle-status-dashboard-html-with-testing_journal.yaml` | `table-sandbox/v3-pilots/battle_status_dashboard_russian.html` | Standalone Russian battle-status dashboard HTML imported. Inline CSS/JS, no external deps. Post-import testing required. SHA256 verified. Journal draft created. Codex review and human acceptance still pending. |
| V3-20260530-055044-hierarchical-subproject-workflow-master-plan | 2026-05-30 | `imported` | Master rollout plan for hierarchical subproject / Boss / B1 workflow system | `—` | `—` | `local-only zip path: C:/Users/andre/Downloads/V3-20260530-055044-hierarchical-subproject-workflow-master-plan.zip` | `.ai/v3/journals/drafts/V3-20260530-055044-hierarchical-subproject-workflow-master-plan_journal.yaml` | `.ai/plans/master/hierarchical_subproject_workflow_rollout_plan.md` | External chat generated master rollout plan for hierarchical subproject/Boss/B1 workflow. scope: workflow_docs. One planning file created. Post-import testing waived. SHA256 verified. Journal draft created. Codex review and human acceptance still pending. |
| V3-20260530-130503-hierarchical-subproject-working-plan | 2026-05-30 | `request_prepared` | Короткий operational work plan по внедрению hierarchical subproject / Boss / B1 workflow на основе большого master plan и idea doc | `.ai/v3/requests/V3-20260530-130503-hierarchical-subproject-working-plan_request.md` | `.ai/v3/requests/V3-20260530-130503-hierarchical-subproject-working-plan_prompt.md` | `—` | `—` | `—` | External chat is asked to create one concise workflow_docs file: a direct working plan for rollout. First major step must be creation of the subproject entity. Detailed block breakdown is intentionally out of scope for now. |

## Структура `.ai/v3/`

| Файл/папка | Назначение | Статус |
|---|---|---|
| [`README.md`](README.md) | Главный вход в V3 | Phase 1+, process model updated |
| [`V3_navigation.md`](V3_navigation.md) | Этот lifecycle index | Phase 1+, lifecycle archive model updated |
| [`contracts/`](contracts/README.md) | Формальные контракты V3 | Phase 2 |
| [`templates/`](templates/README.md) | Шаблоны V3 | Phase 3 |
| [`prompts/`](prompts/README.md) | Prompt layer V3 | Phase 3 |
| [`docs/`](docs/README.md) | Setup/process docs | Phase 4+ |
| [`requests/`](requests/) | V3 request/prompt artifacts | local/staged workflow layer |

## Prompt and Template Layer

### Промпты

| Файл | Назначение |
|---|---|
| [`prompts/create_v3_request_prompt.md`](prompts/create_v3_request_prompt.md) | Как готовить V3 external request |
| [`prompts/kilo_notebook_v3_mode_prompt.md`](prompts/kilo_notebook_v3_mode_prompt.md) | Raw-input operating reference для `Kilo Notebook V3` |
| [`prompts/codex_v3_review_prompt.md`](prompts/codex_v3_review_prompt.md) | Как Codex проверяет imported result |
| [`prompts/v3_revision_request_prompt.md`](prompts/v3_revision_request_prompt.md) | Как запросить revision |

### Шаблоны

| Файл | Назначение |
|---|---|
| [`templates/v3_request_template.md`](templates/v3_request_template.md) | Шаблон V3 request |
| [`templates/v3_manifest_template.yaml`](templates/v3_manifest_template.yaml) | Шаблон manifest |
| [`templates/v3_journal_template.yaml`](templates/v3_journal_template.yaml) | Шаблон journal |
| [`templates/v3_codex_review_template.md`](templates/v3_codex_review_template.md) | Шаблон Codex review |
| [`templates/v3_revision_request_template.md`](templates/v3_revision_request_template.md) | Шаблон revision request |

## Связанные документы вне `.ai/v3/`

| Документ | Назначение |
|---|---|
| [`../plans/master/v3_workflow_implementation_plan.md`](../plans/master/v3_workflow_implementation_plan.md) | Поэтапный план внедрения V3 |
| [`docs/manual_kilo_notebook_v3_setup.md`](docs/manual_kilo_notebook_v3_setup.md) | Ручная настройка режима |
| [`contracts/v3_request_contract.md`](contracts/v3_request_contract.md) | V3 request contract |
| [`contracts/v3_storage_policy.md`](contracts/v3_storage_policy.md) | Storage/input policy |
| [`contracts/v3_acceptance_policy.md`](contracts/v3_acceptance_policy.md) | Acceptance и import rules |
| [`../../../AGENTS.md`](../../../AGENTS.md) | Repo-level workflow contract |

## Примечания к записям

- `V3_navigation.md` должен обновляться как живой lifecycle index, а не только после финального accept.
- `Created Files` — это именно итоговые project files, которые появились после import-run.
- Если внешний чат вернул только архив, но импорта ещё не было, `Created Files` остаётся пустым (`—`).
- Краткая суть ответа внешнего чата должна попадать в `Summary`.
- journal не должен дублировать lifecycle-строку, а `V3_navigation.md` не должен копировать технические подробности journal.
