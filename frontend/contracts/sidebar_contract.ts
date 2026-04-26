export type SidebarSection =
  | "foundation_navigation"
  | "operator_navigation"
  | "module_navigation";

export interface SidebarItem {
  itemId: string;
  label: string;
  section: SidebarSection;
  visible: true;
}

export interface SidebarContract {
  sidebarId: "sidebar_contract_001";
  items: readonly SidebarItem[];
  operatorVisible: true;
  truthBound: true;
  description: string;
}

function requireNonEmpty(value: string, fieldName: string): void {
  if (!value.trim()) {
    throw new Error(`${fieldName} must be non-empty.`);
  }
}

export function validateSidebarContract(
  contract: SidebarContract,
): SidebarContract {
  requireNonEmpty(contract.sidebarId, "sidebarId");
  requireNonEmpty(contract.description, "description");

  if (contract.items.length < 3) {
    throw new Error("Sidebar contract must contain at least 3 canonical items.");
  }

  for (const item of contract.items) {
    requireNonEmpty(item.itemId, "item.itemId");
    requireNonEmpty(item.label, "item.label");
    if (item.visible !== true) {
      throw new Error("All canonical sidebar items must remain visible.");
    }
  }

  if (contract.operatorVisible !== true) {
    throw new Error(
      "operatorVisible must remain true for canonical sidebar contract.",
    );
  }

  if (contract.truthBound !== true) {
    throw new Error("truthBound must remain true for canonical sidebar contract.");
  }

  return contract;
}

export function buildSidebarContract(): SidebarContract {
  return validateSidebarContract({
    sidebarId: "sidebar_contract_001",
    items: [
      {
        itemId: "sidebar_item_system_status",
        label: "System Status",
        section: "foundation_navigation",
        visible: true,
      },
      {
        itemId: "sidebar_item_operator",
        label: "Operator",
        section: "operator_navigation",
        visible: true,
      },
      {
        itemId: "sidebar_item_modules",
        label: "Modules",
        section: "module_navigation",
        visible: true,
      },
    ],
    operatorVisible: true,
    truthBound: true,
    description: "Canonical sidebar contract for frontend shell foundation.",
  });
}
