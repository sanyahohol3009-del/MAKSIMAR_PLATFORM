import { buildChatContextBindingReadModel } from "../chatContextBindingReadModel.js";
import {
  buildEmbeddedChatSurfaceReadModel,
  type EmbeddedChatSurfaceReadModel,
} from "./embeddedChatSurfaceReadModel.js";
import {
  buildEmbeddedChatSurfaceRegistry,
  type EmbeddedChatSurfaceEntry,
  type EmbeddedChatSurfaceId,
} from "./embeddedChatSurfaceRegistry.js";

export type EmbeddedChatShellExposureTarget =
  | "top_drawer_primary"
  | "left_drawer_context_reference"
  | "right_drawer_inspect_reference";

export type EmbeddedChatShellExposureMode =
  | "primary"
  | "reference_only";

export type EmbeddedChatShellExposureRow = {
  surfaceId: EmbeddedChatSurfaceId;
  title: string;
  target: EmbeddedChatShellExposureTarget;
  exposureMode: EmbeddedChatShellExposureMode;
  targetSection: string;
  bindingStatus: EmbeddedChatSurfaceEntry["bindingStatus"];
  copyable: boolean;
  countLabel: string;
  countValue: number;
};

type EmbeddedChatShellExposureGroup = {
  target: EmbeddedChatShellExposureTarget;
  title: string;
  rows: readonly EmbeddedChatShellExposureRow[];
};

export type EmbeddedChatShellExposureReadModel = {
  totalSurfaceRows: number;
  primaryTopDrawerRows: number;
  leftReferenceRows: number;
  rightReferenceRows: number;
  projectContextBindingReady: boolean;
  duplicationControlEnabled: true;
  groupedExposure: readonly EmbeddedChatShellExposureGroup[];
};

function getExposureTitle(
  target: EmbeddedChatShellExposureTarget,
): string {
  switch (target) {
    case "top_drawer_primary":
      return "Top Drawer Primary";
    case "left_drawer_context_reference":
      return "Left Drawer Context Reference";
    case "right_drawer_inspect_reference":
      return "Right Drawer Inspect Reference";
  }
}

function resolveCountForSurface(
  surfaceId: EmbeddedChatSurfaceId,
  surfaceReadModel: EmbeddedChatSurfaceReadModel,
): { countLabel: string; countValue: number } {
  switch (surfaceId) {
    case "project_context_host":
      return { countLabel: "summary_lines", countValue: 3 };
    case "conversation_history_lane":
      return {
        countLabel: "messages",
        countValue: surfaceReadModel.totalHistoryMessages,
      };
    case "code_output_lane":
      return {
        countLabel: "code_blocks",
        countValue: surfaceReadModel.totalCodeBlocks,
      };
    case "command_support_lane":
      return {
        countLabel: "support_units",
        countValue: surfaceReadModel.totalCommandSupportUnits,
      };
  }
}

export function buildEmbeddedChatShellExposureReadModel():
  EmbeddedChatShellExposureReadModel {
  const registry = buildEmbeddedChatSurfaceRegistry();
  const surfaceReadModel = buildEmbeddedChatSurfaceReadModel();
  const bindingReadModel = buildChatContextBindingReadModel();

  const primaryRows: readonly EmbeddedChatShellExposureRow[] = registry.map(
    (entry) => {
      const count = resolveCountForSurface(entry.surfaceId, surfaceReadModel);

      return {
        surfaceId: entry.surfaceId,
        title: entry.title,
        target: "top_drawer_primary",
        exposureMode: "primary",
        targetSection: "jarvis_chat_drawer",
        bindingStatus: entry.bindingStatus,
        copyable: entry.copyable,
        countLabel: count.countLabel,
        countValue: count.countValue,
      };
    },
  );

  const leftReferenceRows: readonly EmbeddedChatShellExposureRow[] = [
    registry.find((entry) => entry.surfaceId === "project_context_host"),
  ]
    .filter((entry): entry is EmbeddedChatSurfaceEntry => entry !== undefined)
    .map((entry) => {
      const count = resolveCountForSurface(entry.surfaceId, surfaceReadModel);

      return {
        surfaceId: entry.surfaceId,
        title: entry.title,
        target: "left_drawer_context_reference",
        exposureMode: "reference_only",
        targetSection: "embedded_chat_context",
        bindingStatus: entry.bindingStatus,
        copyable: entry.copyable,
        countLabel: count.countLabel,
        countValue: count.countValue,
      };
    });

  const rightReferenceRows: readonly EmbeddedChatShellExposureRow[] = [
    registry.find((entry) => entry.surfaceId === "command_support_lane"),
  ]
    .filter((entry): entry is EmbeddedChatSurfaceEntry => entry !== undefined)
    .map((entry) => {
      const count = resolveCountForSurface(entry.surfaceId, surfaceReadModel);

      return {
        surfaceId: entry.surfaceId,
        title: entry.title,
        target: "right_drawer_inspect_reference",
        exposureMode: "reference_only",
        targetSection: "inspect",
        bindingStatus: entry.bindingStatus,
        copyable: entry.copyable,
        countLabel: count.countLabel,
        countValue: count.countValue,
      };
    });

  const exposureTargetOrder: readonly EmbeddedChatShellExposureTarget[] = [
    "top_drawer_primary",
    "left_drawer_context_reference",
    "right_drawer_inspect_reference",
  ];

  const allRows: readonly EmbeddedChatShellExposureRow[] = [
    ...primaryRows,
    ...leftReferenceRows,
    ...rightReferenceRows,
  ];

  const groupedExposure: readonly EmbeddedChatShellExposureGroup[] =
    exposureTargetOrder.map((target) => ({
      target,
      title: getExposureTitle(target),
      rows: allRows.filter((row) => row.target === target),
    }));

  return {
    totalSurfaceRows: allRows.length,
    primaryTopDrawerRows: primaryRows.length,
    leftReferenceRows: leftReferenceRows.length,
    rightReferenceRows: rightReferenceRows.length,
    projectContextBindingReady: bindingReadModel.projectContextBindingReady,
    duplicationControlEnabled: true,
    groupedExposure,
  };
}
