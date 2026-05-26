from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map.pytest_report_gate import (
    get_pytest_report_gate_decision,
    is_maksimar_full_platform_report_enabled,
)


class _Config:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def getoption(self, name: str, default: bool = False) -> bool:
        if name == "maksimar_full_platform_reports":
            return self.enabled
        return default


def test_pytest_report_gate_env_contract_smoke(monkeypatch) -> None:
    monkeypatch.delenv("MAKSIMAR_FULL_PLATFORM_REPORTS", raising=False)

    disabled = get_pytest_report_gate_decision(_Config(False))
    assert disabled.full_reports_enabled is False
    assert disabled.source == "disabled"
    assert is_maksimar_full_platform_report_enabled(_Config(False)) is False

    option_enabled = get_pytest_report_gate_decision(_Config(True))
    assert option_enabled.full_reports_enabled is True
    assert option_enabled.source == "pytest_option"

    monkeypatch.setenv("MAKSIMAR_FULL_PLATFORM_REPORTS", "1")
    env_enabled = get_pytest_report_gate_decision(_Config(False))
    assert env_enabled.full_reports_enabled is True
    assert env_enabled.source == "env"
