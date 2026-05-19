from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.no_direct_canonical_write_contract import (
    DATA_PLANE_NO_DIRECT_CANONICAL_WRITE_CONTRACT,
    NoDirectCanonicalWriteContract,
)


def test_data_plane_no_direct_canonical_write_contract_is_enforced() -> None:
    contract = DATA_PLANE_NO_DIRECT_CANONICAL_WRITE_CONTRACT

    assert contract.layer_id == "DATA_PLANE"
    assert contract.no_direct_canonical_write is True
    assert contract.canonical_write_allowed is False
    assert contract.runtime_mutation_allowed is False
    assert contract.dashboard_safe is True


def test_data_plane_no_direct_canonical_write_contract_rejects_canonical_write() -> None:
    with pytest.raises(ValueError, match="canonical_write_allowed"):
        NoDirectCanonicalWriteContract(
            contract_id="bad_contract",
            layer_id="DATA_PLANE",
            no_direct_canonical_write=True,
            canonical_write_allowed=True,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            reason_codes=("bad_canonical_write",),
        )
