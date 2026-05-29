# Ручная настройка режима Kilo Notebook V3

Этот гайд объясняет, как вручную добавить и проверить режим `Kilo Notebook V3` в интерфейсе Kilo Code.

Важно: это setup guide, а не доказательство, что режим уже настроен.

## Текущий статус

- Режим `kilo-notebook-v3` / `Kilo Notebook V3` canonically разрешён в правилах.
- `.ai/v3/` foundation, contracts, prompts и templates уже созданы.
- Этот setup guide существует.
- Но live UI status режима нужно подтверждать отдельно.

### Operational status fields

При фактической настройке человек должен явно зафиксировать:

```text
Kilo Notebook V3 mode configured in UI: yes / no
Date:
Who confirmed:
Notes:
```

Пока такого подтверждения нет, import-stage нельзя считать готовым.

## Что этот документ не доказывает

Этот документ не доказывает, что:

- режим уже создан в живом Kilo UI;
- Kilo уже умеет принимать ZIP;
- import-stage уже начался;
- `.ai/v3/staging/` уже является обязательным input path.

## Когда использовать этот guide

Этот guide нужен только на переходе в `Phase 5C - Kilo Notebook V3 UI Setup`.

Он не нужен для:

- `Phase 5A - External Artifact Generation Pilot`;
- `Phase 5B - Pre-Kilo Package Review`.

До этих стадий внешний package можно тестировать без настройки режима.

## 1. Добавить режим в интерфейс Kilo

1. Откройте интерфейс Kilo Code.
2. Найдите список доступных Kilo modes.
3. Добавьте новый режим:
   - **Внутреннее mode-значение:** `kilo-notebook-v3`
   - **UI-имя:** `Kilo Notebook V3`
   - **Описание:** безопасный raw-input import/check/write/journal flow для V3 artifact package
4. Убедитесь, что новый режим виден в списке modes.

### Рекомендуемая связка

- `Kilo mode = Kilo Notebook V3`
- `Task role = Notebook Agent`

Не путать:

- `Kilo Notebook` — `/v1-only`
- `Kilo Recorder` — `/r1-only`
- `Kilo Notebook V3` — отдельный V3 import mode

## 2. Проверить repo-level canon

После настройки в UI убедитесь, что repo-level docs уже знают про этот режим:

- [`AGENTS.md`](../../../AGENTS.md)
- [`.ai/README.md`](../../README.md)
- [`.ai/rules/agent_protocol.md`](../../rules/agent_protocol.md)
- [`.ai/rules/kilo_mode_contract.md`](../../rules/kilo_mode_contract.md)

## 3. Hard gate before first import run

Запуск `Kilo Notebook V3` нельзя делать, пока одновременно не выполнены все условия:

1. Есть реальный внешний artifact package.
2. Package уже прошёл pre-Kilo package review.
3. Режим реально настроен в UI.
4. Известен raw package source: archive link или local archive path.
5. Человек подтвердил, что текущий шаг — это import pilot.
6. `git rev-parse --show-toplevel` показывает правильный repo root.

Если это не так, текущий статус должен оставаться в pre-Kilo состоянии, а не в import-state.

## 4. Input source

До scripted support input source нельзя считать автоматически решённым.

Правильное правило:

- `.ai/v3/staging/` — это import-stage tool;
- это не обязательная human-обязанность до import-stage;
- если выбран repo-local staging fallback, это должно быть сказано явно в текущем run;
- если import-stage ещё не начался, ZIP можно просто хранить локально и review-ить без staging;
- базовый raw input для режима: archive link или local archive path;
- короткая note из ответа внешнего чата опциональна.

## 4A. Repo root detection

Перед любыми файловыми операциями режим обязан сначала определить реальный git repo root:

```text
git rev-parse --show-toplevel
```

Это обязательный preflight.

Правила:

- все relative target paths считаются только от найденного git repo root;
- journal draft создаётся только внутри этого repo root;
- `V3_navigation.md` обновляется только внутри этого repo root;
- local archive path в `Downloads` или `Documents` не влияет на target root;
- открытая папка VS Code сама по себе не источник истины, если она не совпадает с git repo root.

Если repo root не определяется или режим видит другой root, import-run должен остановиться с `blocked` и ничего не записывать.

## 5. Что нужно для import-stage

Только после перехода в `Phase 5D` нужны:

1. Реальный V3 artifact package.
2. Исходный V3 request или хотя бы `V3 ID`.
3. Operating reference [`../prompts/kilo_notebook_v3_mode_prompt.md`](../prompts/kilo_notebook_v3_mode_prompt.md).
4. Явный package source.
5. Подтверждённый repo root.

## 6. Human preflight checklist

Перед первым import pilot проверьте:

- [ ] Есть реальный внешний package.
- [ ] Package уже review-нут на уровне ZIP/manifest/files/checksums.
- [ ] Режим `Kilo Notebook V3` реально добавлен в UI.
- [ ] Человек понимает, что сейчас идёт именно import test, а не только external package test.
- [ ] Известен archive link или local archive path.
- [ ] `git rev-parse --show-toplevel` показывает нужный repo root.
- [ ] Operating reference прочитан.
- [ ] Journal template понятен.

## 7. Что изменится позже

- **Phase 5A:** внешний package test без Kilo import (завершён).
- **Phase 5B:** pre-Kilo package review (завершён).
- **Phase 5C:** UI setup режима (завершён).
- **Phase 5D:** import pilot (завершён).
- **Phase 7 foundation:** `scripts/v3/*` созданы (validate, stage, journal helpers). `/v3` shortcut не активирован. `apply_v3_package.py` не создан. Manual flow остаётся primary.

## Связанные документы

- [`../README.md`](../README.md)
- [`../V3_navigation.md`](../V3_navigation.md)
- [`../prompts/kilo_notebook_v3_mode_prompt.md`](../prompts/kilo_notebook_v3_mode_prompt.md)
- [`../contracts/v3_storage_policy.md`](../contracts/v3_storage_policy.md)
- [`../contracts/v3_acceptance_policy.md`](../contracts/v3_acceptance_policy.md)
- [`../../plans/master/v3_workflow_implementation_plan.md`](../../plans/master/v3_workflow_implementation_plan.md)
