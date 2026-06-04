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
    def test_builds_effective_inventory_and_report(self) -> None:
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

                    [mcp_servers.node_repl]
                    command = "C:\\\\Tools\\\\node_repl.exe"
                    args = []
                    enabled = true

                    [mcp_servers.google_workspace]
                    command = "uvx"
                    enabled = false

                    [mcp_servers.paper]
                    url = "http://localhost:29979/mcp"
                    enabled = true
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
                                "mcp_server_count": 5,
                                "mcp_servers": "github, node_repl, google_workspace, telemetry_only, codex_apps",
                            },
                            {
                                "mode_id": "B-minimal-config",
                                "mcp_server_count": 2,
                                "mcp_servers": "node_repl, codex_apps",
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
                            "A-current-config": {"total_tool_mcp_activity_records": 10},
                            "B-minimal-config": {"total_tool_mcp_activity_records": 3},
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
            by_name = {row["server_name"]: row for row in inventory_rows}

            github = by_name["github"]
            node_repl = by_name["node_repl"]
            google_workspace = by_name["google_workspace"]
            paper = by_name["paper"]
            telemetry_only = by_name["telemetry_only"]
            codex_apps = by_name["codex_apps"]

            self.assertTrue(github["config_present"])
            self.assertIsNone(github["enabled_raw"])
            self.assertTrue(github["effective_enabled"])
            self.assertEqual(github["enabled_source"], "implicit_default_true")
            self.assertEqual(github["mismatch_flags"], [])

            self.assertTrue(node_repl["config_present"])
            self.assertTrue(node_repl["enabled_raw"])
            self.assertTrue(node_repl["effective_enabled"])
            self.assertEqual(node_repl["enabled_source"], "explicit_true")
            self.assertTrue(node_repl["observed_in_current_telemetry"])
            self.assertTrue(node_repl["observed_in_minimal_telemetry"])

            self.assertFalse(google_workspace["enabled_raw"])
            self.assertFalse(google_workspace["effective_enabled"])
            self.assertEqual(google_workspace["enabled_source"], "explicit_false")
            self.assertIn("observed_current_but_config_disabled", google_workspace["mismatch_flags"])
            self.assertIn("config_disabled_but_observed_current", google_workspace["mismatch_flags"])

            self.assertTrue(paper["enabled_raw"])
            self.assertTrue(paper["effective_enabled"])
            self.assertEqual(paper["enabled_source"], "explicit_true")
            self.assertIn("config_enabled_but_not_observed_current", paper["mismatch_flags"])

            self.assertFalse(telemetry_only["config_present"])
            self.assertIsNone(telemetry_only["enabled_raw"])
            self.assertEqual(telemetry_only["effective_enabled"], "unknown")
            self.assertEqual(telemetry_only["enabled_source"], "config_missing")
            self.assertIn("observed_current_but_config_missing", telemetry_only["mismatch_flags"])

            self.assertFalse(codex_apps["config_present"])
            self.assertEqual(codex_apps["effective_enabled"], "unknown")
            self.assertTrue(codex_apps["observed_in_current_telemetry"])
            self.assertTrue(codex_apps["observed_in_minimal_telemetry"])

            self.assertEqual(github["command_safe"], "npx")
            self.assertEqual(node_repl["command_safe"], "node_repl.exe")
            self.assertEqual(github["args_count"], 2)
            self.assertEqual(github["env_keys_count"], 2)
            self.assertEqual(github["env_keys_sanitized"], ["GITHUB_TOKEN", "USER_EMAIL"])
            self.assertEqual(github["tool_count"], 1)
            self.assertGreater(github["total_schema_chars"], github["total_description_chars"])
            self.assertEqual(github["estimated_schema_tokens"], (github["total_schema_chars"] + 3) // 4)

            summary = json.loads((out_dir / "mcp_schema_inventory_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["metadata"]["token_estimator"], "ceil(chars / 4)")
            self.assertFalse(summary["metadata"]["tools_executed"])
            self.assertEqual(summary["counts"]["configured_server_count"], 4)
            self.assertEqual(summary["counts"]["effective_enabled_server_count"], 3)
            self.assertEqual(summary["counts"]["explicit_disabled_server_count"], 1)
            self.assertEqual(summary["counts"]["observed_current_telemetry_count"], 5)
            self.assertEqual(summary["counts"]["observed_minimal_telemetry_count"], 2)
            self.assertGreaterEqual(summary["counts"]["mismatch_count"], 4)

            summary_by_name = {row["server_name"]: row for row in summary["servers"]}
            self.assertEqual(summary_by_name["google_workspace"]["enabled_source"], "explicit_false")
            self.assertEqual(summary_by_name["telemetry_only"]["enabled_source"], "config_missing")

            mismatch_by_name = {row["server_name"]: row for row in summary["mismatches"]}
            self.assertIn("observed_current_but_config_disabled", mismatch_by_name["google_workspace"]["flags"])
            self.assertIn("observed_current_but_config_missing", mismatch_by_name["telemetry_only"]["flags"])

            warnings_text = (out_dir / "mcp_schema_inventory_warnings.jsonl").read_text(encoding="utf-8")
            self.assertIn("schema_unavailable", warnings_text)
            self.assertIn("token_estimate_rough", warnings_text)

            effective_summary = json.loads(
                (out_dir / "effective_mcp_inventory_summary.json").read_text(encoding="utf-8")
            )
            self.assertFalse(effective_summary["metadata"]["live_config_modified"])
            self.assertFalse(effective_summary["metadata"]["raw_otel_read"])
            self.assertEqual(effective_summary["counts"]["configured_server_count"], 4)
            self.assertEqual(effective_summary["counts"]["effective_enabled_server_count"], 3)
            self.assertEqual(effective_summary["counts"]["explicit_disabled_server_count"], 1)
            self.assertEqual(effective_summary["counts"]["observed_current_telemetry_count"], 5)
            self.assertEqual(effective_summary["counts"]["observed_minimal_telemetry_count"], 2)
            self.assertTrue(effective_summary["mismatches"])

            effective_report = (out_dir / "effective_mcp_inventory_report.md").read_text(encoding="utf-8")
            self.assertIn("Effective MCP Inventory Report", effective_report)
            self.assertIn("Configured servers", effective_report)
            self.assertIn("observed_current_but_config_disabled", effective_report)

            report = (out_dir / "mcp_schema_inventory_report.md").read_text(encoding="utf-8")
            self.assertIn("MCP Schema Inventory Report", report)
            self.assertIn("+10155", report)

            output_text = "\n".join(path.read_text(encoding="utf-8") for path in out_dir.iterdir())
            self.assertNotIn("secret-value", output_text)
            self.assertNotIn("user@example.test", output_text)

    def test_builds_tool_environment_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            config_path = root / "config.toml"
            before_after_path = root / "before_vs_after_4_mcp_summary.json"
            playwright_path = root / "playwright_only_confirmation_summary.json"
            effective_path = root / "effective_mcp_inventory_summary.json"
            before_after_report = root / "before_vs_after_4_mcp_report.md"
            playwright_report = root / "playwright_only_confirmation_report.md"
            effective_report = root / "effective_mcp_inventory_report.md"
            out_dir = root / "tool_environment_inventory"
            ai_root = root / ".ai"
            ai_root.mkdir()
            (ai_root / "policies").mkdir()

            config_path.write_text(
                textwrap.dedent(
                    """
                    [features]
                    rmcp_client = true
                    js_repl = false

                    [plugins."github@openai-curated"]
                    enabled = true

                    [plugins."browser@openai-bundled"]
                    enabled = true

                    [plugins."streak@openai-curated"]
                    enabled = false

                    [mcp_servers.playwright]
                    command = "npx"
                    args = ["-y", "@playwright/mcp@latest"]
                    url = "http://localhost:4318/v1/tools?token=secret-value"

                    [mcp_servers.playwright.env]
                    PLAYWRIGHT_API_KEY = "top-secret"
                    USER_EMAIL = "user@example.test"

                    [mcp_servers.node_repl]
                    command = "C:\\\\Tools\\\\node_repl.exe"
                    enabled = true

                    [mcp_servers.node_repl.env]
                    CODEX_CLI_PATH = "C:\\\\Tools\\\\codex.exe"
                    BROWSER_USE_AVAILABLE_BACKENDS = "iab"

                    [[skills.config]]
                    path = "C:\\\\Skills\\\\calendar\\\\SKILL.md"
                    enabled = false

                    [[skills.config]]
                    name = "paper-design"
                    enabled = false
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            (root / "AGENTS.md").write_text("# Large agents file\n" + ("A" * 30000), encoding="utf-8")
            (root / "README.md").write_text("# Repo readme\n", encoding="utf-8")
            (ai_root / "README.md").write_text("# AI readme\n", encoding="utf-8")
            (ai_root / "repo_navigation.md").write_text("# Nav\n", encoding="utf-8")
            (ai_root / "project_state.md").write_text("# State\n", encoding="utf-8")
            (ai_root / "policies" / "policy.md").write_text("# Policy\nsecret-value\n?token=abc\n", encoding="utf-8")
            before_after_path.write_text(
                json.dumps(
                    {
                        "baseline": {
                            "selected_turn": {"input_tokens": 21177},
                            "observed_mcp": {"server_count": 13},
                        },
                        "after": {
                            "selected_turn": {"input_tokens": 19024},
                            "observed_mcp": {"server_count": 13},
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            playwright_path.write_text(
                json.dumps(
                    {
                        "selected_turn": {
                            "input_tokens": 21698,
                            "output_tokens": 39,
                            "cached_tokens": 6016,
                            "reasoning_tokens": 31,
                            "tool_tokens": 21737,
                        },
                        "observed_mcp": {
                            "server_count": 3,
                            "servers": ["codex_apps", "node_repl", "playwright"],
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8-sig",
            )
            effective_path.write_text(
                json.dumps(
                    {"counts": {"configured_server_count": 2, "effective_enabled_server_count": 2}},
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            before_after_report.write_text("ok\n", encoding="utf-8")
            playwright_report.write_text("ok\n", encoding="utf-8")
            effective_report.write_text("ok\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--mode",
                    "tool-environment",
                    "--config",
                    str(config_path),
                    "--output-dir",
                    str(out_dir),
                    "--before-after-summary",
                    str(before_after_path),
                    "--playwright-summary",
                    str(playwright_path),
                    "--effective-summary",
                    str(effective_path),
                    "--before-after-report",
                    str(before_after_report),
                    "--playwright-report",
                    str(playwright_report),
                    "--effective-report",
                    str(effective_report),
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)

            summary = json.loads(
                (out_dir / "reports" / "tool_environment_inventory_summary.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["mcp"]["configured_count"], 2)
            self.assertEqual(summary["mcp"]["effective_enabled_count"], 2)
            self.assertEqual(summary["mcp"]["explicit_disabled_count"], 0)
            self.assertEqual(summary["plugins"]["configured_count"], 3)
            self.assertEqual(summary["plugins"]["effective_enabled_count"], 2)
            self.assertEqual(summary["plugins"]["explicit_disabled_count"], 1)
            self.assertIn("github@openai-curated", summary["openai_curated_plugin_candidates"])
            self.assertIn("browser@openai-bundled", [row["name"] for row in summary["plugins"]["plugins"]])
            self.assertIn("node_repl", [row["name"] for row in summary["runtime_internal_candidates"]])
            self.assertIn("codex_apps", [row["name"] for row in summary["runtime_internal_candidates"]])
            self.assertEqual(summary["telemetry_context"]["old_current_a1"]["input_tokens"], 21177)
            self.assertEqual(summary["telemetry_context"]["playwright_only"]["observed_mcp_server_count"], 3)
            self.assertIn("playwright", summary["telemetry_context"]["playwright_only"]["observed_mcp_servers"])
            self.assertIn("skills_and_instructions", summary)
            self.assertEqual(len(summary["skills_and_instructions"]["configured_skill_candidates"]), 2)
            self.assertGreaterEqual(len(summary["skills_and_instructions"]["repo_instruction_files"]), 5)
            self.assertIn("large_agents_md_candidate", summary["skills_and_instructions"]["warnings"])
            self.assertIn("configured_skills_present", summary["skills_and_instructions"]["warnings"])
            self.assertEqual(
                next(
                    row["likely_auto_loaded"]
                    for row in summary["skills_and_instructions"]["repo_instruction_files"]
                    if row["path"] == "AGENTS.md"
                ),
                "yes",
            )
            self.assertEqual(
                next(
                    row["approx_tokens"]
                    for row in summary["skills_and_instructions"]["repo_instruction_files"]
                    if row["path"] == "README.md"
                ),
                4,
            )
            self.assertIn(
                "skills.config[1]",
                [row["section_path"] for row in summary["skills_and_instructions"]["global_instruction_candidates"]],
            )

            features_row = next(
                row for row in summary["other_tool_like_sections"] if row["section_path"] == "features"
            )
            self.assertIn("rmcp_client", features_row["matching_keys"])
            self.assertIn("js_repl", features_row["matching_keys"])

            config_extract = (out_dir / "configs" / "config_tool_environment_sanitized.toml").read_text(encoding="utf-8")
            report_text = (out_dir / "reports" / "tool_environment_inventory_report.md").read_text(encoding="utf-8")
            output_text = summary["interpretation"] + "\n" + config_extract + "\n" + report_text

            self.assertIn("github@openai-curated", output_text)
            self.assertIn("browser@openai-bundled", output_text)
            self.assertIn("codex_apps", output_text)
            self.assertIn("node_repl", output_text)
            self.assertIn("Skills / instructions / auto-loaded context candidates", report_text)
            self.assertIn("AGENTS.md", report_text)
            self.assertIn("13", report_text)
            self.assertIn("3", report_text)
            self.assertNotIn("secret-value", output_text)
            self.assertNotIn("top-secret", output_text)
            self.assertNotIn("user@example.test", output_text)
            self.assertNotIn("?token=", output_text)
            self.assertIn("localhost:4318/v1/tools", output_text)


if __name__ == "__main__":
    unittest.main()
