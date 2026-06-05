# Token Cost Normalizer v1 Implementation Pack

V3 ID: `V3-20260605-141503-token-cost-normalizer-v1`
Task title: `Create repo-local implementation pack for Token Cost Normalizer v1`
Target project file for this V3 package: `.ai/subprojects/tokken_dashboard/drafts/token_cost_normalizer_v1_implementation_pack.md`

## No Repo Access Statement

Я понимаю и фиксирую границы этого V3 artifact-producing запроса:

- у внешнего чата нет прямого доступа на запись в репозиторий и нет локального filesystem-доступа к workspace;
- внешний чат может читать публичный GitHub-контекст по raw/blob-ссылкам из запроса;
- этот результат — ZIP artifact package, а не запись файлов напрямую в repo;
- package может быть отдельно review-нут до local apply-stage;
- локальное создание реальных `scripts/`, `config/`, `tests/` и doc updates произойдёт позже отдельным Kilo apply/run;
- test execution сейчас не выполняется внешним чатом и остаётся за Kilo;
- финальный review и решение о принятии остаются у Codex и человека.

## Scope Boundary

Этот файл является implementation pack. Он содержит полные ready-to-apply contents будущих mixed-scope files, но сам V3 package создаёт только этот markdown-файл.

Allowed project file in this package:

```text
.ai/subprojects/tokken_dashboard/drafts/token_cost_normalizer_v1_implementation_pack.md
```

Future files documented here, but not directly created by this V3 package:

```text
scripts/codex_token_cost_normalizer.py
config/token_pricing.json
tests/test_codex_token_cost_normalizer.py
```

## Context Readback

Read/used public context from the request:

- `AGENTS.md`: repo language policy keeps internal identifiers/file names in English and Russian is allowed for user-facing docs/reports; implementation/report outputs should include concrete verification and human-readable notes.
- `scripts/codex_token_debugger.py`: existing parser emits sanitized artifacts such as `token_usage.jsonl`, `sessions.jsonl`, `session_summary.json`, warnings and a Russian diagnostic report; the normalizer should build on sanitized parser outputs, not raw OTel.
- `scripts/codex_otel_compare.py`, `scripts/mcp_schema_inventory.py`, `scripts/tool_mcp_activity_inspector.py`: current diagnostic stack is local, JSON/JSONL-based, CLI-oriented, and writes markdown reports plus summary JSON.
- `tokken_dashboard_decisions.md`: accepted decision `D-20260604-009` requires future token comparisons to use cache-adjusted metrics and estimated cost, not raw input alone.
- `tokken_dashboard_readme/navigation/journal`: subproject is active and should add new generated tools/docs through explicit navigation/journal updates after local materialization.

## Required formulas encoded by the future implementation

```text
non_cached_input_tokens = max(input_tokens - cached_tokens, 0)
cached_ratio = cached_tokens / input_tokens if input_tokens > 0, else 0
estimated_input_cost_usd = non_cached_input_tokens * input_price_per_1m / 1_000_000
estimated_cached_input_cost_usd = cached_tokens * cached_input_price_per_1m / 1_000_000
estimated_output_cost_usd = output_tokens * output_price_per_1m / 1_000_000
estimated_total_cost_usd = estimated_input_cost_usd + estimated_cached_input_cost_usd + estimated_output_cost_usd
```

If `cached_tokens > input_tokens`, future script must:

- emit a warning;
- keep `cached_ratio = cached_tokens / input_tokens` when `input_tokens > 0`;
- clamp `non_cached_input_tokens` to `0` via `max(input_tokens - cached_tokens, 0)`.

If model pricing is unknown, future script must:

- not invent a price;
- set `pricing_unknown = true`;
- set `prices_per_1m = null`;
- set all `estimated_cost_usd` fields to `null`;
- emit a warning.

## Future CLI

```bash
python scripts/codex_token_cost_normalizer.py --input-dir <path> --out-dir <path> --pricing config/token_pricing.json
```

The future script accepts either:

- `<path>/parsed/token_usage.jsonl`, `<path>/parsed/session_summary.json`, `<path>/parsed/sessions.jsonl`; or
- `<path>/token_usage.jsonl`, `<path>/session_summary.json`, `<path>/sessions.jsonl` when `<path>` is already the parsed directory.

Optional nearby inputs:

```text
compare_summary.json
*_confirmation_summary.json
old summary JSON files
```

If optional files are missing, the future script warns and continues.

## Future outputs

```text
token_cost_turns.jsonl
token_cost_sessions.json
token_cost_summary.json
token_cost_report.md
token_cost_dashboard_data.json
```

`token_cost_dashboard_data.json` is safe to treat as optional/future-facing dashboard payload, but this implementation writes it because it is useful and deterministic.

## Future normalized turn shape

Each row in `token_cost_turns.jsonl` has this shape:

```json
{
  "schema_version": "token-cost-normalizer.v1",
  "source_run_id": "fixture-run",
  "thread_id": "thread-1",
  "turn_id": "t1",
  "turn_index": 1,
  "timestamp": "2026-06-05T00:00:00+00:00",
  "model": "gpt-5.5",
  "reasoning_effort": "medium",
  "input_tokens": 1000,
  "cached_tokens": 200,
  "non_cached_input_tokens": 800,
  "cached_ratio": 0.2,
  "output_tokens": 100,
  "reasoning_tokens": 7,
  "tool_tokens": 3,
  "prices_per_1m": {
    "input": 5.0,
    "cached_input": 0.5,
    "output": 30.0
  },
  "estimated_cost_usd": {
    "input": 0.004,
    "cached_input": 0.0001,
    "output": 0.003,
    "total": 0.0071
  },
  "observed_mcp_server_count": 0,
  "observed_mcp_servers": [],
  "enabled_plugins_count": 0,
  "enabled_skills_count": 0,
  "global_user_instructions_status": "unknown",
  "repo_context_status": "unknown",
  "pricing_unknown": false,
  "warnings": [],
  "source_files": ["parsed/token_usage.jsonl"]
}
```

## Future session aggregation shape

Each item in `token_cost_sessions.json.sessions` has this shape:

```json
{
  "thread_id": "thread-1",
  "turn_count": 2,
  "models": ["gpt-5.5"],
  "reasoning_efforts": ["medium"],
  "total_input_tokens": 1200,
  "total_cached_tokens": 250,
  "total_non_cached_input_tokens": 950,
  "average_cached_ratio": 0.225,
  "total_output_tokens": 130,
  "total_reasoning_tokens": 8,
  "total_tool_tokens": 3,
  "estimated_total_cost_usd": 0.009,
  "model_switch_detected": false,
  "reasoning_switch_detected": false,
  "warnings": []
}
```

## Future file: `scripts/codex_token_cost_normalizer.py`

```python
#!/usr/bin/env python3
"""Normalize parsed Codex token telemetry into cache-adjusted cost artifacts.

This script reads sanitized parser outputs produced by scripts/codex_token_debugger.py
and creates cost-oriented artifacts for later dashboard/report layers.
It never reads raw OTel telemetry and does not invent prices for unknown models.
"""
from __future__ import annotations

import argparse
import json
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "token-cost-normalizer.v1"

TOKEN_TYPE_TO_FIELD = {
    "input": "input_tokens",
    "input_tokens": "input_tokens",
    "prompt": "input_tokens",
    "cached_input": "cached_tokens",
    "cached": "cached_tokens",
    "cached_tokens": "cached_tokens",
    "output": "output_tokens",
    "output_tokens": "output_tokens",
    "completion": "output_tokens",
    "reasoning_output": "reasoning_tokens",
    "reasoning": "reasoning_tokens",
    "reasoning_tokens": "reasoning_tokens",
    "tool": "tool_tokens",
    "tool_tokens": "tool_tokens",
}

INPUT_KEYS = (
    "input_tokens",
    "input_token_count",
    "prompt_tokens",
    "codex.turn.token_usage.input",
    "gen_ai.usage.input_tokens",
    "codex.usage.input_tokens",
)
CACHED_KEYS = (
    "cached_tokens",
    "cached_token_count",
    "cached_input_tokens",
    "codex.turn.token_usage.cached_input",
    "gen_ai.usage.cached_tokens",
    "codex.usage.cached_input_tokens",
)
OUTPUT_KEYS = (
    "output_tokens",
    "output_token_count",
    "completion_tokens",
    "codex.turn.token_usage.output",
    "gen_ai.usage.output_tokens",
    "codex.usage.output_tokens",
)
REASONING_KEYS = (
    "reasoning_tokens",
    "reasoning_token_count",
    "codex.turn.token_usage.reasoning_output",
    "gen_ai.usage.reasoning_tokens",
    "codex.usage.reasoning_tokens",
)
TOOL_KEYS = (
    "tool_tokens",
    "tool_token_count",
    "codex.turn.token_usage.tool",
    "gen_ai.usage.tool_tokens",
    "codex.usage.tool_tokens",
)

OPTIONAL_EXACT_FILES = ("compare_summary.json",)
OPTIONAL_GLOB_GROUPS = (
    ("*_confirmation_summary.json", "confirmation_summary_files"),
    ("*summary.json", "old_summary_json_files"),
)


@dataclass
class OptionalContext:
    loaded_files: list[str] = field(default_factory=list)
    missing_warnings: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    summaries: dict[str, Any] = field(default_factory=dict)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize parsed Codex token usage into cache-adjusted cost artifacts."
    )
    parser.add_argument("--input-dir", required=True, help="Input dir containing parsed/ outputs or the parsed dir itself.")
    parser.add_argument("--out-dir", required=True, help="Output dir for token cost artifacts.")
    parser.add_argument("--pricing", required=True, help="Path to config/token_pricing.json.")
    return parser.parse_args(argv)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_markdown(path: Path, lines: list[str]) -> None:
    # UTF-8 with BOM makes Russian markdown safer for ordinary Windows editors.
    path.write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def resolve_parsed_dir(input_dir: Path) -> Path:
    parsed = input_dir / "parsed"
    if parsed.exists() and parsed.is_dir():
        return parsed
    return input_dir


def to_int(value: Any, default: int = 0) -> int:
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return default


def to_float_or_none(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def first_present(row: dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    attrs = row.get("attributes") if isinstance(row.get("attributes"), dict) else {}
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
        if key in attrs and attrs[key] is not None:
            return attrs[key]
    return default


def first_text(row: dict[str, Any], keys: Iterable[str], default: str) -> str:
    value = first_present(row, keys)
    if value is None or value == "":
        return default
    return str(value)


def pricing_table(pricing_payload: dict[str, Any]) -> dict[str, dict[str, float]]:
    raw = pricing_payload.get("prices_per_1m", pricing_payload)
    table: dict[str, dict[str, float]] = {}
    if not isinstance(raw, dict):
        return table
    for model, payload in raw.items():
        if not isinstance(payload, dict):
            continue
        input_price = to_float_or_none(payload.get("input"))
        cached_price = to_float_or_none(payload.get("cached_input"))
        output_price = to_float_or_none(payload.get("output"))
        if input_price is None or cached_price is None or output_price is None:
            continue
        table[str(model)] = {
            "input": input_price,
            "cached_input": cached_price,
            "output": output_price,
        }
    return table


def direct_token_counts(row: dict[str, Any]) -> dict[str, int]:
    return {
        "input_tokens": to_int(first_present(row, INPUT_KEYS, 0)),
        "cached_tokens": to_int(first_present(row, CACHED_KEYS, 0)),
        "output_tokens": to_int(first_present(row, OUTPUT_KEYS, 0)),
        "reasoning_tokens": to_int(first_present(row, REASONING_KEYS, 0)),
        "tool_tokens": to_int(first_present(row, TOOL_KEYS, 0)),
    }


def has_direct_counts(row: dict[str, Any]) -> bool:
    counts = direct_token_counts(row)
    return any(value != 0 for value in counts.values())


def metric_group_key(row: dict[str, Any], index: int) -> str:
    for key in ("turn_id", "response_id", "traceId", "spanId"):
        value = row.get(key)
        if value:
            return f"{key}:{value}"
    return "|".join(
        [
            "metric",
            str(row.get("timestamp", "no-time")),
            str(row.get("model", "unknown-model")),
            str(row.get("service_name", "unknown-service")),
        ]
    ) or f"metric-row-{index}"


def base_turn_metadata(row: dict[str, Any], source_run_id: str, generated_index: int) -> dict[str, Any]:
    attrs = row.get("attributes") if isinstance(row.get("attributes"), dict) else {}
    mcp_servers = row.get("observed_mcp_servers", attrs.get("observed_mcp_servers", row.get("mcp_servers", attrs.get("mcp_servers", []))))
    if isinstance(mcp_servers, str):
        observed_mcp_servers = [item.strip() for item in mcp_servers.split(",") if item.strip()]
    elif isinstance(mcp_servers, list):
        observed_mcp_servers = [str(item) for item in mcp_servers if str(item)]
    else:
        observed_mcp_servers = []
    observed_count = first_present(row, ("observed_mcp_server_count", "mcp_server_count"), None)
    if observed_count is None:
        observed_count = len(observed_mcp_servers)
    return {
        "source_run_id": first_text(row, ("source_run_id", "run_id", "mode_id"), source_run_id),
        "thread_id": first_text(row, ("thread_id", "session_id", "session_key", "traceId"), source_run_id),
        "turn_id": first_text(row, ("turn_id", "response_id", "spanId"), f"turn-{generated_index:03d}"),
        "turn_index": to_int(first_present(row, ("turn_index", "index"), generated_index), generated_index),
        "timestamp": first_text(row, ("timestamp", "window_start", "start_time"), ""),
        "model": first_text(row, ("model",), "unknown"),
        "reasoning_effort": first_text(row, ("reasoning_effort", "reasoning", "effort"), "unknown"),
        "observed_mcp_server_count": to_int(observed_count, 0),
        "observed_mcp_servers": observed_mcp_servers,
        "enabled_plugins_count": to_int(first_present(row, ("enabled_plugins_count", "plugin_count"), 0), 0),
        "enabled_skills_count": to_int(first_present(row, ("enabled_skills_count", "skill_count"), 0), 0),
        "global_user_instructions_status": first_text(row, ("global_user_instructions_status",), "unknown"),
        "repo_context_status": first_text(row, ("repo_context_status",), "unknown"),
    }


def build_turn_inputs(token_rows: list[dict[str, Any]], sessions_rows: list[dict[str, Any]], source_run_id: str) -> list[dict[str, Any]]:
    direct_rows: list[dict[str, Any]] = []
    metric_groups: OrderedDict[str, dict[str, Any]] = OrderedDict()
    metric_group_first_index: dict[str, int] = {}

    for index, row in enumerate(token_rows, start=1):
        token_type = str(row.get("token_type", "")).strip()
        field_name = TOKEN_TYPE_TO_FIELD.get(token_type)
        value = to_int(row.get("value", row.get("count", 0)), 0)
        if field_name and not has_direct_counts(row):
            key = metric_group_key(row, index)
            if key not in metric_groups:
                metric_groups[key] = {**base_turn_metadata(row, source_run_id, index), **direct_token_counts({})}
                metric_group_first_index[key] = index
            metric_groups[key][field_name] += value
            continue
        direct_rows.append({**base_turn_metadata(row, source_run_id, index), **direct_token_counts(row)})

    turns = direct_rows + list(metric_groups.values())
    if turns:
        turns.sort(key=lambda item: (item.get("timestamp") or "", int(item.get("turn_index") or 0), str(item.get("turn_id") or "")))
        for index, turn in enumerate(turns, start=1):
            if not turn.get("turn_index"):
                turn["turn_index"] = index
        return turns

    # Fallback: if a legacy parser only produced session rows, expose each session row as one aggregate turn.
    fallback: list[dict[str, Any]] = []
    for index, row in enumerate(sessions_rows, start=1):
        fallback.append({**base_turn_metadata(row, source_run_id, index), **direct_token_counts(row)})
    return fallback


def estimate_costs(
    input_tokens: int,
    cached_tokens: int,
    output_tokens: int,
    prices: dict[str, float] | None,
) -> dict[str, float | None]:
    if prices is None:
        return {"input": None, "cached_input": None, "output": None, "total": None}
    non_cached_input_tokens = max(input_tokens - cached_tokens, 0)
    estimated_input_cost_usd = non_cached_input_tokens * prices["input"] / 1_000_000
    estimated_cached_input_cost_usd = cached_tokens * prices["cached_input"] / 1_000_000
    estimated_output_cost_usd = output_tokens * prices["output"] / 1_000_000
    estimated_total_cost_usd = estimated_input_cost_usd + estimated_cached_input_cost_usd + estimated_output_cost_usd
    return {
        "input": estimated_input_cost_usd,
        "cached_input": estimated_cached_input_cost_usd,
        "output": estimated_output_cost_usd,
        "total": estimated_total_cost_usd,
    }


def normalize_turns(turn_inputs: list[dict[str, Any]], prices_by_model: dict[str, dict[str, float]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(turn_inputs, start=1):
        input_tokens = to_int(item.get("input_tokens"), 0)
        cached_tokens = to_int(item.get("cached_tokens"), 0)
        output_tokens = to_int(item.get("output_tokens"), 0)
        warnings: list[str] = []
        non_cached_input_tokens = max(input_tokens - cached_tokens, 0)
        cached_ratio = cached_tokens / input_tokens if input_tokens > 0 else 0
        if cached_tokens > input_tokens:
            warnings.append(
                "cached_tokens is greater than input_tokens; non_cached_input_tokens was clamped to 0"
            )
        model = str(item.get("model") or "unknown")
        prices = prices_by_model.get(model)
        pricing_unknown = prices is None
        if pricing_unknown:
            warnings.append(f"pricing is unknown for model: {model}")
        estimated_cost_usd = estimate_costs(input_tokens, cached_tokens, output_tokens, prices)
        normalized.append(
            {
                "schema_version": SCHEMA_VERSION,
                "source_run_id": str(item.get("source_run_id") or "unknown-run"),
                "thread_id": str(item.get("thread_id") or "unknown-thread"),
                "turn_id": str(item.get("turn_id") or f"turn-{index:03d}"),
                "turn_index": to_int(item.get("turn_index"), index),
                "timestamp": str(item.get("timestamp") or ""),
                "model": model,
                "reasoning_effort": str(item.get("reasoning_effort") or "unknown"),
                "input_tokens": input_tokens,
                "cached_tokens": cached_tokens,
                "non_cached_input_tokens": non_cached_input_tokens,
                "cached_ratio": cached_ratio,
                "output_tokens": output_tokens,
                "reasoning_tokens": to_int(item.get("reasoning_tokens"), 0),
                "tool_tokens": to_int(item.get("tool_tokens"), 0),
                "prices_per_1m": prices,
                "estimated_cost_usd": estimated_cost_usd,
                "observed_mcp_server_count": to_int(item.get("observed_mcp_server_count"), 0),
                "observed_mcp_servers": item.get("observed_mcp_servers") if isinstance(item.get("observed_mcp_servers"), list) else [],
                "enabled_plugins_count": to_int(item.get("enabled_plugins_count"), 0),
                "enabled_skills_count": to_int(item.get("enabled_skills_count"), 0),
                "global_user_instructions_status": str(item.get("global_user_instructions_status") or "unknown"),
                "repo_context_status": str(item.get("repo_context_status") or "unknown"),
                "pricing_unknown": pricing_unknown,
                "warnings": warnings,
                "source_files": ["parsed/token_usage.jsonl"],
            }
        )
    return normalized


def aggregate_sessions(turns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_thread: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for turn in turns:
        by_thread.setdefault(str(turn.get("thread_id") or "unknown-thread"), []).append(turn)

    sessions: list[dict[str, Any]] = []
    for thread_id, thread_turns in by_thread.items():
        models = sorted({str(turn.get("model") or "unknown") for turn in thread_turns})
        reasoning_efforts = sorted({str(turn.get("reasoning_effort") or "unknown") for turn in thread_turns})
        pricing_unknown = any(bool(turn.get("pricing_unknown")) for turn in thread_turns)
        total_cost = None
        if not pricing_unknown:
            total_cost = sum(float(turn["estimated_cost_usd"]["total"] or 0.0) for turn in thread_turns)
        turn_warnings = [warning for turn in thread_turns for warning in turn.get("warnings", [])]
        if len(models) > 1:
            turn_warnings.append("model switch detected in same thread")
        if len(reasoning_efforts) > 1:
            turn_warnings.append("reasoning effort switch detected in same thread")
        sessions.append(
            {
                "thread_id": thread_id,
                "turn_count": len(thread_turns),
                "models": models,
                "reasoning_efforts": reasoning_efforts,
                "total_input_tokens": sum(to_int(turn.get("input_tokens"), 0) for turn in thread_turns),
                "total_cached_tokens": sum(to_int(turn.get("cached_tokens"), 0) for turn in thread_turns),
                "total_non_cached_input_tokens": sum(to_int(turn.get("non_cached_input_tokens"), 0) for turn in thread_turns),
                "average_cached_ratio": (
                    sum(float(turn.get("cached_ratio") or 0.0) for turn in thread_turns) / len(thread_turns)
                    if thread_turns
                    else 0
                ),
                "total_output_tokens": sum(to_int(turn.get("output_tokens"), 0) for turn in thread_turns),
                "total_reasoning_tokens": sum(to_int(turn.get("reasoning_tokens"), 0) for turn in thread_turns),
                "total_tool_tokens": sum(to_int(turn.get("tool_tokens"), 0) for turn in thread_turns),
                "estimated_total_cost_usd": total_cost,
                "model_switch_detected": len(models) > 1,
                "reasoning_switch_detected": len(reasoning_efforts) > 1,
                "warnings": sorted(set(turn_warnings)),
            }
        )
    return sessions


def scan_optional_context(input_root: Path, parsed_dir: Path) -> OptionalContext:
    context = OptionalContext()
    search_roots = []
    for path in (input_root, parsed_dir, parsed_dir.parent):
        if path not in search_roots:
            search_roots.append(path)

    for filename in OPTIONAL_EXACT_FILES:
        found = next((root / filename for root in search_roots if (root / filename).exists()), None)
        if not found:
            context.missing_warnings.append(f"optional file missing: {filename}")
            continue
        try:
            context.summaries[filename] = read_json(found)
            context.loaded_files.append(str(found))
        except (OSError, json.JSONDecodeError) as exc:
            context.warnings.append(f"optional file unreadable: {found}: {exc}")

    for pattern, group_name in OPTIONAL_GLOB_GROUPS:
        matches: list[Path] = []
        for root in search_roots:
            matches.extend(sorted(root.glob(pattern)))
        matches = [path for path in matches if path.name not in {"session_summary.json", "token_cost_summary.json"}]
        if not matches:
            context.missing_warnings.append(f"optional file group missing: {pattern}")
            continue
        for path in matches:
            try:
                context.summaries[f"{group_name}:{path.name}"] = read_json(path)
                context.loaded_files.append(str(path))
            except (OSError, json.JSONDecodeError) as exc:
                context.warnings.append(f"optional file unreadable: {path}: {exc}")
    return context


def read_required_or_warn_json(path: Path, warnings: list[str]) -> Any:
    if not path.exists():
        warnings.append(f"expected parsed file missing: {path.name}")
        return None
    try:
        return read_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        warnings.append(f"expected parsed file unreadable: {path.name}: {exc}")
        return None


def read_required_or_warn_jsonl(path: Path, warnings: list[str]) -> list[dict[str, Any]]:
    if not path.exists():
        warnings.append(f"expected parsed file missing: {path.name}")
        return []
    try:
        return read_jsonl(path)
    except (OSError, json.JSONDecodeError) as exc:
        warnings.append(f"expected parsed file unreadable: {path.name}: {exc}")
        return []


def build_summary(
    turns: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
    global_warnings: list[str],
    optional_context: OptionalContext,
    source_files: list[str],
) -> dict[str, Any]:
    pricing_unknown = any(bool(turn.get("pricing_unknown")) for turn in turns)
    estimated_total_cost = None
    if not pricing_unknown:
        estimated_total_cost = sum(float(turn["estimated_cost_usd"]["total"] or 0.0) for turn in turns)
    return {
        "schema_version": SCHEMA_VERSION,
        "turn_count": len(turns),
        "session_count": len(sessions),
        "total_input_tokens": sum(to_int(turn.get("input_tokens"), 0) for turn in turns),
        "total_cached_tokens": sum(to_int(turn.get("cached_tokens"), 0) for turn in turns),
        "total_non_cached_input_tokens": sum(to_int(turn.get("non_cached_input_tokens"), 0) for turn in turns),
        "average_cached_ratio": (sum(float(turn.get("cached_ratio") or 0.0) for turn in turns) / len(turns) if turns else 0),
        "total_output_tokens": sum(to_int(turn.get("output_tokens"), 0) for turn in turns),
        "total_reasoning_tokens": sum(to_int(turn.get("reasoning_tokens"), 0) for turn in turns),
        "total_tool_tokens": sum(to_int(turn.get("tool_tokens"), 0) for turn in turns),
        "estimated_total_cost_usd": estimated_total_cost,
        "pricing_unknown_turn_count": sum(1 for turn in turns if turn.get("pricing_unknown")),
        "model_switch_thread_count": sum(1 for session in sessions if session.get("model_switch_detected")),
        "reasoning_switch_thread_count": sum(1 for session in sessions if session.get("reasoning_switch_detected")),
        "warnings": sorted(set(global_warnings + optional_context.missing_warnings + optional_context.warnings + [warning for turn in turns for warning in turn.get("warnings", [])])),
        "optional_loaded_files": optional_context.loaded_files,
        "source_files": source_files,
    }


def money(value: Any) -> str:
    if value is None:
        return "unknown"
    return f"{float(value):.8f}"


def ratio(value: Any) -> str:
    try:
        return f"{float(value):.4f}"
    except (TypeError, ValueError):
        return "0.0000"


def build_report(summary: dict[str, Any], turns: list[dict[str, Any]], sessions: list[dict[str, Any]], input_dir: Path) -> list[str]:
    lines = [
        "# Token Cost Report",
        "",
        "Кодировка файла: UTF-8 с BOM. Это сделано специально, чтобы обычные Windows-редакторы корректно открывали русский текст.",
        "",
        "## Цель",
        "",
        "Нормализовать parsed token usage в cache-adjusted cost view: отдельно показать raw input, cached input, non-cached input, output/reasoning/tool tokens и приблизительную стоимость по параметризованному pricing config.",
        "",
        "## Входные данные",
        "",
        f"- Input dir: `{input_dir}`",
        "- Основной вход: `parsed/token_usage.jsonl`",
        "- Дополнительные входы: `parsed/session_summary.json`, `parsed/sessions.jsonl`, optional compare/confirmation/summary JSON files.",
        "- Если optional files отсутствуют, это warning, а не crash.",
        "",
        "## Summary table",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Turns | {summary['turn_count']} |",
        f"| Sessions | {summary['session_count']} |",
        f"| Total input tokens | {summary['total_input_tokens']} |",
        f"| Total cached tokens | {summary['total_cached_tokens']} |",
        f"| Total non-cached input tokens | {summary['total_non_cached_input_tokens']} |",
        f"| Average cached ratio | {ratio(summary['average_cached_ratio'])} |",
        f"| Total output tokens | {summary['total_output_tokens']} |",
        f"| Total reasoning tokens | {summary['total_reasoning_tokens']} |",
        f"| Total tool tokens | {summary['total_tool_tokens']} |",
        f"| Estimated total cost USD | {money(summary['estimated_total_cost_usd'])} |",
        f"| Pricing unknown turns | {summary['pricing_unknown_turn_count']} |",
        "",
        "## Turns table",
        "",
        "| Thread | Turn | Model | Effort | Input | Cached | Non-cached | Cache ratio | Output | Reasoning | Tool | Est. total USD | Warnings |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for turn in turns:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(turn.get("thread_id", "")),
                    str(turn.get("turn_id", "")),
                    str(turn.get("model", "")),
                    str(turn.get("reasoning_effort", "")),
                    str(turn.get("input_tokens", 0)),
                    str(turn.get("cached_tokens", 0)),
                    str(turn.get("non_cached_input_tokens", 0)),
                    ratio(turn.get("cached_ratio")),
                    str(turn.get("output_tokens", 0)),
                    str(turn.get("reasoning_tokens", 0)),
                    str(turn.get("tool_tokens", 0)),
                    money(turn.get("estimated_cost_usd", {}).get("total")),
                    "; ".join(turn.get("warnings", [])) or "-",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Sessions table",
            "",
            "| Thread | Turns | Models | Efforts | Input | Cached | Non-cached | Avg cache ratio | Output | Reasoning | Tool | Est. total USD | Switches |",
            "|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for session in sessions:
        switches = []
        if session.get("model_switch_detected"):
            switches.append("model")
        if session.get("reasoning_switch_detected"):
            switches.append("reasoning")
        lines.append(
            "| "
            + " | ".join(
                [
                    str(session.get("thread_id", "")),
                    str(session.get("turn_count", 0)),
                    ", ".join(session.get("models", [])),
                    ", ".join(session.get("reasoning_efforts", [])),
                    str(session.get("total_input_tokens", 0)),
                    str(session.get("total_cached_tokens", 0)),
                    str(session.get("total_non_cached_input_tokens", 0)),
                    ratio(session.get("average_cached_ratio")),
                    str(session.get("total_output_tokens", 0)),
                    str(session.get("total_reasoning_tokens", 0)),
                    str(session.get("total_tool_tokens", 0)),
                    money(session.get("estimated_total_cost_usd")),
                    ", ".join(switches) or "-",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Простая интерпретация",
            "",
            "- `input_tokens` показывает общий входной контекст, но не равен реальной цене, если значительная часть входа cached.",
            "- `non_cached_input_tokens` ближе к реально дорогой части входа: это `max(input_tokens - cached_tokens, 0)`.",
            "- Высокий `cached_ratio` обычно означает, что повторные ходы могут быть дешевле первого, но это нужно смотреть вместе с output cost.",
            "- Если внутри одного thread меняется model или reasoning effort, такой thread помечается switch-флагом и не должен сравниваться как стабильный baseline.",
            "- Если pricing для model неизвестен, стоимость оставлена `unknown`, а не подменена выдуманными числами.",
            "",
            "## Warnings",
            "",
        ]
    )
    if summary.get("warnings"):
        for warning in summary["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- Предупреждений нет.")
    return lines


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_root = Path(args.input_dir).resolve()
    parsed_dir = resolve_parsed_dir(input_root)
    out_dir = Path(args.out_dir).resolve()
    pricing_path = Path(args.pricing).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    global_warnings: list[str] = []
    source_files: list[str] = []

    if not pricing_path.exists():
        raise SystemExit(f"Pricing file not found: {pricing_path}")
    prices_by_model = pricing_table(read_json(pricing_path))
    source_files.append(str(pricing_path))

    token_usage_path = parsed_dir / "token_usage.jsonl"
    session_summary_path = parsed_dir / "session_summary.json"
    sessions_path = parsed_dir / "sessions.jsonl"

    token_rows = read_required_or_warn_jsonl(token_usage_path, global_warnings)
    if token_usage_path.exists():
        source_files.append("parsed/token_usage.jsonl")
    session_summary = read_required_or_warn_json(session_summary_path, global_warnings)
    if session_summary_path.exists():
        source_files.append("parsed/session_summary.json")
    sessions_rows = read_required_or_warn_jsonl(sessions_path, global_warnings)
    if sessions_path.exists():
        source_files.append("parsed/sessions.jsonl")

    source_run_id = input_root.name or "unknown-run"
    if isinstance(session_summary, dict):
        source_run_id = str(session_summary.get("source_run_id") or session_summary.get("run_id") or source_run_id)

    optional_context = scan_optional_context(input_root, parsed_dir)
    turn_inputs = build_turn_inputs(token_rows, sessions_rows, source_run_id)
    turns = normalize_turns(turn_inputs, prices_by_model)
    sessions = aggregate_sessions(turns)
    summary = build_summary(turns, sessions, global_warnings, optional_context, source_files)

    write_jsonl(out_dir / "token_cost_turns.jsonl", turns)
    write_json(out_dir / "token_cost_sessions.json", {"schema_version": SCHEMA_VERSION, "sessions": sessions})
    write_json(out_dir / "token_cost_summary.json", summary)
    write_markdown(out_dir / "token_cost_report.md", build_report(summary, turns, sessions, input_root))
    write_json(
        out_dir / "token_cost_dashboard_data.json",
        {
            "schema_version": SCHEMA_VERSION,
            "summary": summary,
            "turns": turns,
            "sessions": sessions,
        },
    )
    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Future file: `config/token_pricing.json`

```json
{
  "schema_version": 1,
  "currency": "USD",
  "unit": "per_1m_tokens",
  "prices_per_1m": {
    "gpt-5.5": {
      "input": 5.0,
      "cached_input": 0.5,
      "output": 30.0
    },
    "gpt-5.4": {
      "input": 2.5,
      "cached_input": 0.25,
      "output": 15.0
    },
    "gpt-5.4-mini": {
      "input": 0.75,
      "cached_input": 0.075,
      "output": 4.5
    }
  }
}
```

## Future file: `tests/test_codex_token_cost_normalizer.py`

```python
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "codex_token_cost_normalizer.py"
SPEC = importlib.util.spec_from_file_location("codex_token_cost_normalizer", SCRIPT_PATH)
normalizer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = normalizer
SPEC.loader.exec_module(normalizer)


PRICING = {
    "schema_version": 1,
    "currency": "USD",
    "unit": "per_1m_tokens",
    "prices_per_1m": {
        "gpt-5.5": {"input": 5.0, "cached_input": 0.5, "output": 30.0},
        "gpt-5.4": {"input": 2.5, "cached_input": 0.25, "output": 15.0},
        "gpt-5.4-mini": {"input": 0.75, "cached_input": 0.075, "output": 4.5},
    },
}


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


class TokenCostNormalizerTests(unittest.TestCase):
    def make_fixture(self, rows: list[dict[str, object]], include_optional: bool = False) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        parsed = root / "parsed"
        parsed.mkdir(parents=True)
        write_jsonl(parsed / "token_usage.jsonl", rows)
        write_json(parsed / "session_summary.json", {"source_run_id": "fixture-run"})
        write_jsonl(parsed / "sessions.jsonl", [])
        pricing = root / "token_pricing.json"
        write_json(pricing, PRICING)
        if include_optional:
            write_json(root / "compare_summary.json", {"ok": True})
            write_json(root / "lean_confirmation_summary.json", {"ok": True})
        out_dir = root / "out"
        return temp, root, pricing, out_dir

    def run_normalizer(self, rows: list[dict[str, object]], include_optional: bool = False) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp, root, pricing, out_dir = self.make_fixture(rows, include_optional=include_optional)
        result = normalizer.main(["--input-dir", str(root), "--out-dir", str(out_dir), "--pricing", str(pricing)])
        self.assertEqual(result, 0)
        return temp, out_dir

    def read_turns(self, out_dir: Path) -> list[dict[str, object]]:
        return [json.loads(line) for line in (out_dir / "token_cost_turns.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]

    def read_sessions(self, out_dir: Path) -> dict[str, object]:
        return json.loads((out_dir / "token_cost_sessions.json").read_text(encoding="utf-8"))

    def read_summary(self, out_dir: Path) -> dict[str, object]:
        return json.loads((out_dir / "token_cost_summary.json").read_text(encoding="utf-8"))

    def test_known_pricing_formula(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "thread-1",
                    "turn_id": "t1",
                    "turn_index": 1,
                    "model": "gpt-5.5",
                    "reasoning_effort": "medium",
                    "input_tokens": 1000,
                    "cached_tokens": 200,
                    "output_tokens": 100,
                    "reasoning_tokens": 7,
                    "tool_tokens": 3,
                }
            ],
            include_optional=True,
        )
        self.addCleanup(temp.cleanup)
        turn = self.read_turns(out_dir)[0]
        self.assertEqual(turn["non_cached_input_tokens"], 800)
        self.assertAlmostEqual(turn["cached_ratio"], 0.2)
        self.assertAlmostEqual(turn["estimated_cost_usd"]["input"], 800 * 5.0 / 1_000_000)
        self.assertAlmostEqual(turn["estimated_cost_usd"]["cached_input"], 200 * 0.5 / 1_000_000)
        self.assertAlmostEqual(turn["estimated_cost_usd"]["output"], 100 * 30.0 / 1_000_000)
        self.assertAlmostEqual(turn["estimated_cost_usd"]["total"], 0.0071)
        self.assertFalse(turn["pricing_unknown"])

    def test_unknown_pricing(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "thread-1",
                    "turn_id": "t1",
                    "model": "gpt-unknown",
                    "input_tokens": 100,
                    "cached_tokens": 10,
                    "output_tokens": 20,
                }
            ]
        )
        self.addCleanup(temp.cleanup)
        turn = self.read_turns(out_dir)[0]
        self.assertTrue(turn["pricing_unknown"])
        self.assertIsNone(turn["prices_per_1m"])
        self.assertIsNone(turn["estimated_cost_usd"]["total"])
        self.assertTrue(any("pricing is unknown" in warning for warning in turn["warnings"]))

    def test_cached_greater_than_input_warns_and_clamps(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "thread-1",
                    "turn_id": "t1",
                    "model": "gpt-5.5",
                    "input_tokens": 100,
                    "cached_tokens": 150,
                    "output_tokens": 10,
                }
            ]
        )
        self.addCleanup(temp.cleanup)
        turn = self.read_turns(out_dir)[0]
        self.assertEqual(turn["non_cached_input_tokens"], 0)
        self.assertAlmostEqual(turn["cached_ratio"], 1.5)
        self.assertTrue(any("cached_tokens is greater" in warning for warning in turn["warnings"]))

    def test_same_thread_session_aggregation(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {"thread_id": "same", "turn_id": "t1", "model": "gpt-5.5", "reasoning_effort": "low", "input_tokens": 100, "cached_tokens": 10, "output_tokens": 5, "reasoning_tokens": 1, "tool_tokens": 0},
                {"thread_id": "same", "turn_id": "t2", "model": "gpt-5.5", "reasoning_effort": "low", "input_tokens": 200, "cached_tokens": 40, "output_tokens": 15, "reasoning_tokens": 2, "tool_tokens": 3},
            ],
            include_optional=True,
        )
        self.addCleanup(temp.cleanup)
        sessions = self.read_sessions(out_dir)["sessions"]
        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertEqual(session["turn_count"], 2)
        self.assertEqual(session["total_input_tokens"], 300)
        self.assertEqual(session["total_cached_tokens"], 50)
        self.assertEqual(session["total_non_cached_input_tokens"], 250)
        self.assertEqual(session["total_output_tokens"], 20)
        self.assertEqual(session["total_reasoning_tokens"], 3)
        self.assertEqual(session["total_tool_tokens"], 3)
        self.assertFalse(session["model_switch_detected"])
        self.assertFalse(session["reasoning_switch_detected"])

    def test_model_switch_in_same_thread(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {"thread_id": "same", "turn_id": "t1", "model": "gpt-5.5", "reasoning_effort": "low", "input_tokens": 100, "cached_tokens": 10, "output_tokens": 5},
                {"thread_id": "same", "turn_id": "t2", "model": "gpt-5.4", "reasoning_effort": "low", "input_tokens": 100, "cached_tokens": 10, "output_tokens": 5},
            ],
            include_optional=True,
        )
        self.addCleanup(temp.cleanup)
        session = self.read_sessions(out_dir)["sessions"][0]
        self.assertTrue(session["model_switch_detected"])
        self.assertIn("gpt-5.5", session["models"])
        self.assertIn("gpt-5.4", session["models"])
        self.assertTrue(any("model switch" in warning for warning in session["warnings"]))

    def test_missing_optional_files_without_crash(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {"thread_id": "thread-1", "turn_id": "t1", "model": "gpt-5.5", "input_tokens": 10, "cached_tokens": 0, "output_tokens": 1}
            ],
            include_optional=False,
        )
        self.addCleanup(temp.cleanup)
        summary = self.read_summary(out_dir)
        self.assertEqual(summary["turn_count"], 1)
        self.assertTrue(any("optional file" in warning for warning in summary["warnings"]))


if __name__ == "__main__":
    unittest.main()
```

## Documentation update instructions for later Kilo apply/run

These are exact update instructions. They must be applied later by Kilo after materializing the future files above. This V3 package must not directly update these live docs.

### `.ai/subprojects/tokken_dashboard/tokken_dashboard_journal.md`

Add a new journal entry under `## Записи` and add its anchor to Quick Navigation.

Suggested entry:

```markdown
### J-20260605-002 - Token Cost Normalizer v1 materialized

- Этап жизненного цикла: `Stage 1 - cache-adjusted cost normalization`
- Роль: `Kilo Notebook V3 apply/run`
- Маршрут выполнения: `V3 package -> local materialization -> verification`
- Source package: `V3-20260605-141503-token-cost-normalizer-v1`
- Related decisions:
  - [D-20260604-009](./tokken_dashboard_decisions.md#d-20260604-009)
- Созданные файлы:
  - `scripts/codex_token_cost_normalizer.py`
  - `config/token_pricing.json`
  - `tests/test_codex_token_cost_normalizer.py`
- Суть результата:
  - добавлен слой нормализации parsed token usage в cache-adjusted cost artifacts;
  - считаются `cached_tokens`, `non_cached_input_tokens`, `cached_ratio`, output/reasoning/tool tokens и estimated USD cost;
  - unknown model pricing не подменяется выдуманными числами;
  - `cached_tokens > input_tokens` фиксируется warning-ом, а non-cached input clamp-ится до `0`.
- Проверка:
  - `python -m unittest tests.test_codex_token_cost_normalizer tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment`
  - `git diff --check`
- Баги и сложности:
  - Заполнить по фактическому local run Kilo: `not found`, `found and fixed`, `still open` или `pending human check`.
- Human Check:
  - `suggested`
  - Открыть будущий `token_cost_report.md` на локальных parsed данных и проверить, что русский текст читается нормально в обычном Windows-редакторе.
```

### `.ai/subprojects/tokken_dashboard/tokken_dashboard_navigation.md`

Add links to the new draft pack and future materialized files after Kilo applies them.

Suggested navigation block:

```markdown
### Token Cost Normalizer v1

- Draft implementation pack: [`drafts/token_cost_normalizer_v1_implementation_pack.md`](./drafts/token_cost_normalizer_v1_implementation_pack.md)
- Future script after materialization: [`scripts/codex_token_cost_normalizer.py`](../../../scripts/codex_token_cost_normalizer.py)
- Future pricing config after materialization: [`config/token_pricing.json`](../../../config/token_pricing.json)
- Future tests after materialization: [`tests/test_codex_token_cost_normalizer.py`](../../../tests/test_codex_token_cost_normalizer.py)

Purpose: cache-adjusted token/cost normalization layer over sanitized parser outputs.
```

If relative links are inconsistent with the existing navigation style, preserve the existing style and use plain code paths instead.

### `.ai/subprojects/tokken_dashboard/tokken_dashboard_readme.md`

Add a short section describing the layer.

Suggested section:

```markdown
## Token Cost Normalizer v1

`Token Cost Normalizer v1` is the next local layer after the sanitized Codex token parser and comparison tools.

It reads parsed artifacts such as:

- `parsed/token_usage.jsonl`
- `parsed/session_summary.json`
- `parsed/sessions.jsonl`
- optional nearby compare/confirmation summary JSON files

It writes cache-adjusted cost artifacts:

- `token_cost_turns.jsonl`
- `token_cost_sessions.json`
- `token_cost_summary.json`
- `token_cost_report.md`
- `token_cost_dashboard_data.json`

Important interpretation rule: future token comparisons must not use raw `input_tokens` alone. They must check `cached_tokens`, `non_cached_input_tokens`, `cached_ratio`, output/reasoning/tool tokens, model/reasoning switches and estimated cost from `config/token_pricing.json`.

Unknown model pricing is intentionally left unknown. The normalizer must not invent prices.
```

### `.ai/subprojects/tokken_dashboard/tokken_dashboard_decisions.md`

A new decision is not strictly required because `D-20260604-009` already establishes the cache-adjusted and cost-adjusted interpretation rule.

If Codex/human decide to record materialization as a stable accepted implementation rule, add:

```markdown
### D-20260605-002 - Token Cost Normalizer v1 is the canonical cache-adjusted cost layer

- Status: `accepted`
- Source: `V3-20260605-141503-token-cost-normalizer-v1 local apply/run`
- Decision: `scripts/codex_token_cost_normalizer.py` is the canonical local layer for converting sanitized parser outputs into cache-adjusted token cost artifacts.
- Reason: reports based only on raw `input_tokens` are misleading when cached input, model pricing, output tokens, reasoning tokens and model/reasoning switches matter.
- Consequence: future dashboard/report work should consume `token_cost_turns.jsonl`, `token_cost_sessions.json`, `token_cost_summary.json` and `token_cost_dashboard_data.json` instead of re-implementing cost formulas ad hoc.
- Boundary: pricing remains config-driven in `config/token_pricing.json`; unknown models must remain `pricing_unknown` with null estimated cost fields.
- Human approval: `pending local review`
```

## Exact verification commands for later Kilo run

V3 does not run these tests now. Kilo runs them later after local materialization.

```bash
python -m unittest tests.test_codex_token_cost_normalizer tests.test_mcp_schema_inventory tests.test_tool_mcp_activity_inspector tests.test_codex_otel_compare tests.test_codex_token_debugger tests.test_codex_otel_ab_experiment
git diff --check
```

## Human Check

`recommended after local materialization`

Простой human check после Kilo apply/run:

1. Открыть будущий `token_cost_report.md` в обычном Windows-редакторе.
2. Проверить, что русский текст читается без кракозябр.
3. Проверить в таблице, что есть колонки `Input`, `Cached`, `Non-cached`, `Cache ratio`, `Est. total USD`.
4. Если pricing неизвестен для модели, убедиться, что стоимость показана как `unknown`, а не как выдуманная цена.

## Баги и сложности

Для этого external artifact package:

- bugs found: not found during package assembly;
- tests: not run by V3 external artifact generation;
- remaining risk: Kilo must verify syntax/tests after local materialization because this package intentionally does not create live `scripts/`, `config/`, or `tests/` files directly.
