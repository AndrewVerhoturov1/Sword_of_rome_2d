from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "codex_token_debugger.py"
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "codex_otel_sample.jsonl"


class CodexTokenDebuggerTest(unittest.TestCase):
    def test_parser_creates_sanitized_outputs_and_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir) / "out"
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--input", str(FIXTURE_PATH), "--output-dir", str(output_dir)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)

            expected_files = {
                "clean_events.jsonl",
                "token_usage.jsonl",
                "spans.jsonl",
                "metrics.jsonl",
                "sessions.jsonl",
                "session_summary.json",
                "warnings.jsonl",
                "diagnostic_report.md",
            }
            self.assertEqual(expected_files, {path.name for path in output_dir.iterdir()})

            clean_lines = [
                json.loads(line) for line in (output_dir / "clean_events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()
            ]
            clean_blob = json.dumps(clean_lines, ensure_ascii=False)
            self.assertNotIn("user.email", clean_blob)
            self.assertNotIn("user.account_id", clean_blob)
            self.assertNotIn("conversation.id", clean_blob)
            self.assertIn('"prompt": "[REDACTED]"', clean_blob)
            self.assertIn('"prompt_length": "25"', clean_blob)

            token_lines = [
                json.loads(line) for line in (output_dir / "token_usage.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()
            ]
            self.assertTrue(any(item.get("metric_name") == "codex.turn.token_usage" for item in token_lines))
            self.assertTrue(any(item.get("input_token_count") == 29895 for item in token_lines))

            span_lines = [
                json.loads(line) for line in (output_dir / "spans.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()
            ]
            self.assertEqual(span_lines[0]["duration_ms"], 3000.0)
            self.assertEqual(span_lines[0]["traceId"], "trace-2")

            metric_lines = [
                json.loads(line) for line in (output_dir / "metrics.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()
            ]
            self.assertTrue(any(item.get("metric_name") == "codex.turn.tool.call" for item in metric_lines))

            warning_lines = [
                json.loads(line) for line in (output_dir / "warnings.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()
            ]
            warning_kinds = {item["warning_type"] for item in warning_lines}
            self.assertIn("private_fields_detected_in_raw", warning_kinds)
            self.assertIn("prompt_metadata_present", warning_kinds)
            self.assertNotIn("prompt_field_present_in_raw", warning_kinds)
            self.assertIn("many_mcp_servers", warning_kinds)
            self.assertIn("high_input_low_output", warning_kinds)

            private_warning = next(item for item in warning_lines if item["warning_type"] == "private_fields_detected_in_raw")
            self.assertIn("user.email", private_warning["context"]["detected_field_names"])
            self.assertIn("user.account_id", private_warning["context"]["detected_field_names"])
            self.assertIn("conversation.id", private_warning["context"]["detected_field_names"])

            summary = json.loads((output_dir / "session_summary.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(summary["counts"]["clean_events"], 2)
            self.assertIn("input_token_count", summary["token_fields_found"])

            report_text = (output_dir / "diagnostic_report.md").read_text(encoding="utf-8")
            self.assertIn("`prompt_length` сохраняется как диагностический сигнал.", report_text)
            self.assertIn("Текст prompt не должен храниться в открытом виде.", report_text)


if __name__ == "__main__":
    unittest.main()
