# codex_v3_review_prompt.md — Промпт для Codex Review после V3 Import

Версия: 0.1 (Phase 3)
Назначение: промпт для Codex, выполняющего review после того, как `Kilo Notebook V3` импортировал V3 artifact package и создал journal entry.
Статус: рабочий prompt. Опирается на Phase 2 контракты, особенно [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md).

---

## 1. Когда использовать этот промпт

Этот промпт используется Codex после того, как:

1. Внешний чат создал V3 artifact package (ZIP).
2. `Kilo Notebook V3` импортировал package.
3. Journal entry создан в `.ai/v3/journals/drafts/<v3_id>_journal.yaml`.

Codex review — обязательный шаг между импортом и human verdict. Без Codex review результат не может быть принят человеком.

---

## 2. Промпт

```text
Ты выполняешь Codex review после V3 import.

Твоя задача — проверить результат импорта V3 artifact package: journal entry, реальные файлы, сверку с V3 request и scope, риски.

Ты НЕ доверяешь package на слово. Ты проверяешь journal и реальные файлы. Ты не принимаешь решение за человека, но даёшь verdict и рекомендации.

---

## Входные данные

Тебе доступны:
1. V3 request — исходный запрос, отправленный внешнему чату.
2. Journal entry — `.ai/v3/journals/drafts/<v3_id>_journal.yaml`.
3. Импортированные файлы — физически в репозитории.
4. Staging-папка с распакованным пакетом — `.ai/v3/staging/<имя_папки>/`.

Если journal entry отсутствует — остановись. Статус: `blocked`. Причина: `no_journal`.

---

## Порядок review

### Шаг 1. Проверить journal

Открой journal entry и проверь:

- [ ] `v3_id` совпадает с V3 ID из request.
- [ ] `import_status` не `failed` и не `blocked`. Если `failed` или `blocked` — дальнейший review бессмыслен, verdict: `reject`.
- [ ] `imported_files` содержат ожидаемые файлы (сверь с `expected_files` из request).
- [ ] `skipped_files` обоснованы: причина каждого skip понятна и допустима.
- [ ] `verification_notes` не содержат ошибок: все ключи `true` или явно указаны проблемы.

### Шаг 2. Проверить реальные файлы

Для КАЖДОГО файла из `imported_files`:

1. Открой файл по project-relative пути.
2. Проверь:
   - Файл реально существует.
   - Файл не пуст (если не ожидается пустым).
   - Содержимое соответствует задаче из V3 request.
   - Файл не содержит секретов, токенов, паролей.
   - Файл не содержит вредоносного кода (для скриптов).
   - Формат файла соответствует ожидаемому (markdown, yaml, json, etc.).

Если файл не существует, но указан в `imported_files` — это ошибка. Зафиксируй.

### Шаг 3. Сверить с request и scope

Сверь результат с V3 request:

- [ ] Все ли `expected_files` из request созданы? Отсутствующие — зафиксируй.
- [ ] `scope` соблюдён? Нет файлов вне заявленного scope?
- [ ] `allowed_paths` соблюдены? Все импортированные файлы внутри allowed_paths?
- [ ] `forbidden_paths` не нарушены? Ни один файл не попал в forbidden_paths?
- [ ] `action` соответствует? Для MVP — только `create`.
- [ ] `acceptance_criteria` из request выполнены?

### Шаг 4. Оценить риски

Оцени:

- Есть ли риски, не указанные в `known_risks` манифеста?
- Нужно ли запросить V2 review для сложных изменений?
- Нужно ли явно указать человеку, что проверить вручную?
- Есть ли неожиданные изменения (файлы не из expected_files)?

### Шаг 5. Сформировать verdict

Выбери один из verdict-ов:

- **`accept`** — результат годен. Все проверки пройдены. Можно показывать человеку.
- **`accept_with_notes`** — результат годен, но с замечаниями. Замечания не блокируют приёмку, но человек должен их увидеть.
- **`revision_needed`** — нужна доработка. Проблемы исправимы через повторный запрос к внешнему чату.
- **`reject`** — результат не годен. Импорт не должен быть принят.

**Когда `revision_needed`:**
- Часть файлов не импортирована (skipped по неожиданной причине).
- Содержимое не полностью соответствует задаче.
- Scope или allowed paths нарушены, но исправимы.
- Acceptance criteria выполнены частично.

**Когда `reject`:**
- Manifest невалиден.
- Checksums не совпадают массово.
- Пакет содержит нелегальные файлы вне manifest.
- Содержимое вредоносное или содержит секреты.
- Scope грубо нарушен (например, product_code при scope: docs_only).
- Два revision цикла уже провалились.

### Шаг 6. Обновить journal

Обнови journal entry — добавь секцию `codex_review`:

```yaml
codex_review:
  reviewer: "codex"
  verdict: "<accept | accept_with_notes | revision_needed | reject>"
  timestamp: "<ISO 8601 UTC>"
  summary: "<краткое резюме проверки>"

  checks:
    journal_valid: true
    files_exist: true
    files_match_request: true
    scope_respected: true
    allowed_paths_respected: true
    forbidden_paths_respected: true
    acceptance_criteria_met: true

  notes: "<подробные заметки>"

  human_review_required: true
  human_review_items:
    - "<что проверить человеку>"
```

### Шаг 7. Сообщить человеку

Выдай короткое резюме:

- Verdict.
- Что проверено.
- Что импортировано (список файлов).
- Что пропущено (список с причинами).
- Риски.
- Что человек должен проверить вручную (если нужно).
- Следующий шаг: accept / revision / reject.

---

## Когда запрашивать human review

Ты обязан явно попросить человека проверить вручную, если:

- Это первый V3 import (pilot).
- Scope содержит `scripts` или `product_code`.
- Импортированы файлы, меняющие workflow rules.
- Ты не можешь проверить содержимое автоматически (бинарные файлы, сложная логика).
- Ты сам не уверен в verdict и хочешь human gate.

---

## Что ты НЕ делаешь

- НЕ доверяешь package на слово без проверки journal.
- НЕ считаешь, что файл существует только потому, что он в manifest.
- НЕ пропускаешь проверку реальных файлов.
- НЕ принимаешь решение за человека.
- НЕ выполняешь импорт или запись файлов (это задача Kilo Notebook V3).
- НЕ изменяешь импортированные файлы без явного revision request.
- НЕ превращаешь V3_navigation.md в дубль journal.
- V3_navigation.md уже может быть обновлён как lifecycle index до human accept.
```

---

## 3. Нормализация verdict enum (напоминание)

Codex verdict и human verdict — разные enum. НЕ смешивай их.

### Codex verdict (ты)

| Verdict | Когда |
|---------|-------|
| `accept` | Всё хорошо, можно показывать человеку |
| `accept_with_notes` | Годен, но с замечаниями |
| `revision_needed` | Нужна доработка внешним чатом |
| `reject` | Не годен, импорт должен быть заблокирован |

### Human verdict (человек)

| Verdict | Когда |
|---------|-------|
| `accept` | Принято |
| `revision` | Отправить на доработку |
| `reject` | Отклонено |

См. [`v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md).

---

## 4. Связанные документы

- [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md) — формальный контракт Codex review.
- [`v3_journal_contract.md`](../contracts/v3_journal_contract.md) — контракт journal entry.
- [`v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md) — политика приёмки.
- [`v3_revision_contract.md`](../contracts/v3_revision_contract.md) — контракт revision.
- [`v3_request_contract.md`](../contracts/v3_request_contract.md) — контракт V3 request.
- [`v3_scope_policy.md`](../contracts/v3_scope_policy.md) — уровни scope.
- [`codex_v3_review_template.md`](../templates/v3_codex_review_template.md) — шаблон review note.
