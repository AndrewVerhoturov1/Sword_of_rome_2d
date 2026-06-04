#!/usr/bin/env python3
"""
Build a local MCP inventory/schema size report from sanitized config metadata.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import tomllib
from pathlib import Path
from typing import Any, Iterable


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
    "token",
    "email",
    "account",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build local MCP inventory/schema size artifacts.")
    parser.add_argument("--config", required=True, help="Path to Codex config.toml. Read-only.")
    parser.add_argument("--compare-summary", required=True, help="Path to compare_summary.json.")
    parser.add_argument("--activity-summary", required=True, help="Path to tool_mcp_activity_summary.json.")
    parser.add_argument("--output-dir", required=True, help="Output dir for MCP schema inventory artifacts.")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def is_sensitive_key(key: str) -> bool:
    normalized = key.lower()
    return any(fragment in normalized for fragment in SENSITIVE_FIELD_FRAGMENTS)


def sanitize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: sanitize_value(item) for key, item in value.items() if not is_sensitive_key(str(key))}
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    return value


def parse_server_list(value: Any) -> list[str]:
    if value is None:
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]


def mode_servers(compare_summary: dict[str, Any], mode_id: str) -> list[str]:
    for mode in compare_summary.get("modes", []):
        if mode.get("mode_id") == mode_id:
            return parse_server_list(mode.get("mcp_servers"))
    return []


def source_for_server(server_name: str, current_servers: set[str], minimal_servers: set[str], config_servers: set[str]) -> str:
    in_current = server_name in current_servers or server_name in config_servers
    in_minimal = server_name in minimal_servers
    if in_current and in_minimal:
        return "both"
    if in_current:
        return "current_config"
    if in_minimal:
        return "minimal_config"
    return "unknown"


def command_safe(command: Any) -> str | None:
    if not isinstance(command, str) or not command:
        return None
    return os.path.basename(command.replace("\\", os.sep).replace("/", os.sep)) or command


def detect_transport(server_config: dict[str, Any]) -> str:
    transport = server_config.get("transport")
    if isinstance(transport, str) and transport:
        normalized = transport.lower().replace("-", "_")
        if normalized in {"stdio", "http", "streamable_http", "sse"}:
            return normalized
    if server_config.get("url") or server_config.get("endpoint"):
        return "http"
    if server_config.get("command"):
        return "stdio"
    return "unknown"


def tool_schema_payload(tool_config: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    description = tool_config.get("description")
    if isinstance(description, str):
        payload["description"] = description
    for key in ("input_schema", "inputSchema", "json_schema", "schema"):
        if key in tool_config:
            payload["input_schema"] = sanitize_value(tool_config[key])
            break
    return payload


def serialized_chars(value: Any) -> int:
    if value in (None, {}, [], ""):
        return 0
    return len(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def estimate_tokens(chars: int | None) -> int | None:
    if chars is None:
        return None
    return math.ceil(chars / 4)


def build_server_row(
    server_name: str,
    server_config: dict[str, Any],
    source: str,
) -> dict[str, Any]:
    has_config_section = bool(server_config)
    env = server_config.get("env", {})
    if not isinstance(env, dict):
        env = {}
    env_keys = sorted(str(key) for key in env.keys())
    tools = server_config.get("tools", {})
    if not isinstance(tools, dict):
        tools = {}

    largest_tools: list[dict[str, Any]] = []
    total_description_chars = 0
    total_input_schema_chars = 0
    total_schema_chars = 0
    tool_names = sorted(str(name) for name in tools.keys())

    for tool_name in tool_names:
        tool_config = tools.get(tool_name, {})
        if not isinstance(tool_config, dict):
            tool_config = {}
        payload = tool_schema_payload(tool_config)
        description_chars = len(tool_config.get("description", "")) if isinstance(tool_config.get("description"), str) else 0
        input_schema_chars = serialized_chars(payload.get("input_schema"))
        schema_chars = serialized_chars(payload)
        total_description_chars += description_chars
        total_input_schema_chars += input_schema_chars
        total_schema_chars += schema_chars
        if schema_chars:
            largest_tools.append(
                {
                    "tool_name": tool_name,
                    "schema_chars": schema_chars,
                    "estimated_tokens": estimate_tokens(schema_chars),
                }
            )

    largest_tools.sort(key=lambda row: row["schema_chars"], reverse=True)
    warnings: list[str] = []
    if not total_schema_chars:
        warnings.append("schema_unavailable")
    if any(is_sensitive_key(key) for key in env_keys):
        warnings.append("sanitized_secret_key_present")
    if has_config_section and not tool_names:
        warnings.append("no_tools_found")

    return {
        "server_name": server_name,
        "enabled": True,
        "source": source,
        "transport": detect_transport(server_config),
        "command_safe": command_safe(server_config.get("command")),
        "args_count": len(server_config.get("args", [])) if isinstance(server_config.get("args"), list) else 0,
        "env_keys_count": len(env_keys),
        "env_keys_sanitized": env_keys,
        "tool_count": len(tool_names) if tool_names else None,
        "tool_names": tool_names,
        "total_schema_chars": total_schema_chars or None,
        "total_description_chars": total_description_chars or None,
        "total_input_schema_chars": total_input_schema_chars or None,
        "estimated_schema_tokens": estimate_tokens(total_schema_chars) if total_schema_chars else None,
        "largest_tools": largest_tools[:10],
        "warnings": warnings,
    }


def load_mcp_config(config_path: Path) -> dict[str, dict[str, Any]]:
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    servers = data.get("mcp_servers", {})
    if not isinstance(servers, dict):
        return {}
    return {str(name): config for name, config in servers.items() if isinstance(config, dict)}


def build_inventory(config_path: Path, compare_summary: dict[str, Any]) -> list[dict[str, Any]]:
    config_servers = load_mcp_config(config_path)
    current_servers = set(mode_servers(compare_summary, "A-current-config"))
    minimal_servers = set(mode_servers(compare_summary, "B-minimal-config"))
    all_servers = sorted(set(config_servers.keys()) | current_servers | minimal_servers)
    rows = []
    for server_name in all_servers:
        source = source_for_server(server_name, current_servers, minimal_servers, set(config_servers.keys()))
        rows.append(build_server_row(server_name, config_servers.get(server_name, {}), source))
    return rows


def build_summary(
    inventory: list[dict[str, Any]],
    compare_summary: dict[str, Any],
    activity_summary: dict[str, Any],
) -> dict[str, Any]:
    current = [row for row in inventory if row["source"] in {"current_config", "both"}]
    minimal = [row for row in inventory if row["source"] in {"minimal_config", "both"}]
    schema_available = [row for row in inventory if row["estimated_schema_tokens"] is not None]
    warnings = sorted({warning for row in inventory for warning in row["warnings"]} | {"token_estimate_rough"})
    return {
        "metadata": {
            "token_estimator": "ceil(chars / 4)",
            "exact_tokenizer_used": False,
            "read_only": True,
            "tools_executed": False,
            "schema_source": "config metadata and sanitized parsed outputs only",
        },
        "totals": {
            "server_count_current": len(current),
            "server_count_minimal": len(minimal),
            "schema_available_server_count": len(schema_available),
            "total_tool_count_current": sum(row["tool_count"] or 0 for row in current),
            "total_estimated_schema_tokens_current": sum(row["estimated_schema_tokens"] or 0 for row in current),
        },
        "servers_ranked_by_estimated_tokens": [
            {
                "server_name": row["server_name"],
                "tool_count": row["tool_count"],
                "total_schema_chars": row["total_schema_chars"],
                "estimated_schema_tokens": row["estimated_schema_tokens"],
            }
            for row in sorted(schema_available, key=lambda item: item["estimated_schema_tokens"] or 0, reverse=True)
        ],
        "servers_ranked_by_tool_count": [
            {
                "server_name": row["server_name"],
                "tool_count": row["tool_count"],
                "estimated_schema_tokens": row["estimated_schema_tokens"],
            }
            for row in sorted(inventory, key=lambda item: item["tool_count"] or 0, reverse=True)
        ],
        "servers_with_unavailable_schema": [row["server_name"] for row in inventory if "schema_unavailable" in row["warnings"]],
        "previous_compare_context": {
            "baseline_overhead_input_tokens": compare_summary.get("comparisons", {})
            .get("baseline_overhead", {})
            .get("A1_minus_B1_input_tokens"),
            "current_activity_records": activity_summary.get("modes", {})
            .get("A-current-config", {})
            .get("total_tool_mcp_activity_records"),
            "minimal_activity_records": activity_summary.get("modes", {})
            .get("B-minimal-config", {})
            .get("total_tool_mcp_activity_records"),
        },
        "warnings": warnings,
    }


def build_warnings(inventory: list[dict[str, Any]], summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [{"warning": "token_estimate_rough", "severity": "info", "server_name": None}]
    for row in inventory:
        for warning in row["warnings"]:
            rows.append({"warning": warning, "severity": "warning", "server_name": row["server_name"]})
    if not inventory:
        rows.append({"warning": "config_not_found", "severity": "error", "server_name": None})
    if summary["totals"]["server_count_current"] == 0:
        rows.append({"warning": "source_config_ambiguous", "severity": "warning", "server_name": None})
    return rows


def build_sanitized_config_extract(inventory: list[dict[str, Any]]) -> str:
    lines = [
        "# Sanitized MCP config extract.",
        "# Values of env vars and args are intentionally not stored.",
        "",
    ]
    for row in inventory:
        lines.append(f"[mcp_servers.{row['server_name']}]")
        if row.get("command_safe"):
            lines.append(f'command_safe = "{row["command_safe"]}"')
        lines.append(f'transport = "{row["transport"]}"')
        lines.append(f"args_count = {row['args_count']}")
        lines.append(f"env_keys_count = {row['env_keys_count']}")
        if row["env_keys_sanitized"]:
            keys = ", ".join(json.dumps(key, ensure_ascii=False) for key in row["env_keys_sanitized"])
            lines.append(f"env_keys_sanitized = [{keys}]")
        lines.append("")
    return "\n".join(lines)


def fmt(value: Any) -> str:
    return "" if value is None else str(value)


def format_delta(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, int) and value >= 0:
        return f"+{value}"
    return str(value)


def build_report(inventory: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    baseline = summary["previous_compare_context"]["baseline_overhead_input_tokens"]
    total_tokens = summary["totals"]["total_estimated_schema_tokens_current"]
    schema_available_count = summary["totals"]["schema_available_server_count"]
    lines = [
        "# MCP Schema Inventory Report",
        "",
        "## Цель",
        "",
        "Понять, какие MCP servers и tool schemas потенциально дают постоянный MCP/tool environment overhead.",
        "",
        "## Связь с предыдущим token compare",
        "",
        f"- current config: `{summary['totals']['server_count_current']}` MCP servers.",
        f"- minimal config: `{summary['totals']['server_count_minimal']}` MCP servers.",
        f"- current дороже minimal примерно на `{format_delta(baseline)}` input tokens.",
        "- safe tool-call добавил около `+200` input tokens.",
        "- Значит основной overhead надо искать в постоянном MCP/tool schema окружении.",
        "",
        "## MCP servers",
        "",
        "| Server | Source | Transport | Tool count | Estimated schema tokens | Warnings |",
        "|---|---|---|---:|---:|---|",
    ]
    for row in inventory:
        warnings = ", ".join(row["warnings"])
        lines.append(
            f"| {row['server_name']} | {row['source']} | {row['transport']} | {fmt(row['tool_count'])} | "
            f"{fmt(row['estimated_schema_tokens'])} | {warnings} |"
        )

    lines.extend(
        [
            "",
            "## Heaviest servers by estimated schema tokens",
            "",
            "| Rank | Server | Tools | Schema chars | Estimated tokens |",
            "|---:|---|---:|---:|---:|",
        ]
    )
    for index, row in enumerate(summary["servers_ranked_by_estimated_tokens"][:10], start=1):
        lines.append(
            f"| {index} | {row['server_name']} | {fmt(row['tool_count'])} | "
            f"{fmt(row['total_schema_chars'])} | {fmt(row['estimated_schema_tokens'])} |"
        )

    lines.extend(
        [
            "",
            "## Heaviest servers by tool count",
            "",
            "| Rank | Server | Tool count | Estimated tokens |",
            "|---:|---|---:|---:|",
        ]
    )
    for index, row in enumerate(summary["servers_ranked_by_tool_count"][:10], start=1):
        lines.append(f"| {index} | {row['server_name']} | {fmt(row['tool_count'])} | {fmt(row['estimated_schema_tokens'])} |")

    largest_tools = [
        {"server": row["server_name"], **tool}
        for row in inventory
        for tool in row.get("largest_tools", [])
    ]
    largest_tools.sort(key=lambda item: item["schema_chars"], reverse=True)
    lines.extend(
        [
            "",
            "## Largest tools",
            "",
            "| Server | Tool | Schema chars | Estimated tokens |",
            "|---|---|---:|---:|",
        ]
    )
    for tool in largest_tools[:20]:
        lines.append(f"| {tool['server']} | {tool['tool_name']} | {tool['schema_chars']} | {tool['estimated_tokens']} |")

    lines.extend(
        [
            "",
            "## What this explains",
            "",
            f"- Measured schema estimate for current config: `{total_tokens}` rough tokens.",
            f"- Previous observed overhead: `{format_delta(baseline)}` input tokens.",
            f"- Schema available for `{schema_available_count}` servers.",
        ]
    )
    if baseline and total_tokens:
        if total_tokens >= baseline * 0.75:
            lines.append("- Estimate is close enough to support schema overhead hypothesis.")
        else:
            lines.append("- Estimate is much lower than overhead; routing/context/inventory metadata likely also matters.")
    else:
        lines.append("- Schemas are mostly unavailable, so conclusion is limited.")

    lines.extend(
        [
            "",
            "## Confirmed facts",
            "",
            f"- Current config server count from compare summary: `{summary['totals']['server_count_current']}`.",
            f"- Minimal config server count from compare summary: `{summary['totals']['server_count_minimal']}`.",
            f"- Servers with unavailable schema: `{len(summary['servers_with_unavailable_schema'])}`.",
            "- No real tool calls were executed by this inventory script.",
            "",
            "## Likely interpretation",
            "",
            "- Current config has many more MCP servers than minimal config.",
            "- If schemas are unavailable, we can still see constant environment overhead, but cannot rank true schema weight.",
            "- Tool count and config metadata are weaker signals than real schema payload size.",
            "",
            "## Unknown / limitations",
            "",
            "- Это грубая оценка, не официальный tokenizer OpenAI. Она нужна только для относительного сравнения MCP servers.",
            "- Это не официальный billing number.",
            "- list_tools/schema discovery может отличаться от того, что реально попадает в model context.",
            "- OTel не дает точные per-server tokens.",
            "- Некоторые MCP schemas могли быть недоступны.",
            "",
            "## Recommended next step",
            "",
        ]
    )
    if schema_available_count:
        lines.append("Если schema inventory достаточно полезен: сделать MCP group attribution experiment по группам servers.")
    else:
        lines.append("Так как schemas недоступны: делать group attribution через реальные A/B micro-runs с разными MCP groups.")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).resolve()
    compare_summary_path = Path(args.compare_summary).resolve()
    activity_summary_path = Path(args.activity_summary).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    compare_summary = read_json(compare_summary_path)
    activity_summary = read_json(activity_summary_path)
    inventory = build_inventory(config_path, compare_summary)
    summary = build_summary(inventory, compare_summary, activity_summary)
    warnings = build_warnings(inventory, summary)

    write_jsonl(output_dir / "mcp_schema_inventory.jsonl", inventory)
    (output_dir / "mcp_schema_inventory_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_jsonl(output_dir / "mcp_schema_inventory_warnings.jsonl", warnings)
    (output_dir / "mcp_schema_inventory_report.md").write_text(build_report(inventory, summary), encoding="utf-8")
    (output_dir / "config.mcp_sections.sanitized.toml").write_text(
        build_sanitized_config_extract(inventory),
        encoding="utf-8",
    )
    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
