# Первая публикация репозитория в GitHub

Гид для `sword-of-rome-web`. Помогает выполнить `git init`, первый commit и первый push без включения local-only мусора.

## Статус этого документа после публикации

Этот файл больше не описывает текущий статус repo как "ещё не опубликован". Репозиторий уже опубликован на GitHub как [`AndrewVerhoturov1/Sword_of_rome_2d`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d).

Сейчас этот гид нужен как:

- историческая запись первого public bootstrap;
- safety-checklist для похожей первой публикации в новом repo;
- напоминание, какие local-only и runtime-пути нельзя тащить в public commit.

## Что уже подготовлено

### `.gitignore` уже настроен

Файл [`../../.gitignore`](../../.gitignore) исключает:

- `arena-prototype-launcher/` — отдельный локальный launcher
- `_local/` — локальные архивы планов и материалов
- `output/Arena tests/` — архив тестовых прототипов
- `**/node_modules/` — зависимости
- `**/.codex-logs/`
- `dist/`, `build/`
- `.DS_Store`, `Thumbs.db`
- runtime `.ai/`-подпапки: `handoffs/`, `reports/`, `plans/sessions/`, `reviews/`, `model_tests/`, `sync/`, `bootstrap/runs/`
- runtime external_chats-подпапки: `requests/`, `responses/`, `tasks/`, `recorder_packages/`, `notebook_sources/`, `notebook_packages/`

### Разделение слоёв

| Слой | Назначение | Публикуется |
|------|-----------|-------------|
| `canon/` | Принятый проектовый контекст | Да |
| `references/` | Справочные материалы (правила, карта, UI-референсы) | Да |
| `docs/` | Процессные документы (workflow, гайды) | Да |
| `scripts/` | Workflow-скрипты (bootstrap, синхронизация, notebook) | Да |
| `ideas/` | Непринятые идеи и гипотезы | Да |
| `.ai/` | Workflow-слой Codex+Kilo (кроме runtime-артефактов) | Да, частично |
| `output/README.md` | Пояснение про локальный архивный слой | Да |
| `arena-prototype-launcher/` | Локальный launcher прототипов | Нет |
| `_local/` | Локальные архивы и служебные материалы | Нет |
| `output/Arena tests/` | Архив тестовых прототипов | Нет |

### Что не должно попасть в публичный commit

- `arena-prototype-launcher/` — содержит локальные настройки, БД прототипов, запрещён к публикации по workflow policy
- `_local/` — agent-планы, временные заметки, дубли материалов
- `output/Arena tests/` — хаотичные тестовые прототипы, не канон проекта
- runtime `.ai/`-артефакты — handoffs, reports, review, session-планы, bootstrap-runs, external-chat-материалы
- `node_modules/` — стандартный git-мусор

## Команды

Выполнять в PowerShell из корня репозитория (`D:\Codex+Kilocode\projects\sword-of-rome-web`).

### 1. Инициализация Git

```powershell
git init
```

Создаст пустой `.git`-каталог.

### 2. Первый `git add`

Добавляем только публичные файлы. Используем точечный add, чтобы случайно не захватить лишнее.

```powershell
git add .gitignore
git add README.md
git add AGENTS.md
git add canon/
git add references/
git add docs/
git add scripts/
git add ideas/
git add output/README.md
git add .ai/repo_navigation.md
git add .ai/project_state.md
git add .ai/project_brief.md
git add .ai/architecture.md
git add .ai/decisions.md
git add .ai/README.md
git add .ai/backlog/
git add .ai/external_chats/V1_navigation.md
git add .ai/external_chats/notebook/
git add .ai/external_chats/external_chat_rules.md
git add .ai/external_chats/external_agent_static_manual.md
git add .ai/external_chats/manual.md
git add .ai/external_chats/publisher_config.json
git add .ai/external_chats/tasks/README.md
git add .ai/prompts/
git add .ai/rules/
git add .ai/templates/
git add .ai/validators/
git add .ai/plans/README.md
git add .ai/bootstrap/portable/
```

### 3. Проверка состава staged файлов

```powershell
git status
```

Убедись, что:

- `arena-prototype-launcher/` — **не** в списке staged
- `_local/` — **не** в списке staged
- `output/Arena tests/` — **не** в списке staged
- `.ai/handoffs/` — **не** в списке staged
- `.ai/reports/` — **не** в списке staged
- `.ai/plans/sessions/` — **не** в списке staged
- `node_modules/` — **не** в списке staged

### 4. Первый commit

```powershell
git commit -m "Initial commit: project context, workflow layer, reference materials"
```

### 5. Создание GitHub-репозитория

Этот шаг уже выполнен для текущего repo. Ниже сохранён исходный pre-publication сценарий как historical setup reference.

Открой [github.com/new](https://github.com/new) и создай репозиторий:

- **Repository name:** `Sword_of_rome_2d` или другое имя нового repo по текущей задаче
- **Description:** Browser-based 2D editor and authoring tool for counter-based wargames
- **Visibility:** Public или Private — на твой выбор
- **Не** ставь галочки «Initialize with README», «Add .gitignore» или «Choose a license» — у тебя уже есть свой README и .gitignore

### 6. Первый push

Для текущего repo этот шаг уже пройден. Команды ниже нужны только если ты повторяешь bootstrap для нового репозитория.

После создания репозитория GitHub покажет команды. Выполни:

```powershell
git remote add origin https://github.com/<ТВОЙ-ЛОГИН>/sword-of-rome-web.git
git branch -M main
git push -u origin main
```

Замени `<ТВОЙ-ЛОГИН>` на своё имя пользователя GitHub.

## Что перепроверить перед push

Перед `git push` выполни `git status` и `git diff --cached --stat`:

```powershell
git status
git diff --cached --stat
```

Убедись:

- [ ] `arena-prototype-launcher/` отсутствует в staged
- [ ] `_local/` отсутствует в staged
- [ ] `output/Arena tests/` отсутствует в staged
- [ ] Подпапки `.ai/handoffs/`, `.ai/reports/`, `.ai/plans/sessions/`, `.ai/reviews/`, `.ai/model_tests/` отсутствуют
- [ ] Подпапки `.ai/external_chats/requests/`, `responses/`, `tasks/`, `recorder_packages/`, `notebook_sources/`, `notebook_packages/` отсутствуют
- [ ] `node_modules/` нигде нет
- [ ] `canon/`, `references/`, `docs/`, `scripts/`, `ideas/` присутствуют
- [ ] `.ai/repo_navigation.md`, `.ai/project_state.md`, `.ai/project_brief.md`, `.ai/architecture.md`, `.ai/decisions.md` присутствуют
- [ ] `README.md` и `AGENTS.md` присутствуют

## Почему `arena-prototype-launcher/`, `_local/` и `output/Arena tests/` не должны публиковаться

| Папка | Причина |
|-------|---------|
| `arena-prototype-launcher/` | Содержит локальную БД прототипов (registry.json), серверные ключи, настройки запуска. Это отдельный локальный сервис, не часть публичного проекта. |
| `_local/` | Содержит agent-планы, временные дампы, дубли материалов. Ничего из этого не является каноном или стабильным артефактом. |
| `output/Arena tests/` | Хаотичные тестовые прототипы, сгенерированные Arena.ai и ChatGPT. Это временный архив, который не отражает направление проекта. |

## После публикации

После первого push репозиторий будет содержать только публичный слой проекта:

- проектовый контекст (`canon/`)
- справочные материалы (`references/`)
- процессные документы (`docs/`)
- workflow-скрипты (`scripts/`)
- workflow-правила и конфигурацию (`.ai/`)
- идеи (`ideas/`)
- навигацию (`README.md`, `AGENTS.md`, `.ai/repo_navigation.md`)

Локальные слои (`arena-prototype-launcher/`, `_local/`, `output/Arena tests/`) остаются только на твоей машине и в `git status` будут показываться как untracked (если не захочешь их удалить из рабочей директории — они не влияют на Git).
