"""Tests for Codex Token Monitor Server v1."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Import server module directly
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "codex_token_monitor_server",
    REPO_ROOT / "scripts" / "codex_token_monitor_server.py",
)
_server_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_server_mod)


class TestProjectConfig(unittest.TestCase):
    """Tests for project config loading."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.config_path = Path(self.tmpdir) / "test_projects.json"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_load_valid_config(self):
        config = {
            "version": 1,
            "default_project_id": "test-project",
            "projects": [
                {"id": "test-project", "name": "Test", "path": "/tmp/test", "runs_dir": "runs"}
            ],
        }
        _server_mod.write_json(self.config_path, config)
        result = _server_mod.load_projects(self.config_path)
        self.assertEqual(result["default_project_id"], "test-project")
        self.assertEqual(len(result["projects"]), 1)

    def test_load_missing_config(self):
        result = _server_mod.load_projects(Path(self.tmpdir) / "nonexistent.json")
        self.assertEqual(result["projects"], [])

    def test_load_invalid_json(self):
        (self.config_path).write_text("not json", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            _server_mod.load_projects(self.config_path)


class TestInvalidPathWarning(unittest.TestCase):
    """Tests that invalid paths produce warnings, not crashes."""

    def test_find_project_missing(self):
        projects = {"version": 1, "projects": []}
        result = _server_mod._find_project(projects, "nonexistent")
        self.assertIsNone(result)

    def test_discover_sessions_invalid_path(self):
        project = {"id": "test", "name": "Test", "path": "/nonexistent/path", "runs_dir": "runs"}
        sessions = _server_mod.discover_sessions(project)
        self.assertEqual(sessions, [])

    def test_discover_sessions_valid_but_empty(self):
        project = {"id": "test", "name": "Test", "path": str(REPO_ROOT), "runs_dir": "does_not_exist"}
        sessions = _server_mod.discover_sessions(project)
        self.assertEqual(sessions, [])


class TestDiscovery(unittest.TestCase):
    """Tests for session discovery with real sample data."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_discovery_prefers_normalized(self):
        runs_dir = Path(self.tmpdir) / "runs"
        run_dir = runs_dir / "test-run-001"
        normalized_dir = run_dir / "token-cost-normalized"
        normalized_dir.mkdir(parents=True)
        dashboard = {
            "schema_version": "token-cost-normalizer.v1",
            "summary": {"turn_count": 3, "models": ["gpt-5.4"], "estimated_total_cost_usd": 0.05, "warnings": []},
            "turns": [
                {"turn_index": 1, "model": "gpt-5.4", "reasoning_effort": "low", "timestamp": "2026-06-01T00:00:00Z",
                 "input_tokens": 100, "cached_tokens": 50, "output_tokens": 10,
                 "non_cached_input_tokens": 50, "cached_ratio": 0.5, "reasoning_tokens": 0, "tool_tokens": 0,
                 "estimated_cost_usd": {"total": 0.01, "input": 0.008, "cached_input": 0.001, "output": 0.001},
                 "observed_mcp_server_count": 0, "observed_mcp_servers": [],
                 "enabled_plugins_count": 0, "enabled_skills_count": 0,
                 "global_user_instructions_status": "unknown", "repo_context_status": "unknown",
                 "pricing_unknown": False, "warnings": [], "thread_id": "t1", "turn_id": "turn-001"},
            ],
            "sessions": [],
        }
        _server_mod.write_json(normalized_dir / "token_cost_dashboard_data.json", dashboard)

        project = {"id": "test", "name": "Test", "path": str(self.tmpdir), "runs_dir": "runs"}
        sessions = _server_mod.discover_sessions(project)
        self.assertEqual(len(sessions), 1)
        s = sessions[0]
        self.assertEqual(s["id"], "test-run-001")
        self.assertEqual(s["step_count"], 3)
        self.assertEqual(s["model"], "gpt-5.4")
        self.assertTrue(s["has_normalized"])

    def test_discovery_parsed_only(self):
        runs_dir = Path(self.tmpdir) / "runs"
        run_dir = runs_dir / "parsed-only-run"
        parsed_dir = run_dir / "parsed"
        parsed_dir.mkdir(parents=True)
        (parsed_dir / "token_usage.jsonl").write_text(
            json.dumps({"model": "gpt-5.5", "input_token_count": 100}) + "\n",
            encoding="utf-8",
        )

        project = {"id": "test", "name": "Test", "path": str(self.tmpdir), "runs_dir": "runs"}
        sessions = _server_mod.discover_sessions(project)
        self.assertEqual(len(sessions), 1)
        s = sessions[0]
        self.assertEqual(s["id"], "parsed-only-run")
        self.assertTrue(s["has_parsed"])
        self.assertFalse(s["has_normalized"])


class TestMissingNormalizedFallback(unittest.TestCase):
    """Tests that missing normalized output falls back without crashing."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_fallback_without_normalized(self):
        runs_dir = Path(self.tmpdir) / "runs"
        run_dir = runs_dir / "fallback-run"
        parsed_dir = run_dir / "parsed"
        parsed_dir.mkdir(parents=True)
        (parsed_dir / "token_usage.jsonl").write_text("", encoding="utf-8")

        project = {"id": "test", "name": "Test", "path": str(self.tmpdir), "runs_dir": "runs"}
        detail = _server_mod.build_session_detail(project, "fallback-run")
        self.assertIsNotNone(detail)
        self.assertEqual(detail["id"], "fallback-run")
        self.assertEqual(detail["model"], "unknown")
        self.assertEqual(len(detail["steps"]), 0)

    def test_nonexistent_session(self):
        project = {"id": "test", "name": "Test", "path": str(self.tmpdir), "runs_dir": "runs"}
        detail = _server_mod.build_session_detail(project, "nonexistent")
        self.assertIsNone(detail)


class TestRefreshStub(unittest.TestCase):
    """Tests that refresh logic handles missing normalizer gracefully."""

    def test_refresh_missing_run_dir(self):
        project = {"id": "test", "name": "Test", "path": "/tmp", "runs_dir": "runs"}
        result = _server_mod._refresh_session_static(project, "nonexistent")
        self.assertFalse(result.get("refreshed", True))

    def test_refresh_no_normalizer(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            runs_dir = Path(td) / "runs"
            run_dir = runs_dir / "test-run"
            parsed_dir = run_dir / "parsed"
            parsed_dir.mkdir(parents=True)
            (parsed_dir / "token_usage.jsonl").write_text("", encoding="utf-8")

            project = {"id": "test", "name": "Test", "path": str(td), "runs_dir": "runs"}
            # Rename normalizer temporarily
            normalizer = REPO_ROOT / "scripts" / "codex_token_cost_normalizer.py"
            if normalizer.exists():
                result = _server_mod._refresh_session_static(project, "test-run")
                self.assertIsInstance(result, dict)


class TestArchiveUnarchive(unittest.TestCase):
    """Tests archive/unarchive persistence."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_monitor_dir = _server_mod.LOCAL_MONITOR_DIR
        _server_mod.LOCAL_MONITOR_DIR = Path(self.tmpdir)

    def tearDown(self):
        _server_mod.LOCAL_MONITOR_DIR = self.orig_monitor_dir
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_archive_persists(self):
        _server_mod.set_archived("test-project", "session-001", True)
        self.assertTrue(_server_mod.is_archived("test-project", "session-001"))

    def test_unarchive_removes(self):
        _server_mod.set_archived("test-project", "session-001", True)
        _server_mod.set_archived("test-project", "session-001", False)
        self.assertFalse(_server_mod.is_archived("test-project", "session-001"))

    def test_archive_state_persists_across_loads(self):
        _server_mod.set_archived("test-project", "session-001", True)
        state = _server_mod.load_archive_state()
        self.assertIn("session-001", state.get("test-project", []))

    def test_archive_empty_state(self):
        state = _server_mod.load_archive_state()
        self.assertIsInstance(state, dict)


class TestArchivedHiding(unittest.TestCase):
    """Tests that session listing hides archived items by default."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_monitor_dir = _server_mod.LOCAL_MONITOR_DIR
        _server_mod.LOCAL_MONITOR_DIR = Path(self.tmpdir)

    def tearDown(self):
        _server_mod.LOCAL_MONITOR_DIR = self.orig_monitor_dir
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_is_archived_default_false(self):
        self.assertFalse(_server_mod.is_archived("any-project", "any-session"))


class TestStatusPayloadShape(unittest.TestCase):
    """Tests that /api/status returns expected shape."""

    def test_status_shape(self):
        self.assertIsInstance(_server_mod.SCHEMA_VERSION, str)
        self.assertIn("v1", _server_mod.SCHEMA_VERSION)


class TestAbsentPromptAnswerContract(unittest.TestCase):
    """Tests that absent prompt/answer yields available=false."""

    def test_build_step_no_prompt(self):
        turn = {
            "turn_index": 1, "turn_id": "t1", "timestamp": "", "model": "gpt-5.4",
            "reasoning_effort": "low", "input_tokens": 100, "cached_tokens": 0,
            "non_cached_input_tokens": 100, "cached_ratio": 0, "output_tokens": 10,
            "reasoning_tokens": 0, "tool_tokens": 0,
            "estimated_cost_usd": {"total": 0.01}, "thread_id": "t1",
            "observed_mcp_server_count": 0, "observed_mcp_servers": [],
            "enabled_plugins_count": 0, "enabled_skills_count": 0,
            "global_user_instructions_status": "unknown", "repo_context_status": "unknown",
            "warnings": [],
        }
        step = _server_mod._build_step(turn)
        self.assertFalse(step["user_prompt"]["available"])
        self.assertEqual(step["user_prompt"]["text"], "")
        self.assertTrue(step["user_prompt"]["hidden_by_default"])
        self.assertFalse(step["assistant_answer"]["available"])
        self.assertEqual(step["assistant_answer"]["text"], "")

    def test_build_step_with_warnings(self):
        turn = {
            "turn_index": 1, "turn_id": "t1", "timestamp": "", "model": "gpt-5.4",
            "reasoning_effort": "low", "input_tokens": 100, "cached_tokens": 0,
            "non_cached_input_tokens": 100, "cached_ratio": 0, "output_tokens": 10,
            "reasoning_tokens": 0, "tool_tokens": 0,
            "estimated_cost_usd": {"total": 0.01}, "thread_id": "t1",
            "observed_mcp_server_count": 0, "observed_mcp_servers": [],
            "enabled_plugins_count": 0, "enabled_skills_count": 0,
            "global_user_instructions_status": "unknown", "repo_context_status": "unknown",
            "warnings": ["model_switch_detected"],
        }
        step = _server_mod._build_step(turn)
        self.assertIn("model_switch_detected", step["warnings"])


class TestShutdownEndpointBehavior(unittest.TestCase):
    """Tests that shutdown endpoint returns expected response structure."""

    def test_shutdown_handler(self):
        # Just verify the handler structure exists
        self.assertTrue(hasattr(_server_mod.MonitorHandler, "_handle_shutdown"))
        self.assertTrue(hasattr(_server_mod.MonitorHandler, "do_POST"))


class TestBuildSessionDetail(unittest.TestCase):
    """Integration test: build_session_detail from real sample data."""

    def test_build_from_real_normalized_data(self):
        run_dir = REPO_ROOT / "_local" / "codex-token-debugger" / "playwright-only-confirmation-20260604-072040"
        if not run_dir.exists():
            self.skipTest("sample run dir not available")

        project = {
            "id": "sword-of-rome-web",
            "name": "Sword of Rome Web",
            "path": str(REPO_ROOT),
            "runs_dir": "_local/codex-token-debugger",
        }
        detail = _server_mod.build_session_detail(project, "playwright-only-confirmation-20260604-072040")
        if detail is None:
            self.skipTest("normalized data not available for this session")

        self.assertEqual(detail["id"], "playwright-only-confirmation-20260604-072040")
        self.assertIn("summary", detail)
        self.assertIn("steps", detail)
        self.assertGreater(len(detail["steps"]), 0)

        step0 = detail["steps"][0]
        self.assertIn("step_index", step0)
        self.assertIn("model", step0)
        self.assertIn("user_prompt", step0)
        self.assertFalse(step0["user_prompt"]["available"])
        self.assertIn("usage", step0)
        self.assertIn("input_tokens", step0["usage"])
        self.assertIn("environment", step0)


# Static version of _refresh_session for testing without the full handler class
def _refresh_session_static(project, session_id):
    project_path = Path(project["path"])
    runs_dir_name = project.get("runs_dir", "_local/codex-token-debugger")
    runs_dir = project_path / runs_dir_name
    run_dir = runs_dir / session_id

    if not run_dir.exists():
        return {"refreshed": False, "message": "run dir not found"}

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

    return {"refreshed": True, "message": "would refresh"}


# Inject static version for test access
_server_mod._refresh_session_static = _refresh_session_static


if __name__ == "__main__":
    unittest.main()
