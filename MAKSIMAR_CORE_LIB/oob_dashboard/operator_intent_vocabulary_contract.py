from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    ALL_INTENT_KINDS,
    ALL_INTENT_STATES,
    ALL_REQUESTED_ACTION_KINDS,
    build_operator_intent_model,
)


@dataclass(frozen=True, slots=True)
class OperatorIntentVocabularyEntry:
    """Canonical operator intent vocabulary entry."""

    vocabulary_entry_id: str
    vocabulary_group: str
    canonical_value: str
    display_label: str
    operator_readable: bool
    approval_relevant: bool
    handoff_relevant: bool
    description: str


@dataclass(frozen=True, slots=True)
class OperatorIntentVocabularyContract:
    """Canonical operator intent vocabulary contract."""

    contract_id: str
    total_entries: int
    intent_kind_entries: int
    intent_state_entries: int
    requested_action_entries: int
    operator_readable_entries: int
    approval_relevant_entries: int
    handoff_relevant_entries: int
    entries: tuple[OperatorIntentVocabularyEntry, ...]


def build_operator_intent_vocabulary_contract() -> OperatorIntentVocabularyContract:
    """Build canonical operator intent vocabulary contract."""
    model = build_operator_intent_model()
    model_entries = model.entries

    approval_relevant_states = {
        "intent_pending_approval",
        "intent_approved",
        "intent_rejected",
    }
    handoff_relevant_states = {
        "intent_handoff_ready",
        "intent_handed_off",
    }
    approval_relevant_actions = {
        "request_control_surface",
        "request_approval_flow",
        "request_system_action",
    }
    handoff_relevant_actions = {
        "request_control_surface",
        "request_system_action",
    }

    entries = tuple(
        [
            *(
                OperatorIntentVocabularyEntry(
                    vocabulary_entry_id=f"operator_intent_kind_{index:03d}",
                    vocabulary_group="intent_kind",
                    canonical_value=intent_kind,
                    display_label=intent_kind.replace("_", " ").title(),
                    operator_readable=True,
                    approval_relevant=intent_kind in {"control_request", "approval_request", "system_action_request"},
                    handoff_relevant=intent_kind in {"control_request", "system_action_request"},
                    description=(
                        f"Canonical operator intent kind vocabulary entry for {intent_kind}."
                    ),
                )
                for index, intent_kind in enumerate(ALL_INTENT_KINDS, start=1)
            ),
            *(
                OperatorIntentVocabularyEntry(
                    vocabulary_entry_id=f"operator_intent_state_{index:03d}",
                    vocabulary_group="intent_state",
                    canonical_value=intent_state,
                    display_label=intent_state.replace("_", " ").title(),
                    operator_readable=True,
                    approval_relevant=intent_state in approval_relevant_states,
                    handoff_relevant=intent_state in handoff_relevant_states,
                    description=(
                        f"Canonical operator intent state vocabulary entry for {intent_state}."
                    ),
                )
                for index, intent_state in enumerate(ALL_INTENT_STATES, start=1)
            ),
            *(
                OperatorIntentVocabularyEntry(
                    vocabulary_entry_id=f"operator_requested_action_{index:03d}",
                    vocabulary_group="requested_action",
                    canonical_value=requested_action,
                    display_label=requested_action.replace("_", " ").title(),
                    operator_readable=True,
                    approval_relevant=requested_action in approval_relevant_actions,
                    handoff_relevant=requested_action in handoff_relevant_actions,
                    description=(
                        "Canonical operator requested action vocabulary entry for "
                        f"{requested_action}."
                    ),
                )
                for index, requested_action in enumerate(
                    ALL_REQUESTED_ACTION_KINDS, start=1
                )
            ),
        ]
    )

    approval_relevant_values = {
        entry.intent_kind
        for entry in model_entries
        if entry.approval_required
    }

    handoff_relevant_values = {
        "control_request",
        "system_action_request",
        "intent_handoff_ready",
        "intent_handed_off",
        "request_control_surface",
        "request_system_action",
    }

    normalized_entries = tuple(
        OperatorIntentVocabularyEntry(
            vocabulary_entry_id=entry.vocabulary_entry_id,
            vocabulary_group=entry.vocabulary_group,
            canonical_value=entry.canonical_value,
            display_label=entry.display_label,
            operator_readable=entry.operator_readable,
            approval_relevant=(
                entry.approval_relevant
                or entry.canonical_value in approval_relevant_values
            ),
            handoff_relevant=(
                entry.handoff_relevant
                or entry.canonical_value in handoff_relevant_values
            ),
            description=entry.description,
        )
        for entry in entries
    )

    return OperatorIntentVocabularyContract(
        contract_id="operator_intent_vocabulary_contract_001",
        total_entries=len(normalized_entries),
        intent_kind_entries=sum(
            1 for entry in normalized_entries if entry.vocabulary_group == "intent_kind"
        ),
        intent_state_entries=sum(
            1 for entry in normalized_entries if entry.vocabulary_group == "intent_state"
        ),
        requested_action_entries=sum(
            1
            for entry in normalized_entries
            if entry.vocabulary_group == "requested_action"
        ),
        operator_readable_entries=sum(
            1 for entry in normalized_entries if entry.operator_readable
        ),
        approval_relevant_entries=sum(
            1 for entry in normalized_entries if entry.approval_relevant
        ),
        handoff_relevant_entries=sum(
            1 for entry in normalized_entries if entry.handoff_relevant
        ),
        entries=normalized_entries,
    )
