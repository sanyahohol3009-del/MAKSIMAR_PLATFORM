import {
  buildEmbeddedChatShellExposureReadModel,
  type EmbeddedChatShellExposureRow,
} from "./embeddedChatShellExposureReadModel.js";
import type { EmbeddedChatSurfaceId } from "./embeddedChatSurfaceRegistry.js";

export type EmbeddedChatShellExposureInspectPresentation = {
  title: string;
  subtitle: string;
  semanticKind: string;
  explanation: string;
  sections: readonly {
    title: string;
    items: readonly {
      key: string;
      value: string;
    }[];
  }[];
};

function findRowsForSurface(
  surfaceId: EmbeddedChatSurfaceId,
): readonly EmbeddedChatShellExposureRow[] {
  const readModel = buildEmbeddedChatShellExposureReadModel();

  return readModel.groupedExposure.flatMap((group) =>
    group.rows.filter((row) => row.surfaceId === surfaceId),
  );
}

export function buildEmbeddedChatShellExposureInspectPresentation(
  surfaceId: EmbeddedChatSurfaceId,
): EmbeddedChatShellExposureInspectPresentation {
  const rows = findRowsForSurface(surfaceId);
  const primaryRow = rows.find((row) => row.exposureMode === "primary") ?? rows[0];
  const referenceRows = rows.filter((row) => row.exposureMode === "reference_only");

  return {
    title: primaryRow?.title ?? surfaceId,
    subtitle: primaryRow?.targetSection ?? "unknown",
    semanticKind: "embedded_chat_shell_exposure",
    explanation:
      "This presentation shows how an embedded chat surface is exposed in the shell as one primary host plus bounded reference-only duplicates where needed.",
    sections: [
      {
        title: "Primary Exposure",
        items: primaryRow
          ? [
              { key: "Surface Id", value: primaryRow.surfaceId },
              { key: "Target", value: primaryRow.target },
              { key: "Target Section", value: primaryRow.targetSection },
              { key: "Exposure Mode", value: primaryRow.exposureMode },
              { key: "Binding Status", value: primaryRow.bindingStatus },
            ]
          : [],
      },
      {
        title: "Reference Exposure",
        items:
          referenceRows.length > 0
            ? referenceRows.map((row) => ({
                key: row.target,
                value: `${row.targetSection} / ${row.exposureMode}`,
              }))
            : [{ key: "Reference", value: "none" }],
      },
      {
        title: "Surface Payload",
        items: primaryRow
          ? [
              { key: "Count Label", value: primaryRow.countLabel },
              { key: "Count Value", value: String(primaryRow.countValue) },
              { key: "Copyable", value: String(primaryRow.copyable) },
            ]
          : [],
      },
    ],
  };
}
