export type ChatContextBindingEntryId =
  | "project_context_to_embedded_chat_host"
  | "chat_panel_host_contract_binding"
  | "command_queue_chat_support_binding"
  | "command_strip_chat_support_binding";

export type ChatContextBindingSource =
  | "project_context_summary_shell_exposure"
  | "frontend_chat_panel_contract"
  | "frontend_command_queue_contract"
  | "frontend_command_strip_contract";

export type ChatContextBindingTarget =
  | "embedded_chat_host"
  | "embedded_chat_command_queue"
  | "embedded_chat_command_strip";

export type ChatContextBindingMode =
  | "read_only_context_binding"
  | "chat_host_capability_binding"
  | "command_queue_visibility_binding"
  | "command_strip_visibility_binding";

export type ChatContextBindingGroup =
  | "chat_host"
  | "command_support";

export type ChatContextBindingRegistryEntry = {
  entryId: ChatContextBindingEntryId;
  order: number;
  sourceSurface: ChatContextBindingSource;
  targetSurface: ChatContextBindingTarget;
  bindingMode: ChatContextBindingMode;
  group: ChatContextBindingGroup;
  operatorVisible: boolean;
  truthBound: boolean;
  guarded: boolean;
  directExecutionAllowed: boolean;
  historyCompatible: boolean;
  commandPathCompatible: boolean;
  rationale: string;
};

export const chatContextBindingRegistry:
  ReadonlyArray<ChatContextBindingRegistryEntry> = [
    {
      entryId: "project_context_to_embedded_chat_host",
      order: 1,
      sourceSurface: "project_context_summary_shell_exposure",
      targetSurface: "embedded_chat_host",
      bindingMode: "read_only_context_binding",
      group: "chat_host",
      operatorVisible: true,
      truthBound: true,
      guarded: true,
      directExecutionAllowed: false,
      historyCompatible: true,
      commandPathCompatible: true,
      rationale:
        "Project context enters the embedded chat host as bounded read-only context rather than as a direct execution path.",
    },
    {
      entryId: "chat_panel_host_contract_binding",
      order: 2,
      sourceSurface: "frontend_chat_panel_contract",
      targetSurface: "embedded_chat_host",
      bindingMode: "chat_host_capability_binding",
      group: "chat_host",
      operatorVisible: true,
      truthBound: true,
      guarded: true,
      directExecutionAllowed: false,
      historyCompatible: true,
      commandPathCompatible: true,
      rationale:
        "Frontend chat panel acts as the visible host surface for bounded project-aware conversation.",
    },
    {
      entryId: "command_queue_chat_support_binding",
      order: 3,
      sourceSurface: "frontend_command_queue_contract",
      targetSurface: "embedded_chat_command_queue",
      bindingMode: "command_queue_visibility_binding",
      group: "command_support",
      operatorVisible: true,
      truthBound: true,
      guarded: true,
      directExecutionAllowed: false,
      historyCompatible: true,
      commandPathCompatible: true,
      rationale:
        "Command queue remains visible as a guarded support lane for chat-driven operator flow.",
    },
    {
      entryId: "command_strip_chat_support_binding",
      order: 4,
      sourceSurface: "frontend_command_strip_contract",
      targetSurface: "embedded_chat_command_strip",
      bindingMode: "command_strip_visibility_binding",
      group: "command_support",
      operatorVisible: true,
      truthBound: true,
      guarded: true,
      directExecutionAllowed: false,
      historyCompatible: true,
      commandPathCompatible: true,
      rationale:
        "Command strip remains visible as a guarded support lane for chat-driven operator flow.",
    },
  ];

export function getChatContextBindingEntry(
  entryId: ChatContextBindingEntryId,
): ChatContextBindingRegistryEntry {
  const entry = chatContextBindingRegistry.find(
    (candidate) => candidate.entryId === entryId,
  );

  if (!entry) {
    throw new Error(`Missing chat context binding entry for ${entryId}.`);
  }

  return entry;
}

export function getChatContextBindingOrder():
  ChatContextBindingEntryId[] {
  return chatContextBindingRegistry.map((entry) => entry.entryId);
}

export function getChatContextBindingGroups(): ReadonlyArray<{
  group: ChatContextBindingGroup;
  title: string;
  entryIds: ChatContextBindingEntryId[];
}> {
  const titles: Record<ChatContextBindingGroup, string> = {
    chat_host: "Embedded Chat Host",
    command_support: "Command Support",
  };

  const order: readonly ChatContextBindingGroup[] = [
    "chat_host",
    "command_support",
  ];

  return order.map((group) => ({
    group,
    title: titles[group],
    entryIds: chatContextBindingRegistry
      .filter((entry) => entry.group === group)
      .map((entry) => entry.entryId),
  }));
}
