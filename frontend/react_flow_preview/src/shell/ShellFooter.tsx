import React from "react";

type ShellFooterProps = {
  isVisible: boolean;
  activeViewTitle: string;
  shellMode: string;
  centerImmutableConfirmed: boolean;
  presenceItems: readonly string[];
};

export function ShellFooter({
  isVisible,
  activeViewTitle,
  shellMode,
  centerImmutableConfirmed,
  presenceItems,
}: ShellFooterProps) {
  if (!isVisible) {
    return null;
  }

  return (
    <footer
      style={{
        borderRadius: 20,
        border: "1px solid rgba(255,255,255,0.08)",
        background: "rgba(10,16,34,0.34)",
        backdropFilter: "blur(14px)",
        boxShadow: "0 14px 36px rgba(0,0,0,0.16)",
        padding: "12px 16px",
        display: "grid",
        gap: 10,
      }}
    >
      <div
        style={{
          display: "flex",
          gap: 10,
          flexWrap: "wrap",
          alignItems: "center",
        }}
      >
        <span
          style={{
            fontSize: 12,
            letterSpacing: "0.16em",
            textTransform: "uppercase",
            opacity: 0.72,
          }}
        >
          System Footer
        </span>

        <span className="inspect-chip">Environment: DEV</span>
        <span className="inspect-chip">Network: Stable</span>
        <span className="inspect-chip">View: {activeViewTitle}</span>
        <span className="inspect-chip">Shell Mode: {shellMode}</span>
        <span className="inspect-chip">
          Center Immutable: {String(centerImmutableConfirmed)}
        </span>
        <span className="inspect-chip">
          Family Presence: {presenceItems.length} online
        </span>
      </div>

      <div
        style={{
          display: "flex",
          gap: 8,
          flexWrap: "wrap",
          alignItems: "center",
        }}
      >
        <button type="button" className="view-switch-button active">
          Family Surface
        </button>

        <button type="button" className="view-switch-button">
          Presence Board
        </button>

        {presenceItems.map((item) => (
          <button
            key={item}
            type="button"
            className="view-switch-button"
          >
            {item}
          </button>
        ))}
      </div>
    </footer>
  );
}
