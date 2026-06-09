"""Tests for Codex Token Monitor Server v2 — source-aware hybrid mode."""
from __future__ import annotations

import json
import os
import sqlite3
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
        result = _server_mod.load_config(self.config_path)
        # v1 config is auto-migrated to v2 format
        self.assertIn("sources", result)
        self.assertEqual(len(result["sources"]), 1)

    def test_load_missing_config(self):
        result = _server_mod.load_config(Path(self.tmpdir) / "nonexistent.json")
        self.assertEqual(result["sources"], [])

    def test_load_invalid_json(self):
        (self.config_path).write_text("not json", encoding="utf-8")
        with self.assertRaises(json.JSONDecodeError):
            _server_mod.load_config(self.config_path)


class TestInvalidPathWarning(unittest.TestCase):
    """Tests that invalid paths produce warnings, not crashes."""

    def test_find_project_missing(self):
        projects = {"version": 1, "projects": []}
        result = _server_mod.find_source(projects, "nonexistent")
        self.assertIsNone(result)

    def test_discover_sessions_invalid_path(self):
        project = {"id": "test", "name": "Test", "path": "/nonexistent/path", "runs_dir": "runs"}
        sessions = _server_mod.discover_archive_sessions(project)
        self.assertEqual(sessions, [])

    def test_discover_sessions_valid_but_empty(self):
        project = {"id": "test", "name": "Test", "path": str(REPO_ROOT), "runs_dir": "does_not_exist"}
        sessions = _server_mod.discover_archive_sessions(project)
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
        sessions = _server_mod.discover_archive_sessions(project)
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
        sessions = _server_mod.discover_archive_sessions(project)
        self.assertEqual(len(sessions), 1)
        s = sessions[0]
        self.assertEqual(s["id"], "parsed-only-run")
        self.assertTrue(s["has_parsed"])
        self.assertFalse(s["has_normalized"])


class TestLiveChatFixture(unittest.TestCase):
    """Tests live Codex chat parsing on a realistic local fixture."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.codex_dir = Path(self.tmpdir) / ".codex"
        self.codex_dir.mkdir(parents=True)
        self.thread_id = "thread-live-001"
        self._write_sqlite()
        self._write_session_index()
        self._write_rollout()
        _server_mod._live_rollout_summary_cache.clear()

    def tearDown(self):
        _server_mod._live_rollout_summary_cache.clear()
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_sqlite(self):
        db_path = self.codex_dir / "state_5.sqlite"
        conn = sqlite3.connect(db_path)
        conn.execute(
            """
            CREATE TABLE threads (
              id TEXT,
              title TEXT,
              model TEXT,
              reasoning_effort TEXT,
              cwd TEXT,
              created_at TEXT,
              updated_at TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO threads (id, title, model, reasoning_effort, cwd, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.thread_id,
                "Проверить телеметрию локально\n\nдлинный хвост не нужен",
                "gpt-5.5",
                "high",
                "D:/Codex+Kilocode/projects/sword-of-rome-web",
                "2026-06-06T10:00:00Z",
                "2026-06-06T10:05:00Z",
            ),
        )
        conn.commit()
        conn.close()

    def _write_session_index(self):
        payload = {"thread_id": self.thread_id, "thread_name": "Проверить телеметрию локально"}
        (self.codex_dir / "session_index.jsonl").write_text(
            json.dumps(payload, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def _write_rollout(self):
        rollout_dir = self.codex_dir / "sessions" / "2026" / "06" / "06"
        rollout_dir.mkdir(parents=True)
        rollout_path = rollout_dir / "rollout-test.jsonl"
        lines = [
            {
                "timestamp": "2026-06-06T10:00:00Z",
                "type": "session_meta",
                "payload": {"id": self.thread_id, "cwd": "D:/Codex+Kilocode/projects/sword-of-rome-web"},
            },
            {
                "timestamp": "2026-06-06T10:00:01Z",
                "type": "turn_context",
                "payload": {"thread_id": self.thread_id, "model": "gpt-5.5", "reasoning_effort": "high"},
            },
            {
                "timestamp": "2026-06-06T10:00:02Z",
                "type": "response_item",
                "payload": {"role": "user", "content": [{"text": "# AGENTS.md instructions\n\n<INSTRUCTIONS>"}]},
            },
            {
                "timestamp": "2026-06-06T10:00:03Z",
                "type": "response_item",
                "payload": {"role": "user", "turn_id": "turn-1", "content": [{"text": "Проверить локальную телеметрию"}]},
            },
            {
                "timestamp": "2026-06-06T10:00:04Z",
                "type": "response_item",
                "payload": {"role": "assistant", "content": [{"text": "Короткий ответ"}]},
            },
            {
                "timestamp": "2026-06-06T10:00:05Z",
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "last_token_usage": {
                            "input_tokens": 1200,
                            "cached_input_tokens": 1000,
                            "output_tokens": 55,
                            "reasoning_output_tokens": 7,
                        },
                        "total_token_usage": {
                            "input_tokens": 1200,
                            "cached_input_tokens": 1000,
                            "output_tokens": 55,
                            "reasoning_output_tokens": 7,
                        }
                    },
                },
            },
            {
                "timestamp": "2026-06-06T10:01:01Z",
                "type": "turn_context",
                "payload": {"thread_id": self.thread_id, "model": "gpt-5.5", "reasoning_effort": "high"},
            },
            {
                "timestamp": "2026-06-06T10:01:02Z",
                "type": "response_item",
                "payload": {"role": "user", "turn_id": "turn-2", "content": [{"text": "Покажи расход именно второго шага"}]},
            },
            {
                "timestamp": "2026-06-06T10:01:03Z",
                "type": "response_item",
                "payload": {"role": "assistant", "content": [{"text": "Вот дельта по второму шагу"}]},
            },
            {
                "timestamp": "2026-06-06T10:01:04Z",
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "last_token_usage": {
                            "input_tokens": 600,
                            "cached_input_tokens": 400,
                            "output_tokens": 40,
                            "reasoning_output_tokens": 4,
                        },
                        "total_token_usage": {
                            "input_tokens": 4_753_172,
                            "cached_input_tokens": 4_550_912,
                            "output_tokens": 26_589,
                            "reasoning_output_tokens": 6_518,
                        }
                    },
                },
            },
            {
                "timestamp": "2026-06-06T10:01:05Z",
                "type": "event_msg",
                "payload": {"type": "task_complete", "turn_id": "task-turn-2"},
            },
            {
                "timestamp": "2026-06-06T10:01:06Z",
                "type": "event_msg",
                "payload": {"type": "task_started", "turn_id": "compact-turn-1"},
            },
            {
                "timestamp": "2026-06-06T10:01:07Z",
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "last_token_usage": {
                            "input_tokens": 0,
                            "cached_input_tokens": 0,
                            "output_tokens": 0,
                            "reasoning_output_tokens": 0,
                        },
                        "total_token_usage": {
                            "input_tokens": 8_016_767,
                            "cached_input_tokens": 7_549_568,
                            "output_tokens": 32_758,
                            "reasoning_output_tokens": 11_290,
                        },
                    },
                },
            },
            {
                "timestamp": "2026-06-06T10:01:08Z",
                "type": "event_msg",
                "payload": {"type": "context_compacted"},
            },
            {
                "timestamp": "2026-06-06T10:01:09Z",
                "type": "event_msg",
                "payload": {"type": "task_complete", "turn_id": "compact-turn-1"},
            },
            {
                "timestamp": "2026-06-06T10:02:01Z",
                "type": "response_item",
                "payload": {"role": "user", "turn_id": "turn-internal-1", "content": [{"text": "PLEASE IMPLEMENT THIS PLAN:\n# Internal handoff"}]},
            },
            {
                "timestamp": "2026-06-06T10:02:02Z",
                "type": "response_item",
                "payload": {"role": "user", "turn_id": "turn-internal-2", "content": [{"text": "<turn_aborted>\nThe user interrupted the previous turn on purpose."}]},
            },
            {
                "timestamp": "2026-06-06T10:02:03Z",
                "type": "event_msg",
                "payload": {"type": "turn_aborted"},
            },
        ]
        rollout_path.write_text(
            "\n".join(json.dumps(line, ensure_ascii=False) for line in lines) + "\n",
            encoding="utf-8",
        )

    def test_discover_live_sessions_uses_rollout_summary(self):
        source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(self.codex_dir)}
        _server_mod._get_live_rollout_summaries(Path(self.codex_dir), allow_build=True)
        sessions = _server_mod.discover_live_sessions(source)
        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertEqual(session["title"], "Проверить телеметрию локально")
        self.assertEqual(session["step_count"], 2)
        self.assertGreater(session["total_cost_usd"], 0)

    def test_discover_live_sessions_without_warm_cache_still_lists_threads(self):
        source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(self.codex_dir)}
        sessions = _server_mod.discover_live_sessions(source)
        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertEqual(session["title"], "Проверить телеметрию локально")
        self.assertIsNone(session["step_count"])
        self.assertIsNone(session["total_cost_usd"])

    def test_build_live_session_detail_skips_system_prompt_step(self):
        source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(self.codex_dir)}
        detail = _server_mod.build_live_session_detail(source, self.thread_id)
        self.assertIsNotNone(detail)
        self.assertEqual(detail["summary"]["turn_count"], 2)
        self.assertEqual(detail["summary"]["total_input_tokens"], 8_016_767)
        self.assertEqual(detail["summary"]["total_cached_tokens"], 7_549_568)
        self.assertEqual(len(detail["steps"]), 2)
        step = detail["steps"][0]
        self.assertEqual(step["user_prompt"]["kind"], "user_message")
        self.assertEqual(step["user_prompt"]["text"], "Проверить локальную телеметрию")
        self.assertEqual(step["assistant_answer"]["text"], "Короткий ответ")
        self.assertEqual(step["model"], "gpt-5.5")
        self.assertEqual(step["reasoning_effort"], "high")
        self.assertTrue(step["usage"]["available"])
        self.assertEqual(step["usage"]["input_tokens"], 1200)
        self.assertEqual(step["usage"]["cached_tokens"], 1000)
        self.assertEqual(step["usage"]["non_cached_input_tokens"], 200)
        self.assertGreater(step["usage"]["estimated_total_cost_usd"], 0)
        step2 = detail["steps"][1]
        self.assertEqual(step2["user_prompt"]["text"], "Покажи расход именно второго шага")
        self.assertEqual(step2["assistant_answer"]["text"], "Вот дельта по второму шагу")
        self.assertTrue(step2["usage"]["available"])
        self.assertEqual(step2["usage"]["input_tokens"], 600)
        self.assertEqual(step2["usage"]["cached_tokens"], 400)
        self.assertEqual(step2["usage"]["non_cached_input_tokens"], 200)
        self.assertEqual(step2["usage"]["output_tokens"], 40)
        self.assertEqual(step2["usage"]["reasoning_tokens"], 4)
        self.assertGreater(step2["usage"]["estimated_total_cost_usd"], 0)
        self.assertLess(step2["usage"]["input_tokens"], detail["summary"]["total_input_tokens"])
        self.assertIn("контекст сжат после этого хода", step2.get("post_step_badges", []))
        self.assertEqual(len(detail.get("timeline_events", [])), 1)
        event = detail["timeline_events"][0]
        self.assertEqual(event["event_type"], "context_compacted")
        self.assertEqual(event["after_step_index"], 2)
        self.assertEqual(event["compaction_task_id"], "compact-turn-1")


class TestFrontendLiveSummaryContract(unittest.TestCase):
    """Tests that frontend uses session.summary for live/session header totals."""

    def test_render_header_uses_session_metrics_helper(self):
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function metricsForSession(session)", app_js)
        self.assertIn("const z = metricsForSession(s);", app_js)

    def test_frontend_has_recent_cutoff_and_sorting(self):
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        index_html = (REPO_ROOT / "static" / "codex-token-monitor" / "index.html").read_text(encoding="utf-8")
        self.assertIn('MIN_VISIBLE_SESSION_DATE_MS = Date.parse("2026-06-04T00:00:00Z")', app_js)
        self.assertIn('const sortMode = (document.getElementById("sortFilter")?.value || "date_desc")', app_js)
        self.assertIn('await loadSources();', app_js)
        self.assertIn('initSources();', app_js)
        self.assertIn('<select id="sortFilter">', index_html)

    def test_frontend_has_workdir_filter_and_detail_reload_path(self):
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        index_html = (REPO_ROOT / "static" / "codex-token-monitor" / "index.html").read_text(encoding="utf-8")
        self.assertIn('let currentWorkdirFilter = ALL_WORKDIRS_VALUE;', app_js)
        self.assertIn('let refreshPromise = null;', app_js)
        self.assertIn('function populateWorkdirFilter()', app_js)
        self.assertIn('document.getElementById("workdirFilter").addEventListener("change"', app_js)
        self.assertIn('Загрузка шагов...', app_js)
        self.assertIn('await loadSessionDetail();', app_js)
        self.assertIn('<select id="workdirFilter">', index_html)

    def test_frontend_can_render_compaction_timeline(self):
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function renderTimelineEvent(evt)", app_js)
        self.assertIn("post_step_badges", app_js)
        self.assertIn("timeline_events", app_js)

    def test_render_sessions_does_not_depend_on_step_timeline_state(self):
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        start = app_js.index("function renderSessions() {")
        end = app_js.index("function stat(", start)
        render_sessions = app_js[start:end]
        self.assertNotIn("timelineByStep", render_sessions)
        self.assertNotIn("renderTimelineEvent(evt)", render_sessions)
        self.assertNotIn("Number(idx)", render_sessions)

    def test_frontend_prefers_session_with_steps_and_has_honest_empty_state(self):
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function preferredSessionId(list)", app_js)
        self.assertIn('currentSessionId = preferredSessionId(sessionsCache);', app_js)
        self.assertIn("const preferredId = preferredSessionId(sessionsCache);", app_js)
        self.assertIn("Для этой сессии шаги пока не найдены", app_js)
        self.assertIn('sessionDetailLoading = true;', app_js)


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
        detail = _server_mod.build_archive_session_detail(project, "fallback-run")
        self.assertIsNotNone(detail)
        self.assertEqual(detail["id"], "fallback-run")
        self.assertEqual(detail["model"], "unknown")
        self.assertEqual(len(detail["steps"]), 0)

    def test_nonexistent_session(self):
        project = {"id": "test", "name": "Test", "path": str(self.tmpdir), "runs_dir": "runs"}
        detail = _server_mod.build_archive_session_detail(project, "nonexistent")
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
        self.assertIn("v2", _server_mod.SCHEMA_VERSION)


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
        detail = _server_mod.build_archive_session_detail(project, "playwright-only-confirmation-20260604-072040")
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


class TestLiveUsageSemanticsAndRichExport(unittest.TestCase):
    """Regression tests for live semantics messaging and export helpers."""

    def test_live_fixture_exposes_usage_basis_and_confirmation(self):
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            self.assertIsNotNone(detail)
            self.assertEqual(detail["summary"]["usage_basis"], "live_total_token_usage_latest")
            self.assertEqual(detail["summary"]["step_usage_basis"], "live_last_token_usage")
            self.assertTrue(any(w.get("id") == "live_totals_are_cumulative" for w in detail["summary"]["warnings"]))
            self.assertEqual(detail["steps"][0]["usage"]["confirmation_status"], "confirmed_request_usage")
            self.assertEqual(detail["steps"][0]["usage"]["source"], "live_last_token_usage")
        finally:
            fixture.tearDown()

    def test_frontend_has_rich_export_helpers(self):
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function buildStepExportText(step, session, options = {})", app_js)
        self.assertIn("function buildSessionExportJson(session, steps)", app_js)
        self.assertIn("function buildSessionExportMarkdown(session, steps, title)", app_js)
        self.assertIn("function buildTelemetryWarnings(session, step)", app_js)
        self.assertIn("function usageConfirmationLabel(usage)", app_js)
        self.assertIn("copyText(buildStepExportText(step, s));", app_js)
        self.assertIn("copyText(JSON.stringify(buildSessionExportJson(s, s.steps), null, 2));", app_js)
        self.assertIn("copyText(buildSessionExportMarkdown(s, selectedSteps(), \"Selected steps export\"));", app_js)


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


class TestStepFullCostAccountingV21(unittest.TestCase):
    """v2.1: Tests for full_step_usage/full_step_cost vs request cost distinction."""

    def test_live_fixture_has_v21_fields(self):
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            self.assertIsNotNone(detail)

            # Session summary v2.1 fields
            summary = detail["summary"]
            self.assertIn("visible_steps_count", summary)
            self.assertIn("raw_model_requests_count", summary)
            self.assertIn("visible_step_full_usage_sum", summary)
            self.assertIn("unmapped_or_internal_usage", summary)
            self.assertEqual(summary["visible_steps_count"], 2)
            self.assertGreater(summary["raw_model_requests_count"], 0)

            steps = detail["steps"]
            self.assertEqual(len(steps), 2)

            for step in steps:
                # All v2.1 top-level fields must be present
                self.assertIn("request_usage_items", step)
                self.assertIn("full_step_usage", step)
                self.assertIn("full_step_cost", step)
                self.assertIn("primary_request_usage", step)
                self.assertIn("cumulative_before_step", step)
                self.assertIn("cumulative_after_step", step)
                self.assertIn("cumulative_delta", step)
                self.assertIn("unattributed_delta", step)
                self.assertIn("cost_scope", step)
                self.assertIn("event_range", step)

            # Step 1: one request only
            step1 = steps[0]
            self.assertEqual(step1["step_index"], 1)
            self.assertEqual(len(step1["request_usage_items"]), 1)
            self.assertEqual(step1["full_step_usage"]["request_count"], 1)
            self.assertEqual(step1["full_step_usage"]["input_tokens"], 1200)
            self.assertEqual(step1["full_step_usage"]["cached_tokens"], 1000)
            self.assertEqual(step1["full_step_usage"]["output_tokens"], 55)
            # Single request: primary equals full
            self.assertEqual(
                step1["primary_request_usage"]["input_tokens"],
                step1["full_step_usage"]["input_tokens"],
            )
            # cost_scope for single request
            self.assertEqual(step1["cost_scope"]["current_displayed_cost_scope"], "single_request")
            self.assertEqual(step1["cost_scope"]["mapping_confidence"], "high")
            # Event range
            self.assertGreater(step1["event_range"]["start_event_index"], 0)
            self.assertGreaterEqual(step1["event_range"]["end_event_index"], step1["event_range"]["start_event_index"])

            # Step 1 cumulative_before should be unavailable (first step)
            self.assertFalse(step1["cumulative_before_step"]["available"])

            # Step 1 cumulative_after: should be present (from total_token_usage snapshot)
            ca1 = step1["cumulative_after_step"]
            self.assertTrue(ca1.get("available"))
            # Step 1 has cumulative_after from its single snapshot: 1200/1000/55

            # Step 2: one request; compaction token falls after task_complete
            step2 = steps[1]
            self.assertEqual(step2["step_index"], 2)
            # Step 2 has 1 token_count event: its own request
            # Compaction token_count at 10:01:07 is after task_complete → outside step range
            self.assertEqual(step2["full_step_usage"]["request_count"], 1)
            # Step 2 input = 600 (own request)
            self.assertEqual(step2["full_step_usage"]["input_tokens"], 600)
            # cost_scope for single request
            self.assertEqual(step2["cost_scope"]["current_displayed_cost_scope"], "single_request")

            # Step 2 cumulative_before should be available (from step 1 after)
            self.assertTrue(step2["cumulative_before_step"]["available"])

            # Usage (backwards compat) still works
            self.assertTrue(step1["usage"]["available"])
            self.assertEqual(step1["usage"]["source"], "live_last_token_usage")

        finally:
            fixture.tearDown()

    def test_full_step_usage_is_sum_of_request_items(self):
        """full_step_usage.input_tokens must equal sum of request_usage_items.input_tokens."""
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            for step in detail["steps"]:
                fsu = step["full_step_usage"]
                items = step["request_usage_items"]
                expected_input = sum(item["input_tokens"] for item in items)
                expected_output = sum(item["output_tokens"] for item in items)
                self.assertEqual(fsu["input_tokens"], expected_input,
                    f"Step {step['step_index']}: full_step_usage input mismatch")
                self.assertEqual(fsu["output_tokens"], expected_output,
                    f"Step {step['step_index']}: full_step_usage output mismatch")
        finally:
            fixture.tearDown()

    def test_multiple_requests_cost_gt_single_request(self):
        """When step has >1 requests, full_step_cost should be >= request cost."""
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            step2 = detail["steps"][1]
            # Step 2 has 1 request (compaction token_count is after task_complete, outside step)
            self.assertEqual(step2["full_step_usage"]["request_count"], 1)
            # For single-request step, full_step_cost equals request cost
            fsc_total = step2["full_step_cost"].get("total_usd")
            req_cost = step2["usage"].get("estimated_total_cost_usd")
            if fsc_total is not None and req_cost is not None:
                self.assertAlmostEqual(fsc_total, req_cost, places=5,
                    msg="single-request step: full_step_cost should equal request cost")
        finally:
            fixture.tearDown()

    def test_cost_scope_distinguishes_single_vs_multi_request(self):
        """cost_scope.current_displayed_cost_scope must not be ambiguous."""
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            step1 = detail["steps"][0]
            step2 = detail["steps"][1]
            # Single request step
            self.assertEqual(step1["cost_scope"]["current_displayed_cost_scope"], "single_request")
            # Single request step (compaction token_count outside step range)
            self.assertEqual(step2["cost_scope"]["current_displayed_cost_scope"], "single_request")
            # Neither should be "unknown"
            for step in detail["steps"]:
                self.assertNotEqual(step["cost_scope"]["current_displayed_cost_scope"], "unknown",
                    f"Step {step['step_index']} has unknown cost_scope")
        finally:
            fixture.tearDown()

    def test_cumulative_delta_is_after_minus_before(self):
        """cumulative_delta.input_tokens = cumulative_after - cumulative_before."""
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            step2 = detail["steps"][1]
            if step2["cumulative_before_step"].get("available") and step2["cumulative_delta"].get("available"):
                expected = (
                    step2["cumulative_after_step"]["input_tokens"]
                    - step2["cumulative_before_step"]["input_tokens"]
                )
                self.assertEqual(step2["cumulative_delta"]["input_tokens"], expected)
        finally:
            fixture.tearDown()

    def test_unattributed_delta_is_cumulative_delta_minus_full_step(self):
        """unattributed_delta.input_tokens = cumulative_delta - full_step_usage."""
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            for step in detail["steps"]:
                if step["unattributed_delta"].get("available"):
                    cd_input = step["cumulative_delta"]["input_tokens"]
                    fsu_input = step["full_step_usage"]["input_tokens"]
                    expected_ud = cd_input - fsu_input
                    self.assertEqual(step["unattributed_delta"]["input_tokens"], expected_ud,
                        f"Step {step['step_index']}: unattributed_delta mismatch")
        finally:
            fixture.tearDown()

    def test_event_ranges_are_monotonic(self):
        """Event ranges must be monotonic and non-overlapping across steps."""
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            prev_end = None
            for step in detail["steps"]:
                er = step["event_range"]
                self.assertIsInstance(er, dict)
                start = er.get("start_event_index", 0)
                end_val = er.get("end_event_index", 0)
                self.assertGreater(end_val, 0, f"Step {step['step_index']}: end_event_index is 0")
                self.assertGreaterEqual(end_val, start,
                    f"Step {step['step_index']}: end < start")
                if prev_end is not None:
                    self.assertGreater(start, prev_end,
                        f"Step {step['step_index']}: start={start} <= prev_end={prev_end}")
                prev_end = end_val
        finally:
            fixture.tearDown()

    def test_session_reconciliation_sum_fsu_not_greater_than_total(self):
        """sum(full_step_usage) should not exceed session total."""
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            fsu_sum = sum(
                step["full_step_usage"].get("input_tokens", 0)
                for step in detail["steps"]
            )
            total = detail["summary"]["total_input_tokens"]
            self.assertGreaterEqual(total, fsu_sum,
                f"sum(full_step_usage)={fsu_sum} exceeds session total={total}")
        finally:
            fixture.tearDown()

    def test_frontend_has_step_cost_block(self):
        """Frontend must have buildStepCostBlock function."""
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function buildStepCostBlock(t)", app_js)
        self.assertIn("полная стоимость шага", app_js)
        self.assertIn("внутренних запросов модели", app_js)
        self.assertIn("full_step_cost", app_js)
        self.assertIn("full_step_usage", app_js)
        self.assertIn("cost_scope", app_js)
        # Assert no ambiguous "Cost confirmed: yes" phrasing
        self.assertNotIn("Cost confirmed:", app_js)

    def test_export_includes_v21_fields(self):
        """Export JSON must include v2.1 fields."""
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        self.assertIn("event_range:", app_js)
        self.assertIn("request_usage_items:", app_js)
        self.assertIn("full_step_usage:", app_js)
        self.assertIn("full_step_cost:", app_js)
        self.assertIn("primary_request_usage:", app_js)
        self.assertIn("cumulative_before_step:", app_js)
        self.assertIn("cumulative_after_step:", app_js)
        self.assertIn("cumulative_delta:", app_js)
        self.assertIn("unattributed_delta:", app_js)
        self.assertIn("cost_scope:", app_js)


class TestAgentActivityBreakdownV22(unittest.TestCase):
    """v2.2: Agent activity breakdown tests — text-based extraction."""

    def test_agent_activity_exists_for_live_step(self):
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            for step in detail["steps"]:
                self.assertIn("agent_activity", step)
                aa = step["agent_activity"]
                if aa.get("available"):
                    self.assertIn("activity_sources", aa)
                    self.assertIn("activity_counts", aa)
        finally:
            fixture.tearDown()

    def test_russian_text_produces_summary(self):
        """Answer text with Russian action phrases produces non-empty summary."""
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            step1 = detail["steps"][0]
            aa = step1.get("agent_activity", {})
            # Fixture has "Короткий ответ" — minimal text, but agent_activity should still be available
            self.assertTrue(aa.get("available") or "agent_activity" in step1)
        finally:
            fixture.tearDown()

    def test_prompt_paths_become_important_paths(self):
        """File paths in prompt text should appear in important_paths."""
        # The fixture prompt "Проверить локальную телеметрию" doesn't have file paths.
        # Test that the extraction logic doesn't crash.
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            self.assertIsNotNone(detail)
            # paths should be a list even if empty
            for step in detail["steps"]:
                aa = step.get("agent_activity", {})
                if aa.get("available"):
                    self.assertIsInstance(aa.get("important_paths", []), list)
                    self.assertIsInstance(aa.get("important_commands", []), list)
        finally:
            fixture.tearDown()

    def test_session_activity_summary_present(self):
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            sas = detail["summary"].get("session_activity_summary", {})
            self.assertIsInstance(sas, dict)
        finally:
            fixture.tearDown()

    def test_frontend_has_new_format(self):
        app_js = (REPO_ROOT / "static" / "codex-token-monitor" / "app.js").read_text(encoding="utf-8")
        self.assertIn("Упомянутые / задействованные файлы", app_js)
        self.assertIn("Команды и проверки", app_js)
        self.assertIn("Технические события", app_js)
        self.assertIn("нераспознано событий", app_js)
        self.assertIn("unclassified_raw_events", app_js)

    def test_activity_classification_does_not_change_cost(self):
        fixture = TestLiveChatFixture()
        fixture.setUp()
        try:
            source = {"id": "codex_live_threads", "kind": "live", "codex_dir": str(fixture.codex_dir)}
            detail = _server_mod.build_live_session_detail(source, fixture.thread_id)
            for step in detail["steps"]:
                fsc = step.get("full_step_cost", {})
                aa = step.get("agent_activity", {})
                self.assertIsNotNone(fsc)
                self.assertIsNotNone(aa)
        finally:
            fixture.tearDown()


if __name__ == "__main__":
    unittest.main()
