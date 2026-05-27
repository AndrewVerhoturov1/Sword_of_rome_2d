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
| V2-20260526-140000 | 2026-05-26 | `cleaned` | Underlay Alignment — map-plane / large image geometry drift | `89fabf1` | `318094d` | [`89fabf1...318094d`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/compare/89fabf1...318094d) | `review/v2/20260526-140000-underlay-alignment` (deleted after Codex cleanup) | `.ai/external_reviews/prompts/V2-20260526-140000_prompt.md` (deleted after Codex cleanup) | pasted directly into Kilo run; raw response not stored separately | legacy pilot exception: ingest summary not persisted as a separate artifact before mandatory ingest-artifact rule was fully enforced | `deleted` | `cleaned` | Three editor fixes applied (clampMapLocal, center-radial scale, getTransformedUnderlayBounds). V2 cycle technically successful. Codex post-accept cleanup completed. |
| V2-20260526-174500 | 2026-05-26 | `implemented` | Underlay Rotate Center Calculation — wrong scale factor in `handleRotateHandleMouseDown` center computation | `c313aa9` | `6b4c2f3` | [`c313aa9...6b4c2f3`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/compare/c313aa9...6b4c2f3) | `review/v2/20260526-174500-rotate-center-fix` | `.ai/external_reviews/prompts/V2-20260526-174500_prompt.md` | pasted directly into Kilo run; raw response not stored separately | `.ai/external_reviews/ingest_summaries/V2-20260526-174500_ingest.md` | `active` | `none` | External review snapshot fixed at `6b4c2f3`. Hypothesis confirmed by external GPT-5.5 Thinking review. Post-review implementation commit `5dfe99e` applies fix: `handleRotateHandleMouseDown` now uses `mapLocalToWorld(naturalWidth/2, naturalHeight/2, underlay)` for center, matching `handleScaleHandleMouseDown`. Typecheck + build pass. |
| V2-20260527-020100 | 2026-05-27 | `implemented` | MapRenderModel Contract Wire-Up 0.1 — review shared type, adapter, debug/bounds render (Handoff 0029) | `03efb8e` | `9b3239a` | [`03efb8e...9b3239a`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/compare/03efb8e...9b3239a) | `review/v2/20260527-020100-map-render-model-wire-up` (request: `.ai/external_reviews/requests/V2-20260527-020100_request.md`) | `.ai/external_reviews/prompts/V2-20260527-020100_prompt.md` | `.ai/external_reviews/responses/V2-20260527-020100_response.md` | `.ai/external_reviews/ingest_summaries/V2-20260527-020100_ingest.md` | `active` | `none` | External GPT-5.5 Thinking review: implementation correct. useState typing already OK. Applied depth fix (DEBUG_DEPTH=-20). Typecheck passes. |
| V2-20260527-151700 | 2026-05-27 | `cleaned` | V3 Phase 1 Docs Foundation Review — `.ai/v3/` foundation correctness, discoverability, boundary check (Handoff 0031) | `269e676` | `dd0d195` | [`269e676...dd0d195`](https://github.com/AndrewVerhoturov1/Sword_of_rome_2d/compare/269e676...dd0d195) | `review/v2/20260527-151700-v3-phase1-docs-foundation` (deleted after Codex cleanup; request existed at `.ai/external_reviews/requests/V2-20260527-151700_request.md`) | `.ai/external_reviews/prompts/V2-20260527-151700_prompt.md` (deleted after Codex cleanup) | `.ai/external_reviews/responses/V2-20260527-151700_response.md` (deleted after Codex cleanup) | `.ai/external_reviews/ingest_summaries/V2-20260527-151700_ingest.md` (deleted after Codex cleanup) | `deleted` | `cleaned` | External GPT-5.5 Thinking review accepted the Phase 1 foundation with 2 minor fixes (snapshot metadata + stale wording). Both fixes applied. Codex accepted Phase 1, transferred persistent docs changes to working branch, and cleaned up the temporary V2 review branch/artifacts. |

### Примечания к записям

`Request Location` должен явно показывать, где лежит request: `main`, `review/v2/...`, commit-pinned ссылка или local-only path.

`Branch State` должен явно фиксировать итог cleanup: `active`, `deleted`, `kept_by_decision`, `cleanup_pending` или другой понятный статус.

`Prompt Location`, `Response Location` и `Ingest Location` обязательны для всех записей после соответствующих этапов. Если external answer был вставлен напрямую (direct paste), `Response Location` должен явно это указывать.

`Snapshot Commit` в записи V2_navigation — это immutable review target: ровно тот commit, который был запушен в review-ветку и показан внешнему чату через commit-pinned links. Последующие implementation commits не заменяют `Snapshot Commit`; их нужно указывать отдельно в `Summary` или в связанных implementation artifacts.
