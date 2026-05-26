# Handoff 0023: V2 Docs Verifier

## Статус

Готово для Kilo

## Рекомендуемый Kilo mode

kilo-verifier

## Task role

Tester Agent

## Task profile

workflow-rules-verification

## Execution mandate

`agent-first`

## Primary execution path

`Kilo Code`

## Allowed agent kinds

- `Kilo Code`

## Session plan

[2026-05-26_v2_external_review_docs_implementation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-05-26_v2_external_review_docs_implementation.md)

## Plan item

`P2: V2 Verification`

## Session run

`003`

## Рекомендуемый класс модели

strong_model

## Default model

Kimi K2.6

## Fallback model или Candidate models

- DeepSeek V4 Pro

## Когда эскалировать в strong_model

- already selected by default: это verifier для `workflow-rules-change`;
- если найдётся конфликт между `AGENTS.md`, `.ai/rules/agent_protocol.md`, `.ai/rules/kilo_mode_contract.md` и `.ai/external_reviews/**`;
- если без file-write исправлений нельзя даже сформулировать verdict.

## Уровень риска

Средний

## Цель

Сделать read-only verification всего текущего V2 docs set после correction passes и внешнего audit. Нужен строгий verdict: можно ли переходить к low-risk manual pilot, или ещё остались contract conflicts / missing fields / unsafe wording.

## Контекст

- P1 уже принят Codex после correction runs и ручных docs-уточнений.
- Последние локальные clarifications уже в `main`:
  - template vs instantiated artifacts;
  - явное объяснение, где placeholders, а где живые ссылки.
- Пользователь хочет следующий шаг по workflow, а не новый redesign.

## Required Inputs

- [AGENTS.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/AGENTS.md)
- [2026-05-26_v2_external_review_docs_implementation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/sessions/2026-05-26_v2_external_review_docs_implementation.md)
- [v2_external_senior_review_system.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/plans/master/v2_external_senior_review_system.md)
- [README.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/README.md)
- [V2_navigation.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/V2_navigation.md)
- [v2_request_template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/templates/v2_request_template.md)
- [v2_prompt_template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/templates/v2_prompt_template.md)
- [v2_response_template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/templates/v2_response_template.md)
- [v2_ingest_summary_template.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/templates/v2_ingest_summary_template.md)
- [v2_safety_checklist.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_reviews/templates/v2_safety_checklist.md)
- [agent_protocol.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/agent_protocol.md)
- [kilo_mode_contract.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/rules/kilo_mode_contract.md)
- [manual.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/external_chats/manual.md)
- [create_external_question_prompt.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/prompts/create_external_question_prompt.md)
- [create_external_chat_request.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/prompts/create_external_chat_request.md)
- [0021_v2_external_review_docs_foundation_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0021_v2_external_review_docs_foundation_report.md)
- [0022_v2_manual_ingest_correction_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0022_v2_manual_ingest_correction_report.md)

## User Overrides

- Основные V2 docs и шаблоны должны быть на русском.
- Технические identifiers, file names, IDs, branch names и machine-readable values должны оставаться на английском.
- V2 first version не использует `kilo-recorder`.
- `kilo-notebook` остаётся `/v1-only`.
- `/v2 preview` обязателен перед любым push.
- Push в public `review/v2/...` branch считается публикацией.

## Allowed Changes

- Ничего не менять в project files.
- Разрешено создать или перезаписать только report-файл по пути ниже.

## Forbidden Changes

- не менять `AGENTS.md`, `.ai/rules/**`, `.ai/external_reviews/**`, `.ai/prompts/**`;
- не создавать новый handoff;
- не создавать pilot artifacts;
- не предлагать широкую переработку, если хватает narrow follow-up fix list.

## Точная задача

Проведи verifier review текущего V2 docs set.

Проверь:

1. Нет ли contract conflicts между:
   - `AGENTS.md`
   - `.ai/rules/agent_protocol.md`
   - `.ai/rules/kilo_mode_contract.md`
   - `.ai/external_chats/manual.md`
   - `.ai/prompts/create_external_question_prompt.md`
   - `.ai/prompts/create_external_chat_request.md`
   - `.ai/external_reviews/**`
2. Ясно ли разведены:
   - template layer;
   - instantiated request/prompt artifacts;
   - review-branch runtime artifacts;
   - raw response / ingest artifacts;
   - sanitized accepted summaries.
3. Нет ли leftover wording drift:
   - `recording step`
   - `interpretation step`
   - `Request Path`
   - других формулировок, которые тянут V2 обратно к `/r1` или `kilo-recorder`.
4. Достаточно ли строгий push/safety model:
   - `/v2 preview` before push;
   - public branch = публикация;
   - raw V2 runtime artifacts not in `main` by default;
   - safety checklist не противоречит README и templates.
5. Достаточно ли практичны templates для первого manual pilot.

## Acceptance Criteria

- [ ] Report даёт явный verdict: `good to implement with small fixes` или `needs substantial revision before pilot`
- [ ] Если есть проблемы, они перечислены по severity и с file references
- [ ] Если blocking problems нет, это сказано прямо
- [ ] Report содержит `Баги и сложности`, `Human Check`, `Runtime metadata`
- [ ] Read-only boundary сохранена

## Report mode

full

## Report write policy

`read-only except report`

## Куда записать report

[0023_v2_docs_verifier_report.md](/D:/Codex+Kilocode/projects/sword-of-rome-web/.ai/reports/0023_v2_docs_verifier_report.md)
