# Digital Disruption Matrix — Edition 2026

The website skeleton for the **Digital Disruption Matrix**. This is the
structural scaffold only — pages are intentionally left empty and will be
populated later.

## Stack

- [Vite](https://vite.dev/) + [React](https://react.dev/) + TypeScript
- [React Router](https://reactrouter.com/) for client-side routing
- [Tailwind CSS v4](https://tailwindcss.com/) for styling
- [lucide-react](https://lucide.dev/) icons

## Layout

A persistent app shell (`src/components/Layout.tsx`) renders on every page:

- **Left sidebar** (`Sidebar.tsx`) — brand title plus three nav groups, each
  with its own accent color:
  - _Explore by Sector_ (cyan): Technology · Industry · Technology x Industry
  - _Explore by Data_ (violet): Professionals' Perception · Unicorn Factor ·
    Research & Innovation
  - _More_ (muted grey): About Us · Methodology · FAQ · Contact
- **Top bar** (`TopBar.tsx`) — three always-visible action buttons:
  - **Key Findings** (amber, lightbulb icon)
  - **HeatMatrix** (rose, mini-heatmap icon)
  - **Download the Report** (emerald, download arrow icon)

All navigation is driven from a single source of truth in `src/navigation.ts`,
so adding or renaming a page only requires editing that file.

## Develop

```bash
npm install
npm run dev      # start the dev server
npm run build    # type-check + production build
npm run preview  # preview the production build
```
