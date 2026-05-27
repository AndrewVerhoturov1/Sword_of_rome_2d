# v3_revision_request_prompt.md — Промпт для Revision Request

Версия: 0.1 (Phase 3)
Назначение: промпт для Codex или человека, который готовит запрос на доработку (revision) V3 artifact package у внешнего чата.
Статус: рабочий prompt. Опирается на [`v3_revision_contract.md`](../contracts/v3_revision_contract.md).

---

## 1. Когда использовать этот промпт

Этот промпт используется, когда Codex (по [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md)) или человек (по [`v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md)) решили, что результат первой попытки V3 import не принимается, но задача в целом разрешена и может быть доработана.

Revision — это **не** новый V3 request. Это запрос на доработку существующего пакета.

---

## 2. Промпт

```text
Ты получаешь запрос на доработку (revision) V3 artifact package.

Это НЕ новая задача. Это доработка существующего пакета `[previous_package_id]`. Исходный V3 ID задачи: `[v3_id]`. Номер revision: `[revision_number]`.

Твоя предыдущая попытка не была принята по следующим причинам. Тебе нужно исправить только указанные файлы. Остальной пакет остаётся без изменений.

---

## Что исправить

[Конкретный список: какие файлы, что именно в них не так, что должно быть вместо этого. Будь максимально конкретным.]

```
[список]
```

## Что повторно используется

Следующие файлы из предыдущего пакета приняты и НЕ требуют изменений. НЕ пересоздавай их и НЕ меняй:

```
[список]
```

## Уточнения scope (если есть)

[Если scope изменился — укажи новый scope. Если нет — напиши: scope не изменился.]

## Требования к ответу

1. Создай НОВЫЙ artifact package (ZIP) с суффиксом `-attempt-[revision_number]`:
   - Имя корневой папки: `V3-YYYYMMDD-HHMMSS-<slug>-attempt-[N]`.
2. Пакет должен содержать только ИСПРАВЛЕННЫЕ файлы. Принятые файлы не включай повторно.
3. Сохрани ту же базовую структуру:
   - `manifest.yaml` (обновлённый: укажи, что это revision, сошли на previous_package_id)
   - `README_FOR_KILO.md` (обновлённый для изменённого набора файлов)
   - `README_FOR_CODEX.md` (обновлённый: что изменилось по сравнению с предыдущей попыткой)
   - `checksums.sha256` (только для изменённых файлов)
   - `files/` (только изменённые файлы)
4. В `manifest.yaml` обязательно укажи:
   - Тот же `v3_id`, что в исходном request.
   - `revision_number` и `previous_package_id`.
   - Что именно изменилось в этой попытке.
5. Соблюдай все контракты V3: manifest, checksums, allowed_paths, forbidden_paths.

---

## Acceptance criteria для этой revision

[Конкретные критерии, по которым будет оцениваться эта попытка.]

```
[список]
```

## Лимиты

Это revision номер [N] из максимум 2. После двух неудачных revision задача будет отклонена.

---

## Правила, которые ты должен соблюдать

- Ты НЕ имеешь доступа к репозиторию.
- Ты НЕ утверждаешь, что уже изменил репозиторий.
- Ты создаёшь ZIP-пакет. Запись — через Kilo Notebook V3.
- Ты используешь только `action: create` (MVP).
- Ты не выходишь за `allowed_paths` из исходного request.
- Ты не заходишь в `forbidden_paths` из исходного request.
```

---

## 3. Правила для Codex при подготовке revision request

### 3.1. Обязательные проверки до отправки

- [ ] `v3_id` тот же, что в исходном request.
- [ ] `revision_number`: 1 или 2.
- [ ] `previous_package_id` явно указан.
- [ ] `what_to_fix` — конкретный список файлов и проблем, не абстрактное «сделай лучше».
- [ ] `what_to_reuse` — явно перечислены файлы, которые приняты без изменений.
- [ ] `scope_changes` — либо `null` (scope не изменился), либо новый scope.
- [ ] `acceptance_criteria` — конкретны и проверяемы.
- [ ] Лимит revision не превышен (максимум 2 попытки).

### 3.2. Когда revision уместен

- Часть файлов не импортирована (skipped по исправимой причине).
- Содержимое не полностью соответствует задаче.
- Scope или allowed paths описаны некорректно в исходном request.
- Acceptance criteria выполнены частично.
- Ошибка в одном-двух файлах.

### 3.3. Когда revision НЕ уместен

- Фундаментальная проблема в request → нужен новый V3 request.
- Внешний чат не соблюдал контракт → reject.
- Два revision цикла уже провалились → reject, нужен новый V3 request.

### 3.4. Что revision НЕ меняет

- Базовый `v3_id` задачи.
- `scope` (если явно не изменён).
- `action` (`create` для MVP).
- Уже принятые файлы (они не пересоздаются).

---

## 4. Traceability между итерациями

Каждая попытка revision должна сохранять traceability:

- Новый package получает суффикс `-attempt-N` (например, `V3-20260527-153000-v3-contracts-attempt-2`).
- Journal entry обновляется, а не перезаписывается: добавляется секция `revision_history`.
- В `revision_history` фиксируется каждая попытка:

```yaml
revision_history:
  - attempt: 1
    package_id: "V3-20260527-153000-v3-contracts-attempt-1"
    result: "revision_needed"
    reason: "Два файла требуют доработки"
  - attempt: 2
    package_id: "V3-20260527-153000-v3-contracts-attempt-2"
    result: "pending"
```

---

## 5. Лимиты revision

| Параметр | Лимит |
|----------|-------|
| Максимум revision циклов | 2 |
| Общий лимит попыток | 3 (1 оригинал + 2 revision) |

После исчерпания лимита: последний verdict — `reject`, задача возвращается на уровень нового V3 request.

---

## 6. Связанные документы

- [`v3_revision_contract.md`](../contracts/v3_revision_contract.md) — формальный контракт revision.
- [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md) — как Codex решает, нужен ли revision.
- [`v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md) — как человек принимает/отклоняет результат revision.
- [`v3_journal_contract.md`](../contracts/v3_journal_contract.md) — как revision фиксируется в journal.
- [`v3_request_contract.md`](../contracts/v3_request_contract.md) — V3 request, от которого revision не отрывается.
- [`v3_revision_request_template.md`](../templates/v3_revision_request_template.md) — шаблон revision request.
