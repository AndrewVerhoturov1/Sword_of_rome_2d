# {Subproject Title} Journal

Слаг: `{subproject_slug}`  
Владелец: `Orc`  
Статус: `active / draft / archived`  
Начат: `YYYY-MM-DD`

## Назначение

Этот файл фиксирует фактические действия по подпроекту.

Журнал отвечает на вопрос:

```text
Что реально произошло?
```

Он не отвечает на вопрос:

```text
Какие долгоживущие решения теперь действуют?
```

Для этого есть:

```text
{subproject_slug}_decisions.md
```

## Что записывать в journal

Записывать:

- выполненный шаг;
- stage/lifecycle state во время шага;
- роль, которая выполняла шаг;
- route/tool, если это важно для evidence;
- созданные файлы;
- изменённые файлы;
- проверку, которая реально была сделана;
- bugs and difficulties;
- human verdict, если он действительно был дан;
- безопасный следующий шаг.

## Что не записывать в journal

Не превращать journal в:

- `plan_full`;
- `battle_plan`;
- `status`;
- `decisions`;
- long chat transcript;
- fake historical backfill;
- список будущих желаний.

Если нужно зафиксировать важное решение, добавь его в `{subproject_slug}_decisions.md`, а в journal оставь только факт, что решение было принято/перенесено.

## Формат записи

```md
### J-YYYYMMDD-001 — <короткий заголовок>

- Этап жизненного цикла: `<stage>`
- Роль: `<Planner / Orc / Codex / Kilo / human / external V3>`
- Маршрут выполнения: `<direct / V3 / Kilo / manual / other>`
- Ссылка на сессию: `<id / path / not available>`
- Созданные файлы:
  - `<path or none>`
- Изменённые файлы:
  - `<path or none>`
- Подтверждение:
  - `<что подтверждено>`
- Проверка:
  - `<какая проверка реально выполнена>`
- Вердикт человека: `<accepted / needs fixes / rejected / pending / not applicable>`
- Баги и сложности:
  - `<none / issue>`
- Следующий шаг:
  - `<safe next step>`
```

## Decision mirror

Если запись содержит важное решение, добавь короткую пометку:

```text
Decision mirror: reflected in {subproject_slug}_decisions.md
```

Не копируй весь decisions file обратно в journal.

## Entries

### J-YYYYMMDD-001 — <первое фактическое действие>

- Этап жизненного цикла: `<stage>`
- Роль: `Orc`
- Маршрут выполнения: `<direct / V3 / Kilo / manual>`
- Ссылка на сессию: `not available`
- Созданные файлы:
  - `<path / none>`
- Изменённые файлы:
  - `<path / none>`
- Подтверждение:
  - `<facts>`
- Проверка:
  - `<checks actually run>`
- Вердикт человека: `pending`
- Баги и сложности:
  - `<none found / issue>`
- Следующий шаг:
  - `<safe next step>`

## Bugs and difficulties

Текущий статус:

```text
none found / open / fixed / pending human review
```

Повторяющиеся process issues:

- `<issue 1>`
- `<issue 2>`

## Open follow-ups

- `<follow-up 1>`
- `<follow-up 2>`

## Maintenance rule

- Не придумывать прошлые события.
- Не закрывать human verdict без явного сообщения человека.
- Не начинать следующий stage через journal.
- Не хранить здесь full strategy.
- Если потерян контекст, сначала читать `{subproject_slug}_status.md`, потом последние journal entries.
