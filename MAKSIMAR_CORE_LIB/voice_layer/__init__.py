from MAKSIMAR_CORE_LIB.voice_layer.voice_command_contract import (
    VoiceCommandContract,
    VoiceCommandEntry,
    VoiceCommandId,
    VoiceCommandIntent,
    VoiceDisplayRole,
    VoiceLanguageCode,
    VoiceLatencyClass,
    VoiceResponseMode,
    VoiceScriptName,
    VoiceTargetViewId,
    VoiceUtterancePatternId,
    build_voice_command_contract,
)


def list_voice_definitions() -> tuple[VoiceCommandEntry, ...]:
    """Return canonical voice command definitions."""
    return build_voice_command_contract().entries


__all__ = [
    "VoiceCommandContract",
    "VoiceCommandEntry",
    "VoiceCommandId",
    "VoiceCommandIntent",
    "VoiceDisplayRole",
    "VoiceLanguageCode",
    "VoiceLatencyClass",
    "VoiceResponseMode",
    "VoiceScriptName",
    "VoiceTargetViewId",
    "VoiceUtterancePatternId",
    "build_voice_command_contract",
    "list_voice_definitions",
]
