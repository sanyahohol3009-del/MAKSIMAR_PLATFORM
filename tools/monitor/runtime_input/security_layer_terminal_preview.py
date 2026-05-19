from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.security_layer.rbac_models import RbacPermission, RbacPolicy, RbacRole
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
    SecurityRiskLevel,
    SecuritySubjectKind,
    build_security_request,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.adapters.security_existing_policy_adapter import (
    ExistingPolicyPermissionBinding,
    ExistingPolicySource,
    build_existing_policy_adapter_snapshot,
    build_rbac_policy_from_existing_policy_adapter,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.adapters.security_vendor_gate_adapter import (
    VendorGateSecuritySignal,
    evaluate_vendor_gate_signal,
)
from MAKSIMAR_SERVER.SECURITY_LAYER.security_gate import evaluate_runtime_security_gate
from MAKSIMAR_SERVER.SECURITY_LAYER.security_telemetry_read_model_builder import (
    build_security_telemetry_read_model,
)


def build_sample_policy() -> tuple[RbacPolicy, object]:
    source = ExistingPolicySource(
        path="SECURITY_LAYER/existing_bindings/security_existing_sources.yaml",
        relation="existing_security_related_surface",
        action="reference_only",
    )
    permission = ExistingPolicyPermissionBinding(
        role_id="operator",
        permission_id="perm_security_preview_read_memory",
        action=SecurityActionKind.READ,
        resource_kind=SecurityResourceKind.MEMORY,
        source_path=source.path,
    )
    adapter = build_existing_policy_adapter_snapshot(
        sources=(source,),
        permission_bindings=(permission,),
    )
    policy = build_rbac_policy_from_existing_policy_adapter(
        adapter,
        policy_id="security_layer_preview_policy",
    )
    return policy, adapter


def build_direct_policy() -> RbacPolicy:
    return RbacPolicy(
        policy_id="security_layer_preview_direct_policy",
        roles=(
            RbacRole(
                role_id="operator",
                permissions=(
                    RbacPermission(
                        permission_id="perm_security_preview_read_memory",
                        action=SecurityActionKind.READ,
                        resource_kind=SecurityResourceKind.MEMORY,
                    ),
                ),
            ),
        ),
    )


def build_preview_payload(*, blocked: bool) -> dict[str, object]:
    if blocked:
        request = build_security_request(
            request_id="security_preview_blocked_001",
            trace_id="trace_security_preview_blocked_001",
            subject_id="unknown",
            subject_kind=SecuritySubjectKind.UNKNOWN,
            roles=(),
            authenticated=False,
            resource_id="core",
            resource_kind=SecurityResourceKind.CORE,
            action=SecurityActionKind.EXECUTE,
            risk_level=SecurityRiskLevel.HIGH,
            source_layer_id="CONTROL_PLANE",
            target_layer_id="CORE_ROOT",
            reason="preview blocked unauthorized high-risk request",
        )
        policy = build_direct_policy()
        policy_adapter = None
    else:
        request = build_security_request(
            request_id="security_preview_allowed_001",
            trace_id="trace_security_preview_allowed_001",
            subject_id="operator",
            subject_kind=SecuritySubjectKind.OPERATOR,
            roles=("operator",),
            authenticated=True,
            resource_id="memory",
            resource_kind=SecurityResourceKind.MEMORY,
            action=SecurityActionKind.READ,
            risk_level=SecurityRiskLevel.LOW,
            source_layer_id="CONTROL_PLANE",
            target_layer_id="MEMORY",
            reason="preview allowed low-risk memory read",
        )
        policy, policy_adapter = build_sample_policy()

    vendor_decision = evaluate_vendor_gate_signal(
        VendorGateSecuritySignal(
            backend_id="security_preview_clean_backend",
            official_remote_verified=True,
            commit_seen_in_remote_refs=True,
            canonical_memory_access=False,
            runtime_mutation_allowed=False,
            risky_static_findings_count=0,
            dependency_vulnerabilities_count=0,
            verified_secret_found=False,
            manual_security_review_required=False,
        )
    )

    evaluation = evaluate_runtime_security_gate(
        request,
        policy,
        existing_policy_adapter=policy_adapter,
        vendor_gate_decision=vendor_decision,
    )
    telemetry = build_security_telemetry_read_model(
        runtime_evaluation=evaluation,
        project_root=PROJECT_ROOT,
    )
    return telemetry.to_dict()


def render_human(payload: dict[str, object]) -> str:
    gate = payload["gate"]
    health = payload["health"]

    if not isinstance(gate, dict):
        raise TypeError("gate payload must be dict")
    if not isinstance(health, dict):
        raise TypeError("health payload must be dict")

    return "\n".join(
        (
            "===== SECURITY LAYER TERMINAL PREVIEW =====",
            f"layer_id: {payload['layer_id']}",
            f"batch_id: {payload['batch_id']}",
            f"status: {payload['status']}",
            f"decision_status: {gate['decision_status']}",
            f"decision_allows_execution: {gate['decision_allows_execution']}",
            f"actual_execution_performed: {gate['actual_execution_performed']}",
            f"health_status: {health['status']}",
            f"missing_files_count: {len(health['missing_files'])}",
            f"dashboard_safe: {payload['dashboard_safe']}",
            f"runtime_mutation_allowed: {payload['runtime_mutation_allowed']}",
            f"canonical_write_allowed: {payload['canonical_write_allowed']}",
            f"direct_execution_allowed: {payload['direct_execution_allowed']}",
            "reason_codes:",
            *[f"  - {item}" for item in payload["reason_codes"]],
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render SECURITY_LAYER read-only terminal preview.")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    parser.add_argument("--blocked", action="store_true")
    args = parser.parse_args()

    payload = build_preview_payload(blocked=args.blocked)

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_human(payload))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
