from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "codex_token_cost_normalizer.py"
SPEC = importlib.util.spec_from_file_location("codex_token_cost_normalizer", SCRIPT_PATH)
normalizer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = normalizer
SPEC.loader.exec_module(normalizer)


PRICING = {
    "schema_version": 1,
    "currency": "USD",
    "unit": "per_1m_tokens",
    "prices_per_1m": {
        "gpt-5.5": {"input": 5.0, "cached_input": 0.5, "output": 30.0},
        "gpt-5.4": {"input": 2.5, "cached_input": 0.25, "output": 15.0},
        "gpt-5.4-mini": {"input": 0.75, "cached_input": 0.075, "output": 4.5},
    },
}


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


class TokenCostNormalizerTests(unittest.TestCase):
    def make_fixture(
        self,
        rows: list[dict[str, object]],
        include_optional: bool = False,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        parsed = root / "parsed"
        parsed.mkdir(parents=True)
        write_jsonl(parsed / "token_usage.jsonl", rows)
        write_json(parsed / "session_summary.json", {"source_run_id": "fixture-run"})
        write_jsonl(parsed / "sessions.jsonl", [])
        pricing = root / "token_pricing.json"
        write_json(pricing, PRICING)
        if include_optional:
            write_json(root / "compare_summary.json", {"ok": True})
            write_json(root / "lean_confirmation_summary.json", {"ok": True})
        out_dir = root / "out"
        return temp, root, pricing, out_dir

    def run_normalizer(
        self,
        rows: list[dict[str, object]],
        include_optional: bool = False,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp, root, pricing, out_dir = self.make_fixture(rows, include_optional=include_optional)
        result = normalizer.main(
            ["--input-dir", str(root), "--out-dir", str(out_dir), "--pricing", str(pricing)]
        )
        self.assertEqual(result, 0)
        return temp, out_dir

    def read_turns(self, out_dir: Path) -> list[dict[str, object]]:
        return [
            json.loads(line)
            for line in (out_dir / "token_cost_turns.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def read_sessions(self, out_dir: Path) -> dict[str, object]:
        return json.loads((out_dir / "token_cost_sessions.json").read_text(encoding="utf-8"))

    def read_summary(self, out_dir: Path) -> dict[str, object]:
        return json.loads((out_dir / "token_cost_summary.json").read_text(encoding="utf-8"))

    def test_known_pricing_formula(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "thread-1",
                    "turn_id": "t1",
                    "turn_index": 1,
                    "model": "gpt-5.5",
                    "reasoning_effort": "medium",
                    "input_tokens": 1000,
                    "cached_tokens": 200,
                    "output_tokens": 100,
                    "reasoning_tokens": 7,
                    "tool_tokens": 3,
                }
            ],
            include_optional=True,
        )
        self.addCleanup(temp.cleanup)
        turn = self.read_turns(out_dir)[0]
        self.assertEqual(turn["non_cached_input_tokens"], 800)
        self.assertAlmostEqual(turn["cached_ratio"], 0.2)
        self.assertAlmostEqual(turn["estimated_cost_usd"]["input"], 800 * 5.0 / 1_000_000)
        self.assertAlmostEqual(turn["estimated_cost_usd"]["cached_input"], 200 * 0.5 / 1_000_000)
        self.assertAlmostEqual(turn["estimated_cost_usd"]["output"], 100 * 30.0 / 1_000_000)
        self.assertAlmostEqual(turn["estimated_cost_usd"]["total"], 0.0071)
        self.assertFalse(turn["pricing_unknown"])

    def test_unknown_pricing(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "thread-1",
                    "turn_id": "t1",
                    "model": "gpt-unknown",
                    "input_tokens": 100,
                    "cached_tokens": 10,
                    "output_tokens": 20,
                }
            ]
        )
        self.addCleanup(temp.cleanup)
        turn = self.read_turns(out_dir)[0]
        self.assertTrue(turn["pricing_unknown"])
        self.assertIsNone(turn["prices_per_1m"])
        self.assertIsNone(turn["estimated_cost_usd"]["total"])
        self.assertTrue(any("pricing is unknown" in warning for warning in turn["warnings"]))

    def test_cached_greater_than_input_warns_and_clamps(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "thread-1",
                    "turn_id": "t1",
                    "model": "gpt-5.5",
                    "input_tokens": 100,
                    "cached_tokens": 150,
                    "output_tokens": 10,
                }
            ]
        )
        self.addCleanup(temp.cleanup)
        turn = self.read_turns(out_dir)[0]
        self.assertEqual(turn["non_cached_input_tokens"], 0)
        self.assertAlmostEqual(turn["cached_ratio"], 1.5)
        self.assertTrue(any("cached_tokens is greater" in warning for warning in turn["warnings"]))

    def test_same_thread_session_aggregation(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "same",
                    "turn_id": "t1",
                    "model": "gpt-5.5",
                    "reasoning_effort": "low",
                    "input_tokens": 100,
                    "cached_tokens": 10,
                    "output_tokens": 5,
                    "reasoning_tokens": 1,
                    "tool_tokens": 0,
                },
                {
                    "thread_id": "same",
                    "turn_id": "t2",
                    "model": "gpt-5.5",
                    "reasoning_effort": "low",
                    "input_tokens": 200,
                    "cached_tokens": 40,
                    "output_tokens": 15,
                    "reasoning_tokens": 2,
                    "tool_tokens": 3,
                },
            ],
            include_optional=True,
        )
        self.addCleanup(temp.cleanup)
        sessions = self.read_sessions(out_dir)["sessions"]
        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertEqual(session["turn_count"], 2)
        self.assertEqual(session["total_input_tokens"], 300)
        self.assertEqual(session["total_cached_tokens"], 50)
        self.assertEqual(session["total_non_cached_input_tokens"], 250)
        self.assertEqual(session["total_output_tokens"], 20)
        self.assertEqual(session["total_reasoning_tokens"], 3)
        self.assertEqual(session["total_tool_tokens"], 3)
        self.assertFalse(session["model_switch_detected"])
        self.assertFalse(session["reasoning_switch_detected"])

    def test_model_switch_in_same_thread(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "same",
                    "turn_id": "t1",
                    "model": "gpt-5.5",
                    "reasoning_effort": "low",
                    "input_tokens": 100,
                    "cached_tokens": 10,
                    "output_tokens": 5,
                },
                {
                    "thread_id": "same",
                    "turn_id": "t2",
                    "model": "gpt-5.4",
                    "reasoning_effort": "low",
                    "input_tokens": 100,
                    "cached_tokens": 10,
                    "output_tokens": 5,
                },
            ],
            include_optional=True,
        )
        self.addCleanup(temp.cleanup)
        session = self.read_sessions(out_dir)["sessions"][0]
        self.assertTrue(session["model_switch_detected"])
        self.assertIn("gpt-5.5", session["models"])
        self.assertIn("gpt-5.4", session["models"])
        self.assertTrue(any("model switch" in warning for warning in session["warnings"]))

    def test_missing_optional_files_without_crash(self) -> None:
        temp, out_dir = self.run_normalizer(
            [
                {
                    "thread_id": "thread-1",
                    "turn_id": "t1",
                    "model": "gpt-5.5",
                    "input_tokens": 10,
                    "cached_tokens": 0,
                    "output_tokens": 1,
                }
            ],
            include_optional=False,
        )
        self.addCleanup(temp.cleanup)
        summary = self.read_summary(out_dir)
        self.assertEqual(summary["turn_count"], 1)
        self.assertTrue(any("optional file" in warning for warning in summary["warnings"]))


if __name__ == "__main__":
    unittest.main()
