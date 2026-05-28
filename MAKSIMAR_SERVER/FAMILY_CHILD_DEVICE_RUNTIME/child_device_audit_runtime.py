from __future__ import annotations

from dataclasses import dataclass, field

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_audit_contract import (
    ChildDeviceAuditContract,
)


@dataclass
class ChildDeviceAuditRuntime:
    _events: dict[str, ChildDeviceAuditContract] = field(default_factory=dict)

    def append(self, event: ChildDeviceAuditContract) -> ChildDeviceAuditContract:
        if event.audit_event_id in self._events:
            raise ValueError(f"audit event already exists: {event.audit_event_id}")
        if event.dashboard_bypass_allowed:
            raise ValueError("dashboard bypass is forbidden")
        if event.contains_pixel_payload:
            raise ValueError("pixel payload is forbidden")
        self._events[event.audit_event_id] = event
        return event

    def list_event_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._events))

    def to_read_model(self) -> dict[str, object]:
        return {
            "runtime": "CHILD_DEVICE_AUDIT_RUNTIME",
            "append_only": True,
            "event_count": len(self._events),
            "event_ids": self.list_event_ids(),
            "visible_on_child_device_required": True,
        }
