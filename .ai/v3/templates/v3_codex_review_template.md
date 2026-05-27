# v3_codex_review_template.md — Шаблон Review Note для Codex

Версия: 0.1 (Phase 3)
Назначение: шаблон для Codex при выполнении review после V3 import. Заполняется Codex и добавляется в journal entry.
Используй совместно с: [`codex_v3_review_prompt.md`](../prompts/codex_v3_review_prompt.md) и [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md).

---

## Как использовать

1. После импорта V3 artifact package найди journal entry в `.ai/v3/journals/drafts/<v3_id>_journal.yaml`.
2. Выполни review по [`codex_v3_review_prompt.md`](../prompts/codex_v3_review_prompt.md).
3. Заполни шаблон ниже.
4. Добавь заполненную секцию `codex_review` в journal entry.
5. Сообщи человеку verdict и что проверять.

---

```yaml
codex_review:
  reviewer: "codex"
  verdict: "<accept | accept_with_notes | revision_needed | reject>"
  timestamp: "<ISO 8601 UTC>"
  summary: >
    <Краткое резюме проверки: что проверено, общее впечатление, ключевые находки.
    Пиши на русском, 2-5 предложений.>

  # === Детальные проверки ===

  checks:
    journal_valid: <true | false>
    # Journal существует, заполнен, v3_id совпадает, import_status не failed/blocked.

    files_exist: <true | false>
    # Все файлы из imported_files реально существуют по указанным путям.

    files_match_request: <true | false>
    # Содержимое файлов соответствует задаче из V3 request.

    scope_respected: <true | false>
    # Scope из request соблюдён. Нет файлов вне заявленного scope.

    allowed_paths_respected: <true | false>
    # Все импортированные файлы внутри allowed_paths.

    forbidden_paths_respected: <true | false>
    # Ни один файл не попал в forbidden_paths.

    acceptance_criteria_met: <true | false>
    # Все acceptance criteria из request выполнены.

  # === Заметки ===

  notes: >
    <Подробные заметки. На русском.>
    
    **Что проверено:**
    - [перечисление]
    
    **Файлы (импортированы):**
    - [список]
    
    **Файлы (пропущены):**
    - [список с причинами]
    
    **Расхождения с request:**
    - [если есть]
    
    **Дополнительные риски (не из known_risks):**
    - [если есть]
    
    **Общее заключение:**
    - [итоговая оценка]

  # === Human review ===

  human_review_required: <true | false>
  # true если: первый pilot, scope scripts/product_code, workflow rules,
  #   бинарные файлы, сложная логика, неуверенность Codex.

  human_review_items:
    # Конкретные пункты для ручной проверки. На русском, простым языком.
    - "<Что открыть, на что посмотреть, что должно произойти.>"
    # - "<Второй пункт, если нужно>"

  # === Рекомендация ===

  recommendation: >
    <Что Codex рекомендует человеку: accept / revision / reject. Почему.>
```

---

## Пример заполненной секции

```yaml
codex_review:
  reviewer: "codex"
  verdict: "accept_with_notes"
  timestamp: "2026-05-27T16:30:00Z"
  summary: >
    Проверен journal entry и 9 контрактов V3. Все файлы существуют,
    содержимое соответствует задаче, scope соблюдён. Два файла имеют
    мелкие замечания по wording, не блокируют приёмку.

  checks:
    journal_valid: true
    files_exist: true
    files_match_request: true
    scope_respected: true
    allowed_paths_respected: true
    forbidden_paths_respected: true
    acceptance_criteria_met: true

  notes: >
    **Что проверено:**
    - Journal entry V3-20260527-153000-v3-contracts_journal.yaml
    - 9 контрактов в .ai/v3/contracts/
    - Сверка с V3 request и scope
    
    **Файлы (импортированы):**
    - v3_request_contract.md
    - v3_artifact_package_contract.md
    - v3_manifest_contract.md
    - v3_journal_contract.md
    - v3_codex_review_contract.md
    - v3_revision_contract.md
    - v3_storage_policy.md
    - v3_scope_policy.md
    - v3_acceptance_policy.md
    
    **Файлы (пропущены):**
    - нет
    
    **Расхождения с request:**
    - нет критических. Мелкие замечания по wording в двух файлах.
    
    **Дополнительные риски:**
    - Контракты описывают процесс, но runtime ещё не готов (ожидаемо для Phase 2).
    
    **Общее заключение:**
    - Результат годен. Можно показывать человеку.

  human_review_required: true
  human_review_items:
    - "Открыть .ai/v3/contracts/README.md и убедиться, что список контрактов полный."
    - "Открыть v3_request_contract.md и проверить, что обязательные поля перечислены."
    - "Открыть v3_acceptance_policy.md и проверить verdict enum."

  recommendation: >
    Рекомендую accept. Мелкие замечания по wording можно поправить
    локально или отложить до V1 critique (Phase 6).
```

---

## Правила заполнения

### `verdict`
- Всегда один из: `accept`, `accept_with_notes`, `revision_needed`, `reject`.
- Не используй human verdict enum (`accept`, `revision`, `reject`).

### `checks`
- Каждый флаг — строго `true` или `false`.
- Если `false` — объясни в `notes`, почему.

### `human_review_required`
- `true` обязательно для: первого pilot, `scripts`/`product_code` scope, workflow rules, неуверенности Codex.
- `false` допустимо для: `docs_only` scope без рисков.

### `human_review_items`
- Конкретные инструкции на русском. Не «проверь файлы», а «открой X, посмотри на Y, убедись что Z».
- Если `human_review_required: false`, список может быть пустым.

---

## Связанные документы

- [`codex_v3_review_prompt.md`](../prompts/codex_v3_review_prompt.md) — промпт для Codex review.
- [`v3_codex_review_contract.md`](../contracts/v3_codex_review_contract.md) — формальный контракт.
- [`v3_journal_contract.md`](../contracts/v3_journal_contract.md) — куда добавляется review note.
- [`v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md) — политика приёмки.
