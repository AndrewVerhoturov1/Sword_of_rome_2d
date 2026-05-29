# V3 Manifest Contract

Версия: 0.2 (Phase 5+ post-import testing correction)
Назначение: формальный контракт `manifest.yaml` — главного файла V3 artifact package, который описывает всё содержимое пакета и правила импорта.
Статус: контракт Phase 2+. Добавлен блок `post_import_testing` (post-import testing correction).

---

## 1. Суть manifest

`manifest.yaml` — это единственный источник правды о содержимом V3 artifact package. Он описывает:

- идентификатор и источник пакета;
- какие файлы входят в пакет;
- куда они должны попасть;
- какие действия требуются;
- какие пути разрешены и запрещены;
- какие критерии приёмки;
- какие риски известны.

`manifest.yaml` находится в корне ZIP-пакета. Без него пакет считается невалидным и не подлежит импорту.

## 2. Обязательные поля manifest

### 2.1. `v3_id`

Уникальный идентификатор пакета. Должен совпадать с `v3_id` из V3 request, на который этот пакет является ответом.

Формат: `V3-YYYYMMDD-HHMMSS-<slug>`.

Пример: `V3-20260527-153000-v3-contracts`.

### 2.2. `task_title`

Короткое название задачи, для которой создан пакет. Может быть на русском или английском.

Пример: `V3 Phase 2 Contract Pack`.

### 2.3. `generated_by`

Кто создал пакет. Допустимые значения:

- `external_chatgpt_5_5`
- `external_deepseek`
- `external_kimi`
- `external_claude`
- или другой идентификатор внешнего чата.

Значение должно быть конкретным. `external_unknown` не допускается.

### 2.4. `action`

Действие, которое должен выполнить импортёр. Для MVP:

- `action: create` — создать новые файлы.

`update`, `overwrite`, `delete` в MVP не поддерживаются.

### 2.5. `scope`

Уровень scope пакета. Должен совпадать с `scope` из V3 request.

Допустимые значения (см. [`v3_scope_policy.md`](v3_scope_policy.md)):

- `docs_only`
- `workflow_docs`
- `schemas`
- `scripts`
- `product_code`

### 2.6. `write_policy`

Политика записи. Содержит:

```yaml
write_policy:
  mode: "create_only"        # для MVP
  require_codex_review: true  # всегда true для V3
  require_human_review: true  # всегда true для V3
  allow_overwrite: false      # для MVP
```

### 2.7. `allowed_paths`

Список project-relative путей, куда разрешено писать файлы.

Пример:

```yaml
allowed_paths:
  - ".ai/v3/"
  - "docs/v3/"
```

Все target paths файлов из секции `files` должны входить в `allowed_paths`.

### 2.8. `forbidden_paths`

Список project-relative путей, куда запрещено писать файлы.

По умолчанию (если не указаны в request):

```yaml
forbidden_paths:
  - ".git/"
  - "node_modules/"
  - "dist/"
  - "build/"
  - "coverage/"
  - "package-lock.json"
  - "yarn.lock"
  - "pnpm-lock.yaml"
```

Forbidden paths имеют приоритет над allowed paths.

### 2.9. `files`

Список файлов в пакете. Каждый элемент содержит:

```yaml
files:
  - path: ".ai/v3/contracts/v3_request_contract.md"
    source_in_zip: "files/.ai/v3/contracts/v3_request_contract.md"
    action: "create"
    required: true
    sha256: "a1b2c3d4e5f6..."
    purpose: "V3 request contract — обязательные поля, scope, allowed/forbidden paths."
```

Обязательные поля каждого файла:

| Поле | Описание |
|------|----------|
| `path` | Project-relative target path в репозитории |
| `source_in_zip` | Путь к файлу внутри ZIP (относительно корня пакета) |
| `action` | Действие: `create` (MVP) |
| `required` | `true` или `false`. Если `true`, отсутствие файла — ошибка импорта |
| `sha256` | SHA-256 хэш содержимого файла |
| `purpose` | Краткое описание, зачем нужен этот файл |

### 2.10. `acceptance_criteria`

Список критериев, по которым Codex будет оценивать результат импорта.

Пример:

```yaml
acceptance_criteria:
  - "All files listed in manifest exist in the ZIP under files/."
  - "No extra files are present under files/ unless explicitly listed in manifest."
  - "All target paths are project-relative and inside allowed_paths."
  - "No target path matches forbidden_paths."
  - "All sha256 checksums match."
  - "KiloCode journal entry is created after import."
  - "Codex review is required before final acceptance."
```

### 2.11. `known_risks`

Известные риски задачи, которые Codex и человек должны учитывать при оценке.

Пример:

```yaml
known_risks:
  - "Generated files describe intended process but not yet wired into existing automation."
  - "Scripts must be reviewed before being executed."
  - "Documentation must not claim V3 is fully operational unless it is."
```

## 3. Блок post_import_testing

### 3.1. Назначение

Блок `post_import_testing` управляет тем, требуется ли post-import testing после импорта пакета через `Kilo Notebook V3`.

### 3.2. Структура

Блок использует трёхрежимную модель:

```yaml
post_import_testing:
  mode: "required"   # required | optional | waived
  prompt_file: "POST_IMPORT_TEST_PROMPT.md"  # обязательно при mode=required, опционально при mode=optional
```

### 3.3. Три режима

| mode | Семантика | Prompt в package | Acceptance gate | Показ prompt после импорта |
|------|-----------|-----------------|-----------------|---------------------------|
| `required` | Testing обязателен для acceptance | Обязателен | Да — без machine-check report или waiver accept невозможен | Да, всегда |
| `optional` | Prompt полезен, но не обязателен. Не блокирует acceptance | Опционален | Нет | Да, если prompt есть в package |
| `waived` | Testing явно не нужен (например, чистый docs_only без рисков) | Не требуется | Нет | Нет, даже если prompt случайно есть |

### 3.4. Правила

| Правило | Описание |
|---------|----------|
| `mode` | `required`, `optional` или `waived`. Определяет acceptance gate и поведение notebook-v3. |
| `prompt_file` | Имя control file с test prompt в корне ZIP. По умолчанию `POST_IMPORT_TEST_PROMPT.md`. |
| `docs_only` default | Для `scope: docs_only` по умолчанию `mode: waived`, если request явно не усиливает testing до `optional` или `required`. |
| `product_code`/`scripts` default | Для code-affecting scope обычно `mode: required`. |

### 3.5. Инварианты

- Если `mode = required`, в корне ZIP должен присутствовать `POST_IMPORT_TEST_PROMPT.md`.
- Если `mode = required`, а `POST_IMPORT_TEST_PROMPT.md` отсутствует — это проблема пакета.
- Если `mode = optional`, prompt может быть, а может отсутствовать. Если есть — показывается.
- Если `mode = waived`, prompt не требуется, и его наличие игнорируется.
- `POST_IMPORT_TEST_PROMPT.md` не перечисляется в секции `files` как project target file.
- Блок `post_import_testing` не вводит новые lifecycle статусы в `V3_navigation.md`.

## 4. Необязательные поля

Следующие поля могут быть добавлены по мере maturity workflow:

- `package_version` — версия package формата (например, `0.1`);
- `source_request` — ссылка на V3 request, на который отвечает этот пакет;
- `human_review_required` — список конкретных пунктов для ручной проверки.

Эти поля не обязательны для MVP, но их наличие повышает traceability.

## 5. Инварианты manifest

| Инвариант | Правило |
|-----------|---------|
| `v3_id` уникален | В рамках одного workflow задача не должна иметь два manifest с одинаковым `v3_id` |
| `action` согласован | `action` в manifest должен совпадать с `action` в V3 request |
| `scope` согласован | `scope` в manifest должен совпадать с `scope` в V3 request |
| `post_import_testing.mode == "required"` согласован с package | `POST_IMPORT_TEST_PROMPT.md` должен быть в корне ZIP |
| `allowed_paths` покрывают все `files[].path` | Каждый target path входит хотя бы в один allowed_path |
| Ни один `files[].path` не входит в `forbidden_paths` | Все target paths валидны |
| Каждый `files[].source_in_zip` существует | Файл реально присутствует в ZIP под этим путём |
| SHA-256 совпадает | Хэш из manifest совпадает с реальным содержимым файла |

## 6. Что manifest не должен содержать

- Пути, не связанные с содержимым пакета.
- Утверждения, что файлы уже записаны в репозиторий.
- Инструкции для импортёра (они в `README_FOR_KILO.md`).
- Инструкции для Codex (они в `README_FOR_CODEX.md`).
- Инструкции для post-import testing (они в `POST_IMPORT_TEST_PROMPT.md`, если есть).
- Секреты, токены, пароли.

---

## Связанные контракты

- [`v3_request_contract.md`](v3_request_contract.md) — V3 request, от которого зависит manifest.
- [`v3_artifact_package_contract.md`](v3_artifact_package_contract.md) — структура пакета, в котором находится manifest.
- [`v3_scope_policy.md`](v3_scope_policy.md) — уровни scope.
- [`v3_codex_review_contract.md`](v3_codex_review_contract.md) — как Codex проверяет результат импорта.
