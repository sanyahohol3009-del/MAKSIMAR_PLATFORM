export interface ExplainPanelContract {
  explainPanelId: "explain_panel_contract_001";
  explainBinding: "read_only_explainability";
  preferredZone: "zone_explainability";
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateExplainPanelContract(
  contract: ExplainPanelContract,
): ExplainPanelContract {
  requireNonEmpty(contract.explainPanelId, "explainPanelId");
  requireNonEmpty(contract.description, "description");

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical explain panel contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical explain panel contract.",
    );
  }

  return contract;
}

export function buildExplainPanelContract(): ExplainPanelContract {
  return validateExplainPanelContract({
    explainPanelId: "explain_panel_contract_001",
    explainBinding: "read_only_explainability",
    preferredZone: "zone_explainability",
    operatorVisible: true,
    truthBound: true,
    description: "Canonical explain panel contract for frontend shell foundation.",
  });
}
