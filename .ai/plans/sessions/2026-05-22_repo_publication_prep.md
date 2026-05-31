# Session: repo_publication_prep

## Session ID

`2026-05-22_repo_publication_prep`

## Status

completed

## Goal

Подготовить понятный public-facing вход в repo перед первой публикацией: добавить практический гид по `git init` и первой публикации, а также довести `README.md` и `.ai/repo_navigation.md` до полного отражения текущей структуры проекта.

## Approved Plan

### P1: Publication Guide And Navigation Sync

- Status: completed.
- Создать один человекочитаемый гид по первой инициализации git и первой публикации этого repo.
- Обновить `README.md` так, чтобы он отражал текущую структуру, public/local-only разделение и путь чтения для внешних чатов.
- Обновить `.ai/repo_navigation.md` так, чтобы он индексировал всю текущую meaningful structure проекта.
- Не трогать product code, launcher и local-only архивы.

## Active Plan Item

`none`

## Runs

- `Session run: 001` - accepted after review. Создан практический гид по первой GitHub-публикации, обновлены `README.md` и `.ai/repo_navigation.md`, public/local-only границы описаны ясно, launcher и локальные архивы не затронуты.

## User Overrides

- Пользователь явно попросил делать этот шаг через Kilo, а не прямой правкой Codex.
- Пользователь хочет, чтобы `/v1` history оставалась видимой в публичном repo.
- `arena-prototype-launcher/` нельзя переносить и нельзя включать в GitHub без отдельного явного запроса.

## Checkpoint State

- Repo [sword-of-rome-web](/D:/Codex+Kilocode/projects/sword-of-rome-web) уже bootstrap-нут из central core.
- Public structure уже начата: `canon/`, `references/`, `docs/`, `.ai/`, `_local/`, `output/`.
- `README.md`, `.ai/repo_navigation.md` и [first_git_publication_guide.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/docs/workflow/first_git_publication_guide.md) синхронизированы под текущую структуру repo.
- Workflow checkpoint commit пока невозможен, потому что в repo ещё нет `.git`; следующий логичный шаг — реальный `git init` по новому guide.
