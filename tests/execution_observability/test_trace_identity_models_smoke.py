from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    CanonicalTraceIdentity,
    CanonicalTraceIdentityContract,
)


def test_trace_identity_models_build() -> None:
    """Canonical trace identity models should build successfully."""
    contract = CanonicalTraceIdentityContract(
        total_trace_patterns=2,
        traces=(
            CanonicalTraceIdentity(
                trace_prefix="trace_exec_",
                identity_pattern="trace_exec_<hex>",
                source_layer="execution_control",
            ),
            CanonicalTraceIdentity(
                trace_prefix="trace_obs_",
                identity_pattern="trace_obs_<hex>",
                source_layer="execution_observability",
            ),
        ),
    )

    assert contract.total_trace_patterns == 2
    assert len(contract.traces) == 2
    assert contract.traces[0].trace_prefix == "trace_exec_"
    assert contract.traces[-1].source_layer == "execution_observability"
