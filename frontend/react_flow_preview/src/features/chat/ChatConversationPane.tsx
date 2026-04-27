import React from "react";

export type ChatConversationMessage = {
  messageId: string;
  role: string;
  kind: string;
  sourceScope: string;
  traceId?: string | null;
  title?: string | null;
  body: string;
};

type ChatConversationPaneProps = {
  messages: readonly ChatConversationMessage[];
};

export function ChatConversationPane({
  messages,
}: ChatConversationPaneProps) {
  return (
    <div style={{ display: "grid", gap: 10 }}>
      {messages.map((message) => (
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
            <span className="inspect-chip">{message.role}</span>
            <span className="inspect-chip">{message.kind}</span>
            <span className="inspect-chip">{message.sourceScope}</span>
            {message.traceId ? (
              <span className="inspect-chip">{message.traceId}</span>
            ) : null}
          </div>

          {message.title ? (
            <h3 style={{ marginTop: 0, marginBottom: 8 }}>
              {message.title}
            </h3>
          ) : null}

          {message.kind === "code" ? (
            <pre
              style={{
                margin: 0,
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
                fontSize: 13,
              }}
            >
              {message.body}
            </pre>
          ) : (
            <p style={{ margin: 0 }}>{message.body}</p>
          )}
        </section>
      ))}
    </div>
  );
}
