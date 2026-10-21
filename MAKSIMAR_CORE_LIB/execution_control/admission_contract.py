from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control.admission_models import (
    AdmissionContract,
    AdmissionDecision,
)


def build_admission_contract() -> AdmissionContract:
    """Build unified admission control contract."""

    decisions = (
        AdmissionDecision(
            request_id="req_001",
            admitted=True,
            reason="resources_available",
            policy_checked=True,
        ),
        AdmissionDecision(
            request_id="req_002",
            admitted=False,
            reason="queue_pressure",
            policy_checked=True,
        ),
    )

    return AdmissionContract(
        total_decisions=len(decisions),
        decisions=decisions,
    )


# Only in-process coordination. This is explicitly NOT a provider-global lease.
import threading
from contextlib import contextmanager
_MODEL_ADMISSION_LOCK = threading.Lock()


def evaluate_model_admission(*, request_id, profile, observation, requested_context,
                             policy_allowed, now_monotonic, locally_serialized=False):
    """Execute the existing admission authority over exact, fresh resource facts."""
    import math
    from MAKSIMAR_CORE_LIB.ai_orchestration.model_resource_requirements_contract import ModelLoadResourceDemand
    from MAKSIMAR_CORE_LIB.execution_control.admission_models import ModelResourceObservation
    evidence = (("local_coordination_scope", "PROCESS_ONLY"),
                ("provider_exclusive_reservation_created", "NO"))
    def result(reason, admitted=False):
        return AdmissionDecision(request_id=str(request_id), admitted=admitted,
            reason=reason, policy_checked=policy_allowed is True,
            model_id=str(getattr(profile, "model_id", "")),
            role_id=str(getattr(profile, "role_id", "")), resource_evidence=evidence)
    if policy_allowed is not True:
        return result("model_policy_or_stopgate_denied")
    if locally_serialized is not True:
        return result("local_admission_not_acquired")
    if profile is None or getattr(profile, "status", None) != "installed" or getattr(profile, "installed", None) is not True:
        return result("model_profile_unavailable")
    demand = getattr(profile, "load_resource_demand", None)
    if not isinstance(demand, ModelLoadResourceDemand) or demand.bound_kind != "VERIFIED_UPPER_BOUND":
        return result("model_resource_demand_unknown")
    evidence += (("demand_provenance", demand.provenance), ("model_revision", demand.model_revision))
    if (demand.model_id != profile.model_id or demand.backend_id != profile.backend_id
            or type(requested_context) is not int or requested_context != demand.context_tokens):
        return result("model_resource_demand_mismatch")
    if not isinstance(observation, ModelResourceObservation):
        return result("resource_observation_unavailable")
    evidence += (("observation_source", observation.source),
                 ("resource_scope", observation.scope_id),
                 ("provider_ownership_source", observation.ownership_source or "UNKNOWN"))
    if observation.provider_available is not True:
        return result("model_provider_unavailable")
    if (type(now_monotonic) not in (int, float)
            or type(observation.observed_monotonic) not in (int, float)):
        return result("resource_observation_invalid")
    age = now_monotonic - observation.observed_monotonic
    if (not math.isfinite(age)
            or age < 0 or age > demand.max_observation_age_seconds):
        return result("resource_observation_stale")
    if (observation.complete is not True or not observation.source
            or observation.scope_confirmed is not True or not observation.scope_id
            or not observation.provider_instance_id or observation.backend_id != demand.backend_id):
        return result("resource_scope_unproven")
    if observation.model_revision != demand.model_revision:
        return result("model_resource_revision_mismatch")
    if (observation.ownership_verified is not True or not observation.ownership_source
            or type(observation.active_concurrency) is not int or observation.active_concurrency < 0):
        return result("shared_provider_ownership_unknown")
    if observation.active_concurrency >= demand.max_concurrency:
        return result("provider_concurrency_limit")
    if (type(observation.resident_models) is not tuple
            or any(type(e) is not tuple or len(e) != 2 for e in observation.resident_models)):
        return result("resource_observation_invalid")
    if any(model != profile.model_id or revision != demand.model_revision
           for model, revision in observation.resident_models):
        return result("unexpected_provider_residency")
    def capacities(entries):
        if type(entries) is not tuple:
            raise ValueError("mutable resource observation")
        out = {}
        for entry in entries:
            if type(entry) is not tuple or len(entry) != 2:
                raise ValueError("invalid resource observation")
            key, value = entry
            if not isinstance(key, str) or not key or key in out or type(value) is not int or value < 0:
                raise ValueError("invalid or duplicate resource identity")
            out[key] = value
        return out
    try:
        memory = capacities(observation.memory_available_bytes)
        accelerators = capacities(observation.accelerator_available_bytes)
    except (TypeError, ValueError):
        return result("resource_observation_invalid")
    if not memory:
        return result("memory_observation_unknown")
    # A guest/cgroup/host share constrains the same allocation. Never sum them.
    if any(value < demand.peak_ram_bytes + demand.ram_headroom_bytes for value in memory.values()):
        return result("insufficient_available_memory")
    if type(observation.cpu_threads) is not int or observation.cpu_threads < demand.min_cpu_threads:
        return result("insufficient_cpu_capacity")
    if demand.accelerator_bytes and observation.physical_identity_verified is not True:
        return result("physical_accelerator_identity_unknown")
    for device, peak in demand.accelerator_bytes:
        if device not in accelerators:
            return result("accelerator_placement_unknown")
        if accelerators[device] < peak + demand.accelerator_headroom_bytes:
            return result("insufficient_available_accelerator_memory")
    return result("resources_observed_with_verified_provider_ownership", True)


@contextmanager
def model_admission(*, request_id, profile, observe, requested_context,
                    policy_allowed, clock):
    """Hold only this local operation; never claim foreign-client exclusion."""
    if not _MODEL_ADMISSION_LOCK.acquire(blocking=False):
        yield AdmissionDecision(str(request_id), False, "local_admission_busy", False,
                                str(getattr(profile, "model_id", "")), str(getattr(profile, "role_id", "")))
        return
    try:
        # Unknown demand/policy is denied without even probing provider metadata.
        demand = getattr(profile, "load_resource_demand", None)
        try:
            observation = observe() if (policy_allowed is True and demand is not None) else None
        except Exception:
            observation = None
        decision = evaluate_model_admission(request_id=request_id, profile=profile,
            observation=observation, requested_context=requested_context,
            policy_allowed=policy_allowed, now_monotonic=clock(), locally_serialized=True)
        yield decision
    finally:
        _MODEL_ADMISSION_LOCK.release()
