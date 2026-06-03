from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "tool_mcp_activity_inspector.py"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


class ToolMcpActivityInspectorTest(unittest.TestCase):
    def test_builds_activity_outputs_without_private_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            a_dir = root / "a"
            b_dir = root / "b"
            compare_dir = root / "compare"
            out_dir = compare_dir / "tool_mcp_activity"
            a_dir.mkdir()
            b_dir.mkdir()
            compare_dir.mkdir()

            compare_summary = {
                "modes": [
                    {
                        "mode_id": "A-current-config",
                        "mcp_server_count": 3,
                        "mcp_servers": "github, node_repl, playwright",
                        "turns": [
                            {
                                "turn_id": "A1",
                                "turn_index": 1,
                                "prompt_type": "short_no_tool",
                                "input_tokens": 100,
                                "output_tokens": 10,
                                "cached_tokens": 0,
                                "reasoning_tokens": 1,
                                "tool_tokens": 110,
                                "tool_call_status": "none_expected",
                                "window_start": "2026-06-03T21:55:00+00:00",
                                "window_end": "2026-06-03T21:55:20+00:00",
                            },
                            {
                                "turn_id": "A2",
                                "turn_index": 2,
                                "prompt_type": "second_short_no_tool",
                                "input_tokens": 120,
                                "output_tokens": 10,
                                "cached_tokens": 60,
                                "reasoning_tokens": 1,
                                "tool_tokens": 130,
                                "tool_call_status": "none_expected",
                                "window_start": "2026-06-03T21:55:30+00:00",
                                "window_end": "2026-06-03T21:55:40+00:00",
                            },
                            {
                                "turn_id": "A3",
                                "turn_index": 3,
                                "prompt_type": "safe_tool_call_then_answer",
                                "input_tokens": 180,
                                "output_tokens": 20,
                                "cached_tokens": 70,
                                "reasoning_tokens": 0,
                                "tool_tokens": 200,
                                "tool_call_status": "called",
                                "window_start": "2026-06-03T21:55:50+00:00",
                                "window_end": "2026-06-03T21:56:10+00:00",
                            },
                        ],
                    },
                    {
                        "mode_id": "B-minimal-config",
                        "mcp_server_count": 1,
                        "mcp_servers": "node_repl",
                        "turns": [
                            {
                                "turn_id": "B1",
                                "turn_index": 1,
                                "prompt_type": "short_no_tool",
                                "input_tokens": 80,
                                "output_tokens": 8,
                                "cached_tokens": 0,
                                "reasoning_tokens": 1,
                                "tool_tokens": 88,
                                "tool_call_status": "none_expected",
                                "window_start": "2026-06-03T22:00:00+00:00",
                                "window_end": "2026-06-03T22:00:20+00:00",
                            },
                            {
                                "turn_id": "B2",
                                "turn_index": 2,
                                "prompt_type": "second_short_no_tool",
                                "input_tokens": 90,
                                "output_tokens": 9,
                                "cached_tokens": 50,
                                "reasoning_tokens": 1,
                                "tool_tokens": 99,
                                "tool_call_status": "none_expected",
                                "window_start": "2026-06-03T22:00:30+00:00",
                                "window_end": "2026-06-03T22:00:40+00:00",
                            },
                            {
                                "turn_id": "B3",
                                "turn_index": 3,
                                "prompt_type": "safe_tool_call_then_answer",
                                "input_tokens": 95,
                                "output_tokens": 15,
                                "cached_tokens": 50,
                                "reasoning_tokens": 0,
                                "tool_tokens": 110,
                                "tool_call_status": "called",
                                "window_start": "2026-06-03T22:00:50+00:00",
                                "window_end": "2026-06-03T22:01:10+00:00",
                            },
                        ],
                    },
                ],
                "comparisons": {
                    "baseline_overhead": {"A1_minus_B1_input_tokens": 20},
                    "tool_turn_overhead": {"A3_minus_A2_input_tokens": 60, "B3_minus_B2_input_tokens": 5},
                    "mcp_tool_environment_overhead": {"A3_minus_B3_input_tokens": 85},
                },
            }
            (compare_dir / "compare_summary.json").write_text(
                json.dumps(compare_summary, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            write_jsonl(
                a_dir / "clean_events.jsonl",
                [
                    {
                        "event_name": "codex.conversation_starts",
                        "timestamp": "2026-06-03T21:54:50+00:00",
                        "attributes": {"mcp_servers": "github, node_repl, playwright", "mcp_server_count": 3},
                    },
                    {
                        "event_name": "codex.test",
                        "timestamp": "2026-06-03T21:55:02+00:00",
                        "attributes": {"event.name": "codex.test", "list_all_tools": True, "user.email": "hidden@example.test"},
                    },
                ],
            )
            write_jsonl(
                a_dir / "spans.jsonl",
                [
                    {
                        "span_name": "list_all_tools",
                        "service_name": "codex-app-server",
                        "start_time": "2026-06-03T21:55:03+00:00",
                        "duration_ms": 12,
                        "traceId": "trace-a1",
                        "spanId": "span-a1",
                        "attributes": {"target": "codex_mcp::connection_manager"},
                    },
                    {
                        "span_name": "transport_worker",
                        "service_name": "codex-app-server",
                        "start_time": "2026-06-03T21:55:33+00:00",
                        "duration_ms": 7,
                        "traceId": "trace-a2",
                        "spanId": "span-a2",
                        "attributes": {"code.module.name": "rmcp::transport::StreamableHttpClientWorker"},
                    },
                    {
                        "span_name": "build_tool_call",
                        "service_name": "codex-app-server",
                        "start_time": "2026-06-03T21:55:55+00:00",
                        "duration_ms": 5,
                        "traceId": "trace-a3",
                        "spanId": "span-a3",
                        "attributes": {"conversation.id": "secret-conversation"},
                    },
                ],
            )
            write_jsonl(
                a_dir / "metrics.jsonl",
                [
                    {
                        "metric_name": "codex.turn.tool.call",
                        "service_name": "codex-app-server",
                        "timestamp": "2026-06-03T21:55:58+00:00",
                        "value": 1,
                        "attributes": {"tool": "safe_read"},
                    }
                ],
            )
            write_jsonl(b_dir / "clean_events.jsonl", [])
            write_jsonl(b_dir / "spans.jsonl", [])
            write_jsonl(
                b_dir / "metrics.jsonl",
                [
                    {
                        "metric_name": "codex.mcp.call.duration_ms",
                        "service_name": "codex-app-server",
                        "timestamp": "2026-06-03T22:00:55+00:00",
                        "value": 3,
                        "attributes": {"mcp": "node_repl"},
                    }
                ],
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--compare-summary",
                    str(compare_dir / "compare_summary.json"),
                    "--a-parsed",
                    str(a_dir),
                    "--b-parsed",
                    str(b_dir),
                    "--output-dir",
                    str(out_dir),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)

            activity_rows = [
                json.loads(line)
                for line in (out_dir / "tool_mcp_activity.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            activity_types = {row["activity_type"] for row in activity_rows}
            self.assertIn("mcp_tool_discovery", activity_types)
            self.assertIn("mcp_transport", activity_types)
            self.assertIn("tool_call_build", activity_types)
            self.assertIn("tool_call_metric", activity_types)
            self.assertIn("mcp_call_duration_metric", activity_types)

            a3_build = next(row for row in activity_rows if row["activity_type"] == "tool_call_build")
            self.assertEqual(a3_build["mode_id"], "A-current-config")
            self.assertEqual(a3_build["turn_id"], "A3")
            self.assertEqual(a3_build["attach_method"], "time_window")

            summary = json.loads((out_dir / "tool_mcp_activity_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["modes"]["A-current-config"]["mcp_server_count"], 3)
            self.assertEqual(summary["turns"]["A-current-config::A3"]["tool_call_status"], "called")
            self.assertGreater(summary["turns"]["A-current-config::A3"]["activity_counts_by_type"]["tool_call_build"], 0)

            report = (out_dir / "tool_mcp_activity_report.md").read_text(encoding="utf-8")
            self.assertIn("Tool/MCP Activity Report", report)
            self.assertIn("A-current-config", report)
            self.assertIn("+20", report)

            output_text = (out_dir / "tool_mcp_activity.jsonl").read_text(encoding="utf-8")
            self.assertNotIn("hidden@example.test", output_text)
            self.assertNotIn("secret-conversation", output_text)


if __name__ == "__main__":
    unittest.main()
