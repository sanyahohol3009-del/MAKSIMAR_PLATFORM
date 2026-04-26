export type PanelFamily =
  | "foundation"
  | "operator"
  | "explainability"
  | "command";

export interface PanelRegistryEntry {
  panelId: string;
  panelLabel: string;
  panelFamily: PanelFamily;
  defaultVisible: true;
  truthBound: true;
}

export interface PanelRegistryContract {
  registryId: "panel_registry_contract_001";
  entries: readonly PanelRegistryEntry[];
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validatePanelRegistryContract(
  contract: PanelRegistryContract,
): PanelRegistryContract {
  requireNonEmpty(contract.registryId, "registryId");
  requireNonEmpty(contract.description, "description");

  if (contract.entries.length < 4) {
    throw new Error(
      "Panel registry contract must contain at least 4 canonical entries.",
    );
  }

  for (const entry of contract.entries) {
    requireNonEmpty(entry.panelId, "entry.panelId");
    requireNonEmpty(entry.panelLabel, "entry.panelLabel");

    if (entry.defaultVisible !== true) {
      throw new Error(
        "All canonical panel registry entries must remain defaultVisible=true.",
      );
    }

    if (entry.truthBound !== true) {
      throw new Error(
        "All canonical panel registry entries must remain truthBound=true.",
      );
    }
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical panel registry contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical panel registry contract.",
    );
  }

  return contract;
}

export function buildPanelRegistryContract(): PanelRegistryContract {
  return validatePanelRegistryContract({
    registryId: "panel_registry_contract_001",
    entries: [
      {
        panelId: "panel_system_status",
        panelLabel: "System Status",
        panelFamily: "foundation",
        defaultVisible: true,
        truthBound: true,
      },
      {
        panelId: "panel_operator_main",
        panelLabel: "Operator Main",
        panelFamily: "operator",
        defaultVisible: true,
        truthBound: true,
      },
      {
        panelId: "panel_explainability",
        panelLabel: "Explainability",
        panelFamily: "explainability",
        defaultVisible: true,
        truthBound: true,
      },
      {
        panelId: "panel_command_strip",
        panelLabel: "Command Strip",
        panelFamily: "command",
        defaultVisible: true,
        truthBound: true,
      },
    ],
    operatorVisible: true,
    truthBound: true,
    description:
      "Canonical panel registry contract for frontend registry/state layer.",
  });
}
