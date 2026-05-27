# V3 Storage Policy

Версия: 0.1 (Phase 2)
Назначение: формальная политика хранения V3 артефактов — какие файлы tracked, какие local-only, что считается persistent repo-layer, что — локальным runtime.
Статус: контракт Phase 2. Описывает правила хранения, но не является готовым runtime/cleanup script.

---

## 1. Принцип

V3 workflow создаёт несколько типов артефактов. Не все они должны попадать в Git. Разделение:

- **Persistent repo-layer** — файлы, которые должны быть в Git: контракты, навигация, accepted journal entries, stable docs.
- **Local runtime** — артефакты, которые создаются и используются в рамках одного workflow цикла: raw ZIP, staging-папки, temporary journal drafts, rejected packages.
- **Human-decision zone** — артефакты, которые становятся persistent только после явного решения человека (accepted journal entries, V3 navigation updates).

## 2. Классификация артефактов

### 2.1. Persistent (tracked в Git)

| Артефакт | Путь | Условие |
|----------|------|---------|
| V3 contracts | `.ai/v3/contracts/*.md` | Сразу после создания |
| V3 README | `.ai/v3/README.md` | Сразу после создания |
| V3 navigation | `.ai/v3/V3_navigation.md` | После каждого accepted import |
| V3 journal (accepted) | `.ai/v3/journals/V3-*_journal.yaml` | Только после human accept |
| V3 docs | `.ai/v3/docs/*.md` | После принятия |
| V3 prompts | `.ai/v3/prompts/*.md` | После принятия (Phase 3) |
| V3 templates | `.ai/v3/templates/*` | После принятия (Phase 3) |

### 2.2. Local-only (не трекаются в Git)

| Артефакт | Путь | Правило |
|----------|------|---------|
| Raw ZIP | `.ai/v3/staging/*.zip` | Удаляется после успешного импорта или при очистке |
| Staging распаковка | `.ai/v3/staging/V3-*/` | Удаляется после импорта |
| Rejected packages | `.ai/v3/staging/rejected/` | Хранятся до очистки, не публикуются |
| Temporary journal drafts | `.ai/v3/journals/drafts/` | Удаляются после финализации. Codex может читать pending draft до human accept в рамках review flow |
| Revision attempt packages | `.ai/v3/staging/revisions/` | Хранятся до завершения revision цикла |

### 2.3. Human-decision zone

| Артефакт | Путь | Правило |
|----------|------|---------|
| Journal entry (pending) | `.ai/v3/journals/drafts/V3-*_journal.yaml` | Не публикуется до human accept; после accept перемещается в `.ai/v3/journals/` и становится persistent |
| V3 navigation update | `.ai/v3/V3_navigation.md` | Не коммитится до accept всего V3 import |
| Review notes | journal entry | Аналогично journal |

## 3. Правила по умолчанию

### 3.1. Не публиковать по умолчанию

Ни один V3 runtime артефакт не публикуется в Git по умолчанию. Публикация — это явное действие после human accept.

Исключение: stable contracts, README, navigation, journal (после accept). Эти файлы могут быть включены в коммит как часть workflow checkpoint.

### 3.2. Raw ZIP и staging — local-only

- Raw ZIP-архивы хранятся в `.ai/v3/staging/`.
- После успешного импорта raw ZIP может быть удалён.
- staging-папки не попадают в Git.

### 3.3. Cleanup после accept

После human accept:

- raw ZIP удаляется из staging;
- staging-папка очищается;
- journal entry (теперь accepted) остаётся как persistent;
- V3 navigation обновляется.

### 3.4. Cleanup после reject

После human reject:

- raw ZIP перемещается в `.ai/v3/staging/rejected/` для возможного анализа;
- journal entry помечается как `rejected`;
- staging-папка очищается.

## 4. Что НЕЛЬЗЯ публиковать

Следующие артефакты никогда не должны публиковаться в Git:

- бинарные файлы из ZIP (если не были явно разрешены);
- external chat response, содержащие V3 package в текстовой форме;
- секреты, токены, пароли, ключи;
- внутренние draft-версии контрактов (только финальные);
- rejected packages (могут храниться локально для анализа, но не публикуются).

## 5. V staging directory

```
.ai/v3/staging/
  V3-YYYYMMDD-HHMMSS-<slug>/
    ... распакованный ZIP ...
  rejected/
    V3-YYYYMMDD-HHMMSS-<slug>/
      ... rejected package ...
  revisions/
    V3-YYYYMMDD-HHMMSS-<slug>-attempt-2/
      ... revision package ...
```

## 6. Persistent storage (tracked)

```
.ai/v3/
  contracts/
    v3_request_contract.md
    v3_artifact_package_contract.md
    v3_manifest_contract.md
    v3_journal_contract.md
    v3_codex_review_contract.md
    v3_revision_contract.md
    v3_storage_policy.md
    v3_scope_policy.md
    v3_acceptance_policy.md
  journal/
    V3-YYYYMMDD-HHMMSS-<slug>_journal.yaml  (только accepted)
  V3_navigation.md
  README.md
```

---

## Связанные контракты

- [`v3_journal_contract.md`](v3_journal_contract.md) — journal entry, который переходит из local-only в persistent после accept.
- [`v3_acceptance_policy.md`](v3_acceptance_policy.md) — после какого verdict артефакты становятся persistent.
- [`v3_codex_review_contract.md`](v3_codex_review_contract.md) — review-шаг, после которого определяется статус.
