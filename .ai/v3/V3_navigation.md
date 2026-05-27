# V3 Navigation — sword-of-rome-web

Навигация по V3 artifact-producing workflow слою этого репозитория. Нужна людям, Codex и будущим оркестраторам для быстрого входа в V3.

## Текущий статус

**Phase 4 (Runtime Mode Integration) завершён (2026-05-27):** создан setup guide [`docs/manual_kilo_notebook_v3_setup.md`](docs/manual_kilo_notebook_v3_setup.md). Bootstrap portable docs синхронизированы. Global rules больше не отстают от факта существования `.ai/v3/` слоя. Manual runtime readiness достигнута.

Full operational V3 workflow — в следующих фазах rollout. Сейчас:

- `/v3` shortcut не активирован;
- `scripts/v3/*` не созданы (Phase 7);
- первый pilot — Phase 5.

## Структура `.ai/v3/`

| Файл/папка | Назначение | Статус |
|------------|------------|--------|
| [`README.md`](README.md) | Главный вход в V3 | ✅ Phase 1, обновлён Phase 3 |
| [`V3_navigation.md`](V3_navigation.md) | Этот файл — навигация | ✅ Phase 1, обновлён Phase 3 |
| [`contracts/`](contracts/README.md) | 9 формальных контрактов V3 | ✅ Phase 2 |
| [`templates/`](templates/README.md) | 5 шаблонов V3 | ✅ Phase 3 |
| [`prompts/`](prompts/README.md) | 4 промпта V3 | ✅ Phase 3 |
| [`docs/`](docs/README.md) | Документация V3 | Setup guide создан (Phase 4), остальное — Phase 3+ |

## Prompt and Template Layer (Phase 3)

### Промпты (`.ai/v3/prompts/`)

| Файл | Назначение |
|------|------------|
| [`create_v3_request_prompt.md`](prompts/create_v3_request_prompt.md) | Как Codex/человеку подготовить V3-запрос к внешнему чату |
| [`kilo_notebook_v3_mode_prompt.md`](prompts/kilo_notebook_v3_mode_prompt.md) | Mode prompt для Kilo Notebook V3: безопасный import flow |
| [`codex_v3_review_prompt.md`](prompts/codex_v3_review_prompt.md) | Как Codex проверяет результат V3 import |
| [`v3_revision_request_prompt.md`](prompts/v3_revision_request_prompt.md) | Как запросить доработку у внешнего чата |

### Шаблоны (`.ai/v3/templates/`)

| Файл | Назначение |
|------|------------|
| [`v3_request_template.md`](templates/v3_request_template.md) | Шаблон V3 request с placeholder-полями |
| [`v3_manifest_template.yaml`](templates/v3_manifest_template.yaml) | YAML-скелет manifest.yaml |
| [`v3_journal_template.yaml`](templates/v3_journal_template.yaml) | YAML-скелет journal entry |
| [`v3_codex_review_template.md`](templates/v3_codex_review_template.md) | Шаблон review note для Codex |
| [`v3_revision_request_template.md`](templates/v3_revision_request_template.md) | Шаблон revision request |

## Связанные документы вне `.ai/v3/`

| Документ | Назначение |
|----------|------------|
| [`../plans/master/v3_artifact_producing_workflow_contract.md`](../plans/master/v3_artifact_producing_workflow_contract.md) | Проектный контракт V3 (draft 0.1) |
| [`../plans/master/v3_workflow_implementation_plan.md`](../plans/master/v3_workflow_implementation_plan.md) | Поэтапный план внедрения V3 |
| [`../rules/agent_protocol.md`](../rules/agent_protocol.md) | Агентный протокол (секция `kilo-notebook-v3`) |
| [`../rules/kilo_mode_contract.md`](../rules/kilo_mode_contract.md) | Контракт Kilo mode (секция `kilo-notebook-v3`) |
| [`../repo_navigation.md`](../repo_navigation.md) | Общая навигация репозитория (секция V3) |
| [`../../../AGENTS.md`](../../../AGENTS.md) | Workflow contract репозитория |

## Ожидаемые future additions (после Phase 4)

- `docs/` — safety rules, storage policy, pilot notes (Phase 4+);
- `journals/` — journal entries после первого pilot (Phase 5+).

`contracts/` — созданы в Phase 2, не ожидают изменений до hardening после pilot.
`templates/` и `prompts/` — созданы в Phase 3, могут уточняться после V1 critique (Phase 6).
