# Repo Navigation — sword-of-rome-web

Справочник по публичному и project-specific контексту этого repo. Нужен людям, Codex и внешним чатам, когда им передают этот файл как project-specific navigation.

## Что здесь главное

- Это repo про browser-based editor / authoring tool для 2D counter-based варгеймов.
- Sword of Rome-like материалы здесь = первый тестовый модуль и reference layer.
- История `/v1` считается частью публичного контекста проекта.
- Репозиторий опубликован на GitHub: [`AndrewVerhoturov1/Sword_of_rome_2d`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d). Гайд по публикации — [`docs/workflow/first_git_publication_guide.md`](../docs/workflow/first_git_publication_guide.md).

## External Start Here

- Начни с [`README.md`](../README.md), потом читай [`AGENTS.md`](../AGENTS.md), затем [`canon/context/sword_of_rome_web_project_context.md`](../canon/context/sword_of_rome_web_project_context.md).
- Для текущей зрелости repo отдельно проверь [`project_state.md`](project_state.md) до чтения архитектурных деталей.
- Не путай planned architecture с уже реализованным product code: архитектурные документы описывают целевой editor/runtime, а не готовое приложение.
- Local-only пути `arena-prototype-launcher/`, `_local/`, `output/Arena tests/` и runtime-подпапки `.ai/` не считаются публичным каноном.

## Reading Order Для Внешнего Чата

Если ты внешний чат и читаешь этот файл как project-specific navigation:

1. [`README.md`](../README.md) — общее описание, структура, public/local-only разделение.
2. [`AGENTS.md`](../AGENTS.md) — workflow contract этого repo.
3. [`canon/context/sword_of_rome_web_project_context.md`](../canon/context/sword_of_rome_web_project_context.md) — главный проектовый контекст.
4. [`project_brief.md`](project_brief.md) — краткая формулировка цели.
5. [`project_state.md`](project_state.md) — текущий статус repo.
6. [`architecture.md`](architecture.md) — зафиксированный architectural focus.
7. [`decisions.md`](decisions.md) — принятые решения.

## Публичные Слои

### Стартовые Точки

- [`README.md`](../README.md) — краткое описание проекта и разделение public/local-only слоёв.
- [`AGENTS.md`](../AGENTS.md) — workflow contract этого repo.
- [`project_brief.md`](project_brief.md) — краткая формулировка цели.
- [`project_state.md`](project_state.md) — текущий статус repo.
- [`architecture.md`](architecture.md) — architectural focus.
- [`decisions.md`](decisions.md) — принятые решения.

### Canon

- [`canon/context/sword_of_rome_web_project_context.md`](../canon/context/sword_of_rome_web_project_context.md) — главный проектовый контекст и framing проекта.
- [`canon/README.md`](../canon/README.md) — как использовать папку `canon/`.

### References

- [`references/rules/sword_of_rome_rules_2010_v2_ai.md`](../references/rules/sword_of_rome_rules_2010_v2_ai.md) — правила и reference-материал по Sword of Rome.
- [`references/maps/sword_of_rome_map.jpg`](../references/maps/sword_of_rome_map.jpg) — карта-референс.
- [`references/ui/UI_REFERENCE_App.tsx`](../references/ui/UI_REFERENCE_App.tsx) — UI reference prototype.
- [`references/README.md`](../references/README.md) — назначение reference-слоя.

### Docs

- [`docs/workflow/first_git_publication_guide.md`](../docs/workflow/first_git_publication_guide.md) — гид по `git init` и первой GitHub-публикации.
- [`docs/workflow/prototyping_workflow.md`](../docs/workflow/prototyping_workflow.md) — как в проекте используются внешние прототипы, Arena.ai и локальная арена.
- [`docs/README.md`](../docs/README.md) — назначение docs-слоя.

### Scripts

- [`scripts/stage_v1_notebook.py`](../scripts/stage_v1_notebook.py) — создание staged notebook entry из raw external response.
- [`scripts/write_v1_notebook.py`](../scripts/write_v1_notebook.py) — writer-step для внутреннего notebook package.
- [`scripts/bootstrap_workflow.py`](../scripts/bootstrap_workflow.py) — bootstrap workflow из central core.
- [`scripts/sync_kilo_workflow.py`](../scripts/sync_kilo_workflow.py) — синхронизация workflow-файлов.
- [`scripts/safe_sync_workflow.py`](../scripts/safe_sync_workflow.py) — безопасная синхронизация с валидацией.
- [`scripts/validate_kilo_contract.py`](../scripts/validate_kilo_contract.py) — валидация Kilo handoff контракта.
- [`scripts/validate_session_contract.py`](../scripts/validate_session_contract.py) — валидация session контракта.
- [`scripts/validate_external_chat_package.py`](../scripts/validate_external_chat_package.py) — валидация external chat package.
- [`scripts/external_chat_publish.py`](../scripts/external_chat_publish.py) — публикация artifacts для External Web Chat.

### Table Sandbox (First Product Code)

- [`table-sandbox/`](../table-sandbox/) — первый product-code блок: Phaser-based renderer, runtime action/event pipeline, game state, React debug panel.
- [`table-sandbox/src/renderer/phaserScene.ts`](../table-sandbox/src/renderer/phaserScene.ts) — Phaser render scene.
- [`table-sandbox/src/renderer/PhaserStage.tsx`](../table-sandbox/src/renderer/PhaserStage.tsx) — React-Phaser bridge component.
- [`table-sandbox/src/runtime/actionEvent.ts`](../table-sandbox/src/runtime/actionEvent.ts) — Action/Event pipeline: input → validation → resolution → commit → state mutation → log.
- [`table-sandbox/src/runtime/GameState.ts`](../table-sandbox/src/runtime/GameState.ts) — Game state model.
- [`table-sandbox/src/debug/DebugPanel.tsx`](../table-sandbox/src/debug/DebugPanel.tsx) — Debug panel component.
- [`table-sandbox/src/App.tsx`](../table-sandbox/src/App.tsx) — Main app component.
- [`table-sandbox/package.json`](../table-sandbox/package.json) — Dependencies and scripts.
- [`table-sandbox/vite.config.ts`](../table-sandbox/vite.config.ts) — Vite build config.

### Ideas

- [`ideas/README.md`](../ideas/README.md) — место для непринятых идей.

## Workflow-Слой `.ai/`

- `.ai/` содержит workflow-правила, конфигурацию, промпты и навигацию для `Codex + Kilo Code`.

### Ключевые Файлы

- [`logs/bug_journal.md`](logs/bug_journal.md) — shared project journal of important/repeated bugs and fixes.
- [`policies/bug_tracking_policy.md`](policies/bug_tracking_policy.md) — project policy for required bug/difficulty reporting and bug journal usage.
- [`policies/human_review_policy.md`](policies/human_review_policy.md) — project policy for mandatory/suggested human review, plain Russian user checks, and `pending human check` status.
- [`policies/language_policy.md`](policies/language_policy.md) — project language policy: English technical identifiers, Russian user-facing UI/docs.
- [`rules/agent_protocol.md`](rules/agent_protocol.md) — агентный протокол.
- [`rules/codex_orchestrator.md`](rules/codex_orchestrator.md) — правила Codex-оркестратора.
- [`rules/model_roster.md`](rules/model_roster.md) — политика выбора моделей.
- [`rules/kilo_mode_contract.md`](rules/kilo_mode_contract.md) — контракты Kilo mode-ов.
- [`rules/kilo_builder.md`](rules/kilo_builder.md) — правила Kilo Builder.
- [`rules/kilo_docs.md`](rules/kilo_docs.md) — правила Kilo Docs.
- [`rules/kilo_debugger.md`](rules/kilo_debugger.md) — правила Kilo Debugger.
- [`rules/kilo_tester.md`](rules/kilo_tester.md) — правила Kilo Tester.
- [`rules/kilo_refactor.md`](rules/kilo_refactor.md) — правила Kilo Refactor.
- [`prompts/`](prompts/) — промпты для создания handoff, external request, block orchestration.
- [`templates/`](templates/) — шаблоны для block plan, report, orchestration package.
- [`validators/`](validators/) — валидаторы workflow-артефактов.
- [`external_chats/external_chat_rules.md`](external_chats/external_chat_rules.md) — правила для External Web Chat.
- [`external_chats/external_agent_static_manual.md`](external_chats/external_agent_static_manual.md) — статический мануал для внешних агентов.
- [`external_chats/chatgpt_project_source_repo_onboarding.md`](external_chats/chatgpt_project_source_repo_onboarding.md) — onboarding-конспект для внешнего агента в ChatGPT Projects.
- [`external_chats/publisher_config.json`](external_chats/publisher_config.json) — конфигурация publisher для External Web Chat.
- [`bootstrap/portable/`](bootstrap/portable/) — portable bootstrap package для переноса workflow в новый проект.

### Master Plans

- [`plans/master/post_0_1_platform_roadmap.md`](plans/master/post_0_1_platform_roadmap.md) вЂ” macro-roadmap РїРѕСЃР»Рµ `Table Sandbox 0.1`: `0.2` hardening, `0.3` authoring expansion, `0.4` assisted runtime, `0.5` generic cards/documents, `1.0` modular platform alpha.
- [`plans/master/module_package_model.md`](plans/master/module_package_model.md) вЂ” mature module package model: required vs optional package parts, evolution from compact `0.1` layout, anti-bloat rules, packaging zones.

- [`plans/master/domain_schemas_contract.md`](plans/master/domain_schemas_contract.md) — master-plan по domain/data contract: canonical entities, file set, invariants, open questions.
- [`plans/master/minimal_canonical_file_schemas.md`](plans/master/minimal_canonical_file_schemas.md) — master-plan по minimal canonical file schemas: compact entity definitions, validation, invariants.
- [`plans/master/rules_hooks_interface.md`](plans/master/rules_hooks_interface.md) — master-plan по boundary между universal runtime и module-specific rules hooks.
- [`plans/master/action_event_contract.md`](plans/master/action_event_contract.md) — master-plan по action/event backbone: input → validation → resolution → commit → state mutation → log, с разделением Action (запрос) и Event (подтверждённый факт).
- [`plans/master/table_sandbox_0_1_milestone_plan.md`](plans/master/table_sandbox_0_1_milestone_plan.md) — operational milestone plan для первого universal tabletop sandbox.
- [`plans/master/first_vertical_slice_spec.md`](plans/master/first_vertical_slice_spec.md) — spec одного end-to-end proof slice: движение фишки через полный canonical pipeline.
- [`plans/master/first_milestone_runtime_skeleton.md`](plans/master/first_milestone_runtime_skeleton.md) — next-step working skeleton для Table Sandbox 0.1.
- [`plans/master/module_authoring_workflow.md`](plans/master/module_authoring_workflow.md) — authoring workflow: workspace shell + editor surfaces + play sandbox preview.
- [`plans/master/v3_artifact_producing_workflow_contract.md`](plans/master/v3_artifact_producing_workflow_contract.md) — draft V3 artifact-producing workflow contract: внешний чат создаёт artifact package, Kilo Notebook V3 импортирует его безопасно, Codex проверяет, человек принимает.

### Навигация

- [`repo_navigation.md`](repo_navigation.md) — этот файл.
- [`project_brief.md`](project_brief.md) — краткая формулировка цели.
- [`project_state.md`](project_state.md) — текущий статус.
- [`architecture.md`](architecture.md) — architectural focus.
- [`decisions.md`](decisions.md) — принятые решения.

## V1 History

- [`external_chats/V1_navigation.md`](external_chats/V1_navigation.md) — индекс прошлых `/v1` ответов.
- [`external_chats/notebook/`](external_chats/notebook/) — notebook entry files.
- [`external_chats/notebook/README.md`](external_chats/notebook/README.md) — что лежит в notebook entry history.

## V2 External Senior Review

- [`external_reviews/README.md`](external_reviews/README.md) — протокол V2 External Senior Review.
- [`external_reviews/V2_navigation.md`](external_reviews/V2_navigation.md) — индекс V2 requests.
- [`external_reviews/templates/`](external_reviews/templates/) — шаблоны V2 (request, prompt, response, ingest summary, safety checklist).

## V3 Artifact Workflow

- [`plans/master/v3_artifact_producing_workflow_contract.md`](plans/master/v3_artifact_producing_workflow_contract.md) — проектный контракт V3: внешний чат генерирует artifact package, Kilo Notebook V3 импортирует только разрешённые файлы, Codex делает review, человек даёт финальное принятие.

## Public vs Local-only

### Public (canon, references, docs, scripts, ideas, .ai core)

Всё, что перечислено выше. Эти файлы попадают в GitHub после публикации.

### Local-only, не source of truth для внешнего чата

- `arena-prototype-launcher/` — локальный launcher прототипов с собственной БД.
- `_local/` — локальные архивы и agent/workflow материалы.
- `output/Arena tests/` — локальный архив тестовых prototype-папок.
- `.ai/handoffs/`, `.ai/reports/`, `.ai/plans/sessions/`, `.ai/reviews/`, `.ai/model_tests/` — runtime Kilo-артефакты.
- `.ai/external_chats/requests/`, `responses/`, `tasks/`, `recorder_packages/`, `notebook_sources/`, `notebook_packages/` — runtime внешних чатов.

Эти пути не надо считать публичным каноном проекта, пока человек отдельно не скажет обратное.
## Recent Additions

- [`plans/implementation/first_product_code_block.md`](plans/implementation/first_product_code_block.md) — the concrete implementation brief that freezes the first coding block before technical bootstrap begins.

- [`plans/master/pre_code_closure_and_first_execution_plan.md`](plans/master/pre_code_closure_and_first_execution_plan.md) вЂ” the short bridge from accepted planning canon to the first narrow product-code slice.

- [`plans/master/module_product_ux_model.md`](plans/master/module_product_ux_model.md) — product-wide UX model: authoring, playtest, runtime/save flows, daily loop, mode transitions, and anti-confusion rules.
- [`plans/master/prototype_integration_mapping.md`](plans/master/prototype_integration_mapping.md) — how to use the external `table-map-editor-canvas-local-fixed` prototype as a reference donor without turning it into the product foundation.
