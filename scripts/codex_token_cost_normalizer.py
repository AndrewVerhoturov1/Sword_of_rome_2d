#!/usr/bin/env python3
"""Normalize parsed Codex token telemetry into cache-adjusted cost artifacts."""
from __future__ import annotations

import argparse
import json
from collections import OrderedDict
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
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Input dir containing parsed/ outputs or the parsed dir itself.",
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Output dir for token cost artifacts.",
    )
    parser.add_argument(
        "--pricing",
        required=True,
        help="Path to config/token_pricing.json.",
    )
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
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_markdown(path: Path, lines: list[str]) -> None:
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
    return any(value != 0 for value in direct_token_counts(row).values())


def metric_group_key(row: dict[str, Any], index: int) -> str:
    for key in ("turn_id", "response_id", "traceId", "spanId"):
        value = row.get(key)
        if value:
            return f"{key}:{value}"
    parts = [
        "metric",
        str(row.get("timestamp", "no-time")),
        str(row.get("model", "unknown-model")),
        str(row.get("service_name", "unknown-service")),
    ]
    return "|".join(parts) or f"metric-row-{index}"


def observed_mcp_servers_from_row(row: dict[str, Any]) -> list[str]:
    value = first_present(
        row,
        ("observed_mcp_servers", "mcp_servers"),
        [],
    )
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return []


def base_turn_metadata(row: dict[str, Any], source_run_id: str, generated_index: int) -> dict[str, Any]:
    servers = observed_mcp_servers_from_row(row)
    observed_count = first_present(row, ("observed_mcp_server_count", "mcp_server_count"))
    if observed_count is None:
        observed_count = len(servers)
    return {
        "source_run_id": first_text(row, ("source_run_id", "run_id", "mode_id"), source_run_id),
        "thread_id": first_text(
            row,
            ("thread_id", "session_id", "session_key", "traceId"),
            source_run_id,
        ),
        "turn_id": first_text(row, ("turn_id", "response_id", "spanId"), f"turn-{generated_index:03d}"),
        "turn_index": to_int(first_present(row, ("turn_index", "index"), generated_index), generated_index),
        "timestamp": first_text(row, ("timestamp", "window_start", "start_time"), ""),
        "model": first_text(row, ("model",), "unknown"),
        "reasoning_effort": first_text(row, ("reasoning_effort", "reasoning", "effort"), "unknown"),
        "observed_mcp_server_count": to_int(observed_count, 0),
        "observed_mcp_servers": servers,
        "enabled_plugins_count": to_int(first_present(row, ("enabled_plugins_count", "plugin_count"), 0), 0),
        "enabled_skills_count": to_int(first_present(row, ("enabled_skills_count", "skill_count"), 0), 0),
        "global_user_instructions_status": first_text(row, ("global_user_instructions_status",), "unknown"),
        "repo_context_status": first_text(row, ("repo_context_status",), "unknown"),
    }


def build_turn_inputs(
    token_rows: list[dict[str, Any]],
    sessions_rows: list[dict[str, Any]],
    source_run_id: str,
) -> list[dict[str, Any]]:
    direct_rows: list[dict[str, Any]] = []
    metric_groups: OrderedDict[str, dict[str, Any]] = OrderedDict()

    for index, row in enumerate(token_rows, start=1):
        token_type = str(row.get("token_type", "")).strip()
        field_name = TOKEN_TYPE_TO_FIELD.get(token_type)
        value = to_int(row.get("value", row.get("count", 0)), 0)
        if field_name and not has_direct_counts(row):
            key = metric_group_key(row, index)
            if key not in metric_groups:
                metric_groups[key] = {
                    **base_turn_metadata(row, source_run_id, index),
                    **direct_token_counts({}),
                }
            metric_groups[key][field_name] += value
            continue
        direct_rows.append(
            {
                **base_turn_metadata(row, source_run_id, index),
                **direct_token_counts(row),
            }
        )

    turns = direct_rows + list(metric_groups.values())
    if turns:
        turns.sort(
            key=lambda item: (
                item.get("timestamp") or "",
                int(item.get("turn_index") or 0),
                str(item.get("turn_id") or ""),
            )
        )
        for index, turn in enumerate(turns, start=1):
            if not turn.get("turn_index"):
                turn["turn_index"] = index
        return turns

    fallback: list[dict[str, Any]] = []
    for index, row in enumerate(sessions_rows, start=1):
        fallback.append(
            {
                **base_turn_metadata(row, source_run_id, index),
                **direct_token_counts(row),
            }
        )
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
    estimated_total_cost_usd = (
        estimated_input_cost_usd + estimated_cached_input_cost_usd + estimated_output_cost_usd
    )
    return {
        "input": estimated_input_cost_usd,
        "cached_input": estimated_cached_input_cost_usd,
        "output": estimated_output_cost_usd,
        "total": estimated_total_cost_usd,
    }


def normalize_turns(
    turn_inputs: list[dict[str, Any]],
    prices_by_model: dict[str, dict[str, float]],
) -> list[dict[str, Any]]:
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
                "estimated_cost_usd": estimate_costs(input_tokens, cached_tokens, output_tokens, prices),
                "observed_mcp_server_count": to_int(item.get("observed_mcp_server_count"), 0),
                "observed_mcp_servers": item.get("observed_mcp_servers")
                if isinstance(item.get("observed_mcp_servers"), list)
                else [],
                "enabled_plugins_count": to_int(item.get("enabled_plugins_count"), 0),
                "enabled_skills_count": to_int(item.get("enabled_skills_count"), 0),
                "global_user_instructions_status": str(
                    item.get("global_user_instructions_status") or "unknown"
                ),
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
        efforts = sorted({str(turn.get("reasoning_effort") or "unknown") for turn in thread_turns})
        pricing_unknown = any(bool(turn.get("pricing_unknown")) for turn in thread_turns)
        total_cost = None
        if not pricing_unknown:
            total_cost = sum(float(turn["estimated_cost_usd"]["total"] or 0.0) for turn in thread_turns)
        warnings = [warning for turn in thread_turns for warning in turn.get("warnings", [])]
        if len(models) > 1:
            warnings.append("model switch detected in same thread")
        if len(efforts) > 1:
            warnings.append("reasoning effort switch detected in same thread")
        sessions.append(
            {
                "thread_id": thread_id,
                "turn_count": len(thread_turns),
                "models": models,
                "reasoning_efforts": efforts,
                "total_input_tokens": sum(to_int(turn.get("input_tokens"), 0) for turn in thread_turns),
                "total_cached_tokens": sum(to_int(turn.get("cached_tokens"), 0) for turn in thread_turns),
                "total_non_cached_input_tokens": sum(
                    to_int(turn.get("non_cached_input_tokens"), 0) for turn in thread_turns
                ),
                "average_cached_ratio": (
                    sum(float(turn.get("cached_ratio") or 0.0) for turn in thread_turns) / len(thread_turns)
                    if thread_turns
                    else 0
                ),
                "total_output_tokens": sum(to_int(turn.get("output_tokens"), 0) for turn in thread_turns),
                "total_reasoning_tokens": sum(
                    to_int(turn.get("reasoning_tokens"), 0) for turn in thread_turns
                ),
                "total_tool_tokens": sum(to_int(turn.get("tool_tokens"), 0) for turn in thread_turns),
                "estimated_total_cost_usd": total_cost,
                "model_switch_detected": len(models) > 1,
                "reasoning_switch_detected": len(efforts) > 1,
                "warnings": sorted(set(warnings)),
            }
        )
    return sessions


def scan_optional_context(input_root: Path, parsed_dir: Path) -> OptionalContext:
    context = OptionalContext()
    search_roots: list[Path] = []
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
        matches = [
            path for path in matches if path.name not in {"session_summary.json", "token_cost_summary.json"}
        ]
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
    models = sorted({str(turn.get("model") or "unknown") for turn in turns})
    unknown_pricing_turns = sum(1 for turn in turns if turn.get("pricing_unknown"))
    total_estimated_cost = None
    if unknown_pricing_turns == 0:
        total_estimated_cost = sum(float(turn["estimated_cost_usd"]["total"] or 0.0) for turn in turns)
    warnings = list(global_warnings)
    warnings.extend(optional_context.missing_warnings)
    warnings.extend(optional_context.warnings)
    warnings.extend(
        warning
        for turn in turns
        for warning in turn.get("warnings", [])
        if warning not in warnings
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "turn_count": len(turns),
        "session_count": len(sessions),
        "models": models,
        "total_input_tokens": sum(to_int(turn.get("input_tokens"), 0) for turn in turns),
        "total_cached_tokens": sum(to_int(turn.get("cached_tokens"), 0) for turn in turns),
        "total_non_cached_input_tokens": sum(
            to_int(turn.get("non_cached_input_tokens"), 0) for turn in turns
        ),
        "average_cached_ratio": (
            sum(float(turn.get("cached_ratio") or 0.0) for turn in turns) / len(turns) if turns else 0
        ),
        "total_output_tokens": sum(to_int(turn.get("output_tokens"), 0) for turn in turns),
        "total_reasoning_tokens": sum(to_int(turn.get("reasoning_tokens"), 0) for turn in turns),
        "total_tool_tokens": sum(to_int(turn.get("tool_tokens"), 0) for turn in turns),
        "unknown_pricing_turn_count": unknown_pricing_turns,
        "estimated_total_cost_usd": total_estimated_cost,
        "source_files": source_files,
        "optional_context": {
            "loaded_files": optional_context.loaded_files,
            "missing_warnings": optional_context.missing_warnings,
            "warnings": optional_context.warnings,
        },
        "warnings": warnings,
    }


def build_report(
    summary: dict[str, Any],
    turns: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
    input_root: Path,
) -> list[str]:
    lines = [
        "# Token Cost Report",
        "",
        "## Что это",
        "",
        "Локальный отчёт по нормализации token telemetry в cache-adjusted cost view.",
        "",
        "## Вход",
        "",
        f"- input dir: `{input_root}`",
        f"- turn count: `{summary['turn_count']}`",
        f"- session count: `{summary['session_count']}`",
        f"- models: `{', '.join(summary['models']) if summary['models'] else 'none'}`",
        "",
        "## Сводка",
        "",
        f"- input tokens: `{summary['total_input_tokens']}`",
        f"- cached tokens: `{summary['total_cached_tokens']}`",
        f"- non-cached input tokens: `{summary['total_non_cached_input_tokens']}`",
        f"- average cached ratio: `{summary['average_cached_ratio']:.4f}`",
        f"- output tokens: `{summary['total_output_tokens']}`",
        f"- reasoning tokens: `{summary['total_reasoning_tokens']}`",
        f"- tool tokens: `{summary['total_tool_tokens']}`",
        f"- unknown pricing turns: `{summary['unknown_pricing_turn_count']}`",
        f"- estimated total cost usd: `{summary['estimated_total_cost_usd']}`",
        "",
        "## Ходы",
        "",
    ]
    for turn in turns:
        lines.extend(
            [
                f"### Turn `{turn['turn_id']}`",
                "",
                f"- model: `{turn['model']}`",
                f"- reasoning effort: `{turn['reasoning_effort']}`",
                f"- input tokens: `{turn['input_tokens']}`",
                f"- cached tokens: `{turn['cached_tokens']}`",
                f"- non-cached input tokens: `{turn['non_cached_input_tokens']}`",
                f"- cached ratio: `{turn['cached_ratio']:.4f}`",
                f"- output tokens: `{turn['output_tokens']}`",
                f"- reasoning tokens: `{turn['reasoning_tokens']}`",
                f"- tool tokens: `{turn['tool_tokens']}`",
                f"- estimated total cost usd: `{turn['estimated_cost_usd']['total']}`",
                "",
            ]
        )
    lines.extend(["## Сессии", ""])
    for session in sessions:
        lines.extend(
            [
                f"### Session `{session['thread_id']}`",
                "",
                f"- turn count: `{session['turn_count']}`",
                f"- models: `{', '.join(session['models'])}`",
                f"- reasoning efforts: `{', '.join(session['reasoning_efforts'])}`",
                f"- model switch: `{session['model_switch_detected']}`",
                f"- reasoning switch: `{session['reasoning_switch_detected']}`",
                f"- estimated total cost usd: `{session['estimated_total_cost_usd']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Интерпретация",
            "",
            "- Смотреть нужно не только на raw `input_tokens`, но и на `cached_tokens`, `non_cached_input_tokens` и `cached_ratio`.",
            "- Высокий `cached_ratio` часто означает, что повторные ходы дешевле первого, но output cost всё равно важен.",
            "- Если внутри одного thread меняются model или reasoning effort, такой thread нельзя считать стабильным baseline без пометки про switch.",
            "- Если pricing для модели неизвестен, стоимость остаётся `unknown`, а не подменяется выдуманными числами.",
            "",
            "## Warnings",
            "",
        ]
    )
    if summary["warnings"]:
        lines.extend([f"- {warning}" for warning in summary["warnings"]])
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
