export interface InteractionSplitContract {
  interactionSplitId: "interaction_split_contract_001";
  chatPanelId: "chat_panel_contract_001";
  explainViewId: "explain_view_contract_001";
  commandQueueViewId: "command_queue_view_contract_001";
  splitMode: "chat_explain_command_ready";
  readOnlyExplain: true;
  guardedCommandPath: true;
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateInteractionSplitContract(
  contract: InteractionSplitContract,
): InteractionSplitContract {
  requireNonEmpty(contract.interactionSplitId, "interactionSplitId");
  requireNonEmpty(contract.chatPanelId, "chatPanelId");
  requireNonEmpty(contract.explainViewId, "explainViewId");
  requireNonEmpty(contract.commandQueueViewId, "commandQueueViewId");
  requireNonEmpty(contract.description, "description");

  if (contract.splitMode !== "chat_explain_command_ready") {
    throw new Error("splitMode must remain chat_explain_command_ready.");
  }

  if (contract.readOnlyExplain !== true) {
    throw new Error(
      "readOnlyExplain must remain true for canonical interaction split contract.",
    );
  }

  if (contract.guardedCommandPath !== true) {
    throw new Error(
      "guardedCommandPath must remain true for canonical interaction split contract.",
    );
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical interaction split contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical interaction split contract.",
    );
  }

  return contract;
}

export function buildInteractionSplitContract(): InteractionSplitContract {
  return validateInteractionSplitContract({
    interactionSplitId: "interaction_split_contract_001",
    chatPanelId: "chat_panel_contract_001",
    explainViewId: "explain_view_contract_001",
    commandQueueViewId: "command_queue_view_contract_001",
    splitMode: "chat_explain_command_ready",
    readOnlyExplain: true,
    guardedCommandPath: true,
    operatorVisible: true,
    truthBound: true,
    description:
      "Canonical interaction split contract for chat/explain/command layer.",
  });
}
