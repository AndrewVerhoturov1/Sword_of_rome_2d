from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "codex_otel_compare.py"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


class CodexOtelCompareTest(unittest.TestCase):
    def test_compare_builds_turn_summary_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            a_dir = root / "a"
            b_dir = root / "b"
            out_dir = root / "out"
            a_dir.mkdir()
            b_dir.mkdir()

            a_events = [
                {"event_name": "codex.conversation_starts", "timestamp": "2026-06-03T21:54:33+00:00", "attributes": {"mcp_servers": "a, b, c", "model": "gpt-5.4"}},
                {"event_name": "codex.user_prompt", "timestamp": "2026-06-03T21:55:20+00:00", "attributes": {"prompt_length": "165", "model": "gpt-5.5"}},
                {"event_name": "codex.sse_event", "timestamp": "2026-06-03T21:55:39+00:00", "attributes": {"event.kind": "response.completed", "model": "gpt-5.5", "input_token_count": "100", "output_token_count": "10", "cached_token_count": 0, "reasoning_token_count": 1, "tool_token_count": "110"}},
                {"event_name": "codex.user_prompt", "timestamp": "2026-06-03T21:55:51+00:00", "attributes": {"prompt_length": "165", "model": "gpt-5.5"}},
                {"event_name": "codex.sse_event", "timestamp": "2026-06-03T21:55:58+00:00", "attributes": {"event.kind": "response.completed", "model": "gpt-5.5", "input_token_count": "90", "output_token_count": "9", "cached_token_count": 50, "reasoning_token_count": 0, "tool_token_count": "99"}},
                {"event_name": "codex.user_prompt", "timestamp": "2026-06-03T21:56:07+00:00", "attributes": {"prompt_length": "661", "model": "gpt-5.5"}},
                {"event_name": "codex.sse_event", "timestamp": "2026-06-03T21:56:21+00:00", "attributes": {"event.kind": "response.completed", "model": "gpt-5.5", "input_token_count": "130", "output_token_count": "15", "cached_token_count": 60, "reasoning_token_count": 0, "tool_token_count": "145"}},
            ]
            b_events = [
                {"event_name": "codex.conversation_starts", "timestamp": "2026-06-03T21:40:18+00:00", "attributes": {"mcp_servers": "node_repl, codex_apps", "model": "gpt-5.4"}},
                {"event_name": "codex.user_prompt", "timestamp": "2026-06-03T21:40:40+00:00", "attributes": {"prompt_length": "165", "model": "gpt-5.5"}},
                {"event_name": "codex.sse_event", "timestamp": "2026-06-03T21:40:54+00:00", "attributes": {"event.kind": "response.completed", "model": "gpt-5.5", "input_token_count": "80", "output_token_count": "8", "cached_token_count": 10, "reasoning_token_count": 2, "tool_token_count": "88"}},
                {"event_name": "codex.user_prompt", "timestamp": "2026-06-03T21:41:03+00:00", "attributes": {"prompt_length": "165", "model": "gpt-5.5"}},
                {"event_name": "codex.sse_event", "timestamp": "2026-06-03T21:41:08+00:00", "attributes": {"event.kind": "response.completed", "model": "gpt-5.5", "input_token_count": "70", "output_token_count": "7", "cached_token_count": 40, "reasoning_token_count": 1, "tool_token_count": "77"}},
                {"event_name": "codex.user_prompt", "timestamp": "2026-06-03T21:41:17+00:00", "attributes": {"prompt_length": "685", "model": "gpt-5.5"}},
                {"event_name": "codex.sse_event", "timestamp": "2026-06-03T21:41:22+00:00", "attributes": {"event.kind": "response.completed", "model": "gpt-5.5", "input_token_count": "85", "output_token_count": "9", "cached_token_count": 45, "reasoning_token_count": 0, "tool_token_count": "94"}},
            ]
            a_spans = [
                {"span_name": "list_tools_for_server", "start_time": "2026-06-03T21:56:10+00:00"},
                {"span_name": "handle_tool_call", "start_time": "2026-06-03T21:56:12+00:00"},
                {"span_name": "transport_worker", "start_time": "2026-06-03T21:56:13+00:00"},
            ]
            b_spans = [
                {"span_name": "handle_tool_call", "start_time": "2026-06-03T21:41:18+00:00"},
            ]
            a_metrics = [
                {"metric_name": "codex.turn.tool.call", "timestamp": "2026-06-03T21:56:15+00:00"},
                {"metric_name": "codex.mcp.tools.list.duration_ms", "timestamp": "2026-06-03T21:56:15+00:00"},
            ]
            b_metrics = [
                {"metric_name": "codex.turn.tool.call", "timestamp": "2026-06-03T21:41:19+00:00"},
            ]

            for directory, events, spans, metrics in (
                (a_dir, a_events, a_spans, a_metrics),
                (b_dir, b_events, b_spans, b_metrics),
            ):
                write_jsonl(directory / "clean_events.jsonl", events)
                write_jsonl(directory / "spans.jsonl", spans)
                write_jsonl(directory / "metrics.jsonl", metrics)

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--a-parsed", str(a_dir), "--b-parsed", str(b_dir), "--output-dir", str(out_dir)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            summary = json.loads((out_dir / "compare_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["modes"][0]["turns"][0]["turn_id"], "A1")
            self.assertEqual(summary["modes"][0]["turns"][2]["tool_call_status"], "called")
            self.assertEqual(summary["modes"][1]["turns"][2]["tool_call_status"], "called")
            self.assertEqual(summary["comparisons"]["baseline_overhead"]["A1_minus_B1_input_tokens"], 20)
            self.assertEqual(summary["comparisons"]["tool_turn_overhead"]["A3_minus_A2_input_tokens"], 40)

            report = (out_dir / "compare_report.md").read_text(encoding="utf-8")
            self.assertIn("A-current-config", report)
            self.assertIn("B-minimal-config", report)
            self.assertIn("tool-turn environment overhead", report)


if __name__ == "__main__":
    unittest.main()
