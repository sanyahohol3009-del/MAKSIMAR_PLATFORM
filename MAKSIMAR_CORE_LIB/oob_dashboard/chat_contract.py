from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.chat_models import (
    DashboardChatContract,
    DashboardChatMessage,
)


def build_dashboard_chat_contract() -> DashboardChatContract:
    """Build read-only chat contract for dashboard text/code exchange."""
    messages = [
        DashboardChatMessage(
            message_id="msg_001",
            role="system",
            content_type="diagnostic",
            content="OOB dashboard chat pane initialized.",
        ),
        DashboardChatMessage(
            message_id="msg_002",
            role="jarvis",
            content_type="text",
            content="Диагностический канал готов. Здесь можно читать ответы и копировать кодовые блоки.",
        ),
        DashboardChatMessage(
            message_id="msg_003",
            role="jarvis",
            content_type="code",
            content="print('diagnostic code block placeholder')",
        ),
    ]

    return DashboardChatContract(
        total_messages=len(messages),
        messages=messages,
        copy_enabled=True,
        input_enabled=True,
    )
