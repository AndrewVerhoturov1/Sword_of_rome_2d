# Журнал решений

## `2026-05-22` — `Authoring tool first`

### Контекст

Проект легко спутать с веб-адаптацией Sword of Rome, но фактическая цель шире: создать редактор и рабочий стол для 2D counter-based варгеймов.

### Решение

Считать Sword of Rome-like модуль первым тестовым модулем внутри универсального authoring tool, а не единственным продуктом.

### Причины

- Это даёт правильный architectural focus на reusable capabilities.
- Это лучше согласуется с уже существующим контекстом и прототипами.

### Последствия

- Канон, архитектура и roadmap должны описывать editor/runtime platform, а не "одну игру".
- Конкретные игровые материалы держим как test module/reference layer.

### Статус

`Принято`

## `2026-05-22` — `Public repo with visible V1 history and hidden Kilo runtime`

### Контекст

Половина дальнейшей работы планируется через внешние чаты. Им нужна удобная GitHub-навигация и видимая история прошлых `/v1` вопросов. При этом Kilo runtime-мусор не должен попадать в публичную плоскость.

### Решение

Публиковать `.ai/external_chats/V1_navigation.md` и `.ai/external_chats/notebook/`, но не публиковать `.ai/handoffs/`, `.ai/reports/`, `.ai/plans/sessions/` и runtime-папки external route.

### Причины

- Внешнему чату нужен накопленный контекст.
- Внутренний execution noise мешает навигации и засоряет repo.

### Последствия

- `.gitignore` обязан жёстко разделять public и local-only workflow-слои.
- Repo navigation должен явно вести внешнего чата в V1 history.

### Статус

`Принято`

## `2026-05-23` — `4-layer product architecture with rules hook boundary`

### Контекст

После двух `/v1` second opinion по architectural decomposition (`V1-20260523-052756` и `V1-20260523-052757`) стало ясно, что грубая `2-layer` модель полезна только как стартовая интуиция, но недостаточна для product planning.

Главная проблема 2-layer framing:

- внутри `editor layer` смешиваются infrastructure, data model и authoring tools;
- внутри `project-specific layer` смешиваются content и rules;
- отсутствует явный universal runtime/play layer как буфер между editor и конкретной игрой.

### Решение

Для product code принять `4-layer` архитектуру:

1. `Core Infrastructure + Project/Data Model`
2. `Universal Authoring / Editor Capabilities`
3. `Universal Runtime / Play Sandbox`
4. `Module Package`

Внутри `Module Package` явно разделять:

- `Module Content`
- `Module Rules/Hooks`

Между universal runtime и module-specific rules ввести явный boundary-контракт:

`RulesHooksInterface`

Также явно держать разделение:

- `map.json`
- `scenario.json`
- `savegame.json`

### Причины

- Это не даёт Sword of Rome-like модулю превратиться в hardcoded центр всей платформы.
- Это сохраняет Phaser в роли renderer, а не source of truth.
- Это создаёт чистый шов между universal runtime и module-specific behavior.
- Это снижает риск смешивания editor-логики и play-логики.
- Это лучше готовит платформу к later server-authoritative architecture.

### Последствия

- `.ai/architecture.md` должен описывать именно `4-layer` модель и module boundaries.
- Первый product-code skeleton должен следовать этим слоям, а не начинаться как "одна игра".
- `RulesHooksInterface` нужно отдельно зафиксировать до начала substantive product-code implementation.
- `Table Sandbox 0.1` должен планироваться как набор universal modules, а не как первый hardcoded Sword of Rome runtime.

### Статус

`Принято`

## `2026-05-23` — `Canonical domain/data split and file contract`

### Контекст

После двух `/v1` ответов по domain/data contract (`V1-20260523-055021` и `V1-20260523-055021-2`) стало ясно, что для дальнейшей реализации недостаточно только layer architecture. Нужен явный canonical split между definitions, runtime state и module-specific rules.

Без этого быстро смешаются:

- тип фишки и конкретная фишка в партии;
- карта и текущее состояние партии;
- JSON metadata и executable rule logic;
- request/intention и committed fact.

### Решение

Принять следующий canonical split:

1. `definitions`
2. `runtime state`
3. `module rules`

Принять следующий canonical file set:

- `project.json`
- `modules/<moduleId>/module.json`
- `modules/<moduleId>/map.json`
- `modules/<moduleId>/scenario.<scenarioId>.json`
- `modules/<moduleId>/rules.metadata.json`
- `saves/<saveId>.savegame.json`

Также принять как canonical distinctions:

- `PieceDefinition` != `PieceInstance`
- `MapDefinition` != `ScenarioState` != `SaveGameState`
- `Action` != `Event`

Executable rules не хранятся в JSON metadata. JSON хранит только metadata и ссылки; исполняемая rules logic живёт отдельно за boundary `RulesHooksInterface`.

### Причины

- Это удерживает платформу data-driven.
- Это не даёт Phaser стать source of truth.
- Это сохраняет чистый шов между universal runtime и module-specific behavior.
- Это делает возможными save/load, replay, migration и later server-authoritative flow.
- Это уменьшает риск захардкодить Sword of Rome-like module в universal schema.

### Последствия

- `architecture.md` должен содержать explicit domain/data contract, а не только слойную схему.
- Следующий уровень детализации должен идти в будущие schema docs и hook contract docs.
- Любой product-code skeleton должен следовать именно этому split.
- Спорные темы не считаются принятыми автоматически:
  - stack model
  - module dependencies
  - exact save compatibility policy

### Статус

`Принято`

## `2026-05-23` — `Platform-first macro-roadmap after Table Sandbox 0.1`

### Контекст

После серии `/v1` ответов база для `Table Sandbox 0.1` стала достаточно ясной:
layers, file contract, `Action/Event`, save policy, stack safe default,
authoring workflow. Следующий риск уже не в architecture gap, а в том, что
проект может слишком рано скатиться в "доделывание Sword of Rome-like игры", а
не в platform growth.

### Решение

Принять post-`0.1` roadmap как platform-first ladder:

1. `0.2` — hardening / validation / save compatibility.
2. `0.3` — authoring workspace expansion.
3. `0.4` — assisted runtime through `RulesHooksInterface`.
4. `0.5` — generic cards/documents capabilities.
5. `1.0` — modular platform alpha.

Sword of Rome-like module остаётся reference/test module. Он не должен
формировать Layer 1-3 как hardcoded одну игру.

### Причины

- Это сохраняет project framing как reusable authoring/runtime platform.
- Это не даёт test module захватить lower layers.
- Это определяет понятную очередь крупных milestones, а не утопание в
  game-specific details.

### Последствия

- Нужен отдельный master planning artifact после `0.1`.
- Каждый следующий milestone нужно описывать в терминах universal capabilities,
  а не в терминах одной игры.
- Generic test module и Sword of Rome-like reference module желательно держать
  как две отдельные acceptance lenses.

### Статус

`Принято`

## `2026-05-23` — `Module package evolves from compact 0.1 layout to mature multi-part package`

### Контекст

`Table Sandbox 0.1` уже достаточно ясно описал compact package shape:
manifest, map, scenario, rules metadata, save/runtime split, temporary inline
`pieces/factions` if needed. Следующий шаг не ломает этот базис, а делает
package модель зрелой: с ясными content zones, optional rich content и runtime
boundary.

### Решение

Принять направление, что:

- `module package` в будущем становится multi-part product bundle;
- `module.json` остаётся manifest, не content dump;
- `savegame.json` остаётся runtime artifact, не canonical module content;
- richer content files появляются по мере взросления модуля;
- `module_package_model.md` становится главным planning doc для этой цели.

### Причины

- Это сохраняет эволюцию от `0.1` без painful rewrite.
- Это даёт понятный путь для import/export, reuse и future publishing.
- Это не даёт Sword of Rome-like reference module навязать shape всей
  платформе.

### Последствия

- Нужно вести отдельный master plan for package model.
- Compact `0.1` layout остаётся допустимым только как стартовая simplification.
- Optional content zones не должны попадать в early package просто ради
  "будущей красоты".

### Статус

`Принято`

## `2026-05-23` — `Hybrid module authoring workspace with specialized surfaces`

### Контекст

После `/v1` ответа по developer-side authoring workflow стало ясно, что для
этого проекта удобнее не один супередитор и не полностью разрозненные редакторы,
а единый authoring shell с несколькими специализированными surface-ами внутри.

### Решение

Принять гибридную модель:

1. `Module Authoring Workspace` как общий рабочий центр модуля.
2. Внутри него отдельные surface-ы для map, pieces/factions, scenario, module
   settings / rules metadata.
3. Отдельный `Play Sandbox Preview` для runtime-проверки через
   `GameState` и `Action/Event` pipeline.

### Причины

- Это сохраняет единую package-логику для модуля.
- Это не смешивает definitions, scenario setup и runtime state.
- Это даёт дизайнеру понятный практический workflow.
- Это лучше подходит для `Table Sandbox 0.1`, где нужно быстро собрать и
  проверить маленький module package.

### Последствия

- `architecture.md` должен явно говорить о Module Authoring Workspace как о
  practical shape Layer 2.
- Нужно отдельное planning-описание authoring workflow.
- Play Sandbox Preview остаётся runtime-shell частью, а не editor for definitions.

### Статус

`Принято`
## `2026-05-23` — `Product UX stays mode-based and explicit`

### Контекст

После `/v1`-синтеза по product UX model стало ясно, что одной
authoring-схемы недостаточно. Продукт нужно читать как явные
режимы работы с понятными переходами, иначе быстро смешаются
definitions, scenario setup и runtime state.

### Решение

Принять mode-based UX rule:

- `authoring`, `playtest preview`, `runtime/save` flows остаются явными;
- они не должны тихо перекрывать друг друга одним и тем же
  user action;
- `save module` и `save runtime snapshot` должны оставаться разными
  workflow outcomes.

### Причины

- Это удерживает user mental model чистым.
- Это защищает canonical split `definitions / runtime state / module rules`.
- Это не даёт Play Sandbox превратиться в скрытый definitions editor.

### Последствия

- Нужен отдельный UX planning doc для product-wide workflow.
- Authoring docs, package docs и milestone docs должны говорить одним
  языком про mode transitions.
- Future UX growth нужно строить поверх этой explicit boundary, а не
  через смешанные actions.

### Статус

`Принято`
## `2026-05-23` вЂ” `External prototype is a reference donor, not foundation`

### Контекст

External prototype `table-map-editor-canvas-local-fixed` was reviewed as a
candidate input for the future Map Editor surface.

### Решение

Treat it as:

- reference prototype;
- selective donor of map-editor UX and interaction ideas;
- not direct product-code foundation;
- not source of canonical architecture.

### Причины

- it is useful for map-editing behavior;
- it preserves ideas that fit the authoring shell;
- it must not override canonical package/runtime boundaries;
- it must not become the base architecture for the whole product.

### Последствия

- Map Editor can borrow interaction patterns from it;
- other surfaces should not inherit its internal shape;
- product code still starts from canonical architecture and narrow slices;
- controlled extraction is the default integration method.

## `2026-05-24` — `Narrow-first execution start after short closure`

### Контекст

После readiness-аудита и детального execution-plan синтеза стало ясно, что
архитектурная база уже достаточна для старта кода, но только если старт будет
узким и жёстко зафиксированным. Broad implementation по-прежнему слишком легко
размоет границы между canonical data, runtime, authoring и prototype inputs.

### Решение

Начинать product code только через короткий pre-code closure и затем через
узкий `Table Sandbox 0.1` slice.

Обязательные элементы closure:

- first product-code brief;
- technical shell decision;
- tiny canonical fixture set;
- fixed `move_piece_requested -> piece_moved` pair;
- explicit acceptance checklist;
- frozen prototype role.

### Причины

- это останавливает бесконечное broad planning;
- это не даёт стартовать слишком широкой реализации;
- это держит первый код вокруг одного проверяемого runtime proof;
- это снижает риск того, что внешний prototype или test module станут скрытой
  архитектурной основой.

### Последствия

- broad product-code start остаётся запрещённым;
- первый implementation block должен идти через canonical fixtures и
  `Action -> Event -> GameState -> log -> render`;
- post-`0.1` roadmap считается следующим слоем только после первого
  executable proof;
- отдельный operational bridge-doc становится обязательной частью planning
  canon.

### Статус

`Принято`

### Статус

`Принято`
## `2026-05-24` — `First coding starts from first_product_code_block.md`

### Контекст

После уточняющего `/v1` про единственный ближайший шаг стало ясно, что short
closure должен быть зафиксирован не только как общая фаза, но и как один
конкретный implementation brief.

### Решение

Первый приоритетный шаг перед coding phase:

- создать и принять `first_product_code_block.md`.

Этот файл должен заморозить:

- technical shell;
- tiny fixture set;
- first action/event pair;
- runtime rule;
- acceptance checklist;
- prototype role;
- explicit non-goals.

### Причины

- это превращает общий bridge-plan в один конкретный handoff target;
- это снижает implementation drift в самом первом coding block;
- это не даёт silently расширить первый scope до editor migration, full rules
  или prototype-led architecture.

### Последствия

- первый coding block не должен стартовать без этого brief;
- immediate next step после принятия brief = technical bootstrap;
- first vertical slice должен исполняться через этот brief, а не напрямую из
  broad planning canon.

### Статус

`Принято`
