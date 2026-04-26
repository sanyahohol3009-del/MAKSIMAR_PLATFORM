export interface WorkspaceSwitchTarget {
  workspaceId: string;
  label: string;
  reachable: true;
}

export interface WorkspaceSwitchContract {
  workspaceSwitchId: "workspace_switch_contract_001";
  activeWorkspaceId: "workspace_main";
  targets: readonly WorkspaceSwitchTarget[];
  guardedSwitching: true;
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateWorkspaceSwitchContract(
  contract: WorkspaceSwitchContract,
): WorkspaceSwitchContract {
  requireNonEmpty(contract.workspaceSwitchId, "workspaceSwitchId");
  requireNonEmpty(contract.description, "description");

  if (contract.targets.length < 2) {
    throw new Error(
      "Workspace switch contract must contain at least 2 canonical targets.",
    );
  }

  for (const target of contract.targets) {
    requireNonEmpty(target.workspaceId, "target.workspaceId");
    requireNonEmpty(target.label, "target.label");
    if (target.reachable !== true) {
      throw new Error("All canonical workspace targets must remain reachable.");
    }
  }

  if (contract.guardedSwitching !== true) {
    throw new Error(
      "guardedSwitching must remain true for canonical workspace switch contract.",
    );
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical workspace switch contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical workspace switch contract.",
    );
  }

  return contract;
}

export function buildWorkspaceSwitchContract(): WorkspaceSwitchContract {
  return validateWorkspaceSwitchContract({
    workspaceSwitchId: "workspace_switch_contract_001",
    activeWorkspaceId: "workspace_main",
    targets: [
      {
        workspaceId: "workspace_main",
        label: "Main Workspace",
        reachable: true,
      },
      {
        workspaceId: "workspace_secondary",
        label: "Secondary Workspace",
        reachable: true,
      },
    ],
    guardedSwitching: true,
    operatorVisible: true,
    truthBound: true,
    description:
      "Canonical workspace switch contract for frontend registry/state layer.",
  });
}
