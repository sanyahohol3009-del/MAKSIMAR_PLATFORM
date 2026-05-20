from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.network_containerization.network_segment_models import (
    REQUIRED_NETWORK_SEGMENTS,
    NetworkSegmentModel,
    build_default_network_segments,
    build_network_segment_model,
)


def test_default_network_segments_cover_required_ids() -> None:
    segments = build_default_network_segments()

    assert {segment.segment_id for segment in segments} == set(REQUIRED_NETWORK_SEGMENTS)
    assert all(segment.public_exposure_allowed is False for segment in segments)
    assert all(segment.runtime_network_mutation_allowed is False for segment in segments)
    assert all(segment.internal_only is True for segment in segments)
    assert all(segment.dashboard_safe is True for segment in segments)


def test_network_segment_model_rejects_public_exposure() -> None:
    with pytest.raises(ValueError, match="public_exposure_allowed"):
        NetworkSegmentModel(
            segment_id="net_control",
            title="Control",
            public_exposure_allowed=True,
            runtime_network_mutation_allowed=False,
            internal_only=True,
            dashboard_safe=True,
            reason_codes=("bad",),
        )


def test_unknown_network_segment_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown network segment"):
        build_network_segment_model("net_unknown")  # type: ignore[arg-type]
