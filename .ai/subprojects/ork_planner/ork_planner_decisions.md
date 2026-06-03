# Ork Planner Decisions

Slug: `ork_planner`  
Owner: `Orc`  
Status: `active-draft-pending-local-review`  
Last updated: `2026-06-01`  
Decision layer: `subproject-level accepted decisions`

## Назначение файла

Этот файл фиксирует важные решения подпроекта `ork_planner`, которые должны переживать отдельные сессии и влиять на дальнейшую работу.

Здесь не фиксируется обычный выбор инструмента Орка, технический способ выполнения одного шага или подробный лог действий. Такие вещи относятся к `ork_planner_journal.md`.

Главное правило:

```text
journal = что произошло;
decisions = какие важные решения теперь действуют;
status = самый свежий короткий контекст для продолжения.
```

## Human-requested correction note

Эта версия файла исправлена по прямому запросу человека.

Человек уточнил, что прежний draft ошибочно смешал `decisions` и `journal`: в `decisions` были записаны в основном выборы execution route / tool route Орка, а важные решения подпроекта из journal entries `J-20260601-002`, `J-20260601-003`, `J-20260601-004` не были вынесены в отдельный decisions layer.

Исправление не является самовольной переинтерпретацией внешнего draft. Оно сделано потому, что человек явно указал:

- `ork_planner_decisions.md` должен хранить важные решения подпроекта в целом;
- выбор конкретного инструмента Орка должен оставаться в journal;
- решения, временно записанные в journal до появления `ork_planner_decisions.md`, должны быть отражены здесь как принятые решения.

## Decision policy

### Что попадает в этот файл

В этот файл попадают решения, которые:

- меняют правила дальнейшей работы подпроекта;
- закрывают или уточняют human gate;
- фиксируют принятую границу роли;
- фиксируют принятый язык документации;
- фиксируют запрет или разрешение на крупное изменение;
- нужны будущему Орку/Planner, чтобы не повторить уже решённый спор.

### Что не попадает в этот файл

В этот файл не нужно заносить:

- какой tool был использован в конкретной сессии;
- технический маршрут одного update, если он не меняет процесс;
- полный список созданных/изменённых файлов;
- checksums, import report, command output;
- подробную историю чата;
- временные operational notes, которые важны только для ближайшего шага.

Это должно жить в `ork_planner_journal.md` или `ork_planner_status.md`.

## Разделение decision layers

### Planner decisions

Planner-owned решения живут в:

```text
.ai/subprojects/ork_planner/ork_planner_plan_decisions.md
```

Они отвечают за стратегию, lifecycle-модель, основание плана и Planner-level reasoning.

### Orc / subproject execution decisions

Orc-owned решения подпроекта живут здесь:

```text
.ai/subprojects/ork_planner/ork_planner_decisions.md
```

Они отвечают за принятые operational/process решения, которые важны для исполнения подпроекта, но не являются rewrite стратегии Planner.

### Human approvals

Human approval — отдельный gate evidence. Агент может рекомендовать, но не может сам заменить human approval.

Если human approval отсутствует, gate остаётся `pending`, даже если агент считает документ хорошим.

## Accepted subproject decisions

### D-20260601-001 — Stage 2 report accepted, но process issue по `grill-me` зафиксирован

- Status: `accepted`
- Source journal entry: `J-20260601-002`
- Decision: Stage 2 files/report считаются принятыми человеком, но в process memory остаётся замечание: `grill-me` был чрезмерно подробным и содержал слишком много низкоценных вопросов.
- Useful part preserved: вопрос про execution route был полезным.
- Consequence: дальше нельзя превращать каждый checkpoint в длинный опрос, если план уже утверждён и человеку нужен operational progress.
- Human approval: человек подтвердил, что Stage 2 files хорошие и приняты.
- Boundary: это не открывает автоматически Stage 3/4/5; каждый следующий gate требует своего allowed step.

### D-20260601-002 — Approved route нельзя обходить без explicit human override

- Status: `accepted`
- Source journal entry: `J-20260601-002`
- Decision: если route уже был утверждён человеком, агент не должен молча обходить его и выполнять альтернативный route.
- Reason: ранее был process error — approved Kilo route был обойдён до последующего explicit human override.
- Consequence: спорный route может быть рекомендован агентом, но утверждает человек.
- Human approval: process issue recorded by human request.

### D-20260601-003 — Документация подпроекта ведётся на русском языке

- Status: `accepted`
- Source journal entry: `J-20260601-003`
- Decision: user-facing документация `ork_planner` ведётся на русском языке.
- Allowed English: technical identifiers, file names, IDs, route names, machine-readable values.
- Reason: человек прямо сказал, что `ork_planner_journal.md` будет читаться часто, и документация должна быть понятна человеку.
- Consequence: новые local docs и reusable templates должны писать объяснения по-русски. English допустим только там, где он технически нужен.
- Human approval: recorded.

### D-20260601-004 — `battle_plan` является сжатым исполнительным конспектом оставшихся шагов из `plan_full`

- Status: `accepted`
- Source journal entry: `J-20260601-004`
- Human-requested clarification: человек дополнительно уточнил, что battle plan — это, по сути, весь полный план в части ещё невыполненных шагов, но оформленный сокращённо и конкретно для Орка.
- Decision: `ork_planner_battle_plan.md` понимается как сжатый operational/execution-конспект оставшегося пути из принятого `ork_planner_plan_full.md`, а не как документ только про Stage 4 и не как набор новых идей.
- Consequence: Stage 4 docs и reusable templates должны объяснять battle plan как документ выполнения: что Орк делает по оставшимся шагам полного плана, в каком порядке, с какими allowed/forbidden paths, checks и gates.
- Boundary: наличие Stage 5/6 в battle plan не означает, что Stage 5/6 уже начаты. Это только remaining path; фактический start stage требует соответствующего gate.
- Human approval: recorded.

### D-20260601-005 — Большие смысловые переписывания existing docs требуют explicit human permission

- Status: `accepted`
- Source journal entry: `J-20260601-004`
- Decision: большие смысловые rewrite existing docs нельзя начинать без явного разрешения человека.
- Reason: ранее была преждевременно подготовлена большая переработка.
- Consequence: Stage 4 package может обновлять только разрешённые файлы в пределах allowed paths. `plan_full`, `battle_plan`, `plan_index` не переписываются.
- Human approval: recorded.

### D-20260601-006 — Для Stage 4/templates из journal и plan_decisions берутся только универсальные process rules

- Status: `accepted`
- Source journal entry: `J-20260601-004`
- Decision: reusable template layer должен брать из `ork_planner_journal.md` и `ork_planner_plan_decisions.md` только универсальные process rules, а не всю локальную историю `ork_planner`.
- Consequence: templates не должны быть копией `ork_planner` с заменой slug. Они должны быть пригодны для будущих подпроектов.
- Human approval: recorded.

### D-20260601-007 — `readme`, `status`, `journal`, `decisions`, `navigation` имеют разные задачи

- Status: `accepted-for-stage4-doc-system`
- Decision: local docs system должен сохранять разделение обязанностей:
  - `readme` = human-first entry door;
  - `status` = самый свежий короткий live snapshot;
  - `journal` = factual execution log;
  - `decisions` = важные решения подпроекта;
  - `navigation` = карта документов и reading routes.
- Consequence: нельзя сливать эти файлы в один общий отчёт.
- Human approval: pending with Stage 4 acceptance, but correction requested by human.

### D-20260601-008 — `Planner -> Orc` остаётся единственным active route

- Status: `accepted-for-current-subproject`
- Decision: активный route для `ork_planner` — `Planner -> Orc`.
- Rejected active routes: legacy `Boss / B1 / Junior Orchestrator`.
- Consequence: legacy terms можно упоминать только как historical context, не как active route.
- Human approval: pending with Stage 4 acceptance for this docs slice; consistent with task constraints.

### D-20260601-009 — Stage 4 package остаётся external draft until local review and human verdict

- Status: `active-for-current-package`
- Decision: текущий Stage 4 docs slice — внешний V3 draft package, а не изменение репозитория.
- Consequence: package может быть review/import candidate, но не считается принятым до local review and human verdict.
- Human approval: `pending`.

### D-20260602-010 — Универсальный стартовый минимум документов для нового подпроекта

- Status: `accepted`
- Source journal entry: `J-20260602-003`
- Decision: в начале работы над новым подпроектом Орк должен создавать минимальный стартовый набор документов:
  - `*_readme.md`
  - `*_decisions.md`
  - `*_plan_index.md`
  - `*_journal.md`
  - `*_navigation.md`
- Consequence: этот набор считается базовым стартовым минимумом для новых подпроектов, пока человек явно не утвердит другое правило для конкретного пилота.
- Boundary: это правило не означает автоматическое создание полного doc-set и не делает `battle_plan` обязательным первым артефактом.
- Human approval: recorded by direct user instruction.

## Superseded or corrected decisions

### S-20260601-001 — `ork_planner_decisions.md` как log tool-route choices

- Status: `corrected-by-human-request`
- Old draft issue: файл был сделан слишком похожим на список execution/tool decisions Орка.
- Corrected rule: tool route и выбор способа действия фиксируются в journal; decisions фиксирует важные решения подпроекта.
- Evidence: human correction request after first package draft.

### S-20260601-002 — `ork_planner_status.md` как расширенный state document

- Status: `corrected-by-human-request`
- Old draft issue: status был слишком длинным и слишком похожим на отдельный state document.
- Corrected rule: status — короткий live snapshot ближайшего контекста, который может постоянно перезаписываться.
- Evidence: human correction request after first package draft.

## Rejected options

### R-20260601-001 — Начать Stage 5 или Stage 6 внутри этого package

- Status: `rejected`
- Reason: текущая работа — Stage 4 only. Stage 5/6 остаются future stages and require later human gate.

### R-20260601-002 — Переписать `ork_planner_plan_full.md`

- Status: `rejected`
- Reason: forbidden path for this package; большие смысловые переписывания existing docs без explicit human permission недопустимы.

### R-20260601-003 — Переписать `ork_planner_battle_plan.md`

- Status: `rejected`
- Reason: battle plan уже принят человеком и не должен заново оспариваться в Stage 4 docs package.

### R-20260601-004 — Вернуть legacy route как active route

- Status: `rejected`
- Reason: active route remains `Planner -> Orc`.

## Waivers

### W-20260601-001 — Post-import testing waived

- Status: `active`
- Waiver: automated post-import testing waived by task request.
- Reason: docs-only external package; no source-code behavior is part of this task.
- Remaining check: local review, path check, checksum check, human read-and-follow.

### W-20260601-002 — Direct repo write unavailable

- Status: `active`
- Waiver: no direct repository write is performed by external artifact producer.
- Reason: task explicitly asks for ZIP artifact package only.
- Remaining check: local Codex/Kilo review/import path if human chooses.

## Human approvals and verdicts

### HA-20260601-001 — Stage 2 report accepted

- Status: `accepted`
- Evidence: recorded in `J-20260601-002`.
- Boundary: this accepts Stage 2 report, not Stage 4 docs.

### HA-20260601-002 — Battle plan accepted

- Status: `accepted`
- Evidence: task context says battle plan already accepted by human.
- Boundary: do not rewrite battle plan in this package.

### HA-20260601-003 — Stage 4 docs acceptance

- Status: `pending`
- Required evidence: explicit human verdict after local review.

Example accepted wording:

```text
Stage 4 local docs accepted
```

Example correction wording:

```text
Stage 4 needs fixes: <что поправить>
```

## Relation to planner decision log

`ork_planner_plan_decisions.md` remains Planner-owned. This file does not replace it.

Use separation:

```text
Planner plan_decisions = why strategy/lifecycle exists.
Orc decisions = what important execution/process decisions now govern this subproject.
Human approvals = gates closed by the human, not by the agent.
Journal = factual actions and evidence.
Status = nearest live continuation context.
```

For future reusable templates, take only universal process rules from this file, not local `ork_planner` history.
