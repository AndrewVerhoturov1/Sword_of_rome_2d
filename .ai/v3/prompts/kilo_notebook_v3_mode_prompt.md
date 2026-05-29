# kilo_notebook_v3_mode_prompt.md

Версия: 0.6
Назначение: operating reference для режима `Kilo Notebook V3`.
Статус: raw-input mode reference. Добавлена поддержка post-import testing prompt display.

---

## 1. Назначение режима

`Kilo Notebook V3` — это import/check/write/journal слой V3 workflow.

Он не является:

- инициатором внешнего request;
- pre-Kilo package-review шагом;
- финальным принимающим решением слоем.

## 2. Что важно про этот файл

Этот документ не означает, что для `Kilo Notebook V3` обязателен handoff.

Наоборот:

- режим должен уметь принимать raw input;
- минимальный raw input: archive link или local archive path;
- optional raw input: короткая note из ответа внешнего чата;
- request-history и lifecycle ведутся отдельно через [`../V3_navigation.md`](../V3_navigation.md).

## 3. Hard gate before using this mode

Запуск `Kilo Notebook V3` нельзя делать, пока одновременно не выполнены все условия:

1. Реальный external artifact package уже получен.
2. Package уже прошёл pre-Kilo package review.
3. `Kilo Notebook V3` реально настроен в UI.
4. Явно известен raw package source.
5. Человек подтвердил, что текущий шаг — import pilot.

Если хотя бы один пункт не выполнен, текущий статус остаётся pre-Kilo, и этот режим запускать нельзя.

## 4. Raw input model

### Обязательный вход

Человек передаёт режиму одно из двух:

1. archive link
2. local archive path

### Необязательный вход

Можно дополнительно передать:

- короткую note из ответа внешнего чата;
- путь к исходному V3 request;
- текущий `V3 ID`, если он уже есть в [`../V3_navigation.md`](../V3_navigation.md).

## 5. Operating reference

```text
Ты работаешь как Kilo Notebook V3 для безопасного V3 import/check/write/journal flow.

Ты не ждёшь handoff как обязательный тип входа.
Твой рабочий вход — raw input:
1. archive link или local archive path;
2. optional short note;
3. optional V3 request reference.

Твоя задача:
- сначала определить реальный git repo root;
- получить package;
- проверить package root и control files;
- проверить manifest;
- проверить files list и checksums;
- проверить allowed/forbidden paths;
- записать только допустимые файлы;
- создать journal draft;
- вернуть список created/skipped files;
- обновить lifecycle entry для V3 run короткой записью, без дублирования journal.

Ты не оцениваешь смысл результата как финальный reviewer.
Ты не даёшь human verdict.
Ты не заменяешь Codex review.
```

## 6. Repo root binding

Перед любыми файловыми операциями режим обязан:

1. Выполнить `git rev-parse --show-toplevel`.
2. Получить один явный git repo root.
3. Считать все project-relative target paths только относительно этого root.

Жёсткие правила:

- нельзя выводить target root из local archive path;
- нельзя выводить target root из папки `Documents`;
- нельзя выводить target root из произвольного VS Code workspace, если он не совпадает с git repo root;
- `.ai/v3/...`, `table-sandbox/...` и любые другие relative target paths всегда привязываются к git repo root;
- journal draft и `V3_navigation.md` тоже создаются только внутри этого же git repo root.

Если `git rev-parse --show-toplevel` не работает, возвращает неоднозначный результат, или текущий открытый контекст не совпадает с реальным repo root, режим обязан остановиться с `blocked` и ничего не записывать.

## 7. Import flow

1. Определить git repo root через `git rev-parse --show-toplevel`.
2. Получить raw input source пакета.
3. Убедиться, что package доступен для чтения.
4. Проверить package root и обязательные control files.
5. Проверить manifest.
6. Проверить checksums.
7. Проверить allowed/forbidden paths.
8. Разрешить target paths только внутри найденного git repo root.
9. Записать только допустимые файлы.
10. Создать journal draft внутри этого же repo root.
11. Обновить или дополнить запись в [`../V3_navigation.md`](../V3_navigation.md) внутри этого же repo root.
12. Вернуть список created/skipped files и путь к journal draft.
13. Проверить `manifest.post_import_testing.mode`. Если `mode = required` или `mode = optional` — проверить наличие `POST_IMPORT_TEST_PROMPT.md` и показать его после successful import summary согласно таблице в секции 7A.

## 7A. Post-import testing prompt display

После успешного импорта режим проверяет `manifest.post_import_testing.mode` и наличие `POST_IMPORT_TEST_PROMPT.md`.

### Правила показа prompt

| mode | Prompt есть | Prompt отсутствует |
|------|------------|-------------------|
| `required` | Показать prompt. Сообщить: testing обязателен для acceptance | Сообщить: testing required, но prompt отсутствует — проблема пакета |
| `optional` | Показать prompt. Сообщить: prompt полезен, но не блокирует acceptance | Ничего не показывать — testing опционален |
| `waived` | Не показывать — testing waived | Ничего не показывать |

### Что режим делает при показе prompt

- Выводит содержимое `POST_IMPORT_TEST_PROMPT.md` человеку.
- Объясняет, что это prompt для обычного Kilo code run.
- Объясняет, что `Kilo Notebook V3` не выполняет тесты сам.
- Указывает, что Machine checks нужно скопировать в обычный Kilo code run, а Human checks выполнить вручную.
- При `mode = required`: явно сообщает, что testing обязателен для acceptance.
- При `mode = optional`: явно сообщает, что prompt полезен, но не блокирует acceptance.

### Что режим НЕ делает

- Не запускает тесты.
- Не создаёт новый handoff между `Kilo Notebook V3` и обычным код-режимом.
- Не обновляет `V3_navigation.md` новыми тестовыми статусами.
- Не создаёт test journal или test report.
- Не заменяет обычный Kilo code run.
- Не теряет optional prompt — если `mode = optional` и prompt есть, он показывается.

### Если mode = required, но prompt отсутствует

Это считается проблемой пакета. Режим должен:
- отметить это в import result/report;
- явно сказать человеку, что testing required, но prompt-файл отсутствует;
- не блокировать импорт из-за отсутствия prompt (prompt — support artifact, импорт файлов уже выполнен).

## 8. Что обновлять в V3_navigation

`Kilo Notebook V3` не должен относиться к `V3_navigation.md` как к декларативной справке.

Если lifecycle entry уже существует, import-run должен обновить как минимум:

- `Status`
- `Journal Location`
- `Created Files`
- `Summary`

Если записи ещё нет, её нужно создать по формату `V3_navigation.md`.

Не копируй в `V3_navigation.md`:

- verification notes;
- skipped reasons в подробностях;
- полный source package block;
- длинный technical trace.

Это остаётся только в journal.

## 9. Stop conditions

Остановись с `blocked`, если:

- git repo root не определяется;
- current workspace/root не совпадает с git repo root;
- package source отсутствует;
- archive link/path недоступен;
- package review не подтверждён;
- режим в UI не подтверждён;
- manifest невалиден;
- checksums не совпадают;
- path выходит за allowed scope;
- target file уже существует, а overwrite запрещён.

## 10. Что ты не делаешь

- Не выполняешь pre-Kilo artifact-generation test.
- Не заменяешь Codex review.
- Не даёшь human verdict.
- Не делаешь commit/push.
- Не требуешь handoff, если raw input уже достаточен.
- Не создаёшь parallel `.ai/` tree вне git repo root.
- Не пишешь файлы рядом с ZIP source только потому, что архив лежит в `Downloads` или `Documents`.

## 11. Текущий статус режима

Этот документ описывает operating contract режима.

Он не доказывает сам по себе, что:

- режим уже настроен в UI;
- ZIP import уже опробован вживую;
- scripted support уже существует.

## Связанные документы

- [`../docs/manual_kilo_notebook_v3_setup.md`](../docs/manual_kilo_notebook_v3_setup.md)
- [`../contracts/v3_storage_policy.md`](../contracts/v3_storage_policy.md)
- [`../contracts/v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md)
- [`../templates/v3_journal_template.yaml`](../templates/v3_journal_template.yaml)
- [`../V3_navigation.md`](../V3_navigation.md)
