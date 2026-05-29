/**
 * A tiny 3x3 "heatmap" glyph used for the HeatMatrix action button.
 * Drawn inline so the cells can pick up a warm gradient regardless of theme.
 */
export function HeatmapIcon({ className }: { className?: string }) {
  const cells = [
    0.35, 0.6, 0.85,
    0.55, 0.9, 0.5,
    0.8, 0.45, 0.7,
  ];
  return (
    <svg
      viewBox="0 0 24 24"
      className={className}
      aria-hidden="true"
      fill="none"
    >
      {cells.map((intensity, i) => {
        const col = i % 3;
        const row = Math.floor(i / 3);
        return (
          <rect
            key={i}
            x={2 + col * 7}
            y={2 + row * 7}
            width={6}
            height={6}
            rx={1.4}
            fill="currentColor"
            opacity={intensity}
          />
        );
      })}
    </svg>
  );
}
