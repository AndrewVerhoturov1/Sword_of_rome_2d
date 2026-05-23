# Handoff 0005: Arena Publish UI Controls

## Статус

Готово для Kilo

## Рекомендуемый Kilo mode

kilo-handoff-runner

## Task role

Builder Agent

## Task profile

small-code

## Execution mandate

`agent-first`

## Primary execution path

`Kilo Code`

## Allowed agent kinds

- `Kilo Code`

## Default preference

Работать только внутри:

- [sword-of-rome-web](/D:/Codex+Kilocode/projects/sword-of-rome-web)

Remote write target в этом handoff не нужен.

## Exception status

`none`

## Minimum substantive agent work

Реализовать второй execution chunk publish-фичи:

- frontend publish-controls в карточке prototype и в detail panel;
- frontend types и API client для `publish / publish-update / remove`;
- UI state для in-flight publish операций и ошибок;
- отображение `publishState`, `repoUrl`, `demoUrl`, `lastError`, `lastPublishedAt`;
- disable/guard поведения кнопок во время publish/update/remove;
- проверка, что UI собирается после изменений.

Недостаточно только добавить кнопки без wiring к `App.tsx`, без disabled/error state или без build-проверки UI.

## Sequential agent policy

Только один run в рамках этого handoff: один запуск -> report -> review Codex.

## If no agent path fits -> return escalation note

Если для UI-контракта не хватает backend response shape, если требуются backend изменения вне уже принятого `P1`, или если существующая UI-архитектура требует заметного redesign вне `App.tsx` + publish-controls, не расширять scope молча. Вернуть `Blocked` с точной причиной.

## Session plan

[2026-05-23_arena_publish_github_pages.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-05-23_arena_publish_github_pages.md)

## Plan item

`P2: Launcher UI Publish Controls`

## Session run

`002`

## Рекомендуемый класс модели

fast_coding_model

## Default model

Qwen3 Coder 480B

## Fallback model или Candidate models

- Qwen3 Coder Next
- DeepSeek V4 Pro

## Когда эскалировать в strong_model

- если существующий UI state owner в `App.tsx` не позволяет добавить publish state без заметной перестройки;
- если фактический backend contract расходится с принятым `P1` и требует пересмотра API shape;
- если safe UX для async publish/remove требует нетривиальной архитектурной развилки.

## Уровень риска

Средний

## Цель

Довести publish-фичу до usable UI-слоя в локальной арене: пользователь должен видеть, можно ли prototype публиковать, запускать `Опубликовать`, `Обновить GitHub`, `Убрать из GitHub`, открывать `repo` и `demo`, а также понимать текущий publish-state и ошибки.

## Контекст проекта

- `P1` уже принят: backend endpoints и remote bootstrap считать существующим contract, а не целью рефакторинга.
- Этот handoff только про UI launcher-а.
- Источник истины для project списка и selected project сейчас живёт в [`App.tsx`](../../arena-prototype-launcher/ui/src/App.tsx).
- Publish state приходит как часть project payload от server.
- Корневой `.gitignore` игнорирует `arena-prototype-launcher/`, поэтому review будет опираться на фактическое содержимое файлов и report, а не на top-level `git diff`.

## Required Inputs

- [arena-prototype-launcher/ui/src/App.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/App.tsx)
- [arena-prototype-launcher/ui/src/types.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/types.ts)
- [arena-prototype-launcher/ui/src/api/client.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/api/client.ts)
- [arena-prototype-launcher/ui/src/components/ProjectGrid.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/components/ProjectGrid.tsx)
- [arena-prototype-launcher/ui/src/components/ProjectCard.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/components/ProjectCard.tsx)
- [arena-prototype-launcher/ui/src/components/DetailPanel.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/components/DetailPanel.tsx)
- [arena-prototype-launcher/server/src/types.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/types.ts)
- [arena-prototype-launcher/server/src/routes/projects.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/routes/projects.ts)
- [2026-05-23_arena_publish_github_pages.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-05-23_arena_publish_github_pages.md)

## Lookup Inputs

- [arena-prototype-launcher/ui/package.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/package.json)
- [arena-prototype-launcher/ui/src/styles.css](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/styles.css)
- [arena-prototype-launcher/ui/src/components/helpers.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/components/helpers.ts)
- [arena-prototype-launcher/server/src/publishService.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/publishService.ts)

## Do Not Read Unless Blocked

- старые handoff/report files, не связанные с arena publish
- public canon/reference/docs files вне прямой связи с launcher UI
- `.ai/external_chats/**`
- любые папки в `output/`

## Context Budget

- Фокус только на chunk `P2`.
- Не менять backend logic `P1`, если нет прямой ошибки UI-контракта.
- Не делать `P3` verification с живым Pages deploy.
- Не рефакторить общую визуальную систему launcher-а.
- Не добавлять новый глобальный state manager.
- Не трогать unrelated components.

## Важные файлы

- [arena-prototype-launcher/ui/src/App.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/App.tsx)
- [arena-prototype-launcher/ui/src/api/client.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/api/client.ts)
- [arena-prototype-launcher/ui/src/types.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/types.ts)
- [arena-prototype-launcher/ui/src/components/ProjectCard.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/components/ProjectCard.tsx)
- [arena-prototype-launcher/ui/src/components/DetailPanel.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/components/DetailPanel.tsx)
- [arena-prototype-launcher/server/src/types.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/types.ts)

## Expected Implementation Shape

### Frontend contract

- Добавить в UI types:
  - `PublishStatus`
  - `PublishState`
  - поле `publishState?: PublishState` в `Project`
- Согласовать shape с server `types.ts`, не изобретать отдельный несовместимый контракт.

### API client

- Добавить методы:
  - `publishProject(id)`
  - `publishUpdateProject(id)`
  - `removePublishedProject(id)`
- Тип ответа должен позволять обновить `Project.publishState` без повторного полного refresh, где это разумно.
- Если remove endpoint возвращает только `{ success: true }`, UI может локально сбрасывать publishState и/или делать `refreshProjects()`.

### App state owner

- В `App.tsx` добавить handlers для:
  - first publish
  - publish update
  - publish remove
- Добавить per-project in-flight UI state, чтобы блокировать кнопки во время операции.
- Ошибки publish должны попадать в user-visible state, а не только в `console.error`.
- После успешной операции UI должен синхронизировать `projects` state и `selectedProject`.

### Card / Detail UI

- В карточке:
  - если prototype publish-eligible и не опубликован: показать `Опубликовать`
  - если опубликован: показать `Обновить GitHub`, `Убрать из GitHub`
  - если есть `demoUrl`: показать действие открытия demo
  - если есть `repoUrl`: показать действие открытия repo
- В detail panel:
  - показать publish-state
  - показать `demoUrl` / `repoUrl`
  - показать `lastError`, если есть
  - показать `lastPublishedAt`, если есть
- Во время async publish/update/remove соответствующие кнопки disabled и визуально не выглядят доступными.

### Eligibility rules

- Если у project нет `publishState` и нет явного backend-флага eligibility, не изобретать сложную эвристику.
- Допустимый v1 fallback: считать кнопку `Опубликовать` доступной для non-archived проектов и полагаться на backend validation/error response.
- Если в текущем payload можно надёжно вывести eligibility без backend изменений, использовать это. Если нет — не расширять scope `P2` ради нового backend поля.

## Allowed Changes

Локально:

- `arena-prototype-launcher/ui/src/App.tsx`
- `arena-prototype-launcher/ui/src/types.ts`
- `arena-prototype-launcher/ui/src/api/client.ts`
- `arena-prototype-launcher/ui/src/components/ProjectGrid.tsx`
- `arena-prototype-launcher/ui/src/components/ProjectCard.tsx`
- `arena-prototype-launcher/ui/src/components/DetailPanel.tsx`
- `arena-prototype-launcher/ui/src/styles.css`, только если реально нужен маленький styling fix
- новый report по пути ниже

## Forbidden Changes

- не менять backend publish logic из `P1`, если UI можно довести без этого
- не трогать `arena-prototype-launcher/server/src/publishService.ts`, кроме случая явного blocked mismatch; в таком случае вернуть `Blocked`, не чинить молча
- не делать Pages verification
- не трогать другие prototype folders
- не трогать `output/`
- не создавать новые handoff files

## Report mode

full

## File writing policy

Можно писать только:

- разрешённые UI-файлы из scope выше
- новый report по пути ниже

## Stop Conditions

- backend response shape делает UI wiring невозможным без backend change
- publish-controls требуют заметного redesign launcher layout вне обозначенного scope
- `npm run build` в UI падает по причине, не связанной с этим chunk, и безопасно локально изолировать её нельзя

## Критерии приёмки

- [ ] UI types знают `publishState`
- [ ] В `api/client.ts` есть методы publish/update/remove
- [ ] `App.tsx` умеет запускать publish/update/remove и обновлять локальный `projects` state
- [ ] В карточке есть publish-controls для нужных состояний
- [ ] В detail panel видны publish-state, ошибки и ссылки `demo/repo`
- [ ] Кнопки disabled во время async publish-операций
- [ ] Ошибки publish видны пользователю
- [ ] `arena-prototype-launcher/ui` проходит `npm run build`
- [ ] Report фиксирует локально изменённые файлы, принятые UX-решения, проверки и остаточные риски

## Куда записать report

[0005_arena_publish_ui_controls_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0005_arena_publish_ui_controls_report.md)

## Что вернуть после запуска

- путь к report
- список локально изменённых файлов
- краткий список user-visible UI changes
- статус:
  - `Готово для review`
  - или `Blocked`
