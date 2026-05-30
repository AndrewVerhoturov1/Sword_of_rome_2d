# README_FOR_CODEX

## Что это за пакет

Это V3 external artifact package для:

```text
V3-20260530-130503-hierarchical-subproject-working-plan
```

Он содержит один proposed project-файл:

```text
.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md
```

Важное изменение этой версии: основной документ написан **на русском языке**, чтобы человек мог читать его напрямую.

## Что проверить

Codex должен проверить:

- в пакете ровно один project-файл под `files/`;
- путь project-файла совпадает с allowed path;
- `action` = `create`;
- `scope` = `workflow_docs`;
- документ на русском языке и пригоден для чтения человеком;
- документ короче и практичнее master rollout plan;
- первый крупный рабочий шаг — создание сущности подпроекта;
- нет детального block-by-block breakdown;
- есть rough work volume без фальшивой точности;
- есть decision gates;
- есть `Do Not Do Yet` или смысловой аналог;
- есть immediate next step;
- документ не утверждает, что repo уже изменён;
- документ не утверждает, что route уже fully validated.

## Что не входит

Этот пакет не выполняет Kilo import, не создаёт journals, не обновляет V3 navigation и не запускает тесты.
