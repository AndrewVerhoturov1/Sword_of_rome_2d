"""Tests for Codex Token Monitor Audit module."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from codex_token_monitor_audit import run_audit, generate_audit_artifacts


class TestRunAudit(unittest.TestCase):
    """Test run_audit with various session detail inputs."""

    def _make_live_detail(self, **overrides):
        base = {
            "id": "thread-abc-123", "title": "Test chat",
            "date": "2026-06-06T15:00:00Z", "model": "deepseek-v4-pro",
            "reasoning": "medium", "workdir": "D:\\test\\repo",
            "source_kind": "live",
            "summary": {
                "turn_count": 3, "session_count": 1,
                "usage_basis": "live_total_token_usage_latest",
                "step_usage_basis": "live_last_token_usage",
                "total_input_tokens": 50000, "total_cached_tokens": 30000,
                "total_non_cached_input_tokens": 20000, "average_cached_ratio": 0.6,
                "total_output_tokens": 5000, "total_reasoning_tokens": 2000,
                "total_tool_tokens": 0, "estimated_total_cost_usd": 0.15,
                "models": ["deepseek-v4-pro"],
                "warnings": [{"id": "cumulative", "message": "cumulative"}],
            },
            "steps": [
                {
                    "step_index": 1, "turn_id": "turn-1",
                    "model": "deepseek-v4-pro", "reasoning_effort": "medium",
                    "user_prompt": {"available": True, "text": "hello", "hidden_by_default": True, "kind": "user_message"},
                    "assistant_answer": {"available": True, "text": "hi", "hidden_by_default": True},
                    "usage": {
                        "input_tokens": 12000, "cached_tokens": 10000,
                        "non_cached_input_tokens": 2000, "cached_ratio": 0.833,
                        "output_tokens": 500, "reasoning_tokens": 200, "tool_tokens": 0,
                        "available": True,
                        "confirmation_status": "confirmed_request_usage",
                        "source": "live_last_token_usage", "note": "",
                        "estimated_total_cost_usd": 0.02,
                    },
                    "environment": {"thread_id": "thread-abc-123"},
                    "warnings": [], "post_step_badges": [],
                },
                {
                    "step_index": 2, "turn_id": "turn-2",
                    "model": "deepseek-v4-pro", "reasoning_effort": "medium",
                    "user_prompt": {"available": True, "text": "go", "hidden_by_default": True, "kind": "user_message"},
                    "assistant_answer": {"available": False, "text": "", "hidden_by_default": True},
                    "usage": {
                        "input_tokens": 0, "cached_tokens": 0, "non_cached_input_tokens": 0,
                        "cached_ratio": 0, "output_tokens": 0, "reasoning_tokens": 0, "tool_tokens": 0,
                        "available": False,
                        "confirmation_status": "missing_request_usage",
                        "source": "missing", "note": "no confirmed usage",
                    },
                    "environment": {"thread_id": "thread-abc-123"},
                    "warnings": [], "post_step_badges": [],
                },
            ],
            "timeline_events": [],
        }
        base.update(overrides)
        return base

    def _make_archive_detail(self, **overrides):
        base = {
            "id": "run-20260605-test001", "title": "run-20260605-test001",
            "date": "2026-06-05T10:00:00Z", "model": "qwen3-coder",
            "reasoning": "low", "workdir": "D:\\test\\repo",
            "source_kind": "archive",
            "summary": {
                "turn_count": 2, "session_count": 1,
                "total_input_tokens": 30000, "total_cached_tokens": 5000,
                "total_non_cached_input_tokens": 25000, "average_cached_ratio": 0.167,
                "total_output_tokens": 3000, "estimated_total_cost_usd": 0.05,
                "models": ["qwen3-coder"], "warnings": [],
            },
            "steps": [{
                "step_index": 1, "model": "qwen3-coder", "reasoning_effort": "low",
                "user_prompt": {"available": False, "text": "", "hidden_by_default": True},
                "assistant_answer": {"available": False, "text": "", "hidden_by_default": True},
                "usage": {
                    "input_tokens": 15000, "cached_tokens": 0,
                    "non_cached_input_tokens": 15000, "cached_ratio": 0.0,
                    "output_tokens": 1500, "reasoning_tokens": 0, "tool_tokens": 0,
                    "available": True, "estimated_total_cost_usd": 0.025,
                },
                "environment": {"thread_id": "run-001"}, "warnings": [],
            }],
        }
        base.update(overrides)
        return base

    def test_live_source_identity_ok(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertEqual(result["source_kind"], "live")
        self.assertTrue(any(f["id"] == "source_kind_ok" for f in result["findings"]))

    def test_source_kind_invalid(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="cloud", session_id="thread-abc-123")
        self.assertEqual(result["audit_status"], "fail")

    def test_source_kind_mismatch(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="archive", session_id="thread-abc-123")
        self.assertEqual(result["audit_status"], "fail")

    def test_session_id_ok(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertTrue(any(f["id"] == "session_id_ok" for f in result["findings"]))

    def test_session_id_missing(self):
        detail = self._make_live_detail()
        detail.pop("id", None)
        result = run_audit(detail, source_kind="live", session_id="")
        self.assertTrue(any(f["id"] == "session_id_missing" for f in result["findings"]))

    def test_session_id_mismatch(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="wrong-id")
        self.assertTrue(any(f["id"] == "session_id_mismatch" for f in result["findings"]))

    def test_step_usage_confirmed(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        sf1 = next((s for s in result.get("step_findings", []) if s["step_index"] == 1), None)
        self.assertIsNotNone(sf1)
        self.assertTrue(sf1["usage_available"])

    def test_step_usage_missing(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        sf2 = next((s for s in result.get("step_findings", []) if s["step_index"] == 2), None)
        self.assertIsNotNone(sf2)
        self.assertFalse(sf2["usage_available"])

    def test_usage_confirmation_partial(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertEqual(result["usage_confirmation"], "partial")

    def test_usage_confirmation_all_confirmed(self):
        detail = self._make_live_detail()
        detail["steps"][1]["usage"]["available"] = True
        detail["steps"][1]["usage"]["confirmation_status"] = "confirmed_request_usage"
        detail["steps"][1]["usage"]["source"] = "live_last_token_usage"
        detail["steps"][1]["usage"]["input_tokens"] = 5000
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertEqual(result["usage_confirmation"], "all_confirmed")

    def test_fallback_detected(self):
        detail = self._make_live_detail()
        detail["steps"][0]["usage"]["source"] = "total_token_usage"
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertTrue(result["fallback_used"])

    def test_step_confidence_low_with_fallback(self):
        detail = self._make_live_detail()
        detail["steps"][0]["usage"]["source"] = "total_token_usage"
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertEqual(result["step_attribution_confidence"], "low")

    def test_archive_audit_all_confirmed(self):
        detail = self._make_archive_detail()
        result = run_audit(detail, source_kind="archive", session_id="run-20260605-test001")
        self.assertIn(result["audit_status"], ("ok", "warning"))
        self.assertEqual(result["usage_confirmation"], "all_confirmed")

    def test_live_summary_basis_acknowledged(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertTrue(any(f["id"] == "summary_cumulative_acknowledged" for f in result["findings"]))

    def test_visible_step_sum_smaller_than_total(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertTrue(any(f["id"] == "summary_visible_step_mismatch" for f in result["findings"]))

    def test_cost_confidence_live_partial(self):
        detail = self._make_live_detail()
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertEqual(result["cost_confidence"], "estimated_from_cumulative")

    def test_empty_steps(self):
        detail = self._make_live_detail()
        detail["steps"] = []
        detail["summary"]["turn_count"] = 0
        detail["summary"]["total_input_tokens"] = 0
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertEqual(result["usage_confirmation"], "not_applicable")

    def test_no_summary(self):
        detail = self._make_live_detail()
        detail.pop("summary", None)
        result = run_audit(detail, source_kind="live", session_id="thread-abc-123")
        self.assertTrue(any(f["id"] == "summary_missing" for f in result["findings"]))


class TestGenerateArtifacts(unittest.TestCase):
    """Test artifact generation."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_result(self):
        return {
            "audit_status": "ok", "usage_confirmation": "all_confirmed",
            "step_attribution_confidence": "high", "cost_confidence": "per_step_estimated",
            "fallback_used": False,
            "findings": [{"id": "source_kind_ok", "level": "ok", "message": "ok"}],
            "step_findings": [{
                "step_index": 1, "usage_available": True,
                "usage_confirmation_status": "confirmed_request_usage",
                "usage_source": "live_last_token_usage",
                "findings": [{"id": "step_usage_confirmed", "level": "ok", "message": "ok"}],
            }],
            "source_kind": "live", "session_id": "test-123",
            "source_id": "test-source", "audit_timestamp": "2026-06-06T15:00:00Z",
        }

    def test_generates_json_and_md(self):
        result = self._make_result()
        output_dir = Path(self.tmpdir) / "audit-output"
        summary_path, report_path = generate_audit_artifacts(result, output_dir)
        self.assertTrue(summary_path.exists())
        self.assertTrue(report_path.exists())
        self.assertEqual(summary_path.name, "monitor_audit_summary.json")
        self.assertEqual(report_path.name, "monitor_audit_report.md")
        summary_data = json.loads(summary_path.read_text(encoding="utf-8"))
        self.assertEqual(summary_data["audit_status"], "ok")
        md_text = report_path.read_text(encoding="utf-8")
        self.assertIn("# Codex Token Monitor Audit Report", md_text)
        self.assertIn("## Audit Findings", md_text)
        self.assertIn("## \u0418\u043d\u0442\u0435\u0440\u043f\u0440\u0435\u0442\u0430\u0446\u0438\u044f \u0441\u0442\u0430\u0442\u0443\u0441\u043e\u0432", md_text)

    def test_empty_findings(self):
        result = self._make_result()
        result["findings"] = []
        result["step_findings"] = []
        output_dir = Path(self.tmpdir) / "audit-empty"
        _, rp = generate_audit_artifacts(result, output_dir)
        md_text = rp.read_text(encoding="utf-8")
        self.assertIn("\u041d\u0435\u0442 \u0437\u0430\u043c\u0435\u0447\u0430\u043d\u0438\u0439", md_text)


if __name__ == "__main__":
    unittest.main()
