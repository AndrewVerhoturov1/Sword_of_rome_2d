# Notebook Entry

- External Question ID: `V1-20260602-093009`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-06-02_V1-20260602-093009_v1-20260602-093009-grounded-critique-tekuschego-lokalnogo-plan.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/subprojects/ork_planner/ork_planner_stage5_first_pilot_bridge.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/v3/contracts/v3_request_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/v3/contracts/v3_artifact_package_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-28_V1-20260528-031912_updated-root-cause-analysis-after-user-clarified-that.md`

## Candidate Navigation Entry

Topic: `V1-20260602-093009`: Grounded critique текущего локального `plan_full` для Stage 5/V3 request-pack skill pilot
Summary: Verdict: план сильный, но слишком широкий для первого маленького pilot; его стоит ужать, добавить authorization boundary, конкретный boring proof task, full V3 request checklist и отложить automation до отдельного human gate. Узкий script уместен только как request-pack preflight, без package generation, import или repo writes.

## Raw Response

## External Question ID

V1-20260602-093009

## Context Readback

* `external_chat_rules.md` — fully read.
* `ai-workflow-core/repo_navigation.md` — fully read.
* Required pinned Project V1 navigation URL — opened, but returned `404 Not Found`; not read as pinned source.
* Required pinned Stage 5 bridge URL — opened, but returned `404 Not Found`; not read as pinned source.
* Required pinned V3 request contract URL — opened, but returned `404 Not Found`; not read as pinned source.
* Required pinned V3 artifact package contract URL — opened, but returned `404 Not Found`; not read as pinned source.
* Same/similar project files on `main` — opened as fallback, not treated as the requested pinned versions.
* Current live `plan_full` excerpt from prompt — fully read and treated as the most important local context.
* Relevant V1 navigation entries / notebook entries on `main` — opened where useful for Stage 5/V3 background.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central rules require honest readback: `fully read` is allowed only for actually opened files, and repo/workflow answers must separate central-doc claims, provided excerpts, and not-verified areas. That matters here because several required pinned project URLs returned `404`, so they cannot be treated as read. ([GitHub][1])

Central navigation is only an allowed navigation map for central core files; it does not give authority to claim facts about the consumer repo unless those project files are explicitly provided or opened. ([GitHub][2])

### Confirmed from available project docs / provided excerpt

The available Stage 5 bridge on `main` says the first Stage 5 pilot should stay a tiny docs-only pilot, should not become a repo-level standard, should not bypass human gates, and should not open Stage 6. ([GitHub][3])

The available V3 request contract says the key separation is: request ≠ package ≠ imported result ≠ accepted result. It also requires explicit fields such as `action`, `scope`, `current_stage`, `allowed_paths`, `forbidden_paths`, `expected_files`, `acceptance_criteria`, `known_risks`, `post_import_testing`, and `no_repo_access_statement`; it also requires GitHub-first context mode and explicit `post_import_testing.mode`. ([GitHub][4])

The available artifact package contract says a real V3 package is a ZIP with a root folder, `manifest.yaml`, `README_FOR_KILO.md`, `README_FOR_CODEX.md`, `checksums.sha256`, and `files/`; project files must live under `files/`, be listed in the manifest, and match checksums. ([GitHub][5])

A relevant prior V1 navigation entry says the earlier V3 root-cause correction was: do not treat Phase/Stage 5 as immediate Kilo import; first get a real package, review it, configure Kilo Notebook V3, choose transport, and only then explicitly enter import-pilot stage. ([GitHub][6])

## Verdict

План в целом **хороший и безопасный по направлению**, но для первого маленького Stage 5 pilot он **слишком широкий**. Его не надо переписывать с нуля. Его лучше ужать и сделать более "пилотным": меньше lifecycle-театра, больше конкретного первого доказательства.

Главный риск: план уже описывает почти весь путь до skill build, внешнего package и final verdict. Формально он ставит gates, но новый Orc/чат может всё равно прочитать это как разрешение двигаться дальше по цепочке. Нужно сильнее отделить: **сейчас принимается только план подпроекта**, а skill creation, внешний прогон и package review — отдельные будущие шаги после отдельных human gates.

## 1. Критика самого плана

### Что в плане уже правильно

План правильно не путает этот pilot с `/v1`, legacy flow и `Kilo Notebook V3 import`. Он держит V3-границу: внешний чат делает package, но не пишет repo и не принимает результат. Это совпадает с V3-contract логикой `request != package != import != accepted`. ([GitHub][4])

Хорошо, что proof не останавливается на красивом request pack. Для этого skill действительно важно доказать не "мы написали хороший prompt", а "по нему внешний чат реально вернул годный artifact package".

Хорошо, что есть package-only review перед import. Это прямо защищает от старой ошибки: package received ≠ import-stage started. Эта граница подтверждается и prior root-cause entry. ([GitHub][6])

### Что лишнее / тяжеловато

**Лишний объём lifecycle.** Для первого маленького pilot 13 шагов lifecycle выглядят как полноценная программа внедрения. Я бы оставил в `plan_full` только 5 крупных фаз:

1. `Planner plan accepted`
2. `Orc docs-only setup accepted`
3. `Separate human gate for global skill materialization`
4. `One workflow_docs V3 request-pack proof`
5. `Package-only review + final pilot verdict`

Детальные подпункты лучше перенести в battle plan, иначе `plan_full` становится почти operational script.

**Слишком много документов для tiny pilot.** В live plan оставлен `decisions.md`, и это можно оправдать, потому что есть долгоживущие решения: global skill home, proof bar, gates, stop rules. Но надо явно сказать: `decisions.md` создаётся только для этих решений, не для пересказа журнала. Иначе он снова превратится в "журнал под видом решений".

**Слишком рано указан глобальный skill path как почти решённый факт.** Путь `C:\Users\andre\.codex\skills\v3-request-pack-prep\` нормален как proposed target, но в плане надо написать жёстче:

> До capability-sensitive human gate это только proposed target, не installed skill и не permission to write global files.

Иначе появляется тихий drift из repo-local docs-only подпроекта в глобальную установку skill.

### Что missing

**Не хватает точного первого proof task.** Сейчас proof profile говорит "1–2 markdown-файла под `.ai/` или `docs/`", но это всё ещё абстрактно. Для маленького пилота надо зафиксировать один кандидат, например:

```text
Proof task candidate:
создать 1 короткий markdown-документ:
.ai/subprojects/v3_request_pack_skill_pilot/examples/example_v3_request_pack_checklist.md

Scope:
workflow_docs

Action:
create only

Post-import testing:
waived

Allowed paths:
.ai/subprojects/v3_request_pack_skill_pilot/examples/

Forbidden paths:
AGENTS.md
.ai/repo_navigation.md
.ai/rules/
.ai/v3/contracts/
scripts/
src/
package.json
```

Это сильно снизит риск scope drift.

**Не хватает full request checklist по контракту.** В плане перечислены многие поля, но лучше добавить прямой checklist всех обязательных полей из V3 request contract: `v3_id`, `task_title`, `generated_by`, `action`, `scope`, `current_stage`, `context_summary`, `task_description`, `allowed_paths`, `forbidden_paths`, `expected_files`, `package_format`, `acceptance_criteria`, `known_risks`, `post_import_testing`, `no_repo_access_statement`. ([GitHub][4])

**Не хватает проверки root folder package.** В package-only review у тебя перечислены `manifest.yaml`, `README...`, `checksums`, `files/`, но стоит добавить, что они должны быть внутри root folder вида `V3-YYYYMMDD-HHMMSS-short-topic/`, а не просто россыпью в ZIP. Это требование есть в available artifact package contract. ([GitHub][5])

**Не хватает "no promotion" формулировки для результата.** План говорит не предлагать repo-level promotion заранее, но в success criteria лучше добавить:

> Даже успешный pilot даёт только `candidate skill/process evidence`, а не разрешение на repo-level promotion, Stage 6 или расширение scope.

### Что стоит ужесточить

Я бы добавил один жёсткий блок:

```md
## Authorization boundary

Acceptance of this `plan_full` authorizes only:
- creation/revision of the local subproject planning docs;
- preparation of a later human decision point.

It does not authorize:
- materializing the global skill;
- running the external V3 proof;
- importing any package;
- updating repo-level workflow docs;
- opening Stage 6.
```

И второй блок:

```md
## First proof must be boring

The first proof task must be intentionally boring:
- one package;
- one external chat run;
- one create-only markdown target;
- no scripts;
- no schemas;
- no product code;
- no overwrite;
- no import.
```

Это защитит план от "давай сразу сделаем полезнее".

## 2. Automation / script

Да, узкий script здесь уместен, но **только один** и только как **preflight/checklist helper**, не как генератор, не как importer и не как validator всей V3-системы.

Лучший вариант для этого pilot:

```text
scripts/v3_request_pack_preflight.py
```

Но важная поправка: **не сейчас как обязательный результат первого docs-only шага**. Его можно разрешить только после отдельного human gate, потому что сам live plan пока говорит "без scripts" для первого proof. Если script добавить прямо сейчас, это будет scope drift.

Что script может делать безопасно:

```text
Input:
- path to draft V3 request markdown/yaml/json

Checks:
- required fields exist;
- current_stage is external_artifact_generation_only;
- action is create;
- scope is workflow_docs;
- package_format is zip;
- post_import_testing.mode is waived or optional, not missing;
- allowed_paths not empty;
- forbidden_paths not empty;
- expected_files not empty;
- no_repo_access_statement exists;
- all source links look like full raw GitHub URLs;
- raw GitHub URLs look commit-pinned, not main;
- forbidden_paths do not overlap badly with expected_files;
- expected_files are inside allowed_paths;
- expected_files are not inside forbidden_paths.

Output:
- human-readable preflight report;
- no file writes by default;
- no package generation;
- no import;
- no repo mutation.
```

Что script не должен делать:

```text
- не создавать V3 request pack сам;
- не собирать ZIP;
- не распаковывать ZIP;
- не писать в repo;
- не обновлять V3_navigation;
- не вызывать Kilo;
- не принимать human gate;
- не пытаться быть универсальным V3 validator.
```

Самое безопасное место для automation в текущем pilot — не "V3 package validator", а именно **request-pack lint/preflight**. Это ускоряет ручную сборку и ловит типичные ошибки, но не открывает import-stage и не заменяет человека.

## Recommended patch to plan_full

Я бы внёс 6 точечных правок:

1. Переименовать `Целевой home` в `Proposed skill home until human capability gate`.
2. Добавить `Authorization boundary`.
3. Ужать lifecycle до 5 фаз, а мелкие шаги оставить battle plan.
4. Добавить конкретный boring first proof task.
5. Добавить full required-fields checklist из V3 request contract.
6. Добавить automation policy: "script allowed only after separate human gate; first candidate is request-pack preflight, no apply/import/package generation".

## Final recommendation

Текущий `plan_full` можно принимать **после targeted simplification**, не нужен полный rewrite. Самая важная правка — сделать его менее похожим на план всего rollout и более похожим на первый контролируемый Stage 5 pilot.

Automation — да, но только позже и очень узко: **request-pack preflight script**, без записи файлов, без ZIP, без import, без Stage 6.

## Not available / not verified

Я не видел локальный filesystem, git status, actual local diff и реальный локальный файл `v3_request_pack_skill_pilot_plan_full.md`. Также pinned project URLs из prompt открылись как `404`, поэтому claims по pinned-версии контрактов/bridge я не делаю. Live excerpt из prompt принят как главный текущий источник для самого `plan_full`.

## Candidate Navigation Entry

`V1-20260602-093009`: Grounded critique текущего локального `plan_full` для Stage 5/V3 request-pack skill pilot. Verdict: план сильный, но слишком широкий для первого маленького pilot; его стоит ужать, добавить authorization boundary, конкретный boring proof task, full V3 request checklist и отложить automation до отдельного human gate. Узкий script уместен только как request-pack preflight, без package generation, import или repo writes.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/subprojects/ork_planner/ork_planner_stage5_first_pilot_bridge.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/v3/contracts/v3_request_contract.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/v3/contracts/v3_artifact_package_contract.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-28_V1-20260528-031912_updated-root-cause-analysis-after-user-clarified-that.md "raw.githubusercontent.com"
