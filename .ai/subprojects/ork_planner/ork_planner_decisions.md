# Ork Planner Decisions

Slug: `ork_planner`

---

## D-001 - Active route for this subproject

Date: 2026-05-31  
Status: accepted

### Decision

Подпроект `ork_planner` использует active route `Planner -> Orc`.

### Reason

Это соответствует accepted subproject model и role contract Planner.

### Consequences

Legacy `Boss / B1 / Junior Orchestrator` не используется как active маршрут.

### Related documents

- `ork_planner_plan_full.md#current-execution-model`
- `ork_planner_journal.md`

---

## D-002 - Bootstrap stops before Orc execution

Date: 2026-05-31  
Status: accepted

### Decision

Первая версия `ork_planner` ограничивается bootstrap-настройкой documentation container до отдельного human-approved Orc step.

### Reason

Задача просит создать подпроект и остановиться после bootstrap, без перехода к исполнению задач внутри него.

### Consequences

Следующий шаг требует отдельного решения человека.

### Related documents

- `ork_planner_plan_full.md#active-plan-rules`
- `ork_planner_status.md`

---

## D-003 - Do not use legacy B1/BOS route

Date: 2026-05-31  
Status: accepted

### Decision

`Boss / B1 / Junior Orchestrator` и block-style subfolders не являются active route для `ork_planner`.

### Reason

Accepted model для этого подпроекта держит planning и future execution в `Planner -> Orc`, а не в legacy hierarchy.

### Consequences

Use `plan_active`, `journal`, `status`, `decisions` вместо legacy block artifacts.

### Related documents

- `ork_planner_plan_full.md#removed-files`
- `ork_planner_navigation.md`

---

## D-004 - Keep critique files isolated under reviews

Date: 2026-05-31  
Status: accepted

### Decision

Imported critique files live only under `reviews/` and do not replace source `ork_planner_*.md` files.

### Reason

Review artifacts must stay separate from source-of-truth docs, otherwise resume and Orc handoff become ambiguous.

### Consequences

When critique package is imported, human and future sessions read `reviews/` as commentary layer, then update source docs separately if needed.

### Related documents

- `ork_planner_navigation.md`
- `ork_planner_status.md`
- `ork_planner_journal.md`
