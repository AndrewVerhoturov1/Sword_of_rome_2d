# Notebook Entry

- External Question ID: `V1-20260602-061552`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-06-02_V1-20260602-061552_grounded-second-opinion-po-stage-5-bridge.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/subprojects/ork_planner/ork_planner_plan_full.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/subprojects/ork_planner/ork_planner_battle_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/subprojects/templates/subproject_templates_guide.md`

## Candidate Navigation Entry

Topic: Grounded second opinion по Stage 5 bridge
Summary: Рекомендован один временный документ `.ai/subprojects/ork_planner/ork_planner_stage5_first_pilot_bridge.md`, который не является repo-level standard и нужен только для первого tiny docs-only pilot. Минимальный pilot set: `plan_full`, `battle_plan`, `readme`, `status`, `navigation`, `journal`; `plan_index` и `decisions` допустимо waive-нуть при явном условии.

## Raw Response

# External Chat Response

## External Question ID

V1-20260602-061552

## Context Readback

* `external_chat_rules.md` — required central rules: fully read.
* `ai-workflow-core/repo_navigation.md` — required central navigation: fully read.
* `Sword_of_rome_2d/.ai/repo_navigation.md` — project-specific navigation: partially read.
* `ork_planner_battle_plan.md` — project-specific link: partially read.
* `ork_planner_navigation.md` — project-specific link: partially read.
* `subproject_templates_guide.md` — project-specific link: partially read.
* `AGENTS.md` — project-specific link: partially read.
* `V1_navigation.md` — required project V1 navigation: partially read.
* Navigation-discovered V1 notebook `V1-20260601-015836`: fully read.
* Navigation-discovered V1 notebook `V1-20260531-221800`: fully read.
* Navigation-discovered `ork_planner_plan_full.md`: partially read.
* Navigation-discovered `ork_planner_plan_decisions.md`: partially read.
* Navigation-discovered `ork_planner_readme.md`: partially read.
* Navigation-discovered `ork_planner_status.md`: fully read.
* Navigation-discovered `ork_planner_decisions.md`: partially read.
* Navigation-discovered `ork_planner_journal.md`: partially read.
* Prompt context excerpts: fully read.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require exactly this kind of answer discipline: honest Context Readback, no `fully read` unless a file was actually opened, separation of central-doc claims from project/excerpt claims, and no claims about local repo state without provided project-specific context. ([GitHub][1])

Central navigation confirms that central `ai-workflow-core` navigation is a closed set for central workflow docs and does **not** give authority over consumer repo facts; consumer repo files must be explicitly provided as project-specific links/excerpts. ([GitHub][2])

### Confirmed from provided excerpts

From your excerpt, the current local fact for this question is: `Stage 4` accepted by human, changes committed and pushed to `main`, commit `f06c1bc`, message `Docs: accept ork_planner stage 4 docs system`. I did not independently verify the commit hash; I treat it as provided context.

Project `plan_full` says `Stage 5` starts only after Stage 4 local docs system is accepted, creates a new tiny docs-only subproject from scratch, must prove `Planner -> Orc` on clean context, and must not become repo-wide migration. ([GitHub][3])

`plan_full` also says Stage 5 can use a smaller document set if the tiny task justifies it, but any reduction must be explicit and must not weaken role boundaries. ([GitHub][3])

`battle_plan` says Stage 5 has no preselected slug, must create a new small docs-only subproject, write only inside its local subproject layer, not touch repo-level files, and not become hidden continuation of `ork_planner`. It also says the exact Stage 5 paths must be named by Orc and accepted by the human at Stage 5 start. ([GitHub][4])

The template guide confirms the normal full doc-set separation: `plan_full`, `plan_index`, `navigation`, `journal`, `battle_plan`, `readme`, `status`, `decisions`; it also says these layers must not be mixed, and that `battle_plan` is a compressed operational summary of remaining steps from accepted `plan_full`, not a new strategy. ([GitHub][5])

### Not available / not verified

I did not verify local filesystem state, `git status`, actual local diff, or whether every Stage 4 file on disk now reflects the accepted state.

Some opened `main` documents still contain older wording such as `draft-pending-local-review` / Stage 4 pending. For this answer, I treat your prompt excerpt as newer local truth and the opened docs as possibly stale where they conflict.

I did not read every individual template file. I read the template guide and navigation references, so exact template body quality is not verified here.

Stage 5 slug and tiny pilot topic are not available in provided context and should not be invented as already chosen.

### Recommended temporary bridge

Да, для первого `Stage 5` pilot chat достаточно **одного temporary bridge-doc**.

Рекомендуемый документ:

```text
.ai/subprojects/ork_planner/ork_planner_stage5_first_pilot_bridge.md
```

Роль: временная инструкция-переходник для первого нового Stage 5 chat.

Почему это безопасное место:

* документ относится к `ork_planner` как к pilot/meta-подпроекту, который уже содержит текущую локальную правду о Stage 4 и Stage 5;
* он не создаёт repo-level standard;
* он не требует заранее выбранного Stage 5 slug;
* он не загрязняет будущий новый подпроект до human decision по slug/scope;
* после первого pilot его можно удалить, архивировать или заменить repo-level alignment на Stage 6, но сам он не становится каноном.

### Minimal pilot set

Для первого tiny docs-only pilot я рекомендую **reduced set из 6 обязательных файлов**, а не full doc-set:

```text
.ai/subprojects/{stage5_slug}/{stage5_slug}_plan_full.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_battle_plan.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_readme.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_status.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_navigation.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_journal.md
```

Можно отложить / waiver для первого tiny pilot:

```text
.ai/subprojects/{stage5_slug}/{stage5_slug}_plan_index.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_decisions.md
```

Почему это безопасно:

* `plan_full` сохраняет Planner-owned основу;
* `battle_plan` сохраняет Orc-owned исполнительный конспект;
* `readme`, `status`, `navigation` дают human-first вход, live snapshot и карту;
* `journal` даёт evidence, что маршрут реально соблюдался;
* `plan_index` можно не создавать, если `plan_full` короткий и сам имеет понятные заголовки;
* `decisions` можно не создавать, если нет долгоживущих решений, кроме уже принятых human gates. Если появляется важное решение, waiver сразу отменяется и файл `{slug}_decisions.md` нужно создать.

### Draft document

````md
# Temporary Stage 5 Bridge — первый tiny docs-only pilot

Status: `temporary-bridge`
Owner: `Orc`, но только как bridge-инструкция
Audience: новый Codex chat + человек
Active route: `Planner -> Orc`
Scope: первый новый `Stage 5` docs-only pilot
Not a repo-level standard: yes

## 1. Назначение

Этот документ — временный bridge для первого нового `Stage 5` chat.

Он нужен только потому, что локальная docs system для `ork_planner` уже собрана и принята человеком, но ещё не поднята в repo-level global docs. Новый chat без bridge может не понять:

- где сейчас живёт правда по документации;
- что читать первым;
- какие файлы создавать;
- где остановиться;
- где нужен human gate;
- что нельзя считать автоматически разрешённым.

Этот bridge не является:

- `readme`;
- `status`;
- `navigation`;
- `journal`;
- `decisions`;
- `battle_plan`;
- `plan_full`;
- repo-level workflow standard.

Он не заменяет ни один из этих документов.

## 2. Текущая правда на момент bridge

Для старта первого `Stage 5` считать текущей правдой:

```text
Stage 4 accepted by human.
Changes committed and pushed to main.
Commit: f06c1bc
Commit message: Docs: accept ork_planner stage 4 docs system
Active route: Planner -> Orc
Stage 5 has not started.
Stage 6 has not started.
```

Если какой-то уже существующий `ork_planner` документ всё ещё говорит, что Stage 4 pending, считать это stale wording относительно текущего human-provided fact. Не исправлять такие файлы в рамках Stage 5 без отдельного разрешения.

## 3. Где сейчас живёт documentation truth

Текущая локальная правда по системе подпроектов живёт здесь:

```text
.ai/subprojects/ork_planner/
.ai/subprojects/templates/
```

Главные файлы для Stage 5:

```text
.ai/subprojects/ork_planner/ork_planner_plan_full.md
.ai/subprojects/ork_planner/ork_planner_battle_plan.md
.ai/subprojects/ork_planner/ork_planner_navigation.md
.ai/subprojects/ork_planner/ork_planner_status.md
.ai/subprojects/ork_planner/ork_planner_journal.md
.ai/subprojects/ork_planner/ork_planner_decisions.md
.ai/subprojects/templates/subproject_templates_guide.md
```

Важно:

```text
ork_planner_plan_full.md = Planner-owned strategy
ork_planner_battle_plan.md = Orc-owned execution summary
ork_planner_navigation.md = map of current docs
ork_planner_status.md = short live state
ork_planner_journal.md = factual execution evidence
ork_planner_decisions.md = important accepted subproject decisions
subproject_templates_guide.md = guide to reusable templates
```

Не смешивать эти роли документов.

## 4. Minimal read order для нового Stage 5 chat

### Human-first read order

Если человек хочет быстро понять, можно ли запускать Stage 5:

```text
1. этот bridge
2. .ai/subprojects/ork_planner/ork_planner_readme.md
3. .ai/subprojects/ork_planner/ork_planner_status.md
4. .ai/subprojects/ork_planner/ork_planner_navigation.md
5. .ai/subprojects/templates/subproject_templates_guide.md
```

### Agent-oriented read order

Новый Codex chat перед созданием Stage 5 файлов читает:

```text
1. этот bridge
2. AGENTS.md
3. .ai/subprojects/ork_planner/ork_planner_plan_full.md
4. .ai/subprojects/ork_planner/ork_planner_battle_plan.md
5. .ai/subprojects/ork_planner/ork_planner_navigation.md
6. .ai/subprojects/ork_planner/ork_planner_status.md
7. .ai/subprojects/ork_planner/ork_planner_decisions.md
8. latest relevant entries in .ai/subprojects/ork_planner/ork_planner_journal.md
9. .ai/subprojects/templates/subproject_templates_guide.md
10. only the specific templates needed for the reduced Stage 5 set
```

Не читать весь repo "на всякий случай". Stage 5 — маленький docs-only pilot.

## 5. Stage 5 не имеет выбранного slug заранее

Новый chat не должен считать slug уже выбранным.

Перед созданием файлов нужно явно зафиксировать:

```text
stage5_slug = <короткий безопасный slug>
tiny task = <одна маленькая docs-only задача>
target folder = .ai/subprojects/{stage5_slug}/
```

Slug должен быть маленьким и техническим, например:

```text
docs_naming_pilot
navigation_cleanup_pilot
tiny_docs_pilot
```

Это только примеры, не готовое решение.

## 6. Reduced creation set для первого tiny pilot

Для первого Stage 5 pilot использовать reduced set, а не full doc-set по умолчанию.

Обязательные файлы:

```text
.ai/subprojects/{stage5_slug}/{stage5_slug}_plan_full.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_battle_plan.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_readme.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_status.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_navigation.md
.ai/subprojects/{stage5_slug}/{stage5_slug}_journal.md
```

Допустимые waivers:

```text
.ai/subprojects/{stage5_slug}/{stage5_slug}_plan_index.md
```

Можно отложить, если `{stage5_slug}_plan_full.md` очень короткий и имеет понятные headings.

```text
.ai/subprojects/{stage5_slug}/{stage5_slug}_decisions.md
```

Можно отложить, если нет долгоживущих решений подпроекта. Если появляется важное решение, human approval, изменение scope или спорная граница роли — создать decisions file.

## 7. Что создавать первым

Первым создаётся только Planner-owned base:

```text
.ai/subprojects/{stage5_slug}/{stage5_slug}_plan_full.md
```

Этот файл должен быть коротким. Он должен ответить:

* зачем нужен tiny pilot;
* какой точный docs-only task;
* почему он low-risk;
* какие файлы разрешено создать;
* какие файлы запрещено трогать;
* где Planner останавливается;
* как Orc продолжает только после human approval.

После создания `{stage5_slug}_plan_full.md` новый chat обязан остановиться и попросить human acceptance.

## 8. Planner -> Orc gate

Orc не начинается автоматически.

После `{stage5_slug}_plan_full.md` нужен явный human signal, например:

```text
План принят. Запускаем Orc для tiny Stage 5 pilot.
```

Без такого сигнала нельзя создавать Orc-owned docs.

Orc-owned docs:

```text
{stage5_slug}_battle_plan.md
{stage5_slug}_readme.md
{stage5_slug}_status.md
{stage5_slug}_navigation.md
{stage5_slug}_journal.md
{stage5_slug}_decisions.md, если waiver отменён
{stage5_slug}_plan_index.md, если waiver отменён
```

## 9. Orc execution order

После human approval Planner base:

```text
1. Orc создаёт {stage5_slug}_battle_plan.md.
2. Orc останавливается и просит human approval battle plan.
3. После approval Orc создаёт remaining reduced docs:
   - readme
   - status
   - navigation
   - journal
   - optional decisions if needed
   - optional plan_index if needed
4. Orc возвращает report.
5. Human принимает или отклоняет Stage 5.
```

Для tiny pilot допускается один короткий battle plan. Он не должен превращаться в новый большой plan.

## 10. Stop rules

Новый chat обязан остановиться, если:

* Stage 5 slug не выбран;
* tiny task не выбран;
* target paths не названы явно;
* хочется трогать repo-level files;
* хочется менять `AGENTS.md`;
* хочется менять `.ai/repo_navigation.md`;
* хочется менять `.ai/rules/*`;
* хочется менять source code;
* хочется начинать Stage 6;
* возникает legacy route `Boss / B1 / Junior Orchestrator`;
* нужно изменить `ork_planner_plan_full.md`;
* нужно исправлять stale Stage 4 wording в старых файлах;
* требуется full doc-set вместо reduced set без причины;
* agent хочет сам принять human gate.

В этих случаях ответ должен быть:

```text
Остановился. Нужен human decision: <какое решение нужно>.
```

## 11. Human decisions, которые нельзя подменять

Human должен явно принять:

```text
1. Stage 5 slug.
2. Tiny docs-only task.
3. Reduced creation set and waivers.
4. {stage5_slug}_plan_full.md.
5. {stage5_slug}_battle_plan.md.
6. Final Stage 5 result.
```

Agent может рекомендовать, но не может сам заменить human approval.

## 12. Forbidden for first Stage 5 pilot

Запрещено:

```text
Stage 6
repo-level alignment
AGENTS.md edits
.ai/repo_navigation.md edits
.ai/rules/* edits
source code edits
scripts edits
ideas/ edits
.ai/v3/ edits
Boss / B1 / Junior Orchestrator route
hidden continuation of ork_planner
```

Stage 5 должен быть fresh tiny docs-only subproject from scratch.

## 13. Acceptance criteria

Stage 5 можно считать успешным только если:

* новый подпроект создан с нуля;
* он остался docs-only;
* route был `Planner -> Orc`;
* reduced set and waivers были явными;
* human gates не подменялись агентом;
* repo-level files не менялись;
* legacy route не вернулся;
* человек может открыть `readme -> status -> navigation` и понять состояние;
* journal показывает фактическую историю без выдуманного backfill;
* после context loss новый chat сможет продолжить работу по документам.

## 14. Конец bridge

После первого Stage 5 pilot этот bridge нужно считать временным историческим документом.

Он не должен автоматически становиться:

```text
repo-level standard
template
global policy
Stage 6 input without review
```

Если Stage 5 успешен, repo-level alignment делается только в Stage 6 и только после отдельного human approval.
```

## Candidate Navigation Entry

V1-20260602-061552: Grounded second opinion по Stage 5 bridge. Рекомендован один временный документ `.ai/subprojects/ork_planner/ork_planner_stage5_first_pilot_bridge.md`, который не является repo-level standard и нужен только для первого tiny docs-only pilot. Минимальный pilot set: `plan_full`, `battle_plan`, `readme`, `status`, `navigation`, `journal`; `plan_index` и `decisions` допустимо waive-нуть при явном условии.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/subprojects/ork_planner/ork_planner_plan_full.md
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/subprojects/ork_planner/ork_planner_battle_plan.md
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/subprojects/templates/subproject_templates_guide.md
