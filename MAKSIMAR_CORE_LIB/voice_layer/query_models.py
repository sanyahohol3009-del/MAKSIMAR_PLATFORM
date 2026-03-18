from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


VoiceCapability = Literal[
    "speech_to_text",
    "text_to_speech",
    "wake_word",
]


@dataclass(frozen=True, slots=True)
class VoiceQuery:
    """Canonical voice query model."""

    query_text: str
    capability: VoiceCapability | None = None
    limit: int = 10


@dataclass(frozen=True, slots=True)
class VoiceRetrievalItem:
    """Canonical voice retrieval item."""

    policy_id: str
    version: str
