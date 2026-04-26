export type EmbeddedChatSurfaceId =
  | "project_context_host"
  | "conversation_history_lane"
  | "code_output_lane"
  | "command_support_lane";

export type EmbeddedChatSurfaceShellLane =
  | "communication"
  | "history"
  | "output"
  | "support";

export type EmbeddedChatSurfaceBindingStatus =
  | "preview_ready"
  | "history_pending"
  | "runtime_pending";

export type EmbeddedChatSurfaceEntry = {
  surfaceId: EmbeddedChatSurfaceId;
  title: string;
  summary: string;
  targetSurface: string;
  shellLane: EmbeddedChatSurfaceShellLane;
  canonicalOwner: string;
  sourceScope: string;
  bindingStatus: EmbeddedChatSurfaceBindingStatus;
  readOnly: true;
  copyable: boolean;
  nonExecutable: true;
};

export const embeddedChatSurfaceOrder: readonly EmbeddedChatSurfaceId[] = [
  "project_context_host",
  "conversation_history_lane",
  "code_output_lane",
  "command_support_lane",
] as const;

const embeddedChatSurfaceRegistryRecord: Record<
  EmbeddedChatSurfaceId,
  EmbeddedChatSurfaceEntry
> = {
  project_context_host: {
    surfaceId: "project_context_host",
    title: "Project Context Host",
    summary:
      "Read-only bounded project context host attached to the embedded communication surface.",
    targetSurface: "top_chat_drawer",
    shellLane: "communication",
    canonicalOwner: "jarvis_chat_drawer_layer",
    sourceScope: "project_context",
    bindingStatus: "preview_ready",
    readOnly: true,
    copyable: false,
    nonExecutable: true,
  },
  conversation_history_lane: {
    surfaceId: "conversation_history_lane",
    title: "Conversation History Lane",
    summary:
      "Visible conversation/history lane for operator review inside the embedded chat surface.",
    targetSurface: "top_chat_drawer",
    shellLane: "history",
    canonicalOwner: "jarvis_chat_drawer_layer",
    sourceScope: "chat",
    bindingStatus: "history_pending",
    readOnly: true,
    copyable: false,
    nonExecutable: true,
  },
  code_output_lane: {
    surfaceId: "code_output_lane",
    title: "Code Output Lane",
    summary:
      "Copyable code/result lane inside the embedded chat surface without direct execution.",
    targetSurface: "top_chat_drawer",
    shellLane: "output",
    canonicalOwner: "jarvis_chat_drawer_layer",
    sourceScope: "chat",
    bindingStatus: "preview_ready",
    readOnly: true,
    copyable: true,
    nonExecutable: true,
  },
  command_support_lane: {
    surfaceId: "command_support_lane",
    title: "Command Support Lane",
    summary:
      "Guarded command-support and handoff visibility lane for preview-only operator flow.",
    targetSurface: "top_chat_drawer",
    shellLane: "support",
    canonicalOwner: "jarvis_chat_drawer_layer",
    sourceScope: "command_support",
    bindingStatus: "runtime_pending",
    readOnly: true,
    copyable: false,
    nonExecutable: true,
  },
};

export function buildEmbeddedChatSurfaceRegistry():
  readonly EmbeddedChatSurfaceEntry[] {
  return embeddedChatSurfaceOrder.map(
    (surfaceId) => embeddedChatSurfaceRegistryRecord[surfaceId],
  );
}

export function getEmbeddedChatSurfaceEntry(
  surfaceId: EmbeddedChatSurfaceId,
): EmbeddedChatSurfaceEntry {
  return embeddedChatSurfaceRegistryRecord[surfaceId];
}
