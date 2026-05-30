# V3 Artifact-Producing Workflow Contract

Версия: 0.1 draft  
Назначение: описать V3-процесс для внешних ChatGPT-сессий, которые создают реальные проектные артефакты для GitHub-репозитория.  
Язык документа: русский.  
Статус: проектный рабочий контракт, предназначенный для внедрения и дальнейшей доработки.

---

## 1. Короткая суть V3

V3 — это процесс, в котором внешний ChatGPT, например модель 5.5, используется не только как советчик или ревьюер, а как **генератор готовых файлов** для реального проекта.

Он получает:

- контекст проекта;
- правила работы;
- границы допустимых изменений;
- конкретную задачу;
- формат ожидаемого результата;
- метаданные V3-запроса.

После этого внешний ChatGPT создаёт **artifact package** — пакет артефактов. Предпочтительный формат пакета — ZIP-архив со строгой внутренней структурой:

```text
V3-YYYYMMDD-HHMMSS-<slug>/
  manifest.yaml
  README_FOR_KILO.md
  README_FOR_CODEX.md
  checksums.sha256
  files/
    ...готовые файлы проекта...
```

Человек скачивает ZIP и передаёт его в KiloCode Notebook V3 вместе с исходным V3-запросом и ответом ChatGPT.

KiloCode Notebook V3:

- принимает ZIP;
- распаковывает его в staging-зону;
- проверяет manifest;
- проверяет пути;
- проверяет хэши;
- создаёт или обновляет только явно разрешённые файлы;
- записывает факт операции в journal.

Codex:

- читает journal;
- проверяет реально созданные файлы;
- сверяет их с задачей;
- проверяет риски;
- просит человека вручную проверить важные места;
- принимает изменения или просит доработку.

Человек остаётся финальным владельцем решения.

Ключевая идея V3:

> Внешняя мощная модель создаёт готовые проектные файлы, но не получает прямого доступа к репозиторию. Все записи проходят через KiloCode, журналируются и проверяются Codex и человеком.

---

## 2. Чем V3 отличается от V1 и V2

### 2.1. V1

V1 — это внешний prompt-only разбор.

Модель получает контекст и вопрос. Она возвращает:

- мнение;
- анализ;
- план;
- критику;
- предложения;
- риски.

V1 не создаёт реальные файлы для вставки в проект. Он полезен для мышления, архитектуры, внешнего взгляда и обсуждения.

### 2.2. V2

V2 — это bounded technical review.

Модель получает зафиксированный snapshot реального кода и конкретную задачу на проверку. Она должна:

- читать только заданные источники;
- честно отделять подтверждённое от неподтверждённого;
- проверять конкретный участок кода;
- давать bounded review;
- не фантазировать о локальном доступе;
- не писать, что она что-то изменила, если она ничего не изменила.

V2 ближе к инженерному ревью, но в основном остаётся текстовым процессом.

### 2.3. V3

V3 — это artifact-producing workflow.

Модель не просто говорит, что нужно сделать, а подготавливает:

- файлы документации;
- инструкции;
- схемы данных;
- скрипты;
- тестовые fixtures;
- шаблоны;
- код;
- migration notes;
- checklists;
- request templates;
- review templates.

Но модель не утверждает, что записала их в репозиторий. Она только создаёт пакет.

Запись в репозиторий выполняет KiloCode Notebook V3. Проверку выполняет Codex. Финальное принятие делает человек.

---

## 3. Главный принцип V3

V3 не должен быть хаотичным способом «попросить ChatGPT написать код и потом как-нибудь вставить».

V3 должен быть управляемым конвейером:

```text
Codex / человек
  ↓
готовит V3 request
  ↓
ChatGPT 5.5
  ↓
создаёт V3 artifact package ZIP
  ↓
человек скачивает ZIP
  ↓
KiloCode Notebook V3
  ↓
распаковывает, проверяет, записывает в staging / project files
  ↓
пишет journal
  ↓
Codex
  ↓
проверяет journal и реальные файлы
  ↓
человек
  ↓
принимает / отклоняет / отправляет на доработку
```

Главный принцип:

> ChatGPT создаёт артефакты. KiloCode физически пишет файлы. Codex проверяет. Человек принимает.

---

## 4. Роли участников

### 4.1. Human

Человек — владелец решения.

Он:

- формулирует намерение;
- подтверждает, что V3-задача действительно нужна;
- переносит V3-запрос во внешний ChatGPT;
- скачивает ZIP;
- передаёт ZIP в KiloCode Notebook V3;
- смотрит результат;
- принимает или отклоняет изменения;
- решает спорные моменты.

Человек не обязан вручную раскладывать файлы из ZIP. Это задача KiloCode. Но человек должен понимать, какие изменения предлагаются.

### 4.2. Codex

Codex — постановщик, проверяющий и контролёр качества.

Codex должен:

- помогать подготовить V3 request package;
- определить цель задачи;
- определить допустимые пути записи;
- определить запрещённые зоны;
- указать критерии приёмки;
- после выполнения читать journal;
- проверять реальные файлы;
- указывать человеку, что именно нужно проверить вручную;
- принимать, отклонять или просить доработку.

Codex не должен молча доверять ZIP-архиву.

Codex не должен считать, что файл существует только потому, что ChatGPT написал его в ответе. Источник факта создания файла — journal KiloCode и реальное состояние рабочей копии.

### 4.3. ChatGPT 5.5 external

Внешний ChatGPT — генератор артефактов.

Он должен:

- читать V3 request;
- соблюдать правила проекта;
- не выходить за границы allowed paths;
- создавать ZIP-пакет;
- включать manifest;
- включать инструкции для KiloCode;
- включать инструкции для Codex;
- включать checksums;
- честно указывать, какие файлы должны быть созданы или обновлены;
- не писать, что он уже изменил репозиторий.

Он не должен:

- утверждать, что записал файлы в GitHub;
- подменять journal;
- скрывать файлы в ZIP;
- создавать файлы вне manifest;
- добавлять неожиданные бинарные файлы;
- менять запрещённые зоны;
- смешивать planned architecture с уже реализованным product code.

### 4.4. KiloCode Notebook V3

KiloCode Notebook V3 — файловый оператор.

Он должен:

- принять ZIP;
- принять исходный V3 prompt/request;
- принять ответ ChatGPT;
- распаковать ZIP в staging;
- прочитать manifest;
- проверить, что все файлы из ZIP перечислены в manifest;
- проверить, что все пути безопасны;
- проверить allowed paths и forbidden paths;
- проверить контрольные суммы;
- записать файлы в staging или целевые места по режиму задачи;
- не писать ничего лишнего;
- не перезаписывать существующие файлы без явного разрешения;
- создать journal entry;
- передать статус на проверку Codex.

KiloCode не должен быть главным смысловым инициатором V3. Он может помогать собрать технический контекст, но его основная роль — безопасная запись и журналирование.

---

## 5. Почему ZIP-формат предпочтителен

ZIP лучше, чем простая вставка файлов в чат, потому что:

- сохраняет вложенную структуру папок;
- снижает риск поломки форматирования;
- позволяет передать много файлов сразу;
- удобен для автоматической обработки;
- позволяет проверять хэши;
- упрощает staging;
- позволяет хранить полный пакет как исходный артефакт.

Но ZIP не должен быть единственным источником правды.

ZIP обязательно должен содержать manifest. KiloCode должен доверять не архиву как таковому, а связке:

```text
ZIP + manifest + checksums + allowed paths + journal
```

Если в ZIP лежит файл, которого нет в manifest, он должен быть заблокирован или проигнорирован.

Если manifest говорит одно, а содержимое ZIP другое, импорт должен остановиться.

---

## 6. Внутренняя структура V3 ZIP

Рекомендуемая структура:

```text
V3-YYYYMMDD-HHMMSS-<short-task-slug>/
  manifest.yaml
  README_FOR_KILO.md
  README_FOR_CODEX.md
  checksums.sha256
  files/
    <project-relative-path-1>
    <project-relative-path-2>
    <project-relative-path-3>
```

Пример:

```text
V3-20260527-153000-v3-contract/
  manifest.yaml
  README_FOR_KILO.md
  README_FOR_CODEX.md
  checksums.sha256
  files/
    .ai/v3/V3_process_contract.md
    .ai/v3/V3_artifact_packet_schema.md
    .ai/v3/V3_journal_schema.md
    scripts/v3/validate-v3-package.mjs
```

### 6.1. manifest.yaml

Главный файл пакета.

Он описывает:

- V3 ID;
- название задачи;
- тип пакета;
- кто создал пакет;
- какие файлы входят;
- куда они должны попасть;
- какие действия требуются;
- какие пути разрешены;
- какие пути запрещены;
- какие проверки обязательны;
- какие риски известны;
- требуется ли review Codex;
- требуется ли ручная проверка человеком.

### 6.2. README_FOR_KILO.md

Инструкция для KiloCode Notebook V3.

Она должна объяснять:

- как распаковывать пакет;
- какой режим записи использовать;
- какие пути разрешены;
- что делать при конфликте;
- что делать при несовпадении хэша;
- что писать в journal;
- когда остановиться.

### 6.3. README_FOR_CODEX.md

Инструкция для Codex.

Она должна объяснять:

- зачем создан пакет;
- какие файлы ожидаются;
- какую задачу они решают;
- какие критерии приёмки;
- какие места проверить особенно внимательно;
- какие ручные проверки попросить у человека;
- какие признаки должны привести к отклонению.

### 6.4. checksums.sha256

Файл с контрольными суммами.

Он нужен, чтобы KiloCode мог убедиться, что файлы не были повреждены или подменены после генерации.

Формат может быть обычным:

```text
<sha256>  files/.ai/v3/V3_process_contract.md
<sha256>  files/scripts/v3/validate-v3-package.mjs
```

### 6.5. files/

Папка с реальными проектными файлами.

Внутри `files/` должна быть структура, повторяющая project-relative paths.

Например, если файл должен попасть в:

```text
.ai/v3/V3_process_contract.md
```

то в ZIP он должен лежать как:

```text
files/.ai/v3/V3_process_contract.md
```

---

## 7. Пример manifest.yaml

```yaml
v3_id: "V3-20260527-153000-v3-contract"
task_title: "Create V3 artifact-producing workflow contract"
generated_by: "external_chatgpt_5_5"
artifact_format: "zip"
package_version: "0.1"

source_request:
  request_id: "V3-20260527-153000"
  prepared_by: "codex"
  human_requested: true

write_policy:
  mode: "staging_first"
  require_codex_review: true
  require_human_review: true
  allow_overwrite: false

allowed_paths:
  - ".ai/v3/"
  - "docs/v3/"
  - "scripts/v3/"

forbidden_paths:
  - ".git/"
  - "node_modules/"
  - "dist/"
  - "build/"
  - "coverage/"
  - "package-lock.json"
  - "pnpm-lock.yaml"
  - "yarn.lock"
  - "src/"

files:
  - path: ".ai/v3/V3_process_contract.md"
    source_in_zip: "files/.ai/v3/V3_process_contract.md"
    action: "create"
    required: true
    sha256: "REPLACE_WITH_SHA256"
    purpose: "Main V3 process contract and implementation explanation."

  - path: ".ai/v3/V3_artifact_packet_schema.md"
    source_in_zip: "files/.ai/v3/V3_artifact_packet_schema.md"
    action: "create"
    required: true
    sha256: "REPLACE_WITH_SHA256"
    purpose: "Schema and rules for V3 ZIP artifact packages."

  - path: "scripts/v3/validate-v3-package.mjs"
    source_in_zip: "files/scripts/v3/validate-v3-package.mjs"
    action: "create"
    required: true
    sha256: "REPLACE_WITH_SHA256"
    purpose: "Local validator for V3 package structure."

acceptance_criteria:
  - "All files listed in manifest exist in the ZIP under files/."
  - "No extra files are present under files/ unless explicitly listed in manifest."
  - "All target paths are project-relative and inside allowed_paths."
  - "No target path matches forbidden_paths."
  - "All sha256 checksums match."
  - "KiloCode journal entry is created after import."
  - "Codex review is required before final acceptance."

known_risks:
  - "Generated files may describe intended process but not yet be wired into existing project automation."
  - "Scripts must be reviewed before being executed."
  - "Documentation must not claim that V3 is already fully implemented unless it is."

human_review_required:
  - "Confirm that the created V3 contract matches the intended workflow."
  - "Confirm whether generated scripts may be committed or should remain drafts."
```

---

## 8. V3 request package

Перед тем как внешний ChatGPT создаст ZIP, ему нужно дать V3 request.

V3 request — это не просто обычный prompt. Это структурированная постановка задачи.

Он должен включать:

- V3 ID;
- цель;
- контекст проекта;
- ссылки или выдержки из правил;
- текущие ограничения;
- allowed paths;
- forbidden paths;
- ожидаемый формат ZIP;
- список желаемых файлов;
- критерии приёмки;
- требования к честности;
- указание, что модель не имеет доступа к репозиторию;
- указание, что она должна создать пакет, а не утверждать, что уже изменила проект.

### 8.1. Пример V3 request

```text
V3 ID: V3-20260527-153000-v3-contract

You are participating in a V3 artifact-producing workflow.

This is not a prompt-only review. Your task is to produce a ZIP artifact package containing real files intended for a GitHub repository.

You do not have direct repository write access. Do not claim that you changed the repository.

You must create a package with this structure:

V3-20260527-153000-v3-contract/
  manifest.yaml
  README_FOR_KILO.md
  README_FOR_CODEX.md
  checksums.sha256
  files/
    ...project-relative files...

Project goal:
...

Task:
Create the first draft of the V3 workflow contract and implementation notes.

Allowed target paths:
- .ai/v3/
- docs/v3/
- scripts/v3/

Forbidden target paths:
- .git/
- node_modules/
- dist/
- build/
- src/
- package-lock.json

Required files:
- .ai/v3/V3_process_contract.md
- .ai/v3/V3_artifact_packet_schema.md
- .ai/v3/V3_journal_schema.md
- .ai/v3/V3_codex_review_checklist.md

Rules:
- Do not include files not listed in manifest.
- Every file under files/ must be listed in manifest.
- Every listed file must have purpose and sha256.
- Include README_FOR_KILO.md.
- Include README_FOR_CODEX.md.
- Include checksums.sha256.
- Do not claim repository changes were applied.
```

---

## 9. Жизненный цикл V3-задачи

### 9.1. Статусы

Рекомендуемые статусы:

```text
draft_requested
request_prepared
external_generation_pending
artifact_generated
artifact_received_by_human
kilo_import_pending
kilo_validation_failed
kilo_files_staged
kilo_files_written
journal_written
codex_review_pending
codex_review_passed
codex_review_failed
human_review_pending
accepted
needs_revision
rejected
superseded
```

### 9.2. Описание статусов

`draft_requested` — человек решил, что нужна V3-задача.

`request_prepared` — Codex подготовил структурированный V3 request.

`external_generation_pending` — request передан во внешний ChatGPT, ожидается artifact package.

`artifact_generated` — ChatGPT создал ZIP и сопроводительный ответ.

`artifact_received_by_human` — человек скачал ZIP.

`kilo_import_pending` — ZIP передан в KiloCode Notebook V3, импорт ещё не завершён.

`kilo_validation_failed` — KiloCode обнаружил проблему: путь, хэш, лишний файл, конфликт, неправильный manifest.

`kilo_files_staged` — файлы распакованы в staging, но ещё не применены в целевые места.

`kilo_files_written` — KiloCode записал файлы в разрешённые целевые места.

`journal_written` — создана journal-запись о фактических действиях.

`codex_review_pending` — Codex должен проверить journal и файлы.

`codex_review_passed` — Codex не нашёл блокирующих проблем.

`codex_review_failed` — Codex нашёл блокирующие проблемы.

`human_review_pending` — требуется ручная проверка человеком.

`accepted` — задача принята.

`needs_revision` — нужны правки.

`rejected` — пакет отклонён.

`superseded` — пакет заменён более новой V3-задачей.

---

## 10. Journal V3

Journal — это источник правды о том, что KiloCode реально сделал с файлами.

Внешний ChatGPT не может писать journal за KiloCode. Он может только предложить ожидаемый формат.

Journal должен фиксировать:

- V3 ID;
- время импорта;
- путь к исходному ZIP;
- хэш ZIP;
- путь к распакованному staging;
- список файлов из manifest;
- список реально записанных файлов;
- список пропущенных файлов;
- конфликты;
- ошибки;
- итоговый статус;
- ссылку на исходный request;
- ссылку на ответ внешнего ChatGPT;
- кто запустил импорт;
- требуется ли Codex review;
- требуется ли human review.

### 10.1. Пример journal entry

```yaml
journal_entry_id: "V3J-20260527-160245-v3-contract"
v3_id: "V3-20260527-153000-v3-contract"
status: "kilo_files_written"
created_at: "2026-05-27T16:02:45+02:00"
created_by: "kilocode-notebook-v3"

source:
  zip_path: "_local/v3/inbox/V3-20260527-153000-v3-contract.zip"
  zip_sha256: "REPLACE_WITH_ZIP_SHA256"
  request_path: ".ai/v3/requests/V3-20260527-153000-v3-contract.md"
  external_response_path: ".ai/v3/responses/V3-20260527-153000-v3-contract.md"

staging:
  path: ".ai/v3/staging/V3-20260527-153000-v3-contract/"
  created: true

validation:
  manifest_found: true
  checksums_found: true
  all_manifest_files_found: true
  no_extra_files: true
  paths_safe: true
  checksums_match: true
  overwrite_conflicts: false

written_files:
  - path: ".ai/v3/V3_process_contract.md"
    action: "create"
    sha256: "REPLACE_WITH_SHA256"
    result: "written"

  - path: ".ai/v3/V3_artifact_packet_schema.md"
    action: "create"
    sha256: "REPLACE_WITH_SHA256"
    result: "written"

skipped_files: []
errors: []

review:
  codex_review_required: true
  human_review_required: true
  codex_status: "pending"
  human_status: "pending"
```

---

## 11. Staging-first режим

По умолчанию V3 должен работать в режиме `staging_first`.

Это значит:

1. KiloCode распаковывает ZIP в staging-папку.
2. Проверяет структуру и manifest.
3. Проверяет хэши.
4. Проверяет пути.
5. Только после этого переносит файлы в целевые места или оставляет их в staging до подтверждения.

Рекомендуемая staging-папка:

```text
.ai/v3/staging/<v3_id>/
```

Исходные ZIP можно хранить локально, например:

```text
_local/v3/inbox/<v3_id>.zip
```

Если `_local/` не должен попадать в публичный репозиторий, это нужно явно закрепить в правилах.

---

## 12. Allowed paths и forbidden paths

V3 обязательно должен работать с явными границами.

### 12.1. Allowed paths

Allowed paths — это места, куда V3-пакет имеет право предлагать запись.

Примеры безопасных стартовых зон:

```text
.ai/v3/
docs/v3/
scripts/v3/
canon/drafts/
examples/
```

Для первых V3-задач лучше не разрешать запись в продуктовый код.

### 12.2. Forbidden paths

Forbidden paths — это места, куда V3-пакет не имеет права писать.

Минимальный список:

```text
.git/
node_modules/
dist/
build/
coverage/
.cache/
.env
.env.local
.env.production
package-lock.json
pnpm-lock.yaml
yarn.lock
```

На раннем этапе также желательно запретить:

```text
src/
public/
package.json
tsconfig.json
vite.config.ts
```

Потом можно точечно разрешать части product-code, но только после того, как V3-инфраструктура станет надёжной.

---

## 13. Политика перезаписи файлов

По умолчанию V3 не должен перезаписывать существующие файлы.

В manifest у каждого файла должно быть поле `action`:

```text
create
update
replace
delete
```

На раннем этапе лучше разрешить только:

```text
create
```

`update` можно разрешать позже, но только при наличии:

- описания причины;
- ожидаемого diff;
- старого пути;
- нового содержания;
- критериев проверки;
- Codex review;
- human review.

`replace` и `delete` должны считаться опасными действиями. Их нельзя выполнять без явного подтверждения человека.

---

## 14. Проверки KiloCode Notebook V3

Перед записью файлов KiloCode должен выполнить проверки.

### 14.1. Проверка структуры ZIP

Проверить:

- есть ровно одна корневая папка пакета;
- есть `manifest.yaml`;
- есть `README_FOR_KILO.md`;
- есть `README_FOR_CODEX.md`;
- есть `checksums.sha256`;
- есть `files/`;
- нет неожиданных системных файлов, например `__MACOSX/`, `.DS_Store`.

### 14.2. Проверка manifest

Проверить:

- manifest валиден как YAML;
- есть `v3_id`;
- есть `task_title`;
- есть `files`;
- каждый файл имеет `path`, `source_in_zip`, `action`, `sha256`, `purpose`;
- `path` является project-relative;
- `path` не абсолютный;
- `path` не содержит `..`;
- `path` не выходит за allowed paths;
- `path` не попадает в forbidden paths.

### 14.3. Проверка файлов

Проверить:

- каждый `source_in_zip` существует;
- каждый файл под `files/` указан в manifest;
- нет лишних файлов;
- хэши совпадают;
- размер файлов разумный;
- бинарные файлы запрещены, если не разрешены явно;
- кодовые файлы не содержат очевидных опасных команд.

### 14.4. Проверка конфликтов

Проверить:

- существует ли целевой файл;
- разрешено ли действие `create`, если файл уже существует;
- разрешено ли действие `update`, если файл отсутствует;
- нужно ли остановить импорт.

### 14.5. Проверка результата

После записи:

- перечитать записанные файлы;
- снова посчитать хэши;
- сравнить с manifest;
- записать journal.

---

## 15. Проверки Codex

Codex проверяет не обещания внешнего ChatGPT, а фактические файлы и journal.

Codex должен проверить:

1. Есть ли journal entry.
2. Совпадает ли V3 ID.
3. Все ли файлы из manifest реально записаны.
4. Нет ли лишних файлов.
5. Не были ли затронуты запрещённые пути.
6. Соответствует ли содержимое задаче.
7. Нет ли неподтверждённых утверждений.
8. Нет ли смешения planned architecture и уже реализованного product code.
9. Нет ли опасных скриптов.
10. Не нужно ли сначала оставить результат как draft.
11. Что должен проверить человек.

Codex verdict должен быть явным:

```text
pass
pass_with_notes
needs_revision
fail
```

### 15.1. Пример Codex review verdict

```yaml
v3_id: "V3-20260527-153000-v3-contract"
reviewed_by: "codex"
status: "pass_with_notes"

checked:
  journal_present: true
  files_exist: true
  no_forbidden_paths: true
  manifest_matches_files: true
  content_matches_task: true
  scripts_safe_to_read: true
  scripts_safe_to_run: false

notes:
  - "Documentation is acceptable as first draft."
  - "Generated scripts should not be executed until manually reviewed."

human_review_required:
  - "Confirm whether .ai/v3/ should be public repo context or local-only context."
  - "Confirm whether scripts/v3/ should be committed now or kept as draft."

verdict: "pass_with_notes"
```

---

## 16. Что должен проверять человек

Человек не должен вручную выполнять всю работу Codex, но он должен проверить смысл.

Минимальная ручная проверка:

- соответствует ли результат изначальной задумке;
- не создал ли ChatGPT лишнюю концепцию;
- не усложнил ли процесс сверх необходимости;
- не положил ли файлы не туда;
- не появились ли спорные формулировки;
- можно ли это принимать в проект;
- нужно ли отправить на доработку.

Для документации человек проверяет смысл и тон.

Для скриптов человек должен быть осторожнее: скрипты нельзя запускать только потому, что они сгенерированы. Их должен проверить Codex, а при необходимости и человек.

---

## 17. Безопасность V3

V3 добавляет мощный путь внесения файлов в проект. Поэтому нужны ограничения.

### 17.1. Нельзя доверять ZIP без проверки

ZIP может содержать:

- лишние файлы;
- неправильные пути;
- скрытые системные файлы;
- бинарные вложения;
- попытку записи за пределы проекта;
- неожиданные изменения.

Поэтому KiloCode должен импортировать только manifest-listed файлы.

### 17.2. Нельзя исполнять сгенерированные скрипты автоматически

Скрипты из V3-пакета можно записать как файлы, но нельзя сразу запускать без review.

Особенно опасны:

- shell-скрипты;
- Node.js-скрипты с файловыми операциями;
- команды удаления;
- команды установки пакетов;
- сетевые запросы;
- изменение git history;
- работа с токенами;
- работа с `.env`.

### 17.3. Нельзя писать секреты

V3-пакет не должен содержать:

- токены;
- ключи API;
- пароли;
- private SSH keys;
- `.env`;
- реальные персональные данные;
- приватные локальные пути, если они не нужны.

### 17.4. Нельзя смешивать уровни зрелости

Документация должна честно различать:

- уже реализовано;
- planned;
- draft;
- proposal;
- experimental;
- local-only;
- public context.

Это особенно важно для проектов, где есть большой архитектурный слой и не всё из него уже реализовано в product-code.

### 17.5. Нельзя обходить Codex review

Даже если пакет кажется простым, journal должен идти на проверку.

Codex review — обязательный gate.

Human review — финальный gate.

---

## 18. Рекомендуемые первые V3-задачи

Не стоит начинать V3 сразу с боевого product-code.

Лучшие первые задачи:

```text
.ai/v3/V3_process_contract.md
.ai/v3/V3_artifact_packet_schema.md
.ai/v3/V3_journal_schema.md
.ai/v3/V3_codex_review_checklist.md
.ai/v3/V3_kilo_import_checklist.md
scripts/v3/validate-v3-package.mjs
docs/v3/V3_quickstart.md
```

После этого можно переходить к:

- генерации схем JSON;
- генерации fixtures;
- генерации dev-only scripts;
- генерации документации по архитектуре;
- генерации тестовых примеров;
- генерации миграционных планов.

Только потом — к product-code.

---

## 19. Рекомендуемая структура V3 в репозитории

Возможная структура:

```text
.ai/v3/
  V3_process_contract.md
  V3_artifact_packet_schema.md
  V3_journal_schema.md
  V3_codex_review_checklist.md
  V3_kilo_import_checklist.md
  requests/
    V3-....md
  responses/
    V3-....md
  journals/
    V3J-....yaml
  reviews/
    V3R-....yaml
  staging/
    V3-....

docs/v3/
  V3_quickstart.md
  V3_operator_manual.md

scripts/v3/
  validate-v3-package.mjs
  import-v3-package.mjs
```

Важно решить, что из этого публично, а что local-only.

Возможный подход:

- `.ai/v3/*.md` — публичные правила и схемы;
- `.ai/v3/requests/` — можно публично, если нет приватного контекста;
- `.ai/v3/responses/` — осторожно, зависит от содержимого;
- `.ai/v3/journals/` — возможно публично, если без локальных путей и секретов;
- `.ai/v3/staging/` — лучше local-only или gitignored;
- `_local/v3/inbox/` — local-only;
- исходные ZIP — local-only, если в них есть непроверенный контент.

---

## 20. Формат README_FOR_KILO.md

Рекомендуемый шаблон:

```markdown
# README_FOR_KILO

V3 ID: ...

## Purpose

This package contains generated files for ...

## Import mode

Use staging_first.

## Required checks

- Validate manifest.yaml.
- Validate checksums.sha256.
- Reject extra files under files/.
- Reject unsafe paths.
- Do not overwrite existing files unless action explicitly allows it.

## Allowed paths

...

## Forbidden paths

...

## Expected result

...

## Journal

After import, write a journal entry with:

- v3_id;
- zip path;
- zip sha256;
- staging path;
- written files;
- skipped files;
- validation result;
- Codex review required.

## Stop conditions

Stop if:

- manifest is missing;
- checksum mismatch;
- extra file found;
- unsafe path found;
- overwrite conflict found;
- forbidden path targeted.
```

---

## 21. Формат README_FOR_CODEX.md

Рекомендуемый шаблон:

```markdown
# README_FOR_CODEX

V3 ID: ...

## Task summary

...

## Files expected

...

## What changed conceptually

...

## Review goals

Check that:

- journal exists;
- files were written exactly as manifest declared;
- content matches the task;
- no forbidden paths were touched;
- generated docs do not claim unimplemented features are already implemented;
- generated scripts are not executed before review.

## Acceptance criteria

...

## Human review prompts

Ask the human to confirm:

- ...

## Rejection criteria

Reject if:

- ...
```

---

## 22. Как внешний ChatGPT должен отвечать в V3

Идеальный ответ внешнего ChatGPT должен включать:

1. Короткое подтверждение, что он понял V3-режим.
2. Список файлов, которые будут внутри ZIP.
3. Сам ZIP-архив как вложение, если интерфейс это позволяет.
4. Краткую инструкцию для человека: скачать ZIP и передать в KiloCode Notebook V3.
5. Честное уточнение: репозиторий не изменён, создан только artifact package.

Он не должен вставлять весь огромный код в чат, если ZIP уже приложен. Но может продублировать manifest в тексте для удобства проверки.

---

## 23. Если ZIP создать невозможно

Если внешний ChatGPT не может создать ZIP, допускается fallback-формат:

```text
BEGIN V3 ARTIFACT PACKAGE

FILE: manifest.yaml
CONTENT:
...
END FILE

FILE: README_FOR_KILO.md
CONTENT:
...
END FILE

FILE: files/.ai/v3/example.md
CONTENT:
...
END FILE

END V3 ARTIFACT PACKAGE
```

Но ZIP предпочтительнее.

Если используется fallback-формат, KiloCode должен парсить его ещё осторожнее.

---

## 24. Минимальный MVP V3

Для первого внедрения не нужно строить идеальную систему.

Минимальный рабочий V3:

1. Codex готовит V3 request.
2. ChatGPT создаёт ZIP с:
   - manifest.yaml;
   - README_FOR_KILO.md;
   - README_FOR_CODEX.md;
   - checksums.sha256;
   - files/.
3. KiloCode вручную или полуавтоматически распаковывает ZIP в staging.
4. KiloCode проверяет manifest и пути.
5. KiloCode записывает файлы.
6. KiloCode создаёт journal YAML.
7. Codex проверяет journal и файлы.
8. Человек принимает или просит правки.

MVP-ограничения:

- только `action: create`;
- только documentation-first файлы;
- без автоматического запуска скриптов;
- без записи в `src/`;
- без перезаписи существующих файлов.

---

## 25. Расширенный V3

После MVP можно добавить:

- автоматическую проверку ZIP;
- автоматическую генерацию journal;
- diff-preview перед записью;
- режим dry-run;
- режим apply-after-human-confirmation;
- автоматический Codex review template;
- список известных V3-пакетов;
- индекс V3-задач;
- связь V3-задач с issues;
- связь V3-задач с commits;
- повторную генерацию пакета по needs_revision;
- версионирование manifest schema;
- подпись пакета;
- policy для разных типов файлов.

---

## 26. Типы V3-задач

Рекомендуемые типы:

```text
docs_only
schema_only
script_draft
test_fixture
prototype_code
product_code_draft
product_code_patch
migration_plan
review_materials
workflow_contract
```

### 26.1. docs_only

Самый безопасный тип.

Создаёт только документацию.

### 26.2. schema_only

Создаёт схемы данных, типы контрактов, JSON Schema, YAML Schema.

### 26.3. script_draft

Создаёт скрипты, но они не должны запускаться до review.

### 26.4. test_fixture

Создаёт тестовые данные.

### 26.5. prototype_code

Создаёт код прототипа, не product-code.

### 26.6. product_code_draft

Создаёт черновой product-code в staging или draft-папке.

### 26.7. product_code_patch

Самый опасный тип. Разрешать только после зрелого V3-процесса.

---

## 27. Правила для product-code

На раннем этапе V3 не должен напрямую менять product-code.

Когда product-code всё-таки разрешён, нужны дополнительные правила:

- Codex должен подготовить очень точный request;
- allowed paths должны быть узкими;
- нужно указать конкретные файлы;
- нужен expected diff;
- нужны тесты или проверочные команды;
- нужен rollback plan;
- нужен human review;
- нельзя менять архитектуру шире задачи;
- нельзя «заодно» переписывать соседние части.

---

## 28. Что делать при needs_revision

Если Codex или человек просит доработку, не нужно править старый ZIP вручную.

Нужно создать новую V3-задачу или revision:

```text
V3-20260527-153000-v3-contract-r1
V3-20260527-153000-v3-contract-r2
```

Revision request должен включать:

- исходный V3 ID;
- что было принято;
- что было отклонено;
- какие файлы нужно изменить;
- какие ошибки исправить;
- какие файлы не трогать.

Journal должен связать revision с исходной задачей.

---

## 29. Индекс V3-задач

Полезно вести индекс:

```text
.ai/v3/V3_navigation.md
```

Он может содержать:

```markdown
# V3 Navigation

| V3 ID | Task | Status | Package | Journal | Codex Review | Human Verdict |
|---|---|---|---|---|---|---|
| V3-... | Create V3 contract | accepted | local zip | V3J-... | V3R-... | accepted |
```

Это позволит быстро понимать историю V3-пакетов.

---

## 30. Важные формулировки для правил внешнего ChatGPT

В V3 request стоит прямо писать:

```text
You do not have repository write access.
You are generating an artifact package only.
Do not claim that files were written to the repository.
Do not include files outside manifest.yaml.
Do not include hidden files.
Do not target forbidden paths.
Every file must have a clear purpose.
Every file must be safe to inspect before execution.
If unsure, create documentation or draft files instead of product-code.
```

На русском:

```text
У тебя нет прямого доступа на запись в репозиторий.
Ты создаёшь только пакет артефактов.
Не утверждай, что файлы уже записаны в репозиторий.
Не включай файлы вне manifest.yaml.
Не включай скрытые файлы.
Не указывай запрещённые пути.
У каждого файла должна быть понятная цель.
Любой скрипт должен быть безопасен для чтения до запуска.
Если есть сомнение, создавай документацию или draft-файлы, а не product-code.
```

---

## 31. Практическая рекомендация по внедрению

Лучший первый шаг — создать V3-инфраструктуру через сам V3-процесс, но в безопасном режиме.

Первая V3-задача может быть такой:

```text
Create initial V3 workflow documentation and schemas.
Allowed paths:
- .ai/v3/
- docs/v3/
No product-code.
No scripts except draft documentation.
Action: create only.
```

Вторая V3-задача:

```text
Create KiloCode Notebook V3 import checklist and pseudo-code.
Allowed paths:
- .ai/v3/
- docs/v3/
No executable scripts yet.
```

Третья V3-задача:

```text
Create validate-v3-package.mjs as a draft script.
Allowed paths:
- scripts/v3/
Script must not be executed automatically.
Codex must review before use.
```

Только после этого можно делать автоматический импорт.

---

## 32. Краткая версия для нового чата

Если нужно объяснить V3 новому чату коротко:

```text
V3 is an artifact-producing workflow for this GitHub project.
External ChatGPT receives project context, rules, metadata, allowed paths, forbidden paths, and a concrete task.
It must generate a ZIP artifact package, not just advice.
The ZIP must contain manifest.yaml, README_FOR_KILO.md, README_FOR_CODEX.md, checksums.sha256, and files/ with project-relative files.
ChatGPT must not claim it wrote to the repository.
A human downloads the ZIP and gives it to KiloCode Notebook V3.
KiloCode validates the package, stages/writes only manifest-listed safe files, and writes a journal entry.
Codex reads the journal and reviews the actual files.
The human gives the final acceptance or asks for revision.
Default mode: staging_first, action:create only, documentation-first, no product-code until the workflow is proven.
```

---

## 33. Итог

V3 нужен для того, чтобы использовать мощную внешнюю модель как генератор реальных проектных артефактов, но без хаоса и без прямого доступа к репозиторию.

Система держится на пяти опорах:

1. Структурированный V3 request.
2. ZIP artifact package с manifest и checksums.
3. KiloCode Notebook V3 как безопасный файловый оператор.
4. Journal как источник правды о фактической записи.
5. Codex review и human acceptance как обязательные gates.

Если эти опоры соблюдаются, V3 даёт сильный выигрыш:

- можно использовать мощную модель для больших задач;
- можно получать готовые файлы, а не только советы;
- можно сохранять контроль над репозиторием;
- можно проверять каждое действие;
- можно масштабировать внешний AI-workflow без потери управляемости.

Главное правило:

> V3 не должен заменять контроль. V3 должен усиливать производство артефактов при сохранении контроля через KiloCode, journal, Codex и человека.
