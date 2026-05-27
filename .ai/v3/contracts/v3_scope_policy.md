# V3 Scope Policy

Версия: 0.1 (Phase 2)
Назначение: формальная политика scope — какие уровни допустимых изменений существуют в V3 workflow, как они соотносятся с allowed paths и acceptance gates.
Статус: контракт Phase 2. Описывает уровни scope как policy layer; MVP не обязан разрешать все уровни в первом pilot.

---

## 1. Суть scope

Scope — это обязательное поле V3 request (см. [`v3_request_contract.md`](v3_request_contract.md)), которое определяет, к каким файлам проекта может обращаться V3 artifact package.

Scope — это policy-level защита. Даже если allowed paths технически шире, scope задаёт смысловую границу задачи и не позволяет случайно перейти в другую зону.

## 2. Уровни scope

### 2.1. `docs_only`

- Только `.md` файлы.
- Запрещены: любые скрипты, код, схемы, конфиги, шаблоны, валидаторы.
- Типичные задачи: документация, заметки, спецификации.
- Примеры: `docs/v3/setup_guide.md`, `docs/workflow/prototyping_workflow.md`.
- Не включает: контракты workflow (`.ai/v3/contracts/*.md`) — они относятся к `workflow_docs`.

### 2.2. `workflow_docs`

- `.md` файлы в `.ai/` и `docs/`.
- Включает: агентные протоколы, mode contracts, контракты, политики, навигацию, планы.
- Запрещены: product code, скрипты, схемы данных.
- Типичные задачи: workflow docs, rules, contracts, policies.

### 2.3. `schemas`

- Yaml, JSON, TypeScript type definitions, схемы данных.
- Включает: контракты данных, entity definitions, валидационные схемы.
- Ограничение: только data layer, без runtime execution.
- Типичные задачи: schemas для module packages, entity definitions, data contracts.

### 2.4. `scripts`

- Исполняемые файлы: Python, TypeScript/JavaScript, shell.
- Включает: валидаторы, конвертеры, утилиты, вспомогательные скрипты.
- Требует: обязательный Codex review, обязательный human review.
- Типичные задачи: staging helpers, validators, converters.

### 2.5. `product_code`

- Любые файлы продукта (например, `table-sandbox/src/`, `table-sandbox/renderer/`).
- Высокий риск. Требует:
  - узкий `allowed_paths`;
  - обязательный Codex review;
  - обязательный human review;
  - при крупных изменениях — V2 review до принятия.
- Типичные задачи: bounded code changes, narrow feature добавления.

## 3. Scope и allowed paths

Scope определяет, какие пути могут быть в `allowed_paths`.

| Scope | Допустимые allowed_paths |
|-------|--------------------------|
| `docs_only` | Любые пути, оканчивающиеся на `.md` |
| `workflow_docs` | `.ai/`, `docs/` |
| `schemas` | `.ai/v3/`, `canon/`, `docs/schemas/` |
| `scripts` | `scripts/` |
| `product_code` | `table-sandbox/`, `src/` (но не `.git/`, `node_modules/`) |

Нарушение: `scope: docs_only` с `allowed_paths: src/` — невалидно.

## 4. Acceptance gates для каждого уровня

Каждый уровень scope имеет минимальные acceptance gates:

| Scope | Codex review | Human review | V2 review (если крупные изменения) |
|-------|-------------|-------------|-----------------------------------|
| `docs_only` | Обязателен | Suggested | Не требуется |
| `workflow_docs` | Обязателен | Required для workflow rules | Не требуется |
| `schemas` | Обязателен | Required | Suggested |
| `scripts` | Обязателен | Required | Suggested |
| `product_code` | Обязателен | Required | Required для крупных изменений |

### 4.1. Дополнительные gates для `scripts`

- Codex должен прочитать и проверить каждый скрипт.
- Человек должен явно подтвердить, что разрешает выполнение скрипта.
- Скрипт не должен выполняться автоматически после импорта.

### 4.2. Дополнительные gates для `product_code`

- `allowed_paths` должен быть максимально узким.
- `forbidden_paths` должен включать все критические зоны.
- Ожидаемый diff должен быть описан в request.
- Codex проверяет diff до human review.
- Для крупных изменений — V2 review на snapshot.

## 5. MVP-ограничения

Первый pilot V3 (Phase 5) работает только с `docs_only`.

`workflow_docs` и `schemas` — допустимы в следующих pilots по решению человека.

`scripts` — не разрешены до Phase 7 (после hardening через V2).

`product_code` — не разрешён до Phase 8 (после успешного docs-only pilot и V2 review).

## 6. Что scope НЕ определяет

Scope не определяет:

- какой `action` используется (`create` для MVP);
- сколько файлов может быть в пакете;
- какой внешний чат генерирует package;
- кто выполняет review.

Это отдельные поля V3 request.

---

## Связанные контракты

- [`v3_request_contract.md`](v3_request_contract.md) — scope как обязательное поле request.
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md) — gates для каждого уровня scope.
- [`v3_codex_review_contract.md`](v3_codex_review_contract.md) — Codex проверяет scope при review.
- [`v3_storage_policy.md`](v3_storage_policy.md) — что persistent, что local-only для разных scope.
