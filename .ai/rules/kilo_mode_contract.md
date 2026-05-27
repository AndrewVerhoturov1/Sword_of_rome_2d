# Контракт Kilo Mode И Task Role

Этот файл фиксирует терминологию для workflow `Codex + Kilo Code`.

## Обязательные значения

### Handoff: `Рекомендуемый Kilo mode`

Допустимы только:

- `kilo-handoff-runner`
- `kilo-debugger`
- `kilo-verifier`
- `kilo-recorder`
- `kilo-notebook`
- `kilo-notebook-v3`

### Launch package: `Kilo mode:`

Допустимы только UI-значения:

- `Kilo Handoff Runner`
- `Kilo Debugger`
- `Kilo Verifier`
- `Kilo Recorder`
- `Kilo Notebook`
- `Kilo Notebook V3`

### Handoff: `Task role`

Допустимы только:

- `Builder Agent`
- `Docs Agent`
- `Tester Agent`
- `Refactor Agent`
- `Debugger Agent`
- `Recorder Agent`
- `Notebook Agent`

## Что запрещено

- Использовать как mode значения `kilo-builder`, `kilo-docs`, `kilo-tester`, `kilo-refactor`.
- Подставлять role в поле `Kilo mode:`.
- Подставлять mode в поле `Task role`.

## Правило по умолчанию

Если задача является обычной code, docs, setup или refactor-задачей по одному handoff, mode по умолчанию должен быть `kilo-handoff-runner`.

## Контракт для kilo-recorder

Режим `kilo-recorder` имеет отдельный, строгий контракт.

### Назначение

- Режим предназначен исключительно для `External Web Chat`.
- Используется только для записи ответа внешнего чата в локальный response-файл.
- Рекомендуемая связка: `Kilo mode = kilo-recorder`, `Task role = Recorder Agent`.

### Приоритет mode-specific contract

`Recorder Package Contract` переопределяет общие task/global wording для `kilo-recorder` там, где есть конфликт. Recorder пишет только файлы из `allowed_writes`, не создаёт report и не выполняет `git status`. `attempt_completion` используется только как финальное завершение запуска.

### Разрешённые операции

- Запись response-файла с ответом внешнего чата.
- Перечитать response после записи и убедиться, что он не пустой.
- Писать дополнительные файлы только если они явно перечислены в `allowed_writes`.

### Запрещённые операции

- Review содержимого ответа внешнего чата.
- Содержательная правка ответа внешнего чата.
- Изменение project files вне `allowed_writes`.
- Интерпретация ответа внешнего чата как факта о repo без локальной проверки.
- Использование для задач, не связанных с External Web Chat.
- Создание report-файла.
- Выполнение `git status`.

### UI-примечание

Фактическое добавление режима `Kilo Recorder` в интерфейс выполняется человеком вручную через интерфейс Kilo. Этот шаг меняет только repo-level contract и launch/handoff rules.

## Контракт для kilo-notebook

Режим `kilo-notebook` имеет отдельный контракт для `/v1` staged local persistence.

### Назначение

- Режим предназначен только для `/v1`.
- Используется только для локального staged save внешнего ответа в notebook entry и `V1_navigation.md`.
- Рекомендуемая связка: `Kilo mode = kilo-notebook`, `Task role = Notebook Agent`.
- User-facing вход: сырой ответ внешнего чата, вставленный напрямую в `Kilo Notebook`.

### Runtime path

- Основной путь: `raw external response -> source artifact (.ai/external_chats/notebook_sources/) -> python scripts/stage_v1_notebook.py --input <source-file> -> internal notebook package -> notebook entry + V1_navigation.md`.
- Source artifact создаётся через file-edit path как штатный internal transport artifact, а не как временный workaround.
- Shell text-dump (`echo`, heredoc, длинный CLI literal) запрещён как стандартный transport.
- `notebook package` остаётся обязательным внутренним артефактом воспроизводимости.
- `write_v1_notebook.py` — внутренний writer-step, не первым шагом для человека/Kilo Notebook.

### Обязательные поля notebook package

- `external_question_id`
- `notebook_entry_path`
- `v1_navigation_path`
- `allowed_writes`
- `candidate_navigation_entry`
- `raw_response`

### Служебные поля notebook package

- `entry_status: staged`
- `provider_model`
- `context_links`

### Разрешённые операции

- Принять сырой ответ внешнего чата через `stdin` как основной user-facing вход.
- Автоматически создать internal `notebook package` через `stage_v1_notebook.py`.
- Создать или обновить notebook entry по пути из internal `notebook package`.
- Обновить `V1_navigation.md`.
- Писать дополнительные файлы только если они явно перечислены в `allowed_writes`.

### Запрещённые операции

- Обновлять `repo_navigation.md`.
- Публиковать notebook entry.
- Присваивать `accepted` или `published` статусы.
- Использовать режим для `/r1`.
- Интерпретировать внешний ответ как факт о repo без локальной проверки.

### UI-примечание

Фактическое добавление режима `Kilo Notebook` в интерфейс выполняется человеком вручную через интерфейс Kilo. Этот шаг меняет только repo-level contract и launch/handoff rules.

## Контракт для kilo-notebook-v3

Режим `kilo-notebook-v3` имеет отдельный контракт для будущего V3 artifact-producing workflow.

### Назначение

- Режим предназначен для V3 artifact-producing workflow.
- Используется для безопасного импорта артефактов из внешнего V3 artifact package.
- Рекомендуемая связка: `Kilo mode = kilo-notebook-v3`, `Task role = Notebook Agent`.
- Отдельный от `kilo-notebook` (который остаётся `/v1-only`).
- Отдельный от `kilo-recorder` (который остаётся `/r1-only`).
- Отдельный от V2.

### Текущий статус (Phase 4)

- Режим canonically разрешён в mode lists, validator и rules (Phase 0).
- `.ai/v3/` foundation, контракты, промпты, шаблоны созданы (Phases 1-3).
- Manual setup guide доступен: [`.ai/v3/docs/manual_kilo_notebook_v3_setup.md`](../v3/docs/manual_kilo_notebook_v3_setup.md) (Phase 4).
- `/v3` shortcut не активирован.
- `scripts/v3/*` не созданы (Phase 7).
- Pilot ещё не проведён (Phase 5).
- Режим готов к ручному запуску, scripted support — в следующих фазах.

### Разрешённые операции (после активации)

- Принять ZIP artifact package от внешнего чата.
- Распаковать package в staging-зону.
- Проверить manifest, пути, хэши.
- Записать только явно разрешённые файлы.
- Создать journal entry.

### Запрещённые операции

- Писать файлы вне `allowed_writes`.
- Перезаписывать существующие файлы без явного разрешения.
- Выполнять auto-apply без Codex review.

### UI-примечание

Фактическое добавление режима `Kilo Notebook V3` в интерфейс выполняется человеком вручную через интерфейс Kilo.

## Границы режимов

- `kilo-notebook` = `/v1-only`.
- `kilo-recorder` = `/r1-only`.
- `/v2` = не новый Kilo mode.
- `kilo-notebook-v3` = отдельный V3 import/check/write/journal mode. Режим canonically разрешён (Phase 0). `.ai/v3/` subsystem создана (Phases 1-3), manual setup guide доступен (Phase 4). `/v3` shortcut не активирован, `scripts/v3/*` не созданы, pilot ещё не проведён.

## V2 External Senior Review — не новый Kilo mode

`/v2` — это project-local manual protocol, описанный в [`.ai/external_reviews/README.md`](../external_reviews/README.md). V2 не является новым Kilo mode. V2 работает через существующие допустимые modes: `kilo-handoff-runner` для docs/protocol и `kilo-debugger` для stuck/debug cases. V2 ingest полностью ручной: raw external answer передаётся в ordinary Kilo run вручную, без использования `kilo-recorder`. Для V2 ingest допустимы только `kilo-handoff-runner` и `kilo-debugger`. `kilo-notebook` остаётся `/v1-only` и не используется в V2. V2 не добавляет новые значения в списки допустимых `Kilo mode` или `Task role`.

### `/v2` как interrupt

`/v2` может быть вызван пользователем во время уже идущего Kilo run. Это interrupt, а не новый запуск:

- Kilo обязан поставить обычную debug/build попытку на паузу, кратко зафиксировать WIP state, перейти в `/v2 preview`.
- Explicit user `/v2` — это не `blocked-v2-recommended`. При explicit `/v2` не требуется blocked report и не требуется три неудачные попытки. Достаточно краткого WIP summary.
- После V2-цикла Kilo возвращается к исходной задаче или завершает её по новому решению.

### YOLO и V2 escalation

Правила YOLO Stop Gates, V2 Recommendation Gate и Blocked Report Contract описаны в [`AGENTS.md`](../../AGENTS.md). Коротко:

- Kilo обязан остановиться, если дальнейшие действия рискованны или бессмысленны.
- Blocker на реальном WIP-коде → `blocked-v2-recommended` и рекомендация `/v2 preview` как следующего шага.
- Blocker из-за отсутствия source of truth или private/local-only артефактов → остановка без обязательной рекомендации V2.
- После 3 осмысленных безуспешных попыток или раньше, если следующая попытка уже рискованна → обязательный blocked report.
- YOLO не отменяет safety gates, human-review gates, V2 push approval, local-only policy и scope boundaries.
- `awaiting_human_push_approval` — валидный stop-state даже в YOLO. Kilo обязан остановиться на этом шаге и не продолжать автономно. Продолжение без human confirmation является нарушением протокола.

## Repo-wide policy inheritance

Все ordinary Kilo modes, кроме mode-specific exceptions вроде `kilo-recorder` и `kilo-notebook`, наследуют repo-level policy layer:

- `.ai/policies/language_policy.md`
- `.ai/policies/human_review_policy.md`
- `.ai/policies/bug_tracking_policy.md`

Если task не явно exempted mode-specific contract-ом, report должен содержать:

- `Баги и сложности`
- `Human Check`
- `Runtime metadata`

Debugger / bugfix / repeated-issue runs должны сначала смотреть `.ai/logs/bug_journal.md`.

Failed human check считается real bug/difficulty state, а не формальной пометкой.

## Preflight-check

Перед выдачей `/kilo` Codex обязан:

1. Проверить handoff на запрещённые псевдо-mode значения.
2. Проверить, что в handoff указан один допустимый внутренний mode.
3. Проверить, что launch package содержит ровно одну строку `Kilo mode:`.
4. Проверить, что `Kilo mode:` использует UI-имя режима, а не role.
5. Остановиться и исправить handoff или launch package, если найдено смешение `role` и `mode`.

## External Web Chat launch package

Для `External Web Chat` используется отдельный launch package формат, который не содержит 5 Kilo-моделей.

Такой launch package должен включать:

- `Agent kind: External Web Chat`
- `External provider` (например: ChatGPT / DeepSeek / Any)
- `External mode` (например: text-chat / agent-mode / image-generation)
- один fenced copy-paste prompt
- понятную инструкцию человеку, что вернуть после запуска

## kilo-recorder short wrapper

Для `kilo-recorder` flow допустим короткий wrapper в launch package:

```md
## Kilo mode

- Kilo mode: `Kilo Recorder`
- Task role: `Recorder Agent`
- Mode switching: запрещён
- Recording mode: `response-only`
- Allowed writes: только response-файл, если иной файл не перечислен явно в recorder package
- Finalization: `attempt_completion` only
```

Wrapper должен содержать:

- путь к response-файлу для записи;
- короткую строку `Model policy: use the selected model from the recorder package; if unavailable, write unavailable and ask human to return the model name.`;
- явное указание, что recorder не создаёт report и не делает `git status`.

## kilo-notebook short wrapper

Для `kilo-notebook` flow допустим короткий wrapper в launch package:

```md
## Kilo mode

- Kilo mode: `Kilo Notebook`
- Task role: `Notebook Agent`
- Mode switching: запрещён
- Runtime command: `python scripts/stage_v1_notebook.py --input <source-file>`
- Input source: raw-response source artifact from `.ai/external_chats/notebook_sources/`
- Source artifact naming: `YYYY-MM-DD_<external_question_id>_raw_response.md`
- Entry status: `staged`
- Allowed writes: только notebook entry и `V1_navigation.md`, если иной файл не перечислен явно в notebook package
```

Wrapper должен содержать:

- команду `python scripts/stage_v1_notebook.py --input <source-file>` как основной runtime path;
- указание, что source artifact создаётся в `.ai/external_chats/notebook_sources/` через file-edit path;
- указание, что user-facing input — сырой ответ внешнего чата, который сначала сохраняется как source artifact;
- указание, что internal `notebook package` создаётся автоматически;
- запрет shell text-dump как стандартного transport;
- путь к notebook entry;
- путь к `V1_navigation.md`;
- явное указание, что notebook mode не обновляет `repo_navigation.md` и не публикует entry.
