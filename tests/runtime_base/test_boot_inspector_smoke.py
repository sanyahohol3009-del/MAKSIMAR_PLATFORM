from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_base.boot_inspector import inspect_boot_state


def test_boot_inspector_returns_known_runtime_roots() -> None:
    """Boot inspector should return canonical runtime roots."""
    inspections = inspect_boot_state()

    root_names = {inspection.root_name for inspection in inspections}

    assert "project_runtime" in root_names
    assert "state_runtime" in root_names
    assert "capital_runtime" in root_names
    assert "safety_runtime" in root_names
