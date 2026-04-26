export type JarvisChatMessageRole =
  | "user"
  | "jarvis"
  | "system";

export type JarvisChatMessageKind =
  | "text"
  | "code"
  | "status"
  | "summary";

export type JarvisChatMessageSourceScope =
  | "chat"
  | "project_context"
  | "diagnostics"
  | "command_support";

export type JarvisChatMessageContract = {
  messageId: string;
  role: JarvisChatMessageRole;
  kind: JarvisChatMessageKind;
  createdAt: string;
  traceId: string | null;
  title: string | null;
  body: string;
  language: string | null;
  isGuarded: boolean;
  isExecutable: false;
  sourceScope: JarvisChatMessageSourceScope;
};

export type BuildJarvisChatMessageContractArgs = {
  messageId: string;
  role: JarvisChatMessageRole;
  kind: JarvisChatMessageKind;
  createdAt: string;
  body: string;
  sourceScope: JarvisChatMessageSourceScope;
  traceId?: string | null;
  title?: string | null;
  language?: string | null;
  isGuarded?: boolean;
};

export function buildJarvisChatMessageContract(
  args: BuildJarvisChatMessageContractArgs,
): JarvisChatMessageContract {
  return {
    messageId: args.messageId,
    role: args.role,
    kind: args.kind,
    createdAt: args.createdAt,
    traceId: args.traceId ?? null,
    title: args.title ?? null,
    body: args.body,
    language: args.kind === "code" ? (args.language ?? "text") : null,
    isGuarded: args.isGuarded ?? true,
    isExecutable: false,
    sourceScope: args.sourceScope,
  };
}
