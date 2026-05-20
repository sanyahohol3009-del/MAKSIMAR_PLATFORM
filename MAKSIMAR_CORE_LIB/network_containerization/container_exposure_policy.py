from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ContainerExposurePolicy:
    public_exposure_allowed: bool
    bind_localhost_only: bool
    exposed_ports: tuple[int, ...]
    published_ports: tuple[int, ...]
    internal_network_only: bool
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.public_exposure_allowed:
            raise ValueError("public_exposure_allowed must remain false")
        if not self.bind_localhost_only:
            raise ValueError("bind_localhost_only must remain true")
        _validate_ports("exposed_ports", self.exposed_ports)
        _validate_ports("published_ports", self.published_ports)
        if self.published_ports:
            raise ValueError("published_ports must remain empty")
        if not self.internal_network_only:
            raise ValueError("internal_network_only must remain true")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "public_exposure_allowed": self.public_exposure_allowed,
            "bind_localhost_only": self.bind_localhost_only,
            "exposed_ports": self.exposed_ports,
            "published_ports": self.published_ports,
            "internal_network_only": self.internal_network_only,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_no_public_exposure_policy() -> ContainerExposurePolicy:
    return ContainerExposurePolicy(
        public_exposure_allowed=False,
        bind_localhost_only=True,
        exposed_ports=(),
        published_ports=(),
        internal_network_only=True,
        dashboard_safe=True,
        reason_codes=("no_public_exposure_by_default", "internal_network_only"),
    )


def _validate_ports(field_name: str, ports: tuple[int, ...]) -> None:
    if not isinstance(ports, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    for port in ports:
        if not isinstance(port, int):
            raise TypeError(f"{field_name} values must be integers")
        if port < 1 or port > 65535:
            raise ValueError(f"{field_name} values must be valid TCP/UDP port numbers")


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
