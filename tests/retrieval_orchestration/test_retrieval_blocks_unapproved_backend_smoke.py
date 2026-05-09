from __future__ import annotations

import pytest

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    RetrievalSourceBinding,
)


def test_retrieval_blocks_unapproved_backend_smoke() -> None:
    with pytest.raises(ValueError, match="policy_allowed must be True"):
        RetrievalSourceBinding(
            source_id="retrieval_source_unapproved_backend",
            source_kind="media_memory",
            memory_domain="media_memory",
            registry_ref="experimental://sqlite_vec",
            priority=1,
            evidence_supported=True,
            trace_supported=True,
            policy_allowed=False,
            backend_adapter_required=True,
        )
