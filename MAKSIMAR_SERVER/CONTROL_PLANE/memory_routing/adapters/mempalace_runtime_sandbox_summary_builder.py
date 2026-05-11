from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_runtime_sandbox_backend import (
    build_mempalace_fake_backend_query_result,
    build_mempalace_real_backend_candidate_state,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_runtime_sandbox_models import (
    build_mempalace_runtime_sandbox_policy,
)


def build_mempalace_runtime_sandbox_summary() -> Dict[str, object]:
    policy = build_mempalace_runtime_sandbox_policy()
    fake_query = build_mempalace_fake_backend_query_result()
    real_candidate = build_mempalace_real_backend_candidate_state()

    sandbox_summary_ready = (
        policy.sandbox_policy_ready
        and fake_query.result_ready
        and real_candidate.candidate_state_ready
        and policy.fake_backend_allowed
        and fake_query.fake_backend_used
        and real_candidate.real_backend_candidate_detected
        and real_candidate.real_backend_enabled is False
        and real_candidate.real_backend_query_allowed is False
        and policy.canonical_write_allowed is False
        and policy.runtime_mutation_allowed is False
        and fake_query.canonical_write_allowed is False
        and fake_query.runtime_mutation_allowed is False
    )

    return {
        "sandbox_policy_ready": policy.sandbox_policy_ready,
        "fake_backend_required": policy.fake_backend_required,
        "fake_backend_allowed": policy.fake_backend_allowed,
        "fake_backend_used": fake_query.fake_backend_used,
        "fake_backend_query_ready": fake_query.result_ready,
        "real_backend_candidate_detected": real_candidate.real_backend_candidate_detected,
        "real_backend_enabled": real_candidate.real_backend_enabled,
        "real_backend_query_allowed": real_candidate.real_backend_query_allowed,
        "manual_security_review_required": policy.manual_security_review_required,
        "hard_gate_passed": policy.hard_gate_passed,
        "vendor_import_smoke_passed": real_candidate.vendor_import_smoke_passed,
        "query_only_allowed": policy.query_only_allowed,
        "read_only_allowed": policy.read_only_allowed,
        "evidence_pack_required": policy.evidence_pack_required,
        "preview_trace_required": policy.preview_trace_required,
        "canonical_write_allowed": False,
        "auto_promotion_allowed": policy.auto_promotion_allowed,
        "auto_conflict_resolution_allowed": policy.auto_conflict_resolution_allowed,
        "runtime_mutation_allowed": False,
        "sandbox_summary_ready": sandbox_summary_ready,
    }
