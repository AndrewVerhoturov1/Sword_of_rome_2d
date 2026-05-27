# V3 — Artifact-Producing Workflow Layer

`.ai/v3/` — canonical-слой для будущего V3 artifact-producing workflow в этом репозитории.

## Что такое V3

V3 — это третий workflow route внешнего взаимодействия (после V1 — prompt-only анализ, и V2 — bounded technical review). В V3 внешний ChatGPT выступает как генератор готовых проектных артефактов (файлов, скриптов, схем, шаблонов), которые затем безопасно импортируются в репозиторий через специальный режим `kilo-notebook-v3`.

V3 не заменяет V1 и V2. Это дополнительный маршрут для задач, где внешний чат должен подготовить реальные файлы, а не только текстовый анализ или ревью.

## Текущий статус

**Phase 0 завершён (2026-05-27):** режим `kilo-notebook-v3` / `Kilo Notebook V3` canonically разрешён в mode lists, правилах и валидаторе. Режим отделён от `kilo-notebook` (`/v1-only`), `kilo-recorder` (`/r1-only`) и V2.

**Phase 1 (текущая):** этот README и вся `.ai/v3/` структура созданы как discoverable foundation layer.

Full operational V3 workflow ещё впереди. Сейчас недоступно:

- `/v3` shortcut не активирован;
- operational scripts `scripts/v3/*` не созданы;
- contracts, templates, prompts для V3 ещё не написаны;
- pilot не проведён;
- journaling и Codex review flow не настроены.

## Что здесь будет

По мере rollout-а следующих фаз здесь появятся:

| Папка | Назначение | Фаза |
|-------|------------|------|
| [`contracts/`](contracts/README.md) | Формальные контракты V3: request, artifact package, manifest, journal, review, revision, storage, scope, acceptance | Phase 2 |
| [`templates/`](templates/README.md) | Шаблоны: V3 request, manifest.yaml, journal, Codex review, revision request | Phase 3 |
| [`prompts/`](prompts/README.md) | Промпты: create V3 request, kilo-notebook-v3 mode, Codex review, revision request | Phase 3 |
| [`docs/`](docs/README.md) | Документация: setup guide, safety rules, storage policy, pilot notes | Phase 3+ |

Пока эти папки содержат только placeholder README.

## Как устроен V3 процесс (целевая схема)

```text
Codex / человек
  → готовит V3 request
  → передаёт внешнему ChatGPT

Внешний ChatGPT
  → создаёт V3 artifact package (ZIP)
  → manifest + checksums + files

Kilo Notebook V3
  → принимает package
  → проверяет manifest, пути, хэши
  → записывает только разрешённые файлы
  → создаёт journal entry

Codex
  → проверяет journal и реальные файлы
  → запрашивает human review при необходимости

Человек
  → принимает / отклоняет / отправляет на доработку
```

Главный принцип: ChatGPT создаёт артефакты, KiloCode физически пишет файлы, Codex проверяет, человек принимает.

## Связанные документы

- [`v3_artifact_producing_workflow_contract.md`](../plans/master/v3_artifact_producing_workflow_contract.md) — проектный контракт V3 (draft).
- [`v3_workflow_implementation_plan.md`](../plans/master/v3_workflow_implementation_plan.md) — поэтапный план внедрения V3.
- [`V3_navigation.md`](V3_navigation.md) — навигация по этому V3-слою.
- [`../repo_navigation.md`](../repo_navigation.md) — общая навигация репозитория (секция V3).

## Границы V3

- V3 не подменяет Codex decision layer. Codex остаётся проверяющим.
- Внешний чат не имеет доступа к репозиторию. Он только создаёт пакет.
- Все записи проходят через KiloCode, журналируются и проверяются.
- Финальное решение всегда за человеком.
