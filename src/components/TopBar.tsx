import { NavLink } from "react-router-dom";
import { Lightbulb, Download } from "lucide-react";
import { HeatmapIcon } from "./HeatmapIcon";
import { actionButtons, type ActionButton } from "../navigation";

/** Visual style per action accent. */
const buttonStyles: Record<
  ActionButton["accent"],
  { base: string; active: string }
> = {
  findings: {
    base: "border-[var(--color-findings)]/40 text-[var(--color-findings)] hover:bg-[var(--color-findings)]/15",
    active: "bg-[var(--color-findings)]/20 ring-1 ring-[var(--color-findings)]/60",
  },
  heat: {
    base: "border-[var(--color-heat)]/40 text-[var(--color-heat)] hover:bg-[var(--color-heat)]/15",
    active: "bg-[var(--color-heat)]/20 ring-1 ring-[var(--color-heat)]/60",
  },
  download: {
    base: "border-white/70 text-white hover:bg-white/10",
    active: "bg-white/15 ring-1 ring-white/70",
  },
};

function ActionIcon({ accent }: { accent: ActionButton["accent"] }) {
  const cls = "h-4 w-4 shrink-0";
  if (accent === "findings") return <Lightbulb className={cls} />;
  if (accent === "heat") return <HeatmapIcon className={cls} />;
  return <Download className={cls} />;
}

export function TopBar() {
  return (
    <header className="flex h-16 shrink-0 items-center justify-end gap-3 border-b border-base-800 bg-base-900/70 px-6 backdrop-blur">
      {actionButtons.map((btn) => {
        const styles = buttonStyles[btn.accent];
        return (
          <NavLink
            key={btn.path}
            to={btn.path}
            className={({ isActive }) =>
              [
                "inline-flex items-center gap-2 rounded-lg border px-3.5 py-2 text-sm font-semibold transition-colors",
                styles.base,
                isActive ? styles.active : "",
              ].join(" ")
            }
          >
            <ActionIcon accent={btn.accent} />
            <span className="whitespace-nowrap">{btn.label}</span>
          </NavLink>
        );
      })}
    </header>
  );
}
