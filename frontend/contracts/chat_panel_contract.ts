export interface ChatMessageShape {
  messageId: string;
  role: "user" | "assistant";
  visible: true;
}

export interface ChatPanelContract {
  chatPanelId: "chat_panel_contract_001";
  panelId: "panel_operator_main";
  supportsHistory: true;
  supportsInput: true;
  visibleMessages: readonly ChatMessageShape[];
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateChatPanelContract(
  contract: ChatPanelContract,
): ChatPanelContract {
  requireNonEmpty(contract.chatPanelId, "chatPanelId");
  requireNonEmpty(contract.panelId, "panelId");
  requireNonEmpty(contract.description, "description");

  if (contract.supportsHistory !== true) {
    throw new Error(
      "supportsHistory must remain true for canonical chat panel contract.",
    );
  }

  if (contract.supportsInput !== true) {
    throw new Error(
      "supportsInput must remain true for canonical chat panel contract.",
    );
  }

  if (contract.visibleMessages.length < 2) {
    throw new Error(
      "Chat panel contract must contain at least 2 canonical visible messages.",
    );
  }

  for (const message of contract.visibleMessages) {
    requireNonEmpty(message.messageId, "message.messageId");
    if (message.visible !== true) {
      throw new Error("All canonical chat messages must remain visible.");
    }
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical chat panel contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical chat panel contract.",
    );
  }

  return contract;
}

export function buildChatPanelContract(): ChatPanelContract {
  return validateChatPanelContract({
    chatPanelId: "chat_panel_contract_001",
    panelId: "panel_operator_main",
    supportsHistory: true,
    supportsInput: true,
    visibleMessages: [
      {
        messageId: "chat_message_user_001",
        role: "user",
        visible: true,
      },
      {
        messageId: "chat_message_assistant_001",
        role: "assistant",
        visible: true,
      },
    ],
    operatorVisible: true,
    truthBound: true,
    description:
      "Canonical chat panel contract for chat/explain/command split layer.",
  });
}
