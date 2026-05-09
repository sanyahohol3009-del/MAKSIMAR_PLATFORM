from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_project_output_artifact_memory


def test_project_output_artifact_models_smoke() -> None:
    memory = build_project_output_artifact_memory()

    assert memory.geometry_validation_required is True
    assert memory.simulation_recommended is True
    assert memory.manufacturing_authority_granted is False
