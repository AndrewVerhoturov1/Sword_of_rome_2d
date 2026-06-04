from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "mcp_schema_inventory.py"


class McpSchemaInventoryTest(unittest.TestCase):
    def test_builds_sanitized_inventory_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            config_path = root / "config.toml"
            compare_path = root / "compare_summary.json"
            activity_path = root / "tool_mcp_activity_summary.json"
            out_dir = root / "mcp_schema_inventory"

            config_path.write_text(
                textwrap.dedent(
                    """
                    [mcp_servers.github]
                    command = "npx"
                    args = ["-y", "@github/mcp"]
                    env = { "GITHUB_TOKEN" = "secret-value", "USER_EMAIL" = "user@example.test" }

                    [mcp_servers.github.tools.create_pull_request]
                    description = "Create a pull request from a branch."
                    input_schema = { "type" = "object", "properties" = { "title" = { "type" = "string" } } }

                    [mcp_servers.github.tools.list_issues]
                    description = "List issues."
                    input_schema = { "type" = "object" }

                    [mcp_servers.node_repl]
                    command = "C:\\\\Tools\\\\node_repl.exe"
                    args = []
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            compare_path.write_text(
                json.dumps(
                    {
                        "modes": [
                            {
                                "mode_id": "A-current-config",
                                "mcp_server_count": 3,
                                "mcp_servers": "github, node_repl, tavily",
                            },
                            {
                                "mode_id": "B-minimal-config",
                                "mcp_server_count": 1,
                                "mcp_servers": "node_repl",
                            },
                        ],
                        "comparisons": {
                            "baseline_overhead": {"A1_minus_B1_input_tokens": 10155},
                            "tool_turn_overhead": {"A3_minus_A2_input_tokens": 200, "B3_minus_B2_input_tokens": 205},
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            activity_path.write_text(
                json.dumps(
                    {
                        "modes": {
                            "A-current-config": {"total_list_all_tools": 10},
                            "B-minimal-config": {"total_list_all_tools": 3},
                        }
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--config",
                    str(config_path),
                    "--compare-summary",
                    str(compare_path),
                    "--activity-summary",
                    str(activity_path),
                    "--output-dir",
                    str(out_dir),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)

            inventory_rows = [
                json.loads(line)
                for line in (out_dir / "mcp_schema_inventory.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            github = next(row for row in inventory_rows if row["server_name"] == "github")
            node_repl = next(row for row in inventory_rows if row["server_name"] == "node_repl")
            tavily = next(row for row in inventory_rows if row["server_name"] == "tavily")

            self.assertEqual(github["source"], "current_config")
            self.assertEqual(node_repl["source"], "both")
            self.assertEqual(tavily["warnings"], ["schema_unavailable"])
            self.assertEqual(github["command_safe"], "npx")
            self.assertEqual(node_repl["command_safe"], "node_repl.exe")
            self.assertEqual(github["args_count"], 2)
            self.assertEqual(github["env_keys_count"], 2)
            self.assertEqual(github["env_keys_sanitized"], ["GITHUB_TOKEN", "USER_EMAIL"])
            self.assertEqual(github["tool_count"], 2)
            self.assertIn("create_pull_request", github["tool_names"])
            self.assertGreater(github["total_schema_chars"], github["total_description_chars"])
            self.assertEqual(github["estimated_schema_tokens"], (github["total_schema_chars"] + 3) // 4)

            summary = json.loads((out_dir / "mcp_schema_inventory_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["token_estimator"], "ceil(chars / 4)")
            self.assertFalse(summary["metadata"]["tools_executed"])
            self.assertEqual(summary["totals"]["server_count_current"], 3)
            self.assertEqual(summary["totals"]["server_count_minimal"], 1)
            self.assertEqual(summary["totals"]["schema_available_server_count"], 1)
            self.assertEqual(summary["servers_ranked_by_estimated_tokens"][0]["server_name"], "github")
            self.assertIn("tavily", summary["servers_with_unavailable_schema"])

            warnings_text = (out_dir / "mcp_schema_inventory_warnings.jsonl").read_text(encoding="utf-8")
            self.assertIn("schema_unavailable", warnings_text)
            self.assertIn("token_estimate_rough", warnings_text)

            report = (out_dir / "mcp_schema_inventory_report.md").read_text(encoding="utf-8")
            self.assertIn("MCP Schema Inventory Report", report)
            self.assertIn("+10155", report)
            self.assertIn("Это грубая оценка", report)

            output_text = "\n".join(path.read_text(encoding="utf-8") for path in out_dir.iterdir())
            self.assertNotIn("secret-value", output_text)
            self.assertNotIn("user@example.test", output_text)


if __name__ == "__main__":
    unittest.main()
