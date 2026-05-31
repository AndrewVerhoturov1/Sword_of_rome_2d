# Session: ork_planner_bootstrap_review_resolution

## Session ID

`2026-05-31_ork_planner_bootstrap_review_resolution`

## Status

in_progress

## Goal

Привести `ork_planner` bootstrap-документацию в более устойчивое состояние после импортированного V3 critique:

- разобрать findings;
- принять только минимально полезные правки;
- не раздувать структуру подпроекта;
- не запускать Orc;
- сохранить review artifacts отдельно от core docs;
- подготовить внешний `/v1` вопрос по root-cause analysis сбоя роли Planner.

## Approved Plan

### P1: Resolve accepted V3 findings conservatively

- Status: completed.
- Уточнить anchors и plan/index sync.
- Усилить `navigation`, `status`, `journal`, `decisions` без расширения file-set.
- Зафиксировать границу между source docs и critique layer `reviews/`.
- Не добавлять новые core files сверх исходного 8-file pack.
- Не трогать global workflow docs.
- Не коммитить V3 journal draft, потому что он local-only до human accept.

### P2: Prepare external `/v1` root-cause question

- Status: completed.
- Подготовить prompt-only запрос для внешнего чата.
- Дать commit-pinned GitHub links на rules, design source, session context и текущие `ork_planner` docs.
- Передать Codex diagnosis: где была модельная ошибка, где конфликт правил, где process gap.
- Попросить conservative fix set для active `Planner -> Orc` workflow без возврата к legacy `Boss / B1 / Junior Orchestrator`.

### P3: Apply accepted rule-level fixes after V1 review

- Status: completed.
- Read `V1-20260531-221800` and split fixes into accept/reject.
- Strengthen `codex_role_planner.md` with ownership boundary, Planner preflight, and explicit Planner -> Orc gate.
- Strengthen `codex_role_orc.md` with mirror ownership rule and prohibition on hidden Planner-maintained operational docs.
- Remove loophole in `subproject_single_execution_chat_documentation_system_v2.md`: temporary scaffold != live Orc maintenance.

## Active Plan Item

`P3: Apply accepted rule-level fixes after V1 review`

## Runs

- `Session run: 001` - bootstrap `ork_planner` subproject as 8-file documentation container.
- `Session run: 002` - prepare and import V3 critique package for all 8 core docs.
- `Session run: 003` - review imported critique, accept partial findings, update source docs conservatively, prepare git checkpoint.
- `Session run: 004` - prepare `/v1` external root-cause question about Planner role drift and rule/process fixes.
- `Session run: 005` - read `V1-20260531-221800`, accept conservative fixes, patch Planner/Orc rules and active design source.
- `Session run: 006` - archive current `ork_planner` bootstrap scaffold under `drafts/planner_bootstrap_scaffold_2026-05-31/`.

## User Overrides

- Пользователь явно выбрал `Full minimal pack`, а не one-file bootstrap.
- Пользователь явно потребовал V3 critique package с отдельным `V3-*.md` review file на каждый core doc.
- Пользователь хочет разбор `что берем / что не берем`, а не слепое принятие всего critique.
- Для предыдущего шага пользователь явно разрешил прямое выполнение и git publish из текущего чата.
- Пользователь явно потребовал `/v1` prompt для внешнего чата по problem statement: почему Planner не удержался в своей роли и как это починить.

## Checkpoint State

- `.ai/subprojects/ork_planner/` существует и содержит 8 core files.
- V3 critique imported under `.ai/subprojects/ork_planner/reviews/`.
- V3 lifecycle entry существует в `.ai/v3/V3_navigation.md`.
- `.ai/v3/journals/drafts/V3-20260531-091439-ork-planner-doc-critique_journal.yaml` существует как local-only draft и не должен коммититься на этом шаге.
- Human verdict по текущему виду source docs ещё нужен до Orc step.
- Next planning artifact: `/v1` prompt under `.ai/external_chats/requests/` with commit-pinned GitHub links, Codex diagnosis, and request for conservative repo-level fixes.

## Session Update After V1 Review

- `V1-20260531-221800` imported into notebook and used as grounded second opinion for Planner role drift.
- Accepted fix direction: ownership boundary, Planner preflight, explicit Planner -> Orc gate, external-review consideration or waiver, no hidden Planner-maintained Orc docs.
- Applied rule-layer patch in `codex_role_planner.md`, `codex_role_orc.md`, and `subproject_single_execution_chat_documentation_system_v2.md`.

## Session Update After Scaffold Archival

- Current `ork_planner` bootstrap scaffold moved from root `.ai/subprojects/ork_planner/` into `drafts/planner_bootstrap_scaffold_2026-05-31/`.
- Moved all root `ork_planner_*.md` core docs without changing their meaning.
- Moved `reviews/` into `drafts/planner_bootstrap_scaffold_2026-05-31/reviews/`.
- Root `.ai/subprojects/ork_planner/` now intentionally contains only `drafts/`.
