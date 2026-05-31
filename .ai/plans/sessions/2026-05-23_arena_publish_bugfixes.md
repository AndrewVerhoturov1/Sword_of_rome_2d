# Session: arena_publish_bugfixes

## Session ID

`2026-05-23_arena_publish_bugfixes`

## Status

in_progress

## Goal

Через Kilo найти и исправить баги в publish-контуре арены, которые проявились при реальном использовании:

- publish-кнопка вводит в заблуждение для непригодных prototype folders;
- пользователь не видит ясную причину отказа publish;
- demo URL может открываться как `404`, хотя UI уже считает prototype опубликованным.

## Approved Plan

### P1: Debug Publish Eligibility And Demo Readiness

- Status: pending.
- Воспроизвести и зафиксировать root cause для двух классов проблем:
  - непригодные prototypes выглядят publishable;
  - valid prototype получает false-ready demo state.
- Исправить backend/UI так, чтобы:
  - для непригодных prototypes publish был явно disabled/hidden или имел явную причину;
  - valid publish не выглядел готовым до реальной готовности demo, либо пользователь видел честный deploy-in-progress state.
- Проверить на реальных локальных prototypes и на remote repo `AndrewVerhoturov1/arena-test`.

## Active Plan Item

`P1: Debug Publish Eligibility And Demo Readiness`

## Runs

- `Session run: 001` - pending; prepare Kilo debug/fix handoff for publish eligibility and demo 404 issues.

## User Overrides

- Исполнение делает `Kilo Code`, не Codex worker.
- Нужен один public target repo: `AndrewVerhoturov1/arena-test`.
- Исправлять надо реальные баги по результатам живого прогона, а не только текстовые сообщения.
- Важно отделить ожидаемый reject непригодного prototype от настоящего бага UX/flow.

## Checkpoint State

- Предыдущая session `arena_publish_github_pages` завершена: backend, UI controls и базовый E2E publish-path уже были приняты.
- Новый инцидент найден в реальном использовании после этого:
  - пользователь попытался publish несколько prototypes;
  - только `table-map-editor-v2-gpt` реально опубликовался;
  - для остальных publish-кнопка вела себя как будто действие возможно, но результата не было;
  - demo для опубликованного prototype открывалась как `404`.
- Из preflight-проверки Codex:
  - `qwen-3-7`, `hex-primer`, `table-map-editor-canvas-local-fixed` сейчас не имеют `.arena-publish.json`;
  - только `table-map-editor-v2-gpt` имеет publish-contract;
  - UI publish-controls сейчас не знают publish-eligibility заранее;
  - backend возвращает `published` сразу после source upload/index update, а не после подтверждённой готовности Pages demo.
