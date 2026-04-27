import type { DashboardSkeletonSurface } from "../dashboard_skeleton/types.js";
import { DASHBOARD_RENDERER_ADAPTER_REGISTRY } from "./adapterRegistry.js";
import type {
  DashboardRendererAdapterContract,
  DashboardRendererResolution,
  DashboardRendererValidation,
} from "./types.js";

export function getDashboardRendererAdapters(): readonly DashboardRendererAdapterContract[] {
  return DASHBOARD_RENDERER_ADAPTER_REGISTRY;
}

export function getDashboardRendererAdapterById(
  adapterId: string,
): DashboardRendererAdapterContract | null {
  return (
    DASHBOARD_RENDERER_ADAPTER_REGISTRY.find(
      (adapter) => adapter.adapterId === adapterId,
    ) ?? null
  );
}

export function resolveDashboardRendererAdapterForSurface(
  surface: DashboardSkeletonSurface,
): DashboardRendererResolution {
  const adapter = DASHBOARD_RENDERER_ADAPTER_REGISTRY.find(
    (candidate) =>
      candidate.supportedRenderModes.includes(surface.renderMode) &&
      candidate.supportedTargetZones.includes(surface.targetZone),
  );

  if (!adapter) {
    throw new Error(`renderer_adapter_not_found:${surface.surfaceId}`);
  }

  return {
    surface,
    adapter,
    resolved: true,
  };
}

export function validateDashboardRendererAdapterRegistry(): DashboardRendererValidation {
  const errors: string[] = [];
  const seenAdapterIds = new Set<string>();

  for (const adapter of DASHBOARD_RENDERER_ADAPTER_REGISTRY) {
    if (!adapter.adapterId.trim()) {
      errors.push("adapterId_required");
    }

    if (seenAdapterIds.has(adapter.adapterId)) {
      errors.push(`duplicate_adapterId:${adapter.adapterId}`);
    }

    seenAdapterIds.add(adapter.adapterId);

    if (!adapter.title.trim()) {
      errors.push(`adapter_title_required:${adapter.adapterId}`);
    }

    if (adapter.supportedRenderModes.length === 0) {
      errors.push(`supported_render_modes_required:${adapter.adapterId}`);
    }

    if (adapter.supportedTargetZones.length === 0) {
      errors.push(`supported_target_zones_required:${adapter.adapterId}`);
    }

    if (adapter.appTsxHardcodingAllowed) {
      errors.push(`app_tsx_hardcoding_forbidden:${adapter.adapterId}`);
    }

    if (adapter.directEngineBindingAllowed) {
      errors.push(`direct_engine_binding_forbidden:${adapter.adapterId}`);
    }

    if (adapter.bindingPolicy !== "adapter_boundary_only") {
      errors.push(`adapter_boundary_only_required:${adapter.adapterId}`);
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
