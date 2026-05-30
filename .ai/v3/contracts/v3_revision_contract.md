# V3 Revision Contract

Версия: 0.1 (Phase 2)
Назначение: формальный контракт revision — как запрашивается доработка V3 artifact package у внешнего чата, если Codex или человек не приняли результат первой попытки.
Статус: контракт Phase 2. Описывает обязательный revision flow, но не является готовым prompt/шаблоном (шаблоны — в Phase 3).

---

## 1. Суть revision

Revision — это запрос на доработку V3 artifact package. Он возникает, когда Codex (по [`v3_codex_review_contract.md`](v3_codex_review_contract.md)) или человек (по [`v3_acceptance_policy.md`](v3_acceptance_policy.md)) решают, что результат первой попытки не принимается, но задача в целом разрешена и может быть доработана.

Revision не является:

- новым V3 request (не перезапускает полный цикл);
- откатом импорта (файлы могут остаться до решения);
- бесконечным циклом (количество попыток ограничено).

## 2. Когда revision уместен

Revision запрашивается, если:

- часть файлов не была импортирована (skipped по исправимой причине);
- содержимое файлов не полностью соответствует задаче;
- scope или allowed paths были описаны некорректно в исходном request;
- acceptance criteria выполнены частично;
- ошибка в одном-двух файлах, а не во всём пакете.

Revision НЕ уместен, если:

- фундаментальная проблема в request (тогда нужен новый V3 request);
- внешний чат не соблюдал контракт (тогда reject);
- два revision цикла уже провалились (тогда reject, нужен новый request).

## 3. Структура revision request

Revision request должен содержать:

| Поле | Описание |
|------|----------|
| `v3_id` | Исходный идентификатор V3 задачи (тот же, что в первой попытке) |
| `revision_number` | Номер revision (1, 2, ...) |
| `previous_package_id` | `v3_id` предыдущего пакета (для traceability) |
| `what_to_fix` | Конкретный список того, что нужно исправить |
| `what_to_reuse` | Что остаётся неизменным из предыдущего пакета |
| `scope_changes` | Если scope был уточнён — новые границы |
| `acceptance_criteria` | Критерии, по которым будет оцениваться revision |
| `deadline` | Ожидаемое количество попыток (обычно 1-2 на revision) |

### 3.1. Пример

```yaml
v3_id: "V3-20260527-153000-v3-contracts"
revision_number: 1
previous_package_id: "V3-20260527-153000-v3-contracts-attempt-1"

what_to_fix:
  - "v3_manifest_contract.md: добавить секцию 'Необязательные поля'"
  - "v3_storage_policy.md: уточнить правило для raw ZIP — local-only по умолчанию"

what_to_reuse:
  - "Все остальные файлы из предыдущего пакета принимаются без изменений"
  - "manifest.yaml структура корректна"

scope_changes: null

acceptance_criteria:
  - "Два указанных файла обновлены"
  - "Остальные файлы не изменены"
```

## 4. Что повторно используется из предыдущего цикла

Revision не требует создания нового пакета с нуля. Из предыдущего цикла повторно используются:

- `v3_id` (идентификатор задачи остаётся тем же);
- manifest структура (если не меняется);
- accepted файлы (те, которые прошли review без замечаний);
- journal entry (обновляется, а не создаётся заново).

Новый пакет содержит только исправленные/добавленные файлы. Повторная передача уже принятых файлов не требуется.

## 5. Traceability между итерациями

Каждая итерация revision должна сохранять traceability:

- новый package получает суффикс `-attempt-N` (например, `V3-20260527-153000-v3-contracts-attempt-2`);
- journal entry обновляется, а не перезаписывается;
- в journal добавляется секция `revision_history`:

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

## 6. Лимиты revision

| Параметр | Лимит |
|----------|-------|
| Максимум revision циклов | 2 |
| Максимум попыток на revision | 1 (каждый revision — одна новая попытка) |
| Общий лимит | 3 попытки (1 оригинал + 2 revision) |

После исчерпания лимита:

- последний verdict — `reject`;
- задача возвращается на уровень нового V3 request или блокируется как нерешаемая текущим V3 workflow.

## 7. Что revision НЕ меняет

Revision не меняет:

- базовый `v3_id` задачи;
- `scope`, если он не был явно изменён в revision request;
- `action` (для MVP остаётся `create`);
- уже принятые файлы (они не пересоздаются).

---

## Связанные контракты

- [`v3_codex_review_contract.md`](v3_codex_review_contract.md) — как Codex решает, нужен ли revision.
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md) — как человек принимает/отклоняет результат revision.
- [`v3_journal_contract.md`](v3_journal_contract.md) — как revision фиксируется в journal.
- [`v3_request_contract.md`](v3_request_contract.md) — V3 request, от которого revision не отрывается.
