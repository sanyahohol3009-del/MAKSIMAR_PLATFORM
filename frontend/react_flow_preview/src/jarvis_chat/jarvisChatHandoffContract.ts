export type JarvisChatHandoffGuardState =
  | "none"
  | "review_required"
  | "approval_required"
  | "blocked";

export type JarvisChatHandoffExecutionState =
  | "not_started"
  | "preview_only"
  | "queued";

export type JarvisChatHandoffContract = {
  handoffId: string;
  intentLabel: string;
  targetSurface: string;
  guardState: JarvisChatHandoffGuardState;
  executionState: JarvisChatHandoffExecutionState;
  explanation: string;
  requiresApproval: boolean;
  isExecutable: false;
};

export type BuildJarvisChatHandoffContractArgs = {
  handoffId: string;
  intentLabel: string;
  targetSurface: string;
  guardState: JarvisChatHandoffGuardState;
  executionState: JarvisChatHandoffExecutionState;
  explanation: string;
  requiresApproval: boolean;
};

export function buildJarvisChatHandoffContract(
  args: BuildJarvisChatHandoffContractArgs,
): JarvisChatHandoffContract {
  return {
    handoffId: args.handoffId,
    intentLabel: args.intentLabel,
    targetSurface: args.targetSurface,
    guardState: args.guardState,
    executionState: args.executionState,
    explanation: args.explanation,
    requiresApproval: args.requiresApproval,
    isExecutable: false,
  };
}
