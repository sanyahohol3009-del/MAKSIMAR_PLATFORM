import type { JarvisChatDrawerSectionId } from "../../jarvis_chat/jarvisChatDrawerContract.js";
import type { EmbeddedChatSurfaceId } from "../../jarvis_chat/embeddedChatSurfaceRegistry.js";

type EmbeddedChatSurfaceExposureRow = {
  surfaceId: EmbeddedChatSurfaceId;
  title: string;
};

type EmbeddedChatSurfaceExposureGroup = {
  rows: readonly EmbeddedChatSurfaceExposureRow[];
} | null;

export function getPreferredJarvisSection(
  surfaceId: EmbeddedChatSurfaceId,
): JarvisChatDrawerSectionId {
  switch (surfaceId) {
    case "project_context_host":
      return "project_context";

    case "conversation_history_lane":
      return "conversation";

    case "code_output_lane":
      return "conversation";

    case "command_support_lane":
      return "command_handoff";
  }
}

export function getEmbeddedChatSurfaceLabel(
  topDrawerExposureGroup: EmbeddedChatSurfaceExposureGroup,
  activeEmbeddedChatSurface: EmbeddedChatSurfaceId,
): string {
  return (
    topDrawerExposureGroup?.rows.find(
      (row) => row.surfaceId === activeEmbeddedChatSurface,
    )?.title ?? activeEmbeddedChatSurface
  );
}
