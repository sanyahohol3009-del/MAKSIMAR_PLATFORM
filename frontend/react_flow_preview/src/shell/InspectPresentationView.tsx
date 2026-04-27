import React from "react";

export type InspectPresentationViewModel = {
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

type InspectPresentationViewProps = {
  presentation: InspectPresentationViewModel;
};

export function InspectPresentationView({
  presentation,
}: InspectPresentationViewProps) {
  return (
    <>
      <div
        style={{
          display: "flex",
          gap: 8,
          flexWrap: "wrap",
          marginBottom: 12,
        }}
      >
        <span className="inspect-chip">{presentation.semanticKind}</span>
      </div>

      <div className="inspect-explanation">
        <h3>{presentation.title}</h3>
        <p>{presentation.explanation}</p>
      </div>

      <div className="inspect-sections">
        {presentation.sections.map((section) => (
          <section key={section.title} className="inspect-section">
            <h3>{section.title}</h3>
            <div className="inspect-fields">
              {section.items.map((item) => (
                <div
                  key={`${section.title}:${item.key}`}
                  className="inspect-field"
                >
                  <span className="inspect-field-key">{item.key}</span>
                  <span className="inspect-field-value">{item.value}</span>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </>
  );
}
