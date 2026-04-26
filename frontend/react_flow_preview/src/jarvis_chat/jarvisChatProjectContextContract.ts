export type JarvisChatProjectContextContract = {
  contextId: string;
  title: string;
  summaryLines: readonly string[];
  activeScope: string;
  owner: string;
  lastUpdatedLabel: string;
  relatedPanelIds: readonly string[];
  readOnly: true;
};

export type BuildJarvisChatProjectContextContractArgs = {
  contextId: string;
  title: string;
  summaryLines: readonly string[];
  activeScope: string;
  owner: string;
  lastUpdatedLabel: string;
  relatedPanelIds: readonly string[];
};

export function buildJarvisChatProjectContextContract(
  args: BuildJarvisChatProjectContextContractArgs,
): JarvisChatProjectContextContract {
  return {
    contextId: args.contextId,
    title: args.title,
    summaryLines: args.summaryLines,
    activeScope: args.activeScope,
    owner: args.owner,
    lastUpdatedLabel: args.lastUpdatedLabel,
    relatedPanelIds: args.relatedPanelIds,
    readOnly: true,
  };
}
