from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ACTIVATION_LEVELS = (
    "LEVEL_0_CONTRACT_ONLY",
    "LEVEL_1_VISIBLE_READ_ONLY",
    "LEVEL_2_INSTALLED",
    "LEVEL_3_SMOKE_PROBED",
    "LEVEL_4_OPERATOR_ENABLED_READ_ONLY",
    "LEVEL_5_APPROVAL_GATED_ACTIONS",
    "LEVEL_6_AUTOMATION_WITH_GUARDS",
)


def _require_bool(value: bool, field_name: str) -> None:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class CapabilityActivationEntry:
    capability_id: str
    domain: str
    platform: str
    capability_present: bool
    contract_valid: bool
    dependency_installed: bool
    model_present: bool
    runtime_configured: bool
    smoke_passed: bool
    operator_enabled: bool
    policy_allowed: bool
    runtime_started: bool
    activation_level: str
    blocked_reason: str
    next_required_action: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.capability_id, "capability_id")
        _require_non_empty(self.domain, "domain")
        _require_non_empty(self.platform, "platform")
        _require_non_empty(self.activation_level, "activation_level")
        _require_non_empty(self.blocked_reason, "blocked_reason")
        _require_non_empty(self.next_required_action, "next_required_action")

        for field_name in (
            "capability_present",
            "contract_valid",
            "dependency_installed",
            "model_present",
            "runtime_configured",
            "smoke_passed",
            "operator_enabled",
            "policy_allowed",
            "runtime_started",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if self.activation_level not in ACTIVATION_LEVELS:
            raise ValueError(f"unknown activation_level: {self.activation_level}")

        if not self.evidence_refs:
            raise ValueError("evidence_refs must not be empty")

        if self.runtime_started and not (
            self.capability_present
            and self.contract_valid
            and self.dependency_installed
            and self.runtime_configured
            and self.smoke_passed
            and self.operator_enabled
            and self.policy_allowed
        ):
            raise ValueError("runtime_started requires full readiness chain")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "domain": self.domain,
            "platform": self.platform,
            "capability_present": self.capability_present,
            "contract_valid": self.contract_valid,
            "dependency_installed": self.dependency_installed,
            "model_present": self.model_present,
            "runtime_configured": self.runtime_configured,
            "smoke_passed": self.smoke_passed,
            "operator_enabled": self.operator_enabled,
            "policy_allowed": self.policy_allowed,
            "runtime_started": self.runtime_started,
            "activation_level": self.activation_level,
            "blocked_reason": self.blocked_reason,
            "next_required_action": self.next_required_action,
            "evidence_refs": self.evidence_refs,
        }


@dataclass(frozen=True, slots=True)
class CapabilityActivationMatrix:
    matrix_id: str
    read_only: bool
    direct_execution_allowed: bool
    canonical_write_allowed: bool
    pc_control_allowed: bool
    phone_control_allowed: bool
    deployment_allowed: bool
    entries: tuple[CapabilityActivationEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.matrix_id, "matrix_id")
        if self.read_only is not True:
            raise ValueError("activation matrix must remain read-only")
        for field_name in (
            "direct_execution_allowed",
            "canonical_write_allowed",
            "pc_control_allowed",
            "phone_control_allowed",
            "deployment_allowed",
        ):
            if getattr(self, field_name) is not False:
                raise ValueError(f"{field_name} must remain false in readiness matrix")
        if not self.entries:
            raise ValueError("entries must not be empty")
        ids = [entry.capability_id for entry in self.entries]
        if len(ids) != len(set(ids)):
            raise ValueError("capability_id values must be unique")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "matrix_id": self.matrix_id,
            "read_only": self.read_only,
            "direct_execution_allowed": self.direct_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "phone_control_allowed": self.phone_control_allowed,
            "deployment_allowed": self.deployment_allowed,
            "entries": tuple(entry.to_read_model() for entry in self.entries),
        }


def _entry(
    capability_id: str,
    domain: str,
    platform: str,
    activation_level: str,
    blocked_reason: str,
    next_required_action: str,
    evidence_refs: tuple[str, ...],
    *,
    dependency_installed: bool = False,
    model_present: bool = False,
    runtime_configured: bool = False,
    smoke_passed: bool = False,
    operator_enabled: bool = False,
    policy_allowed: bool = False,
    runtime_started: bool = False,
) -> CapabilityActivationEntry:
    return CapabilityActivationEntry(
        capability_id=capability_id,
        domain=domain,
        platform=platform,
        capability_present=True,
        contract_valid=True,
        dependency_installed=dependency_installed,
        model_present=model_present,
        runtime_configured=runtime_configured,
        smoke_passed=smoke_passed,
        operator_enabled=operator_enabled,
        policy_allowed=policy_allowed,
        runtime_started=runtime_started,
        activation_level=activation_level,
        blocked_reason=blocked_reason,
        next_required_action=next_required_action,
        evidence_refs=evidence_refs,
    )


def build_default_capability_activation_matrix() -> CapabilityActivationMatrix:
    entries = (
        _entry(
            "voice_perception",
            "voice",
            "shared",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "voice perception contracts and preview are visible; live microphone/audio runtime remains parked",
            "complete full-green corrective pass, then start Windows Voice Edge runtime phase",
            (
                "MAKSIMAR_CORE_LIB/voice_perception/voice_perception_status_read_model.py",
                "tools/voice_perception_status_preview.py",
            ),
        ),
        _entry(
            "mobile_on_device_ai",
            "mobile_ai",
            "shared",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "PHASE 9 is closed as app-safe/read-only/proposal-only; runtime activation not started",
            "add controlled model asset/download gate before runtime probe",
            (
                "MAKSIMAR_SERVER/MEMORY_SYNC/mobile_capability_summary_builder.py",
                "tools/mobile_ai_status_preview.py",
            ),
        ),
        _entry(
            "android_junior_model",
            "mobile_ai",
            "android",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "android junior contract exists but model package is not downloaded and runtime is not started",
            "define Android model package manifest, storage path, hash, license, and smoke probe",
            (
                "ANDROID_SHELL/local_ai_runtime/android_local_ai_adapter_contract.py",
                "ANDROID_SHELL/local_ai_runtime/android_model_runtime_status.py",
            ),
        ),
        _entry(
            "ios_junior_model",
            "mobile_ai",
            "ios",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "iOS junior contract exists but model package is not downloaded and runtime is not started",
            "define iOS model package manifest, storage path, hash, license, and smoke probe",
            (
                "IOS_SHELL/local_ai_runtime/ios_local_ai_adapter_contract.py",
                "IOS_SHELL/local_ai_runtime/ios_model_runtime_status.py",
            ),
        ),
        _entry(
            "runtime_history_store",
            "memory",
            "server",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "history store is a read-only recall source; canonical write remains blocked",
            "bind memory recall router to explicit checked_sources reporting",
            (
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
                "runtime_history_store",
            ),
        ),
        _entry(
            "ollama_local_engine",
            "model_runtime",
            "server",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "Ollama is treated as local model engine; action/tool calls remain proposals",
            "keep local engine status visible, then add smoke-probed activation evidence",
            (
                "MAKSIMAR_CORE_LIB/ai_orchestration/model_profile_registry_contract.py",
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
            ),
        ),
        _entry(
            "pc_control_candidates",
            "pc_control",
            "windows",
            "LEVEL_0_CONTRACT_ONLY",
            "PC control remains blocked until approval-gated action library and computer-use phase",
            "do not enable before allowlist, audit log, owner approval, and rollback constraints",
            (
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
                "MAKSIMAR_CORE_LIB/security_layer",
            ),
        ),
        _entry(
            "windows_voice_edge_runtime",
            "voice",
            "windows",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "Windows Voice Edge is planned as a localhost/trust-boundary runtime edge; live audio runtime is not started by this matrix",
            "inventory existing Windows audio/STT/TTS tools, then add an explicit smoke-probed Windows Voice Edge runtime batch",
            (
                "MAKSIMAR_CORE_LIB/voice_perception/voice_perception_status_read_model.py",
                "tools/runtime_activation_matrix_preview.py",
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
            ),
        ),
        _entry(
            "push_to_talk_stt_live",
            "voice",
            "windows",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "Push-to-Talk STT is the safe first live voice mode; always-listening remains parked",
            "bind existing faster-whisper/PTT smoke path through Windows Voice Edge with operator-only local activation",
            (
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
                "MAKSIMAR_RUNTIME/venvs/faster_whisper_stt",
            ),
        ),
        _entry(
            "screen_observer_readonly",
            "perception",
            "windows",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "screen observer remains read-only and must not perform keyboard/mouse/PC actions",
            "surface screen observer readiness in activation matrix before any action-library phase",
            (
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
                "MAKSIMAR_CORE_LIB/security_layer",
            ),
        ),
        _entry(
            "retrieval_readonly_tools",
            "retrieval",
            "server",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "retrieval tools are available only as read-only evidence surfaces; runtime/container start remains blocked",
            "make JARVIS expose mgrep/sqlite_vec/qdrant readiness as checked sources",
            (
                "MAKSIMAR_CORE_LIB/retrieval_backend",
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
            ),
        ),
        _entry(
            "mgrep_readonly",
            "retrieval",
            "server",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "mgrep is a read-only project search tool and must not mutate repository/runtime state",
            "keep project/source search routed to mgrep/repo_search before Ollama",
            (
                "MAKSIMAR_CORE_LIB/retrieval_backend",
                "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
            ),
        ),
        _entry(
            "sqlite_vec_readonly",
            "retrieval",
            "server",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "sqlite_vec is treated as read-only retrieval capability until explicit runtime/storage gate",
            "expose installed/configured/smoke state through later retrieval readiness probe",
            (
                "MAKSIMAR_CORE_LIB/retrieval_backend",
                "tools/runtime_activation_matrix_preview.py",
            ),
        ),
        _entry(
            "qdrant_readonly_status",
            "retrieval",
            "server",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "qdrant status can be inspected read-only; qdrant container/runtime start remains blocked",
            "add explicit qdrant readiness probe before any container start approval",
            (
                "MAKSIMAR_CORE_LIB/retrieval_backend",
                "CONTAINER_DEPLOYMENT",
            ),
        ),
        _entry(
            "approval_gates",
            "security",
            "shared",
            "LEVEL_1_VISIBLE_READ_ONLY",
            "approval gates are visible and required; bypass is not allowed",
            "connect every action-capable runtime edge to allowlist, audit, approval, and rollback evidence before activation",
            (
                "MAKSIMAR_CORE_LIB/security_layer",
                "MAKSIMAR_CORE_LIB/execution_control",
            ),
        ),
        _entry(
            "network_sync_gates",
            "network",
            "shared",
            "LEVEL_0_CONTRACT_ONLY",
            "network/sync gates remain blocked for public exposure, tunnels, and hidden remote control",
            "define localhost-only trust boundary before any sync/runtime exposure",
            (
                "MAKSIMAR_CORE_LIB/network_security",
                "MAKSIMAR_SERVER/MEMORY_SYNC",
            ),
        ),
    )
    return CapabilityActivationMatrix(
        matrix_id="jarvis_capability_activation_matrix_v0_1",
        read_only=True,
        direct_execution_allowed=False,
        canonical_write_allowed=False,
        pc_control_allowed=False,
        phone_control_allowed=False,
        deployment_allowed=False,
        entries=entries,
    )
