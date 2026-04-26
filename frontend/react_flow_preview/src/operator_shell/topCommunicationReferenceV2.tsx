import React from "react";

export type TopCommunicationSidebarMode =
  | "chat"
  | "commands"
  | "code"
  | "memory"
  | "settings";

export type TopCommunicationMessage = {
  messageId: string;
  role: "user" | "jarvis" | "system";
  kind: "text" | "code" | "status";
  title?: string | null;
  body: string;
};

export type TopCommunicationReferenceV2Props = {
  isNarrow: boolean;
  messages: readonly TopCommunicationMessage[];
  codeMessages: readonly TopCommunicationMessage[];
  diagnosticsMessages: readonly TopCommunicationMessage[];
  activeSidebarMode: TopCommunicationSidebarMode;
  onSidebarModeChange: (mode: TopCommunicationSidebarMode) => void;
  chatInput: string;
  onChatInputChange: (value: string) => void;
  onAttachClick?: () => void;
  onVoiceInputClick?: () => void;
  onSendClick?: () => void;
  renderMemoryPanel: () => React.ReactNode;
  renderCommandsPanel: () => React.ReactNode;
};

function getSidebarModeTitle(mode: TopCommunicationSidebarMode): string {
  switch (mode) {
    case "chat":
      return "Чаты";
    case "commands":
      return "Команды";
    case "code":
      return "Код";
    case "memory":
      return "Память";
    case "settings":
      return "Настройки";
  }
}

function filterConversationMessages(
  messages: readonly TopCommunicationMessage[],
): readonly TopCommunicationMessage[] {
  return messages.filter(
    (message) =>
      message.role === "user" ||
      message.role === "jarvis" ||
      (message.role === "system" && message.kind === "code"),
  );
}

function renderMessageBubble(
  message: TopCommunicationMessage,
  isNarrow: boolean,
): React.ReactNode {
  const isUser = message.role === "user";
  const isCode = message.kind === "code";

  return (
    <section
      key={message.messageId}
      style={{
        border: "1px solid rgba(255,255,255,0.08)",
        background: isUser
          ? "rgba(52, 110, 255, 0.18)"
          : "rgba(17, 22, 34, 0.92)",
        borderRadius: 18,
        padding: isNarrow ? 12 : 14,
        boxShadow: isUser
          ? "0 10px 24px rgba(40, 90, 220, 0.12)"
          : "0 10px 24px rgba(0,0,0,0.18)",
      }}
    >
      {message.title ? (
        <h3
          style={{
            margin: 0,
            marginBottom: 8,
            fontSize: 15,
            lineHeight: 1.25,
            color: "#f8fbff",
          }}
        >
          {message.title}
        </h3>
      ) : null}

      {isCode ? (
        <pre
          style={{
            margin: 0,
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
            fontSize: 13,
            lineHeight: 1.55,
            color: "#dff4ff",
            fontFamily:
              'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
          }}
        >
          {message.body}
        </pre>
      ) : (
        <p
          style={{
            margin: 0,
            color: "#eef6ff",
            lineHeight: 1.65,
            fontSize: 14,
          }}
        >
          {message.body}
        </p>
      )}
    </section>
  );
}

function renderCommunicationSidebarBody(
  mode: TopCommunicationSidebarMode,
  codeMessages: readonly TopCommunicationMessage[],
  diagnosticsMessages: readonly TopCommunicationMessage[],
  renderMemoryPanel: () => React.ReactNode,
  renderCommandsPanel: () => React.ReactNode,
): React.ReactNode {
  switch (mode) {
    case "chat":
      return (
        <div style={{ display: "grid", gap: 10 }}>
          <section className="inspect-section">
            <h3>Чаты</h3>
            <div className="inspect-fields">
              <div className="inspect-field">
                <span className="inspect-field-key">Primary Session</span>
                <span className="inspect-field-value">JARVIS Communication</span>
              </div>
              <div className="inspect-field">
                <span className="inspect-field-key">Mode</span>
                <span className="inspect-field-value">Operator Messaging</span>
              </div>
            </div>
          </section>

          {diagnosticsMessages.length ? (
            <section className="inspect-section">
              <h3>Diagnostics</h3>
              <div style={{ display: "grid", gap: 10 }}>
                {diagnosticsMessages.map((message) => (
                  <div
                    key={message.messageId}
                    style={{
                      border: "1px solid rgba(255,255,255,0.07)",
                      background: "rgba(255,255,255,0.03)",
                      borderRadius: 14,
                      padding: 12,
                    }}
                  >
                    {message.title ? (
                      <div
                        style={{
                          marginBottom: 8,
                          fontWeight: 600,
                          color: "#f3f8ff",
                        }}
                      >
                        {message.title}
                      </div>
                    ) : null}
                    <div style={{ color: "#cdd8e6", lineHeight: 1.5 }}>
                      {message.body}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          ) : null}
        </div>
      );

    case "commands":
      return <>{renderCommandsPanel()}</>;

    case "code":
      return (
        <div style={{ display: "grid", gap: 10 }}>
          <section className="inspect-section">
            <h3>Кодовые блоки</h3>
            <div className="inspect-fields">
              <div className="inspect-field">
                <span className="inspect-field-key">Count</span>
                <span className="inspect-field-value">
                  {String(codeMessages.length)}
                </span>
              </div>
            </div>
          </section>

          {codeMessages.map((message) => (
            <section
              key={message.messageId}
              style={{
                border: "1px solid rgba(255,255,255,0.07)",
                background: "rgba(255,255,255,0.03)",
                borderRadius: 14,
                padding: 12,
              }}
            >
              {message.title ? (
                <h3 style={{ marginTop: 0, marginBottom: 8 }}>{message.title}</h3>
              ) : null}
              <pre
                style={{
                  margin: 0,
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word",
                  fontSize: 13,
                  color: "#dff4ff",
                  lineHeight: 1.5,
                }}
              >
                {message.body}
              </pre>
            </section>
          ))}
        </div>
      );

    case "memory":
      return <>{renderMemoryPanel()}</>;

    case "settings":
      return (
        <section className="inspect-section">
          <h3>Настройки</h3>
          <div className="inspect-fields">
            <div className="inspect-field">
              <span className="inspect-field-key">Center Policy</span>
              <span className="inspect-field-value">Immutable</span>
            </div>
            <div className="inspect-field">
              <span className="inspect-field-key">Overlay Mode</span>
              <span className="inspect-field-value">Top Drawer</span>
            </div>
            <div className="inspect-field">
              <span className="inspect-field-key">Sidebar Model</span>
              <span className="inspect-field-value">Right Context Column</span>
            </div>
          </div>
        </section>
      );
  }
}

export default function TopCommunicationReferenceV2(
  props: TopCommunicationReferenceV2Props,
): React.ReactNode {
  const {
    isNarrow,
    messages,
    codeMessages,
    diagnosticsMessages,
    activeSidebarMode,
    onSidebarModeChange,
    chatInput,
    onChatInputChange,
    onAttachClick,
    onVoiceInputClick,
    onSendClick,
    renderMemoryPanel,
    renderCommandsPanel,
  } = props;

  const conversationMessages = filterConversationMessages(messages);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: isNarrow ? "1fr" : "minmax(0, 1fr) 340px",
        gap: isNarrow ? 12 : 16,
        height: "100%",
        minHeight: 0,
      }}
    >
      <div
        style={{
          display: "grid",
          gridTemplateRows: "1fr auto",
          gap: 12,
          minHeight: 0,
        }}
      >
        <div
          style={{
            minHeight: 0,
            overflow: "auto",
            paddingRight: 4,
            borderTop: "1px solid rgba(255,255,255,0.06)",
            paddingTop: 10,
          }}
        >
          <div style={{ display: "grid", gap: 12 }}>
            {conversationMessages.map((message) =>
              renderMessageBubble(message, isNarrow),
            )}
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: isNarrow
              ? "40px 1fr 40px 44px"
              : "44px 1fr 44px 48px",
            gap: 8,
            alignItems: "center",
            borderTop: "1px solid rgba(255,255,255,0.08)",
            paddingTop: 10,
          }}
        >
          <button
            type="button"
            className="view-switch-button"
            onClick={onAttachClick}
            aria-label="attach file"
          >
            ＋
          </button>

          <input
            value={chatInput}
            onChange={(event) => onChatInputChange(event.target.value)}
            placeholder="Введите сообщение..."
            style={{
              width: "100%",
              minWidth: 0,
              height: 50,
              borderRadius: 16,
              border: "1px solid rgba(255,255,255,0.10)",
              background: "rgba(255,255,255,0.045)",
              color: "white",
              padding: "0 14px",
              outline: "none",
              fontSize: 14,
              boxShadow: "inset 0 1px 0 rgba(255,255,255,0.03)",
            }}
          />

          <button
            type="button"
            className="view-switch-button"
            onClick={onVoiceInputClick}
            aria-label="voice input"
          >
            🎤
          </button>

          <button
            type="button"
            className="view-switch-button active"
            onClick={onSendClick}
            aria-label="send"
          >
            ➤
          </button>
        </div>
      </div>

      <aside
        style={{
          display: "grid",
          gridTemplateRows: "auto minmax(0, 1fr)",
          gap: 12,
          minHeight: 0,
          minWidth: 0,
          width: "100%",
          maxWidth: isNarrow ? "100%" : 340,
          justifySelf: isNarrow ? "stretch" : "end",
          borderLeft: isNarrow ? "none" : "1px solid rgba(255,255,255,0.08)",
          paddingLeft: isNarrow ? 0 : 12,
        }}
      >
        <section
          className="inspect-section"
          style={{
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.07)",
            borderRadius: 18,
            padding: isNarrow ? 10 : 12,
            boxShadow: "0 14px 30px rgba(0,0,0,0.12)",
          }}
        >
          <h3 style={{ marginBottom: 10 }}>Коммуникация</h3>

          <div
            style={{
              display: "grid",
              gap: 8,
            }}
          >
            {(
              [
                "chat",
                "commands",
                "code",
                "memory",
                "settings",
              ] as const
            ).map((mode) => (
              <button
                key={mode}
                className={
                  activeSidebarMode === mode
                    ? "view-switch-button active"
                    : "view-switch-button"
                }
                type="button"
                onClick={() => onSidebarModeChange(mode)}
              >
                {getSidebarModeTitle(mode)}
              </button>
            ))}
          </div>
        </section>

        <section
          className="inspect-section"
          style={{
            minHeight: 0,
            overflow: "auto",
            background: "rgba(255,255,255,0.025)",
            border: "1px solid rgba(255,255,255,0.06)",
            borderRadius: 18,
            padding: isNarrow ? 10 : 12,
            boxShadow: "0 14px 30px rgba(0,0,0,0.12)",
          }}
        >
          <h3 style={{ marginTop: 0, marginBottom: 10 }}>Контекст</h3>
          {renderCommunicationSidebarBody(
            activeSidebarMode,
            codeMessages,
            diagnosticsMessages,
            renderMemoryPanel,
            renderCommandsPanel,
          )}
        </section>
      </aside>
    </div>
  );
}
