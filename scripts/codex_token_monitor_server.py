#!/usr/bin/env python3
"""Codex Token Monitor Server v2 — source-aware hybrid monitor over live Codex chats + OTel archives."""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

SCHEMA_VERSION = "token-monitor-server.v2"
ARCHIVE_STATE_VERSION = "archive-state.v2"

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
CONFIG_DIR = REPO_ROOT / "config"
STATIC_DIR = REPO_ROOT / "static" / "codex-token-monitor"
LOCAL_MONITOR_DIR = REPO_ROOT / "_local" / "codex-token-monitor"
AUDITS_DIR = LOCAL_MONITOR_DIR / "audits"
ROLLOUT_INDEX_TTL_SEC = 10.0

_live_rollout_summary_cache: dict[str, tuple[float, dict[str, dict[str, Any]]]] = {}
_live_rollout_summary_lock = threading.Lock()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_json_safe(path: Path) -> Any:
    try:
        return read_json(path)
    except (OSError, json.JSONDecodeError):
        return None


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def to_int(value: Any, default: int = 0) -> int:
    if value is None or value == "":
        return default
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return default


def _extract_content_text(content_parts: Any) -> str:
    if not isinstance(content_parts, list):
        return ""
    return " ".join(
        str(part.get("text", "") if isinstance(part, dict) else part)
        for part in content_parts
    ).strip()


def _looks_like_system_composed_prompt(text: str) -> bool:
    return (
        "AGENTS.md" in text
        or "Global Instructions" in text
        or len(text) > 5000
    )


def _is_internal_live_user_prompt(text: str) -> bool:
    raw = str(text or "").strip()
    if not raw:
        return True
    lower = raw.lower()
    return (
        _looks_like_system_composed_prompt(raw)
        or raw.startswith("PLEASE IMPLEMENT THIS PLAN:")
        or raw.startswith("<turn_aborted>")
        or "the user interrupted the previous turn on purpose" in lower
        or raw.startswith("Прочитай handoff ")
        or raw.startswith("Read handoff ")
    )


def _humanize_live_title(title: str, fallback: str) -> str:
    raw = str(title or "").strip()
    if not raw:
        return fallback
    first_line = next((line.strip() for line in raw.splitlines() if line.strip()), raw)
    if len(first_line) > 140:
        return first_line[:139] + "…"
    return first_line


# ── Config loading ──


def load_config(config_path: Path) -> dict[str, Any]:
    """Load v2 config with sources. Falls back to v1 projects-style config."""
    if not config_path.exists():
        return {
            "version": 2,
            "default_source_id": "",
            "sources": [],
        }
    data = read_json(config_path)

    # v2 config has 'sources' key
    if "sources" in data:
        return data

    # v1 config — migrate on-the-fly to sources
    return _migrate_v1_config(data)


def _migrate_v1_config(data: dict[str, Any]) -> dict[str, Any]:
    """Convert v1 project-based config to v2 source-based config."""
    projects = data.get("projects", [])
    sources = []
    for p in projects:
        sources.append({
            "id": p.get("id", "legacy"),
            "name": p.get("name", "Legacy Project"),
            "kind": "archive",
            "path": p.get("path", ""),
            "runs_dir": p.get("runs_dir", "_local/codex-token-debugger"),
        })
    default_id = data.get("default_project_id", "")
    if not default_id and sources:
        default_id = sources[0]["id"]
    return {
        "version": 2,
        "default_source_id": default_id,
        "sources": sources,
    }


def find_source(config: dict[str, Any], source_id: str) -> dict[str, Any] | None:
    for s in config.get("sources", []):
        if s["id"] == source_id:
            return s
    return None


# ── Archive state ──


def load_archive_state() -> dict[str, list[str]]:
    path = LOCAL_MONITOR_DIR / "archive_state.json"
    data = read_json_safe(path)
    if data and isinstance(data.get("archived_sessions"), dict):
        return data["archived_sessions"]
    return {}


def save_archive_state(state: dict[str, list[str]]) -> None:
    path = LOCAL_MONITOR_DIR / "archive_state.json"
    write_json(path, {"version": ARCHIVE_STATE_VERSION, "archived_sessions": state})


def is_archived(source_id: str, session_id: str) -> bool:
    state = load_archive_state()
    return session_id in state.get(source_id, [])


def set_archived(source_id: str, session_id: str, archived: bool) -> None:
    state = load_archive_state()
    source_archived = state.setdefault(source_id, [])
    if archived:
        if session_id not in source_archived:
            source_archived.append(session_id)
    else:
        if session_id in source_archived:
            source_archived.remove(session_id)
    save_archive_state(state)


def discover_archive_sessions(source: dict[str, Any]) -> list[dict[str, Any]]:
    project_path = Path(source["path"])
    runs_dir_name = source.get("runs_dir", "_local/codex-token-debugger")
    runs_dir = project_path / runs_dir_name

    if not runs_dir.exists() or not runs_dir.is_dir():
        return []

    sessions: list[dict[str, Any]] = []
    for entry in sorted(runs_dir.iterdir(), key=lambda p: p.name, reverse=True):
        if not entry.is_dir():
            continue

        normalized_json = entry / "token-cost-normalized" / "token_cost_dashboard_data.json"
        parsed_jsonl = entry / "parsed" / "token_usage.jsonl"

        has_normalized = normalized_json.exists()
        has_parsed = parsed_jsonl.exists()

        if not has_normalized and not has_parsed:
            continue

        session_id = entry.name
        dashboard = read_json_safe(normalized_json) if has_normalized else None

        title = session_id
        date_iso = ""
        model = "unknown"
        reasoning = "unknown"
        workdir = str(project_path)
        step_count = 0
        total_cost = None
        warnings_count = 0
        confirmation_badges: list[str] = []

        # Check for confirmation summary
        reports_dir = entry / "reports"
        if reports_dir.exists():
            for rpt in reports_dir.glob("*_confirmation_summary.json"):
                cdata = read_json_safe(rpt)
                if cdata and isinstance(cdata, dict):
                    kind = cdata.get("kind", "")
                    if kind == "mixed":
                        confirmation_badges.append("mixed")
                    if kind == "noisy":
                        confirmation_badges.append("noisy")
                    sel_turn = cdata.get("selected_turn") or cdata.get("selected_turn_index")
                    if sel_turn is not None:
                        confirmation_badges.append(f"turn:{sel_turn}")

        if dashboard and isinstance(dashboard, dict):
            summary = dashboard.get("summary", {})
            turns = dashboard.get("turns", [])
            if isinstance(summary, dict):
                date_iso = _extract_date(summary, turns)
                models = summary.get("models", [])
                model = _pick_model(models)
                step_count = summary.get("turn_count", len(turns) if isinstance(turns, list) else 0)
                total_cost = summary.get("estimated_total_cost_usd")
                warnings_count = len(summary.get("warnings", []))
            if isinstance(turns, list) and turns:
                efforts = sorted({str(t.get("reasoning_effort", "unknown")) for t in turns})
                reasoning = efforts[0] if len(efforts) == 1 else "mixed"
                if not date_iso:
                    date_iso = _earliest_timestamp(turns)

        if not date_iso:
            mtime = entry.stat().st_mtime
            date_iso = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()

        sessions.append({
            "id": session_id,
            "title": title,
            "date": date_iso,
            "model": model,
            "reasoning": reasoning,
            "workdir": workdir,
            "step_count": step_count,
            "total_cost_usd": total_cost,
            "warnings_count": warnings_count,
            "has_normalized": has_normalized,
            "has_parsed": has_parsed,
            "source_kind": "archive",
            "confirmation_badges": confirmation_badges,
        })

    return sessions


def _extract_date(summary: dict[str, Any], turns: list[dict[str, Any]]) -> str:
    for turn in turns:
        ts = turn.get("timestamp", "")
        if ts:
            return ts
    return ""


def _earliest_timestamp(turns: list[dict[str, Any]]) -> str:
    timestamps = [t.get("timestamp", "") for t in turns if t.get("timestamp", "")]
    return min(timestamps) if timestamps else ""


def _pick_model(models: list[str]) -> str:
    if not models:
        return "unknown"
    return models[0] if len(models) == 1 else "mixed"


def _compute_turn_summary(turns: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute summary from a list of turn dicts (filtered or full)."""
    total_input = 0
    total_cached = 0
    total_output = 0
    total_reasoning = 0
    total_tool = 0
    total_cost = 0.0
    models: set[str] = set()
    warnings: list[str] = []
    for t in turns:
        total_input += to_int(t.get("input_tokens", 0))
        total_cached += to_int(t.get("cached_tokens", 0))
        total_output += to_int(t.get("output_tokens", 0))
        total_reasoning += to_int(t.get("reasoning_tokens", 0))
        total_tool += to_int(t.get("tool_tokens", 0))
        m = str(t.get("model", ""))
        if m:
            models.add(m)
        w = t.get("warnings")
        if isinstance(w, list):
            warnings.extend(w)
        cost = t.get("estimated_cost_usd", {})
        if isinstance(cost, dict):
            total_cost += float(cost.get("total", 0) or 0)
    non_cached = total_input - total_cached
    ratio = (total_cached / total_input) if total_input > 0 else 0
    return {
        "turn_count": len(turns),
        "session_count": 1,
        "total_input_tokens": total_input,
        "total_cached_tokens": total_cached,
        "total_non_cached_input_tokens": non_cached,
        "average_cached_ratio": ratio,
        "total_output_tokens": total_output,
        "total_reasoning_tokens": total_reasoning,
        "total_tool_tokens": total_tool,
        "estimated_total_cost_usd": total_cost,
        "models": sorted(models),
        "warnings": warnings,
    }


def build_archive_session_detail(source: dict[str, Any], session_id: str) -> dict[str, Any] | None:
    project_path = Path(source["path"])
    runs_dir_name = source.get("runs_dir", "_local/codex-token-debugger")
    runs_dir = project_path / runs_dir_name
    run_dir = runs_dir / session_id

    if not run_dir.exists() or not run_dir.is_dir():
        return None

    normalized_json = run_dir / "token-cost-normalized" / "token_cost_dashboard_data.json"
    dashboard = read_json_safe(normalized_json)

    if not dashboard:
        return _fallback_session(session_id, run_dir)

    summary = dashboard.get("summary", {})
    turns = dashboard.get("turns", [])
    sessions_list = dashboard.get("sessions", [])

    title = session_id
    date_iso = _extract_date(summary, turns)
    if not date_iso:
        mtime = run_dir.stat().st_mtime
        date_iso = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()

    models = summary.get("models", [])
    model_str = _pick_model(models)
    efforts = sorted({str(t.get("reasoning_effort", "unknown")) for t in turns})
    reasoning_str = efforts[0] if len(efforts) == 1 else "mixed"

    confirmation_badges: list[str] = []
    selected_turn_index: int | None = None
    reports_dir = run_dir / "reports"
    if reports_dir.exists():
        for rpt in reports_dir.glob("*_confirmation_summary.json"):
            cdata = read_json_safe(rpt)
            if cdata and isinstance(cdata, dict):
                kind = cdata.get("kind", "")
                if kind == "mixed":
                    confirmation_badges.append("mixed")
                if kind == "noisy":
                    confirmation_badges.append("noisy")
                sel_turn = cdata.get("selected_turn") or cdata.get("selected_turn_index")
                if sel_turn is not None:
                    if isinstance(sel_turn, dict):
                        # selected_turn is an object with model/timestamp — match by these
                        st_model = str(sel_turn.get("model", ""))
                        st_ts = str(sel_turn.get("timestamp", ""))
                        confirmation_badges.append(f"model:{st_model}")
                        selected_turn_index = -1  # signal: match by fields
                        _selected_turn_data = sel_turn
                    else:
                        sel_turn_int = to_int(sel_turn)
                        confirmation_badges.append(f"turn:{sel_turn_int}")
                        selected_turn_index = sel_turn_int

    # When a confirmed turn is selected, show only that turn
    if selected_turn_index is not None and isinstance(turns, list):
        if selected_turn_index == -1:
            # selected_turn was a dict — match by model+timestamp
            st_model = str(_selected_turn_data.get("model", ""))
            st_ts = str(_selected_turn_data.get("timestamp", ""))
            filtered = [t for t in turns
                        if str(t.get("model", "")) == st_model and str(t.get("timestamp", "")) == st_ts]
            if filtered:
                turns = filtered
                model_str = str(turns[0].get("model", model_str))
                reasoning_str = str(turns[0].get("reasoning_effort", reasoning_str))
                summary = _compute_turn_summary(turns)
        else:
            filtered = [t for t in turns if to_int(t.get("turn_index", 0)) == selected_turn_index]
            if filtered:
                turns = filtered
                model_str = str(turns[0].get("model", model_str))
                reasoning_str = str(turns[0].get("reasoning_effort", reasoning_str))
                summary = _compute_turn_summary(turns)

    steps = []
    for t in turns:
        steps.append(_build_step(t))

    return {
        "id": session_id,
        "title": title,
        "date": date_iso,
        "model": model_str,
        "reasoning": reasoning_str,
        "workdir": str(project_path),
        "source_kind": "archive",
        "confirmation_badges": confirmation_badges,
        "summary": summary,
        "steps": steps,
    }


def _fallback_session(session_id: str, run_dir: Path) -> dict[str, Any]:
    mtime = run_dir.stat().st_mtime
    date_iso = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
    return {
        "id": session_id,
        "title": session_id,
        "date": date_iso,
        "model": "unknown",
        "reasoning": "unknown",
        "workdir": "",
        "source_kind": "archive",
        "confirmation_badges": [],
        "summary": {
            "turn_count": 0,
            "session_count": 0,
            "total_input_tokens": 0,
            "total_cached_tokens": 0,
            "total_non_cached_input_tokens": 0,
            "average_cached_ratio": 0,
            "total_output_tokens": 0,
            "total_reasoning_tokens": 0,
            "total_tool_tokens": 0,
            "estimated_total_cost_usd": None,
            "warnings": [],
        },
        "steps": [],
    }


def _build_step(turn: dict[str, Any]) -> dict[str, Any]:
    return {
        "step_index": to_int(turn.get("turn_index"), 0),
        "turn_id": str(turn.get("turn_id", "")),
        "timestamp": str(turn.get("timestamp", "")),
        "model": str(turn.get("model", "unknown")),
        "reasoning_effort": str(turn.get("reasoning_effort", "unknown")),
        "user_prompt": {
            "available": False,
            "text": "",
            "hidden_by_default": True,
        },
        "assistant_answer": {
            "available": False,
            "text": "",
            "hidden_by_default": True,
        },
        "usage": {
            "input_tokens": to_int(turn.get("input_tokens"), 0),
            "cached_tokens": to_int(turn.get("cached_tokens"), 0),
            "non_cached_input_tokens": to_int(turn.get("non_cached_input_tokens"), 0),
            "cached_ratio": float(turn.get("cached_ratio", 0)),
            "output_tokens": to_int(turn.get("output_tokens"), 0),
            "reasoning_tokens": to_int(turn.get("reasoning_tokens"), 0),
            "tool_tokens": to_int(turn.get("tool_tokens"), 0),
            "available": True,
            "estimated_total_cost_usd": (
                turn.get("estimated_cost_usd", {}).get("total")
                if isinstance(turn.get("estimated_cost_usd"), dict)
                else None
            ),
            "estimated_input_cost_usd": (
                turn.get("estimated_cost_usd", {}).get("input")
                if isinstance(turn.get("estimated_cost_usd"), dict)
                else None
            ),
            "estimated_cached_input_cost_usd": (
                turn.get("estimated_cost_usd", {}).get("cached_input")
                if isinstance(turn.get("estimated_cost_usd"), dict)
                else None
            ),
            "estimated_output_cost_usd": (
                turn.get("estimated_cost_usd", {}).get("output")
                if isinstance(turn.get("estimated_cost_usd"), dict)
                else None
            ),
        },
        "environment": {
            "thread_id": str(turn.get("thread_id", "")),
            "observed_mcp_server_count": to_int(turn.get("observed_mcp_server_count"), 0),
            "observed_mcp_servers": turn.get("observed_mcp_servers")
            if isinstance(turn.get("observed_mcp_servers"), list)
            else [],
            "enabled_plugins_count": to_int(turn.get("enabled_plugins_count"), 0),
            "enabled_skills_count": to_int(turn.get("enabled_skills_count"), 0),
            "global_user_instructions_status": str(turn.get("global_user_instructions_status", "unknown")),
            "repo_context_status": str(turn.get("repo_context_status", "unknown")),
        },
        "warnings": turn.get("warnings")
        if isinstance(turn.get("warnings"), list)
        else [],
    }


# ── Live chat adapter ──


def discover_live_sessions(source: dict[str, Any]) -> list[dict[str, Any]]:
    """Read real Codex chats from codex_dir (read-only)."""
    codex_dir = Path(source.get("codex_dir", ""))
    if not codex_dir.exists():
        return []

    sqlite_path = codex_dir / "state_5.sqlite"
    threads = _read_threads_from_sqlite(sqlite_path)

    index_path = codex_dir / "session_index.jsonl"
    index_entries = _read_session_index(index_path)
    rollout_summaries = _get_live_rollout_summaries(codex_dir, allow_build=False)

    sessions: list[dict[str, Any]] = []
    for thread in threads:
        thread_id = thread["id"]
        title = thread.get("title", thread_id) or thread_id
        if title == thread_id:
            ie = index_entries.get(thread_id, {})
            title = ie.get("thread_name", thread_id)
        title = _humanize_live_title(title, thread_id)

        date_iso = thread.get("updated_at", thread.get("created_at", ""))
        model = thread.get("model", "unknown")
        reasoning_effort = thread.get("reasoning_effort", "unknown")
        cwd = thread.get("cwd", source.get("codex_dir", ""))

        step_count = None
        total_cost = None
        rollout_summary = rollout_summaries.get(thread_id, {})
        if rollout_summary:
            step_count = to_int(rollout_summary.get("step_count", 0))
        last_token = rollout_summary.get("last_token_usage", {})
        if isinstance(last_token, dict) and last_token:
            ti = to_int(last_token.get("input_tokens", last_token.get("input_token_count", 0)))
            tc_in = to_int(last_token.get("cached_input_tokens", last_token.get("cached_input_token_count", 0)))
            to_out = to_int(last_token.get("output_tokens", last_token.get("output_token_count", 0)))
            pricing = _load_pricing()
            if model in pricing:
                p = pricing[model]
                non_cached = ti - tc_in
                total_cost = (
                    (non_cached / 1_000_000) * p.get("input", 0)
                    + (tc_in / 1_000_000) * p.get("cached_input", 0)
                    + (to_out / 1_000_000) * p.get("output", 0)
                )

        sessions.append({
            "id": thread_id,
            "title": title,
            "date": date_iso,
            "model": model,
            "reasoning": reasoning_effort,
            "workdir": cwd,
            "step_count": step_count,
            "total_cost_usd": total_cost,
            "warnings_count": 0,
            "has_normalized": False,
            "has_parsed": True,
            "source_kind": "live",
            "confirmation_badges": [],
        })

    sessions.sort(key=lambda s: s.get("date", ""), reverse=True)
    return sessions


def _read_threads_from_sqlite(sqlite_path: Path) -> list[dict[str, Any]]:
    """Read threads table from Codex state_5.sqlite (read-only)."""
    if not sqlite_path.exists():
        return []
    try:
        conn = sqlite3.connect(f"file:{sqlite_path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM pragma_table_info('threads')")
        columns = {r[0] for r in cursor.fetchall()}
        select_cols = []
        for col in ["id", "title", "model", "reasoning_effort", "cwd", "created_at", "updated_at"]:
            if col in columns:
                select_cols.append(col)
            else:
                select_cols.append(f"NULL as {col}")
        query = f"SELECT {', '.join(select_cols)} FROM threads ORDER BY updated_at DESC, created_at DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def _read_session_index(index_path: Path) -> dict[str, dict[str, Any]]:
    """Read session_index.jsonl for thread_name per thread_id."""
    entries: dict[str, dict[str, Any]] = {}
    if not index_path.exists():
        return entries
    try:
        for line in index_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                tid = obj.get("thread_id", "")
                if tid:
                    entries[tid] = obj
            except json.JSONDecodeError:
                continue
    except Exception:
        pass
    return entries


def _scan_rollout_file_summary(rollout_path: Path) -> tuple[str | None, dict[str, Any]]:
    thread_id = None
    step_count = 0
    last_token_usage = None

    try:
        with rollout_path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                outer_type = obj.get("type")
                payload = obj.get("payload", {})
                if not isinstance(payload, dict):
                    payload = {}

                if thread_id is None and outer_type == "session_meta":
                    candidate = str(payload.get("id", "")).strip()
                    if candidate:
                        thread_id = candidate

                if outer_type == "response_item" and payload.get("role") == "user":
                    text = _extract_content_text(payload.get("content", []))
                    if text and not _is_internal_live_user_prompt(text):
                        step_count += 1

                if outer_type == "event_msg":
                    info = payload.get("info", {})
                    token_usage = info.get("total_token_usage") if isinstance(info, dict) else None
                    if isinstance(token_usage, dict):
                        last_token_usage = token_usage
    except OSError:
        return None, {}

    return thread_id, {
        "paths": [str(rollout_path)],
        "step_count": step_count,
        "last_token_usage": last_token_usage if isinstance(last_token_usage, dict) else {},
    }


def _get_live_rollout_summaries(codex_dir: Path, *, allow_build: bool = True) -> dict[str, dict[str, Any]]:
    cache_key = str(codex_dir.resolve())
    now = time.time()
    cached = _live_rollout_summary_cache.get(cache_key)
    if cached and (now - cached[0]) < ROLLOUT_INDEX_TTL_SEC:
        return cached[1]
    if not allow_build:
        return cached[1] if cached else {}

    with _live_rollout_summary_lock:
        now = time.time()
        cached = _live_rollout_summary_cache.get(cache_key)
        if cached and (now - cached[0]) < ROLLOUT_INDEX_TTL_SEC:
            return cached[1]

        sessions_dir = codex_dir / "sessions"
        summaries: dict[str, dict[str, Any]] = {}
        if not sessions_dir.exists():
            _live_rollout_summary_cache[cache_key] = (now, summaries)
            return summaries

        for rollout_path in sorted(sessions_dir.glob("**/rollout-*.jsonl")):
            thread_id, file_summary = _scan_rollout_file_summary(rollout_path)
            if not thread_id:
                continue
            existing = summaries.setdefault(thread_id, {"paths": [], "step_count": 0, "last_token_usage": {}})
            existing["paths"].extend(file_summary.get("paths", []))
            existing["step_count"] = to_int(existing.get("step_count", 0)) + to_int(file_summary.get("step_count", 0))
            if file_summary.get("last_token_usage"):
                existing["last_token_usage"] = file_summary["last_token_usage"]

        _live_rollout_summary_cache[cache_key] = (now, summaries)
        return summaries


def _read_rollout_jsonl(codex_dir: Path, thread_id: str) -> list[dict[str, Any]]:
    """Read rollout JSONL files for a given thread via cached file lookup."""
    events: list[dict[str, Any]] = []
    summary = _get_live_rollout_summaries(codex_dir).get(thread_id, {})
    paths = summary.get("paths", [])
    if not isinstance(paths, list):
        return events

    for raw_path in sorted(str(p) for p in paths):
        rollout_path = Path(raw_path)
        try:
            with rollout_path.open("r", encoding="utf-8") as handle:
                for raw_line in handle:
                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except OSError:
            continue
    return events


def build_live_session_detail(source: dict[str, Any], session_id: str) -> dict[str, Any] | None:
    """Build session detail for a live Codex chat."""
    codex_dir = Path(source.get("codex_dir", ""))
    if not codex_dir.exists():
        return None

    sqlite_path = codex_dir / "state_5.sqlite"
    threads = _read_threads_from_sqlite(sqlite_path)
    thread = next((t for t in threads if t.get("id") == session_id), None)

    index_path = codex_dir / "session_index.jsonl"
    index_entries = _read_session_index(index_path)

    title = session_id
    date_iso = ""
    model = "unknown"
    reasoning = "unknown"
    cwd = ""

    if thread:
        title = thread.get("title", session_id) or session_id
        if title == session_id:
            ie = index_entries.get(session_id, {})
            title = ie.get("thread_name", session_id)
        title = _humanize_live_title(title, session_id)
        date_iso = thread.get("updated_at", thread.get("created_at", ""))
        model = thread.get("model", "unknown")
        reasoning = thread.get("reasoning_effort", "unknown")
        cwd = thread.get("cwd", "")
    if not date_iso:
        date_iso = datetime.now(timezone.utc).isoformat()

    events = _read_rollout_jsonl(codex_dir, session_id)
    steps, timeline_events = _build_live_steps(events, session_id)

    total_cost = None
    total_input = 0
    total_cached = 0
    total_output = 0
    total_reasoning = 0
    total_tool = 0

    last_token = None
    for ev in reversed(events):
        pl = ev.get("payload", ev)
        if not isinstance(pl, dict):
            continue
        # token usage is in event_msg.payload.info.total_token_usage
        if pl.get("type") == "event_msg" or ev.get("type") == "event_msg":
            info = pl.get("info", {})
            tc = info.get("total_token_usage") if isinstance(info, dict) else None
            if tc and isinstance(tc, dict):
                last_token = tc
                break

    if last_token:
        total_input = to_int(last_token.get("input_tokens", last_token.get("input_token_count", 0)))
        total_cached = to_int(last_token.get("cached_input_tokens", last_token.get("cached_input_token_count", 0)))
        total_output = to_int(last_token.get("output_tokens", last_token.get("output_token_count", 0)))
        total_reasoning = to_int(last_token.get("reasoning_output_tokens", last_token.get("reasoning_token_count", 0)))
        total_tool = to_int(last_token.get("tool_tokens", last_token.get("tool_token_count", 0)))

        pricing = _load_pricing()
        if model in pricing:
            p = pricing[model]
            non_cached = total_input - total_cached
            total_cost = (
                (non_cached / 1_000_000) * p.get("input", 0)
                + (total_cached / 1_000_000) * p.get("cached_input", 0)
                + (total_output / 1_000_000) * p.get("output", 0)
            )

    summary_warnings: list[dict[str, str]] = []
    if total_input > 0:
        summary_warnings.append({
            "id": "live_totals_are_cumulative",
            "message": "В live-источнике totals берутся из последнего cumulative total_token_usage по треду, а не из суммы видимых шагов.",
        })
    if any((step.get("usage", {}) or {}).get("available") for step in steps):
        summary_warnings.append({
            "id": "live_steps_use_request_usage",
            "message": "Per-step usage для live-шага берётся из request-level last_token_usage, если он есть в rollout.",
        })

    return {
        "id": session_id,
        "title": title,
        "date": date_iso,
        "model": model,
        "reasoning": reasoning,
        "workdir": cwd,
        "source_kind": "live",
        "summary": {
            "turn_count": len(steps),
            "session_count": 1,
            "usage_basis": "live_total_token_usage_latest",
            "step_usage_basis": "live_last_token_usage",
            "total_input_tokens": total_input,
            "total_cached_tokens": total_cached,
            "total_non_cached_input_tokens": total_input - total_cached,
            "average_cached_ratio": (total_cached / total_input) if total_input > 0 else 0,
            "total_output_tokens": total_output,
            "total_reasoning_tokens": total_reasoning,
            "total_tool_tokens": total_tool,
            "estimated_total_cost_usd": total_cost,
            "warnings": summary_warnings,
        },
        "timeline_events": timeline_events,
        "steps": steps,
    }


def _build_live_steps(events: list[dict[str, Any]], thread_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Parse rollout events into step structure with honest token mapping.

    Real rollout schema:
      {type: "turn_context", payload: {model, effort, turn_id, ...}}
      {type: "response_item", payload: {role: "user"|"assistant", content: [{text}]}}
      {type: "event_msg", payload: {info: {total_token_usage: {input_tokens, ...}}}}
    """
    steps: list[dict[str, Any]] = []
    timeline_events: list[dict[str, Any]] = []
    current_step: dict[str, Any] | None = None
    step_index = 0
    pending_text: list[str] = []
    # Track model/reasoning from turn_context (not present in response_item)
    current_model = "unknown"
    current_reasoning = "unknown"
    last_visible_step_index = 0
    active_task_turn_id = ""
    current_turn_context: dict[str, Any] = {}

    def finalize_current_step(reason: str = "next_user") -> None:
        nonlocal current_step, pending_text, last_visible_step_index
        if not current_step:
            pending_text = []
            return
        current_step["assistant_answer"]["text"] = "\n".join(pending_text)
        current_step["assistant_answer"]["available"] = bool(pending_text)
        pending_text = []

        usage = current_step.get("usage", {})
        last_usage = current_step.pop("_last_request_usage", None)
        if isinstance(usage, dict) and isinstance(last_usage, dict):
            input_tokens = to_int(last_usage.get("input_tokens"), 0)
            cached_tokens = to_int(last_usage.get("cached_tokens"), 0)
            output_tokens = to_int(last_usage.get("output_tokens"), 0)
            reasoning_tokens = to_int(last_usage.get("reasoning_tokens"), 0)
            tool_tokens = to_int(last_usage.get("tool_tokens"), 0)
            non_cached_tokens = max(input_tokens - cached_tokens, 0)
            has_nonzero_usage = any(
                value > 0
                for value in (
                    input_tokens,
                    cached_tokens,
                    output_tokens,
                    reasoning_tokens,
                    tool_tokens,
                )
            )
            usage.update(
                {
                    "input_tokens": input_tokens if has_nonzero_usage else 0,
                    "cached_tokens": cached_tokens if has_nonzero_usage else 0,
                    "non_cached_input_tokens": non_cached_tokens if has_nonzero_usage else 0,
                    "cached_ratio": (cached_tokens / input_tokens) if has_nonzero_usage and input_tokens > 0 else 0,
                    "output_tokens": output_tokens if has_nonzero_usage else 0,
                    "reasoning_tokens": reasoning_tokens if has_nonzero_usage else 0,
                    "tool_tokens": tool_tokens if has_nonzero_usage else 0,
                    "available": has_nonzero_usage,
                    "confirmation_status": "confirmed_request_usage" if has_nonzero_usage else "missing_request_usage",
                    "source": "live_last_token_usage" if has_nonzero_usage else "missing",
                    "note": "" if has_nonzero_usage else "no confirmed last_token_usage for this step",
                    **(
                        _estimate_usage_costs(
                            str(current_step.get("model") or "unknown"),
                            input_tokens,
                            cached_tokens,
                            output_tokens,
                        )
                        if has_nonzero_usage
                        else {
                            "estimated_total_cost_usd": None,
                            "estimated_input_cost_usd": None,
                            "estimated_cached_input_cost_usd": None,
                            "estimated_output_cost_usd": None,
                        }
                    ),
                }
            )
        elif isinstance(usage, dict):
            usage["available"] = False
            usage["confirmation_status"] = "missing_request_usage"
            usage["source"] = "missing"
            if reason == "next_user":
                usage["note"] = "next turn started before token checkpoint for this step"
            elif reason == "task_complete":
                usage["note"] = "task completed without last_token_usage checkpoint"
            elif reason == "session_end":
                usage["note"] = "session ended without last_token_usage checkpoint"
            else:
                usage["note"] = "no confirmed last_token_usage for this step"
        steps.append(current_step)
        last_visible_step_index = to_int(current_step.get("step_index"), last_visible_step_index)
        current_step = None

    for ev in events:
        outer_type = ev.get("type", "")
        pl = ev.get("payload", {})
        if not isinstance(pl, dict):
            continue

        # turn_context carries model/effort for subsequent steps
        if outer_type == "turn_context":
            current_turn_context = pl
            current_model = str(pl.get("model", current_model))
            current_reasoning = str(pl.get("effort", pl.get("reasoning_effort", current_reasoning)))
            continue

        if outer_type == "event_msg":
            event_type = str(pl.get("type", ""))
            if event_type == "task_started":
                active_task_turn_id = str(pl.get("turn_id", "") or "")
            elif event_type == "task_complete":
                if current_step:
                    current_step.setdefault("environment", {})["task_turn_id"] = str(pl.get("turn_id", "") or active_task_turn_id)
                    finalize_current_step("task_complete")
                active_task_turn_id = ""
            elif event_type == "context_compacted":
                if steps:
                    last_step = steps[-1]
                    badges = last_step.setdefault("post_step_badges", [])
                    if "контекст сжат после этого хода" not in badges:
                        badges.append("контекст сжат после этого хода")
                timeline_events.append(
                    {
                        "event_type": "context_compacted",
                        "label": "Сжатие контекста",
                        "timestamp": str(ev.get("timestamp", "")),
                        "after_step_index": last_visible_step_index,
                        "compaction_task_id": active_task_turn_id or None,
                        "after_step_turn_id": (steps[-1].get("turn_id") if steps else None),
                    }
                )

        # response_item routing by outer type, role from payload
        is_user = (outer_type == "response_item" and pl.get("role") == "user")
        is_assistant = (outer_type == "response_item" and pl.get("role") == "assistant")

        # token_count in event_msg: prefer payload.info.last_token_usage for per-step live usage
        token_count = None
        model_context_window = 0
        if outer_type == "event_msg":
            info = pl.get("info", {})
            if isinstance(info, dict):
                token_count = info.get("last_token_usage") or info.get("total_token_usage")
                model_context_window = to_int(info.get("model_context_window"), 0)

        if is_user:
            user_text = ""
            # response_item payload: {type, role, content: [{text: ...}]}
            content_parts = pl.get("content", [])
            user_text = _extract_content_text(content_parts)

            # turn_id from turn_context event or fallback
            turn_id = pl.get("turn_id", f"turn-{step_index + 1}")
            finalize_current_step("next_user")
            if _is_internal_live_user_prompt(user_text):
                continue

            step_index += 1

            current_step = {
                "step_index": step_index,
                "turn_id": str(turn_id),
                "timestamp": str(pl.get("timestamp", ev.get("timestamp", ""))),
                "model": current_model,
                "reasoning_effort": current_reasoning,
                "user_prompt": {
                    "available": bool(user_text.strip()),
                    "text": user_text.strip(),
                    "hidden_by_default": True,
                    "kind": "user_message",
                },
                "assistant_answer": {
                    "available": False,
                    "text": "",
                    "hidden_by_default": True,
                },
                "usage": {
                    "input_tokens": 0,
                    "cached_tokens": 0,
                    "non_cached_input_tokens": 0,
                    "cached_ratio": 0,
                    "output_tokens": 0,
                    "reasoning_tokens": 0,
                    "tool_tokens": 0,
                    "available": False,
                    "note": "per-step token mapping may be cumulative; use session totals",
                    "estimated_total_cost_usd": None,
                    "estimated_input_cost_usd": None,
                    "estimated_cached_input_cost_usd": None,
                    "estimated_output_cost_usd": None,
                },
                "environment": {
                    "thread_id": thread_id,
                    "cwd": str(current_turn_context.get("cwd", "")),
                    "workspace_roots": current_turn_context.get("workspace_roots")
                    if isinstance(current_turn_context.get("workspace_roots"), list)
                    else [],
                    "current_date": str(current_turn_context.get("current_date", "")),
                    "timezone": str(current_turn_context.get("timezone", "")),
                    "approval_policy": str(current_turn_context.get("approval_policy", "")),
                    "sandbox_policy": (
                        current_turn_context.get("sandbox_policy", {}).get("type", "")
                        if isinstance(current_turn_context.get("sandbox_policy"), dict)
                        else ""
                    ),
                    "permission_profile": (
                        current_turn_context.get("permission_profile", {}).get("type", "")
                        if isinstance(current_turn_context.get("permission_profile"), dict)
                        else ""
                    ),
                    "observed_mcp_server_count": 0,
                    "observed_mcp_servers": [],
                    "enabled_plugins_count": 0,
                    "enabled_skills_count": 0,
                    "global_user_instructions_status": "unknown",
                    "repo_context_status": "unknown",
                },
                "warnings": [],
                "post_step_badges": [],
            }

        elif is_assistant:
            content_parts = pl.get("content", [])
            if isinstance(content_parts, list):
                for c in content_parts:
                    if isinstance(c, dict):
                        txt = c.get("text", "") or c.get("output_text", "")
                        if txt:
                            pending_text.append(str(txt))

        if token_count and isinstance(token_count, dict) and current_step:
            current_step["_last_request_usage"] = {
                "input_tokens": to_int(token_count.get("input_tokens", token_count.get("input_token_count", 0))),
                "cached_tokens": to_int(token_count.get("cached_input_tokens", token_count.get("cached_input_token_count", 0))),
                "output_tokens": to_int(token_count.get("output_tokens", token_count.get("output_token_count", 0))),
                "reasoning_tokens": to_int(token_count.get("reasoning_output_tokens", token_count.get("reasoning_token_count", 0))),
                "tool_tokens": to_int(token_count.get("tool_tokens", token_count.get("tool_token_count", 0))),
            }
            current_step.setdefault("environment", {})["model_context_window"] = model_context_window

    finalize_current_step("session_end")

    return steps, timeline_events


def _load_pricing() -> dict[str, dict[str, float]]:
    pricing_path = CONFIG_DIR / "token_pricing.json"
    data = read_json_safe(pricing_path)
    if data:
        return data.get("prices_per_1m", {})
    return {}


def _estimate_usage_costs(
    model: str,
    input_tokens: int,
    cached_tokens: int,
    output_tokens: int,
) -> dict[str, float | None]:
    pricing = _load_pricing()
    prices = pricing.get(model)
    if not prices:
        return {
            "estimated_total_cost_usd": None,
            "estimated_input_cost_usd": None,
            "estimated_cached_input_cost_usd": None,
            "estimated_output_cost_usd": None,
        }
    non_cached_tokens = max(input_tokens - cached_tokens, 0)
    input_cost = (non_cached_tokens / 1_000_000) * prices.get("input", 0)
    cached_cost = (cached_tokens / 1_000_000) * prices.get("cached_input", 0)
    output_cost = (output_tokens / 1_000_000) * prices.get("output", 0)
    return {
        "estimated_total_cost_usd": input_cost + cached_cost + output_cost,
        "estimated_input_cost_usd": input_cost,
        "estimated_cached_input_cost_usd": cached_cost,
        "estimated_output_cost_usd": output_cost,
    }


class MonitorHandler(SimpleHTTPRequestHandler):
    server: MonitorServer

    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _json_response(self, code: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _ok(self, payload: Any) -> None:
        self._json_response(200, payload)

    def _error(self, code: int, message: str) -> None:
        self._json_response(code, {"error": message})

    def _read_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return {}
        return json.loads(self.rfile.read(length))

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        params = parse_qs(parsed.query)

        if path == "/api/status":
            return self._handle_status()
        if path == "/api/sources":
            return self._handle_sources()
        if path == "/api/projects":
            return self._handle_projects()
        if path == "/api/sessions":
            return self._handle_sessions(params)
        if path == "/api/session":
            return self._handle_session(params)

        return self._serve_static(path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        params = parse_qs(parsed.query)
        body = self._read_body()

        if path == "/api/refresh":
            return self._handle_refresh(body, params)
        if path == "/api/archive":
            return self._handle_archive(body, params, archive=True)
        if path == "/api/unarchive":
            return self._handle_archive(body, params, archive=False)
        if path == "/api/audit_session":
            return self._handle_audit_session(body, params)
        if path == "/api/shutdown":
            return self._handle_shutdown()

        self._error(404, "not found")

    def _serve_static(self, path: str) -> None:
        if path == "/":
            path = "/index.html"
        file_path = STATIC_DIR / path.lstrip("/")
        if not file_path.exists() or not file_path.is_file():
            self._error(404, "not found")
            return
        content_type = "text/html; charset=utf-8"
        if file_path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif file_path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_status(self) -> None:
        config = load_config(self.server.config_path)
        self._ok({
            "version": SCHEMA_VERSION,
            "server_pid": os.getpid(),
            "collector": "unknown",
            "prompt_logging": True,
            "last_update": self.server.last_update or "",
            "source_count": len(config.get("sources", [])),
        })

    def _handle_sources(self) -> None:
        config = load_config(self.server.config_path)
        result = []
        for s in config.get("sources", []):
            result.append({
                "id": s["id"],
                "name": s["name"],
                "kind": s.get("kind", "archive"),
            })
        self._ok({
            "version": config.get("version", 2),
            "default_source_id": config.get("default_source_id", ""),
            "sources": result,
        })

    def _handle_projects(self) -> None:
        """Backward-compatible projects endpoint."""
        config = load_config(self.server.config_path)
        result = []
        for s in config.get("sources", []):
            result.append({
                "id": s["id"],
                "name": s["name"],
                "path": s.get("path", s.get("codex_dir", "")),
            })
        default_id = config.get("default_source_id", "")
        self._ok({
            "version": config.get("version", 2),
            "default_project_id": default_id,
            "projects": result,
        })

    def _handle_sessions(self, params: dict[str, list[str]]) -> None:
        config = load_config(self.server.config_path)
        source_id = (params.get("source_id", [""]) or [""])[0]
        project_id = (params.get("project_id", [""]) or [""])[0]

        if not source_id and project_id:
            source_id = project_id
        if not source_id:
            source_id = config.get("default_source_id", "")

        source = find_source(config, source_id)
        if not source:
            self._error(404, f"source not found: {source_id}")
            return

        kind = source.get("kind", "archive")
        if kind == "live":
            sessions = discover_live_sessions(source)
        else:
            sessions = discover_archive_sessions(source)

        show_archived = (params.get("show_archived", ["0"]) or ["0"])[0] == "1"
        if not show_archived:
            sessions = [s for s in sessions if not is_archived(source["id"], s["id"])]

        self._ok({"source_id": source["id"], "source_kind": kind, "sessions": sessions})

    def _handle_session(self, params: dict[str, list[str]]) -> None:
        config = load_config(self.server.config_path)
        source_id = (params.get("source_id", [""]) or [""])[0]
        project_id = (params.get("project_id", [""]) or [""])[0]
        session_id = (params.get("session_id", [""]) or [""])[0]

        if not source_id and project_id:
            source_id = project_id
        if not source_id:
            source_id = config.get("default_source_id", "")

        source = find_source(config, source_id)
        if not source:
            self._error(404, f"source not found: {source_id}")
            return
        if not session_id:
            self._error(400, "session_id is required")
            return

        kind = source.get("kind", "archive")
        if kind == "live":
            detail = build_live_session_detail(source, session_id)
        else:
            detail = build_archive_session_detail(source, session_id)

        if detail is None:
            self._error(404, f"session not found: {session_id}")
            return
        detail["archived"] = is_archived(source["id"], session_id)
        self._ok(detail)

    def _handle_refresh(self, body: dict[str, Any], params: dict[str, list[str]]) -> None:
        config = load_config(self.server.config_path)
        source_id = (
            body.get("source_id") or body.get("project_id")
            or (params.get("source_id", [""]) or [""])[0]
            or (params.get("project_id", [""]) or [""])[0]
        )
        session_id = body.get("session_id") or (params.get("session_id", [""]) or [""])[0]

        if not source_id:
            source_id = config.get("default_source_id", "")

        source = find_source(config, source_id)
        if not source:
            self._error(404, f"source not found: {source_id}")
            return

        kind = source.get("kind", "archive")
        if kind == "live":
            self.server.last_update = datetime.now().isoformat()
            self._ok({"refreshed": True, "refreshed_count": 1, "message": "live data reloaded"})
            return

        result: dict[str, Any] = {"refreshed": False, "message": ""}
        if session_id:
            result.update(self._refresh_archive_session(source, session_id))
        else:
            refreshed_count = 0
            sessions = discover_archive_sessions(source)
            for s in sessions:
                r = self._refresh_archive_session(source, s["id"])
                if r.get("refreshed"):
                    refreshed_count += 1
            result = {"refreshed": refreshed_count > 0, "refreshed_count": refreshed_count}

        self.server.last_update = datetime.now().isoformat()
        self._ok(result)

    def _refresh_archive_session(self, source: dict[str, Any], session_id: str) -> dict[str, Any]:
        project_path = Path(source["path"])
        runs_dir_name = source.get("runs_dir", "_local/codex-token-debugger")
        runs_dir = project_path / runs_dir_name
        run_dir = runs_dir / session_id

        if not run_dir.exists():
            return {"refreshed": False, "message": f"run dir not found: {run_dir}"}

        normalized_json = run_dir / "token-cost-normalized" / "token_cost_dashboard_data.json"
        parsed_jsonl = run_dir / "parsed" / "token_usage.jsonl"

        needs_refresh = False
        if not normalized_json.exists():
            needs_refresh = parsed_jsonl.exists()
        elif parsed_jsonl.exists():
            norm_mtime = normalized_json.stat().st_mtime
            parsed_mtime = parsed_jsonl.stat().st_mtime
            needs_refresh = parsed_mtime > norm_mtime

        if not needs_refresh:
            return {"refreshed": False, "message": "normalized data is up to date"}

        pricing_path = CONFIG_DIR / "token_pricing.json"
        if not pricing_path.exists():
            return {"refreshed": False, "message": "pricing config not found"}

        normalizer = SCRIPTS_DIR / "codex_token_cost_normalizer.py"
        if not normalizer.exists():
            return {"refreshed": False, "message": "normalizer script not found"}

        try:
            result = subprocess.run(
                [
                    sys.executable, str(normalizer),
                    "--input-dir", str(run_dir),
                    "--out-dir", str(run_dir / "token-cost-normalized"),
                    "--pricing", str(pricing_path),
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(REPO_ROOT),
            )
            if result.returncode == 0:
                return {"refreshed": True, "message": "normalization complete"}
            return {"refreshed": False, "message": f"normalizer error: {result.stderr.strip()}"}
        except subprocess.TimeoutExpired:
            return {"refreshed": False, "message": "normalizer timed out"}
        except Exception as exc:
            return {"refreshed": False, "message": str(exc)}

    def _handle_archive(self, body: dict[str, Any], params: dict[str, list[str]], *, archive: bool) -> None:
        config = load_config(self.server.config_path)
        source_id = (
            body.get("source_id") or body.get("project_id")
            or (params.get("source_id", [""]) or [""])[0]
            or (params.get("project_id", [""]) or [""])[0]
        )
        session_id = body.get("session_id") or (params.get("session_id", [""]) or [""])[0]

        if not source_id:
            source_id = config.get("default_source_id", "")
        source = find_source(config, source_id)
        if not source:
            self._error(404, f"source not found: {source_id}")
            return
        if not session_id:
            self._error(400, "session_id is required")
            return
        set_archived(source["id"], session_id, archive)
        self._ok({
            "source_id": source["id"],
            "session_id": session_id,
            "archived": archive,
        })

    def _handle_audit_session(self, body: dict[str, Any], params: dict[str, list[str]]) -> None:
        """Run audit over current session detail and return findings + artifact paths."""
        config = load_config(self.server.config_path)
        source_id = (
            body.get("source_id") or body.get("project_id")
            or (params.get("source_id", [""]) or [""])[0]
            or (params.get("project_id", [""]) or [""])[0]
        )
        session_id = body.get("session_id") or (params.get("session_id", [""]) or [""])[0]

        if not source_id:
            source_id = config.get("default_source_id", "")
        source = find_source(config, source_id)
        if not source:
            self._error(404, f"source not found: {source_id}")
            return
        if not session_id:
            self._error(400, "session_id is required")
            return

        # Build session detail using current monitor logic
        kind = source.get("kind", "archive")
        if kind == "live":
            detail = build_live_session_detail(source, session_id)
        else:
            detail = build_archive_session_detail(source, session_id)

        if detail is None:
            self._error(404, f"session not found: {session_id}")
            return

        # Filter steps if step_indices provided
        step_indices = body.get("step_indices")
        if isinstance(step_indices, list) and step_indices:
            all_steps = detail.get("steps", [])
            if isinstance(all_steps, list):
                idx_set = set(int(i) for i in step_indices)
                detail["steps"] = [s for s in all_steps if s.get("step_index") in idx_set]

        # Load and run audit module
        audit_path = SCRIPTS_DIR / "codex_token_monitor_audit.py"
        if not audit_path.exists():
            self._error(500, "audit module not found")
            return

        try:
            if str(SCRIPTS_DIR) not in sys.path:
                sys.path.insert(0, str(SCRIPTS_DIR))
            import codex_token_monitor_audit as audit_mod
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self._error(500, f"failed to load audit module: {exc}")
            return

        result = audit_mod.run_audit(
            detail,
            source_kind=kind,
            source_id=source["id"],
            session_id=session_id,
        )

        # Generate artifacts
        output_dir = AUDITS_DIR / source["id"] / session_id
        summary_path, report_path = audit_mod.generate_audit_artifacts(
            result, output_dir, session_id=session_id, source_id=source["id"]
        )

        self._ok({
            "audit_status": result["audit_status"],
            "usage_confirmation": result["usage_confirmation"],
            "step_attribution_confidence": result["step_attribution_confidence"],
            "cost_confidence": result["cost_confidence"],
            "fallback_used": result["fallback_used"],
            "findings": result["findings"],
            "step_findings": [
                {
                    "step_index": sf["step_index"],
                    "usage_available": sf["usage_available"],
                    "usage_confirmation_status": sf["usage_confirmation_status"],
                    "usage_source": sf["usage_source"],
                    "finding_count": len(sf.get("findings", [])),
                }
                for sf in result.get("step_findings", [])
            ],
            "summary_path": str(summary_path.relative_to(REPO_ROOT)),
            "report_path": str(report_path.relative_to(REPO_ROOT)),
            "source_kind": kind,
            "session_id": session_id,
            "audit_timestamp": result["audit_timestamp"],
        })

    def _handle_shutdown(self) -> None:
        self._ok({"shutdown": True, "message": "Server will stop."})
        threading.Thread(target=self.server.shutdown, daemon=True).start()


class MonitorServer(ThreadingHTTPServer):
    def __init__(self, host: str, port: int, config_path: Path) -> None:
        self.config_path = config_path
        self.last_update: str = ""
        super().__init__((host, port), MonitorHandler)


def main() -> int:
    parser = argparse.ArgumentParser(description="Codex Token Monitor Server v2")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8765, help="Bind port")
    parser.add_argument("--open-browser", action="store_true", help="Open browser on start")
    parser.add_argument("--config", default=str(CONFIG_DIR / "codex_token_monitor_projects.json"),
                        help="Path to sources config")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = REPO_ROOT / config_path

    LOCAL_MONITOR_DIR.mkdir(parents=True, exist_ok=True)

    if args.open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(f"http://{args.host}:{args.port}")).start()

    server = MonitorServer(args.host, args.port, config_path)
    print(f"Codex Token Monitor Server v2")
    print(f"http://{args.host}:{args.port}")
    print(f"Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Server stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
