# V2 Safety Checklist

Этот checklist обязателен перед каждым V2 push. Kilo должен заполнить его и показать человеку вместе с `/v2 preview`.

## V2 ID

`V2-YYYYMMDD-HHMMSS`

## Дата проверки

YYYY-MM-DD

## Review branch info

- Review branch: `review/v2/YYYYMMDD-HHMMSS-short-topic`
- Base branch: `main`
- Base commit: `<hash>`
- Snapshot commit: `<hash>` (или `not yet committed`)

До push допустимо `not yet committed`. После push, до создания instantiated prompt, это поле обязано быть заменено на фактический snapshot hash.

## Original workspace state (before snapshot)

- Original branch: `<branch name>`
- Original HEAD: `<commit hash>`

### Pre-snapshot `git status --short --branch`

```
<вывод git status --short --branch до любых snapshot-операций>
```

## Snapshot method

- [ ] `separate-worktree` — **preferred**: snapshot готовится в отдельном временном git worktree, основной workspace не трогается
- [ ] `same-worktree-with-restore` — **fallback**: snapshot в том же workspace с обязательным patch/backup restore
- [ ] `other` — **только с явным объяснением**: описать метод и получить human approval

## Git Status Summary (на момент snapshot)

```
<вывод git status --short --branch на review-ветке или в worktree>
```

## WIP files that must remain locally after V2 push

| Файл | Состояние до V2 (M/A/D/untracked) | Должен остаться локально после push? |
|------|-----------------------------------|--------------------------------------|
| `path/to/file` | M | `yes` / `no` / `n/a (not a WIP file)` |

## Файлы

### Changed tracked files (M/A/D)

| Файл | Статус | Проверен |
|------|--------|---------|
| `path/to/file` | M | `ok` / `blocked` / `warning` |

### Untracked files

| Файл | Попадёт в snapshot? | Причина |
|------|-------------------|---------|
| `path/to/file` | `yes` / `no` | ... |

### Suspicious ignored files

| Файл | Почему suspicious | Действие |
|------|------------------|---------|
| `path/to/file` | ... | `block` / `review` / `ok` |

## Проверки безопасности

### Secrets и credentials

- [ ] `.env` / `.env.*` — нет в snapshot
- [ ] key/certificate/credential files — нет в snapshot
- [ ] Пароли, токены, API keys в коде — нет

### Private и local-only пути

- [ ] `_local/**` — нет в snapshot
- [ ] `output/**` — нет в snapshot (кроме `output/README.md`)
- [ ] `arena-prototype-launcher/**` — нет в snapshot
- [ ] `.ai/external_chats/requests/**`, `responses/**`, `tasks/**`, `recorder_packages/**`, `notebook_sources/**`, `notebook_packages/**` — нет в snapshot
- [ ] `.ai/external_reviews/responses/**` — не публикуется в `main` без отдельного решения
- [ ] `.ai/external_reviews/ingest_summaries/**` — не публикуется в `main` без отдельного решения

### Binary и large files

- [ ] Нет large binary files без отдельного разрешения
- [ ] Нет images/assets, которые не должны быть публичными
- [ ] Нет archives (.zip, .tar.gz, .7z)
- [ ] Нет generated build output (`dist/`, `node_modules/`, `.vite/`)

### Logs и debug artifacts

- [ ] Нет log files
- [ ] Нет debug dumps
- [ ] Нет временных test artifacts

### Конфиденциальная информация

- [ ] Нет personal data
- [ ] Нет private paths в тексте файлов
- [ ] Нет internal notes, не предназначенных для публикации

## V2-specific проверки

- [ ] `.ai/external_reviews/requests/**`, `prompts/**`, `safety/**` проверены: в них нет secrets, private paths и запрещённых файлов
- [ ] `.ai/external_reviews/responses/**` и `.ai/external_reviews/ingest_summaries/**` не публикуются в `main` по умолчанию
- [ ] Если request/prompt/safety artifacts уходят в `review/v2/...`, это явно осознано как публичная публикация
- [ ] V2 prompt готов и проверен на отсутствие secrets/local paths
- [ ] Commit-pinned ссылки сформированы (не branch-only links)
- [ ] Compare link сформирован (`base...snapshot`)

Если safety artifact используется дальше после push, эти post-push пункты должны быть обновлены до фактического состояния. Нельзя выдавать внешний prompt, если здесь остаются pre-push placeholders.

## Local workspace preservation / restore

### Post-push verification

- [ ] Возврат на исходную ветку (`<original branch>`)
- [ ] Исходный workspace всё ещё содержит ожидаемые WIP-файлы
- [ ] `git status --short --branch` проверен после push
- [ ] Ни один ожидаемый локальный WIP-файл не потерян
- [ ] Если локальное состояние намеренно изменено, человек явно подтвердил

### Restore result (выбрать один)

- [ ] `preserved` — workspace не менялся (separate-worktree), WIP на месте
- [ ] `restored` — workspace восстановлен после same-worktree-with-restore
- [ ] `restore_failed` — восстановление не удалось; дальнейший lifecycle блокирован
- [ ] `discarded_by_human_decision` — человек явно разрешил не сохранять WIP
- [ ] `unknown_legacy` — только для backfill старых записей V2_navigation.md

### Примечания к local workspace

```
<если restore_failed или discarded_by_human_decision — объяснить причину>
```

## Итог

### Заблокированные файлы (не попавшие в snapshot)

| Файл | Причина блокировки |
|------|-------------------|
| ... | ... |

### Файлы с предупреждениями

| Файл | Предупреждение |
|------|---------------|
| ... | ... |

### Файлы, предложенные в snapshot

| Файл | Статус |
|------|--------|
| ... | `ok` |

## Решение

- [ ] Snapshot безопасен для `/v2 preview`
- [ ] Snapshot НЕ безопасен — требуется ручная проверка
- [ ] Snapshot заблокирован — есть критические проблемы

## Human confirmation

Покажи этот checklist человеку вместе с `/v2 preview`.

Простой вопрос на русском:

```
Проверь safety checklist выше. Разрешаю push review ветки [branch name] в GitHub? Да / Нет
```

Человек должен явно ответить «Да» перед любым V2 push.

## Примечания

- Если любой пункт в «Проверки безопасности» не проходит — файл блокируется.
- Если есть сомнения — файл помечается как `warning` и требует ручной проверки.
- Без заполненного safety checklist и явного «Да» от человека V2 push запрещён.
