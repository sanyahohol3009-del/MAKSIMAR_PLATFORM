import { buildChatContextBindingReadModel } from "../chatContextBindingReadModel.js";
import { buildJarvisChatDrawerFixture } from "./jarvisChatDrawerFixture.js";
import {
  buildEmbeddedChatSurfaceRegistry,
  type EmbeddedChatSurfaceEntry,
  type EmbeddedChatSurfaceShellLane,
} from "./embeddedChatSurfaceRegistry.js";

type EmbeddedChatSurfaceRow = {
  surfaceId: EmbeddedChatSurfaceEntry["surfaceId"];
  title: string;
  shellLane: EmbeddedChatSurfaceShellLane;
  bindingStatus: EmbeddedChatSurfaceEntry["bindingStatus"];
  countLabel: string;
  countValue: number;
  copyable: boolean;
};

type EmbeddedChatSurfaceGroup = {
  shellLane: EmbeddedChatSurfaceShellLane;
  title: string;
  rows: readonly EmbeddedChatSurfaceRow[];
};

export type EmbeddedChatSurfaceReadModel = {
  totalSurfaces: number;
  totalHistoryMessages: number;
  totalCodeBlocks: number;
  totalCommandSupportUnits: number;
  projectContextBindingReady: boolean;
  copyableCodeBlocks: number;
  groupedRows: readonly EmbeddedChatSurfaceGroup[];
};

function getLaneTitle(
  shellLane: EmbeddedChatSurfaceShellLane,
): string {
  switch (shellLane) {
    case "communication":
      return "Communication";
    case "history":
      return "History";
    case "output":
      return "Output";
    case "support":
      return "Support";
  }
}

export function buildEmbeddedChatSurfaceReadModel():
  EmbeddedChatSurfaceReadModel {
  const registry = buildEmbeddedChatSurfaceRegistry();
  const fixture = buildJarvisChatDrawerFixture();
  const bindingReadModel = buildChatContextBindingReadModel();

  const totalHistoryMessages = fixture.messages.length;
  const totalCodeBlocks = fixture.messages.filter(
    (message) => message.kind === "code",
  ).length;
  const totalCommandSupportUnits =
    fixture.messages.filter(
      (message) => message.sourceScope === "command_support",
    ).length + fixture.handoffs.length;

  const rows: readonly EmbeddedChatSurfaceRow[] = registry.map((entry) => {
    switch (entry.surfaceId) {
      case "project_context_host":
        return {
          surfaceId: entry.surfaceId,
          title: entry.title,
          shellLane: entry.shellLane,
          bindingStatus: entry.bindingStatus,
          countLabel: "summary_lines",
          countValue: fixture.projectContextSummary.summaryLines.length,
          copyable: entry.copyable,
        };

      case "conversation_history_lane":
        return {
          surfaceId: entry.surfaceId,
          title: entry.title,
          shellLane: entry.shellLane,
          bindingStatus: entry.bindingStatus,
          countLabel: "messages",
          countValue: totalHistoryMessages,
          copyable: entry.copyable,
        };

      case "code_output_lane":
        return {
          surfaceId: entry.surfaceId,
          title: entry.title,
          shellLane: entry.shellLane,
          bindingStatus: entry.bindingStatus,
          countLabel: "code_blocks",
          countValue: totalCodeBlocks,
          copyable: entry.copyable,
        };

      case "command_support_lane":
        return {
          surfaceId: entry.surfaceId,
          title: entry.title,
          shellLane: entry.shellLane,
          bindingStatus: entry.bindingStatus,
          countLabel: "support_units",
          countValue: totalCommandSupportUnits,
          copyable: entry.copyable,
        };
    }
  });

  const laneOrder: readonly EmbeddedChatSurfaceShellLane[] = [
    "communication",
    "history",
    "output",
    "support",
  ];

  const groupedRows: readonly EmbeddedChatSurfaceGroup[] = laneOrder.map(
    (shellLane) => ({
      shellLane,
      title: getLaneTitle(shellLane),
      rows: rows.filter((row) => row.shellLane === shellLane),
    }),
  );

  return {
    totalSurfaces: registry.length,
    totalHistoryMessages,
    totalCodeBlocks,
    totalCommandSupportUnits,
    projectContextBindingReady: bindingReadModel.projectContextBindingReady,
    copyableCodeBlocks: totalCodeBlocks,
    groupedRows,
  };
}
