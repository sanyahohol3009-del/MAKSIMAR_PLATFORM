from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


CanonicalModuleId = Literal[
    "control_plane",
    "execution_control",
    "execution_observability",
    "oob_dashboard",
]


@dataclass(frozen=True, slots=True)
class CanonicalModuleIdentity:
    """Canonical module identity entry."""

    module_id: CanonicalModuleId
    layer_name: str


@dataclass(frozen=True, slots=True)
class CanonicalModuleIdentityContract:
    """Unified canonical module identity contract."""

    total_modules: int
    modules: tuple[CanonicalModuleIdentity, ...]
