from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    CanonicalQueueIdentity,
    CanonicalQueueIdentityContract,
)


def test_queue_identity_models_build() -> None:
    """Canonical queue identity models should build successfully."""
    contract = CanonicalQueueIdentityContract(
        total_queues=5,
        queues=(
            CanonicalQueueIdentity(
                queue_name="critical_queue",
                priority_class="critical",
            ),
            CanonicalQueueIdentity(
                queue_name="high_queue",
                priority_class="high",
            ),
            CanonicalQueueIdentity(
                queue_name="normal_queue",
                priority_class="normal",
            ),
            CanonicalQueueIdentity(
                queue_name="background_queue",
                priority_class="background",
            ),
            CanonicalQueueIdentity(
                queue_name="deferred_queue",
                priority_class="deferred",
            ),
        ),
    )

    assert contract.total_queues == 5
    assert len(contract.queues) == 5
    assert contract.queues[0].queue_name == "critical_queue"
    assert contract.queues[-1].queue_name == "deferred_queue"
