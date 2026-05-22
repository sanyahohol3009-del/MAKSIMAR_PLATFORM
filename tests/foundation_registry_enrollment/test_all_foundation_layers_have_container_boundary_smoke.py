from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layers_final_acceptance_read_model import (
    FOUNDATION_LAYER_CONTAINER_BOUNDARY_PATHS,
    build_foundation_layers_final_acceptance_read_model,
)


def test_all_foundation_layers_have_container_boundary() -> None:
    read_model = build_foundation_layers_final_acceptance_read_model()

    assert read_model.total_layers == 5
    assert read_model.container_boundary_layers == 5
    assert read_model.all_foundation_layers_have_container_boundary is True

    for entry in read_model.acceptance_entries:
        assert entry.has_container_boundary is True
        assert entry.container_boundary_paths == FOUNDATION_LAYER_CONTAINER_BOUNDARY_PATHS[entry.layer_id]
        assert entry.container_boundary_paths
        for path in entry.container_boundary_paths:
            assert Path(path).is_file()
