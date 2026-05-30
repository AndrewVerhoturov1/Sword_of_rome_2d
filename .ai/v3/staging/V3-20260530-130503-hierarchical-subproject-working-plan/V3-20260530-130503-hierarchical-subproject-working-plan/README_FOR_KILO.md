# README_FOR_KILO

## Назначение пакета

Это V3 artifact package для создания одного нового project-файла:

```text
.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md
```

Основной project-файл написан **на русском языке**, потому что человек должен уметь быстро прочитать и проверить его без перевода.

Пакет не означает, что репозиторий уже изменён.

## Что импортировать

Импортировать только файл внутри `files/`:

```text
files/.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md
```

Целевой путь в репозитории:

```text
.ai/plans/implementation/hierarchical_subproject_workflow_work_plan.md
```

Action: `create`  
Scope: `workflow_docs`  
Language: `ru-RU`

## Важные границы

- Не создавать дополнительные project-файлы из этого пакета.
- Не обновлять `.ai/v3/V3_navigation.md` из этого пакета.
- Не создавать journal-записи как часть самого artifact package.
- Не менять `AGENTS.md`, `.ai/rules/`, `.ai/plans/master/`, `ideas/`, `src/`, `scripts/` или product-code paths.
- Post-import testing mode для этого запроса: `waived`.
- Review выполняет Codex.
- Финальное принятие выполняет человек.

## Проверка перед импортом

Проверить, что под `files/` есть ровно один project-файл и что его путь совпадает с ожидаемым.
