from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VaultAccessStatus(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"


@dataclass(frozen=True, slots=True)
class VaultAccessRequest:
    request_id: str
    subject_id: str
    secret_ref: str
    purpose: str
    approval_present: bool

    def __post_init__(self) -> None:
        for field_name, value in (
            ("request_id", self.request_id),
            ("subject_id", self.subject_id),
            ("secret_ref", self.secret_ref),
            ("purpose", self.purpose),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if self.secret_ref.startswith("/") or ".." in self.secret_ref.split("/"):
            raise ValueError("secret_ref must be a safe vault-relative reference")


@dataclass(frozen=True, slots=True)
class VaultAccessDecision:
    request_id: str
    status: VaultAccessStatus
    secret_material_exposed: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id must not be empty")
        if not isinstance(self.status, VaultAccessStatus):
            raise TypeError("status must be VaultAccessStatus")
        if self.secret_material_exposed:
            raise ValueError("vault boundary must never expose secret material")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")


def evaluate_vault_access(request: VaultAccessRequest) -> VaultAccessDecision:
    if not request.approval_present:
        return VaultAccessDecision(
            request_id=request.request_id,
            status=VaultAccessStatus.DENIED,
            secret_material_exposed=False,
            reason_codes=("vault_approval_missing",),
        )

    return VaultAccessDecision(
        request_id=request.request_id,
        status=VaultAccessStatus.ALLOWED,
        secret_material_exposed=False,
        reason_codes=("vault_access_metadata_allowed",),
    )
