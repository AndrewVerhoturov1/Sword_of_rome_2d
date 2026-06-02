# V3 Request Pack Skill Pilot Decisions

Слаг: `v3_request_pack_skill_pilot`  
Владелец: `Orc`  
Статус: `draft`  
Дата обновления: `2026-06-02`  
Decision layer: `subproject-level accepted decisions`

## Назначение

Этот файл хранит только долгоживущие решения по подпроекту. Он не является журналом действий и не заменяет `plan_full`.

## Accepted subproject decisions

### D-20260602-001 — `plan_full` остаётся стратегической базой подпроекта

- Status: `accepted`
- Source: `v3_request_pack_skill_pilot_plan_full.md`
- Decision: accepted `plan_full` используется как canonical strategy source для этого пилота.
- Reason: пилоту нужен один явный стратегический источник истины.
- Consequence: operational docs опираются на `plan_full`, но не переписывают его заново.
- Boundary: это решение не разрешает менять `plan_full` молча или открывать новый stage без отдельного gate.
- Human approval: `recorded`

### D-20260602-002 — active route остаётся `Planner -> Orc`

- Status: `accepted`
- Source: `accepted plan_full`
- Decision: активный маршрут подпроекта — `Planner -> Orc`.
- Reason: это явная рабочая схема пилота.
- Consequence: `Planner` держит стратегию, `Orc` ведёт execution docs и evidence.
- Boundary: legacy route нельзя возвращать как active route.
- Human approval: `recorded`

### D-20260602-003 — подпроект остаётся docs-only

- Status: `accepted`
- Source: `accepted plan_full`
- Decision: текущий подпроект ограничен docs-only слоем.
- Reason: пилот должен сначала зафиксировать границы и gates.
- Consequence: стартовый набор ограничен документами подпроекта.
- Boundary: решение не разрешает skill execution, proof run, import, scripts или repo-level writes за пределами этого docs slice.
- Human approval: `recorded`

### D-20260602-004 — `request != package != import != accepted result`

- Status: `accepted`
- Source: `accepted plan_full`
- Decision: request, returned package, import и accepted result считаются разными стадиями, их нельзя смешивать.
- Reason: это защищает пилот от ложного прогресса и premature acceptance.
- Consequence: даже хороший request pack сам по себе не равен import-stage или accepted result.
- Boundary: package-only review не открывает import-stage автоматически.
- Human approval: `recorded`

### D-20260602-005 — `Stage 6` не открыт

- Status: `accepted`
- Source: `accepted plan_full`
- Decision: `Stage 6` на текущем шаге не начат.
- Reason: подпроект пока находится в рамках `Stage 5 pilot`.
- Consequence: docs не должны описывать `Stage 6` как активную работу.
- Boundary: нельзя объявлять следующий stage начатым без отдельного human gate.
- Human approval: `recorded`

### D-20260602-006 — repo-level promotion не открыт

- Status: `accepted`
- Source: `accepted plan_full`
- Decision: repo-level promotion пока закрыт.
- Reason: даже успешный pilot не равен promoted standard.
- Consequence: подпроектные docs не трактуются как repo-level policy rollout.
- Boundary: нельзя обновлять repo-level docs как promoted standard без отдельного gate.
- Human approval: `recorded`

### D-20260602-007 — proposed global skill home не materialized

- Status: `accepted`
- Source: `accepted plan_full`
- Decision: proposed global skill home остаётся только proposed до отдельного human gate.
- Reason: materialization skill считается capability-sensitive шагом.
- Consequence: текущий подпроект может ссылаться на proposed path, но не материализует skill.
- Boundary: это решение не разрешает создавать global skill files автоматически.
- Human approval: `recorded`

### D-20260602-008 — automation policy узкая

- Status: `accepted`
- Source: `accepted plan_full`
- Decision: automation допустим только как возможный узкий `request-pack preflight helper` и только по отдельному human decision.
- Reason: пилот должен оставаться узким и контролируемым.
- Consequence: никакая широкая automation layer сейчас не открыта.
- Boundary: нельзя расширять automation до scripts, import helpers или repo-wide tooling без нового gate.
- Human approval: `recorded`

### D-20260602-009 — human approval обязателен

- Status: `accepted`
- Source: `accepted plan_full`
- Decision: human approval ничем не заменяется.
- Reason: gates этого пилота должны закрываться человеком, а не агентным выводом.
- Consequence: любые route recommendation, package review и docs updates держат human verdict отдельно.
- Boundary: agent recommendation не считается approval.
- Human approval: `recorded`

## Rejected options

### R-20260602-001 — автоматическое расширение стартового docs set

- Status: `rejected`
- Option: автоматически создать `battle_plan`, `status`, skill files, request files или proof artifacts на первом шаге.
- Reason: human-approved universal rule задаёт минимальный стартовый набор и запрещает молчаливое расширение.
- Safe alternative: сначала создать только `readme`, `decisions`, `plan_index`, `journal`, `navigation`.

## Maintenance rule

- Не превращать этот файл в journal.
- Не записывать сюда разовые tool choices.
- При новых долгоживущих решениях добавлять новую decision entry, а не переписывать историю действий.
