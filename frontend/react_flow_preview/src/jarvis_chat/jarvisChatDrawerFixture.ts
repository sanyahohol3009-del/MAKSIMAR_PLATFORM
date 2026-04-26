import { buildMemoryKnowledgeShellReadModel } from "../memoryKnowledgeShellReadModel.js";
import {
  buildJarvisChatMessageContract,
  type JarvisChatMessageContract,
} from "./jarvisChatMessageContract.js";
import {
  buildJarvisChatProjectContextContract,
  type JarvisChatProjectContextContract,
} from "./jarvisChatProjectContextContract.js";
import {
  buildJarvisChatHandoffContract,
  type JarvisChatHandoffContract,
} from "./jarvisChatHandoffContract.js";
import {
  buildJarvisChatSessionContract,
  type JarvisChatSessionContract,
} from "./jarvisChatSessionContract.js";

export type JarvisChatDrawerFixture = {
  session: JarvisChatSessionContract;
  messages: readonly JarvisChatMessageContract[];
  projectContextSummary: JarvisChatProjectContextContract;
  handoffs: readonly JarvisChatHandoffContract[];
};

export function buildJarvisChatDrawerFixture():
  JarvisChatDrawerFixture {
  const projectContextInspect =
    buildMemoryKnowledgeShellReadModel("project_context_summary").activeInspect;

  const projectContextSummary = buildJarvisChatProjectContextContract({
    contextId: "project_context_summary",
    title: projectContextInspect.title,
    summaryLines: [
      projectContextInspect.subtitle,
      projectContextInspect.explanation,
      "Bounded project context is attached to the top chat drawer as a read-only summary.",
    ],
    activeScope: "project_context_summary",
    owner: "surface_intelligence_layer",
    lastUpdatedLabel: "shell-read-model",
    relatedPanelIds: [
      "system_status",
      "topology",
      "action_queue",
    ],
  });

  const messages: readonly JarvisChatMessageContract[] = [
    buildJarvisChatMessageContract({
      messageId: "msg_001",
      role: "system",
      kind: "summary",
      createdAt: "2026-04-26T18:00:00Z",
      title: "Project Context Attached",
      body:
        "Top chat drawer now receives bounded project context as read-only summary.",
      sourceScope: "project_context",
    }),
    buildJarvisChatMessageContract({
      messageId: "msg_002",
      role: "user",
      kind: "text",
      createdAt: "2026-04-26T18:00:10Z",
      body:
        "Show me the current operator shell direction and keep the center canvas untouched.",
      sourceScope: "chat",
    }),
    buildJarvisChatMessageContract({
      messageId: "msg_003",
      role: "jarvis",
      kind: "text",
      createdAt: "2026-04-26T18:00:16Z",
      body:
        "Overlay drawers are active. Center canvas remains persistent and is not resized by drawer open/close actions.",
      sourceScope: "chat",
      traceId: "trace_overlay_001",
    }),
    buildJarvisChatMessageContract({
      messageId: "msg_004",
      role: "jarvis",
      kind: "code",
      createdAt: "2026-04-26T18:00:24Z",
      title: "Preview Code Block",
      body:
        "def preview_overlay_state():\n    return {'left': 'hidden', 'right': 'hidden', 'top': 'hidden'}",
      language: "python",
      sourceScope: "chat",
      traceId: "trace_overlay_002",
    }),
    buildJarvisChatMessageContract({
      messageId: "msg_005",
      role: "system",
      kind: "status",
      createdAt: "2026-04-26T18:00:31Z",
      title: "Command Support",
      body:
        "Command queue and command strip remain visible as guarded support lanes.",
      sourceScope: "command_support",
    }),
    buildJarvisChatMessageContract({
      messageId: "msg_006",
      role: "system",
      kind: "status",
      createdAt: "2026-04-26T18:00:39Z",
      title: "Diagnostics",
      body:
        "No direct execution path is opened from the communication drawer. Guard semantics remain active.",
      sourceScope: "diagnostics",
    }),
  ];

  const handoffs: readonly JarvisChatHandoffContract[] = [
    buildJarvisChatHandoffContract({
      handoffId: "handoff_001",
      intentLabel: "Open panel navigation",
      targetSurface: "panel_navigation",
      guardState: "review_required",
      executionState: "preview_only",
      explanation:
        "The request is routed as an operator-visible preview path before any action layer is considered.",
      requiresApproval: false,
    }),
    buildJarvisChatHandoffContract({
      handoffId: "handoff_002",
      intentLabel: "Apply filesystem patch",
      targetSurface: "filesystem",
      guardState: "approval_required",
      executionState: "not_started",
      explanation:
        "Potential write action remains blocked behind approval and is not executable from the chat drawer.",
      requiresApproval: true,
    }),
  ];

  const session = buildJarvisChatSessionContract({
    sessionId: "jarvis_chat_session_primary",
    displayTitle: "JARVIS Communication Surface",
    collapsedTabLabel: "MAKSIMAR Unified Visual Shell Preview",
    messages,
    projectContextSummary,
    handoffs,
    unreadCount: 2,
    defaultVisibility: "hidden",
  });

  return {
    session,
    messages,
    projectContextSummary,
    handoffs,
  };
}
