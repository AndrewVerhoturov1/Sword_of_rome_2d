# V3 Request Pack Skill Pilot Plan Index

Slug: `v3_request_pack_skill_pilot`  
Target file: `v3_request_pack_skill_pilot_plan_full.md`  
Owner: `Orc`  
Audience: agents  
Status: `draft`  
Last updated: `2026-06-02`

> Этот файл — agent-oriented retrieval map. Он не заменяет `v3_request_pack_skill_pilot_plan_full.md` и не пересказывает весь план заново.

## Purpose

Помочь агенту быстро находить нужные секции в `v3_request_pack_skill_pilot_plan_full.md`.

## Index rule

- Индексировать по фактическим названиям секций `plan_full`.
- Использовать section names как retrieval map, потому что явных HTML-style anchors в `plan_full` нет.
- Если `plan_full` меняется, индекс нужно пересмотреть.

## Fast section table

| Need | Section in `plan_full` | Status |
|---|---|---|
| Purpose | `## Назначение документа` | `verified` |
| Quick summary | `## Быстрый итог` | `verified` |
| Source basis | `## Source of Truth и порядок чтения` | `verified` |
| Scope | `## Scope пилота` | `verified` |
| Skill boundary | `## Целевой skill и его границы` | `verified` |
| Authorization boundary | `## Authorization boundary` | `verified` |
| Proof profile | `## Proof profile для первого пилота` | `verified` |
| Lifecycle and gates | `## Lifecycle и gates` | `verified` |
| Automation policy | `## Automation policy` | `verified` |
| Stop rules | `## Stop rules` | `verified` |
| Success criteria | `## Success criteria` | `verified` |
| Safe next step | `## Ближайший безопасный следующий шаг` | `verified` |

## High-value retrieval blocks

| Retrieval block | Section |
|---|---|
| purpose | `## Назначение документа` |
| scope | `## Scope пилота` |
| authorization boundary | `## Authorization boundary` |
| proof profile | `## Proof profile для первого пилота` |
| lifecycle / gates | `## Lifecycle и gates` |
| automation policy | `## Automation policy` |
| stop rules | `## Stop rules` |
| success criteria | `## Success criteria` |

## Stage-to-section map

| Topic | Main section | Notes |
|---|---|---|
| `Stage 5 pilot` framing | `## Быстрый итог` | Короткий summary и ограничения |
| Current pilot scope | `## Scope пилота` | Что внутри и вне scope |
| Future gate boundaries | `## Lifecycle и gates` | Не считать следующий stage открытым |
| Proof bar | `## Proof profile для первого пилота` | Что считается достаточным proof |

## Maintenance rule

Обновлять этот файл только когда меняются секции, названия блоков или retrieval priorities в `plan_full`.
