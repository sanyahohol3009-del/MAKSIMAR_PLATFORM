import { buildCommandStripContract } from "../contracts/command_strip_contract.js";
import { buildDashboardShellContract } from "../contracts/dashboard_shell_contract.js";
import { buildExplainPanelContract } from "../contracts/explain_panel_contract.js";
import { buildSidebarContract } from "../contracts/sidebar_contract.js";
import { buildTopStatusBarContract } from "../contracts/top_status_bar_contract.js";
import { buildWorkspaceFrameContract } from "../contracts/workspace_frame_contract.js";

function main(): void {
  const shell = buildDashboardShellContract();
  const sidebar = buildSidebarContract();
  const topBar = buildTopStatusBarContract();
  const workspace = buildWorkspaceFrameContract();
  const explain = buildExplainPanelContract();
  const command = buildCommandStripContract();

  console.log("SIMPLE SHELL PREVIEW");
  console.log("=".repeat(120));
  console.log(`shell_id=${shell.shellId} | mode=${shell.shellMode}`);
  console.log(`sidebar_items=${sidebar.items.length}`);
  console.log(`top_status_signals=${topBar.signals.length}`);
  console.log(`workspace_zones=${workspace.zones.length}`);
  console.log(`explain_panel=${explain.explainPanelId}`);
  console.log(`command_actions=${command.actions.length}`);
}

main();
