# Стартовый prompt для planner-чата Stage 5

Твоя задача: спланировать первый `Stage 5` pilot после `ork_planner`.

Сначала прочитай bridge:

- [ork_planner_stage5_first_pilot_bridge.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/subprojects/ork_planner/ork_planner_stage5_first_pilot_bridge.md)

Потом используй документы и шаблоны, на которые он ссылается.

Исходная идея пилота минимальная:

- нужно создать pilot, в котором результатом станет skill для Codex;
- назначение skill: помогать готовить `V3` request pack для внешнего чата;
- детали skill заранее не расписаны;
- готовую архитектуру, battle plan и file set за тебя не подготовили намеренно.

Что нужно от тебя:

1. Первым делом определить и зафиксировать папку нового подпроекта.
2. Самостоятельно определить разумный scope пилота.
3. Предложить нужный docs set для этого подпроекта.
4. Определить lifecycle, gates и stop rules.
5. Объяснить, как пилот должен доказать, что такой skill реально полезен.
6. Не уходить в execution и не писать сам skill.

Ограничения:

- не придумывай repo-level promotion заранее;
- не считай `Stage 6` начатым;
- не подменяй human approval;
- не возвращай legacy route;
- если важной информации не хватает, явно остановись и спроси человека.
