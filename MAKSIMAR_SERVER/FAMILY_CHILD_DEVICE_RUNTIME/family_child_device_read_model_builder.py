from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_device_audit_runtime import (
    ChildDeviceAuditRuntime,
)
from MAKSIMAR_SERVER.FAMILY_CHILD_DEVICE_RUNTIME.child_device_session_registry import (
    ChildDeviceSessionRegistry,
)


@dataclass(frozen=True)
class FamilyChildDeviceReadModelBuilder:
    session_registry: ChildDeviceSessionRegistry
    audit_runtime: ChildDeviceAuditRuntime

    def build(self) -> dict[str, object]:
        return {
            "dashboard_section": "Family / Children",
            "runtime": "FAMILY_CHILD_DEVICE_RUNTIME",
            "normal_phone_window": False,
            "guardian_authority_required": True,
            "audit_required": True,
            "visible_child_device_status_required": True,
            "dashboard_bypass_allowed": False,
            "runtime_execution_allowed": False,
            "platform_api_calls_allowed": False,
            "session_registry": self.session_registry.to_read_model(),
            "audit": self.audit_runtime.to_read_model(),
        }
