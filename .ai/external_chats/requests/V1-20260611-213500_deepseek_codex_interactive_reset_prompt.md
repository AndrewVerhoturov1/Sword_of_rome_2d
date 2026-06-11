V1-20260611-213500

Нужен grounded second opinion по странному поведению интерактивного `codex` через DeepSeek shim: почему почти каждый новый ход выглядит как новая сессия, почему identity модели плавает, и почему модель заявляет про файловые действия, которые не подтверждаются локальной проверкой.

Required Central Rules:
Прочитай этот файл. Это правила твоего поведения для этого вопроса. Это central core документ из ai-workflow-core. Требуй честный Context Readback: `fully read` только для реально открытых файлов.
https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/external_chat_rules.md

Required Central Navigation:
Это справочник файлов central core. Можешь переходить по релевантным navigation targets из него. Каждую реально открытую navigation-ссылку добавь в Context Readback. Navigation не даёт права делать claims о consumer repo без project-specific links/excerpts.
https://raw.githubusercontent.com/AndrewVerhoturov1/ai-workflow-core/main/repo_navigation.md

Additional Project-Specific Links:
- Repo rules: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/AGENTS.md
- Project navigation: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/repo_navigation.md
- Evidence file for this case: https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/requests/V1-20260611-213500_deepseek_codex_interactive_reset_evidence.md

Required Project V1 Navigation:
Сначала прочитай этот индекс прошлых `/v1`. Если оттуда видны релевантные entry по Codex workflow, identity drift, transport mismatch, external chat behavior или session discipline, можешь открыть их как дополнительные project-specific sources и добавь каждую реально открытую ссылку в Context Readback.
https://raw.githubusercontent.com/AndrewVerhoturov1/Sword_of_rome_2d/main/.ai/external_chats/V1_navigation.md

Context Excerpts:
- Локальный оператор уже подтвердил, что узкие смоки проходят:
  - direct PowerShell POST на `/v1/responses` возвращал `works`;
  - `codex exec "Reply with exactly one word: works"` возвращал `works`;
  - read-only `codex exec` тоже проходил.
- Проблема проявляется именно в интерактивном `codex`, не в `codex exec`.
- Основной transcript и противоречия см. в evidence file.
- Из transcript уже видно:
  - banner показывает `model: deepseek-v4-flash`;
  - early warning говорит `Model metadata for deepseek-v4-flash not found. Defaulting to fallback metadata`;
  - дальше модель по очереди называет себя `DeepSeek`, `DeepSeek-V3 (0324)`, `Codex`, `GPT-4o`;
  - модель несколько раз заявляет, что создала `test.md`, но локальный `ls` показывает, что файла нет;
  - в конце модель выдаёт DSML-like pseudo-tool markup вместо подтверждённого результата инструмента.

Task For External Chat:
Прочитай central docs, потом project-specific links, потом evidence file. Нужен не общий рассказ, а жёсткий root-cause analysis по узкому вопросу: что вероятнее всего ломает continuity интерактивной сессии `codex` в таком shimmed setup, если одноразовый `codex exec` уже проходит. Раздели анализ минимум на 4 корзины: `transport/session-state mismatch`, `missing agent/tool protocol invariants`, `model confabulation under weak metadata`, `user-visible but non-proven hypotheses`. Отдельно объясни, что именно transcript уже доказывает, а что пока только гипотеза. Особенно важно: 1) какие Responses/SSE invariants могли быть достаточны для one-shot, но недостаточны для multi-turn interactive session; 2) почему identity drift и "Привет! Я ..." на каждом ходе похожи на reset smell; 3) почему ложные claims про file creation и tool use могут появляться, если реальный tool path не завершён или не подтверждён; 4) какой минимальный следующий diagnostic pack стоит собрать локально, чтобы не гадать. Не предлагай broad rewrite. Нужен conservative next-step list с приоритетами.

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
[что central docs реально подтверждают про внешний чат, scope, limits, navigation, допустимые claims]

### Confirmed from provided excerpts
[ranked root-cause analysis именно этого случая; отдельно укажи, что transcript уже доказывает, что только strongly suggests, что пока не доказано]

### Not available / not verified
[границы уверенности, каких фактов о shim-коде и transport-полях всё ещё не хватает]

## Candidate Navigation Entry
[2-4 строки, один абзац: суть вердикта и минимальный следующий diagnostic plan]
