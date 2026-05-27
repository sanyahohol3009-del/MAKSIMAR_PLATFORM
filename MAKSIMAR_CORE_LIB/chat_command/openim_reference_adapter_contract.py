from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_ADAPTER_STATES = ("reference_only", "quarantined", "adapter_contract_declared", "blocked")
_ALLOWED_ADAPTER_ROLES = ("message_transport_reference", "runtime_adapter_candidate", "research_only")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


@dataclass(frozen=True)
class OpenIMReferenceAdapterContract:
    """OpenIM / messenger reference adapter boundary.

    Contract only. External messenger projects remain adapter/reference material.
    They do not define MAKSIMAR chat truth, do not enter immutable core, do not
    execute commands, and are not downloaded or run in this batch.
    """

    adapter_id: str
    adapter_name: str
    upstream_project_ref: str
    adapter_state: str
    adapter_role: str
    chat_truth_source_id: str
    quarantine_required: bool
    policy_gate_required: bool
    external_download_allowed: bool
    runtime_execution_allowed: bool
    source_of_truth_allowed: bool
    direct_command_execution_allowed: bool
    core_import_allowed: bool
    network_access_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "adapter_id", _ensure_non_empty(self.adapter_id, "adapter_id"))
        object.__setattr__(self, "adapter_name", _ensure_non_empty(self.adapter_name, "adapter_name"))
        object.__setattr__(self, "upstream_project_ref", _ensure_non_empty(self.upstream_project_ref, "upstream_project_ref"))
        object.__setattr__(self, "adapter_state", _ensure_allowed(self.adapter_state, "adapter_state", _ALLOWED_ADAPTER_STATES))
        object.__setattr__(self, "adapter_role", _ensure_allowed(self.adapter_role, "adapter_role", _ALLOWED_ADAPTER_ROLES))
        object.__setattr__(self, "chat_truth_source_id", _ensure_non_empty(self.chat_truth_source_id, "chat_truth_source_id"))

        if not self.quarantine_required:
            raise ValueError("quarantine_required must be True")
        if not self.policy_gate_required:
            raise ValueError("policy_gate_required must be True")
        if self.external_download_allowed:
            raise ValueError("external_download_allowed must be False in BATCH 3.3")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.source_of_truth_allowed:
            raise ValueError("source_of_truth_allowed must be False")
        if self.direct_command_execution_allowed:
            raise ValueError("direct_command_execution_allowed must be False")
        if self.core_import_allowed:
            raise ValueError("core_import_allowed must be False")
        if self.network_access_allowed:
            raise ValueError("network_access_allowed must be False")

        if self.chat_truth_source_id != "MAKSIMAR_CHAT_COMMAND_TRUTH":
            raise ValueError("chat_truth_source_id must remain MAKSIMAR_CHAT_COMMAND_TRUTH")


def build_research_only_messenger_reference(adapter_id: str, adapter_name: str, upstream_project_ref: str) -> OpenIMReferenceAdapterContract:
    return OpenIMReferenceAdapterContract(
        adapter_id=adapter_id,
        adapter_name=adapter_name,
        upstream_project_ref=upstream_project_ref,
        adapter_state="reference_only",
        adapter_role="research_only",
        chat_truth_source_id="MAKSIMAR_CHAT_COMMAND_TRUTH",
        quarantine_required=True,
        policy_gate_required=True,
        external_download_allowed=False,
        runtime_execution_allowed=False,
        source_of_truth_allowed=False,
        direct_command_execution_allowed=False,
        core_import_allowed=False,
        network_access_allowed=False,
    )
