# Session: architecture_orchestration_v1_planning

## Latest Accepted Synthesis

- Accepted UX-model synthesis from the latest `/v1` answer:
  - one product shell with explicit modes;
  - clear split between `authoring`, `playtest preview`, and `runtime/save`
    workflows;
  - minimal `0.1` UX loop = edit -> validate -> preview -> inspect -> save
    snapshot -> return;
  - dedicated master doc `.ai/plans/master/module_product_ux_model.md`;
  - synced authoring workflow, package model, roadmap, and `0.1` milestone
    plan around this UX language.

- Accepted prototype-integration synthesis from `V1-20260523-161245`:
  - external prototype is a reference prototype and selective donor;
  - main use is for future Map Editor surface;
  - controlled extraction is preferred;
  - dedicated master doc `.ai/plans/master/prototype_integration_mapping.md`.
- Accepted execution-plan synthesis from `V1-20260524-003946`:
  - broad product-code start stays blocked;
  - next step is short pre-code closure;
  - first implementation starts through a narrow `Table Sandbox 0.1` slice;
  - dedicated master doc
    `.ai/plans/master/pre_code_closure_and_first_execution_plan.md`.
- Accepted single-next-step synthesis from `V1-20260524-005734`:
  - first priority step is to create and accept
    `.ai/plans/implementation/first_product_code_block.md`;
  - that file freezes shell, fixtures, first action/event, acceptance checklist,
    prototype role, and non-goals;
  - immediate next step after acceptance is technical bootstrap.
- Accepted fixture-step decomposition from `V1-20260524-184203`:
  - next narrow implementation step after accepted bootstrap is
    `Canonical Fixture Seed`;
  - scope stays data-only under `table-sandbox/src/fixtures/tiny-module/`;
  - target file set = `project.json`, `module.json`, `map.json`,
    `scenario.basic.json`, `rules.metadata.json`, `savegame.empty.json`,
    `README.md`;
  - loader/runtime/Phaser/prototype migration stay out of this handoff.

## Session ID

`2026-05-23_architecture_orchestration_v1_planning`

## Status

in_progress

## Goal

Собрать и уточнить архитектурный план для browser-based 2D authoring tool / editor, определить основные модули проекта, разделить universal editor layer и project-specific layer, и подготовить последовательность следующих шагов с максимальным использованием `/v1` для внешнего архитектурного осмысления.

## Approved Plan

### P1: Frame Architecture Scope

- Status: completed.
- Зафиксировать рабочую framing-модель проекта как universal authoring tool, а не одну конкретную игру.
- Проверить и уточнить границу между editor/runtime capabilities и Sword of Rome-like test module.
- Сформулировать кандидатный модульный состав верхнего уровня без перехода к product-code реализации.

### P2: Prepare External V1 Research Tracks

- Status: completed.
- Сформулировать несколько разных `/v1` вопросов для внешнего чата.
- Развести вопросы по типам: архитектурная декомпозиция, domain model / data model, roadmap / delivery sequence.
- Выбрать первый `/v1` маршрут только после явного решения человека.

### P3: Consolidate Architecture And Next Steps

- Status: in_progress.
- После возврата ответов `/v1` сверить их с локальным canon.
- Синтезировать рабочую архитектурную схему проекта и список ближайших шагов.
- При необходимости подготовить следующий planning-only артефакт или downstream handoff в рамках session.

## Active Plan Item

`P3: Consolidate Architecture And Next Steps`

## Runs

- `Session run: 001` - handoff `0008_first_product_code_technical_bootstrap.md` executed, corrected, reviewed by Codex and accepted.
- `Session run: 002` - handoff `0009_canonical_fixture_seed.md` prepared for next Kilo execution.
- `Session run: 003` - `0009` reviewed by Codex; rejected for correction because `module.json` is corrupted and report claims do not match actual files.
- `Session run: 004` - corrected `0009` reviewed by Codex and accepted; fixture seed is now internally consistent and scope-clean.
- `Session run: 005` - handoff `0010_runtime_data_bootstrap.md` prepared for next Kilo execution.
- `Session run: 006` - handoff `0011_action_event_spine_first_move.md` prepared for the first narrow move slice through canonical Action/Event flow.
- `Session run: 007` - `0011` reviewed by Codex: build/typecheck passed, scope looks clean, product verdict = pending human check because this is a visible browser/runtime slice.
- `Session run: 008` - user confirmed real browser behavior for `0011`; Codex accepts the first narrow Action/Event move slice and prepares workflow checkpoint.
- `Session run: 009` - handoff `0012_permissive_rules_hooks_shim.md` prepared for the next narrow boundary step: runtime asks, rules answer, runtime commits.
- `Session run: 010` - `0012` reviewed by Codex: code and checks look clean, verdict = pending human check because the browser move loop must still be confirmed after the boundary extraction.
- `Session run: 011` - user confirmed real browser behavior for `0012`; Codex accepts the permissive RulesHooks shim as the next runtime baseline.
- `Session run: 012` - handoff `0013_graph_aware_move_validation.md` prepared for the next narrow hardening step: graph-aware validation for `move_piece_requested`.
- `Session run: 013` - tiny graph-aware validation fix applied directly by Codex at explicit user request; build and typecheck passed locally.
- `Session run: 014` - `/v1` answer `V1-20260524-233900` processed through local notebook pipeline; accepted local takeaway = next narrow step should be minimal local save/load snapshot for runtime state.
- `Session run: 015` - handoff `0014_minimal_runtime_snapshot_save_load.md` prepared for the next narrow persistence step: localStorage snapshot for `GameState + eventLog`.
- `Session run: 016` - `0014` reviewed by Codex; code path for save/load confirmed in repo, initial live confusion traced to wrong URL/port, final human confirmation received: save/load works.
- `Session run: 017` - `/v1` answer `V1-20260525-005823` processed through local notebook pipeline; direction accepted = move from single-action demo toward a manual sandbox action set, but user explicitly wants the full `Manual Sandbox Action Pack 1` handoff rather than a narrower `change_control` slice.
- `Session run: 018` - handoff `0015_manual_sandbox_action_pack_1.md` prepared for the next broader-but-bounded sandbox step: create piece, delete piece, change control, selected object panel, human-readable validation messages, and save/load verification for all added runtime changes.
- `Session run: 019` - `0015` reviewed by Codex; two save/load identity issues were corrected, user confirmed manual browser checks, and the full `Manual Sandbox Action Pack 1` is accepted as the next sandbox baseline.
- `Session run: 020` - `/v1` answer `V1-20260525-033837` processed through local notebook pipeline; user accepted the recommendation to pivot the next significant step toward `Manual Sandbox Interaction Pack 1 - Smart Drag Move`, with bounded 6-space fixture expansion inside the same handoff and prototype used only as UX donor/reference.
- `Session run: 021` - handoff `0016_manual_sandbox_interaction_pack_1_smart_drag_move.md` prepared for the next interaction-oriented step: 6-space tiny map expansion, left-button smart drag move, source tail, nearest-target highlight, snap/magnet, release through existing runtime pipeline, rollback on invalid drop, and save/load verification.
- `Session run: 022` - `0016` reviewed by Codex; one fixture/bootstrap consistency issue was corrected, build/typecheck passed, user confirmed live browser behavior, and the smart drag move pack is accepted as the next interaction baseline.
- `Session run: 023` - `/v1` answer `V1-20260525-042226` accepted by user; handoff `0017_play_sandbox_readiness_pack.md` prepared for the next bounded readiness step: stack/selection readiness, scenario reset, lightweight map/scenario sanity check, and save/load regression across all already-supported manual actions.
- `Session run: 024` - `0017` reviewed by Codex: build/typecheck passed, visual human check passed, stack/selection/reset/save-load behavior confirmed, and the `Play Sandbox Readiness Pack` is accepted as the next stable play-preview baseline.
- `Session run: 025` - `/v1` answer `V1-20260525-051950` accepted by user; handoff `0018_map_authoring_0_1_spaces_and_connections_slice.md` prepared for the first bounded editor branch step: `Map Authoring 0.1` with spaces/connections editing, object list, inspector, validation, preview integration, and aggressive prototype borrowing from `table-map-editor-canvas-local-fixed` without wholesale migration.
- `Session run: 026` - `0018` reviewed by Codex, two editor rendering/layout issues were fixed directly by Codex (`crop` and `zoom pixelation`), build/typecheck passed, human visual check passed, and `Map Authoring 0.1 - Spaces and Connections Slice` is accepted as the first editor baseline.
- `Session run: 027` - handoff `0019_repo_sync_audit.md` prepared as a read-only repo sync audit against `origin/main`: inventory, size/hash-first compare, targeted diff inspection, and suspicious untracked/ignored detection without any sync actions.
- `Session run: 028` - `0019` reviewed by Codex: read-only repo sync audit passed, local `HEAD` equals `origin/main`, important tracked files match by hash, no untracked product/docs drift found, and no sync action is required.

## User Overrides

- Этот чат про orchestration, architecture planning и planning next steps, а не про прямую реализацию product code.
- По возможности использовать `/v1` как основной внешний мозг для архитектурного осмысления.
- Пользователь уже видит два главных слоя:
  - universal editor layer: карта, области, колоды, фишки, базовые сущности и инструменты;
  - project-specific layer: конкретный модуль/проект, собираемый поверх editor capabilities.
- Не переходить к широким изменениям кода без отдельного согласования и без следующего planning шага.
- Пользователь отдельно попросил сохранить локальные planning-файлы и присылать только ссылки на них.
- После `/v1` по следующему шагу пользователь явно выбрал полный `Manual Sandbox Action Pack 1`, а не более узкий `change_control`-only slice.
- Пользователь отдельно запросил быстрый read-only repo sync audit handoff против `origin/main`; это side audit без product-code изменений, commit, push или auto-sync.
- После audit пользователь отдельно запросил зафиксировать `0019` и подготовить новый `/v1` prompt про gap-анализ editor branch и sequencing к уровню prototype.

## Checkpoint State

- `0008` result reviewed and accepted: narrow bootstrap shell exists in `table-sandbox/`, build and typecheck pass, live page opens.
- `0008` correction verified:
  - `tsconfig.tsbuildinfo` no longer appears after build/typecheck;
  - duplicate Phaser boot log under `StrictMode` no longer reproduces in live dev verification.
- User visual confirmation received:
  - green Phaser field is visible;
  - clicking now produces runtime/debug updates on screen.
- Workflow checkpoint for accepted `0008` completed by Codex commit `b566427` (`Workflow: accept Kilo task 0008`).
- `0009` not accepted yet:
  - initial attempt had corrupted `module.json` and false-positive report claims;
  - corrected attempt fixed `module.json` and restored full cross-file consistency.
- `0009` result now accepted:
  - `table-sandbox/src/fixtures/tiny-module/` contains the full requested 7-file tiny fixture set;
  - direct Codex re-check confirmed all required cross-file references resolve;
  - no runtime/Phaser/prototype scope creep detected.
- Workflow checkpoint for accepted `0009` completed by Codex commit `9a61926` (`Workflow: accept Kilo task 0009`).
- Current next practical step is fixed locally, without new `/v1`:
  - `Phase 3 - Runtime/Data Bootstrap`
  - load accepted tiny fixtures into minimal runtime-owned `GameState`
  - keep `move_piece_requested -> piece_moved` for the following handoff, not this one.
- `0010` is now treated as accepted local baseline:
  - runtime bootstrap comes from accepted fixtures, not placeholder state;
  - `GameState` already knows `tiny-project / tiny-module / tiny-map / basic`;
  - runtime knows 2 spaces, 1 connection, 1 piece instance and `phaseId = manual`;
  - next practical step is no longer data bootstrap, but the first narrow `Action/Event Spine`.
- Current next practical step is fixed locally, without new `/v1`:
  - first move slice through `move_piece_requested -> piece_moved`
  - authoritative `GameState` update outside Phaser
  - event log append and visible piece redraw from updated runtime state
- `0011` code review result:
  - narrow move pipeline is present in code;
  - build and typecheck pass locally after the change;
  - no obvious scope creep into save/load, broad rules layer or fixture edits;
  - human visual check is now completed by the user;
  - `0011` is accepted as the first narrow Action/Event move slice baseline.
- Current accepted baseline now includes:
  - `piece-1` can move from `space-a` to `space-b` through `move_piece_requested -> piece_moved`;
  - authoritative `GameState` still lives outside Phaser;
  - renderer redraw follows committed runtime state;
  - event log and debug evidence reflect the committed move.
- Current next practical step is fixed locally, without new `/v1`:
  - extract a minimal permissive `RulesHooks` shim;
  - move `validate` and `resolve` answers behind that boundary;
  - keep current move behavior unchanged.
- `0012` code review result:
  - permissive rules logic is extracted into a dedicated `rulesHooks.ts` shim;
  - runtime now asks rules for `validateAction` and `resolveAction`;
  - runtime still commits events and applies reducer itself;
  - build and typecheck pass locally;
  - human visual check is now completed by the user;
  - `0012` is accepted as the first explicit `runtime asks -> rules answer -> runtime commits` baseline.
- Current accepted baseline now also includes:
  - permissive `RulesHooks` lives in `table-sandbox/src/runtime/rulesHooks.ts`;
  - current move behavior is preserved for the user;
  - runtime/rules boundary is cleaner without expanding rules breadth yet.
- Current next practical step is fixed locally, without new `/v1`:
  - strengthen `RulesHooks.validateAction(...)` for `move_piece_requested`;
  - add first graph-aware checks against spaces and connections in `GameState`;
  - keep the current move behavior and runtime authority unchanged.
- Direct tiny fix baseline update:
  - `RulesHooks.validateAction(...)` now checks source/target spaces and bidirectional connection existence;
  - `move_piece_requested_location_mismatch` now blocks instead of warns;
  - current positive path `space-a -> space-b` remains valid.
- `/v1` follow-up guidance accepted locally:
  - `V1-20260524-233900` confirms `rulesHooks.ts` is present and connected in the current baseline;
  - recommended next narrow step = minimal `localStorage` save/load snapshot;
  - snapshot scope must stay runtime-only: `GameState + eventLog`;
  - no save slots, migrations, import/export, cloud save, or Phaser/UI state persistence in this step.
- `0014` is now accepted:
  - footer has minimal `Сохранить` / `Загрузить` controls;
  - runtime snapshot persists through `localStorage`;
  - both `GameState` and `eventLog` restore successfully;
  - renderer redraw follows restored runtime state;
  - `RulesHooks` remained untouched.
- Current accepted baseline now also includes:
  - one narrow runtime snapshot seam;
  - storage key `table-sandbox.snapshot.v1`;
  - safe no-crash behavior for missing/invalid snapshot;
  - runtime authority preserved through save/load.
- `/v1` follow-up guidance after accepted snapshot baseline:
  - `V1-20260525-005823` recommends moving from single-action demo to a manual sandbox action set;
  - suggested bundle includes create piece, delete piece, change control, selected object panel, human-readable validation messages, and save/load coverage for all new state changes.
- Current next practical step is now fixed by explicit user override:
  - prepare the full `Manual Sandbox Action Pack 1` handoff, not the narrower `change_control` slice;
  - still keep scope bounded: no broad editor, no prototype migration, no large save/rules redesign.
- `0015` is now accepted:
  - manual sandbox actions now cover create piece, delete piece, and change control;
  - runtime carries `controlState` and persists it through existing snapshot flow;
  - selected object panel and Russian validation messages are now part of the visible sandbox baseline;
  - compatibility fix exists for older snapshots without `controlState`;
  - `nextPieceSeq` restore now scans both live pieces and historical `piece_created` events to avoid reused ids after load.
- `/v1` follow-up guidance after accepted `0015` baseline:
  - `V1-20260525-033837` recommends `Manual Sandbox Interaction Pack 1 - Smart Drag Move`;
  - include tiny map expansion to about 6 spaces as bounded prep inside the same handoff;
  - keep prototype role strictly reference/donor only for drag feel;
  - keep runtime authority outside Phaser and reuse existing `move_piece_requested -> RulesHooks -> Event -> reducer -> GameState` path.
- `0016` is now accepted:
  - tiny fixture map is expanded to a small multi-space graph suitable for interaction checks;
  - left-button smart drag is now the primary move UX;
  - drag shows source tail/line, nearest-target highlight, and snap/magnet behavior;
  - release still goes through existing `move_piece_requested -> RulesHooks -> Event -> reducer -> GameState` pipeline;
  - invalid/no-target drop rolls back without mutating committed state and shows a short Russian message;
  - fixture-driven `controlBySpace` is now loaded into runtime bootstrap instead of being dead data;
  - save/load survives committed drag move.
- `/v1` follow-up guidance after accepted `0016` baseline:
  - `V1-20260525-042226` recommends one bounded `Play Sandbox Readiness Pack` before editor branching;
  - scope = stack/selection readiness, scenario reset, lightweight map/scenario sanity check, save/load regression;
  - after this pack, natural next branch becomes `Map Authoring 0.1`, not bigger rules/save/prototype work.
- Current next practical step is now fixed locally by accepted `/v1` guidance and explicit user approval:
  - prepare `0017_play_sandbox_readiness_pack.md`;
  - do not jump yet to broad editor breadth;
  - do not expand into full rules engine or mature save system.
- `0017` is now accepted:
  - stack/selection readiness is present in the visible sandbox baseline;
  - selected piece in a stack remains individually drag-able;
  - reset returns runtime to fixture-based initial scenario state without mutating fixture files;
  - bounded sanity-check messaging exists for key bootstrap/runtime reference problems;
  - save/load regression survives move, drag, create, delete, change control, and reset.
- Current baseline is now good enough to stop readiness-focused sandbox work and branch toward first bounded authoring/editor slices.
- `/v1` follow-up guidance after accepted `0017` baseline:
  - `V1-20260525-051950` says yes, it is time to branch into editor work;
  - recommended next significant step = `Map Authoring 0.1 - Spaces and Connections Slice`;
  - `table-map-editor-canvas-local-fixed` should be used aggressively as UX donor/reference;
  - but authoring `MapDefinition` and runtime `GameState` must stay explicitly separated.
- Current next practical step is now fixed locally by accepted `/v1` guidance and explicit user emphasis:
  - prepare `0018_map_authoring_0_1_spaces_and_connections_slice.md`;
  - prototype borrowing should be maximized where it fits first-slice scope;
  - do not fall back to generic fresh editor UX if prototype already covers the interaction.
- `0018` is now accepted:
  - editor mode and play mode now coexist in one product shell;
  - tiny map loads into a separate editable `MapDraft`;
  - spaces and connections can be created, moved, renamed, and deleted in authoring mode;
  - object list, inspector, context menu, validation, and preview loop now exist in the editor branch;
  - preview uses draft-derived runtime state without making editor draft or Phaser the runtime source of truth;
  - editor surface layout/rendering was hardened after Kilo run: no cropped lower canvas, no CSS-scale blur under zoom.
- `0019` is now accepted:
  - read-only repo sync audit against `origin/main` passed;
  - local `HEAD` and `origin/main` are aligned;
  - important tracked product/docs files matched by hash;
  - no untracked important files and no suspicious ignored drift were found;
  - only local session-planning noise remained outside product sync concerns.
- В repo уже принят framing: проект = browser-based 2D authoring tool / editor / tabletop sandbox, а Sword of Rome-like модуль = первый тестовый модуль.
- По `/v1` уже получены и staged два external second opinion:
  - `V1-20260523-052756`
  - `V1-20260523-052757`
- Оба external ответа сошлись на том, что 2-layer framing недостаточен и нужен `4-layer` product architecture.
- Локальный синтез этих ответов зафиксирован в `.ai/architecture.md`.
- Decision по `4-layer product architecture` и `RulesHooksInterface` boundary зафиксирован в `.ai/decisions.md`.
- В `.ai/decisions.md` уже принято решение `Authoring tool first`.
- В `.ai/project_state.md` указано, что product-code architecture ещё не разложена на реальные модули; repo пока mostly про public context и workflow layer.
- В `.ai/external_chats/V1_navigation.md` уже есть staged `/v1`-ответы не только про public context repo, но и про архитектурную декомпозицию будущего продукта.
- По domain-model вопросу уже есть staged два `/v1`-ответа:
  - `V1-20260523-055021`
  - `V1-20260523-055021-2`
- По next-step decomposition вопросу уже есть staged `/v1`-ответ:
  - `V1-20260524-184203`
- Его полезное знание принято как handoff target:
  - `Canonical Fixture Seed`
  - `table-sandbox/src/fixtures/tiny-module/`
  - data-only fixture scope without loader/runtime/Phaser changes.
- На их основе созданы локальные planning artifacts:
  - `.ai/plans/master/domain_schemas_contract.md`
  - `.ai/plans/master/rules_hooks_interface.md`
- Главные выводы из этих planning artifacts подняты в `.ai/architecture.md` и `.ai/decisions.md`:
  - canonical split `definitions / runtime state / module rules`
  - canonical file set
  - minimal runtime-facing rules hook contract
- По `/v1` вопросу `V1-20260523-062449` получен staged ответ по `RulesHooksInterface`.
- На его основе создан следующий planning artifact:
  - `.ai/plans/master/action_event_contract.md`
- Для следующего шага planning подготовлен skeleton milestone artifact:
  - `.ai/plans/master/first_milestone_runtime_skeleton.md`
- По `/v1` вопросу `V1-20260523-124734` получен staged sequencing answer по `Table Sandbox 0.1`.
- Его полезное знание перенесено в planning layer как:
  - `.ai/plans/master/table_sandbox_0_1_milestone_plan.md`
  - `.ai/plans/master/first_vertical_slice_spec.md`
- По `/v1` вопросу `V1-20260523-130238` получен staged ответ по минимальным canonical file schemas.
- Его полезное знание перенесено в planning layer как:
  - `.ai/plans/master/minimal_canonical_file_schemas.md`
- Current schema-level emphasis:
  - `project.json` = workspace index only;
  - `module.json` = manifest only;
  - `map.json` = topology only;
  - `scenario.json` = initial setup only;
  - `rules.metadata.json` = declarative rules capabilities only;
  - `savegame.json` = mutable runtime state only;
  - temporary compact `pieceDefinitions[]` / `factions[]` in `module.json` is acceptable for `0.1`, but not final target.
- Shared vocabulary aligned across planning docs:
  - workspace index;
  - module manifest;
  - board topology;
  - initial setup;
  - rules capabilities metadata;
  - mutable runtime snapshot.
- Stack model verdict:
  - safe default now is derived stack by shared `locationId`;
  - `Stack` is not a canonical entity for `0.1`;
  - `stackId` and `stackPosition` stay out of the first save format;
  - advanced stack model remains later work.
- По `/v1` вопросу `V1-20260523-141825` получен staged ответ по трём оставшимся вопросам для `Table Sandbox 0.1`.
- Его полезное знание принято в planning layer как:
  - save compatibility for `0.1` = block structural incompatibility, warn on minor safe mismatch, no migration engine yet;
  - authoring changes and runtime changes must stay separated by explicit modes;
  - small `PieceDefinition[]` / `FactionDefinition[]` inside `module.json` remain acceptable as temporary compact `0.1` layout only.
- По `/v1` вопросу `V1-20260523-142942` получен staged ответ по developer-side authoring workflow.
- Его полезное знание принято в planning layer как:
  - hybrid Module Authoring Workspace;
  - specialized surfaces inside workspace;
  - explicit Play Sandbox Preview for runtime proof;
  - authoring creates module package, runtime executes it through `GameState` and `Action/Event`.
- Current working emphasis:
  - minimal canonical data seed;
  - `GameState` bootstrap;
  - `Action/Event` pipeline;
  - permissive `RulesHooks`;
  - first thin vertical slice: move one piece between two spaces.
- РџРѕ `/v1` РІРѕРїСЂРѕСЃСѓ `V1-20260523-150830` РїРѕР»СѓС‡РµРЅ staged macro-roadmap answer
  РїРѕСЃР»Рµ `Table Sandbox 0.1`.
- Р•РіРѕ РїРѕР»РµР·РЅРѕРµ Р·РЅР°РЅРёРµ РїСЂРёРЅСЏС‚Рѕ РІ planning layer РєР°Рє:
  - platform-first ladder `0.2 -> 0.3 -> 0.4 -> 0.5 -> 1.0`;
  - hardening before breadth, breadth before assisted rules, assisted rules
    before richer content subsystems;
  - Sword of Rome-like module stays reference/test module, not lower-layer
    driver.
- РќР° РµРіРѕ РѕСЃРЅРѕРІРµ СЃРѕР·РґР°РЅ РЅРѕРІС‹Р№ master planning artifact:
  - `.ai/plans/master/post_0_1_platform_roadmap.md`
- РџРѕ `/v1` РІРѕРїСЂРѕСЃСѓ `V1-20260523-152316` РїРѕР»СѓС‡РµРЅ staged ответ про
  mature `module package` model.
- Р•РіРѕ РїРѕР»РµР·РЅРѕРµ Р·РЅР°РЅРёРµ РїСЂРёРЅСЏС‚Рѕ РІ planning layer РєР°Рє:
  - `module package` РґРѕР»Р¶РµРЅ РѕСЃС‚Р°С‚СЊСЃСЏ product bundle СЃ required/optional
    package parts;
  - `module.json` stays manifest, not content dump;
  - `savegame.json` stays runtime artifact, not canonical module content;
  - mature shape is documented in `.ai/plans/master/module_package_model.md`.
