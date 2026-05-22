# Sword of Rome Web

Браузерный 2D-редактор и рабочий стол для создания, настройки и тестирования настольных варгеймов с фишками.

Проект не строится как «цифровая версия Sword of Rome». Sword of Rome-like модуль здесь служит первым тестовым модулем для проверки универсального authoring tool.

## Что здесь главное

- Публичный проектовый контекст и принятые материалы лежат в [`canon/`](canon/), [`references/`](references/), [`docs/`](docs/) и [`.ai/`](.ai/).
- История `/v1` хранится в [`.ai/external_chats/notebook/`](.ai/external_chats/notebook/) и индексируется через [`.ai/external_chats/V1_navigation.md`](.ai/external_chats/V1_navigation.md).
- Локальные служебные материалы Kilo, runtime-артефакты и архивы прототипов не должны попадать в публичный GitHub-репозиторий.

## Структура верхнего уровня

### Публичные слои (для GitHub)

| Путь | Назначение |
|------|-----------|
| [`canon/`](canon/) | Принятый проектовый контекст и закреплённые решения |
| [`references/`](references/) | Справочные материалы: правила Sword of Rome, карта, UI-референсы |
| [`docs/`](docs/) | Процессные документы: workflow, гайды, руководства |
| [`scripts/`](scripts/) | Workflow-скрипты: bootstrap, синхронизация, notebook |
| [`ideas/`](ideas/) | Сырые идеи, ещё не ставшие каноном |
| [`.ai/`](.ai/) | Workflow-слой Codex + Kilo Code (правила, навигация, конфигурация) |
| `output/README.md` | Пояснение про локальный архивный слой (сам архив исключён из Git) |

### Локально, не для публикации

| Путь | Причина |
|------|---------|
| `arena-prototype-launcher/` | Отдельный локальный launcher прототипов с собственной БД |
| `_local/` | Локальные архивы планов, дампы и служебные материалы |
| `output/Arena tests/` | Архив тестовых прототипов; временно оставлен на месте |

### Runtime-артефакты `.ai/`, исключённые из Git

Эти подпапки существуют локально, но не публикуются:

- `.ai/handoffs/`, `.ai/reports/`, `.ai/reviews/`, `.ai/plans/sessions/` — workflow-артефакты Kilo
- `.ai/external_chats/requests/`, `responses/`, `tasks/`, `recorder_packages/`, `notebook_sources/`, `notebook_packages/` — runtime внешних чатов
- `.ai/bootstrap/runs/`, `.ai/model_tests/`, `.ai/sync/`

## Как начать работать с репозиторием

1. [`AGENTS.md`](AGENTS.md) — workflow contract этого repo.
2. [`.ai/repo_navigation.md`](.ai/repo_navigation.md) — справочник публичного контекста для людей и агентов.
3. [`canon/context/sword_of_rome_web_project_context.md`](canon/context/sword_of_rome_web_project_context.md) — главный проектовый контекст.
4. [`.ai/project_state.md`](.ai/project_state.md) — текущий статус repo.

## Первая публикация в GitHub

[`docs/workflow/first_git_publication_guide.md`](docs/workflow/first_git_publication_guide.md) — пошаговый гид: `git init`, первый commit, создание GitHub-репозитория и push. Все local-only папки уже исключены через `.gitignore`.
