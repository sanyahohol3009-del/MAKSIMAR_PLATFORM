from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.desktop_screen_observer_contract import (
    DesktopScreenObserverContract,
    FALSE_GATE_KEYS,
    build_desktop_screen_observer_contract,
)


def test_desktop_screen_observer_contract_is_read_only_summary_only() -> None:
    read_model = build_desktop_screen_observer_contract().to_read_model()
    again = build_desktop_screen_observer_contract().to_read_model()

    assert read_model == again
    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["desktop_screen_observer_allowed"] is True
    assert read_model["screenshot_input_allowed"] is True
    assert read_model["screen_summary_allowed"] is True
    assert read_model["model_context_binding_allowed"] is True
    assert read_model["future_pc_action_adapter_requested"] is True
    assert read_model["future_pc_action_requires_allowlist"] is True
    assert read_model["future_pc_action_requires_approval"] is True
    assert read_model["future_pc_action_requires_audit"] is True

    for key in FALSE_GATE_KEYS:
        assert read_model[key] is False


def test_desktop_screen_observer_contract_rejects_dangerous_true_flags() -> None:
    base = build_desktop_screen_observer_contract()
    gates = tuple(
        (key, True if key == "pc_control_allowed" else value)
        for key, value in base.disabled_gates
    )

    with pytest.raises(ValueError, match="must remain disabled"):
        DesktopScreenObserverContract(
            contract_id="desktop_screen_observer_contract_v0_1",
            disabled_gates=gates,
        )


def test_desktop_screen_observer_contract_source_has_no_control_import_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root
        / "MAKSIMAR_CORE_LIB/mobile_screen_observer/desktop_screen_observer_contract.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()
    for marker in (
        "pyautogui",
        "pynput",
        "keyboard.",
        "mouse.",
        "click(",
        "subprocess",
        "os.system",
        "shell=true",
        "webbrowser",
        "socket",
    ):
        assert marker not in lowered

