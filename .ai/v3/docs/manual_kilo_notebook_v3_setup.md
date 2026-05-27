# Ручная настройка режима Kilo Notebook V3

Этот гайд объясняет, как человеку вручную добавить и проверить режим `Kilo Notebook V3` в интерфейсе Kilo Code.

## Текущий статус (Phase 4)

- Режим `kilo-notebook-v3` / `Kilo Notebook V3` canonically разрешён в правилах и валидаторе.
- `.ai/v3/` foundation, контракты (Phase 2), промпты и шаблоны (Phase 3) уже созданы.
- Этот setup guide (Phase 4) делает ручную настройку режима возможной без скриптов.
- `/v3` shortcut **не активирован**.
- `scripts/v3/*` **не созданы** (будут в Phase 7).
- Первый pilot **ещё не проведён** (Phase 5).

## 1. Добавить режим в интерфейс Kilo

Режим `Kilo Notebook V3` добавляется вручную через интерфейс Kilo Code. Repo-level canon фиксирует контракт, но не заменяет ручную настройку UI.

### Что нужно сделать

1. Откройте интерфейс Kilo Code в VS Code.
2. Найдите список доступных Kilo modes.
3. Добавьте новый режим со следующими параметрами:
   - **Внутреннее mode-значение:** `kilo-notebook-v3`
   - **UI-имя:** `Kilo Notebook V3`
   - **Описание:** Безопасный импорт артефактов из внешнего V3 artifact package. Проверка manifest, путей и хэшей. Запись только разрешённых файлов. Journaling.
4. Убедитесь, что новый режим виден в выпадающем списке Kilo modes.

### Рекомендуемая связка

При запуске V3-задачи используйте:

- `Kilo mode = Kilo Notebook V3`
- `Task role = Notebook Agent`

Не путайте:
- `Kilo Notebook` — это `/v1-only` (staged local persistence для prompt-only ответов).
- `Kilo Notebook V3` — это отдельный V3 import/check/write/journal режим.
- `Kilo Recorder` — это `/r1-only` (response capture для External Web Chat).

## 2. Проверить существование режима в правилах

После добавления в UI убедитесь, что режим описан в repo-level документах:

- [`AGENTS.md`](../../../AGENTS.md) — раздел допустимых Kilo mode.
- [`.ai/README.md`](../../README.md) — раздел Kilo modes.
- [`.ai/rules/agent_protocol.md`](../../rules/agent_protocol.md) — режим `kilo-notebook-v3`.
- [`.ai/rules/kilo_mode_contract.md`](../../rules/kilo_mode_contract.md) — контракт `kilo-notebook-v3`.
- [`.ai/README.md`](../../README.md) — role vs mode.

Если режим упомянут во всех этих файлах с корректным статусом, repo-level canon согласован.

## 3. Что нужно для ручного запуска V3 (Phase 4 manual runtime)

На текущей фазе (Phase 4) V3-цикл выполняется вручную. Для запуска нужны:

### 3.1. Входы

1. **V3 artifact package** (ZIP-файл), созданный внешним чатом по контракту [`v3_artifact_package_contract.md`](../contracts/v3_artifact_package_contract.md).
2. **Исходный V3 request** — текст запроса, который был отправлен внешнему чату.
3. **Mode prompt** — [`kilo_notebook_v3_mode_prompt.md`](../prompts/kilo_notebook_v3_mode_prompt.md).

### 3.2. Ручной порядок импорта (до Phase 7)

Поскольку `scripts/v3/*` ещё не созданы, импорт делается вручную:

1. **Распаковать ZIP** в staging-зону: `.ai/v3/staging/<имя_корневой_папки>/`.
2. **Проверить manifest.yaml** — обязательные поля, `v3_id`, `action: create`, `allowed_paths`, `forbidden_paths`, список `files`.
3. **Проверить checksums.sha256** — вычислить SHA-256 для каждого файла и сверить.
4. **Скопировать файлы** из `files/` в целевые project-relative пути.
5. **Создать journal entry** вручную по шаблону [`v3_journal_template.yaml`](../templates/v3_journal_template.yaml) в `.ai/v3/journals/drafts/`.
6. **Передать journal + файлы Codex** для review (по [`codex_v3_review_prompt.md`](../prompts/codex_v3_review_prompt.md)).
7. **Дождаться human verdict** (accept / revision / reject).

Подробный пошаговый контракт импорта описан в [`kilo_notebook_v3_mode_prompt.md`](../prompts/kilo_notebook_v3_mode_prompt.md).

## 4. Текущие границы (Phase 4)

- **Без `/v3` shortcut.** Режим запускается только вручную через выбор в интерфейсе Kilo.
- **Без `scripts/v3/*`.** Импорт, проверка manifest, сверка хэшей и journaling выполняются вручную.
- **Без auto-apply.** Ни один файл не записывается автоматически без ручной проверки.
- **Без pilot.** Первый живой V3-cycle ещё не проведён (Phase 5).
- **MVP-ограничения:** только `action: create`, без overwrite, без delete, без бинарных файлов без явного разрешения.
- **Scope первого pilot:** только `docs_only` (см. [`v3_scope_policy.md`](../contracts/v3_scope_policy.md)).

## 5. Human preflight checklist перед первым pilot

Перед первым живым V3-циклом (Phase 5) проверьте:

- [ ] Режим `Kilo Notebook V3` добавлен в интерфейс Kilo и виден в выпадающем списке.
- [ ] Все 9 контрактов V3 читаются и понятны (`.ai/v3/contracts/`).
- [ ] Промпт для внешнего чата [`create_v3_request_prompt.md`](../prompts/create_v3_request_prompt.md) готов к использованию.
- [ ] Mode prompt [`kilo_notebook_v3_mode_prompt.md`](../prompts/kilo_notebook_v3_mode_prompt.md) прочитан.
- [ ] Шаблон journal entry [`v3_journal_template.yaml`](../templates/v3_journal_template.yaml) понятен.
- [ ] Человек понимает разницу между V1 (prompt-only), V2 (bounded technical review) и V3 (artifact package import).
- [ ] Staging-зона `.ai/v3/staging/` существует.
- [ ] Папка для journal drafts `.ai/v3/journals/drafts/` существует.
- [ ] Человек знает, что первый pilot идёт только в scope `docs_only`.

## 6. Что изменится в следующих фазах

- **Phase 5 (Safe Pilot):** первый живой V3-cycle в безопасной зоне `docs_only`.
- **Phase 6 (External Hardening):** V1 critique + V2 review реального diff.
- **Phase 7 (Scripted Support):** появятся `scripts/v3/validate_v3_package.py`, `scripts/v3/stage_v3_package.py`, `scripts/v3/write_v3_journal.py`. Ручной импорт заменится на скриптованный.
- **Phase 8 (Product-Code Scopes):** расширение scope за пределы `docs_only`.

## Связанные документы

- [`../README.md`](../README.md) — главный вход в V3.
- [`../V3_navigation.md`](../V3_navigation.md) — навигация по V3-слою.
- [`../contracts/README.md`](../contracts/README.md) — 9 контрактов V3 (Phase 2).
- [`../prompts/README.md`](../prompts/README.md) — 4 промпта V3 (Phase 3).
- [`../templates/README.md`](../templates/README.md) — 5 шаблонов V3 (Phase 3).
- [`../../../AGENTS.md`](../../../AGENTS.md) — workflow contract репозитория.
- [`../../plans/master/v3_workflow_implementation_plan.md`](../../plans/master/v3_workflow_implementation_plan.md) — план внедрения V3.
