#!/usr/bin/env python3
"""
Build local MCP schema inventory, effective enabled-state audit artifacts,
and read-only tool environment inventory artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import tomllib
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit


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
    "client_secret",
)

TOOL_LIKE_KEYWORDS = (
    "tool",
    "tools",
    "plugin",
    "plugins",
    "mcp",
    "browser",
    "repl",
    "codex_apps",
    "app",
    "apps",
    "connector",
    "workspace",
)

INSTRUCTION_KEYWORDS = (
    "skill",
    "skills",
    "instruction",
    "instructions",
    "agent",
    "agents",
    "context",
    "autoload",
    "auto_load",
    "auto-load",
)

RUNTIME_INTERNAL_SERVER_NAMES = {
    "codex_apps",
    "node_repl",
    "workspace-developer",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build local Codex inventory artifacts.")
    parser.add_argument(
        "--mode",
        choices=("schema-inventory", "tool-environment"),
        default="schema-inventory",
        help="Artifact mode to build.",
    )
    parser.add_argument("--config", required=True, help="Path to Codex config.toml. Read-only.")
    parser.add_argument("--output-dir", required=True, help="Output dir for generated artifacts.")
    parser.add_argument("--compare-summary", help="Path to compare_summary.json.")
    parser.add_argument("--activity-summary", help="Path to tool_mcp_activity_summary.json.")
    parser.add_argument("--before-after-summary", help="Path to before_vs_after_4_mcp_summary.json.")
    parser.add_argument("--playwright-summary", help="Path to playwright_only_confirmation_summary.json.")
    parser.add_argument("--effective-summary", help="Path to effective_mcp_inventory_summary.json.")
    parser.add_argument("--before-after-report", help="Optional path to before_vs_after_4_mcp_report.md.")
    parser.add_argument("--playwright-report", help="Optional path to playwright_only_confirmation_report.md.")
    parser.add_argument("--effective-report", help="Optional path to effective_mcp_inventory_report.md.")
    return parser.parse_args()


def ensure_args(args: argparse.Namespace, *names: str) -> None:
    missing = [name for name in names if not getattr(args, name.replace("-", "_"), None)]
    if missing:
        joined = ", ".join(f"--{name}" for name in missing)
        raise SystemExit(f"Missing required arguments for mode '{args.mode}': {joined}")


def load_toml(path: Path) -> dict[str, Any]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_json_if_exists(path_value: str | None, warnings: list[str], warning_name: str) -> dict[str, Any] | None:
    if not path_value:
        warnings.append(warning_name)
        return None
    path = Path(path_value).resolve()
    if not path.exists():
        warnings.append(warning_name)
        return None
    return read_json(path)


def check_path_exists(path_value: str | None, warnings: list[str], warning_name: str) -> Path | None:
    if not path_value:
        warnings.append(warning_name)
        return None
    path = Path(path_value).resolve()
    if not path.exists():
        warnings.append(warning_name)
        return None
    return path


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


def sanitize_url(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    parts = urlsplit(value)
    if parts.netloc:
        path = parts.path or "/"
        return f"{parts.netloc}{path}"
    if parts.path:
        return parts.path
    return None


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


def load_mcp_config(config_path: Path) -> dict[str, dict[str, Any]]:
    data = load_toml(config_path)
    servers = data.get("mcp_servers", {})
    if not isinstance(servers, dict):
        return {}
    return {str(name): config for name, config in servers.items() if isinstance(config, dict)}


def load_plugins_config(config_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    plugins = config_data.get("plugins", {})
    if not isinstance(plugins, dict):
        return {}
    return {str(name): config for name, config in plugins.items() if isinstance(config, dict)}


def enabled_state(section_config: dict[str, Any] | None) -> tuple[Any, Any, str]:
    if not section_config:
        return None, "unknown", "config_missing"
    enabled = section_config.get("enabled")
    if enabled is True:
        return True, True, "explicit_true"
    if enabled is False:
        return False, False, "explicit_false"
    if "enabled" not in section_config:
        return None, True, "implicit_default_true"
    return enabled, "unknown", "unknown"


def mismatch_interpretation(server_name: str, flags: list[str]) -> str:
    if "observed_current_but_config_disabled" in flags:
        return (
            f"Old current telemetry observed `{server_name}`, but current config snapshot marks it disabled. "
            "Previous run may have used older config, or telemetry may report configured servers rather than effective enabled servers."
        )
    if "observed_minimal_but_config_disabled" in flags:
        return (
            f"Minimal telemetry observed `{server_name}`, but current config snapshot marks it disabled. "
            "Observed server list may come from another config state or non-effective inventory semantics."
        )
    if "observed_current_but_config_missing" in flags:
        return (
            f"Current telemetry observed `{server_name}`, but this server is absent from current config snapshot. "
            "Telemetry may include synthetic/runtime-only inventory or snapshot drift exists."
        )
    if "config_enabled_but_not_observed_current" in flags:
        return (
            f"Current config can enable `{server_name}`, but old current telemetry did not observe it. "
            "Server may be lazy, unavailable during run, or telemetry list may be incomplete."
        )
    if "config_disabled_but_observed_current" in flags:
        return (
            f"`{server_name}` is explicitly disabled now, yet old current telemetry observed it. "
            "This is direct config-versus-telemetry drift."
        )
    if "source_ambiguous" in flags:
        return f"Source attribution for `{server_name}` is ambiguous."
    return f"Mismatch detected for `{server_name}`."


def mismatch_risk(flags: list[str]) -> str:
    if any(
        flag in flags
        for flag in (
            "observed_current_but_config_disabled",
            "observed_current_but_config_missing",
            "config_disabled_but_observed_current",
        )
    ):
        return "high"
    if any(
        flag in flags
        for flag in (
            "config_enabled_but_not_observed_current",
            "observed_minimal_but_config_disabled",
            "source_ambiguous",
        )
    ):
        return "medium"
    return "low"


def build_server_row(
    server_name: str,
    server_config: dict[str, Any],
    source: str,
    observed_in_current: bool,
    observed_in_minimal: bool,
) -> dict[str, Any]:
    config_present = bool(server_config)
    env = server_config.get("env", {})
    if not isinstance(env, dict):
        env = {}
    env_keys = sorted(str(key) for key in env.keys())
    tools = server_config.get("tools", {})
    if not isinstance(tools, dict):
        tools = {}
    enabled_raw, effective_enabled, enabled_source = enabled_state(server_config if config_present else None)

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
    if config_present and not tool_names:
        warnings.append("no_tools_found")

    mismatch_flags: list[str] = []
    if observed_in_current and effective_enabled is False:
        mismatch_flags.append("observed_current_but_config_disabled")
    if observed_in_minimal and effective_enabled is False:
        mismatch_flags.append("observed_minimal_but_config_disabled")
    if observed_in_current and not config_present:
        mismatch_flags.append("observed_current_but_config_missing")
    if effective_enabled is True and not observed_in_current:
        mismatch_flags.append("config_enabled_but_not_observed_current")
    if enabled_source == "explicit_false" and observed_in_current:
        mismatch_flags.append("config_disabled_but_observed_current")
    if source == "unknown":
        mismatch_flags.append("source_ambiguous")

    return {
        "server_name": server_name,
        "source": source,
        "config_present": config_present,
        "enabled_raw": enabled_raw,
        "effective_enabled": effective_enabled,
        "enabled_source": enabled_source,
        "observed_in_current_telemetry": observed_in_current,
        "observed_in_minimal_telemetry": observed_in_minimal,
        "mismatch_flags": mismatch_flags,
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


def build_inventory(config_path: Path, compare_summary: dict[str, Any]) -> list[dict[str, Any]]:
    config_servers = load_mcp_config(config_path)
    current_servers = set(mode_servers(compare_summary, "A-current-config"))
    minimal_servers = set(mode_servers(compare_summary, "B-minimal-config"))
    all_servers = sorted(set(config_servers.keys()) | current_servers | minimal_servers)
    rows = []
    for server_name in all_servers:
        source = source_for_server(server_name, current_servers, minimal_servers, set(config_servers.keys()))
        rows.append(
            build_server_row(
                server_name,
                config_servers.get(server_name, {}),
                source,
                observed_in_current=server_name in current_servers,
                observed_in_minimal=server_name in minimal_servers,
            )
        )
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
    effective_enabled_rows = [row for row in inventory if row["effective_enabled"] is True]
    explicit_disabled_rows = [row for row in inventory if row["enabled_source"] == "explicit_false"]
    mismatch_rows = [row for row in inventory if row["mismatch_flags"]]
    mismatches = [
        {
            "server_name": row["server_name"],
            "flags": row["mismatch_flags"],
            "interpretation": mismatch_interpretation(row["server_name"], row["mismatch_flags"]),
        }
        for row in mismatch_rows
    ]
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
        "counts": {
            "configured_server_count": sum(1 for row in inventory if row["config_present"]),
            "effective_enabled_server_count": len(effective_enabled_rows),
            "explicit_disabled_server_count": len(explicit_disabled_rows),
            "observed_current_telemetry_count": sum(1 for row in inventory if row["observed_in_current_telemetry"]),
            "observed_minimal_telemetry_count": sum(1 for row in inventory if row["observed_in_minimal_telemetry"]),
            "mismatch_count": len(mismatch_rows),
        },
        "servers": [
            {
                "server_name": row["server_name"],
                "config_present": row["config_present"],
                "enabled_raw": row["enabled_raw"],
                "effective_enabled": row["effective_enabled"],
                "enabled_source": row["enabled_source"],
                "transport": row["transport"],
                "command_safe": row["command_safe"],
                "observed_in_current_telemetry": row["observed_in_current_telemetry"],
                "observed_in_minimal_telemetry": row["observed_in_minimal_telemetry"],
                "mismatch_flags": row["mismatch_flags"],
            }
            for row in inventory
        ],
        "mismatches": mismatches,
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


def build_effective_summary(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    mismatches = []
    for row in inventory:
        if not row["mismatch_flags"]:
            continue
        mismatches.append(
            {
                "server_name": row["server_name"],
                "flags": row["mismatch_flags"],
                "interpretation": mismatch_interpretation(row["server_name"], row["mismatch_flags"]),
                "risk_for_next_test": mismatch_risk(row["mismatch_flags"]),
            }
        )

    mismatch_count = len(mismatches)
    if mismatch_count:
        recommended_next_step = (
            "Есть mismatch. Сначала нужен tiny confirmation run 'current effective config first turn', "
            "потом уже MCP group attribution experiment."
        )
    else:
        recommended_next_step = "Существенных mismatch нет. Можно планировать MCP group attribution от текущего effective baseline."

    return {
        "metadata": {
            "source": "config.toml read-only + compare_summary telemetry observed server lists",
            "live_config_modified": False,
            "raw_otel_read": False,
        },
        "counts": {
            "configured_server_count": sum(1 for row in inventory if row["config_present"]),
            "effective_enabled_server_count": sum(1 for row in inventory if row["effective_enabled"] is True),
            "explicit_disabled_server_count": sum(1 for row in inventory if row["enabled_source"] == "explicit_false"),
            "observed_current_telemetry_count": sum(1 for row in inventory if row["observed_in_current_telemetry"]),
            "observed_minimal_telemetry_count": sum(1 for row in inventory if row["observed_in_minimal_telemetry"]),
            "mismatch_count": mismatch_count,
        },
        "servers": [
            {
                "server_name": row["server_name"],
                "config_present": row["config_present"],
                "enabled_raw": row["enabled_raw"],
                "effective_enabled": row["effective_enabled"],
                "enabled_source": row["enabled_source"],
                "transport": row["transport"],
                "command_safe": row["command_safe"],
                "observed_in_current_telemetry": row["observed_in_current_telemetry"],
                "observed_in_minimal_telemetry": row["observed_in_minimal_telemetry"],
                "mismatch_flags": row["mismatch_flags"],
            }
            for row in inventory
        ],
        "mismatches": mismatches,
        "recommended_next_step": recommended_next_step,
    }


def build_warnings(inventory: list[dict[str, Any]], summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [{"warning": "token_estimate_rough", "severity": "info", "server_name": None}]
    for row in inventory:
        for warning in row["warnings"]:
            rows.append({"warning": warning, "severity": "warning", "server_name": row["server_name"]})
        for mismatch_flag in row["mismatch_flags"]:
            rows.append({"warning": mismatch_flag, "severity": "warning", "server_name": row["server_name"]})
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
        lines.append(f"config_present = {str(row['config_present']).lower()}")
        if row["enabled_raw"] is None:
            lines.append("enabled_raw = null")
        else:
            lines.append(f"enabled_raw = {str(row['enabled_raw']).lower()}")
        effective_enabled = row["effective_enabled"]
        if isinstance(effective_enabled, bool):
            lines.append(f"effective_enabled = {str(effective_enabled).lower()}")
        else:
            lines.append(f'effective_enabled = "{effective_enabled}"')
        lines.append(f'enabled_source = "{row["enabled_source"]}"')
        lines.append(f'observed_in_current_telemetry = {str(row["observed_in_current_telemetry"]).lower()}')
        lines.append(f'observed_in_minimal_telemetry = {str(row["observed_in_minimal_telemetry"]).lower()}')
        if row.get("command_safe"):
            lines.append(f'command_safe = "{row["command_safe"]}"')
        lines.append(f'transport = "{row["transport"]}"')
        lines.append(f"args_count = {row['args_count']}")
        lines.append(f"env_keys_count = {row['env_keys_count']}")
        if row["env_keys_sanitized"]:
            keys = ", ".join(json.dumps(key, ensure_ascii=False) for key in row["env_keys_sanitized"])
            lines.append(f"env_keys_sanitized = [{keys}]")
        if row["mismatch_flags"]:
            flags = ", ".join(json.dumps(flag, ensure_ascii=False) for flag in row["mismatch_flags"])
            lines.append(f"mismatch_flags = [{flags}]")
        lines.append("")
    return "\n".join(lines)


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


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
        "| Server | Source | Effective enabled | Transport | Tool count | Estimated schema tokens | Warnings |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for row in inventory:
        warnings = ", ".join(row["warnings"])
        lines.append(
            f"| {row['server_name']} | {row['source']} | {fmt(row['effective_enabled'])} | {row['transport']} | "
            f"{fmt(row['tool_count'])} | {fmt(row['estimated_schema_tokens'])} | {warnings} |"
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

    largest_tools = [{"server": row["server_name"], **tool} for row in inventory for tool in row.get("largest_tools", [])]
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


def build_effective_report(effective_summary: dict[str, Any], compare_summary: dict[str, Any]) -> str:
    counts = effective_summary["counts"]
    baseline = compare_summary.get("comparisons", {}).get("baseline_overhead", {}).get("A1_minus_B1_input_tokens")
    lines = [
        "# Effective MCP Inventory Report",
        "",
        "## Цель",
        "",
        "Проверить, какие MCP servers реально включены по текущему config, какие только прописаны, а какие были видны в старой telemetry.",
        "",
        "## Почему это важно",
        "",
        "- старый compare показал +10.1k overhead при 13 observed MCP servers;",
        "- текущий sanitized config содержит enabled=false у части servers;",
        "- перед group attribution нельзя путать configured и enabled.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Configured servers | {counts['configured_server_count']} |",
        f"| Effective enabled servers | {counts['effective_enabled_server_count']} |",
        f"| Explicit disabled servers | {counts['explicit_disabled_server_count']} |",
        f"| Observed in current telemetry | {counts['observed_current_telemetry_count']} |",
        f"| Observed in minimal telemetry | {counts['observed_minimal_telemetry_count']} |",
        f"| Mismatches | {counts['mismatch_count']} |",
        "",
        "## Server table",
        "",
        "| Server | Config present | Effective enabled | Enabled source | Transport | Observed current | Observed minimal | Mismatch flags |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in effective_summary["servers"]:
        flags = ", ".join(row["mismatch_flags"])
        lines.append(
            f"| {row['server_name']} | {fmt(row['config_present'])} | {fmt(row['effective_enabled'])} | "
            f"{row['enabled_source']} | {row['transport']} | {fmt(row['observed_in_current_telemetry'])} | "
            f"{fmt(row['observed_in_minimal_telemetry'])} | {flags} |"
        )

    lines.extend(["", "## Mismatches", ""])
    if not effective_summary["mismatches"]:
        lines.append("Mismatch не найден.")
    else:
        for mismatch in effective_summary["mismatches"]:
            lines.append(f"- `{mismatch['server_name']}`")
            lines.append(f"  flags: `{', '.join(mismatch['flags'])}`")
            lines.append(f"  meaning: {mismatch['interpretation']}")
            lines.append(f"  risk for next test: `{mismatch['risk_for_next_test']}`")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "### Confirmed facts",
            "",
            f"- Текущий read-only config содержит `{counts['configured_server_count']}` configured MCP sections.",
            f"- Из них effective enabled по config semantics: `{counts['effective_enabled_server_count']}`.",
            f"- Явно disabled: `{counts['explicit_disabled_server_count']}`.",
            f"- В старой current telemetry observed servers: `{counts['observed_current_telemetry_count']}`.",
            f"- В старой minimal telemetry observed servers: `{counts['observed_minimal_telemetry_count']}`.",
            "",
            "### Likely interpretation",
            "",
        ]
    )
    if counts["mismatch_count"]:
        lines.append(
            f"- Есть `{counts['mismatch_count']}` mismatch. Старый `{format_delta(baseline)}` overhead относится к старому observed current config, "
            "а не гарантированно к текущему effective config."
        )
        lines.append("- Перед group attribution нужен confirmation run от текущего effective baseline.")
    else:
        lines.append("- Существенных mismatch нет. Старый baseline похож на текущий effective baseline.")
        lines.append("- Group attribution можно планировать без дополнительного confirmation run.")

    lines.extend(
        [
            "",
            "### What this does NOT prove",
            "",
            "- не доказывает, что disabled server попадает в model context;",
            "- не доказывает token contribution каждого server;",
            "- не заменяет controlled group attribution runs.",
            "",
            "## Recommended next step",
            "",
            effective_summary["recommended_next_step"],
        ]
    )
    return "\n".join(lines) + "\n"


def sha256_text(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def keyword_match(value: str) -> bool:
    normalized = value.lower()
    tokens = [token for token in re.split(r"[^a-z0-9]+", normalized) if token]
    if "codex_apps" in normalized:
        return True
    if any(keyword in normalized for keyword in ("plugin", "plugins", "browser", "connector", "workspace")):
        return True
    if "mcp" in normalized or normalized.endswith("repl") or "_repl" in normalized:
        return True
    return any(token in {"tool", "tools", "app", "apps"} for token in tokens)


def safe_scalar(value: Any) -> Any:
    if isinstance(value, bool | int | float):
        return value
    if value is None:
        return None
    if isinstance(value, str):
        if value.startswith("http://") or value.startswith("https://"):
            return sanitize_url(value)
        if "\\" in value or "/" in value:
            return command_safe(value)
        return value
    return None


def size_bytes(path: Path) -> int | None:
    try:
        return path.stat().st_size
    except OSError:
        return None


def approx_tokens_from_size(size: int | None) -> int | None:
    if size is None:
        return None
    return math.ceil(size / 4)


def plugin_kind_source(plugin_name: str) -> str:
    lower = plugin_name.lower()
    if "@openai-curated" in lower:
        return "openai-curated"
    if "@openai-bundled" in lower:
        return "openai-bundled"
    if "github" in lower:
        return "github"
    return "unknown"


def may_provide_tools_context(plugin_name: str, effective_enabled: Any) -> str:
    if effective_enabled is False:
        return "no"
    if "@openai-curated" in plugin_name.lower() or "@openai-bundled" in plugin_name.lower():
        return "yes"
    if effective_enabled is True:
        return "yes"
    return "unknown"


def is_runtime_internal_candidate(name: str) -> bool:
    lower = name.lower()
    return lower in RUNTIME_INTERNAL_SERVER_NAMES or lower.startswith("codex_")


def is_user_mcp(name: str) -> bool:
    return not is_runtime_internal_candidate(name)


def build_plugin_rows(config_data: dict[str, Any]) -> list[dict[str, Any]]:
    plugins = load_plugins_config(config_data)
    rows = []
    for plugin_name in sorted(plugins.keys()):
        plugin_config = plugins.get(plugin_name, {})
        enabled_raw, effective_enabled, _ = enabled_state(plugin_config)
        kind_source = plugin_kind_source(plugin_name)
        rows.append(
            {
                "name": plugin_name,
                "enabled_raw": enabled_raw,
                "effective_enabled": effective_enabled,
                "kind_source": kind_source,
                "is_openai_curated_candidate": "@openai-curated" in plugin_name.lower(),
                "may_provide_tools_context": may_provide_tools_context(plugin_name, effective_enabled),
                "notes": [],
            }
        )
    return rows


def build_mcp_rows(config_data: dict[str, Any], observed_playwright_servers: list[str]) -> list[dict[str, Any]]:
    servers = load_mcp_config_from_data(config_data)
    rows = []
    observed_set = set(observed_playwright_servers)
    for name in sorted(servers.keys()):
        server_config = servers[name]
        enabled_raw, effective_enabled, _ = enabled_state(server_config)
        rows.append(
            {
                "name": name,
                "enabled_raw": enabled_raw,
                "effective_enabled": effective_enabled,
                "transport": detect_transport(server_config),
                "command_safe": command_safe(server_config.get("command")),
                "url_safe": sanitize_url(server_config.get("url") or server_config.get("endpoint")),
                "env_key_names": sorted(str(key) for key in server_config.get("env", {}).keys())
                if isinstance(server_config.get("env"), dict)
                else [],
                "is_user_mcp": is_user_mcp(name),
                "is_runtime_internal_candidate": is_runtime_internal_candidate(name) or name in observed_set and not is_user_mcp(name),
                "notes": [],
            }
        )
    return rows


def load_mcp_config_from_data(config_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    servers = config_data.get("mcp_servers", {})
    if not isinstance(servers, dict):
        return {}
    return {str(name): config for name, config in servers.items() if isinstance(config, dict)}


def load_skills_config_entries(config_data: dict[str, Any]) -> list[dict[str, Any]]:
    skills = config_data.get("skills", {})
    if not isinstance(skills, dict):
        return []
    entries = skills.get("config", [])
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


def build_configured_skill_candidates(config_data: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, entry in enumerate(load_skills_config_entries(config_data), start=1):
        path_value = entry.get("path")
        name_value = entry.get("name")
        enabled_raw = entry.get("enabled")
        path_obj = Path(path_value) if isinstance(path_value, str) and path_value else None
        exists = path_obj.exists() if path_obj else False
        size = size_bytes(path_obj) if path_obj and exists else None
        if enabled_raw is True:
            likely = "yes"
        elif enabled_raw is False:
            likely = "no"
        else:
            likely = "unknown"
        notes = []
        if name_value:
            notes.append("named skill entry")
        if path_obj:
            notes.append("path configured")
        if enabled_raw is False:
            notes.append("disabled in config")
        elif enabled_raw is True:
            notes.append("enabled in config")
        rows.append(
            {
                "index": index,
                "name": str(name_value) if isinstance(name_value, str) else None,
                "path": str(path_obj) if path_obj else None,
                "exists": exists,
                "size_bytes": size,
                "approx_tokens": approx_tokens_from_size(size),
                "enabled_raw": enabled_raw if isinstance(enabled_raw, bool) else None,
                "likely_auto_loaded": likely,
                "notes": notes,
            }
        )
    return rows


def instruction_keyword_match(value: str) -> bool:
    normalized = value.lower()
    return any(keyword in normalized for keyword in INSTRUCTION_KEYWORDS)


def build_global_instruction_candidates(config_data: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    def walk(value: Any, path: list[str]) -> None:
        if isinstance(value, dict):
            path_text = ".".join(path)
            matching_keys = sorted(str(key) for key in value.keys() if instruction_keyword_match(str(key)))
            if path_text and (instruction_keyword_match(path_text) or matching_keys):
                if path_text not in seen:
                    seen.add(path_text)
                    scalar_flags: dict[str, Any] = {}
                    for key, item in value.items():
                        if isinstance(item, (bool, int, float, str)):
                            item_safe = safe_scalar(item)
                            if item_safe not in (None, ""):
                                scalar_flags[str(key)] = item_safe
                    rows.append(
                        {
                            "section_path": path_text,
                            "matching_keys": matching_keys,
                            "scalar_flags": scalar_flags,
                            "likely_auto_loaded": "yes" if path and path[0] in {"agents", "skills"} else "unknown",
                            "notes": ["config keyword match"],
                        }
                    )
            for key, item in value.items():
                walk(item, path + [str(key)])
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, path + [f"[{index}]"])

    walk(config_data, [])
    for row in build_configured_skill_candidates(config_data):
        rows.append(
            {
                "section_path": f"skills.config[{row['index']}]",
                "matching_keys": ["path" if row["path"] else "name"],
                "scalar_flags": {"enabled_raw": row["enabled_raw"]} if row["enabled_raw"] is not None else {},
                "likely_auto_loaded": row["likely_auto_loaded"],
                "notes": ["configured skill path or name"],
            }
        )
    rows.sort(key=lambda row: row["section_path"])
    return rows


def repo_instruction_note(relative_path: str) -> tuple[str, str]:
    normalized = relative_path.replace("\\", "/")
    if normalized == "AGENTS.md":
        return "yes", "root agent instructions"
    if normalized == "README.md":
        return "yes", "root repo readme"
    if normalized in {".ai/README.md", ".ai/repo_navigation.md", ".ai/project_state.md"}:
        return "unknown", "high-value workflow context"
    if normalized.startswith(".ai/policies/"):
        return "unknown", "policy candidate"
    if normalized.startswith(".ai/subprojects/"):
        return "unknown", "subproject workflow docs"
    return "no", "repo markdown candidate"


def build_repo_instruction_files(repo_root: Path) -> list[dict[str, Any]]:
    candidates: list[Path] = []
    for relative in ("AGENTS.md", "README.md"):
        path = repo_root / relative
        if path.exists():
            candidates.append(path)
    ai_root = repo_root / ".ai"
    if ai_root.exists():
        candidates.extend(sorted(ai_root.rglob("*.md")))

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in candidates:
        relative = path.relative_to(repo_root).as_posix()
        if relative in seen:
            continue
        seen.add(relative)
        likely, note = repo_instruction_note(relative)
        size = size_bytes(path)
        rows.append(
            {
                "path": relative,
                "name": path.name,
                "exists": True,
                "size_bytes": size,
                "approx_tokens": approx_tokens_from_size(size),
                "likely_auto_loaded": likely,
                "notes": [note],
            }
        )
    rows.sort(key=lambda row: row["path"])
    return rows


def build_skills_and_instructions(repo_root: Path, config_data: dict[str, Any]) -> dict[str, Any]:
    configured_skills = build_configured_skill_candidates(config_data)
    repo_files = build_repo_instruction_files(repo_root)
    global_candidates = build_global_instruction_candidates(config_data)
    largest_files = sorted(repo_files, key=lambda row: row["size_bytes"] or 0, reverse=True)[:10]

    likely_auto_loaded: list[dict[str, Any]] = []
    for row in configured_skills:
        if row["likely_auto_loaded"] != "no":
            likely_auto_loaded.append(
                {
                    "kind": "configured_skill",
                    "id": row["path"] or row["name"] or f"skill-{row['index']}",
                    "likely_auto_loaded": row["likely_auto_loaded"],
                    "notes": row["notes"],
                }
            )
    for row in repo_files:
        if row["likely_auto_loaded"] in {"yes", "unknown"}:
            likely_auto_loaded.append(
                {
                    "kind": "repo_instruction_file",
                    "id": row["path"],
                    "likely_auto_loaded": row["likely_auto_loaded"],
                    "notes": row["notes"],
                }
            )

    warnings: list[str] = []
    agents_row = next((row for row in repo_files if row["path"] == "AGENTS.md"), None)
    if agents_row and (agents_row["size_bytes"] or 0) >= 20_000:
        warnings.append("large_agents_md_candidate")
    if len([row for row in repo_files if row["path"].startswith(".ai/")]) >= 100:
        warnings.append("many_ai_markdown_files")
    if configured_skills:
        warnings.append("configured_skills_present")

    return {
        "configured_skill_candidates": configured_skills,
        "repo_instruction_files": repo_files,
        "global_instruction_candidates": global_candidates,
        "largest_instruction_files": largest_files,
        "likely_auto_loaded_candidates": likely_auto_loaded,
        "warnings": warnings,
    }


def collect_other_tool_like_sections(config_data: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    def walk(value: Any, path: list[str]) -> None:
        if isinstance(value, dict):
            path_text = ".".join(path)
            if path and path[0] not in {"mcp_servers", "plugins", "projects"}:
                matching_keys = sorted(str(key) for key in value.keys() if keyword_match(str(key)))
                if keyword_match(path_text) or matching_keys:
                    if path_text not in seen:
                        seen.add(path_text)
                        scalar_flags: dict[str, Any] = {}
                        for key, item in value.items():
                            if isinstance(item, (bool, int, float, str)):
                                item_safe = safe_scalar(item)
                                if item_safe not in (None, ""):
                                    scalar_flags[str(key)] = item_safe
                        rows.append(
                            {
                                "section_path": path_text,
                                "matching_keys": matching_keys,
                                "scalar_flags": scalar_flags,
                            }
                        )
            for key, item in value.items():
                walk(item, path + [str(key)])
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, path + [f"[{index}]"])

    walk(config_data, [])
    rows.sort(key=lambda row: row["section_path"])
    return rows


def telemetry_context(
    before_after_summary: dict[str, Any] | None,
    playwright_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    baseline = {}
    after = {}
    playwright = {}
    if before_after_summary:
        baseline = {
            "input_tokens": before_after_summary.get("baseline", {}).get("selected_turn", {}).get("input_tokens"),
            "observed_mcp_server_count": before_after_summary.get("baseline", {}).get("observed_mcp", {}).get("server_count"),
        }
        after = {
            "input_tokens": before_after_summary.get("after", {}).get("selected_turn", {}).get("input_tokens"),
            "observed_mcp_server_count": before_after_summary.get("after", {}).get("observed_mcp", {}).get("server_count"),
        }
    if playwright_summary:
        playwright = {
            "input_tokens": playwright_summary.get("selected_turn", {}).get("input_tokens"),
            "output_tokens": playwright_summary.get("selected_turn", {}).get("output_tokens"),
            "cached_tokens": playwright_summary.get("selected_turn", {}).get("cached_tokens"),
            "reasoning_tokens": playwright_summary.get("selected_turn", {}).get("reasoning_tokens"),
            "tool_tokens": playwright_summary.get("selected_turn", {}).get("tool_tokens"),
            "observed_mcp_server_count": playwright_summary.get("observed_mcp", {}).get("server_count"),
            "observed_mcp_servers": playwright_summary.get("observed_mcp", {}).get("servers", []),
        }
    return {
        "old_current_a1": baseline,
        "after_4_mcp": after,
        "playwright_only": playwright,
    }


def build_runtime_internal_candidates(mcp_rows: list[dict[str, Any]], telemetry: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in mcp_rows:
        if row["is_runtime_internal_candidate"]:
            seen.add(row["name"])
            rows.append(
                {
                    "name": row["name"],
                    "source": "config",
                    "reason": "runtime/internal candidate in current config",
                }
            )
    for name in telemetry.get("playwright_only", {}).get("observed_mcp_servers", []):
        if is_runtime_internal_candidate(name) and name not in seen:
            seen.add(name)
            rows.append(
                {
                    "name": name,
                    "source": "telemetry_only",
                    "reason": "observed in telemetry but not present as user MCP section",
                }
            )
    return rows


def build_interpretation(
    mcp_rows: list[dict[str, Any]],
    plugin_rows: list[dict[str, Any]],
    telemetry: dict[str, Any],
) -> str:
    enabled_plugins = [row["name"] for row in plugin_rows if row["effective_enabled"] is True]
    mcp_names = [row["name"] for row in mcp_rows]
    playwright_only = telemetry.get("playwright_only", {})
    observed_count = playwright_only.get("observed_mcp_server_count")
    input_tokens = playwright_only.get("input_tokens")

    if "playwright" in mcp_names and "node_repl" in mcp_names and observed_count == 3 and input_tokens:
        if enabled_plugins:
            return (
                "Physical MCP removal reduced observed MCP inventory from 13 to 3, but selected input tokens stayed high. "
                "User MCP sections are no longer the main suspect. Next suspect layer is enabled plugins plus runtime/internal tools "
                "such as codex_apps and node_repl."
            )
        return (
            "Physical MCP removal reduced observed MCP inventory from 13 to 3, but selected input tokens stayed high. "
            "Plugins are not the obvious driver, so main suspect becomes runtime/internal Codex Desktop layer: codex_apps, "
            "node_repl, app-server, and system context."
        )
    return "Inventory is incomplete or noisy. More separation between MCP, plugins, and runtime/internal layers is still needed."


def build_tool_environment_summary(
    config_path: Path,
    config_data: dict[str, Any],
    before_after_summary: dict[str, Any] | None,
    playwright_summary: dict[str, Any] | None,
    effective_summary: dict[str, Any] | None,
    warnings: list[str],
) -> dict[str, Any]:
    repo_root = Path.cwd()
    telemetry = telemetry_context(before_after_summary, playwright_summary)
    observed_playwright_servers = telemetry.get("playwright_only", {}).get("observed_mcp_servers", [])
    mcp_rows = build_mcp_rows(config_data, observed_playwright_servers)
    plugin_rows = build_plugin_rows(config_data)
    other_sections = collect_other_tool_like_sections(config_data)
    runtime_rows = build_runtime_internal_candidates(mcp_rows, telemetry)
    skills_and_instructions = build_skills_and_instructions(repo_root, config_data)
    openai_curated = [row["name"] for row in plugin_rows if row["is_openai_curated_candidate"]]
    enabled_plugins = [row["name"] for row in plugin_rows if row["effective_enabled"] is True]

    explicit_disabled_mcp = sum(1 for row in mcp_rows if row["effective_enabled"] is False)
    explicit_disabled_plugins = sum(1 for row in plugin_rows if row["effective_enabled"] is False)

    if not before_after_summary:
        warnings.append("missing_before_after_summary")
    if not playwright_summary:
        warnings.append("missing_playwright_summary")
    if not effective_summary:
        warnings.append("missing_effective_summary")

    return {
        "run_id": "tool-environment-inventory",
        "status": "ok",
        "config_path": str(config_path).replace("\\", "/"),
        "config_sha256": sha256_text(config_path),
        "mcp": {
            "configured_count": len(mcp_rows),
            "effective_enabled_count": sum(1 for row in mcp_rows if row["effective_enabled"] is True),
            "explicit_disabled_count": explicit_disabled_mcp,
            "servers": mcp_rows,
        },
        "plugins": {
            "configured_count": len(plugin_rows),
            "effective_enabled_count": len(enabled_plugins),
            "explicit_disabled_count": explicit_disabled_plugins,
            "plugins": plugin_rows,
        },
        "runtime_internal_candidates": runtime_rows,
        "openai_curated_plugin_candidates": openai_curated,
        "other_tool_like_sections": other_sections,
        "skills_and_instructions": skills_and_instructions,
        "telemetry_context": telemetry,
        "effective_inventory_context": effective_summary or {},
        "interpretation": build_interpretation(mcp_rows, plugin_rows, telemetry),
        "warnings": sorted(dict.fromkeys(warnings + skills_and_instructions["warnings"])),
    }


def build_tool_environment_report(summary: dict[str, Any]) -> str:
    mcp = summary["mcp"]
    plugins = summary["plugins"]
    telemetry = summary["telemetry_context"]
    skills = summary["skills_and_instructions"]
    enabled_plugins = [row["name"] for row in plugins["plugins"] if row["effective_enabled"] is True]
    runtime_names = [row["name"] for row in summary["runtime_internal_candidates"]]
    baseline = telemetry.get("old_current_a1", {})
    after = telemetry.get("after_4_mcp", {})
    playwright = telemetry.get("playwright_only", {})

    lines = [
        "# Tool Environment Inventory Report",
        "",
        "## Цель",
        "",
        "Понять, какие tool/runtime слои остаются после удаления почти всех пользовательских MCP, потому что input tokens не упали.",
        "",
        "## Почему это нужно",
        "",
        f"- MCP inventory упал с `{baseline.get('observed_mcp_server_count')}` до `{playwright.get('observed_mcp_server_count')}`.",
        f"- selected first-turn input tokens не упали: `{baseline.get('input_tokens')}` -> `{playwright.get('input_tokens')}`.",
        "- Значит надо проверить plugins, runtime/internal tools и похожие слои конфигурации.",
        "",
        "## MCP servers in current config",
        "",
        "| MCP | Enabled raw | Effective enabled | Transport | User MCP | Runtime/internal candidate | Notes |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in mcp["servers"]:
        notes = []
        if row["command_safe"]:
            notes.append(f"command={row['command_safe']}")
        if row["url_safe"]:
            notes.append(f"url={row['url_safe']}")
        if row["env_key_names"]:
            notes.append(f"env_keys={len(row['env_key_names'])}")
        lines.append(
            f"| {row['name']} | {fmt(row['enabled_raw'])} | {fmt(row['effective_enabled'])} | {row['transport']} | "
            f"{fmt(row['is_user_mcp'])} | {fmt(row['is_runtime_internal_candidate'])} | {'; '.join(notes)} |"
        )

    lines.extend(["", "## Plugins in current config", ""])
    if not plugins["plugins"]:
        lines.append("В текущем config `[plugins.*]` sections не найдены.")
    else:
        lines.extend(
            [
                "| Plugin | Enabled raw | Effective enabled | OpenAI curated candidate | May provide tools/context | Notes |",
                "|---|---|---|---|---|---|",
            ]
        )
        for row in plugins["plugins"]:
            notes = row["kind_source"]
            lines.append(
                f"| {row['name']} | {fmt(row['enabled_raw'])} | {fmt(row['effective_enabled'])} | "
                f"{fmt(row['is_openai_curated_candidate'])} | {row['may_provide_tools_context']} | {notes} |"
            )

    lines.extend(["", "## Other tool-like sections", ""])
    if not summary["other_tool_like_sections"]:
        lines.append("Другие tool-like sections не найдены.")
    else:
        lines.extend(["| Section | Matching keys | Notes |", "|---|---|---|"])
        for row in summary["other_tool_like_sections"]:
            notes = ", ".join(f"{key}={value}" for key, value in row["scalar_flags"].items()) or "metadata only"
            lines.append(f"| {row['section_path']} | {', '.join(row['matching_keys'])} | {notes} |")

    lines.extend(
        [
            "",
            "## Runtime/internal candidates",
            "",
        ]
    )
    if runtime_names:
        for row in summary["runtime_internal_candidates"]:
            lines.append(f"- `{row['name']}`: {row['reason']}")
    else:
        lines.append("- Явные runtime/internal candidates не выделены.")

    lines.extend(
        [
            "",
            "## Current interpretation",
            "",
            f"- old current A1: `{baseline.get('input_tokens')}` input / `{baseline.get('observed_mcp_server_count')}` observed MCP.",
            f"- after 4 MCP: `{after.get('input_tokens')}` input / `{after.get('observed_mcp_server_count')}` observed MCP.",
            f"- playwright-only: `{playwright.get('input_tokens')}` input / `{playwright.get('observed_mcp_server_count')}` observed MCP.",
            f"- Enabled plugins now: `{', '.join(enabled_plugins) if enabled_plugins else 'none'}`.",
            f"- Runtime/internal candidates now: `{', '.join(runtime_names) if runtime_names else 'none'}`.",
            "",
            summary["interpretation"],
            "",
            "## Next recommended test",
            "",
        ]
    )
    if enabled_plugins:
        lines.append(
            "Следующий самый маленький тест: temporary no-plugin/no-extra-tools run, не трогая runtime tools, чтобы проверить plugin overhead."
        )
    else:
        lines.append(
            "Следующий самый маленький тест: повторный clean playwright-only run или minimal-runtime run, чтобы проверить шум и baseline Codex Desktop."
        )

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- summary: `{summary['run_id']}`",
            f"- config sha256: `{summary['config_sha256']}`",
            "",
            "## Warnings",
            "",
        ]
    )
    if summary["warnings"]:
        for warning in summary["warnings"]:
            lines.append(f"- `{warning}`")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def build_skills_and_instructions_report_section(summary: dict[str, Any]) -> str:
    skills = summary["skills_and_instructions"]
    lines = [
        "",
        "## Skills / instructions / auto-loaded context candidates",
        "",
        f"- configured skill candidates: `{len(skills['configured_skill_candidates'])}`",
        f"- repo instruction files inventoried: `{len(skills['repo_instruction_files'])}`",
        f"- likely auto-loaded candidates: `{len(skills['likely_auto_loaded_candidates'])}`",
        "",
        "### Configured skills",
        "",
    ]
    if not skills["configured_skill_candidates"]:
        lines.append("Configured skills not found in config.")
    else:
        lines.extend(
            [
                "| Skill | Enabled raw | Exists | Size bytes | Approx tokens | Likely auto-loaded | Notes |",
                "|---|---|---|---:|---:|---|---|",
            ]
        )
        for row in skills["configured_skill_candidates"]:
            label = row["name"] or row["path"] or f"skill-{row['index']}"
            lines.append(
                f"| {label} | {fmt(row['enabled_raw'])} | {fmt(row['exists'])} | {row['size_bytes'] or 0} | "
                f"{row['approx_tokens'] or 0} | {row['likely_auto_loaded']} | {', '.join(row['notes']) or 'metadata only'} |"
            )

    lines.extend(["", "### Main repo instruction files", ""])
    primary_repo_files = [
        row
        for row in skills["repo_instruction_files"]
        if row["path"] in {"AGENTS.md", "README.md", ".ai/README.md", ".ai/repo_navigation.md", ".ai/project_state.md"}
    ]
    if not primary_repo_files:
        lines.append("Primary repo instruction files not found.")
    else:
        lines.extend(
            [
                "| Path | Size bytes | Approx tokens | Likely auto-loaded | Notes |",
                "|---|---:|---:|---|---|",
            ]
        )
        for row in primary_repo_files:
            lines.append(
                f"| {row['path']} | {row['size_bytes'] or 0} | {row['approx_tokens'] or 0} | {row['likely_auto_loaded']} | "
                f"{', '.join(row['notes'])} |"
            )

    lines.extend(["", "### Largest instruction files", ""])
    if not skills["largest_instruction_files"]:
        lines.append("Large instruction files not found.")
    else:
        lines.extend(["| Path | Size bytes | Approx tokens | Likely auto-loaded |", "|---|---:|---:|---|"])
        for row in skills["largest_instruction_files"]:
            lines.append(
                f"| {row['path']} | {row['size_bytes'] or 0} | {row['approx_tokens'] or 0} | {row['likely_auto_loaded']} |"
            )

    lines.extend(
        [
            "",
            "### Interpretation",
            "",
            "Large instruction and skill files can explain part of high input cost, especially when root AGENTS.md, root README.md, "
            "configured skill entries, or high-value .ai docs are likely auto-loaded.",
            "If nothing large looks auto-loaded, runtime/internal Codex Desktop overhead becomes stronger suspect.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_tool_environment_config_extract(summary: dict[str, Any]) -> str:
    lines = [
        "# Sanitized tool environment config extract.",
        "# Secrets, token values, cookies, auth headers, emails, account ids, and query strings are removed.",
        "",
    ]
    for row in summary["mcp"]["servers"]:
        lines.append(f"[mcp_servers.{row['name']}]")
        if row["enabled_raw"] is None:
            lines.append("enabled_raw = null")
        else:
            lines.append(f"enabled_raw = {str(row['enabled_raw']).lower()}")
        lines.append(f"effective_enabled = {fmt(row['effective_enabled'])}")
        lines.append(f'transport = "{row["transport"]}"')
        if row["command_safe"]:
            lines.append(f'command_safe = "{row["command_safe"]}"')
        if row["url_safe"]:
            lines.append(f'url_safe = "{row["url_safe"]}"')
        lines.append(f"is_user_mcp = {str(row['is_user_mcp']).lower()}")
        lines.append(f"is_runtime_internal_candidate = {str(row['is_runtime_internal_candidate']).lower()}")
        if row["env_key_names"]:
            keys = ", ".join(json.dumps(key, ensure_ascii=False) for key in row["env_key_names"])
            lines.append(f"env_key_names = [{keys}]")
        lines.append("")

    for row in summary["plugins"]["plugins"]:
        lines.append(f'[plugins."{row["name"]}"]')
        if row["enabled_raw"] is None:
            lines.append("enabled_raw = null")
        else:
            lines.append(f"enabled_raw = {str(row['enabled_raw']).lower()}")
        lines.append(f"effective_enabled = {fmt(row['effective_enabled'])}")
        lines.append(f'kind_source = "{row["kind_source"]}"')
        lines.append(f"is_openai_curated_candidate = {str(row['is_openai_curated_candidate']).lower()}")
        lines.append(f'may_provide_tools_context = "{row["may_provide_tools_context"]}"')
        lines.append("")

    for row in summary["other_tool_like_sections"]:
        lines.append(f'[other_tool_like_sections."{row["section_path"]}"]')
        if row["matching_keys"]:
            keys = ", ".join(json.dumps(key, ensure_ascii=False) for key in row["matching_keys"])
            lines.append(f"matching_keys = [{keys}]")
        for key, value in row["scalar_flags"].items():
            if isinstance(value, bool):
                lines.append(f"{key} = {str(value).lower()}")
            elif isinstance(value, (int, float)):
                lines.append(f"{key} = {value}")
            else:
                lines.append(f'{key} = {json.dumps(value, ensure_ascii=False)}')
        lines.append("")
    return "\n".join(lines)


def build_skills_and_instructions_config_extract(summary: dict[str, Any]) -> str:
    skills = summary["skills_and_instructions"]
    lines = [
        "",
        "# Skills and instructions metadata extract.",
        "# Content bodies are intentionally omitted.",
        "",
    ]

    for row in skills["configured_skill_candidates"]:
        label = row["name"] or row["path"] or f"skill_{row['index']}"
        lines.append(f'[skills_and_instructions.configured_skill_candidates."{label}"]')
        if row["path"]:
            lines.append(f'path = {json.dumps(row["path"], ensure_ascii=False)}')
        if row["name"]:
            lines.append(f'name = {json.dumps(row["name"], ensure_ascii=False)}')
        lines.append(f"exists = {str(row['exists']).lower()}")
        if row["enabled_raw"] is not None:
            lines.append(f"enabled_raw = {str(row['enabled_raw']).lower()}")
        if row["size_bytes"] is not None:
            lines.append(f"size_bytes = {row['size_bytes']}")
        if row["approx_tokens"] is not None:
            lines.append(f"approx_tokens = {row['approx_tokens']}")
        lines.append(f'likely_auto_loaded = "{row["likely_auto_loaded"]}"')
        lines.append("")

    for row in skills["largest_instruction_files"]:
        lines.append(f'[skills_and_instructions.largest_instruction_files."{row["path"]}"]')
        lines.append(f"size_bytes = {row['size_bytes'] or 0}")
        lines.append(f"approx_tokens = {row['approx_tokens'] or 0}")
        lines.append(f'likely_auto_loaded = "{row["likely_auto_loaded"]}"')
        lines.append("")

    for row in skills["global_instruction_candidates"]:
        lines.append(f'[skills_and_instructions.global_instruction_candidates."{row["section_path"]}"]')
        if row["matching_keys"]:
            keys = ", ".join(json.dumps(key, ensure_ascii=False) for key in row["matching_keys"])
            lines.append(f"matching_keys = [{keys}]")
        lines.append(f'likely_auto_loaded = "{row["likely_auto_loaded"]}"')
        lines.append("")
    return "\n".join(lines)


def run_schema_inventory(args: argparse.Namespace) -> int:
    ensure_args(args, "compare-summary", "activity-summary")
    config_path = Path(args.config).resolve()
    compare_summary_path = Path(args.compare_summary).resolve()
    activity_summary_path = Path(args.activity_summary).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    compare_summary = read_json(compare_summary_path)
    activity_summary = read_json(activity_summary_path)
    inventory = build_inventory(config_path, compare_summary)
    summary = build_summary(inventory, compare_summary, activity_summary)
    effective_summary = build_effective_summary(inventory)
    warnings = build_warnings(inventory, summary)

    write_jsonl(output_dir / "mcp_schema_inventory.jsonl", inventory)
    (output_dir / "mcp_schema_inventory_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "effective_mcp_inventory_summary.json").write_text(
        json.dumps(effective_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_jsonl(output_dir / "mcp_schema_inventory_warnings.jsonl", warnings)
    (output_dir / "mcp_schema_inventory_report.md").write_text(build_report(inventory, summary), encoding="utf-8")
    (output_dir / "effective_mcp_inventory_report.md").write_text(
        build_effective_report(effective_summary, compare_summary),
        encoding="utf-8",
    )
    (output_dir / "config.mcp_sections.sanitized.toml").write_text(
        build_sanitized_config_extract(inventory),
        encoding="utf-8",
    )
    print(output_dir)
    return 0


def run_tool_environment_inventory(args: argparse.Namespace) -> int:
    config_path = Path(args.config).resolve()
    config_data = load_toml(config_path)
    output_dir = Path(args.output_dir).resolve()
    reports_dir = output_dir / "reports"
    configs_dir = output_dir / "configs"
    reports_dir.mkdir(parents=True, exist_ok=True)
    configs_dir.mkdir(parents=True, exist_ok=True)

    warnings: list[str] = []
    before_after_summary = read_json_if_exists(args.before_after_summary, warnings, "missing_before_after_summary")
    playwright_summary = read_json_if_exists(args.playwright_summary, warnings, "missing_playwright_summary")
    effective_summary = read_json_if_exists(args.effective_summary, warnings, "missing_effective_summary")
    check_path_exists(args.before_after_report, warnings, "missing_before_after_report")
    check_path_exists(args.playwright_report, warnings, "missing_playwright_report")
    check_path_exists(args.effective_report, warnings, "missing_effective_report")

    summary = build_tool_environment_summary(
        config_path,
        config_data,
        before_after_summary,
        playwright_summary,
        effective_summary,
        warnings,
    )
    report_text = build_tool_environment_report(summary) + build_skills_and_instructions_report_section(summary)
    config_extract = build_tool_environment_config_extract(summary) + build_skills_and_instructions_config_extract(summary)

    (reports_dir / "tool_environment_inventory_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (reports_dir / "tool_environment_inventory_report.md").write_text(report_text, encoding="utf-8")
    (configs_dir / "config_tool_environment_sanitized.toml").write_text(config_extract, encoding="utf-8")
    print(output_dir)
    return 0


def main() -> int:
    args = parse_args()
    if args.mode == "tool-environment":
        return run_tool_environment_inventory(args)
    return run_schema_inventory(args)


if __name__ == "__main__":
    raise SystemExit(main())
