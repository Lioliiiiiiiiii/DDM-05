#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Disruption Matrix 2026 — static site builder.
Assembles the standalone HTML components in _src/ into a coherent multi-page
site under the repo root, adapting every dashboard to the dark design system
(Public/DESIGN_SYSTEM.md / design-tokens.json) without inventing data.
"""
import os, re, html, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
SRC  = os.path.join(ROOT, "_src")

def rd(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()

def wr(relpath, content):
    p = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", relpath, f"({len(content):,}b)")

# ----------------------------------------------------------------------------
# Design-system fonts (loaded on every page / embed)
# ----------------------------------------------------------------------------
DS_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?'
            'family=Montserrat:wght@500;600;700;800&'
            'family=IBM+Plex+Sans:wght@400;500;600;700&'
            'family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">')

# ----------------------------------------------------------------------------
# Technology + industry metadata (slugs match the foresight-matrix data-attrs,
# the perception-overview drill panels, and the selector).
# ----------------------------------------------------------------------------
TECH_ICON = {
 "descriptive-ai":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><rect x="6.4" y="12.5" width="2.6" height="5.5" rx="0.7" fill="currentColor" stroke="none"/><rect x="10.7" y="9.5" width="2.6" height="8.5" rx="0.7" fill="currentColor" stroke="none" opacity="0.5"/><rect x="15" y="6.5" width="2.6" height="11.5" rx="0.7" fill="currentColor" stroke="none"/><path d="M6 9.7l3.6-3.1 3 2 3.9-4.4"/><circle cx="16.5" cy="4.2" r="1.5" fill="currentColor" stroke="none"/></svg>',
 "generative-agentic-ai":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 3c.6 3.8 1.9 5.1 5.7 5.7-3.8.6-5.1 1.9-5.7 5.7-.6-3.8-1.9-5.1-5.7-5.7C10.1 8.1 11.4 6.8 12 3Z" fill="currentColor" stroke="none"/><path d="M18.5 14.5c.3 1.8.9 2.4 2.7 2.7-1.8.3-2.4.9-2.7 2.7-.3-1.8-.9-2.4-2.7-2.7 1.8-.3 2.4-.9 2.7-2.7Z" fill="currentColor" stroke="none" opacity="0.6"/></svg>',
 "blockchain":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.4"/><rect x="14" y="14" width="7" height="7" rx="1.4"/><rect x="14" y="3" width="7" height="7" rx="1.4" opacity="0.5"/><rect x="3" y="14" width="7" height="7" rx="1.4" opacity="0.5"/><path d="M10 6.5h4M6.5 10v4M17.5 10v4M10 17.5h4"/></svg>',
 "robotics":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><rect x="4" y="7.5" width="16" height="11" rx="2.5"/><circle cx="12" cy="4" r="1.3" fill="currentColor" stroke="none"/><path d="M12 5.3v2.2"/><circle cx="9" cy="13" r="1.4" fill="currentColor" stroke="none"/><circle cx="15" cy="13" r="1.4" fill="currentColor" stroke="none"/><path d="M2.5 12v3M21.5 12v3"/></svg>',
 "quantum-computing":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none"/><ellipse cx="12" cy="12" rx="10" ry="4.3"/><ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(120 12 12)"/></svg>',
}
IND_ICON = {
 "energy":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2.5 L6.5 13 H11 L10.3 21.5 L17.8 10 H12.7 Z" fill="currentColor" stroke="none"/><path d="M4.6 6.4a9.5 9.5 0 0 0-1.1 4.3" opacity="0.45"/><path d="M20.5 13.3a9.5 9.5 0 0 1-1.1 4.3" opacity="0.45"/></svg>',
 "materials":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><path d="M12 3 21 7.5 12 12 3 7.5 12 3Z"/><path d="M3 12 12 16.5 21 12" opacity="0.55"/><path d="M3 16.5 12 21 21 16.5" opacity="0.35"/></svg>',
 "industrials":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M21.5 12h-3M5.5 12h-3M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1M18.7 18.7l-2.1-2.1M7.4 7.4 5.3 5.3"/></svg>',
 "consumer-goods":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><path d="M5.5 8h13l-1 11.5a1 1 0 0 1-1 .9H7.5a1 1 0 0 1-1-.9L5.5 8Z"/><path d="M8.5 8V6.5a3.5 3.5 0 0 1 7 0V8"/></svg>',
 "healthcare":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"><path d="M12 20.5S3.5 15 3.5 8.8A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.5 1.8C20.5 15 12 20.5 12 20.5Z"/><path d="M6.5 12h2l1.5-2.5 2 4 1.5-1.5H17"/></svg>',
 "financial-services":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><path d="M3.5 9 12 4l8.5 5"/><path d="M5 9v8M9 9v8M15 9v8M19 9v8"/><path d="M3.5 20.5h17"/></svg>',
 "information-technology":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><rect x="7" y="7" width="10" height="10" rx="1.6"/><path d="M10 7V4M14 7V4M10 20v-3M14 20v-3M7 10H4M7 14H4M20 10h-3M20 14h-3"/></svg>',
 "communication-creative":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><path d="M4 5.5h16a1 1 0 0 1 1 1V16a1 1 0 0 1-1 1H9l-4 3.5V17H4a1 1 0 0 1-1-1V6.5a1 1 0 0 1 1-1Z"/><path d="M8 10h8M8 13h5"/></svg>',
 "real-estate":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><path d="M5 20.5V6l7-3 7 3v14.5"/><path d="M3.5 20.5h17"/><path d="M9.5 11h.01M14.5 11h.01M9.5 15h.01M14.5 15h.01" stroke-width="2"/></svg>',
 "automotive-transport":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><path d="M3 14l1.8-5.2A2 2 0 0 1 6.7 7.5h10.6a2 2 0 0 1 1.9 1.3L21 14v4.5h-3V17H6v1.5H3Z"/><circle cx="7" cy="14.5" r="1.3"/><circle cx="17" cy="14.5" r="1.3"/></svg>',
}

TECHS = [
 dict(slug="descriptive-ai", name="Descriptive AI", color="#f5a623", uni="Descriptive AI",
      desc="Descriptive AI encompasses traditional AI approaches that analyze and interpret existing data to identify patterns, make predictions, and derive insights. This technology forms the foundation of practical AI applications in industry through machine learning, statistical analysis, and pattern recognition."),
 dict(slug="generative-agentic-ai", name="Generative AI &amp; Agentic AI", color="#e84b8a", uni="Agentic & GenAI",
      desc="Generative AI and Agentic AI refers to AI systems that can create new content (text, images, code, synthetic data) and autonomously plan and execute multi-step actions to achieve goals. This technology leverages large language models and neural networks to generate novel outputs based on patterns learned from training data."),
 dict(slug="blockchain", name="Blockchain &amp; Decentralized Systems", color="#f05a32", uni="Blockchain",
      desc="Blockchain technology enables secure, decentralized record-keeping and transactions without requiring central authority. It creates transparent, immutable records across distributed networks, supporting applications from cryptocurrency to supply chain tracking."),
 dict(slug="robotics", name="Physical AI &amp; Robotics", color="#2abfa3", uni="Robotics",
      desc="Physical AI and Robotics encompasses the design and deployment of physical systems that can perceive, reason, learn, and act in the real world with varying levels of intelligence and autonomy. This includes robotics, embodied AI, autonomous systems, and technologies combining intelligence with physical interaction."),
 dict(slug="quantum-computing", name="Quantum Computing", color="#4a90d9", uni="Quantum",
      desc="Quantum Computing harnesses quantum mechanical phenomena like superposition and entanglement to perform computations. This technology enables exponentially faster calculations for specific problems, particularly in cryptography, material science, and complex system optimization."),
]
INDUSTRIES = [
 dict(slug="energy", name="Energy", uni="Energy",
      desc="Companies involved in the exploration, production, or refining of energy products."),
 dict(slug="materials", name="Materials", uni="Materials",
      desc="Businesses in chemicals, construction materials, metals, paper, and forestry products."),
 dict(slug="industrials", name="Industrials", uni="Industrials",
      desc="Aerospace, defense, machinery, construction, fabrication, and manufacturing."),
 dict(slug="consumer-goods", name="Consumer Goods", uni="Consumer Goods",
      desc="Food &amp; Beverage, General Merchandise, Clothing &amp; Apparel, Household &amp; Personal Care, mass-market &amp; luxury goods."),
 dict(slug="healthcare", name="Healthcare", uni="Healthcare",
      desc="Health care equipment and services, pharmaceuticals, and biotechnology companies."),
 dict(slug="financial-services", name="Financial Services", uni="Financial Services",
      desc="Banks, investment funds, insurance companies, and real estate firms."),
 dict(slug="information-technology", name="Information Technology", uni="Information Technology",
      desc="Software, hardware, electronics, and IT services."),
 dict(slug="communication-creative", name="Communication &amp; Creative Services", uni="Communication & Creative Services",
      desc="Telecommunications, media, entertainment, and creative industries."),
 dict(slug="real-estate", name="Real Estate", uni="Real Estate",
      desc="Companies that own commercial, industrial, and residential real estate."),
 dict(slug="automotive-transport", name="Automotive &amp; Transport", uni="Automotive & Transport",
      desc="Mainstream automotive companies and transportation-related industries."),
]
TECH_BY = {t["slug"]: t for t in TECHS}
IND_BY  = {i["slug"]: i for i in INDUSTRIES}

# ============================================================================
# SHELL TEMPLATE
# ============================================================================
def nav_links(root, active):
    groups = [
        ("Explore by Sector", [
            ("technology", "Technology", root+"explore/technology.html"),
            ("industry", "Industry", root+"explore/industry.html"),
            ("tech-x-industry", "Technology &times; Industry", root+"explore/tech-x-industry.html"),
        ]),
        ("Explore by Data", [
            ("perception", "Professionals&rsquo; Perception", root+"data/professionals-perception.html"),
            ("unicorn", "Unicorn Factor", root+"data/unicorn-factor.html"),
            ("research", "Research &amp; Innovation", root+"data/research-innovation.html"),
        ]),
        ("More", [
            ("about", "About us", root+"more/about.html"),
            ("methodology", "Methodology", root+"more/methodology.html"),
            ("faq", "FAQ", root+"more/faq.html"),
            ("contact", "Contact", root+"more/contact.html"),
            ("acknowledgment", "Acknowledgment", root+"more/acknowledgment.html"),
        ]),
    ]
    out = []
    for title, items in groups:
        out.append(f'<div class="nav-group"><div class="nav-eyebrow">{title}</div>')
        for key, label, href in items:
            cls = ' class="active"' if key == active else ''
            out.append(f'<a href="{href}"{cls}>{label}</a>')
        out.append('</div>')
    return "\n      ".join(out)

def topbar_actions(root):
    return f'''<a href="{root}key-findings.html" class="btn btn-ghost btn-anim">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.5.4.5 1 .5 1.6h6c0-.6 0-1.2.5-1.6A6 6 0 0 0 12 3Z"/></svg>
      <span class="lbl">Key findings</span></a>
    <a href="{root}heatmatrix.html" class="btn btn-ghost btn-anim">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><rect x="3.5" y="3.5" width="7" height="7" rx="1.3"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.3" fill="currentColor" stroke="none" opacity=".4"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.3" fill="currentColor" stroke="none" opacity=".4"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.3"/></svg>
      <span class="lbl">Heatmatrix</span></a>
    <a href="{root}download.html" class="btn btn-primary">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v10m0 0 4-4m-4 4-4-4"/><path d="M5 19h14"/></svg>
      <span class="lbl">Download the report</span></a>'''

def shell(root, active, title, crumb, body, head_extra="", body_class=""):
    return f'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Digital Disruption Matrix 2026</title>
{DS_FONTS}
<link rel="stylesheet" href="{root}assets/css/shell.css">
{head_extra}
</head>
<body class="{body_class}">
<div class="glow"></div>
<aside class="sidebar">
  <div class="brand">
    <a href="{root}index.html"><div class="mark">Digital Disruption Matrix</div></a>
    <div class="ed">Edition 2026</div>
  </div>
  <nav class="nav">
      {nav_links(root, active)}
  </nav>
</aside>
<div class="scrim"></div>
<div class="topbar">
  <label class="navtoggle" aria-label="Toggle menu">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
  </label>
  <div class="crumb">{crumb}</div>
  <div class="actions">
    {topbar_actions(root)}
  </div>
</div>
<main class="page">
  <div class="container">
{body}
    <footer class="site">
      <span>Digital Disruption Matrix 2026 · ESSEC Business School</span>
      <span>5 technologies × 10 industries</span>
    </footer>
  </div>
</main>
<script src="{root}assets/js/shell.js"></script>
</body>
</html>'''

print("build.py metadata + shell ready")

# ============================================================================
# RE-THEME HELPERS  (non-destructive: wrap doc + append :root override)
# ============================================================================
def standalone(title, original, override_css, extra_script="", extra_head=""):
    """Wrap an HTML fragment/doc into a valid standalone document themed to DS."""
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{title}</title>{DS_FONTS}{extra_head}</head><body>\n'
            f'{original}\n'
            f'<style id="ds-theme-override">{override_css}</style>\n'
            f'{extra_script}\n</body></html>')

# ---- Perception (light "paper" -> dark) ------------------------------------
PERCEPTION_OVERRIDE = """
:root{
  --paper:#0a0e14; --surface:#11161f; --ink:#e8eef5; --ink-2:#9aa7b5; --ink-3:#5e6b7a;
  --line:#1f2733; --line-2:#2a3340; --mute:#2a3340;
  --tech:#f5a623; --tech-soft:rgba(245,166,35,.16);
  --indus:#4a90d9; --indus-soft:rgba(74,144,217,.16);
  --font-disp:'Montserrat','IBM Plex Sans',sans-serif;
  --font-body:'IBM Plex Sans',-apple-system,sans-serif;
  --font-mono:'IBM Plex Mono',ui-monospace,monospace;
}
html{color-scheme:dark}
html,body{background:#0a0e14!important;color:var(--ink);min-height:0!important;height:auto!important}
.owrap,.gwrap,.wrap{max-width:none!important}
/* surfaces that were pure white */
.module,.kpi,.scatterwrap,.chip,.gcard .module{background:var(--surface)}
.empty{background:var(--panel2,#161b22)}
.track{background:#0d1117}
.fill{background:var(--mute)}
/* stacked timeline segments: Now/Soon are the dark teal end -> white text;
   Later/Never are the light end (.seg.dim) -> dark text */
.seg{color:#fff}
.seg.dim{color:#0a0e14}
.controls{background:#0a0e14!important}
/* active pills -> accent */
.pill.on{background:var(--tech)!important;color:#0a0e14!important;border-color:var(--tech)!important}
.upill.on{background:var(--tech)!important;color:#0a0e14!important;border-color:var(--tech)!important}
/* inverted bars (used --ink as a dark bg + --paper text) */
.drillbar{background:#161b22!important;color:var(--ink)!important;border:1px solid var(--line)}
.drillbar button{color:var(--ink)!important;border-color:var(--line-2)!important;background:transparent}
.drillbar button:hover{background:rgba(255,255,255,.08)!important}
.mod-glyph.indus{background:var(--indus-soft);color:var(--indus)}
.chip-ic{background:var(--indus-soft);color:var(--indus)}
.chip:hover{border-color:var(--indus);box-shadow:0 1px 0 var(--indus)}
.chip.tech .chip-ic{background:var(--tech-soft);color:var(--tech)}
a{color:var(--tech)}
/* breathing room between blocks (match the host page's section rhythm) */
.block+.block{margin-top:34px}
.mod-body{padding:24px 28px 30px}
.kpis{margin-bottom:4px}
/* EMBED MODE (slice): the host section header already names the tech/industry,
   so drop the module's own title row; keep the descriptive sub-line. */
body.embed-slice .mod-top{display:none}
body.embed-slice .mod-head{padding:4px 2px 16px;border-bottom:1px solid var(--line)}
body.embed-slice .mod-body{padding:22px 2px 6px}
body.embed-slice .module{border:0;background:transparent}
body.embed-slice .module::before{display:none}
body.embed-slice .gcard{margin:0}
"""

# parameter script for the foresight slice embed
FORESIGHT_PARAM = """
<script>
(function(){
  var p=new URLSearchParams(location.search);
  var embed=p.get('embed')==='1';
  function setSel(){
    if(typeof sel==='undefined') return setTimeout(setSel,30);
    if(p.get('type')) sel.type=p.get('type');
    if(p.get('tech')) sel.tech=p.get('tech');
    if(p.get('indus')) sel.indus=p.get('indus');
    if(typeof apply==='function') apply();
    if(embed){
      document.body.classList.add('embed-slice');
      var hide=document.querySelectorAll('.gh,.gsub,.controls');
      hide.forEach(function(e){e.style.display='none';});
      var w=document.querySelector('.gwrap'); if(w){w.style.padding='0';w.style.maxWidth='none';}
      var g=document.querySelector('.gcard:not(.hide)'); if(g){g.style.marginTop='0';}
    }
    // initialise the "most-voted use cases" selectors so only the default
    // group (top 3) shows — otherwise every group renders until a pill is clicked.
    document.querySelectorAll('.upill.on').forEach(function(b){ b.click(); });
  }
  setSel();
})();
</script>
"""

OVERVIEW_INIT = """
<script>
(function(){
  // show only the default "most-voted use cases" group (top 3) on load
  function init(){
    var pills=document.querySelectorAll('.upill.on');
    if(!pills.length) return setTimeout(init,40);
    pills.forEach(function(b){ b.click(); });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
</script>
"""

def recolor_perception(body):
    """Swap the green stacked-bar ramp (Now/Soon/Later/Never) for a DS teal ramp.
    Colour only — no data is altered."""
    ramp = {
        "#0C5544": "#0e5a4b",  # Now   (darkest)  -> deep teal
        "#1D9E75": "#1f9e85",  # Soon              -> teal
        "#9FE1CB": "#7bd5c2",  # Later (light)     -> light teal
        "#EDE9DE": "#9aa7b5",  # Never (neutral)   -> DS grey
    }
    for old, new in ramp.items():
        body = body.replace("background:" + old, "background:" + new)
    return body

def build_perception_embeds():
    overview = recolor_perception(rd("perception-overview.html"))
    wr("embed/perception-overview.html",
       standalone("Professionals&rsquo; Perception", overview, PERCEPTION_OVERRIDE, OVERVIEW_INIT))
    foresight = recolor_perception(rd("perception-foresight.html"))
    wr("embed/perception-foresight.html",
       standalone("Foresight matrix — perception", foresight, PERCEPTION_OVERRIDE, FORESIGHT_PARAM))

# ---- Unicorn (legacy dark -> DS tokens + Montserrat display) ----------------
UNICORN_OVERRIDE = """
:root{
  --bg:#0a0e14; --panel:#11161f; --panel2:#161b22;
  --line:rgba(255,255,255,.07); --line2:rgba(255,255,255,.12);
  --ink:#e8eef5; --mut:#9aa7b5; --mut2:#5e6b7a;
  --native:#f5a623; --unicorn:#4a90d9; --emerging:#2abfa3;
  --native-d:rgba(245,166,35,.16); --unicorn-d:rgba(74,144,217,.16); --emerging-d:rgba(42,191,163,.16);
}
html{color-scheme:dark}
html,body{background:#0a0e14!important;background-image:none!important;min-height:0!important;height:auto!important}
.wrap{max-width:none!important}
.disp,h1,h2.sec,.explorer h1,.ebtn .et,.gcard .yoy,#tip .tn,#ftip .tn{
  font-family:'Montserrat','IBM Plex Sans',sans-serif!important;letter-spacing:-.01em}
.toggle button.on{color:#0a0e14}
.toggle button.on.s{background:var(--emerging);color:#04140e}
"""
UNICORN_PARAM = """
<script>
(function(){
  // Options are built in fixed array order (a leading "All" then tech_order /
  // industry list), and clicking one runs the dashboard's own redraw. We match
  // by index, which is robust to the lbl() display transform.
  var TORDER=["Descriptive AI","Agentic & GenAI","Blockchain","Robotics","Quantum"];
  var IORDER=["Energy","Materials","Industrials","Consumer Goods","Healthcare","Financial Services","Information Technology","Communication & Creative Services","Real Estate","Automotive & Transport"];
  // this embed is only ever iframed -> drop the internal hero (the host page
  // supplies its own title) and the dead "#" Explore-more links.
  function hideChrome(){
    ['.hero','#sec-explore'].forEach(function(s){
      var e=document.querySelector(s); if(e) e.style.display='none';});
    var w=document.querySelector('.wrap'); if(w) w.style.paddingTop='8px';
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',hideChrome);
  else hideChrome();
  var p=new URLSearchParams(location.search);
  var tech=p.get('tech'), indus=p.get('indus');
  if(!tech&&!indus) return;
  var ti = tech ? TORDER.indexOf(tech) : -1;
  // technology option index: explicit tech -> ti+1; industry-only -> 0 ("All
  // technologies") so the view spans all five techs within that industry.
  var techIdx = tech ? (ti>=0 ? ti+1 : -1) : (indus ? 0 : -1);
  var ii = indus ? IORDER.indexOf(indus) : -1; // industry option index ii+1
  function clickIdx(boxId, idx){
    var box=document.getElementById(boxId); if(!box) return false;
    var opts=box.querySelectorAll('.opt'); if(opts.length<=idx) return false;
    if(!opts[idx].classList.contains('on')) opts[idx].click();
    return true;
  }
  var tries=0;
  function go(){
    tries++;
    var okT = techIdx<0 || (clickIdx('opt-tech', techIdx) & clickIdx('opt-gtech', techIdx));
    var okI = ii<0     || clickIdx('opt-ind', ii+1);
    if(okT && okI) return;
    if(tries<50) setTimeout(go,80);
  }
  setTimeout(go,140);
})();
</script>
"""
def build_unicorn_embed():
    uni = rd("unicorn.html")
    wr("embed/unicorn.html",
       standalone("Unicorn Factor", uni, UNICORN_OVERRIDE, UNICORN_PARAM))

# ---- Radar (blue/orange -> DS amber + fonts) -------------------------------
RADAR_OVERRIDE = """
:root{
  --bg-0:#0a0e14; --bg-1:#0d1117; --bg-2:#11161f; --panel:#11161f;
  --line:#1f2733; --grid:#2a3340;
  --text:#e8eef5; --text-dim:#9aa7b5; --text-faint:#5e6b7a;
  --acc:#f5a623; --acc-soft:rgba(245,166,35,.30); --acc-line:#f5a623;
}
html{color-scheme:dark}
html,body{font-family:'IBM Plex Sans',-apple-system,sans-serif!important;background:#0a0e14!important;min-height:0!important;height:auto!important}
.eyebrow,.ax-name,.overview-link{font-family:'Montserrat','IBM Plex Sans',sans-serif!important}
.ax-desc,.hint,.dd-btn{font-family:'IBM Plex Sans',-apple-system,sans-serif!important}
.val{font-family:'IBM Plex Mono',ui-monospace,monospace!important}
/* dropdowns sit near the bottom of the embed -> open menus upward so the
   iframe can't clip them */
.dd-menu{top:auto!important;bottom:calc(100% + 8px)!important;max-height:300px!important;overflow-y:auto!important}
"""
# report the radar's own selection (state.tech / state.ind) up to the host page
RADAR_PARAM = """
<script>
(function(){
  // `state` is a const (not on window), so read the selection from the DOM:
  // a chosen dropdown drops its button's "placeholder" class and the label
  // shows the selected key (e.g. "Descriptive AI" / "Energy").
  function val(btnId,lblId){
    var b=document.getElementById(btnId);
    if(!b || b.classList.contains('placeholder')) return null;
    var l=document.getElementById(lblId);
    return l ? l.textContent.trim() : null;
  }
  function emit(){
    try{
      parent.postMessage({source:'ddm-radar',
        tech:val('btn-tech','lbl-tech'), ind:val('btn-ind','lbl-ind')}, '*');
    }catch(e){}
  }
  function hook(){
    if(typeof window.update!=='function') return setTimeout(hook,50);
    var orig=window.update;
    window.update=function(){ var r=orig.apply(this,arguments); setTimeout(emit,0); return r; };
    emit();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',hook); else hook();
})();
</script>
"""
def build_radar_embed():
    radar = rd("radar.html")
    # radar is already a full document; inject DS fonts + override + reporter
    doc = radar
    if "</head>" in doc:
        doc = doc.replace("</head>", DS_FONTS + "</head>", 1)
    else:
        doc = DS_FONTS + doc
    tail = f'<style id="ds-theme-override">{RADAR_OVERRIDE}</style>{RADAR_PARAM}'
    if "</body>" in doc:
        doc = doc.replace("</body>", tail + "</body>", 1)
    else:
        doc = doc + tail
    wr("embed/radar.html", doc)

# ---- Research (already dark; swap Bricolage display -> Montserrat) ----------
RESEARCH_OVERRIDE = """
:root{--disp:'Montserrat','IBM Plex Sans',sans-serif!important}
html{color-scheme:dark}
html,body{background:#0a0e14!important;min-height:0!important;height:auto!important}
/* host section header already says "Research & Innovation" -> drop the
   masthead eyebrow ("Technology Intelligence · … · 2020–2025"), the duplicate
   title and the focus chip. */
.masthead #eyebrow,.masthead h1,.masthead #techChip{display:none!important}
.masthead{border-bottom:0!important;padding-bottom:10px!important}
.card.sel .card-name::after{content:none!important}
"""
def retheme_research(src_name, out_name, title):
    doc = rd(src_name)
    if "</head>" in doc:
        doc = doc.replace("</head>", DS_FONTS + "</head>", 1)
    if "</body>" in doc:
        doc = doc.replace("</body>", f'<style id="ds-theme-override">{RESEARCH_OVERRIDE}</style></body>', 1)
    else:
        doc = doc + f'<style id="ds-theme-override">{RESEARCH_OVERRIDE}</style>'
    wr(out_name, doc)

def build_research_embeds():
    retheme_research("research-dashboard.html", "embed/research-dashboard.html", "Research & Innovation")
    for t in TECHS:
        retheme_research(f"research-{t['slug']}.html", f"embed/research/{t['slug']}.html", t["name"])

print("retheme functions ready")

# ============================================================================
# HOMEPAGE (adapt hero: real nav links + logo files)
# ============================================================================
def build_homepage():
    h = rd("hero.html")
    # swap the 3 base64 images (order: ESSEC, BNP, SIA) for local files
    repls = ["assets/img/essec-blanc.png", "assets/img/bnp.png", "assets/img/sia.jpg"]
    idx = [0]
    def sub(m):
        i = idx[0]; idx[0]+= 1
        return 'src="' + (repls[i] if i < len(repls) else m.group(1)) + '"'
    h = re.sub(r'src="(data:image[^"]*)"', sub, h)
    # rewrite nav + action hrefs to real pages
    linkmap = {
        '#technology':'explore/technology.html', '#industry':'explore/industry.html',
        '#tech-x-industry':'explore/tech-x-industry.html',
        '#perception':'data/professionals-perception.html', '#unicorn':'data/unicorn-factor.html',
        '#research':'data/research-innovation.html',
        '#about':'more/about.html', '#methodology':'more/methodology.html', '#faq':'more/faq.html',
        '#contact':'more/contact.html', '#acknowledgment':'more/acknowledgment.html',
        '#key-findings':'key-findings.html', '#heatmatrix':'heatmatrix.html',
        '#download-report':'download.html',
    }
    for k, v in linkmap.items():
        h = h.replace(f'href="{k}"', f'href="{v}"')
    # brand link
    h = h.replace('<a href="#" style="text-decoration:none">', '<a href="index.html" style="text-decoration:none">')
    # --- visual tweaks requested ---
    # 1. thinner hero title (700 -> 600 reads more refined)
    h = h.replace('h1{font-family:var(--display);font-weight:700', 'h1{font-family:var(--display);font-weight:600')
    # 2. larger nav text + eyebrow
    h = h.replace('font-family:var(--sans);font-size:13.5px;color:var(--ink2);text-decoration:none',
                  'font-family:var(--sans);font-size:15px;color:var(--ink2);text-decoration:none')
    h = re.sub(r'font-size:10\.5px;(\s*)letter-spacing:\.22em', r'font-size:11px;\1letter-spacing:.22em', h)
    # 3. partner logos: the source files were trimmed of their padding, so the
    #    logos now fill the chip. Dark-text marks need a light chip to stay legible,
    #    so keep a tight white badge and size the (now full-bleed) logos generously.
    h = h.replace('.chip.bnp img{height:22px}', '.chip.bnp img{height:26px}')
    h = h.replace('.chip.sia img{height:26px}', '.chip.sia img{height:30px}')
    h = h.replace('.chip{background:#fff;border-radius:9px;padding:10px 14px',
                  '.chip{background:#fff;border-radius:9px;padding:9px 13px')
    # 4. bigger topbar buttons + travelling-border animation on the two ghost ones
    h = h.replace('.btn{display:inline-flex;align-items:center;gap:8px;height:40px;padding:0 17px;',
                  '.btn{display:inline-flex;align-items:center;gap:9px;height:46px;padding:0 21px;')
    h = h.replace('.btn svg{width:15px;height:15px}', '.btn svg{width:17px;height:17px}')
    h = h.replace('font-weight:500;font-size:11.5px;\n    letter-spacing:.06em;text-transform:uppercase',
                  'font-weight:500;font-size:12.5px;\n    letter-spacing:.06em;text-transform:uppercase')
    btn_anim_css = ("<style>"
      "@property --bdr-angle{syntax:'<angle>';initial-value:0deg;inherits:false}"
      ".btn-anim{position:relative;isolation:isolate}"
      ".btn-anim::before{content:\"\";position:absolute;inset:0;border-radius:inherit;padding:1.6px;"
      "background:conic-gradient(from var(--bdr-angle),transparent 0deg,transparent 250deg,var(--accent) 320deg,#fff 340deg,var(--accent) 350deg,transparent 360deg);"
      "-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;"
      "mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);mask-composite:exclude;"
      "animation:bdr-rotate 4.5s linear infinite;pointer-events:none}"
      "@keyframes bdr-rotate{to{--bdr-angle:360deg}}"
      "@media (prefers-reduced-motion:reduce){.btn-anim::before{display:none}}"
      "</style>")
    h = h.replace("</head>", btn_anim_css + "</head>", 1)
    h = h.replace('<a href="key-findings.html" class="btn btn-ghost">',
                  '<a href="key-findings.html" class="btn btn-ghost btn-anim">')
    h = h.replace('<a href="heatmatrix.html" class="btn btn-ghost">',
                  '<a href="heatmatrix.html" class="btn btn-ghost btn-anim">')
    wr("index.html", h)

# ============================================================================
# SELECTOR embed (tech/industry) + explore landing pages
# ============================================================================
SELECTOR_NAV = """
<script>
(function(){
  var techSlug={"Descriptive AI":"descriptive-ai","Generative AI & Agentic AI":"generative-agentic-ai","Blockchain & Decentralized Systems":"blockchain","Physical AI & Robotics":"robotics","Quantum Computing":"quantum-computing"};
  var indSlug={"Energy":"energy","Materials":"materials","Industrials":"industrials","Consumer Goods":"consumer-goods","Healthcare":"healthcare","Financial Services":"financial-services","Information Technology":"information-technology","Communication & Creative Services":"communication-creative","Real Estate":"real-estate","Automotive & Transport":"automotive-transport"};
  var p=new URLSearchParams(location.search), view=p.get('view');
  function go(href){ (window.parent!==window?window.parent:window).location.href=href; }
  function ready(){
    var tg=document.getElementById('techGrid');
    if(!tg||!tg.children.length) return setTimeout(ready,40);
    if(view){
      var btn=document.querySelector('.toggle button[data-view="'+view+'"]');
      if(btn&&!btn.classList.contains('active')) btn.click();
      var tog=document.querySelector('.toggle'); if(tog) tog.style.display='none';
      var hd=document.querySelector('.head'); if(hd){hd.style.justifyContent='flex-start';}
      var ey=document.querySelector('.eyebrow'); if(ey){ey.textContent=(view==='industry'?'Select an industry':'Select a technology');}
    }
    document.querySelectorAll('#techGrid .card').forEach(function(c){
      var nm=c.querySelector('.card-name').textContent.trim(), s=techSlug[nm];
      if(s) c.addEventListener('click',function(){go('../technology/'+s+'.html');});
    });
    document.querySelectorAll('#industryGrid .card').forEach(function(c){
      var nm=c.querySelector('.card-name').textContent.trim(), s=indSlug[nm];
      if(s) c.addEventListener('click',function(){go('../industry/'+s+'.html');});
    });
  }
  ready();
})();
</script>
"""
def build_selector_embed():
    sel = rd("selector.html")
    sel = sel.replace("</body>", SELECTOR_NAV + "</body>", 1)
    wr("embed/selector.html", sel)

def iframe(src, h=900):
    return (f'<div class="embed-wrap"><iframe class="embed-frame" src="{src}" '
            f'style="height:{h}px" title="embedded dashboard" loading="eager" '
            f'scrolling="no" frameborder="0"></iframe></div>')

def build_explore_selectors():
    body_t = f'''    <div class="eyebrow">Explore by Sector</div>
    <h1 class="page-title">Technology</h1>
    <p class="page-lede">Choose one of the five frontier technologies to open its dedicated view — perception, unicorn factor and research &amp; innovation, all focused on that technology.</p>
    {iframe("../embed/selector.html?view=tech", 760)}'''
    wr("explore/technology.html",
       shell("../", "technology", "Technology", '<span>Explore</span><span class="sep">/</span><b>Technology</b>', body_t))

    body_i = f'''    <div class="eyebrow">Explore by Sector</div>
    <h1 class="page-title">Industry</h1>
    <p class="page-lede">Choose one of the ten industries to open its dedicated view — how professionals read the signal and where the ventures cluster, focused on that industry.</p>
    {iframe("../embed/selector.html?view=industry", 760)}'''
    wr("explore/industry.html",
       shell("../", "industry", "Industry", '<span>Explore</span><span class="sep">/</span><b>Industry</b>', body_i))

# ============================================================================
# DATA PAGES (Explore by Data) — full-page embeds
# ============================================================================
def build_data_pages():
    p = f'''    <div class="eyebrow">Explore by Data</div>
    <h1 class="page-title">Professionals&rsquo; Perception</h1>
    <p class="page-lede">How 1,000 surveyed industry professionals read the signal across the five technologies and ten industries — adoption, expected impact, and the intersections that matter most.</p>
    {iframe("../embed/perception-overview.html", 1600)}'''
    wr("data/professionals-perception.html",
       shell("../", "perception", "Professionals&rsquo; Perception",
             '<span>Data</span><span class="sep">/</span><b>Professionals&rsquo; Perception</b>', p))

    u = f'''    <div class="eyebrow">Explore by Data</div>
    <h1 class="page-title">Unicorn Factor</h1>
    <p class="page-lede">Frontier-tech intelligence from the startup and unicorn landscape — where ventures cluster, the 2025 founding wave, and the concentration of capital. Filter by technology, industry and country.</p>
    {iframe("../embed/unicorn.html", 1700)}'''
    wr("data/unicorn-factor.html",
       shell("../", "unicorn", "Unicorn Factor",
             '<span>Data</span><span class="sep">/</span><b>Unicorn Factor</b>', u))

    r = f'''    <div class="eyebrow">Explore by Data</div>
    <h1 class="page-title">Research &amp; Innovation</h1>
    <p class="page-lede">The scholarly and patent signal behind each technology — publication and patent momentum, leading geographies, and how the frontier has shifted from 2020 to 2025.</p>
    {iframe("../embed/research-dashboard.html", 1700)}'''
    wr("data/research-innovation.html",
       shell("../", "research", "Research &amp; Innovation",
             '<span>Data</span><span class="sep">/</span><b>Research &amp; Innovation</b>', r))

# ============================================================================
# COMPOSED PER-TECH / PER-INDUSTRY / CELL PAGES
# ============================================================================
def focus_chip(label, icon, color, pre="Focus"):
    return (f'<div class="focus-chip" style="--accent:{color};border-color:{color};color:{color};'
            f'background:{color}22"><span class="pre">{pre}</span>'
            f'<span style="color:{color}">{icon}</span>{label}</div>')

def section(num, title, desc, inner, note=None, sid=None):
    n = f'<div class="note-strip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.5h.01"/></svg><span>{note}</span></div>' if note else ""
    d = f'<div class="section-desc">{desc}</div>' if desc else ""
    ida = f' id="{sid}"' if sid else ""
    return f'''    <section class="section"{ida}>
      <div class="section-head"><span class="section-num">{num}</span><div><div class="section-title">{title}</div>{d}</div></div>
      {n}
      {inner}
    </section>'''

def scrollspy(items):
    """items: list of (target_id, num, label)."""
    links = "".join(f'<a href="#{sid}"><span class="n">{num}</span>{label}</a>' for sid, num, label in items)
    return f'    <nav class="scrollspy" aria-label="Page sections">{links}</nav>'

def build_tech_pages():
    for i, t in enumerate(TECHS):
        s = t["slug"]; color = t["color"]; icon = TECH_ICON[s]
        uni = urllib.parse.quote(t["uni"])
        head = f'''    <div class="eyebrow">Explore by Sector · Technology</div>
    <h1 class="page-title">{t["name"]}</h1>
    <p class="page-lede">{t["desc"]}</p>
    {focus_chip(t["name"], icon, color)}'''
        # DS rule: a technology view re-themes the whole content accent to that
        # technology's fixed hue (sidebar/topbar stay the global amber chrome).
        accent_css = f'<style>.page{{--accent:{color};--accent-tint:{color}26}}</style>'
        spy = scrollspy([("sec-perception","01","Perception"),
                         ("sec-unicorn","02","Unicorn Factor"),
                         ("sec-research","03","Research")])
        perc = section("01", "Professionals&rsquo; Perception",
                       "How surveyed professionals read this technology across the ten industries.",
                       iframe(f"../embed/perception-foresight.html?embed=1&type=panel-tech&tech={s}", 1100),
                       sid="sec-perception")
        unic = section("02", "Unicorn Factor",
                       "The startup &amp; unicorn signal for this technology — clustering, founding wave and capital concentration.",
                       iframe(f"../embed/unicorn.html?tech={uni}", 1700), sid="sec-unicorn")
        res  = section("03", "Research &amp; Innovation",
                       "Publication and patent momentum behind this technology.",
                       iframe(f"../embed/research/{s}.html", 1700), sid="sec-research")
        body = "\n".join([head, spy, perc, unic, res])
        crumb = '<span>Technology</span><span class="sep">/</span><b>'+t["name"]+'</b>'
        wr(f"technology/{s}.html", shell("../", "technology", t["name"], crumb, body, head_extra=accent_css))

def build_industry_pages():
    for i, ind in enumerate(INDUSTRIES):
        s = ind["slug"]; icon = IND_ICON[s]; indus = urllib.parse.quote(ind["uni"])
        head = f'''    <div class="eyebrow">Explore by Sector · Industry</div>
    <h1 class="page-title">{ind["name"]}</h1>
    <p class="page-lede">{ind["desc"]}</p>
    {focus_chip(ind["name"], icon, "#f5a623")}'''
        spy = scrollspy([("sec-perception","01","Perception"),
                         ("sec-unicorn","02","Unicorn Factor")])
        perc = section("01", "Professionals&rsquo; Perception",
                       "How surveyed professionals read the five technologies within this industry.",
                       iframe(f"../embed/perception-foresight.html?embed=1&type=panel-indus&indus={s}", 1100),
                       sid="sec-perception")
        unic = section("02", "Unicorn Factor",
                       "The startup &amp; unicorn signal filtered to this industry.",
                       iframe(f"../embed/unicorn.html?indus={indus}", 1700), sid="sec-unicorn")
        body = "\n".join([head, spy, perc, unic])
        crumb = '<span>Industry</span><span class="sep">/</span><b>'+ind["name"]+'</b>'
        wr(f"industry/{s}.html", shell("../", "industry", ind["name"], crumb, body))

# ---- Technology × Industry landing (radar-first; sections reveal on select) -
def build_tech_x_industry():
    # radar selection keys -> our slugs
    radar_tech = {"Descriptive AI":"descriptive-ai","Agentic & GenAI":"generative-agentic-ai",
                  "Blockchain & Decentralized Systems":"blockchain","Physical AI & Robotics":"robotics",
                  "Quantum Computing":"quantum-computing"}
    radar_ind = {"Energy":"energy","Materials":"materials","Industrials":"industrials",
                 "Consumer Goods":"consumer-goods","Healthcare":"healthcare","Financial Services":"financial-services",
                 "Information technology":"information-technology","Communication & Creative Services":"communication-creative",
                 "Real Estate":"real-estate","Automotive & Transport":"automotive-transport"}
    import json
    techMap = json.dumps(radar_tech); indMap = json.dumps(radar_ind)
    uniTech = json.dumps({t["slug"]: t["uni"] for t in TECHS})
    uniInd  = json.dumps({i["slug"]: i["uni"] for i in INDUSTRIES})
    nameTech = json.dumps({t["slug"]: t["name"].replace("&amp;","&") for t in TECHS})
    nameInd  = json.dumps({i["slug"]: i["name"].replace("&amp;","&") for i in INDUSTRIES})

    spy = scrollspy([("sec-perception","01","Perception"),
                     ("sec-unicorn","02","Unicorn Factor"),
                     ("sec-research","03","Research")])
    perc = section("01","Professionals&rsquo; Perception",
                   'For the selected <b id="lblA">…</b> &times; <b id="lblB">…</b> intersection.',
                   '<div class="embed-wrap"><iframe id="frPerc" class="embed-frame" style="height:1000px" title="perception cell" scrolling="no" frameborder="0"></iframe></div>',
                   sid="sec-perception")
    unic = section("02","Unicorn Factor",
                   'The intersection, then the technology-level view beneath it.',
                   '<div class="embed-wrap"><iframe id="frUni" class="embed-frame" style="height:1700px" title="unicorn" scrolling="no" frameborder="0"></iframe></div>',
                   sid="sec-unicorn")
    res  = section("03","Research &amp; Innovation",
                   'Publication and patent momentum for the selected technology.',
                   '<div class="embed-wrap"><iframe id="frRes" class="embed-frame" style="height:1700px" title="research" scrolling="no" frameborder="0"></iframe></div>',
                   note="Research &amp; Innovation is measured at the <b>technology level only</b> — it is not specific to the chosen industry.",
                   sid="sec-research")
    body = f'''    <div class="eyebrow">Explore by Sector</div>
    <h1 class="page-title">Technology &times; Industry</h1>
    <p class="page-lede">Pick a technology and an industry in the heat-analysis radar below. Once both are set, the analysis for that intersection appears underneath — how professionals perceive it, where the ventures cluster, and the research signal behind the technology.</p>
    {iframe("../embed/radar.html", 880)}

    <div id="xsections" hidden>
{spy}
{perc}
{unic}
{res}
    </div>'''
    head_extra = """<style>
  #xsections[hidden]{display:none}
  #xsections{animation:xfade .5s ease}
  @keyframes xfade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
</style>"""
    script = f"""<script>
(function(){{
  var TMAP={techMap}, IMAP={indMap}, UTECH={uniTech}, UIND={uniInd}, NTECH={nameTech}, NIND={nameInd};
  var sec=document.getElementById('xsections');
  var fP=document.getElementById('frPerc'), fU=document.getElementById('frUni'), fR=document.getElementById('frRes');
  var cur={{t:null,i:null}};
  function apply(tKey,iKey){{
    var ts=TMAP[tKey], is=IMAP[iKey];
    if(!ts||!is) return;
    if(cur.t===ts && cur.i===is){{ sec.hidden=false; return; }}
    cur.t=ts; cur.i=is;
    document.getElementById('lblA').textContent=NTECH[ts]||tKey;
    document.getElementById('lblB').textContent=NIND[is]||iKey;
    fP.src='../embed/perception-foresight.html?embed=1&type=cell&tech='+ts+'&indus='+is;
    fU.src='../embed/unicorn.html?tech='+encodeURIComponent(UTECH[ts])+'&indus='+encodeURIComponent(UIND[is]);
    fR.src='../embed/research/'+ts+'.html';
    sec.hidden=false;
  }}
  window.addEventListener('message',function(e){{
    var d=e.data; if(!d||d.source!=='ddm-radar') return;
    if(d.tech && d.ind) apply(d.tech,d.ind);
    else sec.hidden=true;  // hide until both chosen again
  }});
}})();
</script>"""
    crumb = '<span>Explore</span><span class="sep">/</span><b>Technology &times; Industry</b>'
    wr("explore/tech-x-industry.html",
       shell("../", "tech-x-industry", "Technology &times; Industry", crumb, body,
             head_extra=head_extra).replace("</main>", "</main>\n"+script))

# ============================================================================
# PLACEHOLDER PAGES
# ============================================================================
PH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8v5l3 2"/><circle cx="12" cy="12" r="9"/></svg>'
def placeholder(root, active, title, crumb, heading, blurb):
    body = f'''    <div class="eyebrow">{crumb}</div>
    <h1 class="page-title">{heading}</h1>
    <div class="placeholder">
      <div class="ph-ic">{PH_ICON}</div>
      <span class="ph-tag">Coming soon</span>
      <h2>{heading}</h2>
      <p>{blurb}</p>
    </div>'''
    cr = f'<b>{heading}</b>'
    return shell(root, active, title, cr, body)

def build_placeholders():
    more = [
        ("about","About us","About the Digital Disruption Matrix and the team behind it."),
        ("methodology","Methodology","How the data was collected, weighted and indexed across sources."),
        ("faq","FAQ","Answers to the most common questions about the matrix and its data."),
        ("contact","Contact","Get in touch with the chair team."),
        ("acknowledgment","Acknowledgment","Credits and acknowledgments for partners and contributors."),
    ]
    for slug, head, blurb in more:
        wr(f"more/{slug}.html", placeholder("../", slug, head, "More", head,
            blurb + " This section is a placeholder for now."))
    tops = [
        ("key-findings","Key findings","The headline findings of the 2026 edition, distilled."),
        ("heatmatrix","Heatmatrix","The full technology × industry heat matrix at a glance."),
        ("download","Download the report","Download the complete Digital Disruption Matrix 2026 report."),
    ]
    for slug, head, blurb in tops:
        wr(f"{slug}.html", placeholder("", slug, head, "Digital Disruption Matrix 2026", head,
            blurb + " This section is a placeholder for now."))

# ============================================================================
def main():
    # embeds (re-themed sources)
    build_perception_embeds()
    build_unicorn_embed()
    build_radar_embed()
    build_research_embeds()
    build_selector_embed()
    # pages
    build_homepage()
    build_explore_selectors()
    build_data_pages()
    build_tech_pages()
    build_industry_pages()
    build_tech_x_industry()
    build_placeholders()
    print("\nDONE")

if __name__ == "__main__":
    main()
