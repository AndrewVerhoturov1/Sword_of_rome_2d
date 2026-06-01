# {Subproject Title} Plan Full

Slug: `{subproject_slug}`  
Status: `draft-planner-owned`  
Owner: `Planner`  
Target file: `.ai/subprojects/{subproject_slug}/{subproject_slug}_plan_full.md`  
Active route: `Planner -> Orc`  
Language: Russian user-facing documentation; English technical identifiers remain English.

> Этот template создаёт большой Planner-owned план. Он не является journal, status, decisions или battle_plan. Он не запускает Orc сам по себе.

## Purpose

Коротко объяснить:

- что это за подпроект;
- какой результат нужен;
- почему это отдельный subproject;
- какой active route используется.

## Plain-Russian summary for human

5-10 строк простым языком:

- где мы сейчас;
- что будет сделано;
- чего не будет сделано;
- где нужен human gate.

## Mission of `{subproject_slug}`

Описать миссию подпроекта так, чтобы Orc мог потом исполнять без угадывания strategy.

## Non-goals and forbidden drifts

Обязательные пункты:

- не смешивать `Planner` и `Orc`;
- не подменять human approval решением агента;
- не трогать forbidden paths;
- не расширять scope без human decision;
- не возвращать legacy active route, если repo использует `Planner -> Orc`.

## Source basis and authority order

Перечислить реально прочитанные или required источники.

Пример:

```text
1. User request
2. Repo-level rules
3. Existing subproject docs
4. Related plans/decisions
5. External critique, if used
```

Правило:

```text
If source was not read, do not claim it as read.
```

## Role boundaries

### Planner

Planner отвечает за strategy, constraints, allowed/forbidden paths, gates and acceptance criteria.

Planner не должен вести live execution journal/status/decisions, кроме явно помеченного temporary scaffold.

### Orc

Orc отвечает за execution route, tool choice, evidence, journal/status/decisions/navigation, stop rules and human checks.

Orc не должен молча переписывать strategy `plan_full`.

### Human

Human отвечает за approval gates, спорные route decisions, final acceptance and scope changes.

## Artifact model

| File | Owner | Audience | Purpose |
|---|---|---|---|
| `{subproject_slug}_plan_full.md` | `Planner` | human + agents | Full strategy and lifecycle. |
| `{subproject_slug}_plan_index.md` | `Orc` | agents | Anchor/index map for `plan_full`. |
| `{subproject_slug}_navigation.md` | `Orc` | human + agents | Subproject-wide map. |
| `{subproject_slug}_journal.md` | `Orc` | human + agents | Factual execution log. |
| `{subproject_slug}_battle_plan.md` | `Orc` | human + agents | Сжатый исполнительный конспект оставшихся шагов из принятого `plan_full`. |
| `{subproject_slug}_readme.md` | `Orc` | human-first | Simple entry door. |
| `{subproject_slug}_status.md` | `Orc` | human + agents | Current live snapshot. |
| `{subproject_slug}_decisions.md` | `Orc` | human + agents | Orc execution decisions. |
| `{subproject_slug}_plan_decisions.md` | `Planner` | Planner + reviewers | Planner decision memory, if needed. |

## Lifecycle overview

Заполнить stages под конкретный подпроект.

Пример:

```text
Stage 1 — Planner plan review
Stage 2 — First Orc navigation pass
Stage 3 — Battle plan + human approval
Stage 4 — Local docs/execution slice
Stage 5 — Optional proof/pilot/follow-up slice
Stage 6 — Optional repo-level alignment
```

Если stages меньше, явно объяснить почему.

## Allowed writes

Перечислить точные allowed paths по stage.

```text
.ai/subprojects/{subproject_slug}/...
```

Не писать “и другие похожие файлы”, если scope строгий.

## Forbidden writes

Перечислить forbidden paths.

Типовые examples:

```text
.ai/rules/
.ai/repo_navigation.md
AGENTS.md
src/
scripts/
ideas/
```

Если repo-level update нужен, вынести его в отдельный stage and human gate.

## Tool route recommendation or waiver

Для каждого крупного шага указать одно из двух:

```text
Recommended route: <route>
Reason: <why>
Human gate: <needed/not needed>
```

или

```text
Waiver: <tool route waived>
Reason: <why safe>
```

## Human gates

Каждый gate должен отвечать:

- что человек должен проверить;
- какая фраза закрывает gate;
- что запрещено до закрытия gate.

## Verification expectations

Указать проверки:

- existence checks;
- path checks;
- diff scope;
- link/navigation checks;
- human read-and-follow check;
- tests, if applicable.

Если tests waived, написать почему.

## Stop rules

Orc обязан остановиться, если нет human approval, нужен forbidden path, route спорный, scope изменился, plan стал недостаточным или требуется новая strategy.

## Acceptance criteria

Список конкретных done conditions:

- files exist;
- navigation points to them;
- status says current gate;
- journal has factual entry;
- human accepted gate.

## Anchor map

| Section | Anchor | Purpose |
|---|---|---|
| Purpose | `#purpose` | Why this file exists |
| Role boundaries | `#role-boundaries` | Planner/Orc/Human split |
| Lifecycle | `#lifecycle-overview` | Stage sequence |
| Acceptance | `#acceptance-criteria` | Done conditions |

## Final operating rule

```text
Planner creates plan. Human accepts. Orc executes. Human gates remain explicit.
```
