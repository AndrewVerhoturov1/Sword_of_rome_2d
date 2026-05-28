# V3 Documentation

Эта папка содержит документацию V3 artifact-producing workflow.

## Текущий статус

**Phase 4 (2026-05-27):** создан setup guide [`manual_kilo_notebook_v3_setup.md`](manual_kilo_notebook_v3_setup.md).

**Phase 5 process split:** docs теперь различают:

- pre-Kilo external artifact generation;
- pre-Kilo package review;
- Kilo UI setup;
- raw-input import pilot.

## Содержимое

| Файл | Назначение | Статус |
|---|---|---|
| [`manual_kilo_notebook_v3_setup.md`](manual_kilo_notebook_v3_setup.md) | Ручная настройка режима `Kilo Notebook V3` и правила перед первым import-run | Phase 4+, обновлён под raw-input flow |

## Что важно

- setup guide не доказывает, что режим уже настроен в живом UI;
- внешний ZIP package можно тестировать до Kilo import;
- `.ai/v3/staging/` не является обязательным human-step до import-stage;
- `Kilo Notebook V3` работает как raw-input mode;
- `V3_navigation.md` ведётся как lifecycle/archive index, как в `V1` и `V2`.

## Сейчас доступно

- [`../README.md`](../README.md) - общее описание V3 и current status.
- [`../V3_navigation.md`](../V3_navigation.md) - навигация и lifecycle archive.
- [`../contracts/v3_storage_policy.md`](../contracts/v3_storage_policy.md) - storage/input policy.
- [`../contracts/v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md) - acceptance и import rules.
- [`../../plans/master/v3_workflow_implementation_plan.md`](../../plans/master/v3_workflow_implementation_plan.md) - master plan.
