# Handoff 0006: Arena Publish End-To-End Verification And Hardening

## Статус

Готово для Kilo

## Рекомендуемый Kilo mode

kilo-handoff-runner

## Task role

Tester Agent

## Task profile

capability-sensitive

## Execution mandate

`agent-first`

## Primary execution path

`Kilo Code`

## Allowed agent kinds

- `Kilo Code`

## Default preference

Работать только внутри:

- [sword-of-rome-web](/D:/Codex+Kilocode/projects/sword-of-rome-web)

Remote write target только один:

- `AndrewVerhoturov1/arena-test`

## Exception status

`none`

## Minimum substantive agent work

Реализовать третий execution chunk publish-фичи:

- реально прогнать сценарий `publish -> GitHub Pages deploy -> demo URL -> update -> remove` для sample prototype `table-map-editor-v2-gpt`;
- использовать launcher path как primary verification route, а не только ручной `gh api`;
- подтвердить, что repo URL, Pages catalog и demo URL действительно работают;
- если verification выявит маленькие и локальные дефекты в launcher publish/UI/bootstrap files, исправить их в рамках этого chunk;
- зафиксировать итоговые evidence, remote paths и residual risks в report.

Недостаточно только запустить build или только проверить remote repo contents без живого Pages deploy и без demo URL проверки.

## Sequential agent policy

Только один run в рамках этого handoff: один запуск -> report -> review Codex.

## If no agent path fits -> return escalation note

Если нет `gh` auth, если GitHub Pages не может быть активирован из текущего repo state, если launcher server path невозможно поднять локально, или если найденные дефекты требуют уже не hardening, а новый крупный redesign publish architecture, не расширять scope молча. Вернуть `Blocked` с фактами и точной причиной.

## Session plan

[2026-05-23_arena_publish_github_pages.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-05-23_arena_publish_github_pages.md)

## Plan item

`P3: End-To-End Verification And Hardening`

## Session run

`003`

## Рекомендуемый класс модели

strong_model

## Default model

DeepSeek V4 Pro

## Fallback model или Candidate models

- Qwen3 Coder 480B
- Qwen3 Coder Next

## Когда эскалировать в strong_model

- уже эскалировано по умолчанию: есть live remote verification, GitHub Pages workflow, публичный demo URL и возможные hardening fixes;
- если Pages activation/state в `AndrewVerhoturov1/arena-test` ведёт себя нестандартно;
- если publish работает, но deployed demo ломается из-за asset/base/runtime contract.

## Уровень риска

Средний-высокий

## Цель

Подтвердить, что publish-контур действительно работает end-to-end: из локальной арены можно опубликовать sample prototype в `AndrewVerhoturov1/arena-test`, дождаться GitHub Pages deploy, открыть demo и catalog, затем обновить prototype и убрать его из public repo/site. Если verification выявит маленькие дефекты, устранить их в том же chunk без выхода за узкий hardening scope.

## Контекст проекта

- `P1` и `P2` уже приняты по review.
- Текущий sample prototype для проверки: `table-map-editor-v2-gpt`.
- В sample prototype уже есть publish contract и `vite.config.ts` с Pages-safe `base`.
- Root `.gitignore` игнорирует `arena-prototype-launcher/` и `_local/`, поэтому review будет опираться на фактическое содержимое файлов, report и remote state, а не на top-level `git diff`.
- `arena-test` уже bootstrap-нут workflow/tool-файлами, но именно live Pages verification ещё не подтверждён.

## Required Inputs

- [2026-05-23_arena_publish_github_pages.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-05-23_arena_publish_github_pages.md)
- [0004_arena_publish_backend_bootstrap_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0004_arena_publish_backend_bootstrap_report.md)
- [0005_arena_publish_ui_controls_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0005_arena_publish_ui_controls_report.md)
- [arena-prototype-launcher/server/src/routes/projects.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/routes/projects.ts)
- [arena-prototype-launcher/server/src/publishService.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/publishService.ts)
- [arena-prototype-launcher/server/src/types.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/types.ts)
- [arena-prototype-launcher/ui/src/App.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/App.tsx)
- [_local/prototypes/arena-tests/table-map-editor-v2 gpt/.arena-publish.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/prototypes/arena-tests/table-map-editor-v2%20gpt/.arena-publish.json)
- [_local/prototypes/arena-tests/table-map-editor-v2 gpt/vite.config.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/prototypes/arena-tests/table-map-editor-v2%20gpt/vite.config.ts)
- [arena-prototype-launcher/server/package.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/package.json)
- [arena-prototype-launcher/ui/package.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/package.json)

## Lookup Inputs

- [arena-prototype-launcher/launcher-data/registry.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/launcher-data/registry.json)
- [arena-prototype-launcher/server/src/registry.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/registry.ts)
- [scripts/external_chat_publish.py](/D:/Codex+Kilocode/projects/sword-of-rome-web/scripts/external_chat_publish.py)

## Do Not Read Unless Blocked

- старые handoff/report files вне `0004` и `0005`
- public canon/reference/docs files вне прямой связи с arena publish
- `.ai/external_chats/**`
- любые папки в `output/`

## Context Budget

- Фокус только на chunk `P3`.
- Не делать новый feature scope вне verification/hardening.
- Допустимы только маленькие fixes, которые прямо нужны для прохождения end-to-end publish path.
- Не рефакторить launcher шире publish-контуров.
- Не добавлять OAuth, PAT storage, новый deploy provider или новый repo layout.

## Важные файлы

- [arena-prototype-launcher/server/src/routes/projects.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/routes/projects.ts)
- [arena-prototype-launcher/server/src/publishService.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/server/src/publishService.ts)
- [arena-prototype-launcher/ui/src/App.tsx](/D:/Codex+Kilocode/projects/sword-of-rome-web/arena-prototype-launcher/ui/src/App.tsx)
- [_local/prototypes/arena-tests/table-map-editor-v2 gpt/.arena-publish.json](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/prototypes/arena-tests/table-map-editor-v2%20gpt/.arena-publish.json)
- [_local/prototypes/arena-tests/table-map-editor-v2 gpt/vite.config.ts](/D:/Codex+Kilocode/projects/sword-of-rome-web/_local/prototypes/arena-tests/table-map-editor-v2%20gpt/vite.config.ts)

## Expected Implementation Shape

### Verification path

- Поднять или использовать локальный launcher server.
- Пройти `publish` через launcher route для `table-map-editor-v2-gpt`.
- Подтвердить, что source и metadata появились в `AndrewVerhoturov1/arena-test`.
- Дождаться GitHub Actions / Pages deploy.
- Проверить:
  - root catalog URL;
  - demo URL prototype;
  - что demo реально отдаёт страницу и assets не 404.
- Затем изменить sample prototype минимально и безопасно, чтобы был осмысленный `update` signal.
- Пройти `publish-update`.
- Подтвердить, что remote source changed и deployed demo обновился.
- Затем пройти `remove`.
- Подтвердить, что source subtree удалён, index очищен, catalog/demo больше не доступны как актуальный published state.

### Hardening scope

- Если verification вскроет маленький defect в:
  - `arena-prototype-launcher/server/src/**`
  - `arena-prototype-launcher/ui/src/**`
  - sample prototype publish files
  - remote bootstrap files в `arena-test`
  и fix локален и прямо нужен для прохождения `P3`, исправить его.
- Если найден defect крупнее этого scope, вернуть `Blocked`, а не разворачивать большой redesign.

### Evidence expectations

- В report должны быть:
  - точные абсолютные даты/времена прогона;
  - launcher/API path, который использовался;
  - remote paths created/updated/removed;
  - URL catalog/demo;
  - что именно подтвердило update;
  - что именно подтвердило remove;
  - все ошибки и how resolved, если были;
  - если были hardening fixes, перечислить файлы и причину каждого fix.

## Allowed Changes

Локально:

- `arena-prototype-launcher/server/src/**`, только если нужен маленький hardening fix
- `arena-prototype-launcher/ui/src/**`, только если нужен маленький hardening fix
- `_local/prototypes/arena-tests/table-map-editor-v2 gpt/**`, только если нужен маленький publish/update verification change
- `arena-prototype-launcher/launcher-data/registry.json`, если verification path его реально меняет
- новый report по пути ниже

Remote-only через `gh api` в `AndrewVerhoturov1/arena-test`:

- `prototypes/**`
- `.github/workflows/pages.yml`
- `tools/**`

## Forbidden Changes

- не трогать другие prototype folders
- не трогать `output/`
- не трогать public workflow rules текущего repo
- не добавлять новые handoff files
- не менять architecture assumptions v1
- не переходить на другой hosting provider

## Report mode

full

## File writing policy

Можно писать только:

- разрешённые локальные файлы из scope выше
- новые/обновлённые remote files в `AndrewVerhoturov1/arena-test` через `gh api`
- новый report по пути ниже

## Stop Conditions

- `gh` недоступен или не авторизован
- нет write access в `AndrewVerhoturov1/arena-test`
- GitHub Pages нельзя активировать/использовать из текущего repo state
- launcher/API path не поднимается локально и без этого честный `P3` невозможен
- verification требует крупного redesign, а не маленького fix

## Критерии приёмки

- [ ] Реальный `publish` пройден через launcher path для `table-map-editor-v2-gpt`
- [ ] В `AndrewVerhoturov1/arena-test` появился published source subtree и metadata
- [ ] GitHub Pages workflow реально отработал
- [ ] Root catalog URL открывается
- [ ] Demo URL prototype открывается и assets не ломаются
- [ ] Реальный `publish-update` пройден и изменение дошло до deployed demo
- [ ] Реальный `remove` пройден и published state убран из repo/site
- [ ] Все найденные маленькие defects, мешающие `P3`, либо исправлены, либо run честно помечен `Blocked`
- [ ] UI/server после hardening-поправок проходят релевантную проверку (`npm run build`, если затронут UI; server/runtime check, если затронут backend)
- [ ] Report содержит проверяемое evidence по publish/update/remove и residual risks

## Куда записать report

[0006_arena_publish_e2e_verification_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0006_arena_publish_e2e_verification_report.md)

## Что вернуть после запуска

- путь к report
- список локально изменённых файлов
- список remote paths, созданных/обновлённых/удалённых в `AndrewVerhoturov1/arena-test`
- user-visible итог:
  - `publish verified`
  - `update verified`
  - `remove verified`
  - или `Blocked`
