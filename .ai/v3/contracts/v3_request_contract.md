# V3 Request Contract

Версия: 0.1 (Phase 2)
Назначение: формальный контракт V3-запроса — что должно быть в запросе, который Codex или человек передаёт внешнему чату для генерации artifact package.
Статус: контракт Phase 2. Описывает обязательные правила, но не является готовым runtime/prompt-шаблоном (шаблоны — в Phase 3).

---

## 1. Суть V3 request

V3 request — это структурированная постановка задачи для внешнего чата. Это не обычный prompt, не `/v1` вопрос и не `/r1` full external launch package.

V3 request говорит внешнему чату:

- какую задачу нужно решить;
- в каком формате вернуть результат;
- какие файлы создать;
- куда их положить внутри пакета;
- какие зоны запрещены;
- что модель не имеет доступа к репозиторию и не должна утверждать обратное.

## 2. Обязательные поля V3 request

Любой V3 request, независимо от scope и action, обязан содержать:

| Поле | Описание |
|------|----------|
| `v3_id` | Уникальный идентификатор запроса в формате `V3-YYYYMMDD-HHMMSS-<slug>` |
| `task_title` | Короткое название задачи на русском или английском |
| `generated_by` | Кто подготовил запрос: `codex`, `human` или `codex+human` |
| `action` | Действие. Для MVP допустимо только `create` |
| `scope` | Уровень scope запроса (см. [`v3_scope_policy.md`](v3_scope_policy.md)) |
| `context_summary` | Краткое описание контекста: что за проект, что уже сделано, зачем эта задача |
| `task_description` | Конкретное описание задачи: что должно быть создано и зачем |
| `allowed_paths` | Список project-relative путей, куда разрешено писать файлы |
| `forbidden_paths` | Список project-relative путей, куда запрещено писать файлы |
| `expected_files` | Список ожидаемых файлов — project-relative target paths (например, `.ai/v3/contracts/v3_request_contract.md`). Внешний пакет кладёт их под `files/<project-relative-path>`. |
| `package_format` | Формат пакета. Для MVP: `zip` |
| `acceptance_criteria` | Критерии приёмки результата |
| `known_risks` | Известные риски задачи |
| `no_repo_access_statement` | Явное указание, что модель не имеет доступа к репозиторию |

### 2.1. `scope` как обязательное поле

`scope` задаёт уровень допустимых изменений. Возможные значения:

- `docs_only` — только документация (`.md` файлы);
- `workflow_docs` — workflow-документация (`.ai/` и `docs/`);
- `schemas` — схемы данных, контракты, спецификации;
- `scripts` — скрипты и утилиты;
- `product_code` — код продукта (в MVP не используется).

Scope определяет, какие пути могут быть в `allowed_paths`. Нельзя указать `scope: docs_only` и `allowed_paths: src/`.

Подробнее — в [`v3_scope_policy.md`](v3_scope_policy.md).

### 2.2. `action` для MVP

На Phase 2 допустимо только одно значение:

- `action: create` — создание новых файлов.

`action: update`, `action: delete`, `action: overwrite` в MVP не поддерживаются и не должны использоваться в V3 request на текущей фазе.

## 3. Allowed paths и forbidden paths

### 3.1. Правила allowed paths

- Пути задаются как project-relative (от корня репозитория).
- Можно использовать префиксы директорий (например, `.ai/v3/` покрывает всю вложенность).
- Можно указывать конкретные файлы.
- Allowed paths должны быть согласованы со `scope`.

### 3.2. Правила forbidden paths

- Forbidden paths имеют приоритет над allowed paths: если путь попадает и в allowed, и в forbidden, он ЗАПРЕЩЁН.
- По умолчанию всегда запрещены:
  - `.git/`
  - `node_modules/`
  - `dist/`, `build/`
  - `coverage/`
  - lock-файлы (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
  - `.env` и файлы с секретами
- Дополнительные forbidden paths задаются в каждом конкретном request.

### 3.3. Пример

```yaml
allowed_paths:
  - ".ai/v3/"
  - "docs/v3/"

forbidden_paths:
  - ".git/"
  - "node_modules/"
  - "dist/"
  - "src/"
```

## 4. V3 request не равен artifact package

Важное различие:

- **V3 request** — это постановка задачи, которую Codex/человек передаёт внешнему чату.
- **V3 artifact package** — это результат работы внешнего чата: ZIP с manifest, README, checksums и файлами.

Внешний чат получает request и создаёт package. Он не должен:

- утверждать, что уже изменил репозиторий;
- подменять процесс импорта;
- писать файлы напрямую;
- игнорировать manifest.

См. [`v3_artifact_package_contract.md`](v3_artifact_package_contract.md).

## 5. Что request НЕ содержит

Request не содержит:

- готовый manifest (его создаёт внешний чат в ответ);
- checksums (их создаёт внешний чат);
- инструкции для KiloCode (их внешний чат пишет в `README_FOR_KILO.md`);
- инструкции для Codex (их внешний чат пишет в `README_FOR_CODEX.md`);
- файлы проекта (их внешний чат кладёт в `files/`).

Request — это только постановка задачи. Всё остальное создаётся внешним чатом.

## 6. Итоговый контракт

Любой V3 request обязан:

- содержать все обязательные поля из секции 2;
- использовать `action: create` (MVP);
- задавать `scope` одним из допустимых значений;
- явно отделять request от package;
- содержать `no_repo_access_statement`;
- не обещать внешнему чату доступ к репозиторию.

Нарушение любого из этих пунктов делает request невалидным для V3 workflow.

---

## Связанные контракты

- [`v3_artifact_package_contract.md`](v3_artifact_package_contract.md) — структура V3 artifact package.
- [`v3_manifest_contract.md`](v3_manifest_contract.md) — контракт manifest.yaml.
- [`v3_scope_policy.md`](v3_scope_policy.md) — уровни scope и acceptance gates.
- [`v3_storage_policy.md`](v3_storage_policy.md) — что tracked, что local-only.
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md) — как человек принимает/отклоняет результат.
