# V3 Acceptance Policy

Версия: 0.6 (Phase 6 lifecycle hardening)
Назначение: формальная политика того, как человек принимает, отклоняет или отправляет на доработку результат V3 import-stage. Добавлены accepted journal promotion rules.
Статус: contract layer. Добавлен post-import testing gate с canonical machine-check report и waiver path. Добавлены accepted journal promotion rules и разделение draft/accepted (Phase 6).

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
| Post-import testing done (если mode=required) | Machine-check report из обычного Kilo code run или явный testing waiver | Human / Kilo code run |
| Codex review done | Codex проверил journal, реальные файлы и (если mode=required) testing status | Codex |
| Human check done | человек дал verdict | Human |

### 3A. Post-import testing gate

Acceptance gate зависит от `manifest.post_import_testing.mode`:

**`mode = required`:**
Acceptance не может быть выполнен без одного из двух:
1. **Machine-check report** — результат обычного Kilo code run, который выполнил Machine checks из `POST_IMPORT_TEST_PROMPT.md`. Report должен существовать по canonical пути: `.ai/v3/test_reports/<V3-ID>_machine_check_report.md`. Codex читает этот файл как главный источник machine-check результатов.
2. **Testing waiver** — явное решение человека пропустить testing.

**`mode = optional`:**
Testing не блокирует acceptance. Machine-check report из `.ai/v3/test_reports/` может быть учтён, но его отсутствие — не препятствие.

**`mode = waived`:**
Testing gate не применяется.

Testing waiver — лёгкий механизм:
- не новая сущность и не новый журнал;
- explicit note/decision в review chain;
- человек явно говорит Codex «testing не нужен, принимаем без тестов»;
- Codex фиксирует waiver в review notes.

### 3B. Когда testing gate не обязателен

- `mode = optional` или `mode = waived` — testing gate не применяется.
- `docs_only` простые пакеты не должны внезапно становиться тяжёлыми из-за обязательных тестов.

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
- если `manifest.post_import_testing.mode = required`, machine-check report существует и не содержит критических проблем (или есть testing waiver);
- человек подтвердил.

После human accept:
- journal draft из `.ai/v3/journals/drafts/V3-*_journal.yaml` повышается в `.ai/v3/journals/V3-*_journal.yaml` и становится tracked;
- tester prompt copy и machine-check report остаются local-only (не tracked, не journal);
- lifecycle entry в `V3_navigation.md` обновляется до `accepted`.

### `revision`

- package/import частично годен;
- проблемы исправимы через revision loop;
- acceptance ещё не наступил;
- journal draft остаётся в `drafts/`.

### `reject`

- manifest invalid;
- checksums не совпадают;
- repo root не определён или relative paths были разрешены не от git repo root;
- scope грубо нарушен;
- package/import lane невалиден;
- revision loop исчерпан;
- или import вообще не должен был начинаться из-за несоблюдения gates.

После reject:
- journal draft остаётся в `drafts/` как historical record (не tracked);
- package может быть перенесён в rejected local-only зону;
- lifecycle entry в `V3_navigation.md` обновляется до `rejected`.

## 6. Что не является acceptance

- валидный ZIP package без import;
- pre-Kilo package review;
- setup guide без реального UI confirmation;
- Codex verdict без human verdict;
- наличие файлов в repo без полного review chain;
- import без post-import testing, если `manifest.post_import_testing.mode = required` и нет waiver.

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
