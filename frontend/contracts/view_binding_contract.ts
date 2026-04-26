export interface ViewBindingEntry {
  bindingId: string;
  panelId: string;
  zoneId: string;
  bound: true;
}

export interface ViewBindingContract {
  viewBindingId: "view_binding_contract_001";
  bindings: readonly ViewBindingEntry[];
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateViewBindingContract(
  contract: ViewBindingContract,
): ViewBindingContract {
  requireNonEmpty(contract.viewBindingId, "viewBindingId");
  requireNonEmpty(contract.description, "description");

  if (contract.bindings.length < 4) {
    throw new Error(
      "View binding contract must contain at least 4 canonical bindings.",
    );
  }

  for (const binding of contract.bindings) {
    requireNonEmpty(binding.bindingId, "binding.bindingId");
    requireNonEmpty(binding.panelId, "binding.panelId");
    requireNonEmpty(binding.zoneId, "binding.zoneId");

    if (binding.bound !== true) {
      throw new Error("All canonical view bindings must remain bound=true.");
    }
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical view binding contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical view binding contract.",
    );
  }

  return contract;
}

export function buildViewBindingContract(): ViewBindingContract {
  return validateViewBindingContract({
    viewBindingId: "view_binding_contract_001",
    bindings: [
      {
        bindingId: "view_binding_system_status",
        panelId: "panel_system_status",
        zoneId: "zone_navigation",
        bound: true,
      },
      {
        bindingId: "view_binding_operator_main",
        panelId: "panel_operator_main",
        zoneId: "zone_main_workspace",
        bound: true,
      },
      {
        bindingId: "view_binding_explainability",
        panelId: "panel_explainability",
        zoneId: "zone_explainability",
        bound: true,
      },
      {
        bindingId: "view_binding_command_strip",
        panelId: "panel_command_strip",
        zoneId: "zone_diagnostics",
        bound: true,
      },
    ],
    operatorVisible: true,
    truthBound: true,
    description:
      "Canonical view binding contract for frontend registry/state layer.",
  });
}
