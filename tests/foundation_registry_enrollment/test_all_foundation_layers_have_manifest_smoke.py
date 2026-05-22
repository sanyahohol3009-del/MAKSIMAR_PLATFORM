from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layers_final_acceptance_read_model import (
    FOUNDATION_LAYER_MANIFEST_PATHS,
    build_foundation_layers_final_acceptance_read_model,
)


def test_all_foundation_layers_have_manifest() -> None:
    read_model = build_foundation_layers_final_acceptance_read_model()

    assert read_model.total_layers == 5
    assert read_model.manifest_layers == 5
    assert read_model.all_foundation_layers_have_manifest is True

    layer_ids = {entry.layer_id for entry in read_model.acceptance_entries}
    assert layer_ids == set(FOUNDATION_LAYER_MANIFEST_PATHS)

    for entry in read_model.acceptance_entries:
        assert entry.has_manifest is True
        assert entry.manifest_path == FOUNDATION_LAYER_MANIFEST_PATHS[entry.layer_id]
        assert Path(entry.manifest_path).is_file()
