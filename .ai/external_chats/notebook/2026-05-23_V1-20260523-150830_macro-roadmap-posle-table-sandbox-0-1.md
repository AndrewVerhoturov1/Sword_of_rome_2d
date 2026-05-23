# Notebook Entry

- External Question ID: `V1-20260523-150830`
- Entry status: `staged`
- Provider/Model: `OpenAI / GPT-5.5 Thinking`
- Notebook entry path: `.ai/external_chats/notebook/2026-05-23_V1-20260523-150830_macro-roadmap-posle-table-sandbox-0-1.md`

## Context Links

- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-142942_planning-only-otvet-po-developer-side-authoring-workflow.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-141825_planning-only-otvet-po-trem-ostavshimsya-voprosam-dlya.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-131910_planning-only-otvet-po-stack-model-dlya-table.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md`
- `https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md`

## Candidate Navigation Entry

Topic: Macro-roadmap после `Table Sandbox 0.1`
Summary: Рекомендация: развивать проект через platform-first milestones — `0.2` hardening/validation/save compatibility, `0.3` authoring workspace expansion, `0.4` assisted runtime/rules hooks, `0.5` generic cards/documents, `1.0` modular platform alpha; Sword of Rome-like module должен оставаться reference/test module, а не формировать lower layers как hardcoded одну игру.

## Raw Response

## External Question ID

V1-20260523-150830

## Context Readback

* Uploaded prompt / `Вставленный текст(13).txt` — fully read. 
* `external_chat_rules.md` — fully read. ([GitHub][1])
* `repo_navigation.md` — fully read. ([GitHub][2])
* Project `architecture.md` — fully read. ([GitHub][3])
* Project `decisions.md` — fully read. ([GitHub][4])
* `first_milestone_runtime_skeleton.md` — fully read. ([GitHub][5])
* `table_sandbox_0_1_milestone_plan.md` — fully read. ([GitHub][6])
* `first_vertical_slice_spec.md` — fully read. ([GitHub][7])
* `minimal_canonical_file_schemas.md` — fully read. ([GitHub][8])
* `domain_schemas_contract.md` — fully read. ([GitHub][9])
* `action_event_contract.md` — fully read. ([GitHub][10])
* `rules_hooks_interface.md` — fully read. ([GitHub][11])
* `module_authoring_workflow.md` — fully read. ([GitHub][12])
* Project `V1_navigation.md` — fully read. ([GitHub][13])
* V1-navigation-discovered `V1-20260523-142942` notebook entry — partially read. ([GitHub][14])
* V1-navigation-discovered `V1-20260523-141825` notebook entry — partially read. ([GitHub][15])
* V1-navigation-discovered `V1-20260523-131910` notebook entry — partially read. ([GitHub][16])
* V1-navigation-discovered `V1-20260523-130238` notebook entry — partially read. ([GitHub][17])
* V1-navigation-discovered `V1-20260523-124734` notebook entry — partially read. ([GitHub][18])
* Navigation-discovered links from central `repo_navigation.md`: no additional central links opened beyond required `external_chat_rules.md`.

## Provider/Model

OpenAI / GPT-5.5 Thinking

## Answer

### Confirmed from central docs

Central `/v1` rules require honest `Context Readback`, separation between central-doc conclusions, project-specific conclusions, and not-verified material. They also forbid claiming local repo/runtime/test access unless that access was explicitly provided. ([GitHub][1])

Central `repo_navigation.md` confirms that central navigation covers `ai-workflow-core` only and does not authorize claims about a consumer repo unless consumer-project files are explicitly provided. ([GitHub][2])

For this question, central docs define answer discipline only. They do not define the roadmap for this project.

### Confirmed from provided excerpts

The accepted base is clear: the project is a reusable browser-based authoring/runtime platform for 2D counter-based wargames, not a hardcoded Sword of Rome implementation. The architecture already fixes four layers: core/data model, universal authoring, universal runtime/play sandbox, and module package with content plus rules/hooks. ([GitHub][3])

`Table Sandbox 0.1` is already scoped as the first minimal universal sandbox: canonical files load/save, runtime owns `GameState`, actions become events through a visible pipeline, permissive rules stay module-agnostic, and one tiny end-to-end slice proves the architecture. ([GitHub][5])

The roadmap after `0.1` should therefore grow **platform capabilities**, not "complete the Sword of Rome game" first.

---

## Рекомендуемый macro-roadmap после `Table Sandbox 0.1`

### Milestone 0.2 — Platform Hardening / надёжный фундамент

**Что должен доказать:**
Что `0.1` — не одноразовая демонстрация, а стабильный фундамент: файлы загружаются, проверяются, сохраняются, `GameState` собирается из сценария, события пишутся в журнал, сохранения не ломают definitions.

**Новые platform capabilities:**

* более строгая проверка пакета модуля перед запуском;
* понятные ошибки ссылок между файлами;
* базовая политика совместимости сохранений;
* стабильный импорт/экспорт canonical files;
* authoring undo/redo только для редакторских действий;
* play sandbox restart/load/save без сложного runtime undo;
* отдельные проверки: `map.json`, `scenario.json`, `savegame.json`, `rules.metadata.json`.

**Зависимости:**
Зависит от успешного `0.1`: уже должен существовать первый вертикальный срез `move_piece_requested -> piece_moved -> GameState -> log -> render`.

**Главный риск scope creep:**
Начать добавлять правила конкретной игры вместо укрепления загрузки, сохранения, проверки и границ файлов.

**Architectural drift risk:**
Если ради удобства начать копировать definitions в `savegame.json`, писать runtime state в `map.json`, или делать runtime изменения без событий, будет разрушен canonical split. Этот split уже принят как обязательный: definitions, runtime state и module rules должны оставаться раздельными. ([GitHub][9])

---

### Milestone 0.3 — Authoring Workspace расширяется до настоящего конструктора модуля

**Что должен доказать:**
Что дизайнер может не только двигать фишку в песочнице, но и собрать маленький валидный модуль через рабочую область: карта, точки, связи, зоны, фишки, стороны, сценарий, metadata правил.

**Новые platform capabilities:**

* полноценнее `Module Authoring Workspace`;
* отдельные editor surfaces:

  * карта;
  * фишки и стороны;
  * сценарий;
  * настройки модуля;
  * metadata правил;
* вынос `PieceDefinition[]` и `FactionDefinition[]` из `module.json` в `pieces.json` / `factions.json`, когда compact layout станет тесным;
* "проверить модуль" перед запуском;
* безопасный workflow "создать новый сценарий из текущего состояния" как optional tool, но не как silent overwrite;
* улучшенный authoring undo/redo.

**Зависимости:**
Нужен стабильный file contract из `0.1` и hardening из `0.2`. Без этого editor surfaces начнут писать хаотичные структуры.

**Главный риск scope creep:**
Сделать один гигантский супередитор, где карта, сценарий и текущая партия визуально похожи и начинают смешиваться.

**Architectural drift risk:**
Размыть границу между authoring mode и play sandbox mode. В принятом workflow authoring создаёт module package, а play sandbox запускает его как `GameState` через Action/Event pipeline. ([GitHub][12])

---

### Milestone 0.4 — Assisted Runtime / первые полезные правила без strict enforcement

**Что должен доказать:**
Что runtime умеет не только вручную двигать фишки, но и получать подсказки/ограничения от module rules через `RulesHooksInterface`, при этом universal runtime всё ещё не знает конкретных правил Sword of Rome-like модуля.

**Новые platform capabilities:**

* `resolveAction` становится устойчивой частью runtime flow;
* `validateAction` умеет возвращать warning/block;
* `getAllowedActions` помогает UI показывать доступные действия;
* простая phase scaffold;
* phase metadata в `rules.metadata.json`;
* первые assisted checks:

  * движение только между связанными точками, если модуль так решил;
  * предупреждение о неверной фазе;
  * warning-only stacking checks;
* event log остаётся главным источником истории.

**Зависимости:**
Нужны стабильные Action/Event contracts, потому что rules hooks должны возвращать structured output, а runtime должен применять события сам. В текущем контракте уже зафиксировано: action — запрос, event — подтверждённый факт, runtime commits and mutates `GameState`. ([GitHub][10])

**Главный риск scope creep:**
Попытаться сразу сделать полные правила Sword of Rome-like игры: combat, scoring, cards, full phases, victory conditions.

**Architectural drift risk:**
Дать module rules напрямую менять `GameState` или Phaser objects. Это запрещено принятым boundary: runtime asks, module rules answer, runtime applies and logs. ([GitHub][11])

---

### Milestone 0.5 — Generic Cards / Documents / Player Aids как platform capabilities

**Что должен доказать:**
Что платформа может поддерживать card-driven и document-heavy модули универсально, а не только через частные поля Sword of Rome-like модуля.

**Новые platform capabilities:**

* generic card definitions;
* generic deck definitions;
* piles / hands / discard as runtime state;
* documents/player aids registry;
* pinned reference windows;
* простые card actions:

  * draw;
  * discard;
  * reveal;
  * play as manual event;
* связь cards/documents с module package, а не с hardcoded game code.

**Зависимости:**
Нужны стабильные module package files, rules metadata, Action/Event pipeline, save compatibility и runtime state model.

**Главный риск scope creep:**
Сразу реализовать конкретные card effects Sword of Rome-like модуля вместо generic card/deck framework.

**Architectural drift risk:**
Спрятать card effects в JSON metadata как псевдо-язык правил или захардкодить конкретные названия карт в universal runtime. В принятых документах executable rules не должны жить в JSON metadata; rules behavior должен быть за `RulesHooksInterface`. ([GitHub][4])

---

### Milestone 1.0 — Modular Platform Alpha / несколько модулей, packaging, compatibility

**Что должен доказать:**
Что это уже не прототип одной карты, а ранняя модульная платформа: можно создать, проверить, сохранить и запустить больше одного модуля, а Sword of Rome-like модуль остаётся test module, не центром кода.

**Новые platform capabilities:**

* module package import/export;
* module validation report;
* version/reference compatibility policy;
* отдельные файлы для pieces, factions, cards, documents, assets;
* минимум два test modules:

  * tiny generic test module;
  * Sword of Rome-like reference module;
* rules hooks for module-specific behavior;
* basic playtest session manager;
* stable save/load boundaries;
* documented non-goals and extension points.

**Зависимости:**
Нужны `0.2` hardening, `0.3` authoring workflow, `0.4` assisted runtime, `0.5` cards/documents if card-driven modules are required for alpha.

**Главный риск scope creep:**
Назвать `1.0` "готовой игрой" и начать доделывать исторические детали, полные правила и content completeness вместо platform alpha.

**Architectural drift risk:**
Если acceptance criteria будут строиться только вокруг Sword of Rome-like модуля, lower layers начнут получать поля и логику конкретной игры.

---

## Граница: universal platform growth / module-specific growth / Sword of Rome-like growth

**Universal platform growth** — это то, что нужно любому 2D counter-based модулю:

```text
загрузка файлов
валидация
редактор карты
редактор фишек
редактор сценариев
Action/Event pipeline
GameState
save/load
generic cards/decks
documents
RulesHooksInterface
module package import/export
```

**Module-specific growth** — это то, что относится к конкретному модулю, но живёт за boundary:

```text
конкретные фазы
конкретные ограничения движения
конкретные victory checks
конкретные card effects
конкретные scoring rules
```

**Sword of Rome-like test module growth** — это только проверочный контент и проверочная реализация правил:

```text
конкретная карта
конкретные фракции
конкретные фишки
конкретные сценарии
конкретные карточки
конкретные hooks
```

Ключевое правило: **если фича нужна только Sword of Rome-like модулю, она не должна попадать в Layer 1–3 без доказательства, что это универсальная capability.**

---

## Как не дать test module превратить платформу в hardcoded игру

Лучшие практические предохранители:

1. **Всегда держать tiny generic module рядом с Sword of Rome-like module.**
   Любая новая platform capability должна работать хотя бы на двух модулях: нейтральном тестовом и Sword-like reference.

2. **Запретить поля в universal schema с названиями конкретной игры.**
   Нельзя добавлять в универсальный `GameState` поля уровня `romeControl`, `carthageSpecialRule`, `gallicTribeStatus`.

3. **Все специальные правила — только через rules hooks.**
   Runtime может спросить: "это действие разрешено?" Но не должен знать, почему именно у конкретной игры оно разрешено или запрещено.

4. **Content отдельно, behavior отдельно.**
   Карта, фишки, карты, сценарии — это module content. Ограничения, scoring, victory checks — module rules. Это разделение уже принято в архитектуре. ([GitHub][3])

5. **Каждый milestone должен иметь platform acceptance criteria.**
   Например: "редактор сценариев умеет расставлять фишки по locationId", а не "расставляет римские легионы по правилам такой-то игры".

---

## Что deliberately deferred даже после `0.1`

Даже после `0.1` не надо сразу тащить всё, что выглядит полезным.

Сознательно отложить:

* полный strict rules enforcement;
* full Sword of Rome rules;
* combat resolver;
* полноценный scoring/victory engine;
* hidden information;
* response/interrupt windows;
* online multiplayer;
* server-authoritative runtime;
* AI;
* full migration engine;
* advanced stack model как first-class `Stack`;
* polished publishing platform;
* marketplace/library modules;
* collaborative authoring;
* full replay UI;
* полноценный rules scripting language.

Причина: эти вещи полезны, но они не должны появиться раньше стабильных platform foundations.

---

## Fork in the road

### Safe branch

```text
0.1 sandbox loop
→ 0.2 hardening/validation/save compatibility
→ 0.3 authoring workspace breadth
→ 0.4 assisted runtime/rules hooks
→ 0.5 generic cards/documents
→ 1.0 modular platform alpha
```

Плюс: платформа растёт слоями, каждый milestone укрепляет foundation.

### Risky branch

```text
0.1 move-piece slice
→ сразу Sword of Rome full rules
→ сразу cards/combat/scoring
→ сразу конкретные сценарии и исторические детали
→ потом попытка обобщить
```

Минус: почти наверняка lower layers станут "цифровой Sword of Rome", а не универсальной authoring/runtime platform.

---

## Рекомендуемый следующий planning artifact

Следующий planning artifact после этого ответа:

```text
post_0_1_platform_roadmap.md
```

Минимальная структура:

```text
1. Roadmap assumptions after Table Sandbox 0.1
2. Milestone 0.2 — Platform Hardening
3. Milestone 0.3 — Authoring Workspace Expansion
4. Milestone 0.4 — Assisted Runtime / Rules Hooks
5. Milestone 0.5 — Generic Cards and Documents
6. Milestone 1.0 — Modular Platform Alpha
7. Universal vs module-specific boundary
8. Test module anti-hardcoding rules
9. Deferred features
10. Open questions / fork risks
```

### Not available / not verified

* Локальный репозиторий, product-code skeleton, runtime, tests, build и реальные JSON-файлы не проверялись.
* Не проверено, что `Table Sandbox 0.1` уже реализован; вопрос рассматривает его как зафиксированную planning-базу.
* Exact release numbering не принят как local decision.
* Exact acceptance criteria для каждого milestone ещё нужно зафиксировать отдельно.
* Exact migration/versioning policy остаётся частично open.
* Exact hidden info, response windows, server-authoritative model и AI scope не зафиксированы.
* Этот ответ — planning-only roadmap proposal, не accepted local implementation decision.

## Candidate Navigation Entry

V1-20260523-150830: Macro-roadmap после `Table Sandbox 0.1`. Рекомендация: развивать проект через platform-first milestones — `0.2` hardening/validation/save compatibility, `0.3` authoring workspace expansion, `0.4` assisted runtime/rules hooks, `0.5` generic cards/documents, `1.0` modular platform alpha; Sword of Rome-like module должен оставаться reference/test module, а не формировать lower layers как hardcoded одну игру.

[1]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/architecture.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/decisions.md "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_milestone_runtime_skeleton.md "raw.githubusercontent.com"
[6]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/table_sandbox_0_1_milestone_plan.md "raw.githubusercontent.com"
[7]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/first_vertical_slice_spec.md "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/minimal_canonical_file_schemas.md "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/domain_schemas_contract.md "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/action_event_contract.md "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/rules_hooks_interface.md "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/plans/master/module_authoring_workflow.md "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-142942_planning-only-otvet-po-developer-side-authoring-workflow.md "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-141825_planning-only-otvet-po-trem-ostavshimsya-voprosam-dlya.md "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-131910_planning-only-otvet-po-stack-model-dlya-table.md "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-130238_planning-only-otvet-po-minimalnym-canonical-file-schemas.md "raw.githubusercontent.com"
[18]: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/notebook/2026-05-23_V1-20260523-124734_planning-only-sequencing-answer-for-table-sandbox-0.md "raw.githubusercontent.com"
