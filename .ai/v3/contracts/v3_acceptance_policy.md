# V3 Acceptance Policy

Версия: 0.3
Назначение: формальная политика того, как человек принимает, отклоняет или отправляет на доработку результат V3 import-stage.
Статус: contract layer. Уточнена под raw-input notebook flow.

---

## 1. Важное различие

Acceptance flow начинается не с момента получения ZIP, а только после реального import-stage.

Нужно различать:

- внешний package получен;
- package review выполнен;
- import-stage выполнен;
- Codex review выполнен;
- human verdict дан.

ZIP сам по себе не входит в acceptance flow.

## 2. Import gates before acceptance flow

Acceptance/import chain нельзя начинать, пока одновременно не выполнены все условия:

1. Реальный external package существует.
2. Package review уже выполнен.
3. `Kilo Notebook V3` реально настроен в UI.
4. Известен raw package source.
5. Текущий шаг явно объявлен import-stage.
6. Реальный git repo root определён и используется как единственный target root.

Если это не так, статус должен оставаться pre-Kilo:

- `external_package_received`
- `package_reviewed`
- `kilo_mode_not_configured`

## 3. Minimal acceptance gates after import

После того как import-stage реально начался, ни один результат не может быть принят без:

| Gate | Проверка | Кто выполняет |
|---|---|---|
| Repo root valid | `git rev-parse --show-toplevel` дал правильный repo root, все relative paths разрешались от него | `kilo-notebook-v3` |
| Package valid | manifest/checksums/paths валидны | `kilo-notebook-v3` |
| Journal created | journal draft существует как подробный import trace | `kilo-notebook-v3` |
| Navigation updated | lifecycle entry обновлена как короткий индекс цикла | `kilo-notebook-v3` |
| Codex review done | Codex проверил journal и реальные файлы | Codex |
| Human check done | человек дал verdict | Human |

## 4. Verdict enum

### Codex verdict

```yaml
codex_verdict:
  - accept
  - accept_with_notes
  - revision_needed
  - reject
```

### Human verdict

```yaml
human_verdict:
  - accept
  - revision
  - reject
```

## 5. Что считается accept/revision/reject

### `accept`

- import реально выполнен;
- файлы соответствуют задаче;
- scope соблюдён;
- Codex verdict = `accept` или `accept_with_notes`;
- человек подтвердил.

### `revision`

- package/import частично годен;
- проблемы исправимы через revision loop;
- acceptance ещё не наступил.

### `reject`

- manifest invalid;
- checksums не совпадают;
- repo root не определён или relative paths были разрешены не от git repo root;
- scope грубо нарушен;
- package/import lane невалиден;
- revision loop исчерпан;
- или import вообще не должен был начинаться из-за несоблюдения gates.

## 6. Что не является acceptance

- валидный ZIP package без import;
- pre-Kilo package review;
- setup guide без реального UI confirmation;
- Codex verdict без human verdict;
- наличие файлов в repo без полного review chain.

## 7. Rule for notebook-v3 import run

Запуск `Kilo Notebook V3` нельзя делать до выполнения import gates из секции 2.

Если gates не выполнены, корректный статус:

```text
external_package_received_but_not_import_ready
```

или:

```text
package_reviewed
```

## Связанные контракты

- [`v3_storage_policy.md`](v3_storage_policy.md)
- [`v3_request_contract.md`](v3_request_contract.md)
- [`v3_journal_contract.md`](v3_journal_contract.md)
- [`v3_codex_review_contract.md`](v3_codex_review_contract.md)
