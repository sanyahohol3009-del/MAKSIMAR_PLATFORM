from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from threading import Barrier

import pytest

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import cross_tenant_leak_guard as leak
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import regulatory_retrieval_scope_gate as scope
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import regulatory_routing_preview_builder as routing


@pytest.fixture(scope="module")
def registry():
    return routing.build_regulatory_memory_routing_registry()


def unexpected_rebuild():
    raise AssertionError("nested builder must consume the supplied registry")


def test_root_builds_one_registry_and_retains_security_checks(monkeypatch, registry):
    calls = []
    monkeypatch.setattr(routing, "build_regulatory_memory_routing_registry",
                        lambda: calls.append(registry) or registry)
    monkeypatch.setattr(scope, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    monkeypatch.setattr(leak, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    result = routing.build_regulatory_routing_preview()
    assert calls == [registry]
    assert result["preview_ready"] is True
    assert result["registry_id"] == registry.registry_id
    assert result["route_count"] == len(registry.routes)
    assert result["checked_route_count"] == len(registry.routes)
    assert result["read_only"] is True
    assert result["same_tenant_only"] is True
    assert result["leak_detected"] is False
    for name in ("cross_tenant_retrieval_allowed", "cross_tenant_merge_allowed",
                 "cross_jurisdiction_merge_allowed", "runtime_mutation_allowed",
                 "direct_core_write_allowed", "deployment_allowed_now"):
        assert result[name] is False


@pytest.mark.parametrize("module,name", [
    (scope, "build_regulatory_retrieval_scope_gate"),
    (scope, "build_regulatory_retrieval_scope_gate_preview"),
    (leak, "build_cross_tenant_leak_guard_result"),
    (leak, "build_cross_tenant_leak_guard_preview"),
])
def test_standalone_call_still_builds_exactly_one_fresh_registry(monkeypatch, registry, module, name):
    calls = []
    def build():
        calls.append(registry)
        return registry
    monkeypatch.setattr(module, "build_regulatory_memory_routing_registry", build)
    if module is leak:
        monkeypatch.setattr(scope, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    result = getattr(module, name)()
    assert calls == [registry]
    assert result is not None


@pytest.mark.parametrize("builder", [
    scope.build_regulatory_retrieval_scope_gate,
    scope.build_regulatory_retrieval_scope_gate_preview,
    leak.build_cross_tenant_leak_guard_result,
    leak.build_cross_tenant_leak_guard_preview,
])
def test_explicit_snapshot_requires_no_registry_rebuild(monkeypatch, registry, builder):
    monkeypatch.setattr(scope, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    monkeypatch.setattr(leak, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    assert builder(registry=registry) is not None


def test_next_invocation_observes_next_registry_not_previous_snapshot(monkeypatch, registry):
    snapshots = [replace(registry, registry_id="request_a"), replace(registry, registry_id="request_b")]
    remaining = iter(snapshots)
    monkeypatch.setattr(routing, "build_regulatory_memory_routing_registry", lambda: next(remaining))
    monkeypatch.setattr(scope, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    monkeypatch.setattr(leak, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    assert routing.build_regulatory_routing_preview()["registry_id"] == "request_a"
    assert routing.build_regulatory_routing_preview()["registry_id"] == "request_b"


def test_concurrent_invocations_do_not_share_registry(monkeypatch, registry):
    barrier = Barrier(2)
    snapshots = iter([replace(registry, registry_id="concurrent_a"),
                      replace(registry, registry_id="concurrent_b")])
    def build():
        value = next(snapshots)
        barrier.wait(timeout=3)
        return value
    monkeypatch.setattr(routing, "build_regulatory_memory_routing_registry", build)
    monkeypatch.setattr(scope, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    monkeypatch.setattr(leak, "build_regulatory_memory_routing_registry", unexpected_rebuild)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: routing.build_regulatory_routing_preview(), range(2)))
    assert {item["registry_id"] for item in results} == {"concurrent_a", "concurrent_b"}
    assert all(item["preview_ready"] is True for item in results)


@pytest.mark.parametrize("field,value", [
    ("registry_ready", False), ("read_only", False),
    ("cross_tenant_retrieval_allowed", True), ("cross_tenant_merge_allowed", True),
    ("runtime_mutation_allowed", True), ("direct_core_write_allowed", True),
])
@pytest.mark.parametrize("builder", [
    scope.build_regulatory_retrieval_scope_gate_preview,
    leak.build_cross_tenant_leak_guard_preview,
])
def test_invalid_dependency_remains_fail_closed(registry, field, value, builder):
    # Deliberately corrupt an isolated fixture to prove consuming validators still run.
    invalid = replace(registry)
    object.__setattr__(invalid, field, value)
    with pytest.raises(ValueError):
        builder(registry=invalid)


def test_dependency_failure_is_not_replaced_with_ready_preview(monkeypatch):
    def unavailable():
        raise RuntimeError("registry unavailable")
    monkeypatch.setattr(routing, "build_regulatory_memory_routing_registry", unavailable)
    with pytest.raises(RuntimeError, match="registry unavailable"):
        routing.build_regulatory_routing_preview()
