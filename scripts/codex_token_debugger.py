#!/usr/bin/env python3
"""
Local-only forensic parser for raw Codex OTel JSON/JSONL dumps.
Produces sanitized artifacts for token diagnostics without publishing raw telemetry.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


PRIVATE_ID_FIELDS = {
    "user.email",
    "user.account_id",
    "conversation.id",
    "host.name",
}

TOKEN_FIELD_PREFIXES = (
    "input_token_count",
    "output_token_count",
    "cached_token_count",
    "reasoning_token_count",
    "tool_token_count",
    "codex.turn.token_usage",
    "gen_ai.usage",
    "codex.usage",
    "token_type",
)

PROMPT_REDACTED_SENTINEL = "[REDACTED]"

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


@dataclass
class AnalysisState:
    raw_private_fields: Counter = field(default_factory=Counter)
    raw_token_fields: set[str] = field(default_factory=set)
    clean_events: list[dict[str, Any]] = field(default_factory=list)
    token_usage: list[dict[str, Any]] = field(default_factory=list)
    spans: list[dict[str, Any]] = field(default_factory=list)
    metrics: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)
    session_rows: list[dict[str, Any]] = field(default_factory=list)
    session_summary: dict[str, dict[str, Any]] = field(default_factory=dict)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse local raw Codex OTel JSON/JSONL into sanitized forensic artifacts.")
    parser.add_argument("--input", required=True, help="Path to local raw OTel JSON or JSONL file.")
    parser.add_argument("--output-dir", required=True, help="Directory for sanitized outputs.")
    parser.add_argument("--format", choices=("auto", "json", "jsonl"), default="auto", help="Input format. Default: auto.")
    return parser.parse_args()


def load_records(path: Path, fmt: str) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").lstrip("\ufeff").strip()
    if not text:
        raise ValueError("Input OTel file is empty.")

    candidates = []
    if fmt in {"auto", "json"}:
        candidates.append("json")
    if fmt in {"auto", "jsonl"}:
        candidates.append("jsonl")

    last_error: Exception | None = None
    for candidate in candidates:
        try:
            if candidate == "json":
                data = json.loads(text)
                if isinstance(data, list):
                    return [item for item in data if isinstance(item, dict)]
                if isinstance(data, dict):
                    return [data]
                raise ValueError("Unsupported JSON root type.")
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            return [json.loads(line) for line in lines]
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise ValueError(f"Cannot parse input as JSON/JSONL: {last_error}")


def any_value_to_python(value: dict[str, Any] | None) -> Any:
    if not isinstance(value, dict):
        return value
    if "stringValue" in value:
        return value["stringValue"]
    if "intValue" in value:
        raw = value["intValue"]
        try:
            return int(raw)
        except Exception:  # noqa: BLE001
            return raw
    if "doubleValue" in value:
        return float(value["doubleValue"])
    if "boolValue" in value:
        return bool(value["boolValue"])
    if "arrayValue" in value:
        values = value["arrayValue"].get("values", [])
        return [any_value_to_python(item) for item in values]
    if "kvlistValue" in value:
        values = value["kvlistValue"].get("values", [])
        return attributes_to_dict(values)
    if "bytesValue" in value:
        return value["bytesValue"]
    return value


def attributes_to_dict(attributes: Iterable[dict[str, Any]] | None) -> dict[str, Any]:
    result: dict[str, Any] = {}
    if not attributes:
        return result
    for attribute in attributes:
        key = attribute.get("key")
        if not key:
            continue
        result[key] = any_value_to_python(attribute.get("value"))
    return result


def sanitize_value(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            if is_private_field(key):
                continue
            if key == "prompt":
                cleaned[key] = sanitize_prompt_value(item)
                continue
            cleaned[key] = sanitize_value(item)
        return cleaned
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    return value


def sanitize_prompt_value(value: Any) -> Any:
    if value in ("", None, PROMPT_REDACTED_SENTINEL):
        return value
    return PROMPT_REDACTED_SENTINEL


def is_private_field(key: str) -> bool:
    normalized = key.lower()
    if key in PRIVATE_ID_FIELDS:
        return True
    return any(fragment in normalized for fragment in SENSITIVE_FIELD_FRAGMENTS)


def is_token_field(key: str) -> bool:
    return any(key == prefix or key.startswith(prefix + ".") for prefix in TOKEN_FIELD_PREFIXES)


def to_number(value: Any) -> int | float | None:
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return None
    return None


def unix_nano_to_iso(value: Any) -> str | None:
    number = to_number(value)
    if number is None:
        return None
    return datetime.fromtimestamp(number / 1_000_000_000, tz=timezone.utc).isoformat()


def duration_ms(start: Any, end: Any) -> float | None:
    start_num = to_number(start)
    end_num = to_number(end)
    if start_num is None or end_num is None:
        return None
    return round((end_num - start_num) / 1_000_000, 3)


def record_private_and_token_fields(attributes: dict[str, Any], state: AnalysisState) -> None:
    for key in attributes:
        if is_private_field(key):
            state.raw_private_fields[key] += 1
        if is_token_field(key):
            state.raw_token_fields.add(key)


def extract_session_key(service_name: str | None, model: str | None, attrs: dict[str, Any], trace_id: str | None) -> str:
    session_like = attrs.get("conversation.id") or attrs.get("thread_id") or attrs.get("rpc.request_id") or trace_id or "unknown"
    return f"{service_name or 'unknown'}|{model or 'unknown'}|{session_like}"


def get_session_entry(state: AnalysisState, key: str, service_name: str | None, model: str | None) -> dict[str, Any]:
    if key not in state.session_summary:
        state.session_summary[key] = {
            "session_key": key,
            "service_name": service_name or "unknown",
            "model": model or "unknown",
            "clean_event_count": 0,
            "span_count": 0,
            "metric_count": 0,
            "token_event_count": 0,
            "warning_count": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cached_tokens": 0,
            "reasoning_tokens": 0,
            "tool_tokens": 0,
            "trace_ids": set(),
        }
    return state.session_summary[key]


def append_warning(state: AnalysisState, warning_type: str, severity: str, summary: str, context: dict[str, Any]) -> None:
    state.warnings.append(
        sanitize_value(
            {
                "warning_type": warning_type,
                "severity": severity,
                "summary": summary,
                "context": context,
            }
        )
    )


def process_log_record(
    record: dict[str, Any],
    service_attrs: dict[str, Any],
    scope_name: str | None,
    state: AnalysisState,
) -> None:
    attrs = attributes_to_dict(record.get("attributes"))
    record_private_and_token_fields(attrs, state)
    service_name = service_attrs.get("service.name")
    model = attrs.get("model")
    session_key = extract_session_key(service_name, model, attrs, record.get("traceId"))
    session_entry = get_session_entry(state, session_key, service_name, model)
    session_entry["clean_event_count"] += 1
    if record.get("traceId"):
        session_entry["trace_ids"].add(record["traceId"])

    clean_event = sanitize_value(
        {
            "event_type": "log",
            "service_name": service_name,
            "service_version": service_attrs.get("service.version"),
            "scope_name": scope_name,
            "event_name": attrs.get("event.name") or record.get("eventName"),
            "severity_text": record.get("severityText"),
            "timestamp": unix_nano_to_iso(record.get("observedTimeUnixNano")),
            "traceId": record.get("traceId"),
            "spanId": record.get("spanId"),
            "attributes": attrs,
        }
    )
    state.clean_events.append(clean_event)

    token_payload = {key: to_number(value) for key, value in attrs.items() if is_token_field(key)}
    token_payload = {key: value for key, value in token_payload.items() if value is not None}
    if token_payload:
        state.token_usage.append(
            sanitize_value(
                {
                    "source_type": "log",
                    "service_name": service_name,
                    "scope_name": scope_name,
                    "event_name": attrs.get("event.name"),
                    "event_kind": attrs.get("event.kind"),
                    "timestamp": unix_nano_to_iso(record.get("observedTimeUnixNano")),
                    "traceId": record.get("traceId"),
                    "spanId": record.get("spanId"),
                    "model": model,
                    **token_payload,
                }
            )
        )
        session_entry["token_event_count"] += 1
        session_entry["input_tokens"] += int(token_payload.get("input_token_count", 0) or 0)
        session_entry["output_tokens"] += int(token_payload.get("output_token_count", 0) or 0)
        session_entry["cached_tokens"] += int(token_payload.get("cached_token_count", 0) or 0)
        session_entry["reasoning_tokens"] += int(token_payload.get("reasoning_token_count", 0) or 0)
        session_entry["tool_tokens"] += int(token_payload.get("tool_token_count", 0) or 0)

        input_tokens = int(token_payload.get("input_token_count", 0) or 0)
        output_tokens = int(token_payload.get("output_token_count", 0) or 0)
        cached_tokens = int(token_payload.get("cached_token_count", 0) or 0)
        reasoning_tokens = int(token_payload.get("reasoning_token_count", 0) or 0)
        tool_tokens = int(token_payload.get("tool_token_count", 0) or 0)

        if input_tokens >= 5000 and output_tokens <= max(200, int(input_tokens * 0.05)):
            append_warning(
                state,
                "high_input_low_output",
                "medium",
                "Высокий входной токен-поток при низком выходе.",
                {
                    "model": model,
                    "traceId": record.get("traceId"),
                    "input_token_count": input_tokens,
                    "output_token_count": output_tokens,
                },
            )
        if reasoning_tokens >= max(50, output_tokens):
            append_warning(
                state,
                "high_reasoning",
                "medium",
                "Reasoning tokens выглядят высокими относительно выхода.",
                {
                    "model": model,
                    "traceId": record.get("traceId"),
                    "reasoning_token_count": reasoning_tokens,
                    "output_token_count": output_tokens,
                },
            )
        if input_tokens >= 2000 and cached_tokens <= max(100, int(input_tokens * 0.05)):
            append_warning(
                state,
                "low_cache",
                "low",
                "Кэш выглядит низким для дорогого входа.",
                {
                    "model": model,
                    "traceId": record.get("traceId"),
                    "cached_token_count": cached_tokens,
                    "input_token_count": input_tokens,
                },
            )
        if tool_tokens > 0:
            append_warning(
                state,
                "tool_or_mcp_activity_near_expensive_turn",
                "low",
                "У дорогого хода замечена tool/MCP активность.",
                {
                    "model": model,
                    "traceId": record.get("traceId"),
                    "tool_token_count": tool_tokens,
                    "input_token_count": input_tokens,
                },
            )

    if "mcp_servers" in attrs:
        mcp_servers = [item.strip() for item in str(attrs["mcp_servers"]).split(",") if item.strip()]
        if len(mcp_servers) >= 5:
            append_warning(
                state,
                "many_mcp_servers",
                "low",
                "В сессии включено много MCP servers.",
                {
                    "model": model,
                    "traceId": record.get("traceId"),
                    "mcp_server_count": len(mcp_servers),
                    "mcp_servers": mcp_servers,
                },
            )

    if "prompt" in attrs or "prompt_length" in attrs:
        append_warning(
            state,
            "prompt_metadata_present",
            "info",
            "В raw telemetry есть prompt metadata. Текст prompt должен быть пустым или [REDACTED].",
            {
                "traceId": record.get("traceId"),
                "event_name": attrs.get("event.name"),
                "prompt_present": "prompt" in attrs,
                "prompt_length_present": "prompt_length" in attrs,
            },
        )


def process_span(
    span: dict[str, Any],
    service_attrs: dict[str, Any],
    scope_name: str | None,
    state: AnalysisState,
) -> None:
    attrs = attributes_to_dict(span.get("attributes"))
    record_private_and_token_fields(attrs, state)
    service_name = service_attrs.get("service.name")
    model = attrs.get("model")
    session_key = extract_session_key(service_name, model, attrs, span.get("traceId"))
    session_entry = get_session_entry(state, session_key, service_name, model)
    session_entry["span_count"] += 1
    if span.get("traceId"):
        session_entry["trace_ids"].add(span["traceId"])

    span_row = sanitize_value(
        {
            "service_name": service_name,
            "service_version": service_attrs.get("service.version"),
            "scope_name": scope_name,
            "span_name": span.get("name"),
            "kind": span.get("kind"),
            "traceId": span.get("traceId"),
            "spanId": span.get("spanId"),
            "parentSpanId": span.get("parentSpanId"),
            "start_time": unix_nano_to_iso(span.get("startTimeUnixNano")),
            "end_time": unix_nano_to_iso(span.get("endTimeUnixNano")),
            "duration_ms": duration_ms(span.get("startTimeUnixNano"), span.get("endTimeUnixNano")),
            "status": span.get("status", {}),
            "attributes": attrs,
        }
    )
    state.spans.append(span_row)

    for event in span.get("events", []) or []:
        event_attrs = attributes_to_dict(event.get("attributes"))
        record_private_and_token_fields(event_attrs, state)
        state.clean_events.append(
            sanitize_value(
                {
                    "event_type": "span_event",
                    "service_name": service_name,
                    "scope_name": scope_name,
                    "span_name": span.get("name"),
                    "event_name": event.get("name"),
                    "timestamp": unix_nano_to_iso(event.get("timeUnixNano")),
                    "traceId": span.get("traceId"),
                    "spanId": span.get("spanId"),
                    "attributes": event_attrs,
                }
            )
        )
        token_payload = {key: to_number(value) for key, value in event_attrs.items() if is_token_field(key)}
        token_payload = {key: value for key, value in token_payload.items() if value is not None}
        if token_payload:
            state.token_usage.append(
                sanitize_value(
                    {
                        "source_type": "span_event",
                        "service_name": service_name,
                        "scope_name": scope_name,
                        "span_name": span.get("name"),
                        "event_name": event.get("name"),
                        "timestamp": unix_nano_to_iso(event.get("timeUnixNano")),
                        "traceId": span.get("traceId"),
                        "spanId": span.get("spanId"),
                        "model": model,
                        **token_payload,
                    }
                )
            )
            session_entry["token_event_count"] += 1


def flatten_metric_value(metric_name: str, point: dict[str, Any]) -> dict[str, Any]:
    base: dict[str, Any] = {
        "metric_name": metric_name,
        "timestamp": unix_nano_to_iso(point.get("timeUnixNano")),
        "start_time": unix_nano_to_iso(point.get("startTimeUnixNano")),
        "attributes": attributes_to_dict(point.get("attributes")),
    }
    if "sum" in point:
        base["value"] = to_number(point.get("sum"))
    if "asInt" in point:
        base["value"] = to_number(point.get("asInt"))
    if "asDouble" in point:
        base["value"] = to_number(point.get("asDouble"))
    if "count" in point:
        base["count"] = to_number(point.get("count"))
    if "min" in point:
        base["min"] = to_number(point.get("min"))
    if "max" in point:
        base["max"] = to_number(point.get("max"))
    if "sum" in point and base.get("value") is None:
        base["value"] = to_number(point.get("sum"))
    return base


def process_metric(
    metric: dict[str, Any],
    service_attrs: dict[str, Any],
    scope_name: str | None,
    state: AnalysisState,
) -> None:
    service_name = service_attrs.get("service.name")
    metric_name = metric.get("name")
    metric_type = next((name for name in ("sum", "gauge", "histogram") if name in metric), "unknown")
    payload = metric.get(metric_type, {})
    for point in payload.get("dataPoints", []) or []:
        attrs = attributes_to_dict(point.get("attributes"))
        record_private_and_token_fields(attrs, state)
        model = attrs.get("model")
        session_key = extract_session_key(service_name, model, attrs, None)
        session_entry = get_session_entry(state, session_key, service_name, model)
        session_entry["metric_count"] += 1

        row = sanitize_value(
            {
                "service_name": service_name,
                "service_version": service_attrs.get("service.version"),
                "scope_name": scope_name,
                "metric_name": metric_name,
                "metric_type": metric_type,
                "unit": metric.get("unit"),
                **flatten_metric_value(metric_name, point),
            }
        )
        state.metrics.append(row)

        if metric_name == "codex.turn.token_usage":
            token_type = row.get("attributes", {}).get("token_type")
            value = row.get("value")
            state.token_usage.append(
                sanitize_value(
                    {
                        "source_type": "metric",
                        "service_name": service_name,
                        "scope_name": scope_name,
                        "metric_name": metric_name,
                        "metric_type": metric_type,
                        "timestamp": row.get("timestamp"),
                        "model": model,
                        "token_type": token_type,
                        "value": value,
                        "count": row.get("count"),
                    }
                )
            )
            session_entry["token_event_count"] += 1
            if token_type == "input":
                session_entry["input_tokens"] += int(value or 0)
            elif token_type == "output":
                session_entry["output_tokens"] += int(value or 0)
            elif token_type == "cached_input":
                session_entry["cached_tokens"] += int(value or 0)
            elif token_type == "reasoning_output":
                session_entry["reasoning_tokens"] += int(value or 0)

        if metric_name == "codex.turn.tool.call" and to_number(row.get("value")) not in (None, 0):
            append_warning(
                state,
                "tool_or_mcp_activity_near_expensive_turn",
                "low",
                "В метриках замечена tool activity рядом с ходом.",
                {
                    "model": model,
                    "metric_name": metric_name,
                    "value": row.get("value"),
                },
            )


def analyze_records(records: list[dict[str, Any]]) -> AnalysisState:
    state = AnalysisState()
    for record in records:
        for resource_log in record.get("resourceLogs", []) or []:
            service_attrs = attributes_to_dict(resource_log.get("resource", {}).get("attributes"))
            for scope_log in resource_log.get("scopeLogs", []) or []:
                scope_name = scope_log.get("scope", {}).get("name")
                for log_record in scope_log.get("logRecords", []) or []:
                    process_log_record(log_record, service_attrs, scope_name, state)

        for resource_span in record.get("resourceSpans", []) or []:
            service_attrs = attributes_to_dict(resource_span.get("resource", {}).get("attributes"))
            for scope_span in resource_span.get("scopeSpans", []) or []:
                scope_name = scope_span.get("scope", {}).get("name")
                for span in scope_span.get("spans", []) or []:
                    process_span(span, service_attrs, scope_name, state)

        for resource_metric in record.get("resourceMetrics", []) or []:
            service_attrs = attributes_to_dict(resource_metric.get("resource", {}).get("attributes"))
            for scope_metric in resource_metric.get("scopeMetrics", []) or []:
                scope_name = scope_metric.get("scope", {}).get("name")
                for metric in scope_metric.get("metrics", []) or []:
                    process_metric(metric, service_attrs, scope_name, state)

    if state.raw_private_fields:
        append_warning(
            state,
            "private_fields_detected_in_raw",
            "high",
            "В raw telemetry найдены приватные поля.",
            {
                "detected_field_names": sorted(state.raw_private_fields),
                "detected_field_counts": {f"count::{key}": value for key, value in state.raw_private_fields.items()},
            },
        )

    for session_entry in state.session_summary.values():
        session_entry["warning_count"] = sum(
            1
            for warning in state.warnings
            if warning.get("context", {}).get("model") in {None, session_entry["model"]}
        )
        session_entry["trace_ids"] = sorted(session_entry["trace_ids"])

    state.session_rows = list(state.session_summary.values())
    return state


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_report(path: Path, input_path: Path, state: AnalysisState) -> None:
    top_sessions = sorted(
        state.session_rows,
        key=lambda item: (item["input_tokens"] + item["output_tokens"] + item["reasoning_tokens"]),
        reverse=True,
    )[:5]
    warning_counts = Counter(item["warning_type"] for item in state.warnings)
    lines = [
        "# Diagnostic Report",
        "",
        "## Что разобрано",
        "",
        f"- Входной файл: `{input_path}`",
        f"- Clean events: `{len(state.clean_events)}`",
        f"- Token usage records: `{len(state.token_usage)}`",
        f"- Spans: `{len(state.spans)}`",
        f"- Metrics: `{len(state.metrics)}`",
        f"- Sessions: `{len(state.session_rows)}`",
        f"- Warnings: `{len(state.warnings)}`",
        "",
        "## Что вычищено",
        "",
        "- Удаляются или маскируются поля: `user.email`, `user.account_id`, `conversation.id`, `host.name`, чувствительные `authorization/cookie/api-key/password/secret` поля.",
        "- `prompt_length` сохраняется как диагностический сигнал.",
        "- `prompt` сохраняется только если он уже пустой или `[REDACTED]`. Иначе значение заменяется на `[REDACTED]`.",
        "- Текст prompt не должен храниться в открытом виде.",
        f"- Найденные приватные поля в raw: `{', '.join(sorted(state.raw_private_fields)) if state.raw_private_fields else 'не найдены'}`",
        "",
        "## Найденные token fields",
        "",
        f"- `{', '.join(sorted(state.raw_token_fields)) if state.raw_token_fields else 'не найдены'}`",
        "",
        "## Основные подозрения",
        "",
    ]
    if warning_counts:
        for warning_type, count in sorted(warning_counts.items()):
            lines.append(f"- `{warning_type}`: `{count}`")
    else:
        lines.append("- Автоматические предупреждения не сработали.")

    lines.extend(["", "## Тяжелые сессии", ""])
    if top_sessions:
        for item in top_sessions:
            total = item["input_tokens"] + item["output_tokens"] + item["reasoning_tokens"] + item["cached_tokens"]
            lines.append(
                f"- service=`{item['service_name']}` model=`{item['model']}` total_tokens=`{total}` "
                f"input=`{item['input_tokens']}` output=`{item['output_tokens']}` reasoning=`{item['reasoning_tokens']}` "
                f"cached=`{item['cached_tokens']}` warnings=`{item['warning_count']}`"
            )
    else:
        lines.append("- Сессионные агрегаты не собраны.")

    lines.extend(
        [
            "",
            "## Что это значит",
            "",
            "- Данные уже пригодны для локального forensic-анализа причин дорогих ходов.",
            "- Raw telemetry небезопасно показывать напрямую: приватные поля реально встречаются.",
            "- Для будущего dashboard нужно читать только sanitized outputs из этого parser-слоя.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    records = load_records(input_path, args.format)
    state = analyze_records(records)

    write_jsonl(output_dir / "clean_events.jsonl", state.clean_events)
    write_jsonl(output_dir / "token_usage.jsonl", state.token_usage)
    write_jsonl(output_dir / "spans.jsonl", state.spans)
    write_jsonl(output_dir / "metrics.jsonl", state.metrics)
    write_jsonl(output_dir / "sessions.jsonl", state.session_rows)
    (output_dir / "session_summary.json").write_text(
        json.dumps(
            {
                "counts": {
                    "clean_events": len(state.clean_events),
                    "token_usage": len(state.token_usage),
                    "spans": len(state.spans),
                    "metrics": len(state.metrics),
                    "sessions": len(state.session_rows),
                    "warnings": len(state.warnings),
                },
                "token_fields_found": sorted(state.raw_token_fields),
                "private_fields_found_in_raw": dict(state.raw_private_fields),
                "sessions": state.session_rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_jsonl(output_dir / "warnings.jsonl", state.warnings)
    write_report(output_dir / "diagnostic_report.md", input_path, state)

    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
