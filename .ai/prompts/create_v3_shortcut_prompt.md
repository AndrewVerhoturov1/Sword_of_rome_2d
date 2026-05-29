# Шаблон: Подготовка V3 Import Entry через /v3 Shortcut

**Этот шаблон обязателен для каждого `/v3` shortcut.** При явном shortcut `/v3` Codex **обязан** использовать этот шаблон. Prompt, написанный вручную без шаблона, не считается готовым `/v3` prompt-ом и не должен выдаваться пользователю.

Используй этот шаблон, когда человек вызвал `/v3` (или `/V3`, `/в3`, `/В3`) — import-entry route для V3 artifact package.

**Codex не инициирует `/v3` самостоятельно.** Шаблон используется только после явного shortcut-вызова человеком. Без такого вызова Codex не готовит `/v3` prompt и не предлагает его по собственной инициативе.

## Что такое /v3

`/v3` — это explicit repo-level entry mode, а не новый `Kilo mode` и не новый `Agent kind`. Это import-entry route: у человека уже есть V3 package source, и он хочет пройти V3 import route через [`Kilo Notebook V3`](../rules/kilo_mode_contract.md).

`/v3` только подготавливает правильный runtime entry для V3 import path. Сам импорт выполняет `Kilo Notebook V3`.

### Что /v3 НЕ делает

- Не подменяет `/v1` или `/r1`.
- Не создаёт внешний V3 request вместо import entry.
- Не обходит `Kilo Notebook V3`.
- Не обходит [`scripts/v3/validate_v3_package.py`](../../scripts/v3/validate_v3_package.py) и [`scripts/v3/stage_v3_package.py`](../../scripts/v3/stage_v3_package.py).
- Не делает direct repo apply из Codex.
- Не является auto-import кнопкой.
- Не является shortcut для external request generation.

## Required Authoring Rules

Codex обязан соблюдать эти правила при работе с `/v3`:

1. **Сначала проверить, что package source уже существует.** Если человек вызвал `/v3`, но package source ещё не предоставлен — запросить package source.
2. **Не придумывать package source.** Если человек не дал archive link или local archive path, спросить.
3. **Выводить launch package для `Kilo Notebook V3`, а не для другого mode.**
4. **Указывать repo root discipline:** все relative target paths разрешаются только от `git rev-parse --show-toplevel`.
5. **Упоминать helper scripts как scripted support:** [`validate_v3_package.py`](../../scripts/v3/validate_v3_package.py) и [`stage_v3_package.py`](../../scripts/v3/stage_v3_package.py).
6. **Не обещать auto-apply.** `apply_v3_package.py` не существует и не планируется.
7. **После import ожидать:** tester prompt file (если `post_import_testing` ≠ `waived`), machine-check report, Codex review, human verdict.
8. **Не путать `/v3` с `/v1` или `/r1`.** `/v3` — только import-entry, не prompt-only external question и не full published-artifact route.

## `/v3` Preflight Checklist

До выдачи готового `/v3` launch package пользователю Codex выполняет `/v3` preflight-checklist:

- [ ] Человек явно вызвал `/v3`, `/V3`, `/в3` или `/В3`.
- [ ] Package source подтверждён: archive link или local archive path.
- [ ] Package source реально существует (для local path — файл есть на диске).
- [ ] Launch package target = `Kilo Notebook V3`, не другой mode.
- [ ] Launch package содержит ссылку на [`kilo_notebook_v3_mode_prompt.md`](../v3/prompts/kilo_notebook_v3_mode_prompt.md) как operating reference.
- [ ] Launch package явно требует repo root detection через `git rev-parse --show-toplevel`.
- [ ] Launch package не обещает auto-apply.
- [ ] Launch package упоминает post-import testing flow (если применимо).
- [ ] Codex не пытается сделать import сам (agent-first: import идёт через `Kilo Notebook V3`).

Если любой пункт preflight-checklist не выполнен, `/v3` launch package не считается готовым. Codex обязан довести package до соответствия checklist перед выдачей пользователю.

## Required Inputs

Для подготовки `/v3` launch package Codex должен получить от человека или определить сам:

| Поле | Описание | Обязательность |
|------|----------|---------------|
| Package source | Archive link (URL) или local archive path (.zip) | Обязательно |
| V3 ID | Идентификатор V3-цикла, если уже известен | Опционально (если package уже содержит manifest) |
| Scope notes | Ограничения: что не импортировать, особые условия | Опционально |

## Launch Package Template

Ниже — скелет launch package для `Kilo Notebook V3`. Codex заполняет поля `{{...}}` и отдаёт готовый launch package человеку для копирования в `Kilo Notebook V3`.

```text
## Kilo mode

- Kilo mode: Kilo Notebook V3
- Task role: Notebook Agent
- Mode switching: запрещён

## Package Source

{{Package Source}}

## Pre-import Validation

Перед импортом выполни:
1. `python scripts/v3/validate_v3_package.py --package "{{Package Path}}"`
2. Если validation passed: `python scripts/v3/stage_v3_package.py --package "{{Package Path}}"`

## Operating Reference

Следуй `.ai/v3/prompts/kilo_notebook_v3_mode_prompt.md`.

## Repo Root Discipline

Перед любыми файловыми операциями выполни:
```
git rev-parse --show-toplevel
```
Все relative target paths разрешай только от найденного repo root.

## Safety Boundaries

- Validate, stage, затем import.
- Пиши только разрешённые файлы из manifest.
- Не перезаписывай существующие файлы без явного разрешения.
- Создай journal draft через `python scripts/v3/write_v3_journal.py`.
- Обнови `V3_navigation.md` согласно [`kilo_notebook_v3_mode_prompt.md`](../v3/prompts/kilo_notebook_v3_mode_prompt.md), секция 8.
- Auto-apply запрещён.

## Post-Import

- Если manifest содержит `post_import_testing: required` или `optional` с `POST_IMPORT_TEST_PROMPT.md`, notebook обязан auto-emit tester prompt.
- Верни путь к tester prompt file и путь к journal draft.
- Не делай commit и не делай push.

## Allowed Writes

Только файлы, перечисленные в manifest (секция `files`), плюс:
- `.ai/v3/staging/<V3-ID>/` (staging zone)
- `.ai/v3/journals/drafts/<V3-ID>_journal.yaml` (journal draft)
- `.ai/v3/V3_navigation.md` (lifecycle entry update)
- `.ai/v3/test_prompts/<V3-ID>_post_import_test_prompt.md` (canonical tester prompt copy)
```

### Правила заполнения подстановочных полей

| Поле | Что вставлять |
|------|--------------|
| `{{Package Source}}` | Archive link (URL) или local archive path. Если URL — полная ссылка. Если local path — абсолютный путь к .zip файлу. |
| `{{Package Path}}` | Тот же путь/URL, что и Package Source, в формате, пригодном для передачи в CLI. |

## Что Codex НЕ должен делать

При работе с `/v3` Codex **не должен**:

1. **Пытаться сделать import сам.** Import идёт только через `Kilo Notebook V3`. Codex готовит launch package, но не выполняет import.
2. **Создавать handoff для `/v3`.** `/v3` — это entry mode, который готовит launch package, а не handoff.
3. **Подменять `/v3` на `/v1` или `/r1`.** Если человек явно вызвал `/v3`, нельзя молча переключить на другой shortcut.
4. **Обещать, что import пройдёт без pre-Kilo review.** Package должен быть проверен до import-stage.
5. **Обходить `Kilo Notebook V3`.** Нельзя предлагать «я сам распакую и запишу файлы».
6. **Смешивать `/v3` с external request generation.** `/v3` — это import-entry для уже существующего package, а не создание нового V3 request для внешнего чата.

## Когда `/v3` не подходит

`/v3` не подходит, если:

- Package source ещё не существует → сначала нужен внешний V3 request (обычный Codex flow, не shortcut).
- Нужен prompt-only внешний вопрос → используй `/v1`.
- Нужен full published-artifact route → используй `/r1`.
- Нужен V2 external senior review → используй `/v2` protocol.

## Связанные документы

- [`.ai/v3/README.md`](../v3/README.md) — V3 workflow layer.
- [`.ai/v3/prompts/kilo_notebook_v3_mode_prompt.md`](../v3/prompts/kilo_notebook_v3_mode_prompt.md) — operating reference для `Kilo Notebook V3`.
- [`.ai/v3/docs/manual_kilo_notebook_v3_setup.md`](../v3/docs/manual_kilo_notebook_v3_setup.md) — ручная настройка режима.
- [`scripts/v3/README.md`](../../scripts/v3/README.md) — scripted support helpers.
- [`.ai/plans/master/v3_workflow_implementation_plan.md`](../plans/master/v3_workflow_implementation_plan.md) — план внедрения V3.
