from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.network_trust_boundary_binding_models import (
    NETWORK_SEGMENTATION_READ_MODEL_ID,
    NETWORK_TRUST_BOUNDARY_BINDING_ID,
    NetworkTrustBoundaryBindingReadModel,
    build_network_segmentation_read_model,
    build_network_trust_boundary_binding_read_model,
)


def test_network_trust_boundary_binding_reuses_existing_authority() -> None:
    read_model = build_network_trust_boundary_binding_read_model(project_root=Path.cwd())

    assert read_model.binding_id == NETWORK_TRUST_BOUNDARY_BINDING_ID
    assert read_model.source_exists is True
    assert read_model.source_test_exists is True
    assert read_model.source_doc_exists is True
    assert read_model.existing_contract_importable is True
    assert read_model.network_segmentation_is_source_authority is False
    assert read_model.adapter_binding_only is True
    assert read_model.replace_existing_source_allowed is False
    assert read_model.move_existing_source_allowed is False
    assert read_model.delete_existing_source_allowed is False
    assert read_model.migrate_existing_source_allowed is False
    assert read_model.production_deployment_allowed is False
    assert read_model.public_exposure_allowed is False
    assert read_model.runtime_network_mutation_allowed is False
    assert read_model.canonical_write_allowed is False
    assert read_model.dashboard_execution_allowed is False
    assert read_model.dashboard_safe is True


def test_network_segmentation_read_model_declares_required_segments() -> None:
    read_model = build_network_segmentation_read_model(project_root=Path.cwd())

    assert read_model.read_model_id == NETWORK_SEGMENTATION_READ_MODEL_ID
    assert "net_core_safety" in read_model.segment_ids
    assert "net_control" in read_model.segment_ids
    assert "net_security" in read_model.segment_ids
    assert "net_governance" in read_model.segment_ids
    assert "net_data" in read_model.segment_ids
    assert "net_ai" in read_model.segment_ids
    assert "net_products" in read_model.segment_ids
    assert "net_observability" in read_model.segment_ids
    assert "net_update" in read_model.segment_ids
    assert read_model.healthcheck_required is True
    assert read_model.restart_policy_required is True
    assert read_model.no_public_exposure is True
    assert read_model.production_deployment_allowed is False
    assert read_model.runtime_network_mutation_allowed is False
    assert read_model.dashboard_safe is True


def test_network_trust_boundary_binding_rejects_replacement_authority() -> None:
    base = build_network_trust_boundary_binding_read_model(project_root=Path.cwd())

    with pytest.raises(ValueError, match="NETWORK_SEGMENTATION must not become"):
        NetworkTrustBoundaryBindingReadModel(
            binding_id=base.binding_id,
            source_authority_path=base.source_authority_path,
            source_test_path=base.source_test_path,
            source_doc_path=base.source_doc_path,
            source_exists=base.source_exists,
            source_test_exists=base.source_test_exists,
            source_doc_exists=base.source_doc_exists,
            existing_contract_importable=base.existing_contract_importable,
            network_segmentation_is_source_authority=True,
            adapter_binding_only=True,
            replace_existing_source_allowed=False,
            move_existing_source_allowed=False,
            delete_existing_source_allowed=False,
            migrate_existing_source_allowed=False,
            production_deployment_allowed=False,
            public_exposure_allowed=False,
            runtime_network_mutation_allowed=False,
            canonical_write_allowed=False,
            dashboard_execution_allowed=False,
            dashboard_safe=True,
            reason_codes=("bad",),
        )


def test_network_containerization_xray_marker_read_model_declares_all_markers() -> None:
    from MAKSIMAR_CORE_LIB.network_containerization.network_trust_boundary_binding_models import (
        NETWORK_CONTAINERIZATION_XRAY_MARKER_READ_MODEL_ID,
        build_network_containerization_xray_marker_read_model,
    )

    read_model = build_network_containerization_xray_marker_read_model()

    assert read_model.read_model_id == NETWORK_CONTAINERIZATION_XRAY_MARKER_READ_MODEL_ID
    assert read_model.net_core_safety is True
    assert read_model.net_control is True
    assert read_model.net_security is True
    assert read_model.net_governance is True
    assert read_model.net_data is True
    assert read_model.net_ai is True
    assert read_model.net_products is True
    assert read_model.net_observability is True
    assert read_model.net_update is True
    assert read_model.healthcheck is True
    assert read_model.restart_policy is True
    assert read_model.no_public_exposure is True
    assert read_model.public_exposure_allowed is False
    assert read_model.production_deployment_allowed is False
    assert read_model.runtime_network_mutation_allowed is False
    assert read_model.dashboard_safe is True


def test_network_containerization_explicit_xray_marker_functions_pass() -> None:
    from MAKSIMAR_CORE_LIB.network_containerization.network_trust_boundary_binding_models import (
        build_network_containerization_xray_marker_read_model,
        validate_healthcheck_marker,
        validate_net_ai_marker,
        validate_net_control_marker,
        validate_net_core_safety_marker,
        validate_net_data_marker,
        validate_net_governance_marker,
        validate_net_observability_marker,
        validate_net_products_marker,
        validate_net_security_marker,
        validate_net_update_marker,
        validate_no_public_exposure_marker,
        validate_restart_policy_marker,
    )

    read_model = build_network_containerization_xray_marker_read_model()

    assert validate_net_core_safety_marker(read_model) is True
    assert validate_net_control_marker(read_model) is True
    assert validate_net_security_marker(read_model) is True
    assert validate_net_governance_marker(read_model) is True
    assert validate_net_data_marker(read_model) is True
    assert validate_net_ai_marker(read_model) is True
    assert validate_net_products_marker(read_model) is True
    assert validate_net_observability_marker(read_model) is True
    assert validate_net_update_marker(read_model) is True
    assert validate_healthcheck_marker(read_model) is True
    assert validate_restart_policy_marker(read_model) is True
    assert validate_no_public_exposure_marker(read_model) is True
