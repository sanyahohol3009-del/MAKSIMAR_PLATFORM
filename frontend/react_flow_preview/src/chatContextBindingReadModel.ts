import {
  getChatContextBindingEntry,
  getChatContextBindingGroups,
  chatContextBindingRegistry,
  type ChatContextBindingEntryId,
} from "./chatContextBindingRegistry.js";

export type ChatContextBindingReadModel = {
  totalEntries: number;
  hostEntries: number;
  commandSupportEntries: number;
  guardedEntries: number;
  projectContextBindingReady: boolean;
  groupedBindings: ReadonlyArray<{
    group: string;
    title: string;
    rows: ReadonlyArray<{
      entryId: ChatContextBindingEntryId;
      sourceSurface: string;
      targetSurface: string;
      bindingMode: string;
      historyCompatible: boolean;
      commandPathCompatible: boolean;
      directExecutionAllowed: boolean;
    }>;
  }>;
};

export function buildChatContextBindingReadModel():
  ChatContextBindingReadModel {
  const groupedBindings = getChatContextBindingGroups().map((group) => ({
    group: group.group,
    title: group.title,
    rows: group.entryIds.map((entryId) => {
      const entry = getChatContextBindingEntry(entryId);
      return {
        entryId: entry.entryId,
        sourceSurface: entry.sourceSurface,
        targetSurface: entry.targetSurface,
        bindingMode: entry.bindingMode,
        historyCompatible: entry.historyCompatible,
        commandPathCompatible: entry.commandPathCompatible,
        directExecutionAllowed: entry.directExecutionAllowed,
      };
    }),
  }));

  return {
    totalEntries: chatContextBindingRegistry.length,
    hostEntries: chatContextBindingRegistry.filter(
      (entry) => entry.group === "chat_host",
    ).length,
    commandSupportEntries: chatContextBindingRegistry.filter(
      (entry) => entry.group === "command_support",
    ).length,
    guardedEntries: chatContextBindingRegistry.filter(
      (entry) => entry.guarded,
    ).length,
    projectContextBindingReady: chatContextBindingRegistry.some(
      (entry) =>
        entry.entryId === "project_context_to_embedded_chat_host" &&
        entry.directExecutionAllowed === false &&
        entry.truthBound &&
        entry.operatorVisible,
    ),
    groupedBindings,
  };
}
