# V3 Request Contract

Версия: 0.2
Назначение: формальный контракт V3-запроса к внешнему чату.
Статус: contract layer. Уточнён после Phase 5 root-cause analysis.

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

## 7. Итог

Корректный V3 request обязан:

- явно отделять request-stage от import-stage;
- использовать GitHub-first context mode по умолчанию;
- честно показывать `current_stage`;
- не подменять package review и import ложной готовностью.

## Связанные контракты

- [`v3_scope_policy.md`](v3_scope_policy.md)
- [`v3_artifact_package_contract.md`](v3_artifact_package_contract.md)
- [`v3_storage_policy.md`](v3_storage_policy.md)
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md)
