# V2 Navigation

Индекс V2 External Senior Review requests для проекта `sword-of-rome-web`.

V2_navigation.md — **операционный lifecycle index**. Он обновляется обязательно на каждом из четырёх ключевых этапов V2-цикла. Это не декларативный справочник, а живой журнал состояния.

## Обязательные точки обновления

| Этап | Когда | Что обновить |
|------|-------|-------------|
| **Prompt creation** | После создания instantiated V2 prompt | Создать или обновить запись: V2 ID, дата, статус `prompt_ready` (prompt создан, но ещё не выдан человеку), `Prompt Location`. После выдачи prompt человеку — обновить статус на `waiting_external_answer` |
| **Ingest** | После ingest внешнего ответа | Обновить статус (`ingested`), `Response Location`, `Ingest Location` |
| **Implementation** | После реализации изменений | Обновить статус (`implemented`), краткое описание результата |
| **Cleanup** | После cleanup (или решения отложить) | Обновить статус (`cleaned` / `cleanup_pending` / `kept_by_decision`), `Branch State`, `Cleanup Decision` |

## Формат записи

| V2 ID | Date | Status | Topic | Base Commit | Snapshot Commit | Compare | Request Location | Prompt Location | Response Location | Ingest Location | Branch State | Cleanup Decision | Summary |
|-------|------|--------|-------|-------------|-----------------|---------|------------------|-----------------|-------------------|-----------------|--------------|------------------|---------|

### Допустимые значения полей

**Status:** `draft`, `previewed`, `awaiting_human_push_approval`, `snapshot_pushed`, `prompt_ready`, `waiting_external_answer`, `raw_response_captured`, `ingested`, `implementation_planned`, `implemented`, `superseded`, `cleaned`, `cleanup_pending`, `kept_by_decision`

**Request Location:** путь к request-файлу. Может быть: `main`, `review/v2/...`, commit-pinned ссылка или local-only path.

**Prompt Location:** путь к instantiated prompt-файлу.

**Response Location:** путь к response-файлу ИЛИ `pasted directly into Kilo run; raw response not stored separately`.

**Ingest Location:** путь к ingest summary-файлу.

**Branch State:** `active`, `deleted`, `kept_by_decision`, `cleanup_pending`, `unknown`

**Cleanup Decision:** `cleaned` (default policy выполнена), `cleanup_pending` (отложено человеком), `kept_by_decision` (явно сохранено), `none` (если cleanup ещё не наступил)

## Статусы

Статусы соответствуют lifecycle из [`README.md`](README.md): `draft`, `previewed`, `awaiting_human_push_approval`, `snapshot_pushed`, `prompt_ready`, `waiting_external_answer`, `raw_response_captured`, `ingested`, `implementation_planned`, `implemented`, `superseded`, `cleaned`, `cleanup_pending`, `kept_by_decision`.

## Записи

| V2 ID | Date | Status | Topic | Base Commit | Snapshot Commit | Compare | Request Location | Prompt Location | Response Location | Ingest Location | Branch State | Cleanup Decision | Summary |
|-------|------|--------|-------|-------------|-----------------|---------|------------------|-----------------|-------------------|-----------------|--------------|------------------|---------|
| V2-20260526-140000 | 2026-05-26 | `cleaned` | Underlay Alignment — map-plane / large image geometry drift | `89fabf1` | `318094d` | [`89fabf1...318094d`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/compare/89fabf1...318094d) | `review/v2/20260526-140000-underlay-alignment` (deleted after Codex cleanup) | `.ai/external_reviews/prompts/V2-20260526-140000_prompt.md` (deleted after Codex cleanup) | pasted directly into Kilo run; raw response not stored separately | not persisted as a separate artifact during the first pilot | `deleted` | `cleaned` | Three editor fixes applied (clampMapLocal, center-radial scale, getTransformedUnderlayBounds). V2 cycle technically successful. Codex post-accept cleanup completed. |

### Примечания к записям

`Request Location` должен явно показывать, где лежит request: `main`, `review/v2/...`, commit-pinned ссылка или local-only path.

`Branch State` должен явно фиксировать итог cleanup: `active`, `deleted`, `kept_by_decision`, `cleanup_pending` или другой понятный статус.

`Prompt Location`, `Response Location` и `Ingest Location` обязательны для всех записей после соответствующих этапов. Если external answer был вставлен напрямую (direct paste), `Response Location` должен явно это указывать.
