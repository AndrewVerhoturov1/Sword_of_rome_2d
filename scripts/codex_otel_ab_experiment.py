#!/usr/bin/env python3
"""
Prepare local-only A/B OTel experiment artifacts for Codex turn-cost comparison.
Creates config variants, collector configs, runbook, and compare template.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


OTEL_BLOCK = """
# BEGIN OTEL LOCAL TURN COST TEST
[otel]
environment = "local-turn-cost"
log_user_prompt = false
exporter = { otlp-http = { endpoint = "http://localhost:4318/v1/logs", protocol = "binary" } }
trace_exporter = { otlp-http = { endpoint = "http://localhost:4318/v1/traces", protocol = "binary" } }
metrics_exporter = { otlp-http = { endpoint = "http://localhost:4318/v1/metrics", protocol = "binary" } }
# END OTEL LOCAL TURN COST TEST
""".strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare local Codex OTel A/B turn-cost experiment artifacts.")
    parser.add_argument("--config", required=True, help="Path to live Codex config.toml")
    parser.add_argument("--collector-bin", required=True, help="Path to local otelcol.exe")
    parser.add_argument("--experiment-root", required=True, help="Root directory for local experiment artifacts")
    parser.add_argument("--codex-home", help="Codex home directory. Defaults to parent of config.toml.")
    parser.add_argument("--timestamp", help="Override timestamp label (YYYYMMDD-HHMMSS)")
    return parser.parse_args()


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_otel_block(text: str) -> str:
    lines = normalize_newlines(text).split("\n")
    output: list[str] = []
    skip = False
    for line in lines:
        stripped = line.strip()
        if stripped == "# BEGIN OTEL LOCAL TURN COST TEST":
            skip = True
            continue
        if stripped == "# END OTEL LOCAL TURN COST TEST":
            skip = False
            continue
        if not skip:
            output.append(line)
    return "\n".join(output).rstrip() + "\n"


def strip_mcp_sections(text: str) -> str:
    lines = normalize_newlines(text).split("\n")
    output: list[str] = []
    in_removed_section = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_removed_section = stripped.startswith("[mcp_servers.")
            if in_removed_section:
                continue
        if in_removed_section:
            continue
        output.append(line)

    return "\n".join(output).rstrip() + "\n"


def append_otel_block(text: str) -> str:
    base = strip_otel_block(text).rstrip()
    return f"{base}\n\n{OTEL_BLOCK}\n"


def build_current_config(text: str) -> str:
    return append_otel_block(normalize_newlines(text))


def build_minimal_config(text: str) -> str:
    return append_otel_block(strip_mcp_sections(normalize_newlines(text)))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collector_config_text(raw_file_path: Path) -> str:
    return (
        "receivers:\n"
        "  otlp:\n"
        "    protocols:\n"
        "      grpc:\n"
        "        endpoint: localhost:4317\n"
        "      http:\n"
        "        endpoint: localhost:4318\n"
        "\n"
        "exporters:\n"
        "  file:\n"
        f"    path: {raw_file_path}\n"
        "  debug:\n"
        "    verbosity: basic\n"
        "\n"
        "service:\n"
        "  pipelines:\n"
        "    traces:\n"
        "      receivers: [otlp]\n"
        "      exporters: [file, debug]\n"
        "    logs:\n"
        "      receivers: [otlp]\n"
        "      exporters: [file, debug]\n"
        "    metrics:\n"
        "      receivers: [otlp]\n"
        "      exporters: [file, debug]\n"
    )


def compare_template() -> dict[str, Any]:
    def mode(mode_id: str, config_type: str, tool_turn_id: str) -> dict[str, Any]:
        prefix = "A" if mode_id.startswith("A-") else "B"
        return {
            "mode_id": mode_id,
            "config_type": config_type,
            "fresh_start_confirmed": False,
            "same_session_reliable": None,
            "turns": [
                {
                    "turn_id": f"{prefix}1",
                    "turn_index": 1,
                    "prompt_type": "short_no_tool",
                    "input_tokens": None,
                    "output_tokens": None,
                    "cached_tokens": None,
                    "reasoning_tokens": None,
                    "tool_tokens": None,
                    "cache_ratio": None,
                    "tool_call_status": "none_expected",
                    "tool_mcp_activity": {},
                },
                {
                    "turn_id": f"{prefix}2",
                    "turn_index": 2,
                    "prompt_type": "second_short_no_tool",
                    "input_tokens": None,
                    "output_tokens": None,
                    "cached_tokens": None,
                    "reasoning_tokens": None,
                    "tool_tokens": None,
                    "cache_ratio": None,
                    "tool_call_status": "none_expected",
                    "tool_mcp_activity": {},
                },
                {
                    "turn_id": tool_turn_id,
                    "turn_index": 3,
                    "prompt_type": "safe_tool_call_then_answer",
                    "input_tokens": None,
                    "output_tokens": None,
                    "cached_tokens": None,
                    "reasoning_tokens": None,
                    "tool_tokens": None,
                    "cache_ratio": None,
                    "tool_call_status": "unknown",
                    "tool_mcp_activity": {},
                },
            ],
        }

    return {
        "modes": [
            mode("A-current-config", "current", "A3"),
            mode("B-minimal-config", "minimal_no_mcp", "B3"),
        ],
        "comparisons": {
            "baseline_overhead": {
                "A1_minus_B1_input_tokens": None,
                "interpretation": "",
            },
            "second_turn_cache_effect": {
                "A2_minus_A1_input_tokens": None,
                "A2_minus_A1_cached_tokens": None,
                "B2_minus_B1_input_tokens": None,
                "B2_minus_B1_cached_tokens": None,
                "interpretation": "",
            },
            "tool_turn_overhead": {
                "A3_minus_A2_input_tokens": None,
                "B3_minus_B2_input_tokens": None,
                "interpretation": "",
            },
            "mcp_tool_environment_overhead": {
                "A1_minus_B1_input_tokens": None,
                "A3_minus_B3_input_tokens": None,
                "interpretation": "",
            },
        },
    }


def runbook_text(paths: dict[str, Path], original_sha256: str) -> str:
    return f"""# Codex OTel A/B Turn Cost Experiment

## Goal

Compare two modes in one-session three-turn pattern:

- Mode A: current config
- Mode B: minimal/no MCP config

## Runtime files

- Original config: `{paths["original_config_path"]}`
- Current+OTel config: `{paths["current_config_path"]}`
- Minimal+OTel config: `{paths["minimal_config_path"]}`
- Backup config: `{paths["backup_path"]}`
- A collector config: `{paths["collector_a_config_path"]}`
- B collector config: `{paths["collector_b_config_path"]}`
- Compare template: `{paths["compare_template_path"]}`

Original config SHA256: `{original_sha256}`

## Prompts

### Mode A

- A1: `ответь ровно одним словом: testA1`
- A2: `ответь ровно одним словом: testA2`
- A3: `Сделай один безопасный диагностический вызов инструмента, который не меняет файлы и не раскрывает секреты, например получить текущую рабочую папку или список 5 файлов текущей директории. После вызова инструмента ответь ровно одной строкой: toolA done`

### Mode B

- B1: `ответь ровно одним словом: testB1`
- B2: `ответь ровно одним словом: testB2`
- B3: `Сделай один безопасный диагностический вызов инструмента, который не меняет файлы и не раскрывает секреты, например получить текущую рабочую папку или список 5 файлов текущей директории. После вызова инструмента ответь ровно одной строкой: toolB done`

## STOP POINTS

### STOP POINT 1

backup/config/collector prepared.

### STOP POINT 2

OTel для current config записан.
Нужно вручную полностью перезапустить Codex Desktop/app-server.
Ждать: `continue A run`.

### STOP POINT 3

A1/A2/A3 завершены.
Дальше будет minimal/no MCP config.
Ждать: `continue B config`.

### STOP POINT 4

minimal/no MCP config записан.
Нужно вручную полностью перезапустить Codex Desktop/app-server.
Ждать: `continue B run`.

### STOP POINT 5

B1/B2/B3 завершены.
Нужно восстановить original config.
Ждать: `continue restore config`.

### STOP POINT 6

original config восстановлен, SHA256 проверен.
Нужно вручную перезапустить Codex Desktop/app-server, чтобы он вернулся к original config.
Ждать: `continue final analysis`.
"""


def write_apply_script(path: Path, source_config: Path, target_config: Path) -> None:
    path.write_text(
        "\n".join(
            [
                f"$source = '{source_config}'",
                f"$target = '{target_config}'",
                "Copy-Item -LiteralPath $source -Destination $target -Force",
                "Get-FileHash -Algorithm SHA256 -LiteralPath $target | Format-List",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_restore_script(path: Path, source_config: Path, target_config: Path, expected_sha256: str) -> None:
    path.write_text(
        "\n".join(
            [
                f"$source = '{source_config}'",
                f"$target = '{target_config}'",
                f"$expected = '{expected_sha256}'",
                "Copy-Item -LiteralPath $source -Destination $target -Force",
                "$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $target).Hash.ToLower()",
                "if ($actual -ne $expected) { throw \"SHA256 mismatch after restore\" }",
                "Write-Output \"restore ok\"",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_collector_start_script(path: Path, collector_bin: Path, collector_config: Path, stdout_log: Path, stderr_log: Path) -> None:
    path.write_text(
        "\n".join(
            [
                f"$collector = '{collector_bin}'",
                f"$config = '{collector_config}'",
                f"$stdout = '{stdout_log}'",
                f"$stderr = '{stderr_log}'",
                "Start-Process -FilePath $collector -ArgumentList @('--config', $config) -RedirectStandardOutput $stdout -RedirectStandardError $stderr",
                "",
            ]
        ),
        encoding="utf-8",
    )


def prepare_experiment(
    config_path: Path,
    collector_bin: Path,
    experiment_root: Path,
    codex_home: Path,
    timestamp_label: str | None = None,
) -> dict[str, Any]:
    timestamp = timestamp_label or datetime.now().strftime("%Y%m%d-%H%M%S")
    experiment_dir = experiment_root / f"ab-turn-cost-{timestamp}"
    runtime_dir = codex_home / "tmp" / f"otel-ab-turn-cost-{timestamp}"

    experiment_dir.mkdir(parents=True, exist_ok=True)
    runtime_dir.mkdir(parents=True, exist_ok=True)

    for relative in (
        "A-current-config/raw",
        "A-current-config/parsed",
        "B-minimal-config/raw",
        "B-minimal-config/parsed",
        "compare",
    ):
        (experiment_dir / relative).mkdir(parents=True, exist_ok=True)

    original_bytes = config_path.read_bytes()
    original_text = original_bytes.decode("utf-8")
    original_sha256 = sha256_bytes(original_bytes)

    backup_path = codex_home / f"config.toml.bak-otel-ab-turn-cost-{timestamp}"
    backup_path.write_bytes(original_bytes)

    original_config_path = runtime_dir / "config.original.toml"
    current_config_path = runtime_dir / "config.current-with-otel.toml"
    minimal_config_path = runtime_dir / "config.minimal-no-mcp-with-otel.toml"

    original_config_path.write_bytes(original_bytes)
    current_config_path.write_text(build_current_config(original_text), encoding="utf-8")
    minimal_config_path.write_text(build_minimal_config(original_text), encoding="utf-8")

    raw_a_path = experiment_dir / "A-current-config" / "raw" / "codex-otel.json"
    raw_b_path = experiment_dir / "B-minimal-config" / "raw" / "codex-otel.json"

    collector_a_config_path = runtime_dir / "collector-A-current-config.yaml"
    collector_b_config_path = runtime_dir / "collector-B-minimal-config.yaml"
    collector_a_config_path.write_text(collector_config_text(raw_a_path), encoding="utf-8")
    collector_b_config_path.write_text(collector_config_text(raw_b_path), encoding="utf-8")

    compare_template_path = experiment_dir / "compare" / "compare_summary.template.json"
    compare_template_path.write_text(json.dumps(compare_template(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    compare_report_template_path = experiment_dir / "compare" / "compare_report.template.md"
    compare_report_template_path.write_text(
        "\n".join(
            [
                "# Compare Report",
                "",
                "## Token comparison by turn",
                "",
                "| Mode | Turn | Prompt type | Input | Output | Cached | Reasoning | Tool tokens | Cache ratio | Tool status |",
                "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
                "",
                "## Current vs minimal",
                "",
                "| Comparison | Input delta | Cached delta | Interpretation |",
                "|---|---:|---:|---|",
                "| A1 vs B1: baseline environment overhead |  |  |  |",
                "| A2 vs B2: second-turn environment overhead |  |  |  |",
                "| A3 vs B3: tool-turn environment overhead |  |  |  |",
                "| A2 vs A1: current second-turn/cache effect |  |  |  |",
                "| B2 vs B1: minimal second-turn/cache effect |  |  |  |",
                "| A3 vs A2: current tool-call overhead |  |  |  |",
                "| B3 vs B2: minimal tool-call overhead |  |  |  |",
                "",
                "## Tool/MCP activity by turn",
                "",
                "| Mode | Turn | MCP spans | Tool spans | list_all_tools | transport_worker | tool.call metrics | mcp.call metrics |",
                "|---|---|---:|---:|---:|---:|---:|---:|",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    paths: dict[str, Path] = {
        "backup_path": backup_path,
        "original_config_path": original_config_path,
        "current_config_path": current_config_path,
        "minimal_config_path": minimal_config_path,
        "collector_a_config_path": collector_a_config_path,
        "collector_b_config_path": collector_b_config_path,
        "compare_template_path": compare_template_path,
    }

    runbook_path = experiment_dir / "runbook.md"
    runbook_path.write_text(runbook_text(paths, original_sha256), encoding="utf-8")

    apply_current_script = runtime_dir / "apply-current-config.ps1"
    apply_minimal_script = runtime_dir / "apply-minimal-config.ps1"
    restore_script = runtime_dir / "restore-original-config.ps1"
    write_apply_script(apply_current_script, current_config_path, config_path)
    write_apply_script(apply_minimal_script, minimal_config_path, config_path)
    write_restore_script(restore_script, original_config_path, config_path, original_sha256)

    start_collector_a_script = runtime_dir / "start-collector-A.ps1"
    start_collector_b_script = runtime_dir / "start-collector-B.ps1"
    write_collector_start_script(
        start_collector_a_script,
        collector_bin,
        collector_a_config_path,
        runtime_dir / "collector-A.stdout.log",
        runtime_dir / "collector-A.stderr.log",
    )
    write_collector_start_script(
        start_collector_b_script,
        collector_bin,
        collector_b_config_path,
        runtime_dir / "collector-B.stdout.log",
        runtime_dir / "collector-B.stderr.log",
    )

    manifest = {
        "experiment_id": f"ab-turn-cost-{timestamp}",
        "prepared_at": timestamp,
        "mode_ids": ["A-current-config", "B-minimal-config"],
        "collector_bin": str(collector_bin),
        "live_config_path": str(config_path),
        "backup_path": str(backup_path),
        "original_config_sha256": original_sha256,
        "paths": {
            "experiment_dir": str(experiment_dir),
            "runtime_dir": str(runtime_dir),
            "runbook_path": str(runbook_path),
            "original_config_path": str(original_config_path),
            "current_config_path": str(current_config_path),
            "minimal_config_path": str(minimal_config_path),
            "collector_a_config_path": str(collector_a_config_path),
            "collector_b_config_path": str(collector_b_config_path),
            "compare_template_path": str(compare_template_path),
            "compare_report_template_path": str(compare_report_template_path),
        },
        "stop_points": [
            {"id": "STOP POINT 1", "state": "backup/config/collector prepared."},
            {"id": "STOP POINT 2", "state": "OTel for current config recorded. Wait for continue A run."},
            {"id": "STOP POINT 3", "state": "A1/A2/A3 done. Wait for continue B config."},
            {"id": "STOP POINT 4", "state": "minimal/no MCP config written. Wait for continue B run."},
            {"id": "STOP POINT 5", "state": "B1/B2/B3 done. Wait for continue restore config."},
            {"id": "STOP POINT 6", "state": "original config restored and SHA256 checked. Wait for continue final analysis."},
        ],
    }
    manifest_path = experiment_dir / "experiment_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "experiment_dir": experiment_dir,
        "runtime_dir": runtime_dir,
        "backup_path": backup_path,
        "manifest_path": manifest_path,
        "runbook_path": runbook_path,
        "current_config_path": current_config_path,
        "minimal_config_path": minimal_config_path,
        "original_config_path": original_config_path,
        "collector_a_config_path": collector_a_config_path,
        "collector_b_config_path": collector_b_config_path,
        "compare_template_path": compare_template_path,
        "compare_report_template_path": compare_report_template_path,
        "apply_current_script": apply_current_script,
        "apply_minimal_script": apply_minimal_script,
        "restore_script": restore_script,
        "start_collector_a_script": start_collector_a_script,
        "start_collector_b_script": start_collector_b_script,
    }


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).resolve()
    collector_bin = Path(args.collector_bin).resolve()
    experiment_root = Path(args.experiment_root).resolve()
    codex_home = Path(args.codex_home).resolve() if args.codex_home else config_path.parent

    result = prepare_experiment(
        config_path=config_path,
        collector_bin=collector_bin,
        experiment_root=experiment_root,
        codex_home=codex_home,
        timestamp_label=args.timestamp,
    )
    print(json.dumps({key: str(value) for key, value in result.items()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
