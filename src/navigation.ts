/**
 * Central navigation model for the Digital Disruption Matrix.
 *
 * The sidebar, router and placeholder pages are all generated from this single
 * source of truth so that adding or renaming a page only happens in one place.
 */

export type NavItem = {
  /** URL path (without leading slash collisions — used directly as route). */
  path: string;
  /** Label shown in the sidebar / page heading. */
  label: string;
};

export type NavSection = {
  /** Section heading shown above the group of links. */
  title: string;
  /**
   * Accent key controlling the section's color.
   * Maps to the `--color-*` tokens defined in index.css.
   */
  accent: "sector" | "data" | "more";
  items: NavItem[];
};

export const navSections: NavSection[] = [
  {
    title: "Explore by Sector",
    accent: "sector",
    items: [
      { path: "/technology", label: "Technology" },
      { path: "/industry", label: "Industry" },
      { path: "/technology-x-industry", label: "Technology x Industry" },
    ],
  },
  {
    title: "Explore by Data",
    accent: "data",
    items: [
      { path: "/professionals-perception", label: "Professionals' Perception" },
      { path: "/unicorn-factor", label: "Unicorn Factor" },
      { path: "/research-innovation", label: "Research & Innovation" },
    ],
  },
  {
    title: "More",
    accent: "more",
    items: [
      { path: "/about", label: "About Us" },
      { path: "/methodology", label: "Methodology" },
      { path: "/faq", label: "FAQ" },
      { path: "/contact", label: "Contact" },
    ],
  },
];

/** Top-right action buttons, present on every page. */
export type ActionButton = {
  path: string;
  label: string;
  /** Accent key mapping to `--color-*` tokens. */
  accent: "findings" | "heat" | "download";
};

export const actionButtons: ActionButton[] = [
  { path: "/key-findings", label: "Key Findings", accent: "findings" },
  { path: "/heatmatrix", label: "HeatMatrix", accent: "heat" },
  { path: "/download-report", label: "Download the Report", accent: "download" },
];

/** Flat list of every routed page, used to build the router. */
export const allRoutes: NavItem[] = [
  ...navSections.flatMap((s) => s.items),
  ...actionButtons.map((b) => ({ path: b.path, label: b.label })),
];
