from __future__ import annotations

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layers_final_acceptance_read_model import (
    FoundationLayerFinalAcceptanceEntry,
    FoundationLayersFinalAcceptanceReadModel,
    build_foundation_layers_final_acceptance_read_model,
)


def test_all_foundation_layers_enrolled_without_direct_execution() -> None:
    read_model = build_foundation_layers_final_acceptance_read_model()

    assert read_model.total_layers == 5
    assert read_model.enrolled_layers == 5
    assert read_model.direct_execution_allowed_layers == 0
    assert read_model.dashboard_mutation_allowed_layers == 0
    assert read_model.registry_write_allowed_layers == 0
    assert read_model.runtime_mutation_allowed_layers == 0
    assert read_model.all_foundation_layers_enrolled is True
    assert read_model.all_foundation_layers_enrolled_without_direct_execution is True
    assert read_model.registry_write_allowed is False
    assert read_model.auto_enrollment_write_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.dashboard_mutation_allowed is False
    assert read_model.direct_execution_allowed is False
    assert read_model.deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.final_acceptance_ready is True
    assert read_model.dashboard_safe is True
    assert read_model.read_only is True

    for entry in read_model.acceptance_entries:
        assert entry.enrolled is True
        assert entry.direct_execution_allowed is False
        assert entry.dashboard_mutation_allowed is False
        assert entry.registry_write_allowed is False
        assert entry.runtime_mutation_allowed is False
        assert entry.accepted is True


def test_foundation_layers_final_acceptance_to_dict_is_non_mutating() -> None:
    payload = build_foundation_layers_final_acceptance_read_model().to_dict()

    assert payload["final_acceptance_ready"] is True
    assert payload["registry_write_allowed"] is False
    assert payload["auto_enrollment_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["dashboard_mutation_allowed"] is False
    assert payload["direct_execution_allowed"] is False
    assert payload["deployment_allowed"] is False
    assert payload["public_exposure_allowed"] is False
    assert len(payload["acceptance_entries"]) == 5


def test_final_acceptance_read_model_rejects_direct_execution() -> None:
    good_model = build_foundation_layers_final_acceptance_read_model()
    bad_entry = FoundationLayerFinalAcceptanceEntry(
        layer_id="security_layer",
        manifest_path="SECURITY_LAYER/layer_manifest.yaml",
        container_boundary_paths=("SECURITY_LAYER/boundaries/container_adapter_boundary.yaml",),
        has_manifest=True,
        has_dashboard_visibility=True,
        has_container_boundary=True,
        enrolled=True,
        direct_execution_allowed=False,
        dashboard_mutation_allowed=False,
        registry_write_allowed=False,
        runtime_mutation_allowed=False,
        accepted=True,
    )

    try:
        FoundationLayersFinalAcceptanceReadModel(
            read_model_id="bad",
            readiness_summary=good_model.readiness_summary,
            dashboard_visibility=good_model.dashboard_visibility,
            acceptance_entries=(bad_entry,),
            total_layers=1,
            manifest_layers=1,
            dashboard_visible_layers=1,
            container_boundary_layers=1,
            enrolled_layers=1,
            direct_execution_allowed_layers=1,
            dashboard_mutation_allowed_layers=0,
            registry_write_allowed_layers=0,
            runtime_mutation_allowed_layers=0,
            all_foundation_layers_have_manifest=True,
            all_foundation_layers_have_dashboard_visibility=True,
            all_foundation_layers_have_container_boundary=True,
            all_foundation_layers_enrolled=True,
            all_foundation_layers_enrolled_without_direct_execution=True,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_mutation_allowed=False,
            direct_execution_allowed=False,
            deployment_allowed=False,
            public_exposure_allowed=False,
            final_acceptance_ready=True,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
    except ValueError as exc:
        assert "direct_execution_allowed_layers" in str(exc)
    else:
        raise AssertionError("direct execution count mismatch was not rejected")
