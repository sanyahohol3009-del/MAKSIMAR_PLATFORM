from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection import build_memory_drift_signal_sample


def test_memory_drift_signal_models_smoke() -> None:
    signal = build_memory_drift_signal_sample()

    assert signal.signal_ready is True
    assert signal.human_review_required is True
    assert signal.auto_resolution_allowed is False
    assert signal.canonical_truth_change_allowed is False
    assert signal.confidence > 0
