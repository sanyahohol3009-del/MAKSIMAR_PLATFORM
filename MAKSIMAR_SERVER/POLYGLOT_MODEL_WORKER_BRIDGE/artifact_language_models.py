from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


ArtifactLanguage = Literal["python", "typescript", "javascript", "markdown", "json", "yaml", "sql", "shell"]
ArtifactScript = Literal["latin", "cyrillic", "mixed", "code"]
ArtifactLanguageRole = Literal["source_code", "test_code", "documentation", "config", "query", "script"]


@dataclass(frozen=True, slots=True)
class ArtifactLanguageEntry:
    entry_id: str
    artifact_language: ArtifactLanguage
    script: ArtifactScript
    role: ArtifactLanguageRole
    source_bound: bool
    artifact_ref_required: bool
    build_required: bool
    test_required: bool
    human_review_required: bool
    productization_allowed_now: bool
    entry_ready: bool

    def __post_init__(self) -> None:
        if not self.entry_id:
            raise ValueError("entry_id must be non-empty")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.artifact_ref_required is not True:
            raise ValueError("artifact_ref_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if self.entry_ready is not True:
            raise ValueError("entry_ready must be True")


@dataclass(frozen=True, slots=True)
class ArtifactLanguageContract:
    contract_id: str
    entries: Tuple[ArtifactLanguageEntry, ...]
    artifact_language_models_ready: bool
    source_bound_required: bool
    artifact_ref_required: bool
    build_test_route_required: bool
    human_review_required: bool
    productization_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if not self.entries:
            raise ValueError("entries must be non-empty")
        entry_ids = {entry.entry_id for entry in self.entries}
        if len(entry_ids) != len(self.entries):
            raise ValueError("entry_id values must be unique")
        if self.artifact_language_models_ready is not True:
            raise ValueError("artifact_language_models_ready must be True")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.artifact_ref_required is not True:
            raise ValueError("artifact_ref_required must be True")
        if self.build_test_route_required is not True:
            raise ValueError("build_test_route_required must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if not all(entry.entry_ready for entry in self.entries):
            raise ValueError("all entries must be ready")


def build_artifact_language_contract() -> ArtifactLanguageContract:
    entries = (
        ArtifactLanguageEntry(
            entry_id="artifact_language_python_source_001",
            artifact_language="python",
            script="code",
            role="source_code",
            source_bound=True,
            artifact_ref_required=True,
            build_required=True,
            test_required=True,
            human_review_required=True,
            productization_allowed_now=False,
            entry_ready=True,
        ),
        ArtifactLanguageEntry(
            entry_id="artifact_language_python_test_001",
            artifact_language="python",
            script="code",
            role="test_code",
            source_bound=True,
            artifact_ref_required=True,
            build_required=True,
            test_required=True,
            human_review_required=True,
            productization_allowed_now=False,
            entry_ready=True,
        ),
        ArtifactLanguageEntry(
            entry_id="artifact_language_markdown_doc_001",
            artifact_language="markdown",
            script="mixed",
            role="documentation",
            source_bound=True,
            artifact_ref_required=True,
            build_required=False,
            test_required=True,
            human_review_required=True,
            productization_allowed_now=False,
            entry_ready=True,
        ),
        ArtifactLanguageEntry(
            entry_id="artifact_language_json_config_001",
            artifact_language="json",
            script="code",
            role="config",
            source_bound=True,
            artifact_ref_required=True,
            build_required=False,
            test_required=True,
            human_review_required=True,
            productization_allowed_now=False,
            entry_ready=True,
        ),
        ArtifactLanguageEntry(
            entry_id="artifact_language_shell_script_001",
            artifact_language="shell",
            script="code",
            role="script",
            source_bound=True,
            artifact_ref_required=True,
            build_required=True,
            test_required=True,
            human_review_required=True,
            productization_allowed_now=False,
            entry_ready=True,
        ),
    )

    return ArtifactLanguageContract(
        contract_id="artifact_language_contract_phase_6_7_001",
        entries=entries,
        artifact_language_models_ready=True,
        source_bound_required=True,
        artifact_ref_required=True,
        build_test_route_required=True,
        human_review_required=True,
        productization_allowed_now=False,
    )
