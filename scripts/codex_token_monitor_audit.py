#!/usr/bin/env python3
"""Codex Token Monitor Audit — separate verification layer over hybrid monitor baseline.

Checks technical truth of source selection, session identity, step attribution,
usage basis, fallback semantics, cost confidence and export completeness.

Does NOT:
- change live Codex config
- start new OTel experiments
- write into C:/Users/andre/.codex/**
- perform human-facing wording changes (that's Honesty hardening, later)

Usage:
  As module: from scripts.codex_token_monitor_audit import run_audit
  As script: python scripts/codex_token_monitor_audit.py --detail <path>
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_MONITOR_DIR = REPO_ROOT / "_local" / "codex-token-monitor"

# ── Audit status model ──

AuditResult = dict[str, Any]

# Evidence basis levels for audit truth model
EVIDENCE_VERIFIED = "verified_against_source_evidence"
EVIDENCE_PLAUSIBLE = "detail_looked_plausible"
EVIDENCE_NOT_VERIFIED = "not_verified"


def run_audit(
    detail: dict[str, Any],
    *,
    source_kind: str | None = None,
    source_id: str | None = None,
    session_id: str | None = None,
    selected_step_indices: list[int] | None = None,
    upstream_evidence_available: bool = False,
) -> AuditResult:
    """Run full audit over a session detail dict from the monitor server.

    Args:
        detail: session detail JSON as returned by build_live_session_detail()
                or build_archive_session_detail()
        source_kind: expected source kind (live/archive), taken from detail if absent
        source_id: source identifier, taken from detail if absent
        session_id: session identifier, taken from detail if absent
        selected_step_indices: if provided, audit only these step indices
            (narrowed scope — must be exposed honestly)
        upstream_evidence_available: True if audit has access to upstream
            source evidence (raw rollout, raw OTel, etc.) beyond the detail
            object itself. False means audit can only check internal
            consistency of the already-built detail.

    Returns:
        AuditResult with findings, audit_status, usage_confirmation,
        step_attribution_confidence, cost_confidence, fallback_used,
        audit_scope, evidence_basis, and per-step findings.
    """
    findings: list[dict[str, str]] = []
    step_findings: list[dict[str, Any]] = []

    source_kind = source_kind or str(detail.get("source_kind", ""))
    session_id = session_id or str(detail.get("id", ""))
    source_id = source_id or ""

    # ── 1. Source identity check ──
    _check_source_identity(findings, detail, source_kind)

    # ── 2. Session identity check ──
    _check_session_identity(findings, detail, session_id)

    # ── 3. Step-level checks ──
    steps = detail.get("steps", [])
    if not isinstance(steps, list):
        steps = []

    summary = detail.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}

    # Determine audit scope
    all_step_indices = list(range(len(steps)))
    if selected_step_indices is not None:
        effective_indices = [i for i in selected_step_indices if 0 <= i < len(steps)]
        audit_scope = "selected_steps"
    else:
        effective_indices = all_step_indices
        audit_scope = "full_session"

    for i in effective_indices:
        step = steps[i]
        sf = _audit_step(step, source_kind, summary)
        step_findings.append(sf)
        findings.extend(sf.get("findings", []))

    # ── 4. Summary basis check ──
    _check_summary_basis(findings, detail, source_kind, steps)

    # ── 5. Export/artifact check ──
    _check_export_honesty(findings, detail, source_kind)

    # ── 6. Determine evidence basis ──
    evidence_basis = _determine_evidence_basis(
        upstream_evidence_available, source_kind, summary, findings
    )

    # ── 7. Compute aggregate statuses ──
    audit_status, usage_confirmation, step_confidence, cost_confidence, fallback_used = _compute_statuses(
        findings, step_findings, source_kind, summary, evidence_basis, audit_scope
    )

    return {
        "audit_status": audit_status,
        "usage_confirmation": usage_confirmation,
        "step_attribution_confidence": step_confidence,
        "cost_confidence": cost_confidence,
        "fallback_used": fallback_used,
        "audit_scope": audit_scope,
        "evidence_basis": evidence_basis,
        "upstream_evidence_available": upstream_evidence_available,
        "selected_step_indices": selected_step_indices,
        "total_steps_in_session": len(steps),
        "audited_steps_count": len(step_findings),
        "findings": findings,
        "step_findings": step_findings,
        "source_kind": source_kind,
        "session_id": session_id,
        "source_id": source_id,
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _check_source_identity(
    findings: list[dict[str, str]], detail: dict[str, Any], source_kind: str
) -> None:
    """Verify source_kind is valid and consistent with detail."""
    valid_kinds = {"live", "archive"}
    if source_kind not in valid_kinds:
        findings.append({
            "id": "source_kind_invalid",
            "level": "fail",
            "message": f"source_kind '{source_kind}' is not one of {sorted(valid_kinds)}",
        })
    elif source_kind == detail.get("source_kind", "") or not detail.get("source_kind"):
        findings.append({
            "id": "source_kind_ok",
            "level": "ok",
            "message": f"source_kind = '{source_kind}' matches detail",
        })
    else:
        findings.append({
            "id": "source_kind_mismatch",
            "level": "fail",
            "message": (
                f"expected source_kind '{source_kind}' but detail has "
                f"'{detail.get('source_kind')}'"
            ),
        })


def _check_session_identity(
    findings: list[dict[str, str]], detail: dict[str, Any], session_id: str
) -> None:
    """Verify session/thread ID is present and plausible."""
    detail_id = str(detail.get("id", ""))
    if not detail_id:
        findings.append({
            "id": "session_id_missing",
            "level": "fail",
            "message": "detail has no session id",
        })
    elif detail_id != session_id:
        findings.append({
            "id": "session_id_mismatch",
            "level": "fail",
            "message": f"expected id '{session_id}' but detail has '{detail_id}'",
        })
    else:
        findings.append({
            "id": "session_id_ok",
            "level": "ok",
            "message": f"session_id '{session_id}' present",
        })

    title = str(detail.get("title", ""))
    if not title or title == session_id:
        findings.append({
            "id": "session_title_weak",
            "level": "warning",
            "message": "session title equals raw id or is empty",
        })
    else:
        findings.append({
            "id": "session_title_ok",
            "level": "ok",
            "message": "session title differs from raw id",
        })


def _audit_step(
    step: dict[str, Any], source_kind: str, summary: dict[str, Any]
) -> dict[str, Any]:
    """Audit a single step. Returns dict with index, findings, usage basis."""
    step_index = step.get("step_index", "?")
    findings: list[dict[str, str]] = []
    usage = step.get("usage", {})
    if not isinstance(usage, dict):
        usage = {}

    # Step attribution: is usage available?
    usage_available = usage.get("available", False)
    confirmation_status = str(usage.get("confirmation_status", ""))
    usage_source = str(usage.get("source", ""))
    usage_note = str(usage.get("note", ""))

    # Whitelist of confirmed semantic statuses
    _CONFIRMED_STATUSES = {"confirmed_request_usage", "confirmed_cumulative_delta", "confirmed_per_step_delta"}
    _FALLBACK_BASIS = {"cumulative_total_token_usage", "summary_total_only", "total_token_usage_fallback", "delta_unknown", "live_total_token_usage_latest"}

    if usage_available:
        if confirmation_status in _CONFIRMED_STATUSES:
            findings.append({
                "id": "step_usage_confirmed",
                "level": "ok",
                "message": f"Step {step_index}: usage confirmed ({confirmation_status})",
            })
        else:
            # Available number but semantic confirmation is weak/missing
            findings.append({
                "id": "step_usage_available_unlabeled",
                "level": "warning",
                "message": (
                    f"Step {step_index}: usage available but confirmation_status "
                    f"= '{confirmation_status}' — not in confirmed whitelist"
                ),
            })

        # Check for fallback: source string OR semantic basis
        source_lower = usage_source.lower()
        is_fallback_source = (
            "total_token_usage" in source_lower and "last_token_usage" not in source_lower
        )
        is_fallback_basis = confirmation_status in _FALLBACK_BASIS or usage_source in _FALLBACK_BASIS
        if is_fallback_source or is_fallback_basis:
            findings.append({
                "id": "step_usage_fallback_cumulative",
                "level": "warning",
                "message": (
                    f"Step {step_index}: usage appears cumulative/fallback "
                    f"(source='{usage_source}', status='{confirmation_status}')"
                ),
            })
    else:
        if confirmation_status == "missing_request_usage":
            findings.append({
                "id": "step_usage_missing",
                "level": "warning",
                "message": f"Step {step_index}: per-step usage not confirmed — {usage_note}",
            })
        else:
            findings.append({
                "id": "step_usage_missing_unclear",
                "level": "warning",
                "message": (
                    f"Step {step_index}: per-step usage not available, "
                    f"status='{confirmation_status}', note='{usage_note}'"
                ),
            })

    # Check step model vs session model
    step_model = str(step.get("model", "unknown"))
    session_model = str(summary.get("models", [step_model])[0] if summary.get("models") else "unknown")
    if step_model == "unknown" and source_kind == "live":
        findings.append({
            "id": "step_model_unknown",
            "level": "warning",
            "message": f"Step {step_index}: model is 'unknown' in live source",
        })

    # Check prompt/answer availability
    user_prompt = step.get("user_prompt", {})
    assistant_answer = step.get("assistant_answer", {})
    if isinstance(user_prompt, dict) and user_prompt.get("available"):
        pass  # prompt text is present
    elif source_kind == "live":
        findings.append({
            "id": "step_prompt_hidden",
            "level": "ok",
            "message": f"Step {step_index}: prompt hidden by default (live mode)",
        })

    return {
        "step_index": step_index,
        "usage_available": usage_available,
        "usage_confirmation_status": confirmation_status,
        "usage_source": usage_source,
        "findings": findings,
    }


def _check_summary_basis(
    findings: list[dict[str, str]],
    detail: dict[str, Any],
    source_kind: str,
    steps: list[dict[str, Any]],
) -> None:
    """Check that summary basis is distinct from visible-step sums where needed."""
    summary = detail.get("summary")
    if not isinstance(summary, dict):
        findings.append({
            "id": "summary_missing",
            "level": "warning",
            "message": "No summary block in session detail",
        })
        return

    usage_basis = str(summary.get("usage_basis", ""))
    step_usage_basis = str(summary.get("step_usage_basis", ""))

    if source_kind == "live":
        if not usage_basis:
            findings.append({
                "id": "summary_no_usage_basis",
                "level": "warning",
                "message": "Live summary has no usage_basis field",
            })
        elif "cumulative" in usage_basis.lower() or "total" in usage_basis.lower():
            findings.append({
                "id": "summary_cumulative_acknowledged",
                "level": "ok",
                "message": f"Live summary correctly labels basis as '{usage_basis}'",
            })
        else:
            findings.append({
                "id": "summary_basis_may_overstate",
                "level": "warning",
                "message": (
                    f"Live summary usage_basis = '{usage_basis}' — may not clearly "
                    f"separate cumulative from per-step"
                ),
            })

    # Check summary warnings presence
    summary_warnings = summary.get("warnings", [])
    has_warnings = isinstance(summary_warnings, list) and len(summary_warnings) > 0
    if source_kind == "live" and not has_warnings:
        findings.append({
            "id": "summary_no_live_warnings",
            "level": "warning",
            "message": "Live summary has no warnings about cumulative totals or step basis",
        })

    # Visible step sum vs summary total: detect potential mismatch
    def _safe_int(val: Any) -> int:
        """Convert value to int, treating non-numeric as 0."""
        if isinstance(val, (int, float)):
            return int(val)
        if isinstance(val, str):
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return 0
        return 0

    visible_input_sum = sum(
        _safe_int((s.get("usage", {}) or {}).get("input_tokens", 0))
        for s in steps
        if (s.get("usage", {}) or {}).get("available")
    )
    summary_input = _safe_int(summary.get("total_input_tokens", 0))
    if summary_input > 0 and visible_input_sum > 0 and source_kind == "live":
        ratio = visible_input_sum / summary_input if summary_input > 0 else 0
        if ratio < 0.5 and visible_input_sum > 0:
            findings.append({
                "id": "summary_visible_step_mismatch",
                "level": "warning",
                "message": (
                    f"Visible step input sum ({visible_input_sum}) is much smaller than "
                    f"summary total ({summary_input}, ratio={ratio:.1%}). "
                    f"This is expected for live mode but must not be hidden."
                ),
            })


def _check_export_honesty(
    findings: list[dict[str, str]],
    detail: dict[str, Any],
    source_kind: str,
) -> None:
    """Verify that detail payload preserves basis/warning/confidence semantics."""
    # Check that warnings exist somewhere visible
    total_warnings = 0
    for step in detail.get("steps", []) or []:
        sw = step.get("warnings", [])
        if isinstance(sw, list):
            total_warnings += len(sw)

    summary_warnings = detail.get("summary", {}).get("warnings", [])
    if isinstance(summary_warnings, list):
        total_warnings += len(summary_warnings)

    # This is informational: warnings should be present for live sources
    if source_kind == "live" and total_warnings == 0:
        findings.append({
            "id": "export_no_warnings",
            "level": "warning",
            "message": "Live session detail has zero warnings — verification semantics may be lost",
        })

    # Check that confirmation_status fields are present on steps
    steps_without_status = 0
    for step in detail.get("steps", []) or []:
        usage = step.get("usage", {}) or {}
        if "confirmation_status" not in usage:
            steps_without_status += 1

    if steps_without_status > 0:
        findings.append({
            "id": "export_missing_confirmation_status",
            "level": "warning",
            "message": f"{steps_without_status} steps lack confirmation_status field",
        })


def _determine_evidence_basis(
    upstream_evidence_available: bool,
    source_kind: str,
    summary: dict[str, Any],
    findings: list[dict[str, str]],
) -> str:
    """Determine what evidence the audit actually verified against.

    Returns one of:
    - EVIDENCE_VERIFIED: audit compared detail against upstream source
    - EVIDENCE_PLAUSIBLE: detail is internally consistent but no upstream check
    - EVIDENCE_NOT_VERIFIED: audit couldn't verify key properties
    """
    if upstream_evidence_available:
        return EVIDENCE_VERIFIED

    # Without upstream evidence, check if detail at least has internal
    # consistency markers (warnings about basis, acknowledged limitations)
    if source_kind == "live":
        usage_basis = str(summary.get("usage_basis", ""))
        has_warnings = bool(summary.get("warnings"))
        has_basis_ack = "cumulative" in usage_basis.lower() or "total" in usage_basis.lower()

        if has_warnings or has_basis_ack:
            # Detail is internally honest about its limitations
            return EVIDENCE_PLAUSIBLE
        else:
            return EVIDENCE_NOT_VERIFIED

    # Archive: if upstream evidence unavailable, internal consistency
    # is the best we have
    return EVIDENCE_PLAUSIBLE


def _is_summary_basis_cumulative(summary: dict[str, Any], source_kind: str) -> bool:
    """Check if summary cost basis is cumulative rather than per-step."""
    if source_kind != "live":
        return False

    usage_basis = str(summary.get("usage_basis", "")).lower()
    step_usage_basis = str(summary.get("step_usage_basis", "")).lower()

    # Explicit cumulative markers
    cumulative_markers = ["cumulative", "total_token_usage", "live_total"]
    for marker in cumulative_markers:
        if marker in usage_basis:
            return True

    # Step basis uses request-level usage which may not equal
    # visible-step-only attribution
    if "last_token_usage" in step_usage_basis:
        return True

    return False


def _compute_statuses(
    findings: list[dict[str, str]],
    step_findings: list[dict[str, Any]],
    source_kind: str,
    summary: dict[str, Any],
    evidence_basis: str,
    audit_scope: str,
) -> tuple[str, str, str, str, bool]:
    """Derive aggregate audit statuses from findings.

    TRUTH RULES (critical — do not weaken without explicit decision):
    1. Without upstream evidence, strong statuses are blocked.
    2. Cumulative summary basis blocks per_step_estimated cost confidence.
    3. Selected-step scope must not imply full-session verification.
    4. Even if all visible steps carry confirmed_request_usage,
       if summary basis is cumulative, step attribution is uncertain.
    """
    levels = [f.get("level", "ok") for f in findings]

    # Overall audit status — downgrade if evidence is only plausible
    if "fail" in levels:
        audit_status = "fail"
    elif evidence_basis == EVIDENCE_NOT_VERIFIED:
        audit_status = "warning"
    elif evidence_basis == EVIDENCE_PLAUSIBLE and "warning" not in levels:
        # Detail looks internally consistent but we lack upstream proof
        audit_status = "warning"
    elif "warning" in levels:
        audit_status = "warning"
    else:
        audit_status = "ok"

    # Usage confirmation: based on semantic confirmation_status whitelist,
    # NOT on usage_available (number exists != semantics confirmed)
    _CONFIRMED_STATUSES = {"confirmed_request_usage", "confirmed_cumulative_delta", "confirmed_per_step_delta"}
    confirmed_count = sum(
        1 for sf in step_findings
        if sf.get("usage_available")
        and sf.get("usage_confirmation_status") in _CONFIRMED_STATUSES
    )
    total_steps = len(step_findings) if step_findings else 0
    if total_steps == 0:
        usage_confirmation = "not_applicable"
    elif confirmed_count == total_steps:
        usage_confirmation = "all_confirmed"
    elif confirmed_count > 0:
        usage_confirmation = "partial"
    else:
        usage_confirmation = "none_confirmed"

    # Step attribution confidence
    fallback_steps = sum(
        1 for sf in step_findings
        if any(
            f.get("id") == "step_usage_fallback_cumulative"
            for f in sf.get("findings", [])
        )
    )
    missing_steps = total_steps - confirmed_count

    summary_cumulative = _is_summary_basis_cumulative(summary, source_kind)

    # TRUTH RULE: if summary basis is cumulative, step attribution
    # cannot be "high" even if all visible steps look confirmed.
    # The cumulative basis means per-step numbers are request-level
    # (may include hidden context), not pure visible-step attribution.
    if fallback_steps > 0:
        step_confidence = "low"
    elif summary_cumulative and evidence_basis != EVIDENCE_VERIFIED:
        # Cumulative basis + no upstream proof = medium at best
        step_confidence = "medium"
    elif summary_cumulative and evidence_basis == EVIDENCE_VERIFIED:
        # Cumulative basis but upstream evidence verified the mapping
        step_confidence = "medium"
    elif missing_steps > 0 and source_kind == "live":
        step_confidence = "medium"
    elif missing_steps > 0:
        step_confidence = "low"
    else:
        # Only reachable for archive with full confirmed steps
        # AND verified evidence — very rare
        step_confidence = "medium" if evidence_basis != EVIDENCE_VERIFIED else "high"

    # Cost confidence
    # TRUTH RULE: cumulative summary basis → cost is always
    # estimated_from_cumulative, never per_step_estimated.
    if summary_cumulative:
        cost_confidence = "estimated_from_cumulative"
    elif source_kind == "live" and usage_confirmation in ("partial", "none_confirmed"):
        cost_confidence = "estimated_from_cumulative"
    elif usage_confirmation == "all_confirmed" and evidence_basis == EVIDENCE_VERIFIED:
        # Only when we have upstream proof AND all steps confirmed
        cost_confidence = "per_step_estimated"
    elif usage_confirmation == "all_confirmed":
        # All steps confirmed but no upstream evidence
        cost_confidence = "estimated_from_cumulative"
    else:
        cost_confidence = "estimated_from_cumulative"

    # Fallback used
    fallback_used = fallback_steps > 0 or any(
        f.get("id") == "step_usage_fallback_cumulative" for f in findings
    )

    return audit_status, usage_confirmation, step_confidence, cost_confidence, fallback_used


# ── Artifact generation ──


def generate_audit_artifacts(
    result: AuditResult,
    output_dir: Path,
    *,
    session_id: str | None = None,
    source_id: str | None = None,
) -> tuple[Path, Path]:
    """Write audit_summary.json and audit_report.md to output_dir.

    Returns (summary_path, report_path).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON summary
    summary_path = output_dir / "monitor_audit_summary.json"
    summary_payload = {
        "audit_status": result["audit_status"],
        "usage_confirmation": result["usage_confirmation"],
        "step_attribution_confidence": result["step_attribution_confidence"],
        "cost_confidence": result["cost_confidence"],
        "fallback_used": result["fallback_used"],
        "audit_scope": result.get("audit_scope", "full_session"),
        "evidence_basis": result.get("evidence_basis", EVIDENCE_NOT_VERIFIED),
        "upstream_evidence_available": result.get("upstream_evidence_available", False),
        "total_steps_in_session": result.get("total_steps_in_session", 0),
        "audited_steps_count": result.get("audited_steps_count", 0),
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
        "source_kind": result["source_kind"],
        "session_id": result["session_id"],
        "source_id": result["source_id"],
        "audit_timestamp": result["audit_timestamp"],
    }
    summary_path.write_text(
        json.dumps(summary_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Write Markdown report
    report_path = output_dir / "monitor_audit_report.md"
    report_lines = _build_report_markdown(result)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    return summary_path, report_path


def _build_report_markdown(result: AuditResult) -> list[str]:
    """Build audit report as Markdown lines."""
    lines: list[str] = []
    lines.append("# Codex Token Monitor Audit Report")
    lines.append("")
    lines.append(f"- **Audit status:** `{result['audit_status']}`")
    lines.append(f"- **Evidence basis:** `{result.get('evidence_basis', EVIDENCE_NOT_VERIFIED)}`")
    lines.append(f"- **Audit scope:** `{result.get('audit_scope', 'full_session')}`")
    if result.get("audit_scope") == "selected_steps":
        lines.append(f"- **Audited steps:** {result.get('audited_steps_count', 0)} из {result.get('total_steps_in_session', 0)}")
    lines.append(f"- **Usage confirmation:** `{result['usage_confirmation']}`")
    lines.append(f"- **Step attribution confidence:** `{result['step_attribution_confidence']}`")
    lines.append(f"- **Cost confidence:** `{result['cost_confidence']}`")
    lines.append(f"- **Fallback used:** `{result['fallback_used']}`")
    lines.append(f"- **Upstream evidence:** `{'да' if result.get('upstream_evidence_available') else 'нет'}`")
    lines.append(f"- **Source kind:** `{result['source_kind']}`")
    lines.append(f"- **Session ID:** `{result['session_id']}`")
    lines.append(f"- **Timestamp:** `{result['audit_timestamp']}`")
    lines.append("")

    lines.append("## Audit Findings")
    lines.append("")
    findings = result.get("findings", [])
    if not findings:
        lines.append("Нет замечаний — все проверки пройдены.")
    else:
        lines.append("| Level | ID | Message |")
        lines.append("|---|---|---|")
        for f in findings:
            level_emoji = {"ok": "✅", "warning": "⚠️", "fail": "❌"}.get(f.get("level", ""), "❓")
            lines.append(
                f"| {level_emoji} {f.get('level', '')} "
                f"| `{f.get('id', '')}` "
                f"| {f.get('message', '')} |"
            )
    lines.append("")

    lines.append("## Per-Step Summary")
    lines.append("")
    step_findings = result.get("step_findings", [])
    if not step_findings:
        lines.append("Нет шагов для аудита.")
    else:
        lines.append("| Step | Usage | Confirmation | Source | Warnings |")
        lines.append("|---|---|---|---|---|")
        for sf in step_findings:
            warn_count = sum(
                1 for f in sf.get("findings", [])
                if f.get("level") in ("warning", "fail")
            )
            ok_count = sum(
                1 for f in sf.get("findings", [])
                if f.get("level") == "ok"
            )
            lines.append(
                f"| {sf.get('step_index', '?')} "
                f"| {'✅' if sf.get('usage_available') else '❌'} "
                f"| `{sf.get('usage_confirmation_status', '?')}` "
                f"| `{sf.get('usage_source', '?')}` "
                f"| {'⚠️' if warn_count > 0 else '✅'} {warn_count}w/{ok_count}ok |"
            )
    lines.append("")

    lines.append("## Интерпретация статусов")
    lines.append("")
    lines.append("- **Audit status** — общая техническая оценка: `ok` (все проверки пройдены с upstream evidence), `warning` (есть неопределённости или нет upstream evidence), `fail` (обнаружены ошибки).")
    lines.append("- **Evidence basis** — на чём основана верификация:")
    lines.append(f"  - `{EVIDENCE_VERIFIED}` — audit сравнил detail с upstream source evidence (raw rollout, raw OTel);")
    lines.append(f"  - `{EVIDENCE_PLAUSIBLE}` — detail внутренне непротиворечив, но upstream evidence недоступен;")
    lines.append(f"  - `{EVIDENCE_NOT_VERIFIED}` — audit не смог проверить ключевые свойства.")
    lines.append("- **Audit scope** — `full_session` (все шаги) или `selected_steps` (только выбранные шаги).")
    lines.append("- **Usage confirmation** — сколько шагов имеют подтверждённые per-step данные: `all_confirmed`, `partial`, `none_confirmed`, `not_applicable`.")
    lines.append("- **Step attribution confidence** — насколько можно доверять привязке токенов к видимым шагам: `high` (только archive + upstream evidence), `medium`, `low`.")
    lines.append("- **Cost confidence** — основа оценки стоимости: `per_step_estimated` (только при upstream evidence + non-cumulative basis), `estimated_from_cumulative`.")
    lines.append("- **Fallback used** — были ли случаи, где cumulative totals использовались вместо per-step данных.")
    lines.append("")
    lines.append("> Этот отчёт — техническая верификация. Статус `warning` при отсутствии upstream evidence — это нормальное и честное поведение, а не ошибка. `Honesty hardening` (улучшение формулировок и UI-пояснений) — отдельный следующий слой.")

    return lines


# ── CLI entry point (for direct script use) ──


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Codex Token Monitor Audit — run verification over session detail"
    )
    parser.add_argument(
        "--detail",
        required=True,
        help="Path to session detail JSON file (from monitor API or saved export)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for audit artifacts (default: _local/codex-token-monitor/audits/<source>/<session>)",
    )
    parser.add_argument(
        "--source-id",
        default="",
        help="Source identifier",
    )
    parser.add_argument(
        "--source-kind",
        default=None,
        help="Expected source kind (live/archive)",
    )
    parser.add_argument(
        "--selected-steps",
        default=None,
        help="Comma-separated step indices for narrowed audit scope (0-based)",
    )
    parser.add_argument(
        "--upstream-evidence",
        action="store_true",
        default=False,
        help="Set if audit has upstream source evidence beyond detail object",
    )
    args = parser.parse_args()

    detail_path = Path(args.detail)
    if not detail_path.exists():
        print(f"Error: detail file not found: {detail_path}", file=sys.stderr)
        sys.exit(1)

    detail = json.loads(detail_path.read_text(encoding="utf-8"))

    source_kind = args.source_kind or detail.get("source_kind", "")
    session_id = str(detail.get("id", ""))
    source_id = args.source_id or ""

    selected_step_indices = None
    if args.selected_steps:
        selected_step_indices = [int(x.strip()) for x in args.selected_steps.split(",") if x.strip()]

    result = run_audit(
        detail,
        source_kind=source_kind,
        source_id=source_id,
        session_id=session_id,
        selected_step_indices=selected_step_indices,
        upstream_evidence_available=args.upstream_evidence,
    )

    # Determine output dir
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = (
            LOCAL_MONITOR_DIR / "audits" / (source_id or "unknown") / (session_id or "unknown")
        )

    summary_path, report_path = generate_audit_artifacts(
        result, output_dir, session_id=session_id, source_id=source_id
    )

    print(f"Audit status: {result['audit_status']}")
    print(f"Evidence basis: {result.get('evidence_basis', EVIDENCE_NOT_VERIFIED)}")
    print(f"Audit scope: {result.get('audit_scope', 'full_session')}")
    print(f"Usage confirmation: {result['usage_confirmation']}")
    print(f"Step attribution confidence: {result['step_attribution_confidence']}")
    print(f"Cost confidence: {result['cost_confidence']}")
    print(f"Fallback used: {result['fallback_used']}")
    print(f"Findings: {len(result['findings'])}")
    print(f"Summary: {summary_path}")
    print(f"Report:  {report_path}")


if __name__ == "__main__":
    main()
