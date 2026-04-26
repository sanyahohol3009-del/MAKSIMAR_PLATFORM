export interface WorkspaceFrameZone {
  zoneId: string;
  role: "navigation" | "main_workspace" | "diagnostics" | "explainability";
  visible: true;
}

export interface WorkspaceFrameContract {
  workspaceFrameId: "workspace_frame_contract_001";
  zones: readonly WorkspaceFrameZone[];
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateWorkspaceFrameContract(
  contract: WorkspaceFrameContract,
): WorkspaceFrameContract {
  requireNonEmpty(contract.workspaceFrameId, "workspaceFrameId");
  requireNonEmpty(contract.description, "description");

  if (contract.zones.length < 4) {
    throw new Error(
      "Workspace frame contract must contain 4 canonical zones.",
    );
  }

  for (const zone of contract.zones) {
    requireNonEmpty(zone.zoneId, "zone.zoneId");
    if (zone.visible !== true) {
      throw new Error("All canonical workspace zones must remain visible.");
    }
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical workspace frame contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical workspace frame contract.",
    );
  }

  return contract;
}

export function buildWorkspaceFrameContract(): WorkspaceFrameContract {
  return validateWorkspaceFrameContract({
    workspaceFrameId: "workspace_frame_contract_001",
    zones: [
      { zoneId: "zone_navigation", role: "navigation", visible: true },
      { zoneId: "zone_main_workspace", role: "main_workspace", visible: true },
      { zoneId: "zone_diagnostics", role: "diagnostics", visible: true },
      { zoneId: "zone_explainability", role: "explainability", visible: true },
    ],
    operatorVisible: true,
    truthBound: true,
    description: "Canonical workspace frame contract for frontend shell foundation.",
  });
}
