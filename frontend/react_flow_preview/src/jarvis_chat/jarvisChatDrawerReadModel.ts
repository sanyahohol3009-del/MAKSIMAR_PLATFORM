import { buildChatContextBindingReadModel } from "../chatContextBindingReadModel.js";
import {
  buildJarvisChatDrawerContract,
  type JarvisChatDrawerSectionId,
} from "./jarvisChatDrawerContract.js";
import { buildJarvisChatDrawerFixture } from "./jarvisChatDrawerFixture.js";

type JarvisChatDrawerSectionSummary = {
  sectionId: JarvisChatDrawerSectionId;
  title: string;
  rowCount: number;
};

type JarvisChatConversationRow = {
  messageId: string;
  role: string;
  kind: string;
  title: string | null;
  language: string | null;
};

export type JarvisChatDrawerReadModel = {
  sessionId: string;
  displayTitle: string;
  collapsedStripLabel: string;
  topDrawerHiddenByDefault: boolean;
  preservesCenterCanvas: boolean;
  overlayOnly: boolean;
  chatFirstOrdering: boolean;
  projectContextBindingReady: boolean;
  projectContextVisible: boolean;
  commandSupportVisible: boolean;
  diagnosticsVisible: boolean;
  totalMessages: number;
  codeBlockCount: number;
  copyableCodeCount: number;
  handoffCount: number;
  guardedHandoffCount: number;
  unreadCount: number;
  groupedSections: readonly JarvisChatDrawerSectionSummary[];
  conversationRows: readonly JarvisChatConversationRow[];
};

function getSectionTitle(sectionId: JarvisChatDrawerSectionId): string {
  switch (sectionId) {
    case "conversation":
      return "Conversation";
    case "project_context":
      return "Project Context";
    case "command_handoff":
      return "Command Handoff";
    case "diagnostics":
      return "Diagnostics";
  }
}

export function buildJarvisChatDrawerReadModel():
  JarvisChatDrawerReadModel {
  const drawerContract = buildJarvisChatDrawerContract();
  const fixture = buildJarvisChatDrawerFixture();
  const bindingReadModel = buildChatContextBindingReadModel();

  const diagnosticsRows = fixture.messages.filter(
    (message) => message.sourceScope === "diagnostics",
  );

  const groupedSections = drawerContract.sections.map((sectionId) => {
    switch (sectionId) {
      case "conversation":
        return {
          sectionId,
          title: getSectionTitle(sectionId),
          rowCount: fixture.messages.length,
        };
      case "project_context":
        return {
          sectionId,
          title: getSectionTitle(sectionId),
          rowCount: fixture.projectContextSummary.summaryLines.length,
        };
      case "command_handoff":
        return {
          sectionId,
          title: getSectionTitle(sectionId),
          rowCount: fixture.handoffs.length,
        };
      case "diagnostics":
        return {
          sectionId,
          title: getSectionTitle(sectionId),
          rowCount: diagnosticsRows.length,
        };
    }
  });

  return {
    sessionId: fixture.session.sessionId,
    displayTitle: fixture.session.displayTitle,
    collapsedStripLabel: drawerContract.collapsedStripLabel,
    topDrawerHiddenByDefault: fixture.session.defaultVisibility === "hidden",
    preservesCenterCanvas: drawerContract.preservesCenterCanvas,
    overlayOnly: drawerContract.overlayOnly,
    chatFirstOrdering:
      drawerContract.primarySurface === "jarvis_chat" &&
      drawerContract.sections[0] === "conversation",
    projectContextBindingReady: bindingReadModel.projectContextBindingReady,
    projectContextVisible: fixture.session.hasProjectContext,
    commandSupportVisible: fixture.session.hasCommandSupport,
    diagnosticsVisible: fixture.session.hasDiagnosticsSummary,
    totalMessages: fixture.messages.length,
    codeBlockCount: fixture.messages.filter(
      (message) => message.kind === "code",
    ).length,
    copyableCodeCount: fixture.messages.filter(
      (message) => message.kind === "code" && message.isExecutable === false,
    ).length,
    handoffCount: fixture.handoffs.length,
    guardedHandoffCount: fixture.handoffs.filter(
      (handoff) => handoff.guardState !== "none",
    ).length,
    unreadCount: fixture.session.unreadCount,
    groupedSections,
    conversationRows: fixture.messages.map((message) => ({
      messageId: message.messageId,
      role: message.role,
      kind: message.kind,
      title: message.title,
      language: message.language,
    })),
  };
}
