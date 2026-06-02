# Research & Innovation — Design System

**Version 1.1.0 · Dark theme · For human and agent use**

This document is the source of truth for the visual language of the *Research & Innovation* technology-intelligence dashboards. It is written so an implementing agent can build new screens that match the existing cards without seeing them. Machine-readable tokens live in `design-tokens.json`; a rendered reference lives in `design-system-preview.html`.

> **Changes in 1.1.0:** added the official **SVG line-icon set** — 5 technology icons + 10 industry icons (§6). 
> **1.0.0:** display typeface changed to **Montserrat**; the brand ampersand is **upright** (`font-style: normal`), not italic.

---

## 1. Principles

1. **Dark, quiet, data-first.** A near-black canvas, low-contrast hairlines, and restrained colour so the data carries the visual weight.
2. **One accent at a time.** Amber by default. A technology-focused card re-themes the entire accent (toggles, section numbers, the brand ampersand, the focus chip, bars) to that technology's fixed hue.
3. **Colour means something.** The five technology hues are fixed identifiers; never reassign them. Green/red/grey are reserved for up/down/flat.
4. **Indexed, not absolute.** Rankings are shown as an index to the leader (= 100), never raw counts. Always caption the convention.
5. **Type does the hierarchy.** Montserrat for display and figures, IBM Plex Sans for prose, IBM Plex Mono for labels and anything tabular.

---

## 2. Colour

All values are also in `design-tokens.json` and are intended to be exposed as CSS custom properties (the names below in `--token` form).

### Base & surfaces
| Token | Hex | Role |
|---|---|---|
| `--bg` | `#0a0e14` | Page background |
| `--bg2` | `#0d1117` | Insets, track backgrounds, toggle/tab wells |
| `--panel` | `#11161f` | Primary cards / panels |
| `--panel2` | `#161b22` | Nested cards inside panels |
| `--line` | `#1f2733` | Default hairline / dividers |
| `--line2` | `#2a3340` | Stronger border |

### Ink (text ramp)
| Token | Hex | Role |
|---|---|---|
| `--ink` | `#e8eef5` | Primary text, headlines, key figures |
| `--ink2` | `#9aa7b5` | Secondary text, body |
| `--ink3` | `#5e6b7a` | Muted: labels, captions, axis ticks |

### Accent & semantic
| Token | Hex | Role |
|---|---|---|
| `--accent` | `#f5a623` | Default accent (amber). Overridden per focused technology. |
| `--accent-tint` | `rgba(245,166,35,0.14)` | Accent @ 14% — chip fills, glows, focus shadow |
| *(on-accent)* | `#1a1205` | Text/icon on a solid accent fill |
| `--up` | `#3fb950` | Positive change / upward movement |
| `--down` | `#f85149` | Negative change / downward movement |
| `--flat` | `#8b949e` | No change |

### Technology palette (fixed)
| Technology | Hex | Icon |
|---|---|---|
| Descriptive AI | `#f5a623` ◈ |
| Agentic & GenAI | `#e84b8a` ✦ |
| Blockchain & Decentralized | `#f05a32` ⬡ |
| Physical AI & Robotics | `#2abfa3` ⬢ |
| Quantum Computing | `#4a90d9` ◉ |

**Re-theming rule:** in a technology card, set `--accent` to that technology's hex and `--accent-tint` to the same hue at 14% alpha. Everything bound to `--accent` follows automatically.

### Background flourish
Page uses two faint radial glows (amber top-left, blue top-right) over `--bg`; see `shadow.pageBackdrop` in the tokens. Keep them subtle (~7% alpha).

---

## 3. Typography

Load from Google Fonts: `Montserrat:wght@500;600;700;800`, `IBM+Plex+Sans:wght@400;500;600;700`, `IBM+Plex+Mono:wght@400;500;600`.

| Family | Stack | Use |
|---|---|---|
| **Display** | `'Montserrat', 'IBM Plex Sans', sans-serif` | Headlines, section titles, metrics, brand lockup |
| **Sans** | `'IBM Plex Sans', -apple-system, sans-serif` | Body, names, descriptions |
| **Mono** | `'IBM Plex Mono', ui-monospace, monospace` | Labels, eyebrows, figures, axis ticks |

Apply `font-variant-numeric: tabular-nums` to all mono figures so numbers align.

### Scale
| Style | Family / weight | Size | Tracking | Notes |
|---|---|---|---|---|
| H1 (brand) | Display 700 | `clamp(34px,5.4vw,58px)` | −0.02em | line-height 0.98 |
| Section title | Display 700 | 20px | −0.01em | |
| Metric (large) | Display 800 | 30px | −0.02em | KPI / score |
| Metric (card) | Display 800 | 25px | −0.02em | |
| Eyebrow | Mono 500 | 11px | .32em, UPPER | accent colour |
| Lede | Sans 400 | 13.5px | — | `--ink2`, line-height 1.65 |
| Section desc | Sans 400 | 12.5px | — | `--ink2` |
| Body | Sans 400 | 13.5px | — | `--ink` |
| Body small | Sans 400 | 12px | — | `--ink2` |
| Label | Mono 500 | 10px | .06em, UPPER | `--ink3` |
| Figure | Mono 600 | 12px | — | `--ink2` |
| Caption | Sans **italic** 400 | 10.5px | — | `--ink3`, used for the index note |
| Badge | Mono 600 | 8.5px | .05em | |

### Brand lockup
"Research **&** Innovation" in Display 700. The ampersand is its own span: **upright**, weight 700, coloured with `--accent`.
```html
<h1>Research <span class="amp">&amp;</span> Innovation</h1>
```
```css
h1 .amp{ color: var(--accent); font-weight: 700; font-style: normal; }
```

---

## 4. Spacing, shape & borders

- **Spacing** — 4px base. Steps: 4, 8, 12, 16, 22, 26, 40, 48. Panel padding 20–22px (14px compact). Section gap ≈ 44px. Card gap 12px.
- **Radius** — sm 6 · md 8 · card 11 · panel 14 · pill 30 · bar/dot 3–4.
- **Borders** — 1px solid `--line` (use `--line2` for emphasis). No drop shadows except the focus treatment below.
- **Focus shadow** — `0 0 0 1px var(--accent), 0 10px 30px -12px var(--accent-tint)`.

---

## 5. Iconography

A single **line-icon family** drawn on a 24×24 grid. The set covers the five technologies and the ten industries.

**Drawing rules (all icons):**
- `viewBox="0 0 24 24"`, stroke `currentColor`, **stroke-width 1.5–1.7**, `stroke-linecap="round"`, `stroke-linejoin="round"`.
- Emphasis via selective solid fills (`fill="currentColor" stroke="none"`) and depth via reduced opacity on secondary shapes (`opacity` 0.35–0.6).
- Colour comes from the element's `color`: **technology icons use the technology hue; industry icons inherit the active accent** (default amber, or the focus technology's hue). Never hard-code a hex inside the SVG.
- Render size: 30px default · 29px in tiles · ~17px inline in legends · 30px in selector cards. Pair with a Mono/Display label.

**Technology icons**

| Technology | Hue | Glyph fallback | Visual |
|---|---|---|---|
| Descriptive AI | `#f5a623` | ◈ | Bar chart with a rising trend line |
| Agentic & GenAI | `#e84b8a` | ✦ | Four-point sparkle (twin spark) |
| Blockchain & Decentralized | `#f05a32` | ⬡ | Four linked blocks |
| Physical AI & Robotics | `#2abfa3` | ⬢ | Robot head/body |
| Quantum Computing | `#4a90d9` | ◉ | Atom with three orbitals |

**Industry icons** (rendered in the active accent)

| Industry | Covers |
|---|---|
| Energy | Exploration, production, or refining of energy products. |
| Materials | Chemicals, construction materials, metals, paper & forestry. |
| Industrials | Aerospace, defense, machinery, construction & manufacturing. |
| Consumer Goods | Food & beverage, merchandise, apparel, household & luxury. |
| Healthcare | Health-care equipment & services, pharma, biotech. |
| Financial Services | Banks, investment funds, insurance, real-estate firms. |
| Information Technology | Software, hardware, electronics & IT services. |
| Communication & Creative Services | Telecom, media, entertainment & creative industries. |
| Real Estate | Owners of commercial, industrial & residential property. |
| Automotive & Transport | Automotive companies & transportation industries. |

> The full SVG source for every icon is in `design-tokens.json` under `iconography.technology` and `iconography.industry`. The glyph column is a lightweight Unicode fallback for text-only contexts.

## 6. Charts (Chart.js 4.x)

- Grid `rgba(255,255,255,0.05)`; axis border `rgba(255,255,255,0.08)`; ticks Mono 12px `--ink3`.
- Tooltip: bg `#161b22`, border `#2a3340`, title `--ink`, body `--ink2`, padding 11; sort items descending by value.
- **Line emphasis:** every line keeps its **full** technology colour. Emphasise the focused technology with `borderWidth: 4` and `pointRadius: 4.5`; the rest stay full-colour but `borderWidth: 1.8` with `pointRadius: 0`. Tension 0.4. In an all-technology view (no focus) use a neutral `borderWidth: 2.5`, `pointRadius: 4` for all. `pointBorderColor: #0a0e14`, `pointHoverRadius: 7`.

---

## 7. Data-visualisation conventions

- **Index, don't count.** Bar rankings and leaderboards show `value / max * 100` (one decimal; the leader renders as `100`). Do not show absolute counts; add an italic caption, e.g. *“Indexed to the leader (= 100); each score is a share of the leader's volume. Absolute counts are not shown.”*
- **Trend tags** — vs the prior-period rank: `▲ N` (up, green), `▼ N` (down, red), `— 0` (flat, grey), `▲ new` (not previously ranked). N = positions moved.
- **Badges** — `NEW vs 2020 top-15` (green tint, `--up`) and `↑ from #R` (accent tint). Use a verified prior ranking; only badge "new" when truly absent from the prior list.
- **Flags** — Unicode regional-indicator emoji; fall back to 🏳️.

---

## 8. Components

Each component is themed through `--accent`, so re-theming a card needs no per-component edits.

**Eyebrow** — Mono 11px, .32em uppercase, accent, preceded by a 26px×1px accent rule.

**Focus chip** — pill (radius 30) with `1px solid var(--accent)`, fill `--accent-tint`, Display 600 15px in accent; a Mono "FOCUS" pre-label in `--ink3`, then the technology icon + name.

**Signal toggle** — segmented control in a `--bg2` well, `1px --line2`, radius 10, 3px padding. Buttons Mono 11.5px uppercase `--ink2`; active button = solid `--accent` fill, text `#1a1205`, weight 600.

**Technology selector (accordion tabs)** — Mono 10.5px chips, `--bg2` fill, `1px --line`, radius 8. Active chip: border `--accent`, text `--accent`. Defaults to the card's focused technology.

**Metric / evolution card** — `--panel2`, `1px --line`, radius 11, padding 14–15. Name (Sans 600 11px with icon), score (Display 800 25px in technology colour), label (Mono 9px `--ink3`), divider, vs-2020 / vs-2024 stats (Mono, coloured by semantic). Focused card adds the focus shadow and a Mono "◀ focus" tag after the name.

**Indexed bar row** — rank no. (Mono 10px `--ink3`) · flag · name (Sans 11.5px `--ink2`, truncating) · track (`--bg2`, height 18, radius 4) · fill (technology colour, right-aligned index label in `#0a0e14`) · trend tag.

**Leaderboard row** — big rank (Display 700, accent for #1) · name (Sans 500 12.5px) with optional badge · thin progress bar (accent, 3px) · index value (Mono 600). Row hover = `--bg2`. Close the list with the italic index caption.

**Panel / section** — section header = Mono section number in accent + Display 700 title; optional Sans description in `--ink2`; content in a `--panel` panel (radius 14). Two-up layouts use a `1fr 1fr` grid, ~26px gap, collapsing to one column under ~820px.

---

## 9. Usage rules (do / don't)

- **Do** keep exactly one accent active per screen; re-theme by swapping `--accent`/`--accent-tint` only.
- **Do** keep technology hues fixed and consistent everywhere (lines, dots, bars, scores).
- **Do** caption every indexed visual and verify trend/badge claims against real prior-period data.
- **Don't** use Display (Montserrat) for body text, or Sans for axis/labels — labels and figures are Mono.
- **Don't** italicise the ampersand (changed in v1.0) or introduce drop shadows beyond the focus treatment.
- **Don't** show absolute counts in rankings; the index is the public figure.

---

## 10. Files in this package

| File | Purpose |
|---|---|
| `DESIGN_SYSTEM.md` | This spec — primary reference for an implementing agent. |
| `design-tokens.json` | Machine-readable tokens (colour, type, spacing, radii, chart, technology map). |
| `design-system-preview.html` | Rendered preview to validate look & feel. |
