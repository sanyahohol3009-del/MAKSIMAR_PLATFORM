from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.control_plane_handoff_contract import (
    build_control_plane_handoff_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_models import (
    ALL_HANDOFF_STATES,
    CONTROL_PLANE_TARGETS,
    OperatorControlPlaneHandoffModel,
    build_operator_control_plane_handoff_model,
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorControlPlaneHandoffContractEntry:
    """Canonical operator control-plane handoff contract entry."""

    handoff_id: str
    operator_intent_id: str
    control_plane_target: str
    handoff_state: str
    handoff_created_at: str
    handoff_completed_at: str | None
    handoff_denied_reason: str | None
    trace_id: str
    operator_visible: bool
    target_registered: bool
    state_registered: bool
    baseline_family_aligned: bool
    structurally_valid: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator control-plane handoff contract entry fields."""
        _require_non_empty(self.handoff_id, "handoff_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.control_plane_target, "control_plane_target")
        _require_non_empty(self.handoff_state, "handoff_state")
        _require_non_empty(self.handoff_created_at, "handoff_created_at")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.control_plane_target not in CONTROL_PLANE_TARGETS:
            raise ValueError(
                "control_plane_target must be one of "
                f"{CONTROL_PLANE_TARGETS}, got {self.control_plane_target!r}."
            )

        if self.handoff_state not in ALL_HANDOFF_STATES:
            raise ValueError(
                "handoff_state must be one of "
                f"{ALL_HANDOFF_STATES}, got {self.handoff_state!r}."
            )

        if self.handoff_state == "handoff_acknowledged" and self.handoff_completed_at is None:
            raise ValueError(
                "handoff_acknowledged entries must include handoff_completed_at."
            )

        if self.handoff_state == "handoff_failed" and (
            self.handoff_denied_reason is None or not self.handoff_denied_reason.strip()
        ):
            raise ValueError(
                "handoff_failed entries must include a non-empty handoff_denied_reason."
            )

        if not self.target_registered:
            raise ValueError("target_registered must be true for canonical entries.")

        if not self.state_registered:
            raise ValueError("state_registered must be true for canonical entries.")

        if not self.structurally_valid:
            raise ValueError("structurally_valid must be true for canonical entries.")


@dataclass(frozen=True, slots=True)
class OperatorControlPlaneHandoffContract:
    """Canonical operator control-plane handoff contract."""

    contract_id: str
    total_entries: int
    not_ready_entries: int
    ready_entries: int
    blocked_entries: int
    emitted_entries: int
    acknowledged_entries: int
    failed_entries: int
    operator_visible_entries: int
    baseline_aligned_entries: int
    structurally_valid_entries: int
    entries: tuple[OperatorControlPlaneHandoffContractEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator control-plane handoff contract fields."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.not_ready_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_not_ready"
        ):
            raise ValueError("not_ready_entries must match handoff_not_ready count.")

        if self.ready_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_ready"
        ):
            raise ValueError("ready_entries must match handoff_ready count.")

        if self.blocked_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_blocked"
        ):
            raise ValueError("blocked_entries must match handoff_blocked count.")

        if self.emitted_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_emitted"
        ):
            raise ValueError("emitted_entries must match handoff_emitted count.")

        if self.acknowledged_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_acknowledged"
        ):
            raise ValueError(
                "acknowledged_entries must match handoff_acknowledged count."
            )

        if self.failed_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_failed"
        ):
            raise ValueError("failed_entries must match handoff_failed count.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )

        if self.baseline_aligned_entries != sum(
            1 for entry in self.entries if entry.baseline_family_aligned
        ):
            raise ValueError(
                "baseline_aligned_entries must match baseline_family_aligned count."
            )

        if self.structurally_valid_entries != sum(
            1 for entry in self.entries if entry.structurally_valid
        ):
            raise ValueError(
                "structurally_valid_entries must match structurally_valid count."
            )


def _is_baseline_family_aligned(
    model: OperatorControlPlaneHandoffModel,
) -> dict[str, bool]:
    """Resolve baseline family alignment against the earlier handoff contract."""
    baseline_contract = build_control_plane_handoff_contract()

    baseline_targets = {entry.handoff_target for entry in baseline_contract.entries}
    baseline_modes = {entry.handoff_mode for entry in baseline_contract.entries}

    alignment_by_intent_id: dict[str, bool] = {}

    for entry in model.entries:
        target_alias = "control_plane_router"

        if entry.handoff_state == "handoff_not_ready":
            expected_mode = "read_only_path"
        else:
            expected_mode = "approval_gated"

        target_is_aligned = target_alias in baseline_targets
        mode_is_aligned = expected_mode in baseline_modes

        alignment_by_intent_id[entry.operator_intent_id] = (
            target_is_aligned and mode_is_aligned
        )

    return alignment_by_intent_id


def build_operator_control_plane_handoff_contract() -> OperatorControlPlaneHandoffContract:
    """Build canonical operator control-plane handoff contract."""
    model = build_operator_control_plane_handoff_model()
    baseline_alignment = _is_baseline_family_aligned(model)

    entries = tuple(
        OperatorControlPlaneHandoffContractEntry(
            handoff_id=entry.handoff_id,
            operator_intent_id=entry.operator_intent_id,
            control_plane_target=entry.control_plane_target,
            handoff_state=entry.handoff_state,
            handoff_created_at=entry.handoff_created_at,
            handoff_completed_at=entry.handoff_completed_at,
            handoff_denied_reason=entry.handoff_denied_reason,
            trace_id=entry.trace_id,
            operator_visible=True,
            target_registered=entry.control_plane_target in CONTROL_PLANE_TARGETS,
            state_registered=entry.handoff_state in ALL_HANDOFF_STATES,
            baseline_family_aligned=baseline_alignment[entry.operator_intent_id],
            structurally_valid=(
                entry.control_plane_target in CONTROL_PLANE_TARGETS
                and entry.handoff_state in ALL_HANDOFF_STATES
                and bool(entry.handoff_id.strip())
                and bool(entry.operator_intent_id.strip())
                and bool(entry.trace_id.strip())
                and bool(entry.description.strip())
            ),
            description=entry.description,
        )
        for entry in model.entries
    )

    return OperatorControlPlaneHandoffContract(
        contract_id="operator_control_plane_handoff_contract_001",
        total_entries=len(entries),
        not_ready_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_not_ready"
        ),
        ready_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_ready"
        ),
        blocked_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_blocked"
        ),
        emitted_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_emitted"
        ),
        acknowledged_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_acknowledged"
        ),
        failed_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_failed"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        baseline_aligned_entries=sum(
            1 for entry in entries if entry.baseline_family_aligned
        ),
        structurally_valid_entries=sum(
            1 for entry in entries if entry.structurally_valid
        ),
        entries=entries,
    )
