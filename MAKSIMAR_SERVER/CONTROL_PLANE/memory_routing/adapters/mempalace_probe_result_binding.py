from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

_PROBE_REPORT = Path("EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_controlled_real_backend_probe_report.json")
_BINDING_REPORT = Path("EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_probe_result_binding_report.json")


@dataclass(frozen=True, slots=True)
class MemPalaceProbeResultBinding:
    binding_id: str
    probe_report_path: str
    controlled_probe_success: bool
    real_import_verified: bool
    vendor_venv_used: bool
    denied_env_scrubbed: bool
    network_blocked: bool
    subprocess_blocked: bool
    destructive_filesystem_blocked: bool
    read_only_adapter_binding_allowed: bool
    full_real_backend_enablement_allowed: bool
    general_real_backend_query_allowed: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    evidence_pack: Tuple[str, ...]
    binding_ready: bool

    def __post_init__(self) -> None:
        if not self.binding_id:
            raise ValueError("binding_id must be non-empty")
        if not self.probe_report_path:
            raise ValueError("probe_report_path must be non-empty")
        if not self.evidence_pack:
            raise ValueError("evidence_pack must be non-empty")

        required_true = (
            "controlled_probe_success",
            "real_import_verified",
            "vendor_venv_used",
            "denied_env_scrubbed",
            "network_blocked",
            "subprocess_blocked",
            "destructive_filesystem_blocked",
            "read_only_adapter_binding_allowed",
            "binding_ready",
        )
        for field_name in required_true:
            if getattr(self, field_name) is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = (
            "full_real_backend_enablement_allowed",
            "general_real_backend_query_allowed",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
        )
        for field_name in required_false:
            if getattr(self, field_name) is not False:
                raise ValueError(f"{field_name} must be False")


def _load_probe_report() -> dict[str, object]:
    if not _PROBE_REPORT.exists():
        raise FileNotFoundError(f"probe report missing: {_PROBE_REPORT}")
    return json.loads(_PROBE_REPORT.read_text(encoding="utf-8"))


def build_mempalace_probe_result_binding() -> MemPalaceProbeResultBinding:
    report = _load_probe_report()
    child = report["child_payload"]

    real_import_verified = (
        child["import_success"] is True
        and "EXTERNAL_BACKENDS/mempalace/source/mempalace" in str(child["module_file"])
    )

    vendor_venv_used = "EXTERNAL_BACKENDS/mempalace/venv/bin/python" in str(report["venv_python"])

    binding_ready = (
        report["controlled_probe_success"] is True
        and real_import_verified
        and vendor_venv_used
        and child["denied_env_present_after_scrub"] == []
        and child["network_operations_blocked"] is True
        and child["subprocess_operations_blocked"] is True
        and child["destructive_filesystem_operations_blocked"] is True
        and report["canonical_write_allowed"] is False
        and report["runtime_mutation_allowed"] is False
        and report["full_real_backend_enablement_allowed"] is False
        and report["general_real_backend_query_allowed"] is False
    )

    return MemPalaceProbeResultBinding(
        binding_id="mempalace_probe_result_binding_001",
        probe_report_path=str(_PROBE_REPORT),
        controlled_probe_success=bool(report["controlled_probe_success"]),
        real_import_verified=real_import_verified,
        vendor_venv_used=vendor_venv_used,
        denied_env_scrubbed=child["denied_env_present_after_scrub"] == [],
        network_blocked=bool(child["network_operations_blocked"]),
        subprocess_blocked=bool(child["subprocess_operations_blocked"]),
        destructive_filesystem_blocked=bool(child["destructive_filesystem_operations_blocked"]),
        read_only_adapter_binding_allowed=True,
        full_real_backend_enablement_allowed=False,
        general_real_backend_query_allowed=False,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        evidence_pack=(
            "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_controlled_real_backend_probe_report.json",
            "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_real_backend_approval_envelope_report.json",
            "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_vendor_gate_report.json",
        ),
        binding_ready=binding_ready,
    )


def build_mempalace_probe_result_binding_preview() -> dict[str, object]:
    binding = build_mempalace_probe_result_binding()

    return {
        "binding_id": binding.binding_id,
        "binding_ready": binding.binding_ready,
        "controlled_probe_success": binding.controlled_probe_success,
        "real_import_verified": binding.real_import_verified,
        "vendor_venv_used": binding.vendor_venv_used,
        "denied_env_scrubbed": binding.denied_env_scrubbed,
        "network_blocked": binding.network_blocked,
        "subprocess_blocked": binding.subprocess_blocked,
        "destructive_filesystem_blocked": binding.destructive_filesystem_blocked,
        "read_only_adapter_binding_allowed": binding.read_only_adapter_binding_allowed,
        "full_real_backend_enablement_allowed": binding.full_real_backend_enablement_allowed,
        "general_real_backend_query_allowed": binding.general_real_backend_query_allowed,
        "canonical_write_allowed": binding.canonical_write_allowed,
        "runtime_mutation_allowed": binding.runtime_mutation_allowed,
        "evidence_pack": binding.evidence_pack,
    }


def write_mempalace_probe_result_binding_report() -> Path:
    payload = build_mempalace_probe_result_binding_preview()
    _BINDING_REPORT.parent.mkdir(parents=True, exist_ok=True)
    _BINDING_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return _BINDING_REPORT
