# V3 Codex Review Contract

Версия: 0.1 (Phase 2)
Назначение: формальный контракт того, как Codex проверяет импортированные V3 артефакты — journal, реальные файлы, сверку с request/scope, риски.
Статус: контракт Phase 2. Описывает обязательный review flow, но не является готовым prompt/шаблоном (шаблоны — в Phase 3).

---

## 1. Суть Codex review

После того как `kilo-notebook-v3` импортировал V3 artifact package и создал journal entry, Codex выполняет review.

Codex review — это обязательный шаг между импортом и human verdict. Без Codex review результат не может быть принят человеком.

Codex не доверяет package на слово. Он проверяет:

1. journal entry (что было импортировано);
2. реальные файлы (что физически появилось в репозитории);
3. сверку результата с V3 request и scope;
4. риски и соответствие acceptance criteria.

## 2. Порядок review

### Шаг 1. Проверить journal

Codex открывает journal entry и проверяет:

- `v3_id` совпадает с V3 request;
- `import_status` не `failed` и не `blocked`;
- `imported_files` содержат ожидаемые файлы;
- `skipped_files` обоснованы;
- `verification_notes` не содержат ошибок.

### Шаг 2. Проверить реальные файлы

Codex открывает каждый файл из `imported_files` и проверяет:

- файл реально существует по указанному пути;
- содержимое соответствует ожиданиям (не пустой, не повреждённый);
- файл не содержит неожиданного содержимого (секреты, вредоносный код);
- файл действительно решает задачу из V3 request.

Codex не проверяет только journal. Он всегда смотрит реальные файлы.

### Шаг 3. Сверить с request и scope

Codex сверяет результат с V3 request:

- все ли ожидаемые файлы созданы;
- scope соблюдён (нет файлов вне `scope`);
- allowed paths соблюдены;
- forbidden paths не нарушены;
- action соответствует (`create` для MVP);
- acceptance criteria из request выполнены.

### Шаг 4. Оценить риски

Codex оценивает:

- есть ли риски, не указанные в `known_risks`;
- нужно ли запросить V2 review для сложных изменений;
- нужно ли явно указать человеку, что проверить вручную.

### Шаг 5. Сформировать verdict

Codex формирует один из verdict-ов:

- `accept` — результат годен, можно показывать человеку.
- `revision_needed` — нужна доработка (см. [`v3_revision_contract.md`](v3_revision_contract.md)).
- `reject` — результат не годен, импорт откатывается или блокируется.

### Шаг 6. Обновить journal

Codex обновляет journal entry:

- добавляет `codex_review_notes`;
- фиксирует свой verdict;
- указывает, что именно человек должен проверить вручную.

## 3. Когда Codex должен вернуть revision

Codex возвращает `revision_needed`, если:

- часть файлов не была импортирована (skipped по неожиданной причине);
- содержимое файлов не соответствует задаче;
- scope или allowed paths нарушены;
- acceptance criteria не выполнены, но проблема исправима через доработку внешнего чата.

## 4. Когда Codex должен вернуть reject

Codex возвращает `reject`, если:

- manifest невалиден;
- checksums не совпадают массово (не единичный сбой);
- пакет содержит нелегальные файлы вне manifest;
- содержимое файлов вредоносное, содержит секреты или явно не относится к задаче;
- scope грубо нарушен (например, `product_code` при `scope: docs_only`);
- revision-цикл не дал результата после двух попыток.

## 5. Когда Codex запрашивает human review

Codex обязан явно попросить человека проверить вручную, если:

- это первый V3 import (pilot);
- scope содержит `scripts` или `product_code`;
- импортированы файлы, меняющие workflow rules;
- Codex не может проверить содержимое автоматически (бинарные файлы, сложная логика);
- Codex сам не уверен в verdict и хочет human gate.

## 6. Чего Codex НЕ делает

Codex не должен:

- доверять package на слово без проверки journal;
- считать, что файл существует только потому, что он написан в manifest;
- пропускать проверку реальных файлов;
- принимать решение за человека;
- выполнять импорт или запись файлов (это задача `kilo-notebook-v3`);
- изменять импортированные файлы без явного revision request.

## 7. Нормализация verdict enum

Codex verdict и human verdict — разные enum. Они не должны смешиваться.

### Codex verdict

```yaml
codex_verdict:
  - accept            # результат годен
  - accept_with_notes # результат годен, но с замечаниями
  - revision_needed   # нужна доработка
  - reject            # результат не годен
```

### Human verdict

```yaml
human_verdict:
  - accept    # принято
  - revision  # отправить на доработку
  - reject    # отклонено
```

См. [`v3_acceptance_policy.md`](v3_acceptance_policy.md) для полного описания human verdict.

## 8. Инварианты review

| Инвариант | Правило |
|-----------|---------|
| Review выполнен | Ни один V3 import не может быть принят без Codex review |
| Journal проверен | Codex читает journal до проверки файлов |
| Реальные файлы проверены | Codex открывает каждый импортированный файл |
| Verdict зафиксирован | Verdict записывается в journal entry |
| Human review запрошен при необходимости | Codex явно указывает, что проверить вручную |

---

## Связанные контракты

- [`v3_journal_contract.md`](v3_journal_contract.md) — journal entry, который Codex проверяет.
- [`v3_revision_contract.md`](v3_revision_contract.md) — как запрашивается доработка.
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md) — как человек принимает/отклоняет результат.
- [`v3_request_contract.md`](v3_request_contract.md) — V3 request, с которым Codex сверяет результат.
- [`v3_scope_policy.md`](v3_scope_policy.md) — уровни scope для проверки.
