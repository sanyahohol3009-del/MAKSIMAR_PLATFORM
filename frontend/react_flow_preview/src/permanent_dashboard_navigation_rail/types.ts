import type {
  DashboardSkeletonButtonGroup,
  DashboardSkeletonDomain,
  DashboardSkeletonRenderMode,
  DashboardSkeletonSurfaceStatus,
} from "../dashboardSkeletonSurfaceTaxonomy.js";
import type {
  DashboardRendererAdapterKind,
} from "../dashboardRendererAdapterBoundary.js";
import type {
  LeftDrawerSkeletonNavigationBadge,
} from "../leftDrawerSkeletonNavigationExposure.js";
import type {
  PermanentDashboardNavigationRailVisualDensity,
  PermanentDashboardNavigationRailVisualItemKind,
} from "../permanentDashboardNavigationRailVisualWiring.js";

export type PermanentDashboardNavigationRailShellTarget =
  "permanent_dashboard_navigation_rail_shell_component";

export type PermanentDashboardNavigationRailShellSource =
  "permanent_dashboard_navigation_rail_visual_wiring";

export type PermanentDashboardNavigationRailShellPlacement =
  "left_permanent_rail";

export type PermanentDashboardNavigationRailShellRole =
  "dashboard_navigation";

export type PermanentDashboardNavigationRailShellItem = {
  railItemId: string;
  navigationId: string;
  surfaceId: string;
  title: string;
  buttonGroup: DashboardSkeletonButtonGroup;
  domain: DashboardSkeletonDomain;
  renderMode: DashboardSkeletonRenderMode;
  status: DashboardSkeletonSurfaceStatus;
  rendererAdapterKind: DashboardRendererAdapterKind;
  rendererAdapterId: string;
  visualKind: PermanentDashboardNavigationRailVisualItemKind;
  selected: boolean;
  disabled: boolean;
  requiresApproval: boolean;
  adapterBoundaryRequired: boolean;
  badges: readonly LeftDrawerSkeletonNavigationBadge[];
};

export type PermanentDashboardNavigationRailShellSection = {
  buttonGroup: DashboardSkeletonButtonGroup;
  title: string;
  items: readonly PermanentDashboardNavigationRailShellItem[];
};

export type PermanentDashboardNavigationRailShellReadModel = {
  target: PermanentDashboardNavigationRailShellTarget;
  source: PermanentDashboardNavigationRailShellSource;
  placement: PermanentDashboardNavigationRailShellPlacement;
  role: PermanentDashboardNavigationRailShellRole;
  density: PermanentDashboardNavigationRailVisualDensity;
  activeSurfaceId: string;
  sections: readonly PermanentDashboardNavigationRailShellSection[];
  totalSections: number;
  totalItems: number;
  selectedItems: number;
  memoryItems: number;
  mobileItems: number;
  adapterBoundaryItems: number;
  threeDItems: number;
  simulationItems: number;
  persistent: true;
  overlay: false;
  centerViewportOverlapAllowed: false;
  drawerSemanticsAllowedForMainDashboardList: false;
  appTsxHardcodingAllowed: false;
};

export type PermanentDashboardNavigationRailShellValidation = {
  valid: boolean;
  errors: readonly string[];
};

export type PermanentDashboardNavigationRailShellProps = {
  readModel?: PermanentDashboardNavigationRailShellReadModel;
  activeSurfaceId?: string;
  density?: PermanentDashboardNavigationRailVisualDensity;
  className?: string;
  onSelectSurface?: (surfaceId: string) => void;
};
