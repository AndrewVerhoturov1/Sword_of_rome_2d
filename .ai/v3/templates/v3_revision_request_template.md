# v3_revision_request_template.md — Шаблон Revision Request

Версия: 0.1 (Phase 3)
Назначение: шаблон запроса на доработку (revision) V3 artifact package. Заполняется Codex или человеком после неудачной попытки импорта.
Используй совместно с: [`v3_revision_request_prompt.md`](../prompts/v3_revision_request_prompt.md) и [`v3_revision_contract.md`](../contracts/v3_revision_contract.md).

---

## Как использовать

1. Определи, что именно нужно исправить (конкретные файлы и проблемы).
2. Заполни шаблон ниже.
3. Передай заполненный шаблон внешнему чату вместе с исходным V3 request.
4. Убедись, что номер revision не превышает лимит (максимум 2).

---

```text
<!-- V3 REVISION REQUEST — ЗАПРОС НА ДОРАБОТКУ -->
<!--
  Это НЕ новый V3 request. Это доработка существующего пакета.
  Исходный V3 ID остаётся тем же. Меняются только указанные файлы.
-->

## V3 ID
[V3-YYYYMMDD-HHMMSS-<slug>]
<!-- Тот же v3_id, что в исходном request. НЕ меняй. -->

## Revision Number
[N]
<!-- 1 или 2. Порядковый номер этой попытки доработки. -->

## Previous Package ID
[V3-YYYYMMDD-HHMMSS-<slug>-attempt-N]
<!-- v3_id предыдущего пакета, который не был принят. -->

## Что исправить

[Конкретный список. Для каждого файла: что не так и что должно быть вместо этого.]

```
- [файл 1]: [что исправить]
- [файл 2]: [что исправить]
```

## Что повторно используется

Следующие файлы из предыдущего пакета ПРИНЯТЫ и не требуют изменений:

```
- [файл 1]
- [файл 2]
```

НЕ пересоздавай и НЕ меняй эти файлы в новом пакете.

## Scope Changes
[null | новый scope]
<!-- Если scope изменился — укажи новый. Если нет — null. -->

## Acceptance Criteria

[Конкретные критерии для этой попытки. Не копируй исходные — уточни под revision.]

```
- [ ] [критерий 1]
- [ ] [критерий 2]
```

## Требования к ответу

1. Создай НОВЫЙ artifact package (ZIP).
2. Имя корневой папки: `V3-YYYYMMDD-HHMMSS-<slug>-attempt-[N]`.
3. Включи в пакет только изменённые файлы. Принятые файлы не дублируй.
4. В `manifest.yaml` укажи:
   - Тот же `v3_id`.
   - `revision_number: [N]`.
   - `previous_package_id: "[предыдущий package_id]"`.
   - Секцию `changes_from_previous` с перечислением изменений.
5. Структура пакета стандартная: `manifest.yaml`, `README_FOR_KILO.md`, `README_FOR_CODEX.md`, `checksums.sha256`, `files/`.
6. Соблюдай все контракты V3 (manifest, checksums, allowed_paths, forbidden_paths).

## Лимиты

Это revision номер [N] из максимум 2. Если эта попытка тоже будет отклонена, задача будет rejected.

## Правила

- Ты НЕ имеешь доступа к репозиторию.
- Ты НЕ утверждаешь, что уже изменил репозиторий.
- Ты создаёшь ZIP-пакет. Запись — Kilo Notebook V3. Проверка — Codex. Решение — человек.
- `action: create` (MVP).
- Не выходи за `allowed_paths` из исходного request.
- Не заходи в `forbidden_paths` из исходного request.
```

---

## Правила заполнения

### `v3_id`
- Всегда тот же, что в исходном V3 request.
- НЕ создавай новый v3_id для revision.

### `revision_number`
- 1 для первой доработки.
- 2 для второй (последней).

### `what_to_fix`
- Максимально конкретно: «файл X, секция Y, сейчас написано Z, должно быть W».
- Не «сделай лучше», а «добавь секцию про необязательные поля в v3_manifest_contract.md».

### `what_to_reuse`
- Перечисли все файлы, которые приняты без изменений.
- Это снижает риск случайного изменения уже годных файлов.

### `scope_changes`
- `null` если scope не менялся.
- Если scope расширяется (например, с `docs_only` на `workflow_docs`) — укажи новый scope и причину.

---

## Пример заполнения

```text
## V3 ID
V3-20260527-153000-v3-contracts

## Revision Number
1

## Previous Package ID
V3-20260527-153000-v3-contracts-attempt-1

## Что исправить

- v3_manifest_contract.md: добавить секцию "Необязательные поля" с перечислением package_version, source_request, human_review_required.
- v3_storage_policy.md: уточнить правило для raw ZIP — явно указать "local-only по умолчанию, удаляется после accept".

## Что повторно используется

- v3_request_contract.md
- v3_artifact_package_contract.md
- v3_journal_contract.md
- v3_codex_review_contract.md
- v3_revision_contract.md
- v3_scope_policy.md
- v3_acceptance_policy.md
- README.md, V3_navigation.md, repo_navigation.md (уже обновлены)

## Scope Changes
null

## Acceptance Criteria

- [ ] v3_manifest_contract.md содержит секцию "Необязательные поля"
- [ ] v3_storage_policy.md содержит явное правило "raw ZIP — local-only"
- [ ] Остальные файлы не изменены
- [ ] manifest.yaml корректен, checksums совпадают
```

---

## Связанные документы

- [`v3_revision_request_prompt.md`](../prompts/v3_revision_request_prompt.md) — промпт для revision request.
- [`v3_revision_contract.md`](../contracts/v3_revision_contract.md) — формальный контракт revision.
- [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md) — как Codex решает, нужен ли revision.
- [`v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md) — как человек принимает/отклоняет результат.
