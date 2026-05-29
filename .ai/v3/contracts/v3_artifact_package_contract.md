# V3 Artifact Package Contract

Версия: 0.2 (Phase 5+ post-import testing correction)
Назначение: формальный контракт структуры V3 artifact package — ZIP-архива, который внешний чат создаёт в ответ на V3 request.
Статус: контракт Phase 2+. Добавлен `POST_IMPORT_TEST_PROMPT.md` как допустимый root-level control file (post-import testing correction).

---

## 1. Суть artifact package

V3 artifact package — это ZIP-архив со строгой внутренней структурой. Внешний чат создаёт его в ответ на [`v3_request_contract.md`](v3_request_contract.md) и возвращает человеку. Человек потом передаёт его в `kilo-notebook-v3` как raw input: archive link, local archive path или другой явно выбранный package source.

Пакет — это транспортный контейнер. Он не является источником истины сам по себе. Источник истины — связка:

```text
ZIP + manifest + checksums + allowed paths + journal
```

## 2. Обязательная структура пакета

Корень ZIP обязан содержать строго следующие элементы:

```text
V3-YYYYMMDD-HHMMSS-<slug>/
  manifest.yaml          # обязателен
  README_FOR_KILO.md     # обязателен
  README_FOR_CODEX.md    # обязателен
  checksums.sha256       # обязателен
  files/                 # обязателен
    <project-relative-path-1>
    <project-relative-path-2>
    ...
```

### 2.1. Корневая папка

Имя корневой папки: `V3-YYYYMMDD-HHMMSS-<slug>`, где:

- `V3` — префикс workflow route;
- `YYYYMMDD` — дата создания (UTC);
- `HHMMSS` — время создания (UTC);
- `<slug>` — короткий идентификатор задачи латиницей, например `v3-contracts`.

Пример: `V3-20260527-153000-v3-contracts`.

### 2.2. [`manifest.yaml`](v3_manifest_contract.md)

Главный файл пакета. Описывает всё содержимое и правила импорта. Контракт manifest — в [`v3_manifest_contract.md`](v3_manifest_contract.md).

Обязателен. Без manifest пакет считается невалидным.

### 2.3. README_FOR_KILO.md

Инструкция для `kilo-notebook-v3`. Объясняет:

- как распаковать пакет;
- какой режим записи использовать;
- какие пути разрешены (`allowed_paths`);
- что делать при конфликте имён;
- что делать при несовпадении хэша;
- что писать в journal;
- когда остановиться.

Обязателен. Это не пользовательская документация, а машиночитаемая инструкция для импортёра.

### 2.4. README_FOR_CODEX.md

Инструкция для Codex. Объясняет:

- зачем создан пакет;
- какие файлы ожидаются;
- какую задачу они решают;
- какие критерии приёмки;
- какие места проверить особенно внимательно;
- какие ручные проверки попросить у человека;
- какие признаки должны привести к отклонению.

Обязателен. Без него Codex не может выполнить review по контракту [`v3_codex_review_contract.md`](v3_codex_review_contract.md).

### 2.5. checksums.sha256

Файл с SHA-256 хэшами всех файлов из `files/`. Формат:

```text
<sha256>  files/<project-relative-path>
```

Пример:

```text
a1b2c3d4e5f6...  files/.ai/v3/contracts/v3_request_contract.md
f6e5d4c3b2a1...  files/docs/v3/setup_guide.md
```

Обязателен. Без checksums импортёр не может проверить целостность файлов.

### 2.6. files/

Папка с реальными проектными файлами. Внутри `files/` структура повторяет project-relative пути.

Например, если файл должен попасть в `.ai/v3/contracts/v3_request_contract.md`, то в ZIP он лежит как:

```text
files/.ai/v3/contracts/v3_request_contract.md
```

Все файлы внутри `files/` должны быть перечислены в `manifest.yaml`. Файл, который есть в `files/`, но отсутствует в manifest, считается нелегальным и должен быть заблокирован при импорте.

## 3. Инварианты пакета

При импорте должны выполняться следующие проверки:

| Инвариант | Проверка | Нарушение |
|-----------|----------|-----------|
| Manifest существует | `manifest.yaml` присутствует в корне | Пакет невалиден, импорт остановлен |
| Все файлы из manifest есть в `files/` | Сверка списка `files` в manifest с содержимым `files/` | Импорт остановлен |
| Нет файлов в `files/` вне manifest | Все файлы в `files/` перечислены в manifest | Нелегальные файлы заблокированы |
| Все хэши совпадают | SHA-256 каждого файла совпадает с `checksums.sha256` | Файл заблокирован |
| Все пути в `allowed_paths` | Каждый target path входит в `allowed_paths` из manifest | Файл заблокирован |
| Ни один путь не в `forbidden_paths` | Каждый target path НЕ входит в `forbidden_paths` | Файл заблокирован |

## 4. Опциональный root-level control file: POST_IMPORT_TEST_PROMPT.md

`POST_IMPORT_TEST_PROMPT.md` — это опциональный root-level control file V3 artifact package.

### 4.1. Назначение

Это не project target file. Он не пишется в репозиторий как импортированный файл. Он служит только как post-import support artifact: после успешного импорта `Kilo Notebook V3` показывает этот prompt человеку для дальнейшего тестирования.

### 4.2. Правила размещения

- Находится в корне ZIP-пакета, рядом с `manifest.yaml`, `README_FOR_KILO.md`, `README_FOR_CODEX.md`, `checksums.sha256`.
- Не входит в `files/`.
- Не перечисляется в секции `files` manifest как project target file.
- Не учитывается в `checksums.sha256`.

### 4.3. Когда обязателен

Обязательность `POST_IMPORT_TEST_PROMPT.md` регулируется полем `post_import_testing.mode` в `manifest.yaml`:

- `mode = required` — prompt обязателен, отсутствие = проблема пакета;
- `mode = optional` — prompt опционален, если есть — будет показан, если нет — не проблема;
- `mode = waived` — prompt не требуется, даже если есть — игнорируется.

### 4.4. Требования к содержимому

`POST_IMPORT_TEST_PROMPT.md` должен содержать два слоя проверок:

#### Machine checks

Вещи, которые человеку делать неудобно:
- команды (build, lint, typecheck, запуск);
- file/path checks;
- static checks;
- простые runtime checks, если они безопасны и реально доступны.

#### Human checks

Вещи, которые машине трудно оценить по смыслу:
- визуальный результат;
- UX/удобство;
- смысл текста;
- соответствие ожидаемому результату;
- всё, что user-facing и лучше проверяется глазами.

Prompt также обязан:
- не выдумывать результаты;
- если команда недоступна, писать это честно;
- не утверждать, что внешний чат уже запускал тесты;
- вернуть структурированный machine-check report для Codex.

### 4.5. Что НЕ является POST_IMPORT_TEST_PROMPT.md

- Это не project target file.
- Это не инструкция для импортёра (для этого есть `README_FOR_KILO.md`).
- Это не инструкция для Codex (для этого есть `README_FOR_CODEX.md`).
- Это не замена реального тестирования через обычный Kilo code run.

## 5. Что НЕ является artifact package

- ZIP без `manifest.yaml` — не artifact package.
- ZIP с файлами, но без `checksums.sha256` — не artifact package.
- ZIP без `README_FOR_KILO.md` — не artifact package.
- ZIP без `README_FOR_CODEX.md` — не artifact package.
- ZIP с project target files вне `files/` — не artifact package. Только package control files могут быть в корне ZIP: `manifest.yaml`, `README_FOR_KILO.md`, `README_FOR_CODEX.md`, `checksums.sha256`. `POST_IMPORT_TEST_PROMPT.md` — допустимый опциональный control file, но не project target file.
- Набор файлов в чате, не упакованный в ZIP, — не artifact package.

## 6. MVP-ограничения

На текущей стадии (Phase 5+):

- `action` только `create` (новые файлы);
- перезапись существующих файлов (`overwrite`) не поддерживается;
- удаление файлов (`delete`) не поддерживается;
- бинарные файлы в `files/` не допускаются без явного разрешения в request.

Эти ограничения — часть контракта, а не временное неудобство. Они снимаются только после Phase 5 (Safe Pilot) и Phase 8 (Expansion to Product-Code Scopes).

---

## Связанные контракты

- [`v3_request_contract.md`](v3_request_contract.md) — контракт V3 request.
- [`v3_manifest_contract.md`](v3_manifest_contract.md) — контракт manifest.yaml.
- [`v3_journal_contract.md`](v3_journal_contract.md) — контракт journal entry.
- [`v3_codex_review_contract.md`](v3_codex_review_contract.md) — контракт Codex review.
- [`v3_storage_policy.md`](v3_storage_policy.md) — что tracked, что local-only.
