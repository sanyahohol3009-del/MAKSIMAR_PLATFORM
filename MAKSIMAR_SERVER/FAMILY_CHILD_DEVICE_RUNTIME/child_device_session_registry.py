from __future__ import annotations

from dataclasses import dataclass, field

from MAKSIMAR_CORE_LIB.family_child_device_control.child_device_profile_contract import (
    ChildDeviceProfileContract,
)


@dataclass(frozen=True)
class ChildDeviceSessionRecord:
    profile: ChildDeviceProfileContract

    def __post_init__(self) -> None:
        if not self.profile.is_child_managed():
            raise ValueError("profile must be child-managed")
        if self.profile.dashboard_bypass_allowed:
            raise ValueError("dashboard bypass is forbidden")


@dataclass
class ChildDeviceSessionRegistry:
    _records: dict[str, ChildDeviceSessionRecord] = field(default_factory=dict)

    def register(self, profile: ChildDeviceProfileContract) -> ChildDeviceSessionRecord:
        record = ChildDeviceSessionRecord(profile=profile)
        if profile.child_device_id in self._records:
            raise ValueError(f"child device already registered: {profile.child_device_id}")
        self._records[profile.child_device_id] = record
        return record

    def get(self, child_device_id: str) -> ChildDeviceSessionRecord:
        if child_device_id not in self._records:
            raise KeyError(f"unknown child device: {child_device_id}")
        return self._records[child_device_id]

    def contains(self, child_device_id: str) -> bool:
        return child_device_id in self._records

    def list_child_device_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._records))

    def to_read_model(self) -> dict[str, object]:
        return {
            "runtime": "FAMILY_CHILD_DEVICE_RUNTIME",
            "child_device_count": len(self._records),
            "child_device_ids": self.list_child_device_ids(),
            "dashboard_section": "Family / Children",
            "dashboard_bypass_allowed": False,
        }
