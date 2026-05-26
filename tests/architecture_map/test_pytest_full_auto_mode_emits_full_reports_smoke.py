from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from types import SimpleNamespace

from MAKSIMAR_CORE_LIB.architecture_map import pytest_architecture_plugin


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROOT_CONFTEST = PROJECT_ROOT / "conftest.py"


def _load_root_conftest():
    spec = importlib.util.spec_from_file_location(
        "maksimar_root_conftest_for_full_report_gate_test",
        ROOT_CONFTEST,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class _Config:
    def getoption(self, name: str, default: bool = False) -> bool:
        return default


class _Reporter:
    def __init__(self) -> None:
        self.output: list[str] = []

    def write_sep(self, sep: str, title: str) -> None:
        self.output.append(title)

    def write(self, text: str) -> None:
        self.output.append(text)

    def write_line(self, text: str) -> None:
        self.output.append(text)


def test_pytest_full_auto_mode_emits_full_reports_smoke(monkeypatch) -> None:
    monkeypatch.setenv("MAKSIMAR_FULL_PLATFORM_REPORTS", "1")
    monkeypatch.delenv("PYTEST_XDIST_WORKER", raising=False)

    root_conftest = _load_root_conftest()
    reporter = _Reporter()
    config = _Config()

    assert hasattr(root_conftest, "pytest_terminal_summary")

    def fake_run(*args, **kwargs):
        return SimpleNamespace(returncode=0, stdout="roadmap-next-step-ok\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(
        pytest_architecture_plugin,
        "_render_architecture_radar",
        lambda terminalreporter: terminalreporter.write_line("architecture-radar-ok"),
    )
    monkeypatch.setattr(
        pytest_architecture_plugin,
        "_render_project_xray",
        lambda terminalreporter: terminalreporter.write_line("project-xray-ok"),
    )

    root_conftest.pytest_terminal_summary(reporter, 0, config)
    pytest_architecture_plugin.pytest_terminal_summary(reporter, 0, config)

    rendered = "\n".join(reporter.output)

    assert "MAKSIMAR ROADMAP NEXT STEP" in rendered
    assert "roadmap-next-step-ok" in rendered
    assert "architecture-radar-ok" in rendered
    assert "project-xray-ok" in rendered
