import {
  getMemoryKnowledgeExposureEntry,
  getMemoryKnowledgeExposureGroups,
  memoryKnowledgeExposureRegistry,
  type MemoryKnowledgeExposureKey,
} from "./memoryKnowledgeExposureRegistry.js";
import { buildDefaultInspectPresentation } from "./graphInspectSemantics.js";

export type MemoryKnowledgeInspectPresentation =
  ReturnType<typeof buildDefaultInspectPresentation>;

export type MemoryKnowledgeExposureSnapshot = {
  totalEntries: number;
  inspectEntries: number;
  explainEntries: number;
  chatContextEntries: number;
  groupedEntries: ReadonlyArray<{
    targetSurface: string;
    title: string;
    entries: ReadonlyArray<{
      exposureKey: MemoryKnowledgeExposureKey;
      title: string;
      subtitle: string;
      canonicalOwner: string;
    }>;
  }>;
};

export function buildMemoryKnowledgeExposureSnapshot():
  MemoryKnowledgeExposureSnapshot {
  const groupedEntries = getMemoryKnowledgeExposureGroups().map((group) => ({
    targetSurface: group.targetSurface,
    title: group.title,
    entries: group.exposureKeys.map((exposureKey) => {
      const entry = getMemoryKnowledgeExposureEntry(exposureKey);
      return {
        exposureKey: entry.exposureKey,
        title: entry.title,
        subtitle: entry.subtitle,
        canonicalOwner: entry.canonicalOwner,
      };
    }),
  }));

  return {
    totalEntries: memoryKnowledgeExposureRegistry.length,
    inspectEntries: memoryKnowledgeExposureRegistry.filter(
      (entry) => entry.targetSurface === "inspect",
    ).length,
    explainEntries: memoryKnowledgeExposureRegistry.filter(
      (entry) => entry.targetSurface === "explain",
    ).length,
    chatContextEntries: memoryKnowledgeExposureRegistry.filter(
      (entry) => entry.targetSurface === "chat_context",
    ).length,
    groupedEntries,
  };
}

export function buildMemoryKnowledgeInspectPresentation(
  exposureKey: MemoryKnowledgeExposureKey,
): MemoryKnowledgeInspectPresentation {
  const entry = getMemoryKnowledgeExposureEntry(exposureKey);

  return {
    title: entry.title,
    subtitle: entry.subtitle,
    semanticKind: `${entry.targetSurface}_memory_knowledge_exposure`,
    explanation: entry.rationale,
    sections: [
      {
        title: "Shell Landing",
        items: [
          {
            key: "Target Surface",
            value: entry.targetSurface,
          },
          {
            key: "Canonical Owner",
            value: entry.canonicalOwner,
          },
        ],
      },
      {
        title: "Backend Boundary",
        items: [
          {
            key: "Boundary",
            value: entry.backendBoundary,
          },
        ],
      },
    ],
  };
}
