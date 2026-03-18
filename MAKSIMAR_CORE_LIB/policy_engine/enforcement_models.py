from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


Decision = Literal["allow", "deny", "review"]


@dataclass(frozen=True, slots=True)
class EnforcementRequest:
    """Canonical policy enforcement request."""

    policy_name: str
    operation: str
    context: dict[str, Any]


@dataclass(frozen=True, slots=True)
class EnforcementReason:
    """Single reason contributing to enforcement decision."""

    path: str
    message: str


@dataclass(slots=True)
class EnforcementResult:
    """Canonical policy enforcement result."""

    decision: Decision
    reasons: list[EnforcementReason] = field(default_factory=list)

    def add_reason(self, path: str, message: str) -> None:
        """Append human-readable decision reason."""
        self.reasons.append(
            EnforcementReason(
                path=path,
                message=message,
            )
        )
