export interface ExplainBlock {
  blockId: string;
  blockType: "summary" | "reasoning" | "provenance";
  visible: true;
}

export interface ExplainViewContract {
  explainViewId: "explain_view_contract_001";
  panelId: "panel_explainability";
  readOnlyExplainability: true;
  blocks: readonly ExplainBlock[];
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateExplainViewContract(
  contract: ExplainViewContract,
): ExplainViewContract {
  requireNonEmpty(contract.explainViewId, "explainViewId");
  requireNonEmpty(contract.panelId, "panelId");
  requireNonEmpty(contract.description, "description");

  if (contract.readOnlyExplainability !== true) {
    throw new Error(
      "readOnlyExplainability must remain true for canonical explain view contract.",
    );
  }

  if (contract.blocks.length < 3) {
    throw new Error(
      "Explain view contract must contain at least 3 canonical blocks.",
    );
  }

  for (const block of contract.blocks) {
    requireNonEmpty(block.blockId, "block.blockId");
    if (block.visible !== true) {
      throw new Error("All canonical explain blocks must remain visible.");
    }
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical explain view contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical explain view contract.",
    );
  }

  return contract;
}

export function buildExplainViewContract(): ExplainViewContract {
  return validateExplainViewContract({
    explainViewId: "explain_view_contract_001",
    panelId: "panel_explainability",
    readOnlyExplainability: true,
    blocks: [
      {
        blockId: "explain_summary_block",
        blockType: "summary",
        visible: true,
      },
      {
        blockId: "explain_reasoning_block",
        blockType: "reasoning",
        visible: true,
      },
      {
        blockId: "explain_provenance_block",
        blockType: "provenance",
        visible: true,
      },
    ],
    operatorVisible: true,
    truthBound: true,
    description:
      "Canonical explain view contract for chat/explain/command split layer.",
  });
}
