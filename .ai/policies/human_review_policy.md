# Human Review Policy

## Main rule

Agents must explicitly identify when a result needs human review.

Human review is required when correctness cannot be reliably confirmed by automated checks alone, especially for visual UI, browser interaction, layout, usability, readable Russian text, demos, and user-facing behavior.

Human review requests must be written in simple Russian.

The user is not assumed to be a programmer.

## When human review is required

Human review is required for:

- visible UI/layout changes;
- Phaser/canvas/table rendering;
- click, drag, zoom, pan, selection, or other browser interaction;
- demo/public page checks;
- anything where "it looks correct" matters;
- user-facing Russian labels, messages, tooltips, and instructions;
- accepting a visual or UX checkpoint;
- cases where automated checks pass but the user must confirm the real browser result.

Examples:

- `Проверь, видно ли зелёное поле.`
- `Кликни по полю и посмотри, меняются ли координаты справа.`
- `Проверь, понятно ли написаны кнопки.`
- `Проверь, не съехала ли панель.`

## When human review is suggested, but not mandatory

Human review is suggested when the user can check faster than the agent, for example:

- choosing between two UI wording variants;
- confirming whether an interaction feels convenient;
- checking whether a screen is understandable;
- confirming visual polish.

## When human review is usually not needed

Human review is usually not needed for purely internal changes that automated checks can verify:

- docs-only patch;
- JSON fixture structure;
- TypeScript typecheck;
- build;
- lint;
- unit tests;
- internal refactor with no visible behavior change.

But if the change affects user-facing text or visible behavior, human review may still be required.

## Required report section

Every implementation report or Kilo result must include a section:

`Human Check`

It must say one of:

- `required`
- `suggested`
- `not needed`

If `required` or `suggested`, include:

- why the check is needed;
- simple Russian steps for the user;
- expected result;
- what the user should reply.

## Simple Russian requirement

Human review instructions must be simple and practical.

Bad:

`Verify renderer-runtime integration and event propagation.`

Good:

`Пожалуйста, открой страницу. Кликни по зелёному полю. Справа должны измениться координаты клика.`

## Required human check template

Use this template:

```markdown
### Human Check

Status: required

Reason:
[простыми словами почему нужна проверка человеком]

Please check:
1. [простое действие]
2. [простое действие]
3. [простое действие]

Expected result:
[что должно быть видно или что должно произойти]

Please reply:
[короткая фраза, что пользователь должен написать]
```

Example:

```markdown
### Human Check

Status: required

Reason:
Мы меняли отображение Phaser-поля. Это нужно проверить глазами в браузере.

Please check:
1. Открой приложение.
2. Посмотри, видно ли зелёное поле.
3. Кликни по полю.

Expected result:
Поле видно. После клика справа меняются координаты.

Please reply:
"Поле видно, клик работает" или "Поле не видно / клик не работает".
```

## Acceptance rule

If human review is required, the task should not be marked fully accepted until the user confirms the check.

If the agent cannot get human confirmation in the current run, it must mark the result as:

`pending human check`

and clearly explain what remains to be checked.

## Do not overuse

Do not ask the user to check every tiny internal change.

Use automated checks first when they are available.

Ask for human review when it is actually useful, necessary, faster, or safer.
