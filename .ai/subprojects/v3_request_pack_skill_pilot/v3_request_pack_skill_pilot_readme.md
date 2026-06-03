# V3 Request Pack Skill Pilot Readme

Slug: `v3_request_pack_skill_pilot`  
Owner: `Orc`  
Audience: human first  
Status: `draft`  
Lifecycle stage: `Stage 5 pilot`  
Active route: `Planner -> Orc`

## Что это

`v3_request_pack_skill_pilot` — docs-only подпроект для первого `Stage 5` pilot по теме skill `v3-request-pack-prep`.

Подпроект нужен, чтобы отдельно держать:

- planning;
- boundaries;
- human gates;
- V3 request preparation;
- package-only review.

Он не равен skill execution, import-stage или accepted result.

## Зачем он нужен

Подпроект защищает от путаницы между:

- request;
- returned package;
- import;
- accepted result;
- global skill materialization.

Смысл простой: сначала собрать безопасный docs-layer, потом по отдельным human решениям двигаться дальше.

## Что уже принято

- active route `Planner -> Orc`;
- подпроект остаётся docs-only;
- `request != package != import != accepted result`;
- `Stage 6` не открыт;
- repo-level promotion не открыт;
- global skill materialization требует отдельного human gate;
- automation допустим только как узкий `request-pack preflight helper` по отдельному human decision;
- human approval ничем не заменяется.

## Что уже подготовлено

- `plan_full`;
- minimal docs set;
- accepted `battle_plan`;
- локальный V3 request draft на repo-local `skill_draft`.

## Что читать

| Ситуация | Читать |
|---|---|
| Быстро понять подпроект | этот `readme`, потом `navigation` |
| Проверить границы | `decisions` |
| Проверить стратегию | `plan_full` |
| Найти нужный блок в плане | `plan_index` |
| Проверить фактические действия | `journal` |

## Какие документы уже есть

Canonical docs подпроекта:

- `v3_request_pack_skill_pilot_plan_full.md`
- `v3_request_pack_skill_pilot_battle_plan.md`
- `v3_request_pack_skill_pilot_readme.md`
- `v3_request_pack_skill_pilot_decisions.md`
- `v3_request_pack_skill_pilot_plan_index.md`
- `v3_request_pack_skill_pilot_journal.md`
- `v3_request_pack_skill_pilot_navigation.md`

Связанные V3 request artifacts:

- `V3-20260602-114035-v3-request-pack-skill-draft_request.md`
- `V3-20260602-114035-v3-request-pack-skill-draft_prompt.md`
- `V3-20260602-114035-v3-request-pack-skill-draft_send_note.md`

## Что ещё не начато

- `status`;
- внешний V3 request run;
- returned package;
- import;
- skill materialization в global home;
- `Stage 6`;
- repo-level promotion.

## Current safe next step

Открыть prepared V3 prompt, отправить его во внешний чат и вернуть сюда ZIP package или ZIP-ready representation для package-only review.

## Role warning

- `Planner` держит стратегию.
- `Orc` ведёт operational docs и evidence.
- Human закрывает gates.
- Agent recommendation не равен human approval.
