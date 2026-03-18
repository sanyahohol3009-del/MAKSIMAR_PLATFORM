from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.voice_layer.voice_models import VoicePolicyDefinition
from MAKSIMAR_CORE_LIB.voice_layer.voice_registry import VoiceRegistry


@lru_cache(maxsize=1)
def _get_registry() -> VoiceRegistry:
    """Build cached voice registry."""
    registry = VoiceRegistry()
    registry.load_all()
    return registry


def get_voice_definition(policy_id: str) -> VoicePolicyDefinition:
    """Get voice definition by id."""
    definition = _get_registry().get(policy_id)
    if definition is None:
        raise KeyError(f"Voice definition not found: {policy_id}")
    return definition


def list_voice_definitions() -> list[VoicePolicyDefinition]:
    """List all loaded voice definitions."""
    return _get_registry().list_all()
