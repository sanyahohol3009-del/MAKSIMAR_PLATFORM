export interface CommandStripAction {
  actionId: string;
  label: string;
  guarded: true;
}

export interface CommandStripContract {
  commandStripId: "command_strip_contract_001";
  actions: readonly CommandStripAction[];
  directServerMutationAllowed: false;
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateCommandStripContract(
  contract: CommandStripContract,
): CommandStripContract {
  requireNonEmpty(contract.commandStripId, "commandStripId");
  requireNonEmpty(contract.description, "description");

  if (contract.actions.length < 3) {
    throw new Error(
      "Command strip contract must contain at least 3 canonical actions.",
    );
  }

  for (const action of contract.actions) {
    requireNonEmpty(action.actionId, "action.actionId");
    requireNonEmpty(action.label, "action.label");
    if (action.guarded !== true) {
      throw new Error("All canonical command strip actions must remain guarded.");
    }
  }

  if (contract.directServerMutationAllowed !== false) {
    throw new Error(
      "directServerMutationAllowed must remain false for canonical command strip contract.",
    );
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical command strip contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical command strip contract.",
    );
  }

  return contract;
}

export function buildCommandStripContract(): CommandStripContract {
  return validateCommandStripContract({
    commandStripId: "command_strip_contract_001",
    actions: [
      { actionId: "command_preview", label: "Preview", guarded: true },
      { actionId: "command_review", label: "Review", guarded: true },
      { actionId: "command_route", label: "Route", guarded: true },
    ],
    directServerMutationAllowed: false,
    operatorVisible: true,
    truthBound: true,
    description: "Canonical command strip contract for frontend shell foundation.",
  });
}
