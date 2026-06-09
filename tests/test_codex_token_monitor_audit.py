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
    _parse_rollout_for_cumulative, _parse_redacted_int,
    _compute_step_cumulative_accounting, _compute_session_cumulative_accounting,
    _fmt_token_dict,
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
            evidence_note="checked raw rollout events for this thread",
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
            selected_step_indices=[1],  # step_index=1 (not array offset)
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
            selected_step_indices=[1, 2],  # step_index values
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
            evidence_note="checked archive_normalized source against raw OTel",
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
            "evidence_note",
        ]
        for field in required_fields:
            self.assertIn(field, result, f"Missing required field: {field}")

    # ── V2 review fixes ──

    def test_selected_step_by_step_index_not_offset(self):
        """V2 FIX: selected_step_indices=[2] must audit step with step_index==2,
        NOT steps[2]."""
        detail = self._make_forensic_like_detail()
        # step_index=2 is at array position 1
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            selected_step_indices=[2],  # step_index value, not array offset
            upstream_evidence_available=False,
        )
        self.assertEqual(result["audit_scope"], "selected_steps")
        self.assertEqual(result["audited_steps_count"], 1)
        sf = result["step_findings"][0]
        self.assertEqual(sf["step_index"], 2,
            "Must audit step with step_index==2, not steps[2]")

    def test_selected_step_last_not_dropped(self):
        """V2 FIX: selecting the last step_index must not be silently dropped."""
        detail = self._make_forensic_like_detail()
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            selected_step_indices=[2],  # last visible step_index
            upstream_evidence_available=False,
        )
        self.assertEqual(result["audited_steps_count"], 1,
            "Last step_index=2 must be audited, not dropped")
        self.assertEqual(result["total_steps_in_session"], 2)

    def test_selected_step_nonexistent_ignored(self):
        """V2 FIX: nonexistent step_index silently ignored, not crash."""
        detail = self._make_forensic_like_detail()
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            selected_step_indices=[99],  # nonexistent
            upstream_evidence_available=False,
        )
        self.assertEqual(result["audit_scope"], "selected_steps")
        self.assertEqual(result["audited_steps_count"], 0)

    def test_upstream_evidence_without_note_warns(self):
        """V2 FIX: upstream_evidence=True without evidence_note must
        produce a 'fail' finding and downgrade to EVIDENCE_PLAUSIBLE."""
        detail = self._make_forensic_like_detail()
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=True,
            evidence_note="",
        )
        self.assertTrue(
            any(f["id"] == "evidence_basis_unverified_claim" for f in result["findings"]),
            "Must have evidence_basis_unverified_claim when upstream_evidence=True without note"
        )
        # Without evidence_note, evidence_basis must NOT be EVIDENCE_VERIFIED
        self.assertEqual(result["evidence_basis"], EVIDENCE_PLAUSIBLE,
            "Without evidence_note, evidence_basis must be detail_looked_plausible, not verified")

    def test_upstream_evidence_with_note_ok(self):
        """V2 FIX: upstream_evidence=True with evidence_note is accepted."""
        detail = self._make_forensic_like_detail()
        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=True,
            evidence_note="checked raw rollout events against step usage",
        )
        self.assertTrue(
            any(f["id"] == "evidence_basis_note" for f in result["findings"]),
            "Must record evidence_note when provided"
        )

    def test_unknown_basis_treated_as_cumulative(self):
        """V2 FIX: unknown usage_basis in live mode → cumulative (safe default)."""
        detail = self._make_forensic_like_detail()
        detail["summary"]["usage_basis"] = "some_future_basis_name"
        detail["summary"]["step_usage_basis"] = "unknown_variant"

        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=False,
        )
        self.assertEqual(result["cost_confidence"], "estimated_from_cumulative",
            "Unknown basis must default to cumulative")
        self.assertNotEqual(result["step_attribution_confidence"], "high")

    def test_missing_basis_treated_as_cumulative(self):
        """V2 FIX: missing usage_basis in live mode → cumulative (safe default)."""
        detail = self._make_forensic_like_detail()
        detail["summary"].pop("usage_basis", None)
        detail["summary"].pop("step_usage_basis", None)

        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=False,
        )
        self.assertEqual(result["cost_confidence"], "estimated_from_cumulative",
            "Missing basis must default to cumulative")

    def test_per_step_delta_basis_not_cumulative(self):
        """confirmed_per_step_delta should NOT be treated as cumulative."""
        detail = self._make_forensic_like_detail()
        detail["summary"]["usage_basis"] = "confirmed_per_step_delta"
        detail["summary"]["step_usage_basis"] = "confirmed_per_step_delta"
        # Also fix step sources
        for s in detail["steps"]:
            s["usage"]["confirmation_status"] = "confirmed_per_step_delta"
            s["usage"]["source"] = "per_step_normalized"

        result = run_audit(
            detail,
            source_kind="live",
            session_id="019e9d2a-17d7-7210-ba5e-bd42e6ce6e5f",
            upstream_evidence_available=False,
        )
        # Without upstream evidence, still downgraded, but not because of cumulative basis
        self.assertEqual(result["cost_confidence"], "estimated_from_cumulative",
            "Without upstream evidence, cost still estimated_from_cumulative")
        # But basis detection should not flag this as cumulative
        self.assertNotEqual(result["step_attribution_confidence"], "low",
            "per_step_delta basis should not be treated as cumulative fallback")


class TestCumulativeAccounting(unittest.TestCase):
    """Tests for cumulative-after-step and unattributed-delta accounting."""

    def test_parse_redacted_int_none(self):
        self.assertIsNone(_parse_redacted_int(None))
        self.assertIsNone(_parse_redacted_int("[REDACTED]"))
        self.assertIsNone(_parse_redacted_int("N/A"))
        self.assertIsNone(_parse_redacted_int(""))

    def test_parse_redacted_int_valid(self):
        self.assertEqual(_parse_redacted_int(42), 42)
        self.assertEqual(_parse_redacted_int("42"), 42)
        self.assertEqual(_parse_redacted_int("1234.5"), 1234)

    def test_rollout_parse_empty_file(self):
        tmp = Path(tempfile.mkdtemp()) / "empty.jsonl"
        tmp.write_text("", encoding="utf-8")
        result = _parse_rollout_for_cumulative(tmp, "session-1")
        self.assertEqual(len(result["turns"]), 0)
        self.assertIsNone(result["final_cumulative"])

    def test_rollout_parse_token_count_events(self):
        tmp = Path(tempfile.mkdtemp()) / "test.jsonl"
        tmp.write_text(
            json.dumps({"timestamp": "2026-01-01T00:00:00Z", "type": "event_msg",
                        "payload": {"type": "task_started", "turn_id": "turn-1"}}) + "\n" +
            json.dumps({"timestamp": "2026-01-01T00:00:01Z", "type": "event_msg",
                        "payload": {"type": "token_count",
                                    "info": {"total_token_usage": 1000, "last_token_usage": 200}}}) + "\n" +
            json.dumps({"timestamp": "2026-01-01T00:00:02Z", "type": "event_msg",
                        "payload": {"type": "task_complete", "turn_id": "turn-1"}}) + "\n",
            encoding="utf-8",
        )
        result = _parse_rollout_for_cumulative(tmp, "session-1")
        self.assertEqual(len(result["turns"]), 1)
        turn = result["turns"][0]
        self.assertEqual(turn["turn_id"], "turn-1")
        self.assertEqual(len(turn["cumulative_events"]), 1)
        self.assertEqual(turn["cumulative_events"][0]["total_token_usage"], 1000)
        self.assertEqual(turn["cumulative_events"][0]["last_token_usage"], 200)
        self.assertEqual(result["final_cumulative"]["total_token_usage"], 1000)

    def test_step_cumulative_accounting_basic(self):
        steps = [
            {"step_index": 1, "turn_id": "turn-1",
             "environment": {"task_turn_id": "turn-1"},
             "usage": {"input_tokens": 100, "output_tokens": 50, "available": True,
                       "confirmation_status": "confirmed_request_usage"}},
            {"step_index": 2, "turn_id": "turn-2",
             "environment": {"task_turn_id": "turn-2"},
             "usage": {"input_tokens": 200, "output_tokens": 80, "available": True,
                       "confirmation_status": "confirmed_request_usage"}},
        ]
        turns = [
            {"turn_id": "turn-1",
             "cumulative_events": [
                 {"timestamp": "", "total_token_usage": 1000, "last_token_usage": 150,
                  "input_tokens": 800, "output_tokens": 200}
             ]},
            {"turn_id": "turn-2",
             "cumulative_events": [
                 {"timestamp": "", "total_token_usage": 2500, "last_token_usage": 300,
                  "input_tokens": 1800, "output_tokens": 600}
             ]},
        ]
        rows = _compute_step_cumulative_accounting(steps, turns, "live")
        self.assertEqual(len(rows), 2)

        # Step 1: request_usage from step
        self.assertEqual(rows[0]["request_usage"]["input_tokens"], 100)
        self.assertEqual(rows[0]["cumulative_usage_after_step"]["input_tokens"], 800)
        # Step 1 is first — no cumulative_delta
        self.assertEqual(rows[0]["cumulative_delta_since_previous_visible_step"].get("input_tokens"), None)

        # Step 2: cumulative_delta = 1800 - 800 = 1000
        self.assertEqual(rows[1]["cumulative_delta_since_previous_visible_step"]["input_tokens"], 1000)
        # unattributed_delta = 1000 - 200 = 800
        self.assertEqual(rows[1]["unattributed_delta"]["input_tokens"], 800)
        # First step should have cold-start flag
        self.assertTrue(rows[0].get("first_visible_step_not_cold_start"))

    def test_session_cumulative_accounting(self):
        rows = [
            {"step_index": 1,
             "request_usage": {"input_tokens": 100, "output_tokens": 50},
             "cumulative_delta_since_previous_visible_step": {}},
            {"step_index": 2,
             "request_usage": {"input_tokens": 200, "output_tokens": 80},
             "cumulative_delta_since_previous_visible_step": {"input_tokens": 1000, "output_tokens": 400}},
        ]
        final_cum = {"total_token_usage": 5000, "input_tokens": 4000, "output_tokens": 1000}
        sca = _compute_session_cumulative_accounting(rows, final_cum, {})
        self.assertEqual(sca["session_total_usage"]["input_tokens"], 4000)
        self.assertEqual(sca["visible_steps_request_usage_sum"]["input_tokens"], 300)
        self.assertEqual(sca["visible_steps_cumulative_delta_sum"]["input_tokens"], 1000)
        self.assertEqual(sca["unattributed_session_usage"]["input_tokens"], 3700)  # 4000 - 300
        self.assertTrue(sca["includes_hidden_context_possible"])  # 300/4000 = 0.075

    def test_negative_unattributed_warning(self):
        """Negative unattributed_delta should produce warning, not crash."""
        steps = [
            {"step_index": 1, "turn_id": "turn-1",
             "environment": {"task_turn_id": "turn-1"},
             "usage": {"input_tokens": 500, "available": True,
                       "confirmation_status": "confirmed_request_usage"}},
        ]
        turns = [
            {"turn_id": "turn-1",
             "cumulative_events": [
                 {"timestamp": "", "total_token_usage": 1000, "input_tokens": 300,
                  "output_tokens": 100}
             ]},
        ]
        rows = _compute_step_cumulative_accounting(steps, turns, "live")
        # input_tokens: request=500, cumulative=300 → can't compute delta for first step
        # But no crash
        self.assertEqual(len(rows), 1)

    def test_rollout_parse_redacted_values(self):
        """[REDACTED] values should be parsed as None, not crash."""
        tmp = Path(tempfile.mkdtemp()) / "redacted.jsonl"
        tmp.write_text(
            json.dumps({"timestamp": "2026-01-01T00:00:00Z", "type": "event_msg",
                        "payload": {"type": "task_started", "turn_id": "turn-1"}}) + "\n" +
            json.dumps({"timestamp": "2026-01-01T00:00:01Z", "type": "event_msg",
                        "payload": {"type": "token_count",
                                    "info": {"total_token_usage": "[REDACTED]",
                                             "last_token_usage": "[REDACTED]"}}}) + "\n" +
            json.dumps({"timestamp": "2026-01-01T00:00:02Z", "type": "event_msg",
                        "payload": {"type": "task_complete", "turn_id": "turn-1"}}) + "\n",
            encoding="utf-8",
        )
        result = _parse_rollout_for_cumulative(tmp, "session-1")
        turn = result["turns"][0]
        self.assertIsNone(turn["cumulative_events"][0]["total_token_usage"])

    def test_fmt_token_dict(self):
        self.assertEqual(_fmt_token_dict({}), "—")
        self.assertEqual(_fmt_token_dict({"input_tokens": 1000, "output_tokens": 500}),
                         "input_tokens=1,000, output_tokens=500")
        self.assertEqual(_fmt_token_dict({"a": None, "b": 5}), "a=N/A, b=5")

    def test_artifact_includes_cumulative_fields(self):
        result = {
            "audit_status": "warning", "usage_confirmation": "all_confirmed",
            "step_attribution_confidence": "medium", "cost_confidence": "estimated_from_cumulative",
            "fallback_used": False, "findings": [],
            "step_findings": [],
            "cumulative_accounting_rows": [
                {"step_index": 1, "request_usage": {"input_tokens": 100},
                 "cumulative_usage_after_step": {"input_tokens": 800},
                 "cumulative_delta_since_previous_visible_step": {},
                 "unattributed_delta": {}, "warnings": []},
            ],
            "session_cumulative_accounting": {
                "session_total_usage": {"input_tokens": 4000},
                "visible_steps_request_usage_sum": {"input_tokens": 300},
                "visible_steps_cumulative_delta_sum": {},
                "unattributed_session_usage": {"input_tokens": 3700},
                "includes_hidden_context_possible": True,
            },
            "rollout_parse_errors": [],
            "source_kind": "live", "session_id": "test", "source_id": "test",
            "audit_timestamp": "2026-01-01T00:00:00Z",
        }
        tmpdir = Path(tempfile.mkdtemp()) / "audit-cum"
        sp, rp = generate_audit_artifacts(result, tmpdir)
        summary_data = json.loads(sp.read_text(encoding="utf-8"))
        self.assertEqual(summary_data["schema_version"], "codex-token-monitor-audit")
        self.assertIn("cumulative_accounting_rows", summary_data)
        self.assertIn("session_cumulative_accounting", summary_data)
        md_text = rp.read_text(encoding="utf-8")
        self.assertIn("Cumulative Accounting", md_text)
        self.assertIn("unattributed_session_usage", md_text)

    def test_run_audit_accepts_rollout_path(self):
        """run_audit should accept rollout_path kwarg without error."""
        detail = {
            "id": "test-session", "title": "Test",
            "source_kind": "live", "summary": {"turn_count": 1},
            "steps": [],
        }
        # With rollout_path=None (default)
        result = run_audit(detail, source_kind="live", session_id="test-session")
        self.assertEqual(result["cumulative_accounting_rows"], [])
        self.assertIsNone(result["session_cumulative_accounting"])

    def test_export_includes_cumulative_fields(self):
        """Export honesty: cumulative fields must be present in audit result."""
        detail = {
            "id": "test-session", "title": "Test",
            "source_kind": "live",
            "summary": {"turn_count": 1, "usage_basis": "live_total_token_usage_latest",
                        "warnings": [{"id": "test", "message": "test"}]},
            "steps": [{
                "step_index": 1, "model": "test",
                "user_prompt": {"available": False, "text": "", "hidden_by_default": True},
                "assistant_answer": {"available": False, "text": "", "hidden_by_default": True},
                "usage": {"available": False, "confirmation_status": "missing_request_usage",
                          "source": "missing"},
                "environment": {}, "warnings": [],
            }],
        }
        result = run_audit(detail, source_kind="live", session_id="test-session")
        # Even without rollout, result should have cumulative fields (empty)
        self.assertIn("cumulative_accounting_rows", result)
        self.assertIn("session_cumulative_accounting", result)
        self.assertIn("rollout_parse_errors", result)


class TestAuditV21StepFullCostAccounting(unittest.TestCase):
    """v2.1: Audit checks for full_step_usage, full_step_cost, event_range, cost_scope."""

    def _make_detail_with_v21_fields(self):
        """Create a live detail with v2.1 fields populated."""
        return {
            "id": "v21-test-001", "title": "V2.1 test",
            "date": "2026-06-07T10:00:00Z", "model": "deepseek-v4-pro",
            "reasoning": "medium", "workdir": "D:\\test\\repo",
            "source_kind": "live",
            "summary": {
                "turn_count": 2, "session_count": 1,
                "usage_basis": "live_total_token_usage_latest",
                "step_usage_basis": "live_last_token_usage",
                "total_input_tokens": 4000, "total_cached_tokens": 1500,
                "total_non_cached_input_tokens": 2500, "average_cached_ratio": 0.375,
                "total_output_tokens": 200, "total_reasoning_tokens": 50,
                "total_tool_tokens": 0, "estimated_total_cost_usd": 0.05,
                "models": ["deepseek-v4-pro"],
                "warnings": [{"id": "cumulative", "message": "cumulative"}],
                "visible_steps_count": 2,
                "raw_model_requests_count": 3,
                "visible_step_full_usage_sum": {"input_tokens": 3000, "cached_tokens": 1200, "output_tokens": 150},
                "unmapped_or_internal_usage": {"input_tokens": 1000, "output_tokens": 50},
            },
            "steps": [
                {
                    "step_index": 1, "turn_id": "turn-1",
                    "model": "deepseek-v4-pro", "reasoning_effort": "medium",
                    "user_prompt": {"available": True, "text": "hello", "hidden_by_default": True, "kind": "user_message"},
                    "assistant_answer": {"available": True, "text": "hi", "hidden_by_default": True},
                    "usage": {
                        "input_tokens": 1000, "cached_tokens": 500,
                        "non_cached_input_tokens": 500, "cached_ratio": 0.5,
                        "output_tokens": 50, "reasoning_tokens": 20, "tool_tokens": 0,
                        "available": True,
                        "confirmation_status": "confirmed_request_usage",
                        "source": "live_last_token_usage", "note": "",
                        "estimated_total_cost_usd": 0.01,
                    },
                    "request_usage_items": [
                        {"event_index": 5, "timestamp": "", "source": "live_last_token_usage",
                         "input_tokens": 1000, "cached_tokens": 500, "non_cached_input_tokens": 500,
                         "output_tokens": 50, "reasoning_tokens": 20, "tool_tokens": 0,
                         "estimated_cost": {"total_usd": 0.01}},
                    ],
                    "full_step_usage": {
                        "source": "sum_last_token_usage_inside_visible_step",
                        "request_count": 1, "input_tokens": 1000, "cached_tokens": 500,
                        "non_cached_input_tokens": 500, "output_tokens": 50, "reasoning_tokens": 20,
                        "tool_tokens": 0,
                    },
                    "full_step_cost": {
                        "source": "estimated_from_full_step_usage",
                        "total_usd": 0.01, "input_usd": 0.005, "cached_input_usd": 0.001, "output_usd": 0.004,
                        "confidence": "estimated_from_local_pricing_config",
                    },
                    "primary_request_usage": {
                        "source": "live_last_token_usage",
                        "input_tokens": 1000, "cached_tokens": 500, "output_tokens": 50,
                        "reasoning_tokens": 20, "tool_tokens": 0,
                    },
                    "cumulative_before_step": {"available": False},
                    "cumulative_after_step": {
                        "available": True, "input_tokens": 1500, "cached_tokens": 800,
                        "output_tokens": 100,
                    },
                    "cumulative_delta": {
                        "available": False,
                    },
                    "unattributed_delta": {"available": False},
                    "cost_scope": {
                        "current_displayed_cost_scope": "single_request",
                        "full_step_cost_available": True,
                        "request_cost_available": True,
                        "mapping_confidence": "high",
                    },
                    "event_range": {"start_event_index": 3, "end_event_index": 10, "raw_events_count": 8},
                    "environment": {"thread_id": "v21-test-001"},
                    "warnings": [], "post_step_badges": [],
                },
                {
                    "step_index": 2, "turn_id": "turn-2",
                    "model": "deepseek-v4-pro", "reasoning_effort": "medium",
                    "user_prompt": {"available": True, "text": "more", "hidden_by_default": True, "kind": "user_message"},
                    "assistant_answer": {"available": True, "text": "ok", "hidden_by_default": True},
                    "usage": {
                        "input_tokens": 1500, "cached_tokens": 500,
                        "non_cached_input_tokens": 1000, "cached_ratio": 0.333,
                        "output_tokens": 60, "reasoning_tokens": 30, "tool_tokens": 0,
                        "available": True,
                        "confirmation_status": "confirmed_request_usage",
                        "source": "live_last_token_usage", "note": "",
                        "estimated_total_cost_usd": 0.015,
                    },
                    "request_usage_items": [
                        {"event_index": 12, "timestamp": "", "source": "live_last_token_usage",
                         "input_tokens": 800, "cached_tokens": 300, "non_cached_input_tokens": 500,
                         "output_tokens": 30, "reasoning_tokens": 15, "tool_tokens": 0,
                         "estimated_cost": {"total_usd": 0.008}},
                        {"event_index": 14, "timestamp": "", "source": "live_last_token_usage",
                         "input_tokens": 700, "cached_tokens": 200, "non_cached_input_tokens": 500,
                         "output_tokens": 30, "reasoning_tokens": 15, "tool_tokens": 0,
                         "estimated_cost": {"total_usd": 0.007}},
                    ],
                    "full_step_usage": {
                        "source": "sum_last_token_usage_inside_visible_step",
                        "request_count": 2, "input_tokens": 1500, "cached_tokens": 500,
                        "non_cached_input_tokens": 1000, "output_tokens": 60, "reasoning_tokens": 30,
                        "tool_tokens": 0,
                    },
                    "full_step_cost": {
                        "source": "estimated_from_full_step_usage",
                        "total_usd": 0.015, "input_usd": 0.008, "cached_input_usd": 0.002, "output_usd": 0.005,
                        "confidence": "estimated_from_local_pricing_config",
                    },
                    "primary_request_usage": {
                        "source": "live_last_token_usage",
                        "input_tokens": 700, "cached_tokens": 200, "output_tokens": 30,
                        "reasoning_tokens": 15, "tool_tokens": 0,
                    },
                    "cumulative_before_step": {
                        "available": True, "input_tokens": 1500, "cached_tokens": 800,
                        "output_tokens": 100,
                    },
                    "cumulative_after_step": {
                        "available": True, "input_tokens": 4000, "cached_tokens": 1500,
                        "output_tokens": 200,
                    },
                    "cumulative_delta": {
                        "available": True, "input_tokens": 2500, "cached_tokens": 700,
                        "output_tokens": 100,
                    },
                    "unattributed_delta": {
                        "available": True, "input_tokens": 1000, "cached_tokens": 200,
                        "output_tokens": 40,
                        "interpretation": "cumulative growth not explained by summed request usage inside visible step",
                    },
                    "cost_scope": {
                        "current_displayed_cost_scope": "full_visible_step",
                        "full_step_cost_available": True,
                        "request_cost_available": True,
                        "mapping_confidence": "high",
                    },
                    "event_range": {"start_event_index": 11, "end_event_index": 18, "raw_events_count": 8},
                    "environment": {"thread_id": "v21-test-001"},
                    "warnings": [], "post_step_badges": [],
                },
            ],
            "timeline_events": [],
        }

    def test_event_range_present(self):
        """Audit must confirm event_range exists for each step."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "step_1_event_range_ok" for f in result["findings"]))
        self.assertTrue(any(f["id"] == "step_2_event_range_ok" for f in result["findings"]))

    def test_event_ranges_monotonic(self):
        """Audit must check that event ranges are monotonic."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "event_range_monotonic_ok" for f in result["findings"]))

    def test_full_step_usage_matches_sum_of_request_items(self):
        """Audit verifies full_step_usage equals sum of request_usage_items."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "step_1_full_usage_match" for f in result["findings"]))
        self.assertTrue(any(f["id"] == "step_2_full_usage_match" for f in result["findings"]))

    def test_full_step_cost_source_correct(self):
        """Audit verifies full_step_cost.source is 'estimated_from_full_step_usage'."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "step_1_full_cost_source_ok" for f in result["findings"]))
        self.assertTrue(any(f["id"] == "step_2_full_cost_source_ok" for f in result["findings"]))

    def test_cost_scope_not_ambiguous(self):
        """Audit verifies cost_scope labels are clear (single_request/full_visible_step)."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "step_1_cost_scope_clear" for f in result["findings"]))
        self.assertTrue(any(f["id"] == "step_2_cost_scope_clear" for f in result["findings"]))

    def test_cumulative_monotonic_check(self):
        """Audit verifies cumulative input is monotonic (after >= before)."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "step_2_cumulative_monotonic" for f in result["findings"]))

    def test_unattributed_delta_consistency(self):
        """Audit verifies unattributed_delta = cumulative_delta - full_step_usage."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "step_2_unattributed_match" for f in result["findings"]))

    def test_single_request_matches_full_step(self):
        """Audit confirms single-request step: request cost equals full step cost."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "step_1_single_request_matches" for f in result["findings"]))

    def test_fsu_sum_reconciliation(self):
        """Audit checks sum(full_step_usage) + unmapped ≈ session total."""
        detail = self._make_detail_with_v21_fields()
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        self.assertTrue(any(f["id"] == "fsu_sum_reconciliation_ok" for f in result["findings"]))

    def test_missing_full_step_usage_is_warning(self):
        """Steps without full_step_usage should produce a warning, not crash."""
        detail = self._make_detail_with_v21_fields()
        # Remove full_step_usage from step 1
        detail["steps"][0].pop("full_step_usage", None)
        detail["steps"][0].pop("request_usage_items", None)
        detail["steps"][0].pop("full_step_cost", None)
        detail["steps"][0].pop("event_range", None)
        detail["steps"][0].pop("cost_scope", None)
        result = run_audit(detail, source_kind="live", session_id="v21-test-001")
        # Should not crash, should produce warning about missing event_range
        self.assertIsNotNone(result)
        findings_ids = [f["id"] for f in result.get("findings", [])]
        self.assertIn("step_1_event_range_missing", findings_ids)
        self.assertIn("step_1_request_items_empty", findings_ids)

    def test_no_ambiguous_cost_confirmed_in_audit(self):
        """Audit module code must not use ambiguous 'Cost confirmed' wording."""
        audit_code = (REPO_ROOT / "scripts" / "codex_token_monitor_audit.py").read_text(encoding="utf-8")
        self.assertNotIn("Cost confirmed", audit_code)


if __name__ == "__main__":
    unittest.main()
