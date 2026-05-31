# Session: v3_artifact_contract_and_v1_request

## Session ID

`2026-05-27_v3_artifact_contract_and_v1_request`

## Status

in_progress

## Goal

Сохранить присланный V3-документ как публичный артефакт в repo, сделать его discoverable для внешнего контекста, получить внешний planning input, зафиксировать master-plan внедрения V3 и провести первые rollout-фазы нового режима `Kilo Notebook V3`.

## Approved Plan

1. Прочитать V3-документ и связанные V1/V2 workflow-файлы.
2. Положить V3-документ в public stable path и обновить `repo_navigation.md`.
3. Закоммитить и запушить артефакт V3.
4. Подготовить `/v1` prompt с central links и project-specific ссылками на V1/V2/V3.
5. На основе ответа V1 подготовить master-plan внедрения V3 как отдельного режима `Kilo Notebook V3`.
6. Выполнить `Phase 0. Contract Alignment` через Kilo.
7. Принять и запушить `Phase 0`.
8. Выполнить `Phase 1. V3 Docs Foundation` через Kilo.
9. Выполнить `Phase 2. Contract Pack` через Kilo.
10. Выполнить `Phase 3. Prompt and Template Layer` через Kilo.
11. Выполнить `Phase 4. Runtime Mode Integration` через Kilo.
12. Подготовить первый V3 request и copy-paste prompt для `Phase 5. Safe Pilot`.
13. Выполнить `Phase 5. Safe Pilot` через `Kilo Notebook V3`.
14. Внедрить лёгкий `V3 Post-Import Test Prompt Layer` через Kilo как process-correction для действующего V3 workflow.
15. Выровнять во всей V3-системе wording про доступ внешнего чата: GitHub context readable, direct repo/local workspace write unavailable.

16. РЈСЃРёР»РёС‚СЊ V3 post-import testing flow: notebook auto-emits testing prompt, tester СЃРЅР°С‡Р°Р»Р° СЃРѕРіР»Р°СЃСѓРµС‚ split machine-vs-human checks, machine-check report РїРёС€РµС‚СЃСЏ РІ РѕС‚РґРµР»СЊРЅС‹Р№ V3-ID-based file.
17. Перейти в `Phase 6`: cleanup/hardening V3 lifecycle, policy for tester prompts and machine-check reports, accepted journal policy, closure rules для imported cycles.
18. Запустить первый `Phase 7` slice: scripted support foundation для `scripts/v3/` (`validate_v3_package.py`, `stage_v3_package.py`, `write_v3_journal.py`) без `/v3` shortcut и без `apply_v3_package.py`.
19. Закрыть `Phase 7`: активировать `/v3` shortcut как explicit V3 import-entry mode, привязать его к каноническому prompt template и синхронизировать Phase 7 status во всех source-of-truth файлах без auto-apply слоя.

## Active Plan Item

`19. Закрыть Phase 7: активировать /v3 shortcut как explicit V3 import-entry mode, привязать его к каноническому prompt template и синхронизировать Phase 7 status во всех source-of-truth файлах без auto-apply слоя`

## Runs

- `Session run: 001` - direct Codex execution by explicit user request: сохранить V3-документ в repo, запушить и подготовить `/v1` prompt.
- `Session run: 002` - prepared handoff `0030_v3_phase0_contract_alignment.md` for Kilo execution of `Phase 0. Contract Alignment`.
- `Session run: 003` - Codex review of run `0030`: first report not accepted, correction required.
- `Session run: 004` - accepted corrected run `0030`, created checkpoint commit `269e676` and pushed it.
- `Session run: 005` - prepared handoff `0031_v3_phase1_docs_foundation.md` for Kilo execution of `Phase 1. V3 Docs Foundation`.
- `Session run: 006` - accepted `Phase 1`, transferred persistent docs changes into `codex/editor-play-visual-continuity-plan`, applied accepted V2 fixes, and performed Codex-owned cleanup of `review/v2/20260527-151700-v3-phase1-docs-foundation`.
- `Session run: 007` - prepare handoff `0032_v3_phase2_contract_pack.md` for full `Phase 2. Contract Pack`.
- `Session run: 008` - accepted and pushed `Phase 2`, then prepared handoff `0033_v3_phase3_prompt_and_template_layer.md` for full `Phase 3. Prompt and Template Layer`.
- `Session run: 009` - accepted and pushed `Phase 3`, then prepared handoff `0034_v3_phase4_runtime_mode_integration.md` for full `Phase 4. Runtime Mode Integration`.
- `Session run: 010` - accepted and pushed `Phase 4`, then clarified rollout order for `Phase 5`: first prepare external V3 request/prompt, then run `Kilo Notebook V3` import.
- `Session run: 011` - direct Codex execution by explicit user request: prepared first V3 request artifacts for `Phase 5 Safe Pilot` and shifted handoff `0035_v3_phase5_safe_pilot.md` to the next plan item.
- `Session run: 012` - multiple V3 pilot cycles reviewed and accepted progressively: external package tests, product-code stress tests, root-cause hardening, and first clean docs-only import in the correct repo/workspace.
- `Session run: 013` - prepare handoff `0036_v3_post_import_test_prompt_layer.md` for lightweight post-import testing integration into the active V3 workflow.
- `Session run: 014` - `0036` accepted and pushed; current follow-up: prepare system-wide V3 wording alignment for external chat access semantics.
- `Session run: 015` - prepared handoff `0037_v3_external_chat_access_wording_alignment.md`, accepted wording-alignment result, and synced active turn-tracker V3 request artifacts for the next external cycle.

- `Session run: 016` - prepare handoff `0038_v3_post_import_testing_flow_hardening.md` for deeper V3 testing-flow hardening after first real turn-tracker verification cycle.
- `Session run: 017` - prepare handoff `0039_v3_phase6_lifecycle_cleanup_and_closure.md` for full `Phase 6` V3 lifecycle cleanup/hardening.
- `Session run: 018` - prepare handoff `0040_v3_phase7_scripted_support_foundation.md` for first `Phase 7` scripted-support slice without `/v3` shortcut and without `apply_v3_package.py`.
- `Session run: 019` - prepare handoff `0041_v3_phase7_shortcut_activation_and_runtime_entry.md` for final `Phase 7` closure: activate `/v3` shortcut, bind it to canonical template, sync source-of-truth status without creating auto-apply.

## User Overrides

- Пользователь явно попросил сохранить документ как артефакт и запушить его в репозиторий.
- Пользователь явно выбрал маршрут `V1` для внешнего planning-запроса.
- Внешнему чату нужен общий план внедрения V3, а не только первый микро-шаг.
- В плане внедрения V3 обязательно должен быть отдельный KillaMod/Kilo mode блокнот V3.
- После review Kilo `Phase 0` push делать только если результат реально принят по diff и проверкам.
- Для следующего шага после `Phase 1` не дробить работу слишком мелко: готовить сразу весь `Phase 2`.
- Для следующего шага после `Phase 3` не дробить работу слишком мелко: готовить сразу весь `Phase 4`.
- Для post-import testing в V3 не раздувать workflow лишними статусами и журналами: нужен лёгкий prompt-at-exit flow, где `Kilo Notebook V3` просто выводит тестовый prompt, обычный Kilo code run выполняет machine-checks, человек делает удобные manual checks, а Codex сводит verdict.
- Формулировка про внешний V3 чат должна быть точной во всей системе: он может читать публичный GitHub-контекст по ссылкам, но не имеет прямой записи в repo и не имеет локального filesystem-доступа к workspace.

## Checkpoint State

- Исходный документ `C:/Users/andre/Downloads/V3_system_contract.md` прочитан и сохранён как публичный артефакт.
- V3 master docs созданы и запушены:
  - `.ai/plans/master/v3_artifact_producing_workflow_contract.md`
  - `.ai/plans/master/v3_workflow_implementation_plan.md`
- Ответы V1, использованные для V3 planning и Phase 0 scheduling, сохранены в локальном V1 notebook.
- `Phase 0. Contract Alignment` принят и запушен:
  - checkpoint commit: `269e676b970686d5ee3d2749867bb33cffd61fa9`
  - branch: `codex/editor-play-visual-continuity-plan`
- `Phase 1. V3 Docs Foundation` принят:
  - persistent docs layer `.ai/v3/` перенесён в рабочую ветку;
  - accepted V2 minor fixes применены;
  - temporary V2 review branch удалена по default cleanup policy.
- `Phase 2. Contract Pack` принят и запушен:
  - checkpoint commits: `9f4889c72aee7c6a17cbf979359e90448b5bc2af` и recovery-fix `fafccd0b6fb354612c973950c41d2ed0e600f085`
  - branch: `codex/editor-play-visual-continuity-plan`
- `Phase 3. Prompt and Template Layer` принят и запушен:
  - checkpoint commit: `51458eb0214f307edf06f837afb63a0fd2c23260`
  - branch: `codex/editor-play-visual-continuity-plan`
- `Phase 4. Runtime Mode Integration` принят и запушен:
  - checkpoint commit: `c67d2691d66dbd2ed574ef1b16eb341f53165093`
  - branch: `codex/editor-play-visual-continuity-plan`
- Подготовлены локальные артефакты первого V3 request для `Phase 5 Safe Pilot`.
- `Phase 5` практически доказан:
  - есть валидные external packages;
  - есть product-code stress tests;
  - есть повторный чистый docs-only import в правильном repo/workspace без shadow-write.
- Следующий одобренный шаг: внедрить лёгкий `Post-Import Test Prompt Layer`, чтобы V3 package мог передавать machine-check + human-check prompt дальше в обычный Kilo code run без нового handoff и без раздувания `V3_navigation.md`.
- `0036` принят и запушен:
  - checkpoint commit: `beef31c1f2cf13846846ccda8355cfbe5d1eb37b`
  - branch: `codex/editor-play-visual-continuity-plan`
- Новый открытый follow-up: выровнять во всём V3 canon wording про внешний чат, чтобы везде было явно различено:
  - GitHub read-only context доступен;
  - direct repo write недоступен;
  - local workspace filesystem access недоступен.
- `0037` принят как system wording correction:
  - V3 canon теперь явно различает `GitHub context readable`, `direct repo write unavailable`, `local workspace filesystem unavailable`;
  - historical request files не переписывались;
  - текущий активный цикл `V3-20260529-145329-turn-tracker-html-with-testing` синхронизирован с новым wording.
- `0038` принят и запушен:
  - checkpoint commit: `8e5fdc9`
  - post-import testing flow hardened: auto-emit, execution split, machine-check report path.
- `0039` принят и запушен:
  - checkpoint commit: `b628fd3`
  - `Phase 6` зафиксирован как lifecycle cleanup/hardening, не новый pilot.
- `0040` принят и запушен:
  - checkpoint commit: `7f4303e`
  - `Phase 7 foundation` создан: `scripts/v3/` helper layer существует, safety boundaries сохранены.
- Следующий одобренный шаг: закрыть `Phase 7` через активацию `/v3` shortcut как explicit V3 import-entry mode и синхронизацию source-of-truth wording без auto-apply слоя.
