from dataclasses import replace
import math
import threading
import pytest
from MAKSIMAR_CORE_LIB.ai_orchestration import model_profile_registry_contract as registry
from MAKSIMAR_CORE_LIB.ai_orchestration.model_resource_requirements_contract import ModelLoadResourceDemand
from MAKSIMAR_CORE_LIB.execution_control.admission_models import ModelResourceObservation
from MAKSIMAR_CORE_LIB.execution_control.admission_contract import evaluate_model_admission, model_admission

G = 1024 ** 3

@pytest.fixture
def resource_world():
    base = registry.resolve_runtime_model_profile(role_id="jarvis_chat_model")
    demand = ModelLoadResourceDemand(base.model_id, base.backend_id, "fixture-revision", 4096, 1,
        8 * G, (("fixture-gpu-a", 20 * G),), 4, "fixture validated full-load bound", 5,
        bound_kind="VERIFIED_UPPER_BOUND")
    profile = replace(base, load_resource_demand=demand)
    observation = ModelResourceObservation(100.0, base.backend_id, "fixture-host", "fixture-provider-instance",
        True, "fixture-revision", (("host", 64 * G), ("guest", 32 * G), ("cgroup", 16 * G)),
        (("fixture-gpu-a", 70 * G),), 16, True, True, True,
        "fixture atomic provider exclusion", 0, (), True, "fixture independent resource facts")
    return profile, observation


def decide(profile, observation, **kwargs):
    args = dict(request_id="fixture-request", profile=profile, observation=observation,
        requested_context=4096, policy_allowed=True, now_monotonic=100.0, locally_serialized=True)
    args.update(kwargs)
    return evaluate_model_admission(**args)


def test_real_existing_admission_accepts_explicit_bounds(resource_world):
    p, o = resource_world
    verdict = decide(p, o)
    assert verdict.admitted and verdict.policy_checked
    assert dict(verdict.resource_evidence)["provider_exclusive_reservation_created"] == "NO"
    assert dict(verdict.resource_evidence)["demand_provenance"] == p.load_resource_demand.provenance


@pytest.mark.parametrize("change,reason", [
    ({"provider_available": False}, "model_provider_unavailable"),
    ({"observed_monotonic": 90.0}, "resource_observation_stale"),
    ({"observed_monotonic": 101.0}, "resource_observation_stale"),
    ({"observed_monotonic": float("nan")}, "resource_observation_stale"),
    ({"complete": False}, "resource_scope_unproven"),
    ({"scope_confirmed": False}, "resource_scope_unproven"),
    ({"provider_instance_id": ""}, "resource_scope_unproven"),
    ({"model_revision": "foreign-revision"}, "model_resource_revision_mismatch"),
    ({"ownership_verified": False}, "shared_provider_ownership_unknown"),
    ({"ownership_source": ""}, "shared_provider_ownership_unknown"),
    ({"active_concurrency": None}, "shared_provider_ownership_unknown"),
    ({"active_concurrency": 1}, "provider_concurrency_limit"),
    ({"resident_models": (("foreign-model", "foreign-revision"),)}, "unexpected_provider_residency"),
    ({"memory_available_bytes": (("host", 4 * G), ("guest", 32 * G))}, "insufficient_available_memory"),
    ({"memory_available_bytes": (("host", 32 * G), ("guest", 4 * G))}, "insufficient_available_memory"),
    ({"memory_available_bytes": ()}, "memory_observation_unknown"),
    ({"memory_available_bytes": (("same-domain", 64 * G), ("same-domain", 64 * G))}, "resource_observation_invalid"),
    ({"accelerator_available_bytes": (("fixture-gpu-a", 10 * G),)}, "insufficient_available_accelerator_memory"),
    ({"accelerator_available_bytes": (("unknown-physical-device", 80 * G),)}, "accelerator_placement_unknown"),
    ({"physical_identity_verified": False}, "physical_accelerator_identity_unknown"),
    ({"cpu_threads": 1}, "insufficient_cpu_capacity"),
])
def test_real_admission_rejects_incomplete_stale_or_insufficient_facts(resource_world, change, reason):
    p, o = resource_world
    result = decide(p, replace(o, **change))
    assert not result.admitted and result.reason == reason


@pytest.mark.parametrize("kwargs", [{"policy_allowed": False}, {"locally_serialized": False},
    {"requested_context": 3072}, {"requested_context": True}])
def test_policy_local_scope_and_context_never_guessed(resource_world, kwargs):
    assert not decide(*resource_world, **kwargs).admitted


def test_unknown_profile_demand_rejected_without_external_observation(resource_world):
    p, _ = resource_world
    p = replace(p, load_resource_demand=None)
    with model_admission(request_id="fixture", profile=p,
            observe=lambda: pytest.fail("unknown demand probed provider"), requested_context=4096,
            policy_allowed=True, clock=lambda: 100.0) as result:
        assert not result.admitted and result.reason == "model_resource_demand_unknown"


def test_host_guest_constraints_are_intersected_not_added(resource_world):
    p, o = resource_world
    p = replace(p, load_resource_demand=replace(p.load_resource_demand, peak_ram_bytes=20 * G))
    o = replace(o, memory_available_bytes=(("host", 12 * G), ("guest", 12 * G)))
    assert not decide(p, o).admitted


def test_future_larger_model_and_multiple_devices_need_no_generic_name_or_size_change(resource_world):
    p, o = resource_world
    demand = replace(p.load_resource_demand, model_id="fixture-future-primary",
        peak_ram_bytes=48 * G, accelerator_bytes=(("fixture-gpu-a", 60 * G), ("fixture-gpu-b", 60 * G)))
    p = replace(p, model_id=demand.model_id, load_resource_demand=demand)
    o = replace(o, memory_available_bytes=(("host", 128 * G),),
        accelerator_available_bytes=(("fixture-gpu-a", 80 * G), ("fixture-gpu-b", 80 * G)))
    assert decide(p, o).admitted
    assert not decide(p, replace(o, accelerator_available_bytes=(("fixture-gpu-a", 120 * G),))).admitted


def test_local_concurrent_operation_rejected_and_slot_released(resource_world):
    p, o = resource_world
    entered, release = threading.Event(), threading.Event()
    verdicts = []
    def first():
        with model_admission(request_id="first", profile=p, observe=lambda: o,
                requested_context=4096, policy_allowed=True, clock=lambda: 100.0) as verdict:
            verdicts.append(verdict); entered.set(); assert release.wait(3)
    thread = threading.Thread(target=first); thread.start(); assert entered.wait(3)
    try:
        with model_admission(request_id="second", profile=p,
                observe=lambda: pytest.fail("concurrent denied request observed provider"),
                requested_context=4096, policy_allowed=True, clock=lambda: 100.0) as second:
            assert not second.admitted and second.reason == "local_admission_busy"
    finally:
        release.set(); thread.join(3)
    assert not thread.is_alive() and verdicts[0].admitted
    with model_admission(request_id="third", profile=p, observe=lambda: o,
            requested_context=4096, policy_allowed=True, clock=lambda: 100.0) as third:
        assert third.admitted


def test_observation_failure_and_race_fail_closed_and_release_slot(resource_world):
    p, o = resource_world
    def failure(): raise OSError("fixture observation unavailable")
    with model_admission(request_id="fixture", profile=p, observe=failure,
            requested_context=4096, policy_allowed=True, clock=lambda: 100.0) as result:
        assert not result.admitted
    with model_admission(request_id="fixture", profile=p, observe=lambda: o,
            requested_context=4096, policy_allowed=True, clock=lambda: 106.0) as result:
        assert not result.admitted and result.reason == "resource_observation_stale"


@pytest.mark.parametrize("change", [{"peak_ram_bytes": True}, {"max_concurrency": 0},
    {"max_observation_age_seconds": float("nan")}, {"context_tokens": 0},
    {"accelerator_bytes": (("duplicate", G), ("duplicate", G))}, {"provenance": ""}])
def test_malformed_demand_is_not_an_execution_permission(resource_world, change):
    with pytest.raises(ValueError): replace(resource_world[0].load_resource_demand, **change)
