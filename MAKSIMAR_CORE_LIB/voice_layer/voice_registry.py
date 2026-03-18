from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_layer.voice_loader import load_all_voice_definitions
from MAKSIMAR_CORE_LIB.voice_layer.voice_models import VoicePolicyDefinition


class VoiceRegistry:
    """In-memory registry of voice policy definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, VoicePolicyDefinition] = {}

    def load_all(self) -> None:
        """Load all voice definitions."""
        for result in load_all_voice_definitions():
            if not result.is_valid or result.definition is None:
                continue

            definition = result.definition
            self._definitions[definition.policy_id] = definition

    def get(self, policy_id: str) -> VoicePolicyDefinition | None:
        """Get voice definition by id."""
        return self._definitions.get(policy_id)

    def list_all(self) -> list[VoicePolicyDefinition]:
        """List all loaded voice definitions."""
        return list(self._definitions.values())
