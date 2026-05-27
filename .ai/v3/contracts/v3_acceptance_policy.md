# V3 Acceptance Policy

Версия: 0.1 (Phase 2)
Назначение: формальная политика того, как человек принимает, отклоняет или отправляет на доработку результат V3 import.
Статус: контракт Phase 2. Описывает acceptance gates и human verdict flow; не является готовым prompt/шаблоном (шаблоны — в Phase 3).

---

## 1. Суть acceptance

Acceptance — это финальный шаг V3 workflow. После того как:

1. `kilo-notebook-v3` импортировал package и создал journal entry;
2. Codex выполнил review (по [`v3_codex_review_contract.md`](v3_codex_review_contract.md));

человек принимает финальное решение.

Финальное решение всегда за человеком. Codex может рекомендовать, но не может заменить human verdict.

## 2. Minimal acceptance gates

Ни один V3 import не может быть принят без выполнения всех минимальных gates:

| Gate | Проверка | Кто выполняет |
|------|----------|---------------|
| Package valid | Manifest существует, checksums совпадают, paths валидны | `kilo-notebook-v3` |
| Journal created | Journal entry существует и заполнен | `kilo-notebook-v3` |
| Codex review done | Codex прочитал journal, проверил файлы, дал verdict | Codex |
| Human check done | Человек подтвердил, что результат соответствует ожиданиям | Human |

Если любой из gates не пройден, import считается невалидным.

## 3. Нормализация verdict enum

Codex verdict и human verdict — разные enum. Они не должны смешиваться.

### Codex verdict (фиксируется в journal до human review)

```yaml
codex_verdict:
  - accept            # результат годен
  - accept_with_notes # результат годен, но с замечаниями
  - revision_needed   # нужна доработка
  - reject            # результат не годен
```

См. [`v3_codex_review_contract.md`](v3_codex_review_contract.md).

### Human verdict (финальное решение человека)

```yaml
human_verdict:
  - accept    # принято
  - revision  # отправить на доработку
  - reject    # отклонено
```

### 3.1. `accept` (human verdict)

- Результат годен.
- Файлы остаются в репозитории.
- Journal entry обновляется: `human_review_status: approved`.
- V3 navigation обновляется.
- raw ZIP удаляется из staging.

### 3.2. `revision` (human verdict)

- Результат частично годен, но требует доработки.
- Файлы остаются (не удаляются до следующей попытки).
- Создаётся revision request (по [`v3_revision_contract.md`](v3_revision_contract.md)).
- Journal entry обновляется: `human_review_status: revision_requested`.
- Максимум 2 revision цикла.

### 3.3. `reject` (human verdict)

- Результат не годен.
- Файлы могут быть удалены (по решению человека) или оставлены для анализа.
- Journal entry обновляется: `human_review_status: rejected`.
- raw ZIP перемещается в `.ai/v3/staging/rejected/`.
- Задача возвращается на уровень нового V3 request или блокируется.

## 4. Когда нужен human check

Human check обязателен, если:

- scope: `workflow_docs`, `schemas`, `scripts`, `product_code`;
- это первый V3 import (pilot);
- Codex явно запросил human review;
- меняются workflow rules;
- пакет содержит исполняемые файлы (scripts scope).

Human check suggested (но не обязателен), если:

- scope: `docs_only`;
- изменения касаются только документации;
- Codex не видит рисков.

## 5. Как human verdict фиксируется

### 5.1. В journal entry

После human verdict journal entry обновляется:

```yaml
human_review:
  reviewer: "human"  # или имя человека
  verdict: "accept"  # accept | revision | reject
  timestamp: "2026-05-27T16:00:00Z"
  notes: "Все файлы проверены. Контракты согласованы. Можно принимать."
  codex_recommendation: "accept"
```

### 5.2. В V3 navigation

После `accept`:

- в `V3_navigation.md` добавляется запись об импортированных контрактах/файлах;
- статус обновляется.

### 5.3. В Git

После `accept`:

- принятые файлы (contracts, journal entry, navigation) коммитятся как workflow checkpoint;
- commit message: `V3: accept Phase 2 — Contract Pack`.

## 6. Что считается reject / revision / accept

### 6.1. Критерии accept

- Все файлы из `expected_files` созданы.
- Содержимое соответствует задаче.
- Scope соблюдён.
- Allowed paths соблюдены.
- Forbidden paths не нарушены.
- Codex verdict — `accept` или `accept_with_notes`.
- Human явно подтвердил.

### 6.2. Критерии revision

- Часть файлов не создана (skipped по исправимой причине).
- Содержимое частично не соответствует задаче.
- Все проблемы исправимы через доработку внешнего чата.
- Не превышен лимит revision попыток.

### 6.3. Критерии reject

- Manifest невалиден.
- Checksums не совпадают.
- Пакет содержит нелегальные файлы.
- Scope грубо нарушен.
- Два revision цикла провалились.
- Внешний чат не соблюдал контракт (например, утверждал, что изменил репозиторий).

## 7. Verdict flow diagram

```text
kilo-notebook-v3 import
  ↓
journal created (human_review_status: pending)
  ↓
Codex review
  ↓
Codex verdict: accept / revision_needed / reject
  ↓
Human reviews journal + files + Codex notes
  ↓
Human verdict:
  ├── accept → files persistent, navigation updated, staging cleaned
  ├── revision → revision request, external chat re-engaged
  └── reject  → files removed (or kept for analysis), staging cleaned
```

## 8. Что НЕ является acceptance

- Codex verdict без human confirmation — не acceptance.
- Импорт без journal — не acceptance.
- Наличие файлов в репозитории без human verdict — не acceptance.
- Утверждение внешнего чата, что «всё готово» — не acceptance.

Acceptance — это только явный human verdict после полного review chain.

---

## Связанные контракты

- [`v3_codex_review_contract.md`](v3_codex_review_contract.md) — Codex review до human verdict.
- [`v3_revision_contract.md`](v3_revision_contract.md) — revision flow, если human verdict — revision.
- [`v3_journal_contract.md`](v3_journal_contract.md) — как verdict фиксируется в journal.
- [`v3_storage_policy.md`](v3_storage_policy.md) — что становится persistent после accept.
- [`v3_scope_policy.md`](v3_scope_policy.md) — acceptance gates для разных scope уровней.
