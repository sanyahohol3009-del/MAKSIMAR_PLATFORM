from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NoDirectCanonicalWriteContract:
    contract_id: str
    layer_id: str
    no_direct_canonical_write: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must not be empty")
        if not self.layer_id:
            raise ValueError("layer_id must not be empty")
        if not self.no_direct_canonical_write:
            raise ValueError("no_direct_canonical_write must remain true")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")


DATA_PLANE_NO_DIRECT_CANONICAL_WRITE_CONTRACT = NoDirectCanonicalWriteContract(
    contract_id="data_plane_no_direct_canonical_write_contract_v1",
    layer_id="DATA_PLANE",
    no_direct_canonical_write=True,
    canonical_write_allowed=False,
    runtime_mutation_allowed=False,
    dashboard_safe=True,
    reason_codes=(
        "data_plane_never_writes_directly_to_canonical_store",
        "writes_require_policy_gate_and_data_plane_contract",
    ),
)
