import { buildPanelRegistryContract } from "../contracts/panel_registry_contract.js";
import { buildShellStateContract } from "../contracts/shell_state_contract.js";
import { buildViewBindingContract } from "../contracts/view_binding_contract.js";
import { buildWorkspaceSwitchContract } from "../contracts/workspace_switch_contract.js";

function main(): void {
  const registry = buildPanelRegistryContract();
  const shellState = buildShellStateContract();
  const viewBinding = buildViewBindingContract();
  const workspaceSwitch = buildWorkspaceSwitchContract();

  console.log("REGISTRY / STATE PREVIEW");
  console.log("=".repeat(120));
  console.log(`panel_registry_entries=${registry.entries.length}`);
  console.log(`active_panel=${shellState.activePanelId}`);
  console.log(`view_bindings=${viewBinding.bindings.length}`);
  console.log(`workspace_targets=${workspaceSwitch.targets.length}`);
}

main();
