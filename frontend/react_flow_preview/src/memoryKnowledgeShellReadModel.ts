import {
  buildMemoryKnowledgeExposureSnapshot,
  buildMemoryKnowledgeInspectPresentation,
} from "./memoryKnowledgeExposureSemantics.js";
import {
  getMemoryKnowledgeExposureEntry,
  type MemoryKnowledgeExposureKey,
} from "./memoryKnowledgeExposureRegistry.js";

export type MemoryKnowledgeShellReadModel = {
  activeExposureKey: MemoryKnowledgeExposureKey;
  activeEntry: ReturnType<typeof getMemoryKnowledgeExposureEntry>;
  activeInspect: ReturnType<typeof buildMemoryKnowledgeInspectPresentation>;
  snapshot: ReturnType<typeof buildMemoryKnowledgeExposureSnapshot>;
};

export function buildMemoryKnowledgeShellReadModel(
  activeExposureKey: MemoryKnowledgeExposureKey,
): MemoryKnowledgeShellReadModel {
  return {
    activeExposureKey,
    activeEntry: getMemoryKnowledgeExposureEntry(activeExposureKey),
    activeInspect: buildMemoryKnowledgeInspectPresentation(activeExposureKey),
    snapshot: buildMemoryKnowledgeExposureSnapshot(),
  };
}
