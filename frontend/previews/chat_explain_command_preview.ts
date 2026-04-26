import { buildChatPanelContract } from "../contracts/chat_panel_contract.js";
import { buildCommandQueueViewContract } from "../contracts/command_queue_view_contract.js";
import { buildExplainViewContract } from "../contracts/explain_view_contract.js";
import { buildInteractionSplitContract } from "../contracts/interaction_split_contract.js";

function main(): void {
  const chat = buildChatPanelContract();
  const explain = buildExplainViewContract();
  const command = buildCommandQueueViewContract();
  const split = buildInteractionSplitContract();

  console.log("CHAT / EXPLAIN / COMMAND PREVIEW");
  console.log("=".repeat(120));
  console.log(`chat_messages=${chat.visibleMessages.length}`);
  console.log(`explain_blocks=${explain.blocks.length}`);
  console.log(`command_queue_entries=${command.queueEntries.length}`);
  console.log(`split_mode=${split.splitMode}`);
}

main();
