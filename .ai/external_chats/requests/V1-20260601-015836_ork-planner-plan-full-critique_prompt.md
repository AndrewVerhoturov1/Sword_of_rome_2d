V1-20260601-015836

Нужен grounded critique уже импортированного `ork_planner_plan_full.md`. Не пиши новый план с нуля. Проверь, готов ли текущий файл быть planner-owned base перед первым Orc nav pass.

Required Central Rules:
Прочитай этот файл. Это правила твоего поведения для этого вопроса. Это central core документ из `ai-workflow-core`. Требуй честный Context Readback: `fully read` только для реально открытых файлов.
https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md

Required Central Navigation:
Это справочник файлов central core. Можешь переходить по релевантным navigation targets из него. Каждую реально открытую navigation-ссылку добавь в Context Readback. Navigation не даёт права делать claims о consumer repo без project-specific links/excerpts.
https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md

Additional Project-Specific Links:
- Repo rules: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/AGENTS.md
- Project navigation: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/repo_navigation.md
- Planner role contract: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/rules/codex_role_planner.md
- Orc role contract: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/rules/codex_role_orc.md
- Codex orchestrator contract: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/rules/codex_orchestrator.md
- Subagent tools: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/rules/subagent_tools.md
- Source idea doc: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/ideas/subproject_single_execution_chat_documentation_system_v2.md
- Planner decisions: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/subprojects/ork_planner/ork_planner_plan_decisions.md
- Planner request ideas: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/subprojects/ork_planner/ork_planner_planner_request_ideas.md
- Live `ork_planner_plan_full.md`: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/subprojects/ork_planner/ork_planner_plan_full.md
- V3 first-draft request that produced this file: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/v3/requests/V3-20260601-011520-ork-planner-plan-full-first-draft_request.md

Required Project V1 Navigation:
Сначала прочитай этот индекс прошлых `/v1`. Если оттуда видны релевантные entry по Planner/Orc, workflow docs, role drift, V3 route или pilot planning, можешь открыть их как дополнительные project-specific sources и добавь каждую реально открытую ссылку в Context Readback.
https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/367f32bd4f57090a18b1aa4d0bfeb304c9c3b03d/.ai/external_chats/V1_navigation.md

Context Excerpts:
- Текущее состояние:
  - первый V3 ZIP был локально проверен и вручную импортирован в живой repo path `.ai/subprojects/ork_planner/ork_planner_plan_full.md`;
  - файл сейчас в статусе `local-first-draft-under-review`;
  - Orc ещё не запускался;
  - next intended step после critique = решить, какие точечные правки внести до первого Orc nav pass.
- Уже внесённые локальные правки после импорта:
  - header переведён из `external-first-draft` в `local_planner_review`;
  - section `8.5` переписан в `local-first`, чтобы первый docs execution slice не прыгал сразу в repo-level files;
  - section `16.2` теперь явно включает `AGENTS.md` в будущую repo-level alignment wave;
  - section `11.2`/`11.3` больше не притворяются, что файл ещё не импортирован;
  - `UD-001` теперь про repeatable policy для будущих V3 ZIP, а не про текущий уже выполненный импорт.
- Что особенно важно проверить:
  - нет ли ещё contradictions между sections `8`, `12`, `16`, `18`, `20`, `21`;
  - не слишком ли узок или широк первый Orc nav pass;
  - достаточно ли жёстко отделены `plan_navigation` / `plan_index` / `readme` от более поздних `navigation` / `status` / `journal` / `decisions` / `plan_active_N`;
  - не осталось ли package-stage wording, которое в живом repo-файле уже ложно;
  - не пропущен ли какой-то critical gate перед первым Orc run.

Task For External Chat:
Прочитай central docs, потом project-specific docs. Нужен жёсткий critique именно живого `ork_planner_plan_full.md`, не нового плана с нуля. Сначала дай short verdict: `good enough with targeted edits` / `needs revision before Orc` / `not ready`. Потом найди реальные contradictions, weak points, missing gates, wrong sequencing, ownership blur, unresolved decisions placed wrong, already-resolved items that still look open, и package-stage wording drift. Отдельно проверь шесть зон: 1) Planner vs Orc boundary; 2) V3-first-draft route vs live repo state; 3) first Orc nav pass scope; 4) battle-plan gate; 5) local proof before repo-level alignment; 6) `session != journal`. Не предлагай legacy `Boss / B1 / Junior Orchestrator`. Не раздувай новый meta-process. Нужен conservative patch list: ranked findings by severity, потом 5-10 минимальных правок в этот файл, потом список unresolved decisions, которые правда надо закрыть до первого Orc nav pass, а какие можно оставить позже.

Required Response Format:
Верни ответ строго в следующей структуре:

## External Question ID
[идентификатор вопроса]

## Context Readback
- [название документа/ссылки]: [fully read / partially read / not read]
...
(Включи сюда все navigation-discovered links из repo_navigation.md, которые ты открыл)

## Provider/Model
[провайдер / модель или not available]

## Answer
### Confirmed from central docs
[что central docs реально подтверждают про Planner/Orc boundary, external routes, session rules, approval gates]

### Confirmed from provided excerpts
[дай verdict; потом ranked findings; потом minimal patch list; потом список unresolved decisions: must-close-before-first-Orc-nav-pass vs can-stay-later]

### Not available / not verified
[границы уверенности, что осталось неясным]

## Candidate Navigation Entry
[2-4 строки, один абзац: verdict и главные правки для imported `ork_planner_plan_full.md`]
