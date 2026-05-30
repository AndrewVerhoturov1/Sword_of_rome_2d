# V3 Send Note - D6 Dice Roller Pseudo-3D HTML Pilot

## Что уже подготовлено

- [V3-20260529-032915-d6-dice-roller-pseudo3d_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-032915-d6-dice-roller-pseudo3d_request.md) — структурированный V3 request.
- [V3-20260529-032915-d6-dice-roller-pseudo3d_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-032915-d6-dice-roller-pseudo3d_prompt.md) — готовый copy-paste prompt для внешнего чата.

## Что отправить во внешний чат

1. Вставить целиком prompt из [V3-20260529-032915-d6-dice-roller-pseudo3d_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/v3/requests/V3-20260529-032915-d6-dice-roller-pseudo3d_prompt.md).
2. Ничего руками прикладывать не нужно:
   - внутри prompt уже есть commit-pinned GitHub links;
   - внешний чат должен сам прочитать контекст по этим ссылкам.

## Что должно прийти в ответ

- либо реальный ZIP-файл;
- либо ZIP-ready representation с полным содержимым:
  - `manifest.yaml`
  - `README_FOR_KILO.md`
  - `README_FOR_CODEX.md`
  - `checksums.sha256`
  - `files/table-sandbox/v3-pilots/d6_dice_roller_pseudo3d.html`

## Что должно быть внутри project file

- один standalone HTML-файл;
- интерфейс на русском;
- настройка количества кубиков;
- настройка цвета кубиков;
- кнопка броска;
- псевдо-3D анимация на чистом 2D;
- финальные значения D6;
- без внешних библиотек и без правок существующих файлов.

## Что делать после ответа

1. Если внешний чат дал ZIP или ZIP-ready artifact package, сохранить его локально.
2. Затем вернуться сюда с ответом `Нижний чат ответил`.
3. После этого пойдёт package review.
4. Только потом решим, делать ли import и browser-проверку.

## Что не считается успехом

- просто идея;
- просто текстовое описание анимации;
- просто HTML без package structure;
- пакет с двумя и более project files;
- пакет, который лезет в `src/` или правит `index.html`;
- пакет, который использует внешний 3D/JS-движок;
- пакет, который делает вид, что repo уже изменён.
