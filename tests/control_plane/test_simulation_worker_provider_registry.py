from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.workers_registry.simulation_worker_provider_registry import (
    _reset_simulation_worker_factory_for_tests,
    get_simulation_worker_factory,
    register_simulation_worker_factory,
)


@pytest.fixture(autouse=True)
def _reset_registry():
    # Collection of the canonical semantic-turn tests imports the real worker and
    # registers its factory.  Preserve that process-level production registration:
    # this fixture owns only mutations made by this test module.
    try:
        previous_factory = get_simulation_worker_factory()
    except RuntimeError:
        previous_factory = None
    _reset_simulation_worker_factory_for_tests()
    yield
    _reset_simulation_worker_factory_for_tests()
    if previous_factory is not None:
        register_simulation_worker_factory(previous_factory)


def _factory_a():
    return {"provider": "a"}


def _factory_b():
    return {"provider": "b"}


def test_same_logical_provider_re_registration_is_idempotent():
    # Same logical provider (module/qualname identity) may re-register on reload/re-import.
    register_simulation_worker_factory(_factory_a)
    register_simulation_worker_factory(_factory_a)  # no raise
    assert get_simulation_worker_factory() is _factory_a


def test_conflicting_provider_fails_closed():
    register_simulation_worker_factory(_factory_a)
    with pytest.raises(RuntimeError, match="conflicting simulation worker factory"):
        register_simulation_worker_factory(_factory_b)


def test_worker_runtime_registers_canonical_factory():
    from MAKSIMAR_SERVER.WORKERS.simulation_worker import build_simulation_worker_runtime

    register_simulation_worker_factory(build_simulation_worker_runtime)
    runtime = get_simulation_worker_factory()()
    assert runtime is not None
