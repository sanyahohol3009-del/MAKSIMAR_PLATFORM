export type ShellMode =
  | "operator_shell_foundation"
  | "registry_state_shell"
  | "chat_explain_command_shell";

export interface DashboardShellContract {
  shellId: "dashboard_shell_contract_001";
  shellMode: ShellMode;
  sidebarId: string;
  topStatusBarId: string;
  workspaceFrameId: string;
  explainPanelId: string;
  commandStripId: string;
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateDashboardShellContract(
  contract: DashboardShellContract,
): DashboardShellContract {
  requireNonEmpty(contract.shellId, "shellId");
  requireNonEmpty(contract.sidebarId, "sidebarId");
  requireNonEmpty(contract.topStatusBarId, "topStatusBarId");
  requireNonEmpty(contract.workspaceFrameId, "workspaceFrameId");
  requireNonEmpty(contract.explainPanelId, "explainPanelId");
  requireNonEmpty(contract.commandStripId, "commandStripId");
  requireNonEmpty(contract.description, "description");

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical dashboard shell contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical dashboard shell contract.",
    );
  }

  return contract;
}

export function buildDashboardShellContract(): DashboardShellContract {
  return validateDashboardShellContract({
    shellId: "dashboard_shell_contract_001",
    shellMode: "operator_shell_foundation",
    sidebarId: "sidebar_contract_001",
    topStatusBarId: "top_status_bar_contract_001",
    workspaceFrameId: "workspace_frame_contract_001",
    explainPanelId: "explain_panel_contract_001",
    commandStripId: "command_strip_contract_001",
    operatorVisible: true,
    truthBound: true,
    description:
      "Canonical frontend dashboard shell contract binding sidebar, top status bar, workspace frame, explain panel, and command strip.",
  });
}
