export interface ShellStateContract {
  shellStateId: "shell_state_contract_001";
  activeShellId: "dashboard_shell_contract_001";
  activeWorkspaceId: "workspace_main";
  activePanelId: string;
  stateMode: "registry_state_ready";
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateShellStateContract(
  contract: ShellStateContract,
): ShellStateContract {
  requireNonEmpty(contract.shellStateId, "shellStateId");
  requireNonEmpty(contract.activePanelId, "activePanelId");
  requireNonEmpty(contract.description, "description");

  if (contract.stateMode !== "registry_state_ready") {
    throw new Error("stateMode must remain registry_state_ready.");
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical shell state contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical shell state contract.",
    );
  }

  return contract;
}

export function buildShellStateContract(): ShellStateContract {
  return validateShellStateContract({
    shellStateId: "shell_state_contract_001",
    activeShellId: "dashboard_shell_contract_001",
    activeWorkspaceId: "workspace_main",
    activePanelId: "panel_operator_main",
    stateMode: "registry_state_ready",
    operatorVisible: true,
    truthBound: true,
    description: "Canonical shell state contract for frontend registry/state layer.",
  });
}
