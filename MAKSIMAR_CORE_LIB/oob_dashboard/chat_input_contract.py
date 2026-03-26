from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.chat_input_models import (
    DashboardChatInputBinding,
    DashboardChatInputContract,
)


def build_dashboard_chat_input_contract() -> DashboardChatInputContract:
    """Build unified chat ↔ input integration contract."""

    bindings = (
        DashboardChatInputBinding(
            input_mode="text",
            enabled=True,
            routed_through_input_contract=True,
        ),
        DashboardChatInputBinding(
            input_mode="voice",
            enabled=True,
            routed_through_input_contract=True,
        ),
        DashboardChatInputBinding(
            input_mode="gesture",
            enabled=True,
            routed_through_input_contract=True,
        ),
    )

    output_modes = (
        "text",
        "code",
        "diagnostic",
    )

    return DashboardChatInputContract(
        bindings=bindings,
        output_modes=output_modes,
    )
