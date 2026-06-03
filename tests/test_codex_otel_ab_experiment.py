from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.codex_otel_ab_experiment import (
    build_current_config,
    build_minimal_config,
    prepare_experiment,
    strip_mcp_sections,
)


SAMPLE_CONFIG = """model = "gpt-5.5"

[plugins."github@openai-curated"]
enabled = true

[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"

[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest"]

[mcp_servers.playwright.tools.browser_evaluate]
approval_mode = "approve"

[desktop]
localeOverride = "ru-RU"
"""


class CodexOtelAbExperimentTest(unittest.TestCase):
    def test_strip_mcp_sections_removes_all_mcp_blocks(self) -> None:
        stripped = strip_mcp_sections(SAMPLE_CONFIG)

        self.assertNotIn("[mcp_servers.context7]", stripped)
        self.assertNotIn("[mcp_servers.playwright]", stripped)
        self.assertNotIn("[mcp_servers.playwright.tools.browser_evaluate]", stripped)
        self.assertIn('[plugins."github@openai-curated"]', stripped)
        self.assertIn("[desktop]", stripped)

    def test_build_current_and_minimal_configs_append_localhost_otel(self) -> None:
        current_config = build_current_config(SAMPLE_CONFIG)
        minimal_config = build_minimal_config(SAMPLE_CONFIG)

        self.assertIn('[otel]', current_config)
        self.assertIn('http://localhost:4318/v1/traces', current_config)
        self.assertIn('http://localhost:4318/v1/logs', current_config)
        self.assertIn('http://localhost:4318/v1/metrics', current_config)
        self.assertIn('log_user_prompt = false', current_config)

        self.assertIn('[otel]', minimal_config)
        self.assertNotIn('[mcp_servers.context7]', minimal_config)
        self.assertNotIn('[mcp_servers.playwright]', minimal_config)
        self.assertNotIn('[mcp_servers.playwright.tools.browser_evaluate]', minimal_config)

    def test_prepare_experiment_writes_expected_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            codex_home = root / "codex-home"
            codex_home.mkdir(parents=True)
            config_path = codex_home / "config.toml"
            config_path.write_text(SAMPLE_CONFIG, encoding="utf-8")

            collector_bin = root / "otelcol.exe"
            collector_bin.write_text("fake-binary", encoding="utf-8")

            experiment_root = root / "repo-local"
            experiment_root.mkdir()

            result = prepare_experiment(
                config_path=config_path,
                collector_bin=collector_bin,
                experiment_root=experiment_root,
                codex_home=codex_home,
                timestamp_label="20260604-120000",
            )

            self.assertTrue(result["experiment_dir"].exists())
            self.assertTrue(result["runtime_dir"].exists())
            self.assertTrue(result["backup_path"].exists())
            self.assertEqual(config_path.read_bytes(), Path(result["backup_path"]).read_bytes())
            self.assertEqual(config_path.read_bytes(), Path(result["original_config_path"]).read_bytes())

            current_cfg = Path(result["current_config_path"]).read_text(encoding="utf-8")
            minimal_cfg = Path(result["minimal_config_path"]).read_text(encoding="utf-8")
            self.assertIn("http://localhost:4318/v1/traces", current_cfg)
            self.assertNotIn("[mcp_servers.context7]", minimal_cfg)

            manifest = json.loads(Path(result["manifest_path"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["mode_ids"], ["A-current-config", "B-minimal-config"])
            self.assertEqual(manifest["stop_points"][0]["id"], "STOP POINT 1")

            compare = json.loads(Path(result["compare_template_path"]).read_text(encoding="utf-8"))
            self.assertEqual(compare["modes"][0]["mode_id"], "A-current-config")
            self.assertEqual(compare["modes"][1]["mode_id"], "B-minimal-config")


if __name__ == "__main__":
    unittest.main()
