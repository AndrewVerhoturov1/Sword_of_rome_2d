"""Tests for Codex Token Monitor Audit module."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from codex_token_monitor_audit import (
    run_audit, generate_audit_artifacts,
    EVIDENCE_VERIFIED, EVIDENCE_PLAUSIBLE, EVIDENCE_NOT_VERIFIED,
)


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
                    "available": True,
                    "confirmation_status": "confirmed_request_usage",
                    "source": "archive_normalized",
                    "estimated_total_cost_usd": 0.025,
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


class TestTruthRegression(unittest.TestCase):
    """Regression tests for audit truth model — prevent self-certification.

    These tests are the MOST IMPORTANT part of the audit truth fix.
    They must FAIL if audit ever again self-certifies monitor detail
    without sufficient upstream evidence.
    """

    def _make_forensic_like_detail(self):
        """Build a detail that mimics the forensic live thread 019e9d2a.

        Key properties:
        - All steps have confirmed_request_usage
        - Summary basis is cumulative (live_total_token_usage_latest)
        - Summary has warnings about cumulative nature
        - This is EXACTLY the case where old audit returned ok/high/per_step_estimated
        """
        return {
            "id": "019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            "title": "Скажи тест",
            "date": "2026-06-06T13:41:02Z",
            "model": "gpt-5.4-mini",
            "reasoning": "low",
            "workdir": "D:\\test",
            "source_kind": "live",
            "summary": {
                "turn_count": 2,
                "session_count": 1,
                "usage_basis": "live_total_token_usage_latest",
                "step_usage_basis": "live_last_token_usage",
                "total_input_tokens": 50000,
                "total_cached_tokens": 37000,
                "total_non_cached_input_tokens": 13000,
                "average_cached_ratio": 0.74,
                "total_output_tokens": 500,
                "total_reasoning_tokens": 0,
                "total_tool_tokens": 0,
                "estimated_total_cost_usd": 0.026,
                "models": ["gpt-5.4-mini"],
                "warnings": [
                    {"id": "live_totals_are_cumulative", "message": "cumulative"},
                    {"id": "live_steps_use_request_usage", "message": "request-level"},
                ],
            },
            "steps": [
                {
                    "step_index": 1,
                    "turn_id": "turn-1",
                    "model": "gpt-5.4-mini",
                    "user_prompt": {"available": True, "text": "Скажи тест", "hidden_by_default": True, "kind": "user_message"},
                    "assistant_answer": {"available": True, "text": "тест", "hidden_by_default": True},
                    "usage": {
                        "input_tokens": 30000,
                        "cached_tokens": 27000,
                        "non_cached_input_tokens": 3000,
                        "cached_ratio": 0.9,
                        "output_tokens": 300,
                        "reasoning_tokens": 0,
                        "tool_tokens": 0,
                        "available": True,
                        "confirmation_status": "confirmed_request_usage",
                        "source": "live_last_token_usage",
                        "note": "",
                        "estimated_total_cost_usd": 0.0037,
                    },
                    "environment": {"thread_id": "019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f"},
                    "warnings": [],
                    "post_step_badges": [],
                },
                {
                    "step_index": 2,
                    "turn_id": "turn-2",
                    "model": "gpt-5.4-mini",
                    "user_prompt": {"available": True, "text": "Скажи тест 2", "hidden_by_default": True, "kind": "user_message"},
                    "assistant_answer": {"available": True, "text": "тест2", "hidden_by_default": True},
                    "usage": {
                        "input_tokens": 20000,
                        "cached_tokens": 10000,
                        "non_cached_input_tokens": 10000,
                        "cached_ratio": 0.5,
                        "output_tokens": 200,
                        "reasoning_tokens": 0,
                        "tool_tokens": 0,
                        "available": True,
                        "confirmation_status": "confirmed_request_usage",
                        "source": "live_last_token_usage",
                        "note": "",
                        "estimated_total_cost_usd": 0.002,
                    },
                    "environment": {"thread_id": "019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f"},
                    "warnings": [],
                    "post_step_badges": [],
                },
            ],
            "timeline_events": [],
        }

    def test_self_certification_blocked_no_upstream_evidence(self):
        """TRUTH REGRESSION: forensic-like detail without upstream evidence
        must NOT return ok + high + per_step_estimated."""
        detail = self._make_forensic_like_detail()
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=False,
        )

        # Must NOT be ok — without upstream evidence, cumulative basis → warning
        self.assertNotEqual(result["audit_status"], "ok",
            "BUG: audit returned 'ok' on forensic-like detail without upstream evidence")

        # Must NOT be high — cumulative summary basis blocks high confidence
        self.assertNotEqual(result["step_attribution_confidence"], "high",
            "BUG: step_attribution_confidence='high' on cumulative live summary without upstream evidence")

        # Must NOT be per_step_estimated — cumulative basis always → estimated_from_cumulative
        self.assertNotEqual(result["cost_confidence"], "per_step_estimated",
            "BUG: cost_confidence='per_step_estimated' on cumulative live summary")

        # Evidence must be downgraded
        self.assertEqual(result["evidence_basis"], EVIDENCE_PLAUSIBLE,
            "Expected detail_looked_plausible when no upstream evidence but detail has warnings")

        # Note: fallback_used may be False here because live_last_token_usage
        # is a per-step request-level source (not a cumulative fallback).
        # The truth protection comes from summary basis check, not step fallback.
        # This is correct: steps look individually confirmed, but the summary
        # basis is cumulative → confidence is downgraded.

    def test_cumulative_summary_blocks_per_step_cost(self):
        """TRUTH REGRESSION: even if all steps confirmed, cumulative summary
        basis must block per_step_estimated cost confidence."""
        detail = self._make_forensic_like_detail()
        # All steps confirmed
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=False,
        )

        self.assertEqual(result["usage_confirmation"], "all_confirmed",
            "All steps should be confirmed")
        self.assertEqual(result["cost_confidence"], "estimated_from_cumulative",
            "Cumulative basis must force estimated_from_cumulative even with all_confirmed")

    def test_upstream_evidence_allows_stronger_statuses(self):
        """With upstream evidence, statuses can be stronger (but still
        limited by cumulative basis)."""
        detail = self._make_forensic_like_detail()
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=True,
        )

        # Evidence basis must be verified
        self.assertEqual(result["evidence_basis"], EVIDENCE_VERIFIED)

        # Step confidence still medium (cumulative basis limits even with evidence)
        self.assertEqual(result["step_attribution_confidence"], "medium")

        # Cost still estimated_from_cumulative (cumulative basis is absolute limit)
        self.assertEqual(result["cost_confidence"], "estimated_from_cumulative")

    def test_selected_step_scope_exposed(self):
        """TRUTH REGRESSION: selected-step audit must expose narrowed scope
        and not present as full session."""
        detail = self._make_forensic_like_detail()
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            selected_step_indices=[0],
            upstream_evidence_available=False,
        )

        # Scope must be selected_steps, not full_session
        self.assertEqual(result["audit_scope"], "selected_steps")
        self.assertEqual(result["total_steps_in_session"], 2)
        self.assertEqual(result["audited_steps_count"], 1)

        # Usage confirmation should reflect only audited steps
        self.assertEqual(result["usage_confirmation"], "all_confirmed",
            "Single selected step is confirmed → all_confirmed for that scope")

        # But confidence still downgraded (cumulative basis, no upstream)
        self.assertNotEqual(result["step_attribution_confidence"], "high")

    def test_selected_step_scope_partial_confirmation(self):
        """Selected steps with partial confirmation."""
        detail = self._make_forensic_like_detail()
        # Make step 1 unconfirmed
        detail["steps"][0]["usage"]["confirmation_status"] = "missing_request_usage"
        detail["steps"][0]["usage"]["available"] = False

        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            selected_step_indices=[0, 1],
            upstream_evidence_available=False,
        )

        self.assertEqual(result["audit_scope"], "selected_steps")
        self.assertEqual(result["usage_confirmation"], "partial")

    def test_archive_with_upstream_evidence_can_be_high(self):
        """Archive with upstream evidence and all steps confirmed can reach
        high step confidence (no cumulative basis limitation)."""
        detail = {
            "id": "run-20260605-test001",
            "title": "Test run",
            "date": "2026-06-05T10:00:00Z",
            "model": "qwen3-coder",
            "reasoning": "low",
            "workdir": "D:\\test",
            "source_kind": "archive",
            "summary": {
                "turn_count": 1,
                "total_input_tokens": 15000,
                "total_output_tokens": 1500,
                "estimated_total_cost_usd": 0.025,
                "models": ["qwen3-coder"],
                "warnings": [],
            },
            "steps": [{
                "step_index": 1,
                "model": "qwen3-coder",
                "user_prompt": {"available": False, "text": "", "hidden_by_default": True},
                "assistant_answer": {"available": False, "text": "", "hidden_by_default": True},
                "usage": {
                    "input_tokens": 15000,
                    "output_tokens": 1500,
                    "available": True,
                    "confirmation_status": "confirmed_request_usage",
                    "source": "archive_normalized",
                    "estimated_total_cost_usd": 0.025,
                },
                "environment": {"thread_id": "run-001"},
                "warnings": [],
            }],
        }

        result = run_audit(
            detail,
            source_kind="archive",
            session_id="run-20260605-test001",
            upstream_evidence_available=True,
        )

        self.assertEqual(result["evidence_basis"], EVIDENCE_VERIFIED)
        self.assertEqual(result["step_attribution_confidence"], "high")
        self.assertEqual(result["cost_confidence"], "per_step_estimated")

    def test_archive_without_upstream_evidence_downgraded(self):
        """Archive without upstream evidence: step confidence medium,
        cost estimated_from_cumulative."""
        detail = {
            "id": "run-20260605-test002",
            "title": "Test run",
            "date": "2026-06-05T10:00:00Z",
            "model": "qwen3-coder",
            "reasoning": "low",
            "workdir": "D:\\test",
            "source_kind": "archive",
            "summary": {
                "turn_count": 1,
                "total_input_tokens": 15000,
                "total_output_tokens": 1500,
                "estimated_total_cost_usd": 0.025,
                "models": ["qwen3-coder"],
                "warnings": [],
            },
            "steps": [{
                "step_index": 1,
                "model": "qwen3-coder",
                "user_prompt": {"available": False, "text": "", "hidden_by_default": True},
                "assistant_answer": {"available": False, "text": "", "hidden_by_default": True},
                "usage": {
                    "input_tokens": 15000,
                    "output_tokens": 1500,
                    "available": True,
                    "confirmation_status": "confirmed_request_usage",
                    "source": "archive_normalized",
                    "estimated_total_cost_usd": 0.025,
                },
                "environment": {"thread_id": "run-001"},
                "warnings": [],
            }],
        }

        result = run_audit(
            detail,
            source_kind="archive",
            session_id="run-20260605-test002",
            upstream_evidence_available=False,
        )

        self.assertEqual(result["evidence_basis"], EVIDENCE_PLAUSIBLE)
        self.assertEqual(result["step_attribution_confidence"], "medium")
        self.assertEqual(result["cost_confidence"], "estimated_from_cumulative")

    def test_evidence_basis_not_verified_when_no_warnings(self):
        """Live detail with no warnings and no upstream evidence → not_verified."""
        detail = self._make_forensic_like_detail()
        # Remove warnings and make basis non-cumulative looking
        detail["summary"]["warnings"] = []
        detail["summary"]["usage_basis"] = "per_step"

        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=False,
        )

        self.assertEqual(result["evidence_basis"], EVIDENCE_NOT_VERIFIED)
        self.assertEqual(result["audit_status"], "warning")

    def test_result_includes_new_truth_fields(self):
        """All new truth fields must be present in result."""
        detail = self._make_forensic_like_detail()
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            selected_step_indices=[0],
            upstream_evidence_available=False,
        )

        required_fields = [
            "audit_scope", "evidence_basis", "upstream_evidence_available",
            "selected_step_indices", "total_steps_in_session", "audited_steps_count",
        ]
        for field in required_fields:
            self.assertIn(field, result, f"Missing required field: {field}")


if __name__ == "__main__":
    unittest.main()
