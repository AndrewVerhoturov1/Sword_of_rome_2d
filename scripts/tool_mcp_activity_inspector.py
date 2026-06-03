#!/usr/bin/env python3
"""
Build a local Tool/MCP Activity Inspector from sanitized Codex OTel outputs.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


PRIVATE_ID_FIELDS = {
    "user.email",
    "user.account_id",
    "conversation.id",
    "host.name",
}

SENSITIVE_FIELD_FRAGMENTS = (
    "authorization",
    "proxy-authorization",
    "x-api-key",
    "api-key",
    "api_key",
    "secret",
    "password",
    "cookie",
    "set-cookie",
    "access_token",
    "refresh_token",
    "id_token",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect Tool/MCP activity from sanitized Codex OTel outputs.")
    parser.add_argument("--compare-summary", required=True, help="Path to compare_summary.json.")
    parser.add_argument("--a-parsed", required=True, help="Parsed dir for A-current-config.")
    parser.add_argument("--b-parsed", required=True, help="Parsed dir for B-minimal-config.")
    parser.add_argument("--output-dir", required=True, help="Output dir for Tool/MCP activity artifacts.")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def is_private_field(key: str) -> bool:
    normalized = key.lower()
    if key in PRIVATE_ID_FIELDS:
        return True
    return any(fragment in normalized for fragment in SENSITIVE_FIELD_FRAGMENTS)


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: sanitize(item) for key, item in value.items() if not is_private_field(key)}
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    return value


def stringify_for_match(*parts: Any) -> str:
    return " ".join(json.dumps(part, ensure_ascii=False, default=str) for part in parts if part is not None).lower()


def classify_activity(source_signal: str, name: str, attrs: dict[str, Any]) -> str | None:
    haystack = stringify_for_match(name, attrs)
    name_lower = name.lower()

    if "mcp_servers" in attrs or "mcp_server_count" in attrs:
        return "mcp_server_inventory"
    if source_signal == "metric":
        if name_lower in {"codex.turn.tool.call", "codex.tool.call"}:
            return "tool_call_metric"
        if "tool.call.duration_ms" in name_lower:
            return "tool_call_duration_metric"
        if name_lower == "codex.mcp.call":
            return "mcp_call_metric"
        if "mcp.call.duration_ms" in name_lower:
            return "mcp_call_duration_metric"
        if "tool" in name_lower:
            return "tool_call_metric"
        if "mcp" in name_lower:
            return "mcp_call_metric"

    if "list_all_tools" in haystack or "fetch_uncached" in haystack or "list_tools" in haystack:
        return "mcp_tool_discovery"
    if "transport_worker" in haystack or "streamablehttpclientworker" in haystack or "rmcp" in haystack:
        return "mcp_transport"
    if "session_init.auth_mcp" in haystack or "session_init.mcp" in haystack or "mcp_manager_init" in haystack:
        return "mcp_init"
    if "build_tool_call" in haystack:
        return "tool_call_build"
    if "connection_manager" in haystack:
        return "mcp_tool_discovery"
    if "tool" in haystack:
        return "tool_related_span"
    if "mcp" in haystack:
        return "mcp_related_span"
    return None


def load_turn_windows(compare_summary: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    windows: dict[str, list[dict[str, Any]]] = {}
    for mode in compare_summary.get("modes", []):
        mode_windows: list[dict[str, Any]] = []
        for turn in mode.get("turns", []):
            row = dict(turn)
            row["_start"] = parse_time(turn.get("window_start"))
            row["_end"] = parse_time(turn.get("window_end"))
            mode_windows.append(row)
        windows[mode["mode_id"]] = mode_windows
    return windows


def attach_to_turn(mode_id: str, timestamp: str | None, windows: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    parsed = parse_time(timestamp)
    if parsed is not None:
        for turn in windows.get(mode_id, []):
            start = turn.get("_start")
            end = turn.get("_end")
            if start is not None and end is not None and start <= parsed <= end:
                return {
                    "mode_id": mode_id,
                    "turn_id": turn["turn_id"],
                    "turn_index": turn["turn_index"],
                    "attach_method": "time_window",
                }
    return {
        "mode_id": mode_id,
        "turn_id": "unknown",
        "turn_index": None,
        "attach_method": "mode_level",
    }


def event_name(row: dict[str, Any]) -> str:
    return str(row.get("event_name") or row.get("attributes", {}).get("event.name") or "unknown")


def metric_value(row: dict[str, Any]) -> Any:
    if "value" in row:
        return row["value"]
    if "count" in row:
        return row["count"]
    return None


def selected_details(row: dict[str, Any], source_signal: str) -> dict[str, Any]:
    attrs = row.get("attributes", {}) if isinstance(row.get("attributes"), dict) else {}
    details = {
        "rpc_method": attrs.get("rpc.method"),
        "target": attrs.get("target"),
        "code_module_name": attrs.get("code.module.name"),
        "metric_value": metric_value(row) if source_signal == "metric" else None,
        "mcp_server_count": attrs.get("mcp_server_count"),
        "mcp_servers": attrs.get("mcp_servers"),
    }
    return sanitize({key: value for key, value in details.items() if value is not None})


def build_activity_record(
    mode_id: str,
    source_file: str,
    source_signal: str,
    row: dict[str, Any],
    windows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any] | None:
    attrs = row.get("attributes", {}) if isinstance(row.get("attributes"), dict) else {}
    if source_signal == "span":
        name = str(row.get("span_name") or "unknown")
        timestamp = row.get("start_time")
    elif source_signal == "metric":
        name = str(row.get("metric_name") or "unknown")
        timestamp = row.get("timestamp") or row.get("start_time")
    else:
        name = event_name(row)
        timestamp = row.get("timestamp")

    activity_type = classify_activity(source_signal, name, attrs)
    if activity_type is None:
        return None

    attached = attach_to_turn(mode_id, timestamp, windows)
    return sanitize(
        {
            **attached,
            "source_file": source_file,
            "source_signal": source_signal,
            "activity_type": activity_type,
            "name": name,
            "service_name": row.get("service_name"),
            "timestamp": timestamp,
            "duration_ms": row.get("duration_ms"),
            "trace_id": row.get("traceId"),
            "span_id": row.get("spanId"),
            "details": selected_details(row, source_signal),
        }
    )


def collect_mode_activity(
    mode_id: str,
    parsed_dir: Path,
    windows: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    sources = (
        ("clean_events.jsonl", "event", read_jsonl(parsed_dir / "clean_events.jsonl")),
        ("spans.jsonl", "span", read_jsonl(parsed_dir / "spans.jsonl")),
        ("metrics.jsonl", "metric", read_jsonl(parsed_dir / "metrics.jsonl")),
    )
    records: list[dict[str, Any]] = []
    for source_file, source_signal, rows in sources:
        for row in rows:
            record = build_activity_record(mode_id, source_file, source_signal, row, windows)
            if record is not None:
                records.append(record)
    return records


def counter_to_dict(counter: Counter) -> dict[str, int]:
    return dict(sorted(counter.items()))


def top_counts(counter: Counter, limit: int = 10) -> list[dict[str, Any]]:
    return [{"name": name, "count": count} for name, count in counter.most_common(limit)]


def build_summary(compare_summary: dict[str, Any], activity: list[dict[str, Any]]) -> dict[str, Any]:
    by_mode = defaultdict(list)
    by_turn = defaultdict(list)
    for row in activity:
        by_mode[row["mode_id"]].append(row)
        if row["turn_id"] != "unknown":
            by_turn[f"{row['mode_id']}::{row['turn_id']}"].append(row)

    modes: dict[str, Any] = {}
    turns: dict[str, Any] = {}

    for mode in compare_summary.get("modes", []):
        mode_id = mode["mode_id"]
        mode_rows = by_mode[mode_id]
        type_counts = Counter(row["activity_type"] for row in mode_rows)
        name_counts = Counter(row["name"] for row in mode_rows)
        slow_spans = sorted(
            [row for row in mode_rows if row.get("duration_ms") is not None],
            key=lambda row: row.get("duration_ms") or 0,
            reverse=True,
        )[:10]
        modes[mode_id] = {
            "mcp_server_count": mode.get("mcp_server_count", 0),
            "mcp_servers": mode.get("mcp_servers", ""),
            "total_tool_mcp_activity_records": len(mode_rows),
            "activity_counts_by_type": counter_to_dict(type_counts),
            "top_activity_names": top_counts(name_counts),
            "top_slow_tool_mcp_spans": slow_spans,
            "total_mcp_spans": sum(1 for row in mode_rows if row["activity_type"].startswith("mcp_") and row["source_signal"] == "span"),
            "total_tool_spans": sum(1 for row in mode_rows if "tool" in row["activity_type"] and row["source_signal"] == "span"),
            "total_list_all_tools": sum(1 for row in mode_rows if row["name"] == "list_all_tools"),
            "total_transport_worker": sum(1 for row in mode_rows if row["name"] == "transport_worker"),
            "total_tool_call_metrics": sum(1 for row in mode_rows if row["activity_type"] in {"tool_call_metric", "tool_call_duration_metric"}),
            "total_mcp_call_metrics": sum(1 for row in mode_rows if row["activity_type"] in {"mcp_call_metric", "mcp_call_duration_metric"}),
        }

        for turn in mode.get("turns", []):
            turn_key = f"{mode_id}::{turn['turn_id']}"
            turn_rows = by_turn[turn_key]
            turn_type_counts = Counter(row["activity_type"] for row in turn_rows)
            turns[turn_key] = {
                "mode_id": mode_id,
                "turn_id": turn["turn_id"],
                "turn_index": turn["turn_index"],
                "input_tokens": turn.get("input_tokens"),
                "output_tokens": turn.get("output_tokens"),
                "cached_tokens": turn.get("cached_tokens"),
                "reasoning_tokens": turn.get("reasoning_tokens"),
                "tool_tokens": turn.get("tool_tokens"),
                "mcp_spans": sum(1 for row in turn_rows if row["activity_type"].startswith("mcp_") and row["source_signal"] == "span"),
                "tool_spans": sum(1 for row in turn_rows if "tool" in row["activity_type"] and row["source_signal"] == "span"),
                "list_all_tools": sum(1 for row in turn_rows if row["name"] == "list_all_tools"),
                "transport_worker": sum(1 for row in turn_rows if row["name"] == "transport_worker"),
                "tool_call_metrics": sum(1 for row in turn_rows if row["activity_type"] in {"tool_call_metric", "tool_call_duration_metric"}),
                "mcp_call_metrics": sum(1 for row in turn_rows if row["activity_type"] in {"mcp_call_metric", "mcp_call_duration_metric"}),
                "activity_counts_by_type": counter_to_dict(turn_type_counts),
                "tool_call_status": turn.get("tool_call_status"),
                "interpretation_hint": interpretation_hint(turn, turn_rows),
            }

    return {
        "metadata": {
            "source": "sanitized parsed outputs and compare_summary.json",
            "exact_per_tool_tokens_available": False,
        },
        "modes": modes,
        "turns": turns,
    }


def interpretation_hint(turn: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    if turn.get("tool_call_status") == "called" and rows:
        return "Tool/MCP activity visible near tool turn; token usage remains turn-level only."
    if rows:
        return "Tool/MCP environment activity visible near no-tool turn."
    return "No attached Tool/MCP activity in this turn window."


def fmt_int(value: Any) -> str:
    return "" if value is None else str(value)


def fmt_delta(value: Any) -> str:
    if value is None:
        return "unknown"
    sign = "+" if isinstance(value, int) and value >= 0 else ""
    return f"{sign}{value}"


def build_report(compare_summary: dict[str, Any], summary: dict[str, Any], activity: list[dict[str, Any]]) -> str:
    modes = summary["modes"]
    turns = summary["turns"]
    comparisons = compare_summary.get("comparisons", {})
    baseline_delta = comparisons.get("baseline_overhead", {}).get("A1_minus_B1_input_tokens")
    a_tool_delta = comparisons.get("tool_turn_overhead", {}).get("A3_minus_A2_input_tokens")
    b_tool_delta = comparisons.get("tool_turn_overhead", {}).get("B3_minus_B2_input_tokens")

    lines = [
        "# Tool/MCP Activity Report",
        "",
        "## Цель",
        "",
        "Показать, какая Tool/MCP активность была в current config и minimal/no MCP config, и как она связана с token overhead.",
        "",
        "## Главный вывод",
        "",
        f"- Current config имеет `{modes.get('A-current-config', {}).get('mcp_server_count', 0)}` MCP servers.",
        f"- Minimal config имеет `{modes.get('B-minimal-config', {}).get('mcp_server_count', 0)}` MCP servers.",
        f"- Current дороже minimal примерно на `{fmt_delta(baseline_delta)}` input tokens на baseline turn.",
        f"- Tool-turn добавляет около `{fmt_delta(a_tool_delta)}` tokens в current и `{fmt_delta(b_tool_delta)}` tokens в minimal.",
        "- Основной overhead похож на постоянное Tool/MCP окружение, discovery/transport/inventory, а не на цену одного safe tool call.",
        "",
        "## MCP inventory",
        "",
        "| Mode | MCP server count | MCP servers |",
        "|---|---:|---|",
    ]

    for mode_id, mode in modes.items():
        lines.append(f"| {mode_id} | {mode['mcp_server_count']} | {mode['mcp_servers']} |")

    lines.extend(
        [
            "",
            "## Activity by turn",
            "",
            "| Mode | Turn | Input | Cached | MCP spans | Tool spans | list_all_tools | Transport | Tool call metrics | MCP call metrics | Tool status |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for turn in turns.values():
        lines.append(
            f"| {turn['mode_id']} | {turn['turn_id']} | {fmt_int(turn['input_tokens'])} | {fmt_int(turn['cached_tokens'])} | "
            f"{turn['mcp_spans']} | {turn['tool_spans']} | {turn['list_all_tools']} | {turn['transport_worker']} | "
            f"{turn['tool_call_metrics']} | {turn['mcp_call_metrics']} | {turn['tool_call_status']} |"
        )

    activity_types = sorted({row["activity_type"] for row in activity})
    lines.extend(["", "## Activity types", "", "| Activity type | A-current count | B-minimal count | Notes |", "|---|---:|---:|---|"])
    for activity_type in activity_types:
        a_count = modes.get("A-current-config", {}).get("activity_counts_by_type", {}).get(activity_type, 0)
        b_count = modes.get("B-minimal-config", {}).get("activity_counts_by_type", {}).get(activity_type, 0)
        lines.append(f"| {activity_type} | {a_count} | {b_count} | normalized classifier |")

    name_mode_counts: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for row in activity:
        name_mode_counts[(row["name"], row["activity_type"])][row["mode_id"]] += 1
    top_names = sorted(name_mode_counts.items(), key=lambda item: sum(item[1].values()), reverse=True)[:15]
    lines.extend(["", "## Top tool/MCP activity names", "", "| Name | Activity type | Count | Modes |", "|---|---|---:|---|"])
    for (name, activity_type), counts in top_names:
        modes_text = ", ".join(f"{mode}:{count}" for mode, count in sorted(counts.items()))
        lines.append(f"| {name} | {activity_type} | {sum(counts.values())} | {modes_text} |")

    slow_spans = sorted(
        [row for row in activity if row.get("duration_ms") is not None],
        key=lambda row: row.get("duration_ms") or 0,
        reverse=True,
    )[:10]
    lines.extend(["", "## Slow tool/MCP spans", "", "| Mode | Turn | Name | Activity type | Duration ms | Service |", "|---|---|---|---|---:|---|"])
    for row in slow_spans:
        lines.append(
            f"| {row['mode_id']} | {row['turn_id']} | {row['name']} | {row['activity_type']} | "
            f"{row.get('duration_ms')} | {row.get('service_name') or ''} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "### Confirmed facts",
            "",
            f"- A current has `{modes.get('A-current-config', {}).get('mcp_server_count', 0)}` MCP servers.",
            f"- B minimal has `{modes.get('B-minimal-config', {}).get('mcp_server_count', 0)}` MCP servers.",
            f"- A is about `{fmt_delta(baseline_delta)}` input tokens vs B on first turn.",
            f"- A3 vs A2 tool-turn overhead is about `{fmt_delta(a_tool_delta)}`.",
            f"- B3 vs B2 tool-turn overhead is about `{fmt_delta(b_tool_delta)}`.",
            "- OTel does not expose exact per-tool token usage.",
            "",
            "### Likely interpretation",
            "",
            "- Extra MCP/tool environment in current config likely contributes roughly 10k input tokens.",
            "- Safe tool call itself is cheap in this experiment.",
            "- Expensive part likely tool environment/schema/discovery/context overhead, not actual tool invocation.",
            "",
            "### Unknown / limitations",
            "",
            "- Cannot attribute exact tokens to each MCP server.",
            "- Cannot prove schema size without MCP inventory/tool schema size extraction.",
            "- Cannot prove per-tool token usage from OTel alone.",
            "- Some activity may be attached by time window, not exact causal link.",
            "",
            "## Recommended next diagnostic step",
            "",
            "Next step: MCP inventory / schema size report. It should measure tools per MCP server, tool descriptions/schema sizes, rough schema payload token estimate, and heaviest servers.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    compare_summary_path = Path(args.compare_summary).resolve()
    a_parsed = Path(args.a_parsed).resolve()
    b_parsed = Path(args.b_parsed).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    compare_summary = read_json(compare_summary_path)
    windows = load_turn_windows(compare_summary)
    activity = []
    activity.extend(collect_mode_activity("A-current-config", a_parsed, windows))
    activity.extend(collect_mode_activity("B-minimal-config", b_parsed, windows))
    activity.sort(key=lambda row: (row["mode_id"], row.get("timestamp") or "", row["source_file"], row["name"]))

    summary = build_summary(compare_summary, activity)
    write_jsonl(output_dir / "tool_mcp_activity.jsonl", activity)
    (output_dir / "tool_mcp_activity_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "tool_mcp_activity_report.md").write_text(
        build_report(compare_summary, summary, activity),
        encoding="utf-8",
    )
    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
