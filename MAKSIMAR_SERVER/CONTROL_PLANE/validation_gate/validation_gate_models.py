from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.payload_policy_models import PayloadClass
from MAKSIMAR_CORE_LIB.validation_policy import (
    ValidationErrorCode,
    ValidationTaskClass,
    ValidationTier,
)


ValidationGateStatus = Literal[
    "passed",
    "rejected",
]


@dataclass(frozen=True, slots=True)
class ServerValidationGateEntry:
    """Server-side validation gate execution entry."""

    request_id: str
    task_class: ValidationTaskClass
    payload_class: PayloadClass
    resolved_validation_tier: ValidationTier
    l1_header_passed: bool
    l2_schema_passed: bool
    l3_deep_passed: bool
    final_status: ValidationGateStatus
    blocking_error_code: ValidationErrorCode | str
    description: str

    def __post_init__(self) -> None:
        """Validate validation gate invariants."""
        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.request_id}")

        if self.final_status == "passed":
            if self.blocking_error_code != "":
                raise ValueError(
                    f"passed validation gate entry must not have blocking_error_code: {self.request_id}"
                )

            if not self.l1_header_passed:
                raise ValueError(
                    f"passed validation gate entry must pass L1: {self.request_id}"
                )

            if self.resolved_validation_tier == "L1_HEADER":
                if self.l2_schema_passed:
                    raise ValueError(
                        f"L1_HEADER entry must not mark L2 as passed: {self.request_id}"
                    )
                if self.l3_deep_passed:
                    raise ValueError(
                        f"L1_HEADER entry must not mark L3 as passed: {self.request_id}"
                    )

            if self.resolved_validation_tier == "L2_SCHEMA":
                if not self.l2_schema_passed:
                    raise ValueError(
                        f"L2_SCHEMA entry must pass L2: {self.request_id}"
                    )
                # Важно:
                # для некоторых L2-путей policy может дополнительно требовать L3
                # (например heavy_artifact), поэтому l3_deep_passed здесь
                # допускается как False, так и True.

            if self.resolved_validation_tier == "L3_DEEP":
                if not self.l2_schema_passed:
                    raise ValueError(
                        f"L3_DEEP entry must pass L2: {self.request_id}"
                    )
                if not self.l3_deep_passed:
                    raise ValueError(
                        f"L3_DEEP entry must pass L3: {self.request_id}"
                    )

        if self.final_status == "rejected":
            if self.blocking_error_code == "":
                raise ValueError(
                    f"rejected validation gate entry must have blocking_error_code: {self.request_id}"
                )

            if self.blocking_error_code == "invalid_header":
                if self.l1_header_passed:
                    raise ValueError(
                        f"invalid_header rejection must fail L1: {self.request_id}"
                    )
                if self.l2_schema_passed:
                    raise ValueError(
                        f"invalid_header rejection must not pass L2: {self.request_id}"
                    )
                if self.l3_deep_passed:
                    raise ValueError(
                        f"invalid_header rejection must not pass L3: {self.request_id}"
                    )

            if self.blocking_error_code in (
                "invalid_schema",
                "forbidden_payload_embedding",
                "missing_payload_reference",
                "policy_rule_not_found",
            ):
                if not self.l1_header_passed:
                    raise ValueError(
                        f"{self.blocking_error_code} rejection must pass L1: {self.request_id}"
                    )
                if self.l3_deep_passed:
                    raise ValueError(
                        f"{self.blocking_error_code} rejection must not pass L3: {self.request_id}"
                    )

            if self.blocking_error_code == "deep_validation_failed":
                if not self.l1_header_passed:
                    raise ValueError(
                        f"deep_validation_failed rejection must pass L1: {self.request_id}"
                    )
                if not self.l2_schema_passed:
                    raise ValueError(
                        f"deep_validation_failed rejection must pass L2: {self.request_id}"
                    )
                if self.l3_deep_passed:
                    raise ValueError(
                        f"deep_validation_failed rejection must fail L3: {self.request_id}"
                    )


@dataclass(frozen=True, slots=True)
class ServerValidationGateContract:
    """Unified server-side validation gate contract."""

    total_entries: int
    passed_entries: int
    rejected_entries: int
    entries: tuple[ServerValidationGateEntry, ...]
