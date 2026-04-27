import { useCallback } from "react";
import type { Dispatch, SetStateAction } from "react";

import type {
  LeftDrawerSection,
  RightDrawerSection,
} from "../overlayDrawerLayoutContract.js";
import {
  buildInitialOverlayDrawerShellState,
  toggleOverlayDrawerMode,
} from "../overlayDrawerShellState.js";

type DrawerShellState = ReturnType<typeof buildInitialOverlayDrawerShellState>;

type SetDrawerShellState = Dispatch<SetStateAction<DrawerShellState>>;

export type DrawerShellInteractions = {
  toggleLeftDrawer: () => void;
  toggleRightDrawer: () => void;
  toggleTopDrawer: () => void;
  setActiveLeftDrawerSection: (section: LeftDrawerSection) => void;
  setActiveRightDrawerSection: (section: RightDrawerSection) => void;
};

export function useDrawerShellInteractions(
  setDrawerShellState: SetDrawerShellState,
): DrawerShellInteractions {
  const toggleLeftDrawer = useCallback(() => {
    setDrawerShellState((current) => {
      const nextLeftMode = toggleOverlayDrawerMode(current.leftMode);

      return {
        ...current,
        leftMode: nextLeftMode,
        rightMode: nextLeftMode === "expanded" ? "hidden" : current.rightMode,
      };
    });
  }, [setDrawerShellState]);

  const toggleRightDrawer = useCallback(() => {
    setDrawerShellState((current) => {
      const nextRightMode = toggleOverlayDrawerMode(current.rightMode);

      return {
        ...current,
        rightMode: nextRightMode,
        leftMode: nextRightMode === "expanded" ? "hidden" : current.leftMode,
      };
    });
  }, [setDrawerShellState]);

  const toggleTopDrawer = useCallback(() => {
    setDrawerShellState((current) => ({
      ...current,
      topMode: toggleOverlayDrawerMode(current.topMode),
    }));
  }, [setDrawerShellState]);

  const setActiveLeftDrawerSection = useCallback(
    (section: LeftDrawerSection) => {
      setDrawerShellState((current) => ({
        ...current,
        activeLeftSection: section,
      }));
    },
    [setDrawerShellState],
  );

  const setActiveRightDrawerSection = useCallback(
    (section: RightDrawerSection) => {
      setDrawerShellState((current) => ({
        ...current,
        activeRightSection: section,
      }));
    },
    [setDrawerShellState],
  );

  return {
    toggleLeftDrawer,
    toggleRightDrawer,
    toggleTopDrawer,
    setActiveLeftDrawerSection,
    setActiveRightDrawerSection,
  };
}
