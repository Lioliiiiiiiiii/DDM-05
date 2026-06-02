# Digital Disruption Matrix 2026

A static, multi-page website assembled from the standalone HTML components of the
*Digital Disruption Matrix 2026* (ESSEC Business School), adapted to a single
coherent **dark design system** (see `design-system/DESIGN_SYSTEM.md`).

No build step is required to view the site — it is plain HTML/CSS/JS and can be
served by any static host (e.g. GitHub Pages). `index.html` is the entry point.

## Structure

```
index.html                     Homepage (hero, partner data panel)
explore/
  technology.html              Animated technology selector → /technology/<slug>
  industry.html                Animated industry selector  → /industry/<slug>
  tech-x-industry.html         Heat-analysis radar + combination picker → intersection sections
technology/<slug>.html   (×5)  Title · description · Professionals' Perception · Unicorn Factor · Research & Innovation
industry/<slug>.html     (×10) Title · description · Professionals' Perception · Unicorn Factor
data/
  professionals-perception.html  Full perception survey dashboard
  unicorn-factor.html            Full unicorn / startup landscape dashboard
  research-innovation.html       Full research & innovation dashboard
more/                          About · Methodology · FAQ · Contact · Acknowledgment (placeholders)
key-findings.html              Placeholder
heatmatrix.html                Placeholder
download.html                  Placeholder
assets/                        Shared shell CSS/JS + logos
embed/                         Re-themed, parameter-aware dashboards (loaded via iframes)
_src/                          Original source components + build.py (provenance / rebuild)
design-system/                 Design system spec + tokens (source of truth)
```

## How it is assembled

* **Shared shell.** Every interior page wraps its content in one dark
  design-system shell (sidebar + topbar) from `assets/css/shell.css`.
* **Embeds.** The heavy interactive dashboards are loaded as same-origin
  `<iframe>`s (auto-resized by `assets/js/shell.js`) so their styles never
  collide. They are re-themed to the dark system **without altering the data**:
  each is wrapped and given an appended `:root` override + Montserrat/IBM Plex
  fonts.
* **Real data only.** Per-technology / per-industry / intersection sections are
  *slices* of the real source dashboards (the perception "foresight matrix" cards
  carry `data-type` / `data-tech` / `data-indus` attributes; the unicorn explorer
  is pre-filtered via its own controls). No figures were invented.

## Rebuilding

The generator reads the originals in `_src/` and writes the pages:

```bash
python3 _src/build.py
```

## Placeholders

The **More** pages, **Key findings**, **Heatmatrix** and **Download the report**
are intentional placeholders pending content.
