import { NavLink } from "react-router-dom";
import { navSections, type NavSection } from "../navigation";

/** Per-accent class bundles. Kept explicit so Tailwind keeps the classes. */
const accentStyles: Record<
  NavSection["accent"],
  { heading: string; dot: string; activeText: string; activeBg: string; bar: string }
> = {
  sector: {
    heading: "text-[var(--color-sector)]",
    dot: "bg-[var(--color-sector)]",
    activeText: "text-[var(--color-sector)]",
    activeBg: "bg-[var(--color-sector-soft)]/60",
    bar: "bg-[var(--color-sector)]",
  },
  data: {
    heading: "text-[var(--color-data)]",
    dot: "bg-[var(--color-data)]",
    activeText: "text-[var(--color-data)]",
    activeBg: "bg-[var(--color-data-soft)]/60",
    bar: "bg-[var(--color-data)]",
  },
  more: {
    heading: "text-[var(--color-more)]",
    dot: "bg-[var(--color-more)]",
    activeText: "text-slate-100",
    activeBg: "bg-base-800",
    bar: "bg-[var(--color-more)]",
  },
};

export function Sidebar() {
  return (
    <aside className="flex h-full w-72 shrink-0 flex-col border-r border-base-800 bg-base-900">
      {/* Brand */}
      <NavLink to="/" className="block px-6 py-6">
        <span className="block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
          Digital Disruption Matrix
        </span>
        <span className="mt-1 block text-lg font-bold leading-tight text-slate-100">
          Edition 2026
        </span>
      </NavLink>

      <div className="mx-6 h-px bg-base-800" />

      {/* Sections */}
      <nav className="flex-1 overflow-y-auto px-3 py-5">
        {navSections.map((section) => {
          const styles = accentStyles[section.accent];
          return (
            <div key={section.title} className="mb-7">
              <h2
                className={`px-3 pb-2 text-[0.7rem] font-semibold uppercase tracking-wider ${styles.heading}`}
              >
                {section.title}
              </h2>
              <ul className="space-y-0.5">
                {section.items.map((item) => (
                  <li key={item.path}>
                    <NavLink
                      to={item.path}
                      className={({ isActive }) =>
                        [
                          "group relative flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                          isActive
                            ? `${styles.activeBg} ${styles.activeText} font-medium`
                            : "text-slate-400 hover:bg-base-850 hover:text-slate-200",
                        ].join(" ")
                      }
                    >
                      {({ isActive }) => (
                        <>
                          <span
                            className={[
                              "h-1.5 w-1.5 shrink-0 rounded-full transition-opacity",
                              styles.dot,
                              isActive ? "opacity-100" : "opacity-40 group-hover:opacity-70",
                            ].join(" ")}
                          />
                          <span className="truncate">{item.label}</span>
                          {isActive && (
                            <span
                              className={`absolute left-0 top-1/2 h-5 w-1 -translate-y-1/2 rounded-r ${styles.bar}`}
                            />
                          )}
                        </>
                      )}
                    </NavLink>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </nav>

      <div className="px-6 py-4 text-[0.7rem] text-slate-600">
        © 2026 Digital Disruption Matrix
      </div>
    </aside>
  );
}
