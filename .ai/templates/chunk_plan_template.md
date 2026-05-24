# Chunk Plan Template

## Chunk ID

`CHUNK-NNN_short_name`

## Chunk Name

Краткое название chunk (например, «Governance Bootstrap»)

## Status

`planned` / `active` / `accepted` / `accepted_with_warnings` / `needs_revision` / `rejected` / `blocked`

## Owner Chat

Идентификатор или описание рабочего чата, выполняющего chunk.

## Goal

Чёткое описание цели chunk. Что должно быть сделано и какой результат ожидается.

## Allowed Files

Список файлов, которые разрешено создавать или изменять в рамках chunk.

- `path/to/file1.md`
- `path/to/file2.md`

## Forbidden Files

Список файлов, которые запрещено изменять.

- `path/to/forbidden1.md`
- `path/to/forbidden2.md`

## Required Inputs

Файлы, которые рабочий чат **обязан** прочитать перед началом работы.

- `path/to/required1.md`
- `path/to/required2.md`

## Lookup Inputs

Файлы, которые читаются только при необходимости сверить стиль, конвенции или текущее состояние.

- `path/to/lookup1.md`
- `path/to/lookup2.md`

## Do Not Read Unless Blocked

Файлы, которые не следует читать без крайней необходимости (обычно большие или нерелевантные).

- `path/to/avoid1.md`
- `path/to/avoid2.md`

## Context Budget

Указание по экономии контекста: какие файлы читать частично, какие разделы наиболее релевантны.

## Policy Inputs

РџРѕР»РёС‚РёРєРё, РєРѕС‚РѕСЂС‹Рµ СЂР°Р±РѕС‡РёР№ С‡Р°С‚ РґРѕР»Р¶РµРЅ СЃС‡РёС‚Р°С‚СЊ source of truth РґР»СЏ language / human review / bug reporting.

- `.ai/policies/language_policy.md`
- `.ai/policies/human_review_policy.md`
- `.ai/policies/bug_tracking_policy.md`
- `.ai/logs/bug_journal.md`, РµСЃР»Рё Р·Р°РґР°С‡Р° СЃРІСЏР·Р°РЅР° СЃ bugfix / debugger / repeated issue / visible regression

## Language Policy Expectation

РљСЂР°С‚РєРѕРµ РїСЂР°РІРёР»Рѕ РґР»СЏ СЌС‚РѕРіРѕ chunk:

- internal technical identifiers = English
- user-facing UI text may be Russian
- no transliterated technical names

## Human Check Expectation

`required` / `suggested` / `not needed`

Р•СЃР»Рё `required` РёР»Рё `suggested`, chunk РґРѕР»Р¶РµРЅ СЏРІРЅРѕ Р·Р°С„РёРєСЃРёСЂРѕРІР°С‚СЊ:

- С‡С‚Рѕ РѕС‚РєСЂС‹С‚СЊ;
- РєСѓРґР° РЅР°Р¶Р°С‚СЊ РёР»Рё С‡С‚Рѕ РїРѕСЃРјРѕС‚СЂРµС‚СЊ;
- С‡С‚Рѕ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РІРёРґРЅРѕ;
- С‡С‚Рѕ РґРѕР»Р¶РµРЅ РѕС‚РІРµС‚РёС‚СЊ С‡РµР»РѕРІРµРє.

## Bug Tracking Expectation

- report РѕР±СЏР·Р°РЅ СЃРѕРґРµСЂР¶Р°С‚СЊ `Баги и сложности`
- debugger / bugfix / repeated issue chunks РґРѕР»Р¶РЅС‹ СЃРЅР°С‡Р°Р»Р° СЃРјРѕС‚СЂРµС‚СЊ `.ai/logs/bug_journal.md`
- failed human check = real bug/difficulty state
- verification РґРѕР»Р¶РЅР° Р±С‹С‚СЊ concrete

## Required Report Sections

- `Баги и сложности`
- `Human Check`
- `Runtime metadata`

## Execution Mandate

`agent-first`

Worker Codex не является исполнителем по умолчанию. Содержательное выполнение задач идёт через `Kilo Code` и/или `External Web Chat`. Direct Codex execution без explicit pre-approved exception запрещён.

## Primary Execution Path

`Kilo Code` / `External Web Chat`

## Allowed Agent Kinds

- `Kilo Code`
- `External Web Chat`

## Default Preference

При равной пригодности предпочитать `External Web Chat`, но не для repo-authority/file-edit задач.

## Exception Status

`none` / `Codex-only exception` / `strategist-only` / `human-only` / `checkpoint-only` / `manual external publish`

Если `none` — worker не может использовать direct Codex execution. Если worker считает, что часть scope требует direct Codex execution или правки за пределами списка allowed files, он должен остановиться и вернуть blocked report.

## Minimum Substantive Agent Work

Run считается substantive только если он materially advances goal. Декоративный/tiny run без material progress не засчитывается.

## Sequential Agent Policy

Execution-задачи могут включать несколько агентных шагов, но только последовательно: один запуск → review → следующий запуск. Параллельное выполнение агентов в рамках одного handoff запрещено.

## If No Agent Path Fits → Return Escalation Note

Если ни один agent path не подходит для выполнения задачи, worker должен вернуть blocked report / escalation note, а не выполнять задачу через direct Codex execution.

## Stop Conditions

Условия, при которых chunk должен остановиться и вернуть completion report с блокировкой:

- Условие 1
- Условие 2

## Expected Outputs

Конкретный список артефактов, которые должны быть созданы в результате выполнения chunk.

- `path/to/output1.md`
- `path/to/output2.md`

## Completion Report Path

`path/to/report.md`

## Acceptance Criteria

Чеклист для приёмки chunk стратегическим чатом:

- [ ] Критерий 1
- [ ] Критерий 2
- [ ] Критерий 3
