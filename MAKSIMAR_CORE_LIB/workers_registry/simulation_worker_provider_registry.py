"""Canonical simulation worker provider registry.

WORKERS registers its runtime factory here; SERVER/CONTROL_PLANE callers consume
the factory through this CORE boundary instead of importing the WORKERS runtime
directly (preserving downward dependency direction).
"""
from __future__ import annotations

from typing import Any, Callable

_SimulationWorkerRuntimeFactory = Callable[[], Any]

_FACTORY: _SimulationWorkerRuntimeFactory | None = None
_FACTORY_IDENTITY: tuple[str, str] | None = None


def register_simulation_worker_factory(factory: _SimulationWorkerRuntimeFactory) -> None:
    global _FACTORY, _FACTORY_IDENTITY
    identity = (str(getattr(factory, "__module__", "")), str(getattr(factory, "__qualname__", "")))
    # Idempotent for the SAME logical provider (module reload / xdist worker re-import);
    # fail closed if a DIFFERENT factory tries to replace the registered provider.
    if _FACTORY is not None and _FACTORY_IDENTITY != identity:
        raise RuntimeError(
            f"conflicting simulation worker factory: registered={_FACTORY_IDENTITY} attempted={identity}"
        )
    _FACTORY = factory
    _FACTORY_IDENTITY = identity


def get_simulation_worker_factory() -> _SimulationWorkerRuntimeFactory:
    if _FACTORY is None:
        raise RuntimeError("simulation worker runtime factory not registered")
    return _FACTORY


def is_simulation_worker_factory_registered() -> bool:
    return _FACTORY is not None


def _reset_simulation_worker_factory_for_tests() -> None:
    """Test-isolation reset; not used in production runtime."""
    global _FACTORY, _FACTORY_IDENTITY
    _FACTORY = None
    _FACTORY_IDENTITY = None
