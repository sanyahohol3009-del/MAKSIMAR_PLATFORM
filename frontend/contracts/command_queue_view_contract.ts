export interface CommandQueueEntry {
  commandId: string;
  state: "queued" | "review" | "guarded";
  visible: true;
}

export interface CommandQueueViewContract {
  commandQueueViewId: "command_queue_view_contract_001";
  panelId: "panel_command_strip";
  readOnlyQueueView: true;
  queueEntries: readonly CommandQueueEntry[];
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateCommandQueueViewContract(
  contract: CommandQueueViewContract,
): CommandQueueViewContract {
  requireNonEmpty(contract.commandQueueViewId, "commandQueueViewId");
  requireNonEmpty(contract.panelId, "panelId");
  requireNonEmpty(contract.description, "description");

  if (contract.readOnlyQueueView !== true) {
    throw new Error(
      "readOnlyQueueView must remain true for canonical command queue view contract.",
    );
  }

  if (contract.queueEntries.length < 3) {
    throw new Error(
      "Command queue view contract must contain at least 3 canonical queue entries.",
    );
  }

  for (const entry of contract.queueEntries) {
    requireNonEmpty(entry.commandId, "entry.commandId");
    if (entry.visible !== true) {
      throw new Error("All canonical command queue entries must remain visible.");
    }
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical command queue view contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical command queue view contract.",
    );
  }

  return contract;
}

export function buildCommandQueueViewContract(): CommandQueueViewContract {
  return validateCommandQueueViewContract({
    commandQueueViewId: "command_queue_view_contract_001",
    panelId: "panel_command_strip",
    readOnlyQueueView: true,
    queueEntries: [
      {
        commandId: "command_preview",
        state: "queued",
        visible: true,
      },
      {
        commandId: "command_review",
        state: "review",
        visible: true,
      },
      {
        commandId: "command_route",
        state: "guarded",
        visible: true,
      },
    ],
    operatorVisible: true,
    truthBound: true,
    description:
      "Canonical command queue view contract for chat/explain/command split layer.",
  });
}
