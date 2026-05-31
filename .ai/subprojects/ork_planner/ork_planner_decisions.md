# Ork Planner Decisions

Slug: `ork_planner`

---

## D-001 — Active route for this subproject

Date: 2026-05-31  
Status: accepted

### Decision

Подпроект `ork_planner` использует active route `Planner -> Orc`.

### Reason

Это соответствует текущему active workflow проекта и role contract Planner.

### Consequences

Legacy `Boss / B1 / Junior Orchestrator` не используется как active маршрут.

### Related documents

- `ork_planner_plan_full.md#current-execution-model`
- `ork_planner_journal.md`

---

## D-002 — Bootstrap stops before Orc execution

Date: 2026-05-31  
Status: accepted

### Decision

Первая версия подпроекта ограничивается созданием стартового documentation container без запуска Orc-mode.

### Reason

Задача просит создать подпроект и остановиться после bootstrap, без перехода к исполнению задач внутри него.

### Consequences

Следующий шаг требует отдельного решения человека.

### Related documents

- `ork_planner_plan_full.md#acceptance-criteria`
- `ork_planner_status.md`
