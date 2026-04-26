import { buildJarvisChatDrawerFixture } from "./jarvisChatDrawerFixture.js";
import {
  getEmbeddedChatSurfaceEntry,
  type EmbeddedChatSurfaceId,
} from "./embeddedChatSurfaceRegistry.js";

export type EmbeddedChatSurfaceInspectPresentation = {
  title: string;
  subtitle: string;
  semanticKind: string;
  explanation: string;
  sections: readonly {
    title: string;
    items: readonly {
      key: string;
      value: string;
    }[];
  }[];
};

export function buildEmbeddedChatSurfaceInspectPresentation(
  surfaceId: EmbeddedChatSurfaceId,
): EmbeddedChatSurfaceInspectPresentation {
  const entry = getEmbeddedChatSurfaceEntry(surfaceId);
  const fixture = buildJarvisChatDrawerFixture();

  switch (surfaceId) {
    case "project_context_host":
      return {
        title: entry.title,
        subtitle: entry.targetSurface,
        semanticKind: "embedded_chat_surface",
        explanation:
          "Project context remains bounded, read-only, and attached to the communication surface without direct execution.",
        sections: [
          {
            title: "Surface Identity",
            items: [
              { key: "Surface Id", value: entry.surfaceId },
              { key: "Shell Lane", value: entry.shellLane },
              { key: "Binding Status", value: entry.bindingStatus },
              { key: "Canonical Owner", value: entry.canonicalOwner },
            ],
          },
          {
            title: "Project Context",
            items: [
              {
                key: "Summary Lines",
                value: String(fixture.projectContextSummary.summaryLines.length),
              },
              {
                key: "Active Scope",
                value: fixture.projectContextSummary.activeScope,
              },
              {
                key: "Read-Only",
                value: String(fixture.projectContextSummary.readOnly),
              },
            ],
          },
        ],
      };

    case "conversation_history_lane":
      return {
        title: entry.title,
        subtitle: entry.targetSurface,
        semanticKind: "embedded_chat_surface",
        explanation:
          "Conversation history is visible inside the chat drawer, but live backend history binding is still pending.",
        sections: [
          {
            title: "History Identity",
            items: [
              { key: "Surface Id", value: entry.surfaceId },
              { key: "Shell Lane", value: entry.shellLane },
              { key: "Binding Status", value: entry.bindingStatus },
              { key: "Message Count", value: String(fixture.messages.length) },
            ],
          },
          {
            title: "Safety Boundary",
            items: [
              { key: "Read-Only", value: String(entry.readOnly) },
              { key: "Non-Executable", value: String(entry.nonExecutable) },
            ],
          },
        ],
      };

    case "code_output_lane":
      return {
        title: entry.title,
        subtitle: entry.targetSurface,
        semanticKind: "embedded_chat_surface",
        explanation:
          "Code output is rendered as copyable content only. The lane never acts as an execution surface.",
        sections: [
          {
            title: "Code Output Identity",
            items: [
              { key: "Surface Id", value: entry.surfaceId },
              { key: "Shell Lane", value: entry.shellLane },
              { key: "Binding Status", value: entry.bindingStatus },
            ],
          },
          {
            title: "Code Output Safety",
            items: [
              {
                key: "Code Blocks",
                value: String(
                  fixture.messages.filter((message) => message.kind === "code")
                    .length,
                ),
              },
              { key: "Copyable", value: String(entry.copyable) },
              { key: "Non-Executable", value: String(entry.nonExecutable) },
            ],
          },
        ],
      };

    case "command_support_lane":
      return {
        title: entry.title,
        subtitle: entry.targetSurface,
        semanticKind: "embedded_chat_surface",
        explanation:
          "Command support remains a guarded visibility layer that shows handoff state without allowing direct execution.",
        sections: [
          {
            title: "Support Identity",
            items: [
              { key: "Surface Id", value: entry.surfaceId },
              { key: "Shell Lane", value: entry.shellLane },
              { key: "Binding Status", value: entry.bindingStatus },
            ],
          },
          {
            title: "Guarded Support",
            items: [
              {
                key: "Command Support Messages",
                value: String(
                  fixture.messages.filter(
                    (message) => message.sourceScope === "command_support",
                  ).length,
                ),
              },
              {
                key: "Handoffs",
                value: String(fixture.handoffs.length),
              },
              {
                key: "Non-Executable",
                value: String(entry.nonExecutable),
              },
            ],
          },
        ],
      };
  }
}
