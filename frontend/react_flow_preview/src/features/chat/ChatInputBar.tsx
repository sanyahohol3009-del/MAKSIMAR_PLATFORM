import React from "react";

type ChatInputBarProps = {
  placeholder?: string;
};

export function ChatInputBar({
  placeholder = "Message JARVIS...",
}: ChatInputBarProps) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "auto 1fr auto auto",
        gap: 10,
        alignItems: "center",
        marginTop: 12,
        padding: 10,
        border: "1px solid rgba(255,255,255,0.08)",
        borderRadius: 16,
        background: "rgba(255,255,255,0.04)",
        backdropFilter: "blur(10px)",
      }}
    >
      <button
        type="button"
        className="view-switch-button"
        style={{ minWidth: 44 }}
      >
        +
      </button>

      <input
        type="text"
        placeholder={placeholder}
        style={{
          width: "100%",
          minWidth: 0,
          border: "1px solid rgba(255,255,255,0.08)",
          borderRadius: 12,
          background: "rgba(8,12,24,0.6)",
          color: "white",
          padding: "10px 12px",
          outline: "none",
        }}
      />

      <button
        type="button"
        className="view-switch-button"
        style={{ minWidth: 44 }}
      >
        🎤
      </button>

      <button
        type="button"
        className="view-switch-button active"
        style={{ minWidth: 64 }}
      >
        Send
      </button>
    </div>
  );
}
