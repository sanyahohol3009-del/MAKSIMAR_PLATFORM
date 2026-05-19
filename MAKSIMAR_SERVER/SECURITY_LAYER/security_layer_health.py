from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.security_read_model import (
    SecurityAdapterReadModel,
    SecurityLayerHealthReadModel,
    SecurityReadModelStatus,
    SecurityVerifierReadinessReadModel,
)


EXPECTED_SECURITY_LAYER_FILES: tuple[str, ...] = (
    "SECURITY_LAYER/layer_manifest.yaml",
    "SECURITY_LAYER/container_contract.yaml",
    "SECURITY_LAYER/boundaries/container_adapter_boundary.yaml",
    "SECURITY_LAYER/config/security_layer_policy.yaml",
    "MAKSIMAR_CORE_LIB/security_layer/security_read_model.py",
    "MAKSIMAR_CORE_LIB/security_layer/security_request_models.py",
    "MAKSIMAR_CORE_LIB/security_layer/security_decision_models.py",
    "MAKSIMAR_CORE_LIB/security_layer/rbac_contract.py",
    "MAKSIMAR_CORE_LIB/security_layer/policy_enforcer_contract.py",
    "MAKSIMAR_CORE_LIB/security_layer/security_gate_contract.py",
    "MAKSIMAR_CORE_LIB/security_layer/signature_verifier_contract.py",
    "MAKSIMAR_CORE_LIB/security_layer/execution_bundle_verifier_contract.py",
    "MAKSIMAR_SERVER/SECURITY_LAYER/security_gate.py",
    "MAKSIMAR_SERVER/SECURITY_LAYER/security_decision_builder.py",
    "MAKSIMAR_SERVER/SECURITY_LAYER/security_telemetry_read_model_builder.py",
    "MAKSIMAR_SERVER/SECURITY_LAYER/security_layer_health.py",
    "MAKSIMAR_SERVER/SECURITY_LAYER/adapters/security_existing_policy_adapter.py",
    "MAKSIMAR_SERVER/SECURITY_LAYER/adapters/security_vendor_gate_adapter.py",
)


EXPECTED_VERIFIERS: tuple[str, ...] = (
    "approval_service",
    "execution_bundle_verifier",
    "voice_identity",
    "vault_boundary",
    "signature_verifier",
    "usb_guard",
    "media_quarantine",
    "security_gate",
)


def build_security_layer_health_read_model(
    *,
    project_root: Path,
    adapter_readiness: tuple[SecurityAdapterReadModel, ...] = (),
) -> SecurityLayerHealthReadModel:
    present: list[str] = []
    missing: list[str] = []

    for relative_path in EXPECTED_SECURITY_LAYER_FILES:
        path = project_root / relative_path
        if path.exists():
            present.append(relative_path)
        else:
            missing.append(relative_path)

    verifier_status = (
        SecurityReadModelStatus.HEALTHY
        if not missing
        else SecurityReadModelStatus.DEGRADED
    )

    verifier_reason = (
        "security_verifier_contract_available"
        if not missing
        else "security_verifier_contract_surface_incomplete"
    )

    verifier_readiness = tuple(
        SecurityVerifierReadinessReadModel(
            verifier_id=verifier_id,
            available=not missing,
            status=verifier_status,
            reason_codes=(verifier_reason,),
        )
        for verifier_id in EXPECTED_VERIFIERS
    )

    status = SecurityReadModelStatus.HEALTHY if not missing else SecurityReadModelStatus.DEGRADED
    reason_codes = (
        ("security_layer_health_complete",)
        if not missing
        else ("security_layer_health_missing_files",)
    )

    return SecurityLayerHealthReadModel(
        layer_id="SECURITY_LAYER",
        status=status,
        present_files=tuple(sorted(present)),
        missing_files=tuple(sorted(missing)),
        verifier_readiness=verifier_readiness,
        adapter_readiness=adapter_readiness,
        reason_codes=reason_codes,
    )
