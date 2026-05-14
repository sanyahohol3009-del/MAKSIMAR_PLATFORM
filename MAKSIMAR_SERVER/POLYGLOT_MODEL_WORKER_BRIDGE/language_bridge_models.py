from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE.artifact_language_models import (
    build_artifact_language_contract,
)


LanguageBridgeKind = Literal[
    "artifact_language_bridge",
    "code_language_bridge",
    "documentation_language_bridge",
    "config_language_bridge",
    "test_language_bridge",
]


@dataclass(frozen=True, slots=True)
class LanguageBridgeEntry:
    bridge_id: str
    bridge_kind: LanguageBridgeKind
    source_language: str
    target_language: str
    source_bound: bool
    artifact_ref_required: bool
    semantic_preservation_required: bool
    build_test_required: bool
    human_review_required: bool
    runtime_mutation_allowed: bool
    productization_allowed_now: bool
    bridge_ready: bool

    def __post_init__(self) -> None:
        if not self.bridge_id:
            raise ValueError("bridge_id must be non-empty")
        if not self.source_language:
            raise ValueError("source_language must be non-empty")
        if not self.target_language:
            raise ValueError("target_language must be non-empty")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.artifact_ref_required is not True:
            raise ValueError("artifact_ref_required must be True")
        if self.semantic_preservation_required is not True:
            raise ValueError("semantic_preservation_required must be True")
        if self.build_test_required is not True:
            raise ValueError("build_test_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if self.bridge_ready is not True:
            raise ValueError("bridge_ready must be True")


@dataclass(frozen=True, slots=True)
class LanguageBridgeContract:
    contract_id: str
    bridges: Tuple[LanguageBridgeEntry, ...]
    artifact_language_contract_ready: bool
    language_bridge_models_ready: bool
    source_bound_required: bool
    artifact_ref_required: bool
    build_test_required: bool
    human_review_required: bool
    runtime_mutation_allowed: bool
    productization_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if not self.bridges:
            raise ValueError("bridges must be non-empty")
        bridge_ids = {bridge.bridge_id for bridge in self.bridges}
        if len(bridge_ids) != len(self.bridges):
            raise ValueError("bridge_id values must be unique")
        if self.artifact_language_contract_ready is not True:
            raise ValueError("artifact_language_contract_ready must be True")
        if self.language_bridge_models_ready is not True:
            raise ValueError("language_bridge_models_ready must be True")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.artifact_ref_required is not True:
            raise ValueError("artifact_ref_required must be True")
        if self.build_test_required is not True:
            raise ValueError("build_test_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if not all(bridge.bridge_ready for bridge in self.bridges):
            raise ValueError("all bridges must be ready")


def build_language_bridge_contract() -> LanguageBridgeContract:
    artifact_language = build_artifact_language_contract()

    bridges = (
        LanguageBridgeEntry(
            bridge_id="language_bridge_python_to_test_001",
            bridge_kind="test_language_bridge",
            source_language="python",
            target_language="pytest",
            source_bound=True,
            artifact_ref_required=True,
            semantic_preservation_required=True,
            build_test_required=True,
            human_review_required=True,
            runtime_mutation_allowed=False,
            productization_allowed_now=False,
            bridge_ready=True,
        ),
        LanguageBridgeEntry(
            bridge_id="language_bridge_python_to_markdown_001",
            bridge_kind="documentation_language_bridge",
            source_language="python",
            target_language="markdown",
            source_bound=True,
            artifact_ref_required=True,
            semantic_preservation_required=True,
            build_test_required=True,
            human_review_required=True,
            runtime_mutation_allowed=False,
            productization_allowed_now=False,
            bridge_ready=True,
        ),
        LanguageBridgeEntry(
            bridge_id="language_bridge_json_to_config_review_001",
            bridge_kind="config_language_bridge",
            source_language="json",
            target_language="config_review",
            source_bound=True,
            artifact_ref_required=True,
            semantic_preservation_required=True,
            build_test_required=True,
            human_review_required=True,
            runtime_mutation_allowed=False,
            productization_allowed_now=False,
            bridge_ready=True,
        ),
    )

    return LanguageBridgeContract(
        contract_id="language_bridge_contract_phase_6_7_001",
        bridges=bridges,
        artifact_language_contract_ready=artifact_language.artifact_language_models_ready,
        language_bridge_models_ready=True,
        source_bound_required=True,
        artifact_ref_required=True,
        build_test_required=True,
        human_review_required=True,
        runtime_mutation_allowed=False,
        productization_allowed_now=False,
    )
