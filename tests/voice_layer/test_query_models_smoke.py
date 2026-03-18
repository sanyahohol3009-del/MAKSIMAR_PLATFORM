from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.voice_layer.query_models import VoiceQuery
from MAKSIMAR_CORE_LIB.voice_layer.voice_models import VoicePolicyDefinition
from MAKSIMAR_CORE_LIB.voice_layer.voice_summary import build_voice_summary


def test_build_voice_summary_matches_policy_ids() -> None:
    """Retrieval summary should match by policy_id substring."""
    definitions = [
        VoicePolicyDefinition(
            policy_id="voice_policy",
            version="voice_policy.v1",
            file_path=Path("voice_policy.yaml"),
            payload={},
        ),
        VoicePolicyDefinition(
            policy_id="voice_identity_policy",
            version="voice_identity_policy.v1",
            file_path=Path("voice_identity_policy.yaml"),
            payload={},
        ),
    ]

    query = VoiceQuery(query_text="identity", limit=10)
    summary = build_voice_summary(query, definitions)

    assert summary.total_matches == 1
    assert len(summary.returned_items) == 1
    assert summary.returned_items[0].policy_id == "voice_identity_policy"


def test_build_voice_summary_respects_limit() -> None:
    """Retrieval summary should respect query limit."""
    definitions = [
        VoicePolicyDefinition(
            policy_id="voice_policy",
            version="voice_policy.v1",
            file_path=Path("voice_policy.yaml"),
            payload={},
        ),
        VoicePolicyDefinition(
            policy_id="voice_identity_policy",
            version="voice_identity_policy.v1",
            file_path=Path("voice_identity_policy.yaml"),
            payload={},
        ),
    ]

    query = VoiceQuery(query_text="voice", limit=1)
    summary = build_voice_summary(query, definitions)

    assert summary.total_matches == 2
    assert len(summary.returned_items) == 1
