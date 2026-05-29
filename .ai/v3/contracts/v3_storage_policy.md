# V3 Storage Policy

Версия: 0.4
Назначение: формальная политика хранения V3 артефактов и input sources.
Статус: contract layer. Уточнена под raw-input notebook flow, lifecycle archive model и machine-check reports.

---

## 1. Принцип

V3 создаёт несколько разных слоёв:

- persistent repo-layer;
- request/archive layer;
- local package/input layer;
- import/runtime layer;
- human decision layer.

Главная поправка:

```text
Внешний package может существовать и review-иться
до того, как он вообще войдёт в import lane.
```

И ещё:

```text
Kilo Notebook V3 принимает raw input.
Raw input != handoff.
```

## 2. Классификация артефактов

### 2.1. Persistent tracked layer

| Артефакт | Путь | Условие |
|---|---|---|
| V3 contracts | `.ai/v3/contracts/*.md` | tracked |
| V3 README | `.ai/v3/README.md` | tracked |
| V3 navigation | `.ai/v3/V3_navigation.md` | tracked |
| Stable V3 docs | `.ai/v3/docs/*.md` | tracked |
| V3 prompts | `.ai/v3/prompts/*.md` | tracked |
| V3 templates | `.ai/v3/templates/*` | tracked |
| Accepted journal | `.ai/v3/journals/V3-*_journal.yaml` | только после human accept |

### 2.2. Request/archive layer

| Артефакт | Путь | Правило |
|---|---|---|
| V3 request files | `.ai/v3/requests/*_request.md` | обычно tracked после принятого process update |
| V3 prompt files | `.ai/v3/requests/*_prompt.md` | обычно tracked после принятого process update |
| V3 send notes / helper notes | `.ai/v3/requests/*_send_note.md` | допускаются как request-layer artifacts |
| Lifecycle entry | `.ai/v3/V3_navigation.md` | обновляется по стадиям, как в `V1`/`V2` |

### 2.3. Local package/input layer

| Артефакт | Место | Правило |
|---|---|---|
| Внешний ZIP package | local-only path, archive link, human-provided source | может существовать до import-stage |
| Short external note | human-provided raw text | optional |
| Package review notes | Codex/human review context | package можно review-ить без import |

Важно:

- до import-stage человек не обязан раскладывать ZIP в `.ai/v3/staging/`;
- внешний ZIP сам по себе не считается imported;
- raw input для `Kilo Notebook V3` может быть ссылкой на архив или локальным путём к архиву.

### 2.4. Local import/runtime layer

| Артефакт | Путь | Правило |
|---|---|---|
| Raw ZIP в import lane | `.ai/v3/staging/*.zip` | только если выбран repo-local staging fallback |
| Staging распаковка | `.ai/v3/staging/V3-*/` | только внутри import-stage |
| Rejected packages | `.ai/v3/staging/rejected/` | local-only |
| Revision packages | `.ai/v3/staging/revisions/` | local-only |
| Temporary journal drafts | `.ai/v3/journals/drafts/` | local-only до accept |
| Tester prompt copies | `.ai/v3/test_prompts/<V3-ID>_post_import_test_prompt.md` | local, создаётся `Kilo Notebook V3` после импорта, если в пакете есть `POST_IMPORT_TEST_PROMPT.md` и `mode != waived`. Ordinary Kilo code run и человек используют этот файл как основной prompt source. |
| Machine-check reports | `.ai/v3/test_reports/<V3-ID>_machine_check_report.md` | local, создаётся ordinary Kilo code run после post-import machine checks. Не journal. Не lifecycle registry. Codex читает этот файл как главный источник machine-check результатов. |

### 2.5. Human-decision layer

| Артефакт | Путь | Правило |
|---|---|---|
| Pending journal draft | `.ai/v3/journals/drafts/V3-*_journal.yaml` | не tracked до accept |
| Accepted journal | `.ai/v3/journals/V3-*_journal.yaml` | tracked после accept |
| Navigation update | `.ai/v3/V3_navigation.md` | обновляется по lifecycle стадиям, не только после accept |

## 3. Current input policy

До scripted support input не canonicalized полностью.

Сейчас допустимо:

- человек просто хранит ZIP локально;
- Codex/человек делают pre-Kilo package review без staging;
- import-stage позже использует archive link, local archive path или selected repo-local staging fallback;
- `Kilo Notebook V3` получает raw input, а не обязательный handoff.

Сейчас недопустимо считать по умолчанию, что:

- человек обязан класть ZIP в `.ai/v3/staging/inbox/`;
- `.ai/v3/staging/` уже обязательный universal path;
- любой полученный ZIP автоматически перешёл в import lane.

## 3A. Repo-root binding rule

Для `kilo-notebook-v3` все project-relative target paths, journal paths и lifecycle paths должны разрешаться только относительно реального git repo root.

Обязательный preflight:

```text
git rev-parse --show-toplevel
```

Недопустимо:

- выводить target root из local archive path;
- выводить target root из `Downloads` или `Documents`;
- выводить target root только из текущего VS Code workspace, если он не совпадает с git repo root;
- создавать parallel `.ai/` tree вне текущего репозитория.

Если repo root не определяется или не совпадает с intended repository root, import-run обязан остановиться с `blocked`.

## 4. Repo-local staging fallback

Если текущий import-stage явно выбрал repo-local staging fallback, тогда:

- ZIP может быть сохранён в `.ai/v3/staging/`;
- package может быть распакован в `.ai/v3/staging/V3-*/`;
- staging cleanup идёт после accept/reject.

Но это только selected input method, а не default human obligation для pre-Kilo phase.

## 5. Lifecycle archive rule

`V3_navigation.md` должен вести lifecycle/archive по аналогии с `V1` и `V2`.

Минимум:

- запись создаётся на стадии request/prompt;
- обновляется после получения внешнего package;
- обновляется после import-run;
- обновляется после verdict.

Поле `Created Files` в `V3_navigation.md` должно содержать итоговые созданные project files, если import уже был.

## 6. Cleanup

### После accept

- import-lane staging очищается, если использовался;
- accepted journal становится persistent;
- lifecycle entry переводится в `accepted`.

### После reject

- package может быть перенесён в rejected local-only зону;
- imported result не считается accepted;
- lifecycle entry переводится в `rejected`.

## 7. Что нельзя публиковать

Нельзя публиковать по умолчанию:

- raw external ZIP как runtime artifact;
- staging распаковки;
- rejected packages;
- временные drafts.

## Связанные контракты

- [`v3_request_contract.md`](v3_request_contract.md)
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md)
- [`v3_journal_contract.md`](v3_journal_contract.md)
