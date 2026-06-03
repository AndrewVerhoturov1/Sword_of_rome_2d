# Session: stage5_v3_request_pack_skill_pilot

## Session ID

`2026-06-02_stage5_v3_request_pack_skill_pilot`

## Status

handoff-prepared

## Goal

Зафиксировать planning artifact для первого `Stage 5` pilot после `ork_planner`:

- создать новый tiny docs-only подпроект для skill-пилота;
- целиться в глобальный личный Codex skill, а не в repo-level promotion;
- доказать полезность skill не только через сборку `V3 request pack`, но и через получение годного внешнего `V3 artifact package`;
- не открывать `Stage 6`;
- не подменять human approval;
- не возвращать legacy route.

## Approved Plan

### P1: Stage 5 pilot frame

- Status: ready.
- Новый подпроект: `.ai/subprojects/v3_request_pack_skill_pilot/`.
- Подпроект остаётся docs-only и служит pilot-layer, а не местом repo-level migration.
- Целевой итоговый skill path: `C:\Users\andre\.codex\skills\v3-request-pack-prep\`.
- Active route: `Planner -> Orc`.

### P2: Minimal v1 skill scope

- Status: ready.
- Skill v1 помогает готовить `V3 request pack` для внешнего чата.
- V1 scope ограничен `workflow_docs`.
- Skill удерживает:
  - обязательные поля `V3 request`;
  - GitHub-first rule;
  - границу `request != package != import`;
  - сборку `allowed_paths`, `forbidden_paths`, `expected_files`, `acceptance_criteria`, `known_risks`.
- Вне scope:
  - `Kilo Notebook V3` import;
  - post-import testing;
  - `schemas`, `scripts`, `product_code`;
  - repo-level alignment.

### P3: Subproject docs set and waivers

- Status: ready.
- Обязательный reduced set:
  - `{slug}_plan_full.md`
  - `{slug}_battle_plan.md`
  - `{slug}_readme.md`
  - `{slug}_status.md`
  - `{slug}_navigation.md`
  - `{slug}_journal.md`
  - `{slug}_decisions.md`
- Waiver:
  - `{slug}_plan_index.md` можно не создавать, пока `plan_full` короткий и с понятными headings.
- `decisions.md` обязателен, потому что pilot уже содержит долгоживущие решения по target path, proof bar и stop rules.

### P4: Lifecycle and gates

- Status: ready.
- Planner phase:
  - создать `plan_full`;
  - зафиксировать folder, final skill path, v1 scope, proof profile, waivers;
  - остановиться на human gate.
- Human gate A:
  - человек принимает `plan_full`.
- Orc phase 1:
  - создать `battle_plan`.
- Human gate B:
  - человек принимает `battle_plan`.
- Orc phase 2:
  - создать remaining docs set;
  - вести factual `journal`;
  - вести long-lived `decisions`.
- Human gate C:
  - человек принимает docs-system подпроекта.
- Capability-sensitive gate:
  - отдельный human signal на создание глобального skill вне repo.
- Skill build phase:
  - создать минимальный skill bundle:
    - `SKILL.md`
    - `references/v3-request-pack-core.md`
    - `references/v3-request-pack-example.md`
    - `agents/openai.yaml`
- Proof phase A:
  - применить skill к одной реальной маленькой `workflow_docs` задаче;
  - собрать один реальный `V3 request pack`;
  - сделать human review pack перед внешним прогоном.
- Human gate D:
  - человек явно разрешает внешний прогон.
- Proof phase B:
  - внешний чат возвращает реальный `V3 artifact package`;
  - package проходит pre-Kilo review как package-only результат, без import-stage.
- Human gate E:
  - человек подтверждает, что package годный для своей стадии.

### P5: Success criteria and stop rules

- Status: ready.
- Pilot считается успешным только если:
  - skill v1 создан как глобальный личный Codex skill;
  - по skill собран один реальный `V3 request pack`;
  - по этому pack внешний чат вернул реальный годный `V3 artifact package`;
  - package проходит package-only review;
  - pilot не открыл import-stage и не объявил `Stage 6` начатым.
- Returned package считать годным только если:
  - это реальный ZIP artifact package;
  - соблюдён `v3_artifact_package_contract.md`;
  - package не заявляет, что repo уже изменён;
  - package не выходит за `workflow_docs`.
- Остановиться и вернуть вопрос человеку, если:
  - scope хочет выйти за `workflow_docs`;
  - появляются scripts/codegen/auto-apply;
  - proof требует repo-level writes;
  - кто-то пытается считать package import-stage результатом;
  - возникает попытка открыть `Stage 6` без принятого `Stage 5`.

## Active Plan Item

`P1: Stage 5 pilot frame`

## Runs

| Session run | Summary |
|---|---|
| 001 | прочитан `ork_planner_stage5_first_pilot_bridge.md`, связанные `ork_planner` docs, V3 contracts/prompts/templates и зафиксирован Stage 5 planning artifact |
| 002 | локально прочитан внешний draft `v3_request_pack_skill_pilot_plan_full_draft.md`, подтверждено что draft полезен как input, но слишком велик для canonical `plan_full`; подготовлен отдельный Kilo handoff на compaction и точечную правку baseline `plan_full` |

## User Overrides

- Сохранить план как artifact.
- Закоммитить и запушить artifact.
- Целевой home для итогового skill: глобальный личный Codex skill.
- Proof bar усилен: skill должен дойти дальше request pack и довести flow до годного внешнего `V3 artifact package`.
- Подготовить Kilo-задачу, чтобы отдельный Kilo run выполнил compaction и содержательную правку pilot `plan_full`, после чего Codex сделает review.

## Checkpoint State

- `ork_planner` использован как source-of-truth для Stage 5 constraints, reduced docs set, gates и stop rules.
- Canonical baseline plan перенесён в подпроект: `.ai/subprojects/v3_request_pack_skill_pilot/v3_request_pack_skill_pilot_plan_full.md`.
- Внешний draft `v3_request_pack_skill_pilot_plan_full_draft.md` локально оценён как review input, а не как новый canonical plan.
- Следующий execution slice выделен отдельно: узкий Kilo docs run на compaction и правку только canonical `v3_request_pack_skill_pilot_plan_full.md`.
- Текущий planning artifact не является start signal для `Stage 5 execution`.
- Текущий planning artifact не является разрешением на repo-level promotion.
- Следующий безопасный шаг: выполнить подготовленный Kilo handoff, затем сделать Codex review report и diff.
