# V3 Request Pack Skill Pilot Battle Plan

Slug: `v3_request_pack_skill_pilot`  
Owner: `Orc`  
Status: `draft / pending human approval`  
Date: `2026-06-02`  
Based on: `v3_request_pack_skill_pilot_plan_full.md`  
Active route: `Planner -> Orc`

## Назначение

Этот файл — сжатый operational-конспект для `Orc` по accepted `v3_request_pack_skill_pilot_plan_full.md`.

Он нужен, чтобы держать короткую исполнимую карту текущего allowed path без повторного чтения всего `plan_full`.

Этот battle plan:

- не заменяет `plan_full`;
- не открывает новый stage;
- не подменяет human approval;
- не запускает skill execution, proof, import или `V3 request`;
- не требует `status` как обязательный соседний артефакт.

## Что обязательно сохраняется из `plan_full`

- active route `Planner -> Orc`;
- это `Stage 5 pilot`;
- подпроект остаётся docs-only;
- `request != package != import != accepted result`;
- `Stage 6` не открыт;
- repo-level promotion не открыт;
- global skill materialization не разрешён без отдельного human gate;
- automation допустим только как узкий `request-pack preflight helper` по отдельному human decision;
- human approval ничем не заменяется.

## Границы

Этот battle plan не должен становиться:

- вторым `plan_full`;
- скрытым reopening scope;
- `status`-файлом;
- `journal`;
- `decisions`-логом;
- разрешением на live V3 proof.

Live-проверка V3, внешний прогон, proof, import и любой переход к `V3 request` остаются вне этого battle plan. Если человек захочет открыть такой шаг позже, это отдельный следующий gate.

## Source mapping

| Source section in `plan_full` | Remaining execution item in battle plan | Status |
|---|---|---|
| `## Назначение документа` | Зафиксировать, что battle plan служит только operational compression | `remaining` |
| `## Scope пилота` | Удержать docs-only scope без proof/import/request prep | `remaining` |
| `## Authorization boundary` | Не выходить за planning docs подпроекта | `remaining` |
| `## Lifecycle и gates` | Закрыть только текущий docs-layer через human verdict | `remaining` |
| `## Automation policy` | Не открывать helper без отдельного решения | `remaining` |
| `## Stop rules` | Остановиться при любой попытке открыть live path | `remaining` |
| `## Success criteria` | Считать успехом только согласованный docs-only слой | `remaining` |

## Remaining execution path

### Stage / Step `BP-01` — Проверить текущую docs-базу подпроекта

Purpose:

```text
Убедиться, что стартовый docs set и battle plan смотрят в одну сторону и не расходятся по границам пилота.
```

Do:

1. Прочитать `v3_request_pack_skill_pilot_plan_full.md`.
2. Сверить `readme`, `decisions`, `navigation`, `journal` с accepted boundaries.
3. Зафиксировать battle plan без расширения scope и без открытия новых артефактов.

Allowed paths:

```text
.ai/subprojects/v3_request_pack_skill_pilot/
```

Forbidden paths:

```text
.ai/v3/
scripts/
src/
AGENTS.md
.ai/repo_navigation.md
```

Verification:

- Границы во всех docs согласованы.
- `battle_plan` не требует `status`.

Human gate:

```text
none
```

Stop rule:

```text
Остановиться, если без новых файлов уже нельзя сохранить правду о текущем состоянии подпроекта.
```

Expected output:

```text
Согласованный docs-only battle plan без ложного открытия следующего слоя.
```

Status:

```text
completed
```

### Stage / Step `BP-02` — Получить human verdict по battle plan

Purpose:

```text
Закрыть gate на использование battle plan как рабочего документа Orc.
```

Do:

1. Показать человеку новый `battle_plan`.
2. Попросить проверить, что он не открывает `Stage 6`, proof, import или `V3 request`.
3. Дождаться явного human verdict.

Allowed paths:

```text
.ai/subprojects/v3_request_pack_skill_pilot/
```

Forbidden paths:

```text
Любые новые project files
Любой proof path
Любой import path
Любой repo-level promotion path
```

Verification:

- Человек видит один battle plan.
- Battle plan короче `plan_full` и не спорит с ним.

Human gate:

```text
required after completion
```

Stop rule:

```text
Остановиться сразу после публикации battle plan и не идти дальше без явной фразы человека о принятии.
```

Expected output:

```text
Human verdict: accepted / needs fixes / rejected.
```

Status:

```text
in progress
```

### Stage / Step `BP-03` — Стоп на docs-only readiness

Purpose:

```text
Не смешать согласование battle plan с запуском следующего execution слоя.
```

Do:

1. После human verdict не запускать proof, request prep, import или helper автоматически.
2. Считать любой следующий шаг новым отдельным решением человека.

Allowed paths:

```text
Human review and explicit next decision only
```

Forbidden paths:

```text
V3 request prep
request files
proof artifacts
skill files
status
Stage 6
repo-level docs
```

Verification:

- Никакой следующий слой не стартовал автоматически.
- Battle plan завершает только docs-only readiness.

Human gate:

```text
required before next stage
```

Stop rule:

```text
Остановиться, если кто-то пытается трактовать battle plan как разрешение на live V3 verification внутри этого пилота.
```

Expected output:

```text
Подпроект остаётся в docs-only readiness до нового human decision.
```

Status:

```text
not started
```

## Current execution pointer

```text
Current remaining step: BP-02
Next allowed action: human review of v3_request_pack_skill_pilot_battle_plan.md
Current gate: pending human verdict
```

## Verification before marking a step complete

Проверить:

- battle plan соответствует `plan_full`;
- docs-only граница не нарушена;
- `request != package != import != accepted result` не размыто;
- `Stage 6` не открыт;
- human gate не закрыт агентом;
- `status` не создан молча;
- live V3 check вынесен за пределы этого battle plan.

## Bugs and difficulties

```text
none found
```

## Resume note

Если контекст потерян, сначала открыть:

1. `v3_request_pack_skill_pilot_navigation.md`
2. этот `battle_plan`
3. `v3_request_pack_skill_pilot_plan_full.md`
4. `v3_request_pack_skill_pilot_decisions.md`
5. последние записи `v3_request_pack_skill_pilot_journal.md`

Потом продолжать только с `BP-02` и только в рамках human gate.
