import React from "react";

import type { JarvisChatDrawerSectionId } from "../../jarvis_chat/jarvisChatDrawerContract.js";
import type { EmbeddedChatSurfaceId } from "../../jarvis_chat/embeddedChatSurfaceRegistry.js";

type ChatSidebarProps = {
  activeJarvisChatSection: JarvisChatDrawerSectionId;
  activeEmbeddedChatSurfaceLabel: string;
  jarvisChatSections: readonly JarvisChatDrawerSectionId[];
  onJarvisChatSectionChange: (section: JarvisChatDrawerSectionId) => void;
  getJarvisChatSectionTitle: (
    section: JarvisChatDrawerSectionId,
  ) => string;
  unreadCount: number;
  codeBlockCount: number;
  handoffCount: number;
  diagnosticCount: number;
};

export function ChatSidebar({
  activeJarvisChatSection,
  activeEmbeddedChatSurfaceLabel,
  jarvisChatSections,
  onJarvisChatSectionChange,
  getJarvisChatSectionTitle,
  unreadCount,
  codeBlockCount,
  handoffCount,
  diagnosticCount,
}: ChatSidebarProps) {
  return (
    <div
      style={{
        display: "grid",
        gap: 12,
      }}
    >
      <section
        style={{
          border: "1px solid rgba(255,255,255,0.08)",
          background: "rgba(255,255,255,0.04)",
          borderRadius: 16,
          padding: 12,
        }}
      >
        <div
          style={{
            fontSize: 12,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            opacity: 0.72,
            marginBottom: 10,
          }}
        >
          Communication Sidebar
        </div>

        <div
          style={{
            display: "grid",
            gap: 8,
          }}
        >
          {jarvisChatSections.map((section) => (
            <button
              key={section}
              type="button"
              className={
                activeJarvisChatSection === section
                  ? "view-switch-button active"
                  : "view-switch-button"
              }
              onClick={() => onJarvisChatSectionChange(section)}
              style={{
                width: "100%",
                justifyContent: "flex-start",
              }}
            >
              {getJarvisChatSectionTitle(section)}
            </button>
          ))}
        </div>
      </section>

      <section
        style={{
          border: "1px solid rgba(255,255,255,0.08)",
          background: "rgba(255,255,255,0.04)",
          borderRadius: 16,
          padding: 12,
          display: "grid",
          gap: 10,
        }}
      >
        <div
          style={{
            fontSize: 12,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            opacity: 0.72,
          }}
        >
          Session State
        </div>

        <div className="inspect-fields">
          <div className="inspect-field">
            <span className="inspect-field-key">Active Surface</span>
            <span className="inspect-field-value">
              {activeEmbeddedChatSurfaceLabel}
            </span>
          </div>

          <div className="inspect-field">
            <span className="inspect-field-key">Unread</span>
            <span className="inspect-field-value">{unreadCount}</span>
          </div>

          <div className="inspect-field">
            <span className="inspect-field-key">Code Blocks</span>
            <span className="inspect-field-value">{codeBlockCount}</span>
          </div>

          <div className="inspect-field">
            <span className="inspect-field-key">Handoffs</span>
            <span className="inspect-field-value">{handoffCount}</span>
          </div>

          <div className="inspect-field">
            <span className="inspect-field-key">Diagnostics</span>
            <span className="inspect-field-value">{diagnosticCount}</span>
          </div>
        </div>
      </section>
    </div>
  );
}
