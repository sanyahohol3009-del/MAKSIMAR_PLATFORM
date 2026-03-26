from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    detect_node_hardware,
)


def test_hardware_detection_adapter_builds() -> None:
    """Hardware detection adapter should build successfully."""
    contract = detect_node_hardware(node_id="dev_001")

    assert contract.node_id == "dev_001"
    assert contract.cpu.cpu_arch != ""
    assert contract.cpu.cpu_cores >= 1
    assert contract.cpu.cpu_threads >= 1
    assert contract.memory.ram_total_gb >= 1
    assert contract.memory.ram_pressure_percent >= 0
    assert contract.gpu_count >= 0


def test_hardware_detection_adapter_returns_detection_sources() -> None:
    """Hardware detection adapter should expose at least one detection source."""
    contract = detect_node_hardware(node_id="dev_001")

    assert len(contract.detection_sources) >= 1
