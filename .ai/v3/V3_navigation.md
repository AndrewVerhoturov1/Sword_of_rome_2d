# V3 Navigation — sword-of-rome-web

Навигация по V3 artifact-producing workflow слою этого репозитория. Нужна людям, Codex и будущим оркестраторам для быстрого входа в V3.

## Текущий статус

**Phase 1 (Docs Foundation):** `.ai/v3/` создан как discoverable foundation layer. `kilo-notebook-v3` canonically разрешён в Phase 0.

Full operational V3 workflow — в следующих фазах rollout. Сейчас active:

- `/v3` shortcut не активирован;
- `scripts/v3/*` не созданы;
- operational contracts — в Phase 2.

## Структура `.ai/v3/`

| Файл/папка | Назначение | Статус |
|------------|------------|--------|
| [`README.md`](README.md) | Главный вход в V3 | Создан (Phase 1) |
| [`V3_navigation.md`](V3_navigation.md) | Этот файл — навигация | Создан (Phase 1) |
| [`contracts/`](contracts/README.md) | Формальные контракты V3 | Placeholder (Phase 1), наполнение — Phase 2 |
| [`templates/`](templates/README.md) | Шаблоны V3 | Placeholder (Phase 1), наполнение — Phase 3 |
| [`prompts/`](prompts/README.md) | Промпты V3 | Placeholder (Phase 1), наполнение — Phase 3 |
| [`docs/`](docs/README.md) | Документация V3 | Placeholder (Phase 1), наполнение — Phase 3+ |

## Связанные документы вне `.ai/v3/`

| Документ | Назначение |
|----------|------------|
| [`../plans/master/v3_artifact_producing_workflow_contract.md`](../plans/master/v3_artifact_producing_workflow_contract.md) | Проектный контракт V3 (draft 0.1) |
| [`../plans/master/v3_workflow_implementation_plan.md`](../plans/master/v3_workflow_implementation_plan.md) | Поэтапный план внедрения V3 |
| [`../rules/agent_protocol.md`](../rules/agent_protocol.md) | Агентный протокол (секция `kilo-notebook-v3`) |
| [`../rules/kilo_mode_contract.md`](../rules/kilo_mode_contract.md) | Контракт Kilo mode (секция `kilo-notebook-v3`) |
| [`../repo_navigation.md`](../repo_navigation.md) | Общая навигация репозитория (секция V3) |
| [`../../../AGENTS.md`](../../../AGENTS.md) | Workflow contract репозитория |

## Ожидаемые future additions

После следующих фаз здесь появятся:

- `contracts/` — request, artifact package, manifest, journal, review, revision, storage, scope, acceptance contracts;
- `templates/` — V3 request template, manifest.yaml template, journal template, Codex review template, revision request template;
- `prompts/` — create_v3_request_prompt, kilo_notebook_v3_mode_prompt, codex_v3_review_prompt, v3_revision_request_prompt;
- `docs/` — setup guide, safety rules, storage policy, pilot notes.

Ни один из этих файлов ещё не создан. Не считай их существующими, пока они не появятся в следующих фазах.
