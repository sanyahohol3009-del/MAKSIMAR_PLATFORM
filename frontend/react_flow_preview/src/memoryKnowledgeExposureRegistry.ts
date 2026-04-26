export type MemoryKnowledgeExposureKey =
  | "memory_registry_summary"
  | "knowledge_registry_summary"
  | "project_context_summary"
  | "memory_policy_summary";

export type MemoryKnowledgeTargetSurface =
  | "inspect"
  | "explain"
  | "chat_context";

export type MemoryKnowledgeExposureEntry = {
  exposureKey: MemoryKnowledgeExposureKey;
  order: number;
  title: string;
  subtitle: string;
  targetSurface: MemoryKnowledgeTargetSurface;
  canonicalOwner: string;
  rationale: string;
  backendBoundary: string;
};

export const memoryKnowledgeExposureRegistry:
  ReadonlyArray<MemoryKnowledgeExposureEntry> = [
    {
      exposureKey: "memory_registry_summary",
      order: 1,
      title: "Memory Registry Summary",
      subtitle:
        "Read-only exposure of loaded memory definitions and retrieval summaries.",
      targetSurface: "inspect",
      canonicalOwner: "memory_engine_layer",
      rationale:
        "Memory engine already exposes registry, loader, accessor and retrieval summary primitives.",
      backendBoundary:
        "Raw memory registry internals stay backend-only; shell receives read-only summary.",
    },
    {
      exposureKey: "knowledge_registry_summary",
      order: 2,
      title: "Knowledge Registry Summary",
      subtitle:
        "Read-only exposure of loaded knowledge definitions and retrieval summaries.",
      targetSurface: "inspect",
      canonicalOwner: "knowledge_engine_layer",
      rationale:
        "Knowledge engine already exposes registry, loader, accessor and retrieval summary primitives.",
      backendBoundary:
        "Raw knowledge registry internals stay backend-only; shell receives read-only summary.",
    },
    {
      exposureKey: "project_context_summary",
      order: 3,
      title: "Project Context Summary",
      subtitle:
        "Project-aware context that can later feed inspect, explain and chat context surfaces.",
      targetSurface: "chat_context",
      canonicalOwner: "surface_intelligence_layer",
      rationale:
        "Project context should become visible to operator/chat flows without exposing raw memory internals.",
      backendBoundary:
        "Project context derivation stays backend-side; shell receives bounded context summary only.",
    },
    {
      exposureKey: "memory_policy_summary",
      order: 4,
      title: "Memory Policy Summary",
      subtitle:
        "Explainable summary of memory classification safeguards and write restrictions.",
      targetSurface: "explain",
      canonicalOwner: "memory_policy_layer",
      rationale:
        "Memory classification policy is critical and should be visible as explainable guard semantics.",
      backendBoundary:
        "Approval, deduplication, conflict resolution and provenance enforcement remain backend-only.",
    },
  ];

export function getMemoryKnowledgeExposureOrder():
  MemoryKnowledgeExposureKey[] {
  return memoryKnowledgeExposureRegistry.map((entry) => entry.exposureKey);
}

export function getMemoryKnowledgeExposureEntry(
  exposureKey: MemoryKnowledgeExposureKey,
): MemoryKnowledgeExposureEntry {
  const entry = memoryKnowledgeExposureRegistry.find(
    (candidate) => candidate.exposureKey === exposureKey,
  );

  if (!entry) {
    throw new Error(
      `Missing memory/knowledge exposure registry entry for ${exposureKey}.`,
    );
  }

  return entry;
}

export function getMemoryKnowledgeExposureGroups(): ReadonlyArray<{
  targetSurface: MemoryKnowledgeTargetSurface;
  title: string;
  exposureKeys: MemoryKnowledgeExposureKey[];
}> {
  const targetTitles: Record<MemoryKnowledgeTargetSurface, string> = {
    inspect: "Inspect Surface",
    explain: "Explain Surface",
    chat_context: "Chat Context Surface",
  };

  const order: readonly MemoryKnowledgeTargetSurface[] = [
    "inspect",
    "explain",
    "chat_context",
  ];

  return order.map((targetSurface) => ({
    targetSurface,
    title: targetTitles[targetSurface],
    exposureKeys: memoryKnowledgeExposureRegistry
      .filter((entry) => entry.targetSurface === targetSurface)
      .map((entry) => entry.exposureKey),
  }));
}
