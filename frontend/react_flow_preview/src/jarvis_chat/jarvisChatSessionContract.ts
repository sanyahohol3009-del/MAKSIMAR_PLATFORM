import type { JarvisChatMessageContract } from "./jarvisChatMessageContract.js";
import type { JarvisChatProjectContextContract } from "./jarvisChatProjectContextContract.js";
import type { JarvisChatHandoffContract } from "./jarvisChatHandoffContract.js";

export type JarvisChatSessionDefaultVisibility =
  | "hidden"
  | "open";

export type JarvisChatSessionContract = {
  sessionId: string;
  drawerId: "top_chat_drawer";
  displayTitle: string;
  collapsedTabLabel: string;
  messages: readonly JarvisChatMessageContract[];
  projectContextSummary: JarvisChatProjectContextContract;
  handoffs: readonly JarvisChatHandoffContract[];
  unreadCount: number;
  hasProjectContext: boolean;
  hasCommandSupport: boolean;
  hasDiagnosticsSummary: boolean;
  isOverlayOnly: true;
  isUndockable: true;
  defaultVisibility: JarvisChatSessionDefaultVisibility;
};

export type BuildJarvisChatSessionContractArgs = {
  sessionId: string;
  displayTitle: string;
  collapsedTabLabel: string;
  messages: readonly JarvisChatMessageContract[];
  projectContextSummary: JarvisChatProjectContextContract;
  handoffs: readonly JarvisChatHandoffContract[];
  unreadCount: number;
  defaultVisibility: JarvisChatSessionDefaultVisibility;
};

export function buildJarvisChatSessionContract(
  args: BuildJarvisChatSessionContractArgs,
): JarvisChatSessionContract {
  return {
    sessionId: args.sessionId,
    drawerId: "top_chat_drawer",
    displayTitle: args.displayTitle,
    collapsedTabLabel: args.collapsedTabLabel,
    messages: args.messages,
    projectContextSummary: args.projectContextSummary,
    handoffs: args.handoffs,
    unreadCount: args.unreadCount,
    hasProjectContext: args.projectContextSummary.summaryLines.length > 0,
    hasCommandSupport:
      args.handoffs.length > 0 ||
      args.messages.some(
        (message) => message.sourceScope === "command_support",
      ),
    hasDiagnosticsSummary: args.messages.some(
      (message) => message.sourceScope === "diagnostics",
    ),
    isOverlayOnly: true,
    isUndockable: true,
    defaultVisibility: args.defaultVisibility,
  };
}
