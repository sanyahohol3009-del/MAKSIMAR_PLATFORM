from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PayloadClass = Literal[
    "small_control",
    "medium_contract",
    "heavy_artifact",
]

PayloadDirection = Literal[
    "control_plane",
    "data_plane",
]

PayloadEmbeddingPolicy = Literal[
    "inline_allowed",
    "reference_required",
]


@dataclass(frozen=True, slots=True)
class PayloadClassEntry:
    """Canonical payload class description entry."""

    payload_class: PayloadClass
    routing_direction: PayloadDirection
    embedding_policy: PayloadEmbeddingPolicy
    max_inline_size_kb: int
    description: str


@dataclass(frozen=True, slots=True)
class PayloadClassContract:
    """Unified canonical payload class contract."""

    total_classes: int
    classes: tuple[PayloadClassEntry, ...]


def build_payload_class_contract() -> PayloadClassContract:
    """Build canonical payload class contract."""
    classes = (
        PayloadClassEntry(
            payload_class="small_control",
            routing_direction="control_plane",
            embedding_policy="inline_allowed",
            max_inline_size_kb=32,
            description="Small control payload carried inline through control contracts.",
        ),
        PayloadClassEntry(
            payload_class="medium_contract",
            routing_direction="control_plane",
            embedding_policy="inline_allowed",
            max_inline_size_kb=256,
            description="Medium-sized structured contract payload allowed inline with limits.",
        ),
        PayloadClassEntry(
            payload_class="heavy_artifact",
            routing_direction="data_plane",
            embedding_policy="reference_required",
            max_inline_size_kb=0,
            description="Heavy payload must be routed by reference through data plane.",
        ),
    )

    return PayloadClassContract(
        total_classes=len(classes),
        classes=classes,
    )
