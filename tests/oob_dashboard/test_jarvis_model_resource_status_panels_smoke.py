from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_model_status_panel_contract import (
    build_jarvis_model_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_resource_status_panel_contract import (
    build_jarvis_resource_status_panel_contract,
)


def test_jarvis_model_status_panel_is_blocked_without_selected_model() -> None:
    panel = build_jarvis_model_status_panel_contract().to_read_model()

    assert panel["model_selected"] is False
    assert panel["selected_model_role"] == ""
    assert panel["selected_model_id"] == ""
    assert panel["model_download_allowed"] is False
    assert panel["model_runtime_allowed"] is False
    assert panel["model_download_status"] == "blocked"
    assert panel["model_runtime_status"] == "blocked"
    assert panel["dashboard_execution_allowed"] is False


def test_jarvis_resource_status_panel_does_not_poll_hardware() -> None:
    panel = build_jarvis_resource_status_panel_contract().to_read_model()

    assert panel["gpu_status"] == "unknown"
    assert panel["ram_status"] == "unknown"
    assert panel["gpu_pressure_status"] == "not_polled"
    assert panel["ram_pressure_status"] == "not_polled"
    assert panel["resource_snapshot_available"] is False
    assert panel["resource_polling_enabled"] is False
    assert panel["model_download_allowed"] is False
    assert panel["runtime_start_allowed"] is False


def test_resource_status_panel_source_has_no_hardware_runtime_imports() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root / "MAKSIMAR_CORE_LIB/oob_dashboard/jarvis_resource_status_panel_contract.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()

    for marker in (
        "psutil",
        "gputil",
        "nvidia_smi",
        "subprocess",
        "os.system",
        "torch",
        "cuda",
        "shell=true",
    ):
        assert marker not in lowered

