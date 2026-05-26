# V2 Request: <краткое название>

Этот файл — template-layer. Placeholder-поля, примерные URL и `<...>` значения здесь нормальны. Реальные ссылки и commit hash должны появляться уже в instantiated request-файле, например `.ai/external_reviews/requests/V2-YYYYMMDD-HHMMSS_request.md`.

## V2 ID

`V2-YYYYMMDD-HHMMSS`

## Статус

`draft`

## Дата

YYYY-MM-DD

## Цель

Что нужно получить от внешнего senior review. Опиши конкретную проблему или вопрос, который требует внешнего взгляда на реальный код.

## Контекст

### Почему нужен внешний review

Кратко: почему эта проблема не решается обычным `/v1` или внутренним debug.

### Что уже пробовали

Перечисли, что уже было сделано, какие гипотезы проверены, какие результаты получены.

### Связанные issues / bug journal entries

- BUG-YYYYMMDD-NNN или `none`
- Другие связанные V2 requests: `none` или список ID

## Base и Snapshot

### Base commit

```
<base commit hash>
```

Base branch: `main` или другая

### Snapshot commit

```
<snapshot commit hash>
```

Review branch: `review/v2/YYYYMMDD-HHMMSS-short-topic`

### Compare link

```
https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/compare/<base>...<snapshot>
```

## Ключевые ссылки для review

| Файл | Base raw URL | Snapshot raw URL | Почему важен |
|------|--------------|------------------|--------------|
| `path/to/file1.ts` | `https://raw.githubusercontent.com/.../<base>/path/to/file1.ts` | `https://raw.githubusercontent.com/.../<snapshot>/path/to/file1.ts` | ... |
| `path/to/file2.ts` | `https://raw.githubusercontent.com/.../<base>/path/to/file2.ts` | `https://raw.githubusercontent.com/.../<snapshot>/path/to/file2.ts` | ... |

## Изменённые файлы

| Файл | Статус (M/A/D) | Краткое описание изменений |
|------|---------------|--------------------------|
| `path/to/file1.ts` | M | ... |
| `path/to/file2.ts` | A | ... |

## Файлы, исключённые из snapshot

| Файл | Причина исключения |
|------|-------------------|
| `_local/...` | local-only |
| `output/...` | generated |

## Вопросы к внешнему senior reviewer

1. Конкретный вопрос 1.
2. Конкретный вопрос 2.
3. ...

## Ожидаемый результат

Что мы хотим услышать: bounded technical advice, root cause hypothesis, recommended correction path, risks, suggested implementation notes.

## Границы

### Что внешний чат НЕ должен делать

- Не писать patch без локального repo access.
- Не утверждать, что видел runtime, tests, shell или git status.
- Не предлагать решения, требующие repo authority без оговорок.

### Что вне scope этого V2 request

- ...

## Связанные документы

- [`v2_safety_checklist.md`](../templates/v2_safety_checklist.md) — safety checklist для этого request
- [`v2_prompt_template.md`](../templates/v2_prompt_template.md) — шаблон V2 prompt
- [`v2_ingest_summary_template.md`](../templates/v2_ingest_summary_template.md) — шаблон ingest summary

## Поля политик

### Связано с bug journal?

`none` / `BUG-YYYYMMDD-NNN`

### Нужен human visual check после реализации?

`yes` / `no` / `maybe`

Если yes — опиши, что именно нужно будет проверить человеку.

### Human review для самого V2 request

`required` / `suggested` / `not needed`

## История статусов

| Дата | Статус | Комментарий |
|------|--------|------------|
| YYYY-MM-DD | `draft` | V2 request создан |
