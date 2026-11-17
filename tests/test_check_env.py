from collections import namedtuple
from types import SimpleNamespace

import pytest

from ailab import check_env

VersionInfo = namedtuple("VersionInfo", "major minor micro")


def test_check_python_accepts_minimum_supported_version(monkeypatch):
    monkeypatch.setattr(check_env.sys, "version_info", VersionInfo(3, 10, 0))
    assert check_env.check_python().status == "ok"


def test_check_python_rejects_older_version(monkeypatch):
    monkeypatch.setattr(check_env.sys, "version_info", VersionInfo(3, 9, 9))
    result = check_env.check_python()
    assert result.status == "error"
    assert "3.10" in result.message


def test_virtual_environment_uses_python_prefixes(monkeypatch):
    monkeypatch.setattr(check_env.sys, "prefix", "/project/.venv")
    monkeypatch.setattr(check_env.sys, "base_prefix", "/python")
    assert check_env.check_virtual_environment().status == "ok"

    monkeypatch.setattr(check_env.sys, "prefix", "/python")
    assert check_env.check_virtual_environment().status == "warn"


@pytest.mark.parametrize(("found", "expected"), [("/usr/bin/git", "ok"), (None, "warn")])
def test_check_git_reports_command_availability(monkeypatch, found, expected):
    monkeypatch.setattr(check_env.shutil, "which", lambda _: found)
    assert check_env.check_git().status == expected


def test_check_package_reports_import_success(monkeypatch):
    monkeypatch.setattr(check_env.importlib, "import_module", lambda _: object())
    assert check_env.check_package("sample").status == "ok"


def test_check_package_reports_missing_import(monkeypatch):
    def missing(_):
        raise ImportError("not installed")

    monkeypatch.setattr(check_env.importlib, "import_module", missing)
    assert check_env.check_package("sample").status == "error"


def test_gpu_check_reports_missing_nvidia_tool(monkeypatch):
    monkeypatch.setattr(check_env.shutil, "which", lambda _: None)
    assert check_env.check_nvidia_gpu().status == "info"


def test_gpu_check_reports_name_from_nvidia_tool(monkeypatch):
    monkeypatch.setattr(check_env.shutil, "which", lambda _: "/usr/bin/nvidia-smi")
    monkeypatch.setattr(
        check_env.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(stdout="Example GPU\n"),
    )
    result = check_env.check_nvidia_gpu()
    assert result.status == "ok"
    assert "Example GPU" in result.message


def test_gpu_check_handles_query_timeout(monkeypatch):
    monkeypatch.setattr(check_env.shutil, "which", lambda _: "/usr/bin/nvidia-smi")

    def timeout(*args, **kwargs):
        raise check_env.subprocess.TimeoutExpired("nvidia-smi", 5)

    monkeypatch.setattr(check_env.subprocess, "run", timeout)
    assert check_env.check_nvidia_gpu().status == "info"


def test_main_returns_error_code_when_required_check_fails(monkeypatch, capsys):
    monkeypatch.setattr(
        check_env,
        "run_checks",
        lambda: [check_env.CheckResult("error", "missing package")],
    )
    assert check_env.main() == 1
    assert "[error] missing package" in capsys.readouterr().out
