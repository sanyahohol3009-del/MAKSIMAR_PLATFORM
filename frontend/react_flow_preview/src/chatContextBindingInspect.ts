import { buildDefaultInspectPresentation } from "./graphInspectSemantics.js";
import {
  getChatContextBindingEntry,
  type ChatContextBindingEntryId,
} from "./chatContextBindingRegistry.js";

export type ChatContextBindingInspectPresentation =
  ReturnType<typeof buildDefaultInspectPresentation>;

export function getChatContextBindingDisplayTitle(
  entryId: ChatContextBindingEntryId,
): string {
  switch (entryId) {
    case "project_context_to_embedded_chat_host":
      return "Project Context → Embedded Chat Host";
    case "chat_panel_host_contract_binding":
      return "Chat Panel → Embedded Chat Host";
    case "command_queue_chat_support_binding":
      return "Command Queue → Chat Support";
    case "command_strip_chat_support_binding":
      return "Command Strip → Chat Support";
  }
}

export function buildChatContextBindingInspectPresentation(
  entryId: ChatContextBindingEntryId,
): ChatContextBindingInspectPresentation {
  const entry = getChatContextBindingEntry(entryId);

  return {
    title: getChatContextBindingDisplayTitle(entryId),
    subtitle:
      `Chat context binding lane from ${entry.sourceSurface} to ${entry.targetSurface}.`,
    semanticKind: "embedded_chat_context_binding",
    explanation: entry.rationale,
    sections: [
      {
        title: "Binding Path",
        items: [
          {
            key: "Source Surface",
            value: entry.sourceSurface,
          },
          {
            key: "Target Surface",
            value: entry.targetSurface,
          },
          {
            key: "Binding Mode",
            value: entry.bindingMode,
          },
          {
            key: "Group",
            value: entry.group,
          },
        ],
      },
      {
        title: "Safety and Compatibility",
        items: [
          {
            key: "Operator Visible",
            value: String(entry.operatorVisible),
          },
          {
            key: "Truth Bound",
            value: String(entry.truthBound),
          },
          {
            key: "Guarded",
            value: String(entry.guarded),
          },
          {
            key: "Direct Execution Allowed",
            value: String(entry.directExecutionAllowed),
          },
          {
            key: "History Compatible",
            value: String(entry.historyCompatible),
          },
          {
            key: "Command Path Compatible",
            value: String(entry.commandPathCompatible),
          },
        ],
      },
    ],
  };
}
