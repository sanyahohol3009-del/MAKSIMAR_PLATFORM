import React from "react";

type DrawerHandleProps = {
  isVisible: boolean;
  side: "left" | "right";
  label: string;
  backdropBlurPx: number;
  onToggle: () => void;
};

function SingleDrawerHandle({
  isVisible,
  side,
  label,
  backdropBlurPx,
  onToggle,
}: DrawerHandleProps) {
  if (!isVisible) {
    return null;
  }

  return (
    <button
      type="button"
      onClick={onToggle}
      style={{
        position: "absolute",
        top: "50%",
        [side]: 10,
        transform: "translateY(-50%)",
        zIndex: 40,
        writingMode: "vertical-rl",
        textOrientation: "mixed",
        padding: "12px 8px",
        borderRadius: 999,
        border: "1px solid rgba(255,255,255,0.12)",
        background: "rgba(10,16,34,0.32)",
        backdropFilter: `blur(${backdropBlurPx}px)`,
        color: "white",
        cursor: "pointer",
      }}
    >
      {label}
    </button>
  );
}

type DrawerHandlesProps = {
  showLeftHandle: boolean;
  showRightHandle: boolean;
  leftLabel: string;
  rightLabel: string;
  leftBackdropBlurPx: number;
  rightBackdropBlurPx: number;
  onToggleLeft: () => void;
  onToggleRight: () => void;
};

export function DrawerHandles({
  showLeftHandle,
  showRightHandle,
  leftLabel,
  rightLabel,
  leftBackdropBlurPx,
  rightBackdropBlurPx,
  onToggleLeft,
  onToggleRight,
}: DrawerHandlesProps) {
  return (
    <>
      <SingleDrawerHandle
        isVisible={showLeftHandle}
        side="left"
        label={leftLabel}
        backdropBlurPx={leftBackdropBlurPx}
        onToggle={onToggleLeft}
      />
      <SingleDrawerHandle
        isVisible={showRightHandle}
        side="right"
        label={rightLabel}
        backdropBlurPx={rightBackdropBlurPx}
        onToggle={onToggleRight}
      />
    </>
  );
}
