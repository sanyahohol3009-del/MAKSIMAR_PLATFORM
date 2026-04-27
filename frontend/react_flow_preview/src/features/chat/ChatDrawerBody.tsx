import React from "react";

import type { JarvisChatDrawerSectionId } from "../../jarvis_chat/jarvisChatDrawerContract.js";
import { ChatConversationPane, type ChatConversationMessage } from "./ChatConversationPane.js";
import { ChatInputBar } from "./ChatInputBar.js";

type ProjectContextSummary = {
  title: string;
  activeScope: string;
  owner: string;
  lastUpdatedLabel: string;
  summaryLines: readonly string[];
};

type CommandHandoff = {
  handoffId: string;
  guardState: string;
  executionState: string;
  requiresApproval: boolean;
  intentLabel: string;
  targetSurface: string;
  explanation: string;
};

type ChatDrawerBodyProps = {
  activeJarvisChatSection: JarvisChatDrawerSectionId;
  messages: readonly ChatConversationMessage[];
  projectContextSummary: ProjectContextSummary;
  handoffs: readonly CommandHandoff[];
  diagnosticsMessages: readonly ChatConversationMessage[];
};

export function ChatDrawerBody({
  activeJarvisChatSection,
  messages,
  projectContextSummary,
  handoffs,
  diagnosticsMessages,
}: ChatDrawerBodyProps) {
  switch (activeJarvisChatSection) {
    case "conversation":
      return (
        <div>
          <ChatConversationPane messages={messages} />
          <ChatInputBar />
        </div>
      );

    case "project_context":
      return (
        <section className="inspect-section">
          <h3>{projectContextSummary.title}</h3>

          <div className="inspect-fields">
            <div className="inspect-field">
              <span className="inspect-field-key">Active Scope</span>
              <span className="inspect-field-value">
                {projectContextSummary.activeScope}
              </span>
            </div>

            <div className="inspect-field">
              <span className="inspect-field-key">Owner</span>
              <span className="inspect-field-value">
                {projectContextSummary.owner}
              </span>
            </div>

            <div className="inspect-field">
              <span className="inspect-field-key">Updated</span>
              <span className="inspect-field-value">
                {projectContextSummary.lastUpdatedLabel}
              </span>
            </div>
          </div>

          <div style={{ display: "grid", gap: 8, marginTop: 12 }}>
            {projectContextSummary.summaryLines.map((line, index) => (
              <div
                key={`summary-line-${index}`}
                style={{
                  border: "1px solid rgba(255,255,255,0.08)",
                  background: "rgba(255,255,255,0.04)",
                  borderRadius: 14,
                  padding: 10,
                }}
              >
                {line}
              </div>
            ))}
          </div>
        </section>
      );

    case "command_handoff":
      return (
        <div style={{ display: "grid", gap: 10 }}>
          {handoffs.map((handoff) => (
            <section
              key={handoff.handoffId}
              style={{
                border: "1px solid rgba(255,255,255,0.08)",
                background: "rgba(255,255,255,0.04)",
                borderRadius: 16,
                padding: 12,
              }}
            >
              <div
                style={{
                  display: "flex",
                  gap: 8,
                  flexWrap: "wrap",
                  marginBottom: 8,
                }}
              >
                <span className="inspect-chip">{handoff.guardState}</span>
                <span className="inspect-chip">{handoff.executionState}</span>
                <span className="inspect-chip">
                  {String(handoff.requiresApproval)}
                </span>
              </div>

              <h3 style={{ marginTop: 0, marginBottom: 8 }}>
                {handoff.intentLabel}
              </h3>

              <div className="inspect-fields">
                <div className="inspect-field">
                  <span className="inspect-field-key">Target</span>
                  <span className="inspect-field-value">
                    {handoff.targetSurface}
                  </span>
                </div>
              </div>

              <p style={{ marginBottom: 0 }}>{handoff.explanation}</p>
            </section>
          ))}
        </div>
      );

    case "diagnostics":
      return (
        <div style={{ display: "grid", gap: 10 }}>
          {diagnosticsMessages.map((message) => (
            <section
              key={message.messageId}
              style={{
                border: "1px solid rgba(255,255,255,0.08)",
                background: "rgba(255,255,255,0.04)",
                borderRadius: 16,
                padding: 12,
              }}
            >
              <div
                style={{
                  display: "flex",
                  gap: 8,
                  flexWrap: "wrap",
                  marginBottom: 8,
                }}
              >
                <span className="inspect-chip">{message.kind}</span>
                <span className="inspect-chip">{message.sourceScope}</span>
              </div>

              {message.title ? (
                <h3 style={{ marginTop: 0, marginBottom: 8 }}>
                  {message.title}
                </h3>
              ) : null}

              <p style={{ marginBottom: 0 }}>{message.body}</p>
            </section>
          ))}
        </div>
      );
  }
}
