# V3 - Artifact-Producing Workflow Layer

`.ai/v3/` — canonical-слой для V3 artifact-producing workflow в этом репозитории.

## Что такое V3

V3 — это третий workflow route внешнего взаимодействия:

- V1 — prompt-only анализ;
- V2 — bounded technical review зафиксированного WIP/snapshot;
- V3 — внешний artifact-producing workflow.

В V3 внешний чат не пишет файлы в репозиторий напрямую. Он готовит artifact package. Дальше пакет:

- сначала проходит pre-Kilo review;
- потом, если import-stage реально разрешён, подаётся в `Kilo Notebook V3`;
- затем появляются journal, Codex review и human verdict.

## Текущий статус

**Phase 0 завершён (2026-05-27):** режим `kilo-notebook-v3` / `Kilo Notebook V3` canonically разрешён в mode lists, правилах и validator.

**Phase 1 завершён (2026-05-27):** `.ai/v3/` foundation layer создан.

**Phase 2 завершён (2026-05-27):** создан contract pack.

**Phase 3 завершён (2026-05-27):** создан prompt/template layer.

**Phase 4 завершён (2026-05-27):** создан setup guide и manual runtime readiness docs.

### Operational status right now

- `Kilo Notebook V3` в canon существует.
- Setup guide для ручной настройки режима существует.
- `/v3` shortcut не активирован.
- `scripts/v3/*` не созданы.
- UI-настройка режима в живом Kilo UI подтверждена человеком на первом pilot cycle.
- ZIP import capability подтверждена на pilot cycles, но root-resolution bug повторился и всё ещё требует hardening.
- **Post-import testing layer внедрён (2026-05-29):** лёгкий `POST_IMPORT_TEST_PROMPT.md` как support artifact для проверки импортированных файлов через обычный Kilo code run.

Надо различать:

```text
Target V3 flow:
request -> external package -> Kilo Notebook V3 import -> journal -> [post-import testing, если required] -> Codex review -> human verdict

Current runtime reality:
external package generation уже доказан,
UI mode уже подтверждён,
первый import pilot уже выполнен,
post-import testing layer уже внедрён,
но human verdict по pilot ещё не дан
и preset/root-resolution layer ещё требует hardening.
```

### Root-resolution hard rule

Для `Kilo Notebook V3` source archive path и target repo path — не одно и то же.

Обязательное правило:

```text
Все relative target paths, journal paths и lifecycle paths
разрешаются только от git repo root,
полученного через `git rev-parse --show-toplevel`.
```

Недопустимо:

- писать рядом с ZIP в `Downloads`;
- писать в `Documents`;
- создавать parallel `.ai/` tree вне текущего репозитория;
- считать, что текущий VS Code workspace автоматически равен repo root.

Если git repo root не определяется, import-run должен завершаться `blocked`.

## Как устроен V3 процесс

### Target flow

```text
Codex / человек
  -> готовит V3 request
  -> передаёт его внешнему чату

Внешний чат
  -> читает commit-pinned GitHub context
  -> создаёт V3 artifact package
  -> кратко описывает, что именно создал

Kilo Notebook V3
  -> принимает raw input:
     archive link или archive file path
     + optional short note
  -> проверяет package
  -> пишет только разрешённые файлы
  -> создаёт journal draft
  -> обновляет V3 lifecycle entry

Kilo Notebook V3
  -> принимает raw input:
     archive link или archive file path
     + optional short note
  -> проверяет package
  -> пишет только разрешённые файлы
  -> создаёт journal draft
  -> обновляет V3 lifecycle entry
  -> если есть POST_IMPORT_TEST_PROMPT.md и testing required — показывает prompt человеку

Post-import testing (если required)
  -> человек копирует Machine checks в обычный Kilo code run
  -> Kilo code run выполняет проверки и пишет report
  -> человек выполняет Human checks вручную

Codex
  -> проверяет journal, реальные файлы и (если required) testing status
  -> формирует verdict

Человек
  -> принимает / отправляет на доработку / отклоняет
```

### Current rollout split for Phase 5

Сейчас нельзя смешивать внешний package test и Kilo import pilot. Phase 5 делится так:

```text
Phase 5A - External Artifact Generation Pilot
Внешний чат по GitHub links создаёт package. Kilo import ещё не начинается.

Phase 5B - Pre-Kilo Package Review
Codex / человек проверяют ZIP, manifest, checksums, files list и scope.
Пакет может быть валиден, но ещё не imported.

Phase 5C - Kilo Notebook V3 UI Setup
Человек реально настраивает режим в UI и подтверждает, что он существует.

Phase 5D - Kilo Import Pilot
Только после 5A/5B/5C запускается реальный import-run.
```

### Hard rule

`Kilo Notebook V3` run нельзя запускать, пока одновременно не выполнены все условия:

1. Есть реальный внешний artifact package.
2. Режим `Kilo Notebook V3` реально настроен в UI.
3. Явно выбран import-stage, а не только external artifact test.
4. Явно выбран source пакета для raw input.
5. Человек подтвердил, что сейчас тестируется именно import, а не только package generation.

## GitHub-first rule for external chat

Для V3 external request по умолчанию используется такой режим:

```text
Prompt содержит commit-pinned GitHub raw links.
Внешний чат читает контекст сам по этим ссылкам.
Человек не обязан вручную прикладывать context files,
если fallback_context_mode явно не объявлен.
```

Это правило относится к external request generation stage, а не к import-stage.

## Raw input and storage

Для `Kilo Notebook V3` важно не путать raw input с handoff:

- это не handoff-driven mode;
- это raw-input notebook mode;
- минимальный вход: ссылка на архив или путь к архиву;
- optional: короткая текстовая note из ответа внешнего чата;
- request/prompt/request-history ведутся отдельно через `.ai/v3/requests/` и [`V3_navigation.md`](V3_navigation.md).

До import-stage нельзя навешивать на человека ad-hoc staging как будто это уже canon.

Сейчас правильно так:

- до Phase 5D человек может просто хранить ZIP локально;
- package может быть проверен Codex/человеком без импорта;
- `.ai/v3/staging/` — это зона import-stage, а не обязательный pre-Kilo шаг;
- если позже выбран repo-local staging fallback, он должен быть выбран явно как import source, а не придуман на ходу.

## Что здесь будет

| Папка | Назначение | Статус |
|---|---|---|
| [`contracts/`](contracts/README.md) | Формальные контракты V3 | Phase 2 завершён |
| [`templates/`](templates/README.md) | Шаблоны request/manifest/journal/review/revision | Phase 3 завершён |
| [`prompts/`](prompts/README.md) | Prompt layer для request/import/review/revision | Phase 3 завершён |
| [`docs/`](docs/README.md) | Setup guide и process docs | Phase 4+, уточняется после Phase 5 split |
| [`requests/`](requests/) | Request/prompt artifacts и staged V3 inputs | local workflow layer |

## Границы V3

- Внешний чат может читать публичный GitHub-контекст по ссылкам из prompt. Внешний чат не имеет прямого repo write access и не имеет локального filesystem-доступа к workspace. Внешний чат создаёт ZIP artifact package, а не делает прямой repo write.
- Artifact package не равен imported result.
- Pre-Kilo package review не равен import.
- Setup guide не равен факту, что режим уже настроен в UI.
- `V3_navigation.md` ведётся как lifecycle/archive index, как в `V1` и `V2`.
- Codex остаётся проверяющим слоем.
- Финальное решение остаётся за человеком.

## Связанные документы

- [`V3_navigation.md`](V3_navigation.md) - навигация и lifecycle index по этому V3-слою.
- [`../plans/master/v3_workflow_implementation_plan.md`](../plans/master/v3_workflow_implementation_plan.md) - поэтапный план внедрения V3.
- [`contracts/v3_request_contract.md`](contracts/v3_request_contract.md) - контракт V3 request.
- [`contracts/v3_storage_policy.md`](contracts/v3_storage_policy.md) - storage/input policy.
- [`contracts/v3_acceptance_policy.md`](contracts/v3_acceptance_policy.md) - acceptance rules.
- [`docs/manual_kilo_notebook_v3_setup.md`](docs/manual_kilo_notebook_v3_setup.md) - ручная настройка режима.
