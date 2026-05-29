# V3 Request Contract

Версия: 0.3
Назначение: формальный контракт V3-запроса к внешнему чату.
Статус: contract layer. Уточнён после Phase 5 root-cause analysis. Добавлена поддержка post-import testing.

---

## 1. Суть V3 request

V3 request - это структурированная постановка задачи для внешнего чата, который должен подготовить artifact package.

Важно:

- request не равен package;
- package не равен imported result;
- imported result не равен accepted result.

## 2. Обязательные поля

Любой V3 request обязан содержать:

| Поле | Описание |
|------|----------|
| `v3_id` | Идентификатор в формате `V3-YYYYMMDD-HHMMSS-<slug>` |
| `task_title` | Короткое название задачи |
| `generated_by` | `codex`, `human` или `codex+human` |
| `action` | Для MVP только `create` |
| `scope` | Уровень scope |
| `current_stage` | `external_artifact_generation_only`, `pre_kilo_package_revision` или `import_stage` |
| `context_summary` | Краткий контекст |
| `task_description` | Что именно нужно создать |
| `allowed_paths` | Куда разрешено писать |
| `forbidden_paths` | Куда писать нельзя |
| `expected_files` | Ожидаемые project-relative target paths |
| `package_format` | Для MVP: `zip` |
| `acceptance_criteria` | Проверяемые критерии |
| `known_risks` | Известные риски |
| `post_import_testing` | Режим post-import testing: `required`, `optional` или `waived`. Для `docs_only` по умолчанию `waived`. Если `mode = required`, request должен требовать `POST_IMPORT_TEST_PROMPT.md` от внешнего чата |
| `no_repo_access_statement` | Явное указание, что у внешнего чата нет repo access |

## 3. Current stage - обязательный разделитель

`current_stage` нужен, чтобы не смешивать разные части V3 lifecycle.

### `external_artifact_generation_only`

Используется, когда:

- нужен только package generation test;
- Kilo import ещё не начался;
- package позже может быть review-нут отдельно.

При этом request не должен обещать немедленный import.

### `pre_kilo_package_revision`

Используется, когда:

- package уже существует;
- сейчас нужен review package/revision loop;
- import-stage ещё не выбран.

### `import_stage`

Используется только когда:

- package уже реально существует;
- package review уже пройден;
- `Kilo Notebook V3` реально настроен в UI;
- import-stage выбран явно.

## 4. GitHub-first external context mode

По умолчанию request должен передавать внешний контекст так:

```text
commit-pinned GitHub raw links -> внешний чат читает их сам
```

Правила:

- локальный путь сам по себе бесполезен для внешнего чата;
- ручная передача context files не является default mode;
- fallback excerpts допустимы только если GitHub link невозможен или явно недостаточен.

## 5. Allowed/forbidden paths

- пути всегда project-relative;
- `forbidden_paths` имеют приоритет над `allowed_paths`;
- `allowed_paths` должны быть согласованы со `scope`.

## 6. Request не должен обещать то, что не доказано

Request не должен:

- обещать, что package уже будет импортирован;
- обещать, что `Kilo Notebook V3` уже настроен;
- обещать, что staging path уже canonicalized;
- делать вид, что внешний чат видит локальный repo без GitHub links/excerpts.

## 7. Post-import testing в request

### 7.1. Три режима

Request обязан явно указать один из трёх режимов post-import testing:

| mode | Семантика | Prompt в package | Acceptance gate |
|------|-----------|-----------------|-----------------|
| `required` | Testing обязателен. Внешний чат должен создать `POST_IMPORT_TEST_PROMPT.md` | Обязателен | Да |
| `optional` | Prompt полезен, но не блокирует acceptance. Внешний чат может создать prompt | Опционален | Нет |
| `waived` | Testing явно не нужен | Не требуется | Нет |

### 7.2. Что request НЕ делает

Request не должен:

- писать заранее весь конкретный test prompt сам — финальные файлы создаёт внешний чат;
- требовать `POST_IMPORT_TEST_PROMPT.md` вообще всегда без разбора scope;
- подменять `optional` на `required` или наоборот без явного обоснования.

### 7.3. Правила по scope

| Scope | Default mode | Примечание |
|-------|-------------|------------|
| `docs_only` | `waived` | Если request явно не усиливает testing до `optional` или `required` |
| `workflow_docs` | `waived` или `optional` | Зависит от рисков |
| `schemas` | `optional` или `required` | Зависит от того, нужна ли проверка schema integrity |
| `scripts` | `required` | Скрипты нужно проверять перед запуском |
| `product_code` | `required` | Code-affecting изменения требуют machine-check |

### 7.4. Что request требует от внешнего чата

**При `mode = required`:**
- Создать `POST_IMPORT_TEST_PROMPT.md` в корне ZIP.
- Разделить prompt на `Machine checks` и `Human checks`.
- Не выдумывать результаты тестов.
- Не утверждать, что внешний чат уже запускал тесты.
- Сгенерировать конкретный prompt по фактически созданным файлам, а не абстрактный.

**При `mode = optional`:**
- Внешний чат **может** создать `POST_IMPORT_TEST_PROMPT.md`, если считает проверки полезными.
- Если prompt создан — он будет показан человеку после импорта, но не блокирует acceptance.
- Требования к содержимому те же, что при `required`.

**При `mode = waived`:**
- `POST_IMPORT_TEST_PROMPT.md` не требуется.

## 8. Итог

Корректный V3 request обязан:

- явно отделять request-stage от import-stage;
- использовать GitHub-first context mode по умолчанию;
- честно показывать `current_stage`;
- не подменять package review и import ложной готовностью;
- явно указывать `post_import_testing.mode` как `required`, `optional` или `waived`.

## Связанные контракты

- [`v3_scope_policy.md`](v3_scope_policy.md)
- [`v3_artifact_package_contract.md`](v3_artifact_package_contract.md)
- [`v3_storage_policy.md`](v3_storage_policy.md)
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md)
