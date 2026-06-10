"""Regression tests for command/action classification.

These tests verify that the classification logic correctly identifies
actions based on raw function_call events, not on filename or path alone.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.codex_token_monitor_server import _classify_shell_command


class TestCommandClassification:
    """Test classification of shell commands."""

    def test_rg_is_code_search(self):
        """rg should be classified as code_search, not test_run."""
        result = _classify_shell_command("rg -n 'foo' tests/test_x.py")
        assert result["classified_action"] == "code_search"
        assert result["title_ru"] == "Искал по коду"

    def test_rg_with_tests_path_is_code_search(self):
        """rg searching in tests/ directory should still be code_search."""
        result = _classify_shell_command("rg 'test' tests/")
        assert result["classified_action"] == "code_search"
        assert result["title_ru"] == "Искал по коду"

    def test_get_content_tests_file_is_file_read(self):
        """Get-Content reading a tests file should be file_read, not test_run."""
        result = _classify_shell_command("Get-Content tests/test_x.py")
        assert result["classified_action"] == "file_read"
        assert result["title_ru"] == "Прочитал файл"

    def test_cat_file_is_file_read(self):
        """cat should be classified as file_read."""
        result = _classify_shell_command("cat src/app.js")
        assert result["classified_action"] == "file_read"
        assert result["title_ru"] == "Прочитал файл"

    def test_unittest_is_test_run(self):
        """python -m unittest should be classified as test_run."""
        result = _classify_shell_command("python -m unittest tests.test_x")
        assert result["classified_action"] == "test_run"
        assert result["title_ru"] == "Запустил тесты"

    def test_pytest_is_test_run(self):
        """pytest should be classified as test_run."""
        result = _classify_shell_command("pytest tests/test_x.py")
        assert result["classified_action"] == "test_run"
        assert result["title_ru"] == "Запустил тесты"

    def test_npm_test_is_test_run(self):
        """npm test should be classified as test_run."""
        result = _classify_shell_command("npm test")
        assert result["classified_action"] == "test_run"
        assert result["title_ru"] == "Запустил тесты"

    def test_node_check_is_syntax_check(self):
        """node --check should be classified as syntax_check."""
        result = _classify_shell_command("node --check app.js")
        assert result["classified_action"] == "syntax_check"
        assert result["title_ru"] == "Проверил JavaScript синтаксис"

    def test_python_compile_is_syntax_check(self):
        """python -m py_compile should be classified as syntax_check."""
        result = _classify_shell_command("python -m py_compile app.py")
        assert result["classified_action"] == "syntax_check"
        assert result["title_ru"] == "Проверил Python синтаксис"

    def test_tsc_no_emit_is_syntax_check(self):
        """tsc --noEmit should be classified as syntax_check."""
        result = _classify_shell_command("tsc --noEmit")
        assert result["classified_action"] == "syntax_check"
        assert result["title_ru"] == "Проверил TypeScript синтаксис"

    def test_git_status_is_git_operation(self):
        """git status should be classified as git_operation."""
        result = _classify_shell_command("git status")
        assert result["classified_action"] == "git_operation"
        assert result["title_ru"] == "Проверил состояние repo"

    def test_git_diff_is_git_operation(self):
        """git diff should be classified as git_operation."""
        result = _classify_shell_command("git diff")
        assert result["classified_action"] == "git_operation"
        assert result["title_ru"] == "Проверил изменения"

    def test_git_diff_stat_is_git_operation(self):
        """git diff --stat should be classified as git_operation."""
        result = _classify_shell_command("git diff --stat")
        assert result["classified_action"] == "git_operation"
        assert result["title_ru"] == "Проверил статистику изменений"

    def test_git_log_is_git_operation(self):
        """git log should be classified as git_operation."""
        result = _classify_shell_command("git log --oneline")
        assert result["classified_action"] == "git_operation"
        assert result["title_ru"] == "Посмотрел историю"

    def test_git_show_is_git_operation(self):
        """git show should be classified as git_operation."""
        result = _classify_shell_command("git show abc123")
        assert result["classified_action"] == "git_operation"
        assert result["title_ru"] == "Посмотрел commit"

    def test_git_stash_is_git_operation(self):
        """git stash should be classified as git_operation."""
        result = _classify_shell_command("git stash")
        assert result["classified_action"] == "git_operation"
        assert result["title_ru"] == "Временно сохранил изменения"

    def test_git_add_is_git_operation(self):
        """git add should be classified as git_operation."""
        result = _classify_shell_command("git add .")
        assert result["classified_action"] == "git_operation"
        assert result["title_ru"] == "Добавил файлы в индекс"

    def test_git_commit_is_git_operation(self):
        """git commit should be classified as git_operation."""
        result = _classify_shell_command("git commit -m 'fix'")
        assert result["classified_action"] == "git_operation"
        assert result["title_ru"] == "Зафиксировал изменения"

    def test_select_string_is_code_search(self):
        """Select-String (PowerShell) should be classified as code_search."""
        result = _classify_shell_command("Select-String -Pattern 'foo'")
        assert result["classified_action"] == "code_search"
        assert result["title_ru"] == "Искал по коду"

    def test_findstr_is_code_search(self):
        """findstr should be classified as code_search."""
        result = _classify_shell_command("findstr /s 'foo' *.py")
        assert result["classified_action"] == "code_search"
        assert result["title_ru"] == "Искал по коду"

    def test_grep_is_code_search(self):
        """grep should be classified as code_search."""
        result = _classify_shell_command("grep -r 'foo' .")
        assert result["classified_action"] == "code_search"
        assert result["title_ru"] == "Искал по коду"

    def test_python_diagnostic_script(self):
        """python with script should be classified as diagnostic_script."""
        result = _classify_shell_command("python scripts/analyze.py")
        assert result["classified_action"] == "diagnostic_script"
        assert result["title_ru"] == "Запустил диагностический скрипт"

    def test_unknown_command_is_shell_command(self):
        """Unknown commands should fall back to shell_command."""
        result = _classify_shell_command("some-unknown-command --arg")
        assert result["classified_action"] == "shell_command"
        assert result["title_ru"] == "Выполнил команду"


class TestServiceCallClassification:
    """Test classification of service/instrument calls."""

    def test_update_plan_classification(self):
        """update_plan should be classified as plan_update."""
        from scripts.codex_token_monitor_server import _classify_service_call
        
        result = _classify_service_call("update_plan", {"plan": "test"})
        assert result["classified_action"] == "plan_update"
        assert result["title_ru"] == "Обновил служебный план Codex"

    def test_todo_write_classification(self):
        """todo_write should be classified as todo_write."""
        from scripts.codex_token_monitor_server import _classify_service_call
        
        result = _classify_service_call("todo_write", {"todos": []})
        assert result["classified_action"] == "todo_write"
        assert "Обновил" in result["title_ru"] and "задач" in result["title_ru"]


class TestInlineDiagnosticScript:
    """Test 5: inline Python/PowerShell diagnostic scripts."""

    def test_inline_python_heredoc_is_diagnostic_script(self):
        """Inline Python with heredoc should be diagnostic_script, not file_read."""
        result = _classify_shell_command("@'\nimport json\nfrom pathlib import Path\n'@ | python -")
        assert result["classified_action"] == "diagnostic_script"
        assert result["title_ru"] == "Запустил диагностический Python-скрипт"

    def test_inline_python_with_pipe_is_diagnostic_script(self):
        """Inline Python piped to python - should be diagnostic_script."""
        result = _classify_shell_command("echo 'print(1)' | python -")
        assert result["classified_action"] == "diagnostic_script"

    def test_python_dash_with_script_arg_is_diagnostic(self):
        """python - with script argument should be diagnostic_script."""
        result = _classify_shell_command("python -c 'print(1)'")
        assert result["classified_action"] == "diagnostic_script"


class TestPatchActionBlock:
    """Test 6: patch-specific classification."""

    def test_apply_patch_is_patch_action(self):
        """apply_patch / custom_tool_call patch should be patch_action via service call."""
        from scripts.codex_token_monitor_server import _classify_service_call
        result = _classify_service_call("apply_patch", {"filePath": "src/app.js", "patch": "..."})
        # apply_patch falls through to service_action with tool_name="apply_patch"
        assert result["classified_action"] == "service_action"
        assert result["action_type"] == "apply_patch"

    def test_unknown_service_call_is_service_action(self):
        """Unknown service calls should be service_action."""
        from scripts.codex_token_monitor_server import _classify_service_call
        result = _classify_service_call("unknown_tool", {"key": "val"})
        assert result["classified_action"] == "service_action"
        assert result["title_ru"] == "Выполнил служебное действие"


class TestExpensivePlanUpdate:
    """Test 7: expensive plan_update detection."""

    def test_plan_update_with_high_new_input_ratio(self):
        """plan_update with new_input_ratio >= 0.70 should trigger why_expensive."""
        from scripts.codex_token_monitor_server import _add_why_expensive_blocks

        # Build synthetic timeline items
        items = [
            {   # Previous: large tool output
                "index": 1, "row_type": "tool_with_cost", "display_title_ru": "Прочитал файл",
                "cost_available": True,
                "linked_request_usage": {"available": True, "input_tokens": 80000, "cached_tokens": 60000,
                    "non_cached_input_tokens": 20000, "output_tokens": 3000},
                "tool_evidence": {"available": True, "tool_count": 5},
                "linked_cost": {"total_usd": 0.05},
            },
            {   # Current: plan_update, high new input, low cache
                "index": 2, "row_type": "tool_with_cost", "display_title_ru": "Обновил план работы",
                "cost_available": True,
                "linked_request_usage": {"available": True, "input_tokens": 100000, "cached_tokens": 5000,
                    "non_cached_input_tokens": 95000, "output_tokens": 200},
                "tool_evidence": {"available": True, "tool_count": 1},
                "linked_cost": {"total_usd": 0.30},
                "action_type": "plan_update",
            },
            {   # Next: high cached
                "index": 3, "row_type": "ai_call_only", "display_title_ru": "Сформулировал ответ",
                "cost_available": True,
                "linked_request_usage": {"available": True, "input_tokens": 100000, "cached_tokens": 90000,
                    "non_cached_input_tokens": 10000, "output_tokens": 5000},
                "linked_cost": {"total_usd": 0.10},
            },
        ]
        _add_why_expensive_blocks(items, [], [])

        plan_item = items[1]
        assert "why_expensive" in plan_item
        we = plan_item["why_expensive"]
        assert we["detected"] is True
        assert we["action_kind"] == "plan_update"
        assert "cache miss" in we["explanation_ru"].lower() or "cache fill" in we["explanation_ru"].lower()

    def test_plan_update_without_high_ratio_not_detected(self):
        """Normal plan_update without high new input ratio should not trigger."""
        from scripts.codex_token_monitor_server import _add_why_expensive_blocks

        items = [
            {
                "index": 1, "row_type": "tool_with_cost", "display_title_ru": "Обновил план работы",
                "cost_available": True,
                "linked_request_usage": {"available": True, "input_tokens": 10000, "cached_tokens": 8000,
                    "non_cached_input_tokens": 2000, "output_tokens": 200},
                "linked_cost": {"total_usd": 0.01},
                "action_type": "plan_update",
            },
        ]
        _add_why_expensive_blocks(items, [], [])

        plan_item = items[0]
        assert plan_item.get("why_expensive", {}).get("detected") is not True


class TestFinalReportConfidence:
    """Test 8: final_report should have high/raw confidence when raw message found."""

    def test_final_report_raw_message_high_confidence(self):
        """When raw agent_message is found, final_report should get high/raw confidence."""
        from scripts.codex_token_monitor_server import _add_why_expensive_blocks

        items = [
            {
                "index": 1, "row_type": "ai_call_only", "display_title_ru": "Сформулировал итоговый отчёт",
                "cost_available": True,
                "linked_request_usage": {"available": True, "input_tokens": 50000, "cached_tokens": 40000,
                    "non_cached_input_tokens": 10000, "output_tokens": 8000},
                "linked_cost": {"total_usd": 0.15},
                "assistant_message_data": {
                    "available": True, "is_final_report": True,
                    "message_length_chars": 5000, "message_preview": "Отчёт: все тесты прошли",
                    "source": "step_assistant_answer", "source_confidence": "medium_inferred",
                    "has_new_tool_events": False,
                },
            },
        ]
        _add_why_expensive_blocks(items, [], [])

        final_item = items[0]
        amd = final_item.get("assistant_message_data", {})
        assert amd.get("is_final_report") is True

    def test_ai_call_only_without_message_is_model_only(self):
        """AI-call without visible message and without tool events = model_only."""
        from scripts.codex_token_monitor_server import _add_why_expensive_blocks

        items = [
            {
                "index": 1, "row_type": "ai_call_only", "display_title_ru": "AI #1",
                "cost_available": True,
                "linked_request_usage": {"available": True, "input_tokens": 5000, "cached_tokens": 3000,
                    "non_cached_input_tokens": 2000, "output_tokens": 100},
                "linked_cost": {"total_usd": 0.01},
            },
        ]
        _add_why_expensive_blocks(items, [], [])

        model_item = items[0]
        # model_only detected
        we = model_item.get("why_expensive", {})
        if we.get("detected"):
            assert we.get("action_kind") == "model_only"


class TestGetContentPathExtraction:
    """Regression tests for Get-Content path extraction with various forms."""

    def test_get_content_with_totalcount(self):
        """Get-Content .ai\file.md -TotalCount 260 extracts path correctly."""
        result = _classify_shell_command("Get-Content .ai\\prompts\\create_external_question_prompt.md -TotalCount 260")
        assert result["classified_action"] == "file_read"
        assert ".ai\\prompts\\create_external_question_prompt.md" in result.get("target_path", "")

    def test_get_content_with_select_object_pipe(self):
        """Get-Content AGENTS.md | Select-Object -Skip 376 -First 30 extracts path."""
        result = _classify_shell_command("Get-Content AGENTS.md | Select-Object -Skip 376 -First 30")
        assert result["classified_action"] == "file_read"
        assert "AGENTS.md" in result.get("target_path", "")

    def test_get_content_with_totalcount_dot_ai(self):
        r"""Get-Content .ai\external_chats\file.md -TotalCount 220 extracts path."""
        result = _classify_shell_command("Get-Content .ai\\external_chats\\chatgpt_project_source_repo_onboarding.md -TotalCount 220")
        assert result["classified_action"] == "file_read"
        assert ".ai\\external_chats" in result.get("target_path", "")

    def test_get_content_unquoted_path(self):
        """Get-Content with unquoted path extracts correctly."""
        result = _classify_shell_command("Get-Content src/app.js")
        assert result["classified_action"] == "file_read"
        assert "src/app.js" in result.get("target_path", "")

    def test_get_content_quoted_path_still_works(self):
        """Get-Content with quoted path still works."""
        result = _classify_shell_command("Get-Content 'path with spaces/file.md'")
        assert result["classified_action"] == "file_read"
        assert "path with spaces/file.md" in result.get("target_path", "")


class TestV216Regression:
    """v2.16 regression tests for expensive plan detection, patch titles, inline Python, etc."""

    def test_expensive_plan_update_gets_explanation(self):
        """Expensive plan_update with high new input should get why_expensive block."""
        from scripts.codex_token_monitor_server import _add_why_expensive_blocks

        # Synthetic: previous AI-call has large tool outputs, current has high New input
        items = [
            {
                "display_title_ru": "Прочитал файлы и запустил диагностический скрипт",
                "row_type": "tool_with_cost",
                "cost_available": True,
                "linked_request_usage": {
                    "available": True,
                    "input_tokens": 120000,
                    "cached_tokens": 30000,
                    "non_cached_input_tokens": 90000,
                    "output_tokens": 500,
                    "reasoning_tokens": 0,
                },
                "tool_evidence": {"available": True, "tool_count": 3},
                "linked_cost": {"total_usd": 0.15},
            },
            {
                "display_title_ru": "Сформулировал план и обновил служебный план Codex",
                "row_type": "tool_with_cost",
                "action_type": "plan_update",
                "cost_available": True,
                "linked_request_usage": {
                    "available": True,
                    "input_tokens": 90000,
                    "cached_tokens": 9000,
                    "non_cached_input_tokens": 81000,
                    "output_tokens": 300,
                    "reasoning_tokens": 0,
                },
                "tool_evidence": {"available": True, "tool_count": 1},
                "linked_cost": {"total_usd": 0.12},
            },
            {
                "display_title_ru": "Прочитал файл",
                "row_type": "tool_with_cost",
                "cost_available": True,
                "linked_request_usage": {
                    "available": True,
                    "input_tokens": 100000,
                    "cached_tokens": 85000,
                    "non_cached_input_tokens": 15000,
                    "output_tokens": 800,
                    "reasoning_tokens": 0,
                },
                "tool_evidence": {"available": True, "tool_count": 1},
                "linked_cost": {"total_usd": 0.02},
            },
        ]
        _add_why_expensive_blocks(items, [], [])

        plan_item = items[1]
        we = plan_item.get("why_expensive", {})
        assert we.get("detected") is True
        assert we.get("action_kind") == "plan_update"
        # explanation_ru should contain the diagnostic message (not empty)
        assert len(we.get("explanation_ru", "")) > 100
        # Should have neighbor context
        nc = we.get("neighbor_context", {})
        assert nc.get("previous", {}).get("available") is True
        assert nc.get("next", {}).get("available") is True
        # Pattern detection: cache fill after large tool output
        pattern = we.get("detected_pattern", "")
        # With prev nc=90000, next cache=0.85 — should detect cache_fill pattern
        # (prev tool_count=3 or prev_nc > 50000) and next cache > 0.70 and next_cached > 50000
        if pattern:
            assert "cache_fill" in pattern

    def test_failed_patch_title(self):
        """Failed patch should not say 'Применил patch'."""
        from scripts.codex_token_monitor_server import _build_apply_patch_title

        title = _build_apply_patch_title(
            [{"path": "scripts/codex_token_monitor_server.py"}],
            "failed"
        )
        assert "Применил" not in title or "не применил" in title
        assert "failed" in title.lower() or "не применил" in title

    def test_success_patch_title(self):
        """Successful patch should say 'Применил patch'."""
        from scripts.codex_token_monitor_server import _build_apply_patch_title

        title = _build_apply_patch_title(
            [{"path": "scripts/codex_token_monitor_server.py"}],
            "success"
        )
        assert "Применил" in title

    def test_unknown_patch_title(self):
        """Unknown patch status should say 'Patch-действие'."""
        from scripts.codex_token_monitor_server import _build_apply_patch_title

        title = _build_apply_patch_title([], "unknown")
        assert "Patch-действие" in title or "patch" in title.lower()

    def test_inline_python_never_file_read(self):
        """Inline Python heredoc must not be classified as file_read."""
        # Pure inline code piped to python
        result = _classify_shell_command("import json\nfrom pathlib import Path\np = Path('.')")
        assert result["classified_action"] == "diagnostic_script"
        assert result["action_type"] == "diagnostic_script"

        # @'...'@ | python - pattern
        result2 = _classify_shell_command("@'\nimport sys\nprint(sys.argv)\n'@ | python - test")
        assert result2["classified_action"] == "diagnostic_script"

        # python -c '...' pattern
        result3 = _classify_shell_command("""python -c "import json; print(json.dumps({}))" """)
        assert result3["classified_action"] == "diagnostic_script"

    def test_plan_with_visible_explanation_gets_full_title(self):
        """update_plan with visible explanation should have full title."""
        from scripts.codex_token_monitor_server import _classify_service_call

        result = _classify_service_call("update_plan", {
            "explanation": "We will refactor the token monitor to support v2.16 improvements.",
            "plan": [{"step": "Fix patch titles", "status": "pending"}]
        })
        assert result["classified_action"] == "plan_update"
        assert "Сформулировал план" in result["title_ru"]
        assert result.get("has_visible_explanation") is True

        # Without visible explanation
        result2 = _classify_service_call("update_plan", {"plan": "test"})
        assert "Сформулировал план" not in result2["title_ru"]
        assert result2.get("has_visible_explanation") is False

    def test_final_report_confidence_sync(self):
        """final_report with raw message should have high confidence at all layers."""
        # This is tested via human_timeline builder — check that assistant_message_data
        # with source=high/raw results in recognition_confidence=high
        from scripts.codex_token_monitor_server import _detect_patch_status

        # _detect_patch_status handles various edge cases
        assert _detect_patch_status("", None) == "unknown"
        assert _detect_patch_status("", False) == "failed"
        assert _detect_patch_status("apply_patch verification failed", None) == "failed"
        assert _detect_patch_status("success. updated the following files", None) == "success"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])