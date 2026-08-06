#!/usr/bin/env python3
"""
Generates the animated SVG panels used by readme.md.

Everything here is plain SVG + CSS keyframes, which GitHub renders (and animates)
when the file is referenced with <img src="assets/....svg">. Tweak the palette or
copy below and re-run:  python3 assets/generate.py
"""

import os
import sys
import xml.etree.ElementTree as ET

OUT = os.path.dirname(os.path.abspath(__file__))

# `python3 assets/generate.py --static` emits the same panels with every entrance
# animation neutralised. Handy for verifying layout, and for anyone who'd rather
# ship a motion-free profile.
STATIC = "--static" in sys.argv

# ─────────────────────────────── design tokens ───────────────────────────────

BG        = "#0D1117"   # page / panel background
CARD      = "#161B22"   # raised card
CARD_ALT  = "#1C2128"   # inset / code window
LINE      = "#293138"   # borders
INK       = "#E6EDF3"   # primary text
INK_DIM   = "#9BA7B4"   # secondary text
INK_FAINT = "#6E7A87"   # tertiary text

A1 = "#667EEA"          # indigo
A2 = "#764BA2"          # violet
A3 = "#F093FB"          # fuchsia
A4 = "#FDA085"          # peach

FONT = "'Segoe UI',Roboto,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',ui-monospace,Consolas,'Liberation Mono',Menlo,monospace"

STATIC_CSS = "" if not STATIC else """
  .rise,.slide,.in,.bar,.caret,.blob,.blob2,.halo,.ping,.bob,.draw {
    animation:none !important; opacity:1 !important; transform:none !important;
    stroke-dashoffset:0 !important;
  }"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def write(name, body):
    body = body.strip() + "\n"
    # A malformed SVG renders as a broken-image icon on GitHub with no other
    # warning, so parse every file before it lands on disk.
    try:
        ET.fromstring(body)
    except ET.ParseError as e:
        raise SystemExit(f"✗ {name} is not valid XML: {e}")
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"  ✓ {name}  ({os.path.getsize(path) / 1024:.1f} KB)")


def svg(w, h, body, extra_defs="", rounded=0):
    """Wrap body in a root <svg> carrying the shared defs + animation library.

    `rounded` clips the panel to a rounded rectangle and strokes a border, so the
    corners stay transparent and the panel reads as a card on light *and* dark
    GitHub themes (stacked images always get a few px of line-height between
    them, so panels can never truly butt together).
    """
    if rounded:
        extra_defs = (f'<clipPath id="shell"><rect width="{w}" height="{h}" rx="{rounded}"/>'
                      f'</clipPath>') + extra_defs
        body = (f'<g clip-path="url(#shell)">{body}</g>'
                f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{rounded}" '
                f'fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" fill="none" role="img">
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{A1}"/><stop offset=".45" stop-color="{A2}"/>
    <stop offset=".8" stop-color="{A3}"/><stop offset="1" stop-color="{A4}"/>
  </linearGradient>
  <linearGradient id="accentV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A3}"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A1}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
    <path d="M34 0H0v34" stroke="#FFFFFF" stroke-opacity=".028" stroke-width="1"/>
  </pattern>
  <filter id="blur" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="58"/>
  </filter>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="5" stdDeviation="9" flood-color="#000" flood-opacity=".42"/>
  </filter>
{extra_defs}
</defs>
<style>
  text {{ font-family:{FONT}; }}
  .mono {{ font-family:{MONO}; }}
  @keyframes rise   {{ from {{ opacity:0; transform:translateY(16px); }} to {{ opacity:1; transform:translateY(0); }} }}
  @keyframes slideL {{ from {{ opacity:0; transform:translateX(-22px); }} to {{ opacity:1; transform:translateX(0); }} }}
  @keyframes fade   {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
  @keyframes grow   {{ from {{ transform:scaleX(0); }} to {{ transform:scaleX(1); }} }}
  @keyframes blink  {{ 0%,45% {{ opacity:1; }} 55%,100% {{ opacity:0; }} }}
  @keyframes drift  {{ 0%,100% {{ transform:translate(0,0) scale(1); }} 50% {{ transform:translate(46px,-30px) scale(1.16); }} }}
  @keyframes drift2 {{ 0%,100% {{ transform:translate(0,0) scale(1.1); }} 50% {{ transform:translate(-52px,26px) scale(.9); }} }}
  @keyframes halo   {{ 0%,100% {{ opacity:.34; }} 50% {{ opacity:.8; }} }}
  @keyframes ping   {{ 0% {{ transform:scale(.7); opacity:.85; }} 100% {{ transform:scale(2.6); opacity:0; }} }}
  @keyframes bob    {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(7px); }} }}
  @keyframes draw   {{ from {{ stroke-dashoffset:var(--len); }} to {{ stroke-dashoffset:0; }} }}
  @keyframes sweep  {{ 0% {{ transform:translateX(-100%); }} 100% {{ transform:translateX(100%); }} }}
  .rise  {{ animation:rise .85s cubic-bezier(.22,1,.36,1) both; }}
  .slide {{ animation:slideL .85s cubic-bezier(.22,1,.36,1) both; }}
  .in    {{ animation:fade 1s ease both; }}
  .bar   {{ transform-box:fill-box; transform-origin:left center;
            animation:grow 1.15s cubic-bezier(.22,1,.36,1) both; }}
  .caret {{ animation:blink 1.1s steps(1) infinite; }}
  .blob  {{ transform-box:fill-box; transform-origin:center;
            animation:drift 17s ease-in-out infinite; }}
  .blob2 {{ transform-box:fill-box; transform-origin:center;
            animation:drift2 21s ease-in-out infinite; }}
  .halo  {{ animation:halo 4.5s ease-in-out infinite; }}
  .ping  {{ transform-box:fill-box; transform-origin:center;
            animation:ping 2.6s ease-out infinite; }}
  .bob   {{ animation:bob 2.1s ease-in-out infinite; }}
  .draw  {{ stroke-dasharray:var(--len); animation:draw 1.9s ease-out .25s both; }}
  @media (prefers-reduced-motion:reduce) {{
    .rise,.slide,.in,.bar,.caret,.blob,.blob2,.halo,.ping,.bob,.draw {{
      animation:none !important; opacity:1 !important; transform:none !important;
      stroke-dashoffset:0 !important;
    }}
  }}
{STATIC_CSS}
</style>
{body}
</svg>"""


def panel(x, y, w, h, r=16, fill=CARD, stroke=LINE, sw=1):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def backdrop(w, h, blobs=True):
    out = [f'<rect width="{w}" height="{h}" fill="{BG}"/>',
           f'<rect width="{w}" height="{h}" fill="url(#grid)"/>']
    if blobs:
        out += [
            f'<g filter="url(#blur)" opacity=".3">',
            f'<circle class="blob" cx="{int(w*0.14)}" cy="{int(h*0.2)}" r="{int(h*0.42)}" fill="{A1}"/>',
            f'<circle class="blob2" cx="{int(w*0.82)}" cy="{int(h*0.78)}" r="{int(h*0.38)}" fill="{A3}"/>',
            f'<circle class="blob" cx="{int(w*0.55)}" cy="{int(h*0.1)}" r="{int(h*0.3)}" fill="{A2}"/>',
            f'</g>',
        ]
    return "".join(out)


def chip(x, y, label, w=None, pad=15, fs=12, fill="#FFFFFF", op=".07",
         stroke=None, color=INK_DIM, h=27, weight="600"):
    """Small rounded tag. Width auto-estimated from the label length."""
    w = w if w else int(len(label) * fs * 0.60) + pad * 2
    s = f'stroke="{stroke}" stroke-width="1"' if stroke else ""
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h//2}" fill="{fill}" '
            f'fill-opacity="{op}" {s}/>'
            f'<text x="{x + w/2}" y="{y + h/2 + fs*0.36}" font-size="{fs}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="middle">{esc(label)}</text></g>'), w


# ───────────────────────────────── 1. hero ──────────────────────────────────

def hero():
    W, H = 1200, 452
    b = [backdrop(W, H)]

    # top hairline + faux browser chrome so the panel reads as a page header
    b.append(f'<rect width="{W}" height="3" fill="url(#accent)"/>')

    b.append('<g class="rise" style="animation-delay:.05s">')
    b.append(f'<rect x="72" y="74" width="9" height="9" rx="4.5" fill="{A3}" class="halo"/>')
    b.append(f'<text x="94" y="83" font-size="13" font-weight="700" letter-spacing="2.6" '
             f'fill="{INK_DIM}">SR. FULL STACK ENGINEER</text>')
    b.append('</g>')

    b.append('<g class="rise" style="animation-delay:.18s">')
    b.append(f'<text x="70" y="184" font-size="86" font-weight="800" letter-spacing="-2.6" '
             f'fill="{INK}">Muhammad <tspan fill="url(#accent)">Haris</tspan></text>')
    b.append('</g>')

    b.append('<g class="rise" style="animation-delay:.3s">')
    b.append(f'<text x="72" y="232" class="mono" font-size="19" fill="{INK_DIM}">'
             f'<tspan fill="{A3}">&gt;</tspan> building scalable web, mobile &amp; desktop products'
             f'<tspan class="caret" fill="{A4}">_</tspan></text>')
    b.append('</g>')

    b.append('<g class="rise" style="animation-delay:.42s">')
    b.append(f'<text x="72" y="284" font-size="16.5" fill="{INK_FAINT}">'
             f'4+ years turning complex requirements into products people actually ship on. '
             f'Healthcare, FinTech, E-Commerce, AI &amp; EdTech.</text>')
    b.append('</g>')

    # stat strip
    stats = [("4+", "YEARS"), ("20+", "APPS SHIPPED"), ("10+", "INTEGRATIONS"), ("4", "COMPANIES")]
    x = 72
    b.append('<g class="rise" style="animation-delay:.56s">')
    for i, (big, small) in enumerate(stats):
        b.append(f'<text x="{x}" y="352" font-size="34" font-weight="800" fill="url(#accentV)">{big}</text>')
        b.append(f'<text x="{x}" y="374" font-size="10.5" font-weight="700" letter-spacing="1.7" '
                 f'fill="{INK_FAINT}">{small}</text>')
        if i < len(stats) - 1:
            b.append(f'<rect x="{x + 148}" y="326" width="1" height="52" fill="{LINE}"/>')
        x += 190
    b.append('</g>')

    # call-to-action buttons (decorative here — the real links sit under the image)
    b.append('<g class="rise" style="animation-delay:.68s">')
    b.append(f'<rect x="72" y="404" width="150" height="34" rx="17" fill="url(#accent)"/>')
    b.append(f'<text x="147" y="426" font-size="13.5" font-weight="700" fill="#0D1117" '
             f'text-anchor="middle">View my work ↓</text>')
    b.append(f'<rect x="234" y="404" width="132" height="34" rx="17" fill="none" '
             f'stroke="{LINE}" stroke-width="1.4"/>')
    b.append(f'<text x="300" y="426" font-size="13.5" font-weight="600" fill="{INK_DIM}" '
             f'text-anchor="middle">Get in touch</text>')
    b.append('</g>')

    # decorative orbit on the right
    b.append('<g class="in" style="animation-delay:.7s" opacity=".9">')
    cx, cy = 1002, 214
    for i, r in enumerate((70, 108, 146)):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="#48505A" stroke-width="1.2" '
                 f'stroke-dasharray="4 8" opacity="{0.95 - i*0.18:.2f}"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="url(#accentV)" opacity=".16"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="44" stroke="{A1}" stroke-width="1.4" opacity=".55"/>')
    b.append(f'<text x="{cx}" y="{cy + 9}" class="mono" font-size="25" font-weight="700" '
             f'fill="{INK}" text-anchor="middle">&lt;/&gt;</text>')
    for r, col, dur in ((70, A1, "9s"), (108, A3, "15s"), (146, A4, "22s")):
        b.append(f'<g transform="translate({cx},{cy})">'
                 f'<circle r="5.5" fill="{col}">'
                 f'<animateMotion dur="{dur}" repeatCount="indefinite" '
                 f'path="M {r} 0 A {r} {r} 0 1 1 {-r} 0 A {r} {r} 0 1 1 {r} 0"/>'
                 f'</circle></g>')
    b.append('</g>')
    return svg(W, H, "".join(b), rounded=20)


# ────────────────────────── 2. section headings ─────────────────────────────

HEADER_H = 104   # vertical space a baked-in section heading occupies


def header_frag(kicker, title, color):
    """The section heading, drawn in the top HEADER_H px of a 1200-wide panel."""
    b = ['<g class="slide">']
    b.append(f'<rect x="70" y="30" width="3" height="52" rx="1.5" fill="url(#accentV)"/>')
    b.append(f'<text x="90" y="49" font-size="11.5" font-weight="700" letter-spacing="2.4" '
             f'fill="{INK_FAINT}">{esc(kicker)}</text>')
    b.append(f'<text x="89" y="80" font-size="34" font-weight="800" letter-spacing="-.8" '
             f'fill="{INK}">{esc(title)}</text>')
    b.append('</g>')
    w = int(len(title) * 19) + 40
    b.append(f'<rect x="{89 + w}" y="67" width="{max(60, 1040 - w)}" height="1" fill="url(#fade)" '
             f'class="bar" style="animation-delay:.5s"/>')
    b.append(f'<circle cx="1116" cy="56" r="4" fill="{color}" class="halo"/>')
    b.append(f'<circle cx="1116" cy="56" r="4" fill="{color}" class="ping"/>')
    return "".join(b)


def with_header(w, h, body, kicker, title, color, blobs=True):
    """Stack a section heading on top of an existing panel body."""
    H = h + HEADER_H
    out = [backdrop(w, H, blobs=blobs),
           header_frag(kicker, title, color),
           f'<g transform="translate(0,{HEADER_H})">{body}</g>']
    return svg(w, H, "".join(out), rounded=20)


def section(name, kicker, title, color):
    """Standalone heading, for the sections whose content isn't one of my SVGs."""
    W = 1200
    b = [backdrop(W, HEADER_H, blobs=False), header_frag(kicker, title, color)]
    write(f"sec-{name}.svg", svg(W, HEADER_H, "".join(b), rounded=20))


# ─────────────────────────────── 3. about ───────────────────────────────────

def about():
    W, H = 1200, 546
    b = [f'<g filter="url(#blur)" opacity=".26">'
         f'<circle class="blob2" cx="1080" cy="120" r="190" fill="{A2}"/></g>']

    # ── left: code window ──
    b.append('<g class="rise" style="animation-delay:.1s" filter="url(#soft)">')
    b.append(panel(70, 34, 610, 350, r=14, fill=CARD_ALT))
    b.append(f'<path d="M70 48a14 14 0 0 1 14-14h582a14 14 0 0 1 14 14v30H70z" fill="#22272E"/>')
    b.append(f'<line x1="70" y1="78" x2="680" y2="78" stroke="{LINE}"/>')
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b.append(f'<circle cx="{92 + i*19}" cy="56" r="5.5" fill="{c}"/>')
    b.append(f'<text x="375" y="61" class="mono" font-size="12" fill="{INK_FAINT}" '
             f'text-anchor="middle">haris.ts</text>')
    b.append('</g>')

    K, S, V, P, C = "#FF7B72", "#A5D6FF", "#79C0FF", "#D2A8FF", "#8B949E"
    code = [
        [("const", K), (" haris", V), (": ", C), ("Engineer", P), (" = {", C)],
        [("  role", V), (":       ", C), ('"Sr. Full Stack Engineer"', S), (",", C)],
        [("  based", V), (":      ", C), ('"Pakistan · remote-friendly"', S), (",", C)],
        [("  degree", V), (":     ", C), ('"BS Computer Science, UMT"', S), (",", C)],
        [("", C)],
        [("  builds", V), (": {", C)],
        [("    web", V), (":     [", C), ('"React"', S), (", ", C), ('"Next.js"', S), (", ", C), ('"TypeScript"', S), ("],", C)],
        [("    mobile", V), (":  [", C), ('"Ionic"', S), (", ", C), ('"Capacitor"', S), ("],", C)],
        [("    desktop", V), (": [", C), ('"Electron"', S), ("],", C)],
        [("    api", V), (":     [", C), ('"NestJS"', S), (", ", C), ('"Express"', S), (", ", C), ('"Redis"', S), ("],", C)],
        [("    cloud", V), (":   [", C), ('"AWS"', S), (", ", C), ('"Docker"', S), (", ", C), ('"Jenkins"', S), ("],", C)],
        [("  },", C)],
        [("", C)],
        [("  shipsOnTime", V), (": ", C), ("true", K), (",", C)],
        [("};", C)],
    ]
    y = 106
    for n, line in enumerate(code):
        b.append(f'<g class="in" style="animation-delay:{0.3 + n*0.055:.2f}s">')
        b.append(f'<text x="96" y="{y}" class="mono" font-size="11" fill="#484F58" '
                 f'text-anchor="end">{n+1}</text>')
        parts = "".join(f'<tspan fill="{col}" xml:space="preserve">{esc(t)}</tspan>'
                        for t, col in line)
        b.append(f'<text x="112" y="{y}" class="mono" font-size="13">{parts}</text>')
        b.append('</g>')
        y += 18

    # ── right: highlight cards ──
    cards = [
        ("🏗️", "I build end-to-end", "Frontend, backend, mobile, desktop — and the\npipeline that ships it. No handoff gaps.", A1),
        ("🔌", "I make systems talk", "10+ third-party integrations: payments,\naccounting, shipping, AI, maps.", A3),
        ("🔍", "I raise the bar", "Lead code reviews, refactor tangled logic\nand tune performance until it's fast.", A4),
    ]
    cy = 34
    for i, (icon, title, desc, col) in enumerate(cards):
        b.append(f'<g class="rise" style="animation-delay:{0.34 + i*0.12:.2f}s">')
        b.append(panel(706, cy, 424, 106, r=14))
        b.append(f'<rect x="706" y="{cy}" width="3.5" height="106" rx="2" fill="{col}"/>')
        b.append(f'<rect x="726" y="{cy+22}" width="36" height="36" rx="10" fill="{col}" fill-opacity=".14"/>')
        b.append(f'<text x="744" y="{cy+46}" font-size="18" text-anchor="middle">{icon}</text>')
        b.append(f'<text x="776" y="{cy+36}" font-size="16" font-weight="700" fill="{INK}">{esc(title)}</text>')
        for j, ln in enumerate(desc.split("\n")):
            b.append(f'<text x="776" y="{cy+58+j*17}" font-size="12.5" fill="{INK_FAINT}">{esc(ln)}</text>')
        b.append('</g>')
        cy += 122

    # ── bottom: domain tags ──
    b.append('<g class="rise" style="animation-delay:.8s">')
    b.append(f'<text x="72" y="424" font-size="11.5" font-weight="700" letter-spacing="2.2" '
             f'fill="{INK_FAINT}">DOMAINS I\'VE SHIPPED IN</text>')
    x = 70
    for label, col in (("🏥 Healthcare", A1), ("💳 FinTech", A2), ("🛒 E-Commerce", A3),
                       ("🤖 Artificial Intelligence", A4), ("🎓 EdTech", A1),
                       ("🚚 Logistics", A2), ("🏘️ Rentals", A3)):
        g, w = chip(x, 444, label, fs=13, h=33, pad=17, fill=col, op=".1",
                    stroke=col + "55", color=INK)
        b.append(g)
        x += w + 10
    b.append('</g>')

    b.append('<g class="rise" style="animation-delay:.9s">')
    b.append(f'<rect x="70" y="500" width="1060" height="1" fill="{LINE}"/>')
    b.append(f'<text x="70" y="528" font-size="13.5" font-style="italic" fill="{INK_DIM}">'
             f'“High-quality, maintainable code — delivered on deadline.”</text>')
    b.append('</g>')
    return with_header(W, H, "".join(b), "01 — WHO I AM", "About me", A1, blobs=False)


# ──────────────────────────────── 4. skills ─────────────────────────────────

def skills():
    rows = [
        ("React / Next.js",            100, "Ant Design · MUI · Redux · Tailwind · RHF"),
        ("TypeScript / JavaScript",    100, "Strict typing, shared contracts, monorepos"),
        ("Node.js / NestJS / Express",  92, "REST, WebSockets, Firebase Functions, Redis"),
        ("Ionic / Capacitor",           90, "~15 cross-platform apps shipped to stores"),
        ("SQL / NoSQL + ORMs",          84, "Postgres · MySQL · Mongo · Sequelize/TypeORM/Drizzle"),
        ("AWS / Docker / CI-CD",        76, "EC2 · S3 · Nginx · Jenkins · GitHub Actions"),
        ("Electron",                    74, "3+ desktop apps, offline-first, auto-update"),
    ]
    W = 1200
    H = 116 + len(rows) * 62
    b = [backdrop(W, H, blobs=False)]
    b.append(f'<g filter="url(#blur)" opacity=".22">'
             f'<circle class="blob" cx="140" cy="{H-60}" r="200" fill="{A1}"/></g>')
    b.append(panel(70, 30, 1060, H - 60, r=18))

    b.append(f'<text x="102" y="70" font-size="17" font-weight="700" fill="{INK}">'
             f'Where I&#39;m strongest</text>')
    b.append(f'<text x="1098" y="70" font-size="12" fill="{INK_FAINT}" text-anchor="end">'
             f'self-assessed · depth of production use</text>')
    b.append(f'<rect x="102" y="88" width="996" height="1" fill="{LINE}"/>')

    y = 122
    track_x, track_w = 470, 500
    for i, (label, pct, note) in enumerate(rows):
        d = 0.25 + i * 0.11
        b.append(f'<g class="in" style="animation-delay:{d:.2f}s">')
        b.append(f'<text x="102" y="{y+5}" font-size="14.5" font-weight="650" fill="{INK}">{esc(label)}</text>')
        b.append(f'<text x="102" y="{y+24}" font-size="11.5" fill="{INK_FAINT}">{esc(note)}</text>')
        b.append(f'<rect x="{track_x}" y="{y-6}" width="{track_w}" height="10" rx="5" '
                 f'fill="#FFFFFF" fill-opacity=".055"/>')
        fw = int(track_w * pct / 100)
        b.append(f'<rect x="{track_x}" y="{y-6}" width="{fw}" height="10" rx="5" fill="url(#accent)" '
                 f'class="bar" style="animation-delay:{d+0.1:.2f}s"/>')
        b.append(f'<circle cx="{track_x+fw}" cy="{y-1}" r="7" fill="{A3}" opacity=".35" '
                 f'class="ping" style="animation-delay:{d+1:.2f}s"/>')
        b.append(f'<text x="1098" y="{y+3}" class="mono" font-size="13" font-weight="700" '
                 f'fill="{INK_DIM}" text-anchor="end">{pct}%</text>')
        b.append('</g>')
        y += 62
    return svg(W, H, "".join(b), rounded=20)


# ─────────────────────────────── 5. projects ────────────────────────────────

def projects():
    items = [
        ("🎓", "University LMS", "KEAN University · Septems Systems", A1,
         ["Spearheaded a fully customized Learning",
          "Management System — courses, enrolment,",
          "assessments and reporting, from scratch."],
         ["Next.js", "NestJS", "Postgres"]),
        ("🏥", "Veterinary Oncology Platform", "Vet Oncology Partners · Septems", A3,
         ["Designed the system for a clinical platform",
          "handling patient records and treatment",
          "workflows in a regulated domain."],
         ["React", "Node.js", "AWS"]),
        ("🤖", "AI-Powered Products", "Multiple clients · Septems & Binary Bursts", A4,
         ["Shipped OpenAI-backed assistants, generation",
          "and automation flows wired into real",
          "production workloads."],
         ["OpenAI", "NestJS", "Redis"]),
        ("🖥️", "Desktop Suite", "3+ apps · Binary Bursts", A2,
         ["Cross-platform desktop apps with native-feeling",
          "UX, auto-update and offline-first data",
          "handling."],
         ["Electron", "React", "SQLite"]),
        ("📱", "~15 Mobile Applications", "NOWASYS Services", A1,
         ["Expanded the company's entire mobile offering —",
          "a fleet of cross-platform apps from a single",
          "React + Ionic codebase."],
         ["Ionic", "Capacitor", "Appwrite"]),
        ("🧭", "YOURGUIDE Platform", "Startup · sole full stack developer", A3,
         ["Took a startup platform from empty repo to",
          "launch, solo — frontend, backend, DB design,",
          "caching and performance tuning."],
         ["Next.js", "Express", "Sequelize"]),
    ]
    # two columns inside the 70…1130 content area
    W, CW, CH, GAP = 1200, 516, 232, 28
    rows = (len(items) + 1) // 2
    H = 56 + rows * (CH + GAP)
    b = [f'<g filter="url(#blur)" opacity=".22">'
         f'<circle class="blob" cx="1060" cy="90" r="210" fill="{A3}"/>'
         f'<circle class="blob2" cx="120" cy="{H-90}" r="200" fill="{A1}"/></g>']

    for i, (icon, title, org, col, lines, tags) in enumerate(items):
        cx = 70 + (i % 2) * (CW + GAP)
        cy = 28 + (i // 2) * (CH + GAP)
        b.append(f'<g class="rise" style="animation-delay:{0.1 + i*0.09:.2f}s" filter="url(#soft)">')
        b.append(panel(cx, cy, CW, CH, r=16))
        # gradient top edge, like a hovered card
        b.append(f'<path d="M{cx} {cy+16}a16 16 0 0 1 16-16h{CW-32}a16 16 0 0 1 16 16v2H{cx}z" '
                 f'fill="url(#accent)"/>')
        b.append(f'<rect x="{cx+26}" y="{cy+26}" width="44" height="44" rx="12" '
                 f'fill="{col}" fill-opacity=".14"/>')
        b.append(f'<text x="{cx+48}" y="{cy+55}" font-size="21" text-anchor="middle">{icon}</text>')
        b.append(f'<text x="{cx+84}" y="{cy+45}" font-size="17.5" font-weight="750" fill="{INK}">'
                 f'{esc(title)}</text>')
        b.append(f'<text x="{cx+84}" y="{cy+64}" font-size="11.5" font-weight="600" '
                 f'letter-spacing=".3" fill="{col}">{esc(org)}</text>')
        for j, ln in enumerate(lines):
            b.append(f'<text x="{cx+26}" y="{cy+100+j*18}" font-size="12.8" fill="{INK_DIM}">'
                     f'{esc(ln)}</text>')
        tx = cx + 26
        for t in tags:
            g, w = chip(tx, cy + 172, t, fs=11.5, h=26, pad=13, fill="#FFFFFF", op=".06",
                        stroke=LINE, color=INK_DIM)
            b.append(g)
            tx += w + 8
        b.append(f'<text x="{cx+CW-26}" y="{cy+CH-22}" font-size="12" font-weight="700" '
                 f'fill="{col}" text-anchor="end">production ●</text>')
        b.append('</g>')
    return with_header(W, H, "".join(b), "03 — WHAT I'VE MADE", "Selected work", A3, blobs=False)


# ─────────────────────────────── 6. timeline ────────────────────────────────

def timeline():
    stops = [
        ("Aug 2021 — Aug 2022", "YOURGUIDE", "Full Stack Developer", A1,
         ["Sole full stack dev — took the startup",
          "platform from empty repo to launch.",
          "React/Next + Express + Sequelize."]),
        ("Aug 2022 — Aug 2023", "NOWASYS Services", "Software Engineer", A2,
         ["~15 mobile apps with React + Ionic,",
          "expanding the company's whole mobile",
          "offering. Appwrite + Next.js."]),
        ("Aug 2023 — Aug 2025", "Binary Bursts", "Full Software Engineer", A3,
         ["4+ products across rentals, AI and",
          "desktop. 10+ integrations, 3+ Electron",
          "apps, AWS + Jenkins CI/CD."]),
        ("Aug 2025 — Present", "Septems Systems", "Full Software Engineer", A4,
         ["KEAN University LMS + veterinary",
          "oncology platform. 3+ new products",
          "in healthcare, AI and desktop."]),
    ]
    W, H = 1200, 486
    b = [f'<g filter="url(#blur)" opacity=".18">'
         f'<circle class="blob" cx="600" cy="240" r="230" fill="{A2}"/></g>']

    b.append(f'<text x="70" y="52" font-size="16.5" font-weight="700" fill="{INK}">'
             f'4+ years · 4 teams · 20+ products</text>')
    b.append(f'<text x="1130" y="52" font-size="12" fill="{INK_FAINT}" text-anchor="end">'
             f'2021 → today</text>')

    # 4 cards of CARD_W centred in the 70…1130 content area
    CARD_W = 248
    rail_y = 132
    x0 = 70 + CARD_W // 2
    step = (1060 - CARD_W) // (len(stops) - 1)
    b.append(f'<rect x="70" y="{rail_y-1}" width="1060" height="2" rx="1" fill="{LINE}"/>')
    b.append(f'<rect x="70" y="{rail_y-1.5}" width="1060" height="3" rx="1.5" fill="url(#accent)" '
             f'class="bar" style="animation-delay:.2s"/>')

    for i, (period, org, role, col, lines) in enumerate(stops):
        cx = x0 + i * step
        d = 0.35 + i * 0.14
        b.append(f'<g class="rise" style="animation-delay:{d:.2f}s">')
        # node
        b.append(f'<circle cx="{cx}" cy="{rail_y}" r="9" fill="{col}" opacity=".3" class="ping" '
                 f'style="animation-delay:{d+0.8:.2f}s"/>')
        b.append(f'<circle cx="{cx}" cy="{rail_y}" r="8.5" fill="{BG}" stroke="{col}" stroke-width="3"/>')
        b.append(f'<circle cx="{cx}" cy="{rail_y}" r="3" fill="{col}"/>')
        b.append(f'<text x="{cx}" y="{rail_y-26}" font-size="11.5" font-weight="700" '
                 f'letter-spacing=".6" fill="{INK_FAINT}" text-anchor="middle">{esc(period)}</text>')
        # connector down to card
        b.append(f'<line x1="{cx}" y1="{rail_y+12}" x2="{cx}" y2="{rail_y+42}" stroke="{col}" '
                 f'stroke-width="1.5" stroke-dasharray="3 4" opacity=".7"/>')
        # card
        b.append(f'<g filter="url(#soft)">')
        b.append(panel(cx - CARD_W // 2, rail_y + 42, CARD_W, 194, r=14))
        b.append(f'<rect x="{cx - CARD_W // 2}" y="{rail_y+42}" width="{CARD_W}" height="3" '
                 f'rx="1.5" fill="{col}"/>')
        b.append('</g>')
        b.append(f'<text x="{cx-100}" y="{rail_y+82}" font-size="16.5" font-weight="750" '
                 f'fill="{INK}">{esc(org)}</text>')
        b.append(f'<text x="{cx-100}" y="{rail_y+102}" font-size="12" font-weight="600" '
                 f'fill="{col}">{esc(role)}</text>')
        b.append(f'<rect x="{cx-100}" y="{rail_y+114}" width="200" height="1" fill="{LINE}"/>')
        for j, ln in enumerate(lines):
            b.append(f'<text x="{cx-100}" y="{rail_y+136+j*17}" font-size="12" fill="{INK_DIM}">'
                     f'{esc(ln)}</text>')
        b.append('</g>')

    b.append(f'<g class="in" style="animation-delay:1s">')
    b.append(f'<rect x="70" y="436" width="1060" height="1" fill="{LINE}"/>')
    b.append(f'<text x="70" y="466" font-size="13" fill="{INK_FAINT}">🎓 '
             f'<tspan font-weight="700" fill="{INK_DIM}">BS Computer Science</tspan>'
             f' — University of Management &amp; Technology (UMT)</text>')
    b.append(f'<text x="1130" y="466" font-size="12.5" font-weight="600" fill="{A3}" '
             f'text-anchor="end">open to new opportunities ●</text>')
    b.append('</g>')
    return with_header(W, H, "".join(b), "04 — WHERE I'VE BEEN", "Career journey", A4, blobs=False)


# ──────────────────────────── 7. contact panel ──────────────────────────────

def contact():
    W, H = 1200, 244
    b = []
    b.append(f'<text x="600" y="76" font-size="30" font-weight="800" letter-spacing="-.6" '
             f'fill="{INK}" text-anchor="middle" class="rise">Let&#39;s build something '
             f'<tspan fill="url(#accent)">great</tspan>.</text>')
    b.append(f'<text x="600" y="110" font-size="14.5" fill="{INK_DIM}" text-anchor="middle" '
             f'class="rise" style="animation-delay:.12s">Got an idea that needs building, or a team '
             f'that needs a full stack engineer? My inbox is open.</text>')
    b.append('<g class="rise" style="animation-delay:.24s">')
    b.append(f'<rect x="446" y="142" width="308" height="1" fill="url(#fade)"/>')
    b.append(f'<text x="600" y="176" class="mono" font-size="14" fill="{A3}" text-anchor="middle">'
             f'iammuhammadharis9@gmail.com</text>')
    b.append(f'<text x="600" y="206" font-size="12" fill="{INK_FAINT}" text-anchor="middle">'
             f'Usually replies within a day · Remote-friendly · Available for collaboration</text>')
    b.append('</g>')
    b.append(f'<path d="M592 226l8 9 8-9" stroke="{INK_FAINT}" stroke-width="2" '
             f'stroke-linecap="round" fill="none" class="bob"/>')
    return with_header(W, H, "".join(b), "06 — SAY HELLO", "Get in touch", A3)


# ──────────────────────────────── 8. footer ─────────────────────────────────

def footer():
    W, H = 1200, 132
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity=".5"/>',
         f'<g filter="url(#blur)" opacity=".4">'
         f'<circle class="blob" cx="300" cy="150" r="150" fill="{A1}"/>'
         f'<circle class="blob2" cx="900" cy="150" r="150" fill="{A3}"/></g>',
         f'<rect y="0" width="{W}" height="2" fill="url(#accent)"/>']
    b.append(f'<text x="600" y="52" font-size="17" font-weight="700" fill="{INK}" '
             f'text-anchor="middle" class="rise">Thanks for scrolling all the way down 👋</text>')
    b.append(f'<text x="600" y="78" class="mono in" font-size="12.5" fill="{INK_FAINT}" '
             f'text-anchor="middle">'
             f'built by Muhammad Haris · hand-rolled SVG, no page builder</text>')
    b.append(f'<text x="600" y="106" font-size="12" fill="{INK_FAINT}" text-anchor="middle">'
             f'⭐ Star a repo if it helped you</text>')
    return svg(W, H, "".join(b), rounded=20)


# ─────────────────────────── 9. bits and pieces ─────────────────────────────

def divider():
    # transparent background so the strip works on either GitHub theme
    W, H = 1200, 10
    b = [f'<rect x="0" y="4" width="{W}" height="1.5" fill="{LINE}" opacity=".8"/>']
    b.append(f'<g><rect x="0" y="3.5" width="260" height="3" rx="1.5" fill="url(#accent)" '
             f'opacity=".9"><animate attributeName="x" values="-260;1200" dur="4.5s" '
             f'repeatCount="indefinite"/></rect></g>')
    return svg(W, H, "".join(b))


def button(name, label, w, primary=False):
    """Small pill rendered as its own file so it can be wrapped in a link.

    Background stays transparent — these sit directly on the GitHub page, not on
    one of my dark panels.
    """
    H = 46
    b = []
    if primary:
        b.append(f'<rect x="1" y="4" width="{w-2}" height="{H-8}" rx="19" fill="url(#accent)"/>')
        fill = "#0D1117"
    else:
        b.append(f'<rect x="1" y="4" width="{w-2}" height="{H-8}" rx="19" fill="{CARD}" '
                 f'stroke="{LINE}" stroke-width="1.4"/>')
        fill = INK
    b.append(f'<text x="{w/2}" y="{H/2 + 5}" font-size="14" font-weight="700" fill="{fill}" '
             f'text-anchor="middle">{esc(label)}</text>')
    write(name, svg(w, H, "".join(b)))


def navitem(name, label, w):
    H = 42
    b = [f'<rect x="1" y="4" width="{w-2}" height="{H-8}" rx="9" fill="{CARD}" '
         f'stroke="{LINE}" stroke-width="1"/>',
         f'<text x="{w/2}" y="{H/2 + 5}" font-size="13.5" font-weight="650" fill="{INK_DIM}" '
         f'text-anchor="middle">{esc(label)}</text>']
    write(name, svg(w, H, "".join(b)))


# ──────────────────────────────── build ─────────────────────────────────────

if __name__ == "__main__":
    print("building assets/")
    write("hero.svg", hero())
    write("about.svg", about())
    write("skills.svg", skills())
    write("projects.svg", projects())
    write("timeline.svg", timeline())
    write("contact.svg", contact())
    write("footer.svg", footer())
    write("divider.svg", divider())

    # about / work / journey / contact carry their heading inside the panel;
    # these two sections have non-SVG content, so their heading stands alone.
    section("stack", "02 — WHAT I USE",  "Tech arsenal",    A2)
    section("stats", "05 — THE NUMBERS", "GitHub activity", A1)

    for slug, label, w in (("about", "About", 104), ("stack", "Stack", 100),
                           ("work", "Work", 94), ("journey", "Journey", 116),
                           ("stats", "Stats", 100), ("contact", "Contact", 116)):
        navitem(f"nav-{slug}.svg", label, w)

    button("btn-linkedin.svg", "LinkedIn  ↗", 168, primary=True)
    button("btn-email.svg",    "Email me  ✉", 156)
    button("btn-github.svg",   "Follow  ★",   142)
    print("done.")
