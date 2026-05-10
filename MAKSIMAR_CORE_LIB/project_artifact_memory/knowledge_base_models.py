from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

KnowledgeBaseKind = Literal["project_docs", "engineering_docs", "regulatory_docs"]

_KNOWLEDGE_BASE_ID_PATTERN = re.compile(r"^knowledge_base_[a-z][a-z0-9_]*_[0-9]{3}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class KnowledgeBaseEntry:
    knowledge_base_id: str
    knowledge_base_kind: KnowledgeBaseKind
    storage_node_id: str
    retrieval_source_id: str
    source_ref: str
    source_bound: bool
    versioned: bool
    read_only: bool
    retrieval_enabled: bool
    runtime_write_allowed: bool
    dashboard_visible: bool
    knowledge_base_ready: bool
    description: str

    def __post_init__(self) -> None:
        knowledge_base_id = _ensure_non_empty_str(self.knowledge_base_id, "knowledge_base_id")
        if not _KNOWLEDGE_BASE_ID_PATTERN.fullmatch(knowledge_base_id):
            raise ValueError(f"Invalid knowledge_base_id: {knowledge_base_id}")

        for field_name in (
            "storage_node_id",
            "retrieval_source_id",
            "source_ref",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "source_bound",
            "versioned",
            "read_only",
            "retrieval_enabled",
            "runtime_write_allowed",
            "dashboard_visible",
            "knowledge_base_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.versioned:
            raise ValueError("versioned must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.runtime_write_allowed:
            raise ValueError("runtime_write_allowed must be False in Batch 1")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.knowledge_base_ready:
            raise ValueError("knowledge_base_ready must be True")


@dataclass(frozen=True, slots=True)
class KnowledgeBaseContract:
    total_knowledge_bases: int
    ready_knowledge_bases: int
    source_bound_knowledge_bases: int
    versioned_knowledge_bases: int
    read_only_knowledge_bases: int
    retrieval_enabled_knowledge_bases: int
    runtime_write_allowed_knowledge_bases: int
    dashboard_visible_knowledge_bases: int
    entries: tuple[KnowledgeBaseEntry, ...]

    def __post_init__(self) -> None:
        if self.total_knowledge_bases != len(self.entries):
            raise ValueError("total_knowledge_bases must match entries length")
        if self.total_knowledge_bases <= 0:
            raise ValueError("total_knowledge_bases must be >= 1")

        expected = {
            "ready_knowledge_bases": sum(1 for entry in self.entries if entry.knowledge_base_ready),
            "source_bound_knowledge_bases": sum(1 for entry in self.entries if entry.source_bound),
            "versioned_knowledge_bases": sum(1 for entry in self.entries if entry.versioned),
            "read_only_knowledge_bases": sum(1 for entry in self.entries if entry.read_only),
            "retrieval_enabled_knowledge_bases": sum(1 for entry in self.entries if entry.retrieval_enabled),
            "runtime_write_allowed_knowledge_bases": sum(1 for entry in self.entries if entry.runtime_write_allowed),
            "dashboard_visible_knowledge_bases": sum(1 for entry in self.entries if entry.dashboard_visible),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_knowledge_bases != self.total_knowledge_bases:
            raise ValueError("all knowledge bases must be ready")
        if self.source_bound_knowledge_bases != self.total_knowledge_bases:
            raise ValueError("all knowledge bases must be source-bound")
        if self.versioned_knowledge_bases != self.total_knowledge_bases:
            raise ValueError("all knowledge bases must be versioned")
        if self.read_only_knowledge_bases != self.total_knowledge_bases:
            raise ValueError("all knowledge bases must be read-only")
        if self.runtime_write_allowed_knowledge_bases != 0:
            raise ValueError("runtime writes must remain blocked in Batch 1")


def build_knowledge_base_contract() -> KnowledgeBaseContract:
    entries = (
        KnowledgeBaseEntry(
            knowledge_base_id="knowledge_base_project_docs_001",
            knowledge_base_kind="project_docs",
            storage_node_id="storage_node_retrieval_index",
            retrieval_source_id="retrieval_source_project_docs",
            source_ref="source_ref_project_docs_placeholder_v1",
            source_bound=True,
            versioned=True,
            read_only=True,
            retrieval_enabled=True,
            runtime_write_allowed=False,
            dashboard_visible=True,
            knowledge_base_ready=True,
            description="Read-only project documentation knowledge base placeholder.",
        ),
        KnowledgeBaseEntry(
            knowledge_base_id="knowledge_base_engineering_docs_001",
            knowledge_base_kind="engineering_docs",
            storage_node_id="storage_node_retrieval_index",
            retrieval_source_id="retrieval_source_engineering_docs",
            source_ref="source_ref_engineering_docs_placeholder_v1",
            source_bound=True,
            versioned=True,
            read_only=True,
            retrieval_enabled=True,
            runtime_write_allowed=False,
            dashboard_visible=True,
            knowledge_base_ready=True,
            description="Read-only engineering documentation knowledge base placeholder.",
        ),
        KnowledgeBaseEntry(
            knowledge_base_id="knowledge_base_regulatory_docs_001",
            knowledge_base_kind="regulatory_docs",
            storage_node_id="storage_node_retrieval_index",
            retrieval_source_id="retrieval_source_regulatory_docs",
            source_ref="source_ref_regulatory_docs_placeholder_v1",
            source_bound=True,
            versioned=True,
            read_only=True,
            retrieval_enabled=True,
            runtime_write_allowed=False,
            dashboard_visible=True,
            knowledge_base_ready=True,
            description="Read-only regulatory documentation knowledge base placeholder.",
        ),
    )

    return KnowledgeBaseContract(
        total_knowledge_bases=len(entries),
        ready_knowledge_bases=sum(1 for entry in entries if entry.knowledge_base_ready),
        source_bound_knowledge_bases=sum(1 for entry in entries if entry.source_bound),
        versioned_knowledge_bases=sum(1 for entry in entries if entry.versioned),
        read_only_knowledge_bases=sum(1 for entry in entries if entry.read_only),
        retrieval_enabled_knowledge_bases=sum(1 for entry in entries if entry.retrieval_enabled),
        runtime_write_allowed_knowledge_bases=sum(1 for entry in entries if entry.runtime_write_allowed),
        dashboard_visible_knowledge_bases=sum(1 for entry in entries if entry.dashboard_visible),
        entries=entries,
    )
