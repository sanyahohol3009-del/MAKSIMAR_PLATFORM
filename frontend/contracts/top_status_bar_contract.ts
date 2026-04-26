export interface TopStatusBarSignal {
  signalId: string;
  label: string;
  value: string;
  visible: true;
}

export interface TopStatusBarContract {
  topStatusBarId: "top_status_bar_contract_001";
  signals: readonly TopStatusBarSignal[];
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateTopStatusBarContract(
  contract: TopStatusBarContract,
): TopStatusBarContract {
  requireNonEmpty(contract.topStatusBarId, "topStatusBarId");
  requireNonEmpty(contract.description, "description");

  if (contract.signals.length < 3) {
    throw new Error(
      "Top status bar contract must contain at least 3 canonical signals.",
    );
  }

  for (const signal of contract.signals) {
    requireNonEmpty(signal.signalId, "signal.signalId");
    requireNonEmpty(signal.label, "signal.label");
    requireNonEmpty(signal.value, "signal.value");
    if (signal.visible !== true) {
      throw new Error("All canonical status signals must remain visible.");
    }
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical top status bar contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error(
      "truthBound must remain true for canonical top status bar contract.",
    );
  }

  return contract;
}

export function buildTopStatusBarContract(): TopStatusBarContract {
  return validateTopStatusBarContract({
    topStatusBarId: "top_status_bar_contract_001",
    signals: [
      {
        signalId: "top_signal_health",
        label: "Health",
        value: "green",
        visible: true,
      },
      {
        signalId: "top_signal_mode",
        label: "Mode",
        value: "operator",
        visible: true,
      },
      {
        signalId: "top_signal_workspace",
        label: "Workspace",
        value: "main",
        visible: true,
      },
    ],
    operatorVisible: true,
    truthBound: true,
    description: "Canonical top status bar contract for frontend shell foundation.",
  });
}
