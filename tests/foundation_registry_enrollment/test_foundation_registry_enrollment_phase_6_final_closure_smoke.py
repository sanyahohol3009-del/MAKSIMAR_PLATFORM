from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layers_final_acceptance_read_model import (
    build_foundation_layers_final_acceptance_read_model,
)


PHASE_6_CLOSURE_DOC = Path(
    "docs/architecture/foundation/foundation_registry_enrollment_phase_6_final_closure_v1.md"
)


def test_foundation_registry_enrollment_phase_6_closure_doc_exists() -> None:
    assert PHASE_6_CLOSURE_DOC.is_file()

    text = PHASE_6_CLOSURE_DOC.read_text(encoding="utf-8")

    assert "PHASE 6 is closed." in text
    assert "foundation_registry_enrollment_closed: true" in text
    assert "final_acceptance_ready: true" in text
    assert "roadmap_selection_allowed_after_closure: true" in text
    assert "registry_write_allowed: false" in text
    assert "auto_enrollment_write_allowed: false" in text
    assert "runtime_mutation_allowed: false" in text
    assert "dashboard_mutation_allowed: false" in text
    assert "direct_execution_allowed: false" in text
    assert "deployment_allowed: false" in text
    assert "public_exposure_allowed: false" in text


def test_foundation_registry_enrollment_phase_6_closure_preserves_final_acceptance() -> None:
    read_model = build_foundation_layers_final_acceptance_read_model()

    assert read_model.final_acceptance_ready is True
    assert read_model.all_foundation_layers_have_manifest is True
    assert read_model.all_foundation_layers_have_dashboard_visibility is True
    assert read_model.all_foundation_layers_have_container_boundary is True
    assert read_model.all_foundation_layers_enrolled is True
    assert read_model.all_foundation_layers_enrolled_without_direct_execution is True
    assert read_model.registry_write_allowed is False
    assert read_model.auto_enrollment_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_mutation_allowed is False
    assert read_model.direct_execution_allowed is False
    assert read_model.deployment_allowed is False
    assert read_model.public_exposure_allowed is False


def test_foundation_registry_enrollment_phase_6_closure_lists_all_batches() -> None:
    text = PHASE_6_CLOSURE_DOC.read_text(encoding="utf-8")

    for batch_id in ("6.1", "6.2", "6.3", "6.4", "6.5"):
        assert f"| {batch_id} |" in text

    for layer_id in (
        "security_layer",
        "data_plane",
        "update_recovery_infra",
        "network_containerization",
        "ai_orchestration",
    ):
        assert layer_id in text
