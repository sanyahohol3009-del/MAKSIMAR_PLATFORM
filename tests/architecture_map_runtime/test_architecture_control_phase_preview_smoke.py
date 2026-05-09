from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_architecture_control_phase_preview,
)


def test_architecture_control_phase_preview_smoke() -> None:
    preview = build_architecture_control_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_ready"] is True
    assert preview["read_only"] is True
    assert preview["no_mutation_surface"] is True
    assert preview["no_network_surface"] is True
