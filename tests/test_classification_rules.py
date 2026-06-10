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
        assert result["title_ru"] == "Обновил план работы"

    def test_todo_write_classification(self):
        """todo_write should be classified as todo_write."""
        from scripts.codex_token_monitor_server import _classify_service_call
        
        result = _classify_service_call("todo_write", {"todos": []})
        assert result["classified_action"] == "todo_write"
        assert "Обновил" in result["title_ru"] and "задач" in result["title_ru"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])