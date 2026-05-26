# V2 Prompt Template

Это шаблон prompt-а для внешнего чата в маршруте V2. В отличие от [`/v1`](../../prompts/create_external_question_prompt.md), V2 prompt передаёт внешнему чату commit-pinned ссылки на реальный WIP код и контекст сравнения base vs snapshot.

## Структура V2 Prompt

```text
V2 ID: V2-YYYYMMDD-HHMMSS

Ты участвуешь в V2 External Senior Review. Это НЕ prompt-only вопрос. Тебе дан зафиксированный snapshot реального кода для bounded technical review.

## Required Central Rules

Прочитай этот файл. Это правила твоего поведения для V2.
{{Central Rules Link}}

## V2 Override Note

Central `/v1`-style правила здесь нужны для честного `Context Readback`, source boundaries, запрета на выдуманный local access и явного разделения verified / not verified.
Структура ответа для этого review задаётся именно V2-шаблоном ниже, даже если названия секций отличаются от `/v1`.

## V2 Request Report

Прочитай V2 request report первым. Он описывает цель review, контекст, уже испробованное и конкретные вопросы.
{{V2 Request Report Link}}

## Additional Project Context, if provided

- {{Project AGENTS Link}}
- {{Project Repo Navigation Link}}
- {{Bug Journal Link}}
- {{Previous V1 or V2 Review Link}}

## Base and Snapshot

### Base commit
- Commit: `<base commit hash>`
- Branch: `main`
- Base files: {{Base Files Links}}

### Snapshot commit (review target)
- Commit: `<snapshot commit hash>`
- Branch: `review/v2/YYYYMMDD-HHMMSS-short-topic`
- Snapshot files: {{Snapshot Files Links}}

### Compare
{{Compare Link}}

## Важные правила для этого review

1. Сначала прочитай V2 request report.
2. Открой WIP files на snapshot commit.
3. Сравни их с base files на base commit.
4. Явно сохраняй distinction между base и snapshot.
5. Используй commit-pinned ссылки как основной источник. Branch links — только дополнительный контекст.
6. Перечисли всё, что прочитал, в Context Readback.
7. Отделяй verified facts от hypotheses.
8. Не утверждай, что видел local runtime, tests, shell или git status.
9. Не пиши patch так, как будто у тебя есть локальный repo access.
10. Давай bounded senior technical advice.
11. Явно говори, чего не хватило и где граница уверенности.

## Требуемый формат ответа

Ответ верни строго в следующей структуре:

## V2 ID
[идентификатор V2 request]

## Context Readback
- [название документа/ссылки]: [fully read / partially read / not read]
...

## Provider/Model
[провайдер / модель или not available]

## Answer

### Confirmed from central docs
[выводы, подтверждённые central core документами]

### Confirmed from project docs
[выводы, подтверждённые project-specific документами]

### Confirmed from WIP snapshot
[выводы, подтверждённые прочитанным snapshot кодом]

### Confirmed from base comparison
[выводы из сравнения base и snapshot]

### Not available / not verified
[что осталось неясным, граница уверенности]

### Main assessment
[главная оценка ситуации]

### Root cause hypothesis
[гипотеза о корневой причине, если применимо]

### Recommended correction path
[рекомендуемый путь исправления]

### Risks
[риски предлагаемого подхода]

### Suggested implementation notes
[заметки по реализации, если применимо]

### Questions back to Kilo/user, if any
[вопросы обратно, если есть]

## Candidate Navigation Entry
[2–4 строки — краткая выжимка для V2_navigation.md]
```

## Правила заполнения

| Поле | Что вставлять |
|------|--------------|
| `{{Central Rules Link}}` | Raw URL на `external_chat_rules.md` из central core. Краткое указание: «Прочитай этот файл. Это правила твоего поведения для V2.» |
| `{{V2 Request Report Link}}` | Raw URL на заполненный `v2_request_template.md` — опубликованный в review branch. |
| `{{Project AGENTS Link}}` | Raw URL на `AGENTS.md`, если он нужен для repo-level contract. |
| `{{Project Repo Navigation Link}}` | Raw URL на `.ai/repo_navigation.md`, если нужен project context. |
| `{{Bug Journal Link}}` | Raw URL на `.ai/logs/bug_journal.md`, если review завязан на повторяемый баг. |
| `{{Previous V1 or V2 Review Link}}` | Ссылка на релевантный прошлый внешний review, если он реально нужен. |
| `{{Base Files Links}}` | Commit-pinned raw URL на ключевые файлы в base commit. |
| `{{Snapshot Files Links}}` | Commit-pinned raw URL на те же файлы в snapshot commit. |
| `{{Compare Link}}` | GitHub compare URL: `https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/compare/<base>...<snapshot>` |

## Примечания

- Prompt пишется на русском или английском в зависимости от задачи.
- Commit-pinned ссылки — основной формат. Branch links допустимы только как дополнительный контекст.
- Prompt не требует Recorder Payload (это не `/r1`). V2 ingest полностью ручной: raw external answer передаётся в ordinary Kilo run вручную.
- `kilo-recorder` в первой версии V2 не используется.
- Все ссылки должны быть raw URL (предпочтительно) или blob URL.
