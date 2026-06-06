# Live Monitor Audit Pack 019e9d2a

Этот public forensic-pack подготовлен для внешнего аудита live monitor semantics по thread `019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f`.

Что внутри:

- `live_rollout_redacted.jsonl` — read-only sanitized snapshot live rollout events по проблемному thread.
- `live_session_detail.json` — API-equivalent snapshot current `build_live_session_detail(...)`.
- `live_session_export.json` — structured export snapshot по current export semantics.
- `live_session_export.md` — markdown export всей session по current export semantics.
- `live_step_1_export.md` — markdown export одного шага, эквивалент current `Copy` для step 1.
- `manifest.json` — provenance и состав пакета.

Границы пакета:

- источник данных = local read-only `C:/Users/andre/.codex/**`;
- пакет не меняет live config и не запускает новый OTel experiment;
- redaction маскирует obvious secret-like keys и известные identity fields;
- markdown export сгенерирован локально по текущей логике export, чтобы внешний аудит мог читать готовый результат без запуска UI.

Пакет нужен как publishable substitute для локальных runtime-источников, которые нельзя просто отдать внешнему чату прямыми ссылками из `C:/Users/andre/.codex/**`.
