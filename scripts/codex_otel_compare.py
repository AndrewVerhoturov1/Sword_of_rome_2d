#!/usr/bin/env python3
"""
Compare parsed Codex OTel outputs for current-vs-minimal turn-cost experiments.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


TURN_IDS = ("1", "2", "3")
TOOLISH_SPAN_NAMES = {
    "build_tool_call",
    "dispatch_tool_call_with_terminal_outcome",
    "handle_tool_call",
    "handle_tool_call_with_source",
    "op.dispatch.dynamic_tool_response",
}
MCPISH_SPAN_NAMES = {
    "list_tools_for_server",
    "read_mcp_connection_manager",
    "mcpServerStatus/list",
    "session_init.auth_mcp",
    "session_init.mcp_manager_init",
}
SPECIAL_SPAN_NAMES = {
    "list_all_tools",
    "transport_worker",
    "built_tools",
}


@dataclass
class TurnWindow:
    prompt_time: datetime
    response_time: datetime
    prompt_length: int
    prompt_type: str
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    reasoning_tokens: int
    tool_tokens: int
    model: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare parsed Codex OTel experiment outputs.")
    parser.add_argument("--a-parsed", required=True, help="Parsed dir for current-config run (rerun is fine).")
    parser.add_argument("--b-parsed", required=True, help="Parsed dir for minimal/no-MCP run.")
    parser.add_argument("--output-dir", required=True, help="Directory for compare_summary.json and compare_report.md.")
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)


def load_parsed_dir(parsed_dir: Path) -> dict[str, list[dict[str, Any]]]:
    return {
        "clean_events": read_jsonl(parsed_dir / "clean_events.jsonl"),
        "spans": read_jsonl(parsed_dir / "spans.jsonl"),
        "metrics": read_jsonl(parsed_dir / "metrics.jsonl"),
    }


def find_conversation_starts(clean_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in clean_events if row.get("event_name") == "codex.conversation_starts"]


def find_user_prompts(clean_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompts = [
        row
        for row in clean_events
        if row.get("event_name") == "codex.user_prompt"
        and row.get("attributes", {}).get("model") == "gpt-5.5"
    ]
    return sorted(prompts, key=lambda row: row["timestamp"])


def find_response_completed(
    clean_events: list[dict[str, Any]],
    prompt_time: datetime,
    next_prompt_time: datetime | None,
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for row in clean_events:
        if row.get("event_name") != "codex.sse_event":
            continue
        attrs = row.get("attributes", {})
        if attrs.get("event.kind") != "response.completed":
            continue
        if attrs.get("model") != "gpt-5.5":
            continue
        timestamp = parse_iso(row["timestamp"])
        if timestamp < prompt_time:
            continue
        if next_prompt_time is not None and timestamp >= next_prompt_time:
            continue
        candidates.append(row)
    if not candidates:
        raise ValueError(f"No response.completed found after prompt at {prompt_time.isoformat()}")
    return sorted(candidates, key=lambda row: row["timestamp"])[0]


def detect_prompt_type(index: int) -> str:
    if index == 1:
        return "short_no_tool"
    if index == 2:
        return "second_short_no_tool"
    return "safe_tool_call_then_answer"


def extract_turns(clean_events: list[dict[str, Any]]) -> list[TurnWindow]:
    prompts = find_user_prompts(clean_events)
    if len(prompts) < 3:
        raise ValueError(f"Expected at least 3 gpt-5.5 user prompts, got {len(prompts)}")
    prompts = prompts[-3:]

    turns: list[TurnWindow] = []
    for index, prompt_row in enumerate(prompts, start=1):
        prompt_time = parse_iso(prompt_row["timestamp"])
        next_prompt_time = parse_iso(prompts[index]["timestamp"]) if index < len(prompts) else None
        response_row = find_response_completed(clean_events, prompt_time, next_prompt_time)
        attrs = response_row.get("attributes", {})
        turns.append(
            TurnWindow(
                prompt_time=prompt_time,
                response_time=parse_iso(response_row["timestamp"]),
                prompt_length=int(prompt_row.get("attributes", {}).get("prompt_length", 0)),
                prompt_type=detect_prompt_type(index),
                input_tokens=int(attrs.get("input_token_count", 0)),
                output_tokens=int(attrs.get("output_token_count", 0)),
                cached_tokens=int(attrs.get("cached_token_count", 0)),
                reasoning_tokens=int(attrs.get("reasoning_token_count", 0)),
                tool_tokens=int(attrs.get("tool_token_count", 0)),
                model=str(attrs.get("model", "unknown")),
            )
        )
    return turns


def event_in_window(timestamp: str, start: datetime, end: datetime) -> bool:
    event_time = parse_iso(timestamp)
    return start <= event_time <= end


def summarize_activity(
    spans: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    start: datetime,
    end: datetime,
) -> dict[str, int]:
    span_counts = {
        "mcp_spans": 0,
        "tool_spans": 0,
        "list_all_tools": 0,
        "transport_worker": 0,
    }
    metric_counts = {
        "tool.call metrics": 0,
        "mcp.call metrics": 0,
    }

    for span in spans:
        timestamp = span.get("start_time")
        if not timestamp or not event_in_window(timestamp, start, end):
            continue
        name = span.get("span_name", "")
        if name in MCPISH_SPAN_NAMES:
            span_counts["mcp_spans"] += 1
        if name in TOOLISH_SPAN_NAMES:
            span_counts["tool_spans"] += 1
        if name == "list_all_tools":
            span_counts["list_all_tools"] += 1
        if name == "transport_worker":
            span_counts["transport_worker"] += 1

    for metric in metrics:
        timestamp = metric.get("timestamp")
        if not timestamp or not event_in_window(timestamp, start, end):
            continue
        name = metric.get("metric_name", "")
        if name.startswith("codex.tool.call") or name == "codex.turn.tool.call":
            metric_counts["tool.call metrics"] += 1
        if name.startswith("codex.mcp."):
            metric_counts["mcp.call metrics"] += 1

    return {**span_counts, **metric_counts}


def cache_ratio(input_tokens: int, cached_tokens: int) -> float | None:
    if input_tokens <= 0:
        return None
    return round(cached_tokens / input_tokens, 4)


def conversation_start_meta(clean_events: list[dict[str, Any]], first_prompt: datetime) -> dict[str, Any]:
    starts = find_conversation_starts(clean_events)
    candidates = []
    for row in starts:
        timestamp = parse_iso(row["timestamp"])
        if timestamp <= first_prompt and first_prompt - timestamp <= timedelta(minutes=2):
            candidates.append(row)
    if not candidates:
        return {"fresh_start_confirmed": False, "mcp_servers": "", "mcp_server_count": 0}
    row = sorted(candidates, key=lambda item: item["timestamp"])[-1]
    attrs = row.get("attributes", {})
    mcp_servers = attrs.get("mcp_servers", "")
    count = attrs.get("mcp_server_count")
    if count is None and mcp_servers:
        count = len([item.strip() for item in str(mcp_servers).split(",") if item.strip()])
    return {
        "fresh_start_confirmed": True,
        "mcp_servers": mcp_servers,
        "mcp_server_count": int(count or 0),
    }


def build_mode(
    mode_id: str,
    config_type: str,
    parsed_dir: Path,
    clean_events: list[dict[str, Any]],
    spans: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
) -> dict[str, Any]:
    turns = extract_turns(clean_events)
    meta = conversation_start_meta(clean_events, turns[0].prompt_time)
    output_turns = []
    same_session_reliable = True

    for index, turn in enumerate(turns, start=1):
        activity = summarize_activity(spans, metrics, turn.prompt_time, turn.response_time)
        tool_status = "none_expected"
        if index == 3:
            tool_status = "called" if (activity["tool_spans"] or activity["tool.call metrics"]) else "unknown"

        output_turns.append(
            {
                "turn_id": f"{mode_id[0]}{index}",
                "turn_index": index,
                "prompt_type": turn.prompt_type,
                "prompt_length": turn.prompt_length,
                "input_tokens": turn.input_tokens,
                "output_tokens": turn.output_tokens,
                "cached_tokens": turn.cached_tokens,
                "reasoning_tokens": turn.reasoning_tokens,
                "tool_tokens": turn.tool_tokens,
                "cache_ratio": cache_ratio(turn.input_tokens, turn.cached_tokens),
                "tool_call_status": tool_status,
                "tool_mcp_activity": activity,
                "window_start": turn.prompt_time.isoformat(),
                "window_end": turn.response_time.isoformat(),
                "model": turn.model,
            }
        )

    return {
        "mode_id": mode_id,
        "config_type": config_type,
        "source_parsed_dir": str(parsed_dir),
        "fresh_start_confirmed": meta["fresh_start_confirmed"],
        "same_session_reliable": same_session_reliable,
        "mcp_server_count": meta["mcp_server_count"],
        "mcp_servers": meta["mcp_servers"],
        "turns": output_turns,
    }


def get_turn(mode: dict[str, Any], turn_id: str) -> dict[str, Any]:
    for turn in mode["turns"]:
        if turn["turn_id"] == turn_id:
            return turn
    raise KeyError(turn_id)


def delta(left: int | None, right: int | None) -> int | None:
    if left is None or right is None:
        return None
    return left - right


def format_delta(value: int | None) -> str:
    return "" if value is None else str(value)


def interpret_comparisons(mode_a: dict[str, Any], mode_b: dict[str, Any]) -> dict[str, Any]:
    a1 = get_turn(mode_a, "A1")
    a2 = get_turn(mode_a, "A2")
    a3 = get_turn(mode_a, "A3")
    b1 = get_turn(mode_b, "B1")
    b2 = get_turn(mode_b, "B2")
    b3 = get_turn(mode_b, "B3")

    baseline_delta = delta(a1["input_tokens"], b1["input_tokens"])
    a_cache_delta = delta(a2["cached_tokens"], a1["cached_tokens"])
    b_cache_delta = delta(b2["cached_tokens"], b1["cached_tokens"])
    a_tool_delta = delta(a3["input_tokens"], a2["input_tokens"])
    b_tool_delta = delta(b3["input_tokens"], b2["input_tokens"])

    baseline_text = (
        "Current config дороже на первом сообщении, похоже есть overhead MCP/tool environment."
        if (baseline_delta or 0) > 0
        else "Minimal config не дешевле на первом сообщении; явный baseline overhead не подтвердился."
    )
    second_turn_text = (
        "Второй ход использует больше cache, cache помогает."
        if (a_cache_delta or 0) > 0 or (b_cache_delta or 0) > 0
        else "Рост cache между первым и вторым ходом не выражен."
    )
    tool_turn_text = (
        "Tool-turn дороже no-tool turn."
        if (a_tool_delta or 0) > 0 or (b_tool_delta or 0) > 0
        else "Явного token overhead у tool-turn не видно."
    )
    env_text = (
        "Current config выглядит тяжелее minimal и на baseline, и на tool turn."
        if (baseline_delta or 0) > 0 and (delta(a3["input_tokens"], b3["input_tokens"]) or 0) > 0
        else "Разница current vs minimal есть не на всех turn одинаково."
    )

    return {
        "baseline_overhead": {
            "A1_minus_B1_input_tokens": baseline_delta,
            "interpretation": baseline_text,
        },
        "second_turn_cache_effect": {
            "A2_minus_A1_input_tokens": delta(a2["input_tokens"], a1["input_tokens"]),
            "A2_minus_A1_cached_tokens": a_cache_delta,
            "B2_minus_B1_input_tokens": delta(b2["input_tokens"], b1["input_tokens"]),
            "B2_minus_B1_cached_tokens": b_cache_delta,
            "interpretation": second_turn_text,
        },
        "tool_turn_overhead": {
            "A3_minus_A2_input_tokens": a_tool_delta,
            "B3_minus_B2_input_tokens": b_tool_delta,
            "interpretation": tool_turn_text,
        },
        "mcp_tool_environment_overhead": {
            "A1_minus_B1_input_tokens": baseline_delta,
            "A3_minus_B3_input_tokens": delta(a3["input_tokens"], b3["input_tokens"]),
            "interpretation": env_text,
        },
    }


def build_report(summary: dict[str, Any]) -> str:
    mode_a, mode_b = summary["modes"]
    lines = [
        "# Compare Report",
        "",
        "Сравнение построено по валидной паре: `A-current-config` из rerun и `B-minimal-config` из исходного прогона.",
        "Старый `A-current-config/raw/codex-otel.json` отброшен, потому что collector был убит при рестарте Codex и файл остался пустым.",
        "",
        "## Token comparison by turn",
        "",
        "| Mode | Turn | Prompt type | Input | Output | Cached | Reasoning | Tool tokens | Cache ratio | Tool status |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]

    for mode in (mode_a, mode_b):
        for turn in mode["turns"]:
            lines.append(
                f"| {mode['mode_id']} | {turn['turn_id']} | {turn['prompt_type']} | "
                f"{turn['input_tokens']} | {turn['output_tokens']} | {turn['cached_tokens']} | "
                f"{turn['reasoning_tokens']} | {turn['tool_tokens']} | {turn['cache_ratio'] if turn['cache_ratio'] is not None else ''} | "
                f"{turn['tool_call_status']} |"
            )

    comparisons = summary["comparisons"]
    lines.extend(
        [
            "",
            "## Current vs minimal",
            "",
            "| Comparison | Input delta | Cached delta | Interpretation |",
            "|---|---:|---:|---|",
            f"| A1 vs B1: baseline environment overhead | {format_delta(comparisons['baseline_overhead']['A1_minus_B1_input_tokens'])} |  | {comparisons['baseline_overhead']['interpretation']} |",
            f"| A2 vs B2: second-turn environment overhead | {format_delta(delta(get_turn(mode_a, 'A2')['input_tokens'], get_turn(mode_b, 'B2')['input_tokens']))} | {format_delta(delta(get_turn(mode_a, 'A2')['cached_tokens'], get_turn(mode_b, 'B2')['cached_tokens']))} | Разница на втором ходе. |",
            f"| A3 vs B3: tool-turn environment overhead | {format_delta(delta(get_turn(mode_a, 'A3')['input_tokens'], get_turn(mode_b, 'B3')['input_tokens']))} | {format_delta(delta(get_turn(mode_a, 'A3')['cached_tokens'], get_turn(mode_b, 'B3')['cached_tokens']))} | Разница на tool-turn. |",
            f"| A2 vs A1: current second-turn/cache effect | {format_delta(comparisons['second_turn_cache_effect']['A2_minus_A1_input_tokens'])} | {format_delta(comparisons['second_turn_cache_effect']['A2_minus_A1_cached_tokens'])} | {comparisons['second_turn_cache_effect']['interpretation']} |",
            f"| B2 vs B1: minimal second-turn/cache effect | {format_delta(comparisons['second_turn_cache_effect']['B2_minus_B1_input_tokens'])} | {format_delta(comparisons['second_turn_cache_effect']['B2_minus_B1_cached_tokens'])} | {comparisons['second_turn_cache_effect']['interpretation']} |",
            f"| A3 vs A2: current tool-call overhead | {format_delta(comparisons['tool_turn_overhead']['A3_minus_A2_input_tokens'])} | {format_delta(delta(get_turn(mode_a, 'A3')['cached_tokens'], get_turn(mode_a, 'A2')['cached_tokens']))} | {comparisons['tool_turn_overhead']['interpretation']} |",
            f"| B3 vs B2: minimal tool-call overhead | {format_delta(comparisons['tool_turn_overhead']['B3_minus_B2_input_tokens'])} | {format_delta(delta(get_turn(mode_b, 'B3')['cached_tokens'], get_turn(mode_b, 'B2')['cached_tokens']))} | {comparisons['tool_turn_overhead']['interpretation']} |",
            "",
            "## Tool/MCP activity by turn",
            "",
            "| Mode | Turn | MCP spans | Tool spans | list_all_tools | transport_worker | tool.call metrics | mcp.call metrics |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )

    for mode in (mode_a, mode_b):
        for turn in mode["turns"]:
            activity = turn["tool_mcp_activity"]
            lines.append(
                f"| {mode['mode_id']} | {turn['turn_id']} | {activity['mcp_spans']} | {activity['tool_spans']} | "
                f"{activity['list_all_tools']} | {activity['transport_worker']} | {activity['tool.call metrics']} | {activity['mcp.call metrics']} |"
            )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            f"- Current config `mcp_server_count`: `{mode_a['mcp_server_count']}`",
            f"- Minimal config `mcp_server_count`: `{mode_b['mcp_server_count']}`",
            "- Per-tool token usage здесь не утверждается. OTel показывает token usage по turn и активность tool/MCP рядом с ходом.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    a_parsed = Path(args.a_parsed).resolve()
    b_parsed = Path(args.b_parsed).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    a_data = load_parsed_dir(a_parsed)
    b_data = load_parsed_dir(b_parsed)

    mode_a = build_mode("A-current-config", "current", a_parsed, **a_data)
    mode_b = build_mode("B-minimal-config", "minimal_no_mcp", b_parsed, **b_data)

    summary = {
        "metadata": {
            "comparison_kind": "A-rerun-vs-B",
            "invalidated_runs": [
                "A-current-config/raw/codex-otel.json was empty because collector was terminated during restart."
            ],
        },
        "modes": [mode_a, mode_b],
        "comparisons": interpret_comparisons(mode_a, mode_b),
    }

    (output_dir / "compare_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "compare_report.md").write_text(build_report(summary), encoding="utf-8")
    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
