from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_runtime_sandbox_backend import (
    build_mempalace_fake_backend_query_result,
    build_mempalace_real_backend_candidate_state,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_runtime_sandbox_models import (
    build_mempalace_runtime_sandbox_policy,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_runtime_sandbox_summary_builder import (
    build_mempalace_runtime_sandbox_summary,
)

_SANDBOX_FLOW = (
    "mempalace_vendor_gate_report",
    "mempalace_runtime_sandbox_policy",
    "fake_mempalace_sandbox_backend",
    "real_backend_candidate_state",
    "sandbox_summary",
    "sandbox_preview",
)


def build_mempalace_runtime_sandbox_preview() -> Dict[str, object]:
    policy = build_mempalace_runtime_sandbox_policy()
    fake_query = build_mempalace_fake_backend_query_result()
    real_candidate = build_mempalace_real_backend_candidate_state()
    summary = build_mempalace_runtime_sandbox_summary()

    return {
        "flow": _SANDBOX_FLOW,
        "preview_ready": summary["sandbox_summary_ready"],
        "sandbox_summary_ready": summary["sandbox_summary_ready"],
        "sandbox_policy_ready": policy.sandbox_policy_ready,
        "fake_backend_used": fake_query.fake_backend_used,
        "fake_backend_query_ready": fake_query.result_ready,
        "real_backend_candidate_detected": real_candidate.real_backend_candidate_detected,
        "real_backend_enabled": real_candidate.real_backend_enabled,
        "real_backend_query_allowed": real_candidate.real_backend_query_allowed,
        "manual_security_review_required": policy.manual_security_review_required,
        "hard_gate_passed": policy.hard_gate_passed,
        "query_only_allowed": policy.query_only_allowed,
        "read_only_allowed": policy.read_only_allowed,
        "evidence_pack": fake_query.evidence_pack,
        "preview_trace": fake_query.preview_trace,
        "canonical_write_allowed": False,
        "auto_promotion_allowed": policy.auto_promotion_allowed,
        "auto_conflict_resolution_allowed": policy.auto_conflict_resolution_allowed,
        "runtime_mutation_allowed": False,
    }
