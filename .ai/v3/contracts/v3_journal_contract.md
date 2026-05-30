# V3 Journal Contract

Версия: 0.1 (Phase 2)
Назначение: формальный контракт journal entry — записи, которую `kilo-notebook-v3` создаёт после импорта V3 artifact package.
Статус: контракт Phase 2. Описывает обязательные поля journal entry, но не является готовым runtime/script (скрипты — в Phase 7).

---

## 1. Суть journal

Journal entry — это подробный технический trace одного import-run. Он создаётся `kilo-notebook-v3` после того, как пакет получен, проверен и разрешённые файлы записаны.

Journal — не просто лог. Это источник фактов для Codex review: Codex проверяет journal до того, как смотреть реальные файлы.

Journal не является:

- решением о приёмке (verdict делает Codex + человек);
- репозиторием артефактов (raw ZIP хранится отдельно);
- заменой manifest (manifest — часть пакета, journal — запись импорта);
- заменой [`../V3_navigation.md`](../V3_navigation.md).

### 1.1. Граница между journal и V3_navigation

`V3_navigation.md` хранит короткий lifecycle index цикла:

- `V3 ID`
- статус
- тема
- краткую summary
- ссылки на request/prompt/journal
- список created files

Journal хранит только подробности конкретного import-run:

- какой package source использован;
- какие проверки прошли;
- какие файлы imported;
- какие skipped и почему;
- технические verification notes.

Если journal начинает повторять целиком строку из `V3_navigation.md`, это уже drift и лишнее дублирование.

## 2. Обязательные поля journal entry

### 2.1. `v3_id`

Идентификатор V3 задачи, совпадающий с `v3_id` из manifest импортированного пакета.

Формат: `V3-YYYYMMDD-HHMMSS-<slug>`.

### 2.2. `timestamp`

Метка времени создания journal entry в формате ISO 8601 (UTC).

Пример: `2026-05-27T15:30:00Z`.

### 2.3. `import_status`

Статус импорта. Допустимые значения:

- `imported` — пакет успешно импортирован, файлы записаны.
- `partial` — часть файлов импортирована, часть заблокирована/пропущена.
- `failed` — импорт не удался (критическая ошибка).
- `blocked` — импорт не начинался из-за preflight-ошибки.

### 2.4. `source_package`

Информация об исходном пакете и конкретном input source:

```yaml
source_package:
  package_id: "V3-20260527-153000-v3-contracts"
  source_type: "<archive_link | local_archive_path | repo_local_staging>"
  source_value: "<сама ссылка или путь>"
  manifest_path: "<path внутри staging или extracted package>"
  zip_archive: "<путь к сохранённому ZIP, если он был локально сохранён>"
  checksums_verified: true
```

### 2.5. `imported_files`

Список файлов, которые были успешно импортированы (созданы или обновлены).

Каждый элемент:

```yaml
- path: ".ai/v3/contracts/v3_request_contract.md"
  action: "create"
  sha256_match: true
  notes: ""
```

### 2.6. `skipped_files`

Список файлов, которые были пропущены при импорте (с указанием причины).

```yaml
- path: ".ai/v3/contracts/v3_request_contract.md"
  reason: "file_already_exists"
  notes: "Overwrite not allowed in current action scope."
```

Возможные причины пропуска:

| Причина | Описание |
|---------|----------|
| `outside_allowed_paths` | Файл не входит в `allowed_paths` |
| `in_forbidden_paths` | Файл входит в `forbidden_paths` |
| `checksum_mismatch` | SHA-256 не совпадает |
| `file_already_exists` | Файл уже существует, overwrite запрещён |
| `not_in_manifest` | Файл есть в `files/` ZIP, но отсутствует в manifest |
| `unsupported_action` | Действие не поддерживается (например, `delete`) |
| `binary_file` | Бинарный файл без явного разрешения |

### 2.7. `verification_notes`

Короткие заметки о проверке пакета:

```yaml
verification_notes:
  manifest_valid: true
  all_files_in_manifest: true
  no_extra_files: true
  checksums_all_match: true
  allowed_paths_valid: true
  forbidden_paths_respected: true
```

### 2.8. `human_review_status`

Статус ручной проверки человеком. На момент создания journal entry:

- `pending` — человек ещё не проверил.
- `approved` — человек принял.
- `rejected` — человек отклонил.
- `revision_requested` — человек отправил на доработку.

Начальное значение: `pending`.

## 3. Хранение journal entries

Каждая journal entry сохраняется как отдельный файл в `.ai/v3/journals/`.

Имя файла: `V3-YYYYMMDD-HHMMSS-<slug>_journal.yaml`.

Пример: `V3-20260527-153000-v3-contracts_journal.yaml`.

Pending journal drafts (до human accept) хранятся в `.ai/v3/journals/drafts/` и являются local-only.

Accepted journal entries хранятся в `.ai/v3/journals/` и являются tracked (часть audit trail V3 workflow).

Codex может читать pending local journal draft до human accept в рамках review flow.

`V3_navigation.md` при этом хранит только ссылку на journal и короткую summary, а не копию полей journal.

## 4. Инварианты journal

| Инвариант | Правило |
|-----------|---------|
| `v3_id` уникален | В рамках одного workflow задача не должна иметь два journal с одинаковым `v3_id` |
| `timestamp` не в будущем | Время создания journal entry должно быть <= текущему времени (с допустимой погрешностью) |
| `import_status` согласован | Если `failed` или `blocked`, списки `imported_files` должны быть пусты |
| `imported_files` + `skipped_files` = `files` из manifest | Все файлы из manifest должны быть учтены |
| `human_review_status` начинается с `pending` | Verdict не предопределён на момент импорта |

## 5. Обновление journal

Journal entry может обновляться после Codex review:

- после Codex review добавляются `codex_review_notes`;
- после human verdict обновляется `human_review_status`;

Обновление journal не удаляет и не перезаписывает исходную запись импорта. Оно добавляет новые поля или приложения.

---

## Связанные контракты

- [`v3_artifact_package_contract.md`](v3_artifact_package_contract.md) — структура пакета, который импортируется.
- [`v3_manifest_contract.md`](v3_manifest_contract.md) — manifest, который проверяется при импорте.
- [`v3_codex_review_contract.md`](v3_codex_review_contract.md) — как Codex проверяет journal и реальные файлы.
- [`v3_storage_policy.md`](v3_storage_policy.md) — что tracked, что local-only.
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md) — как человек принимает/отклоняет результат.
