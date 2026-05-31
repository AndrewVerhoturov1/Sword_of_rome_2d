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
- сохранить review artifacts отдельно от core docs.

## Approved Plan

### P1: Resolve accepted V3 findings conservatively

- Status: in_progress.
- Уточнить anchors и plan/index sync.
- Усилить `navigation`, `status`, `journal`, `decisions` без расширения file-set.
- Зафиксировать границу между source docs и critique layer `reviews/`.
- Не добавлять новые core files сверх исходного 8-file pack.
- Не трогать global workflow docs.
- Не коммитить V3 journal draft, потому что он local-only до human accept.

## Active Plan Item

`P1: Resolve accepted V3 findings conservatively`

## Runs

- `Session run: 001` - bootstrap `ork_planner` subproject as 8-file documentation container.
- `Session run: 002` - prepare and import V3 critique package for all 8 core docs.
- `Session run: 003` - review imported critique, accept partial findings, update source docs conservatively, prepare git checkpoint.

## User Overrides

- Пользователь явно выбрал `Full minimal pack`, а не one-file bootstrap.
- Пользователь явно потребовал V3 critique package с отдельным `V3-*.md` review file на каждый core doc.
- Пользователь хочет разбор `что берем / что не берем`, а не слепое принятие всего critique.
- Для этого шага пользователь явно разрешил прямое выполнение и git publish из текущего чата.

## Checkpoint State

- `.ai/subprojects/ork_planner/` существует и содержит 8 core files.
- V3 critique imported under `.ai/subprojects/ork_planner/reviews/`.
- V3 lifecycle entry существует в `.ai/v3/V3_navigation.md`.
- `.ai/v3/journals/drafts/V3-20260531-091439-ork-planner-doc-critique_journal.yaml` существует как local-only draft и не должен коммититься на этом шаге.
- Human verdict по текущему виду source docs ещё нужен до Orc step.
