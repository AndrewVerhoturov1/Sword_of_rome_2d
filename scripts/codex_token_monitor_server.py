#!/usr/bin/env python3
"""Codex Token Monitor Server v1 — local MVP utility over normalized artifacts."""
from __future__ import annotations

import argparse
import json
import os
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

SCHEMA_VERSION = "token-monitor-server.v1"
ARCHIVE_STATE_VERSION = "archive-state.v1"

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
CONFIG_DIR = REPO_ROOT / "config"
STATIC_DIR = REPO_ROOT / "static" / "codex-token-monitor"
LOCAL_MONITOR_DIR = REPO_ROOT / "_local" / "codex-token-monitor"


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


def load_projects(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {"version": 1, "default_project_id": "", "projects": []}
    return read_json(config_path)


def load_archive_state() -> dict[str, list[str]]:
    path = LOCAL_MONITOR_DIR / "archive_state.json"
    data = read_json_safe(path)
    if data and isinstance(data.get("archived_sessions"), dict):
        return data["archived_sessions"]
    return {}


def save_archive_state(state: dict[str, list[str]]) -> None:
    path = LOCAL_MONITOR_DIR / "archive_state.json"
    write_json(path, {"version": ARCHIVE_STATE_VERSION, "archived_sessions": state})


def is_archived(project_id: str, session_id: str) -> bool:
    state = load_archive_state()
    return session_id in state.get(project_id, [])


def set_archived(project_id: str, session_id: str, archived: bool) -> None:
    state = load_archive_state()
    project_archived = state.setdefault(project_id, [])
    if archived:
        if session_id not in project_archived:
            project_archived.append(session_id)
    else:
        if session_id in project_archived:
            project_archived.remove(session_id)
    save_archive_state(state)


def discover_sessions(project: dict[str, Any]) -> list[dict[str, Any]]:
    project_path = Path(project["path"])
    runs_dir_name = project.get("runs_dir", "_local/codex-token-debugger")
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

        if dashboard and isinstance(dashboard, dict):
            summary = dashboard.get("summary", {})
            turns = dashboard.get("turns", [])
            if isinstance(summary, dict):
                date_iso = _extract_date(summary, turns)
                models = summary.get("models", [])
                model = _pick_model(models)
                step_count = summary.get("turn_count", len(turns) if isinstance(turns, list) else 0)
                total_cost = summary.get("estimated_total_cost_usd")
            if isinstance(turns, list) and turns:
                efforts = sorted({str(t.get("reasoning_effort", "unknown")) for t in turns})
                reasoning = efforts[0] if len(efforts) == 1 else "mixed"
                if not date_iso:
                    date_iso = _earliest_timestamp(turns)
        else:
            has_parsed_only = True

        if not date_iso:
            mtime = entry.stat().st_mtime
            date_iso = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()

        warnings_count = 0
        if dashboard and isinstance(dashboard, dict):
            summary = dashboard.get("summary", {})
            if isinstance(summary, dict):
                warnings_count = len(summary.get("warnings", []))

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


def build_session_detail(project: dict[str, Any], session_id: str) -> dict[str, Any] | None:
    project_path = Path(project["path"])
    runs_dir_name = project.get("runs_dir", "_local/codex-token-debugger")
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
        "summary": {
            "turn_count": summary.get("turn_count", len(turns)),
            "session_count": summary.get("session_count", len(sessions_list)),
            "total_input_tokens": summary.get("total_input_tokens", 0),
            "total_cached_tokens": summary.get("total_cached_tokens", 0),
            "total_non_cached_input_tokens": summary.get("total_non_cached_input_tokens", 0),
            "average_cached_ratio": summary.get("average_cached_ratio", 0),
            "total_output_tokens": summary.get("total_output_tokens", 0),
            "total_reasoning_tokens": summary.get("total_reasoning_tokens", 0),
            "total_tool_tokens": summary.get("total_tool_tokens", 0),
            "estimated_total_cost_usd": summary.get("estimated_total_cost_usd"),
            "warnings": summary.get("warnings", []),
        },
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
    prompt_available = False
    prompt_text = ""
    answer_available = False
    answer_text = ""

    return {
        "step_index": to_int(turn.get("turn_index"), 0),
        "turn_id": str(turn.get("turn_id", "")),
        "timestamp": str(turn.get("timestamp", "")),
        "model": str(turn.get("model", "unknown")),
        "reasoning_effort": str(turn.get("reasoning_effort", "unknown")),
        "user_prompt": {
            "available": prompt_available,
            "text": prompt_text,
            "hidden_by_default": True,
        },
        "assistant_answer": {
            "available": answer_available,
            "text": answer_text,
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
        projects = load_projects(self.server.config_path)
        self._ok({
            "version": SCHEMA_VERSION,
            "server_pid": os.getpid(),
            "collector": "unknown",
            "prompt_logging": True,
            "last_update": self.server.last_update or "",
            "project_count": len(projects.get("projects", [])),
        })

    def _handle_projects(self) -> None:
        projects = load_projects(self.server.config_path)
        result = []
        for p in projects.get("projects", []):
            result.append({
                "id": p["id"],
                "name": p["name"],
                "path": p["path"],
            })
        self._ok({
            "version": projects.get("version", 1),
            "default_project_id": projects.get("default_project_id", ""),
            "projects": result,
        })

    def _handle_sessions(self, params: dict[str, list[str]]) -> None:
        projects = load_projects(self.server.config_path)
        project_id = (params.get("project_id", [""]) or [""])[0]
        default_id = projects.get("default_project_id", "")
        if not project_id:
            project_id = default_id
        project = _find_project(projects, project_id)
        if not project:
            self._error(404, f"project not found: {project_id}")
            return
        sessions = discover_sessions(project)
        show_archived = (params.get("show_archived", ["0"]) or ["0"])[0] == "1"
        if not show_archived:
            sessions = [s for s in sessions if not is_archived(project["id"], s["id"])]
        self._ok({"project_id": project["id"], "sessions": sessions})

    def _handle_session(self, params: dict[str, list[str]]) -> None:
        projects = load_projects(self.server.config_path)
        project_id = (params.get("project_id", [""]) or [""])[0]
        session_id = (params.get("session_id", [""]) or [""])[0]
        if not project_id:
            project_id = projects.get("default_project_id", "")
        project = _find_project(projects, project_id)
        if not project:
            self._error(404, f"project not found: {project_id}")
            return
        if not session_id:
            self._error(400, "session_id is required")
            return
        detail = build_session_detail(project, session_id)
        if detail is None:
            self._error(404, f"session not found: {session_id}")
            return
        detail["archived"] = is_archived(project["id"], session_id)
        self._ok(detail)

    def _handle_refresh(self, body: dict[str, Any], params: dict[str, list[str]]) -> None:
        projects = load_projects(self.server.config_path)
        project_id = body.get("project_id") or (params.get("project_id", [""]) or [""])[0]
        session_id = body.get("session_id") or (params.get("session_id", [""]) or [""])[0]
        if not project_id:
            project_id = projects.get("default_project_id", "")
        project = _find_project(projects, project_id)
        if not project:
            self._error(404, f"project not found: {project_id}")
            return

        result = {"refreshed": False, "message": ""}

        if session_id:
            result.update(self._refresh_session(project, session_id))
        else:
            refreshed_count = 0
            sessions = discover_sessions(project)
            for s in sessions:
                r = self._refresh_session(project, s["id"])
                if r.get("refreshed"):
                    refreshed_count += 1
            result = {"refreshed": refreshed_count > 0, "refreshed_count": refreshed_count}

        self.server.last_update = datetime.now().isoformat()
        self._ok(result)

    def _refresh_session(self, project: dict[str, Any], session_id: str) -> dict[str, Any]:
        project_path = Path(project["path"])
        runs_dir_name = project.get("runs_dir", "_local/codex-token-debugger")
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
        projects = load_projects(self.server.config_path)
        project_id = body.get("project_id") or (params.get("project_id", [""]) or [""])[0]
        session_id = body.get("session_id") or (params.get("session_id", [""]) or [""])[0]
        if not project_id:
            project_id = projects.get("default_project_id", "")
        project = _find_project(projects, project_id)
        if not project:
            self._error(404, f"project not found: {project_id}")
            return
        if not session_id:
            self._error(400, "session_id is required")
            return
        set_archived(project["id"], session_id, archive)
        self._ok({
            "project_id": project["id"],
            "session_id": session_id,
            "archived": archive,
        })

    def _handle_shutdown(self) -> None:
        self._ok({"shutdown": True, "message": "Server will stop."})
        threading.Thread(target=self.server.shutdown, daemon=True).start()


class MonitorServer(ThreadingHTTPServer):
    def __init__(self, host: str, port: int, config_path: Path) -> None:
        self.config_path = config_path
        self.last_update: str = ""
        super().__init__((host, port), MonitorHandler)


def _find_project(projects: dict[str, Any], project_id: str) -> dict[str, Any] | None:
    for p in projects.get("projects", []):
        if p["id"] == project_id:
            return p
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Codex Token Monitor Server v1")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8765, help="Bind port")
    parser.add_argument("--open-browser", action="store_true", help="Open browser on start")
    parser.add_argument("--config", default=str(CONFIG_DIR / "codex_token_monitor_projects.json"),
                        help="Path to projects config")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = REPO_ROOT / config_path

    LOCAL_MONITOR_DIR.mkdir(parents=True, exist_ok=True)

    if args.open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(f"http://{args.host}:{args.port}")).start()

    server = MonitorServer(args.host, args.port, config_path)
    print(f"Codex Token Monitor Server v1")
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
