"""'Many tools. One calm workflow.' section: floating tool icons with badges and curves (light + dark)."""
import base64, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
TH = {
    "light": dict(top="#ffffff", bg="#ffffff", ink="#141414", muted="#3a3a3a", line="#141414", sh=".18",
                  chip="#ffffff", chipt="#141414"),
    "dark": dict(top="#0d1117", bg="#0d1117", ink="#e6edf3", muted="#c9d1d9", line="#e6edf3", sh=".6",
                 chip="#161b22", chipt="#e6edf3"),
}
W, H = 1000, 700
RED = "#e5484d"

# icon file, x, y, size, tilt, badge text, badge style ("red", "chip", "dot")
ICONS = [
    ("Github-Dark", 300, 70, 66, -6, "99+", "red"),
    ("Figma-Dark", 52, 248, 60, -4, "", "dot"),
    ("React-Dark", 620, 120, 62, 7, "v19", "red"),
    ("Docker", 860, 150, 64, -5, "Up", "chip"),
    ("Python-Dark", 892, 390, 62, 6, "3.12", "chip"),
    ("Spring-Dark", 262, 560, 58, -8, "200 OK", "chip"),
    ("PyTorch-Dark", 596, 520, 64, 4, "train", "red"),
    ("PostgreSQL-Dark", 860, 590, 60, -4, "live", "chip"),
]
# curves (start, control, end) — they fade in toward the end point
CURVES = [((120, 296), (250, 270), (318, 190)), ((928, 250), (950, 330), (956, 382)),
          ((680, 590), (780, 585), (850, 625)), ((628, 610), (628, 640), (628, 668))]


def badge(x, y, text, style, T):
    if style == "dot":
        return f'<circle cx="{x}" cy="{y}" r="7" fill="{RED}" stroke="{T["bg"]}" stroke-width="2.5"/>'
    w = 14 + 8.2 * len(text)
    fill, col = (RED, "#ffffff") if style == "red" else (T["chip"], T["chipt"])
    stroke = "" if style == "red" else ' stroke="#00000014"'
    return (f'<g filter="url(#tsh)"><rect x="{x - w / 2:.1f}" y="{y - 13}" width="{w:.1f}" height="26" rx="13" fill="{fill}"{stroke}/></g>'
            f'<text x="{x}" y="{y + 5}" style="font-family:{SANS};font-size:14px;font-weight:700;text-anchor:middle;'
            f'dominant-baseline:auto" fill="{col}">{text}</text>')


def build(t):
    T = TH[t]
    o = [f'<svg x="0" y="{{Y}}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<defs><linearGradient id="tbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["top"]}"/>'
         f'<stop offset=".28" stop-color="{T["bg"]}"/></linearGradient>'
         f'<filter id="tsh" x="-40%" y="-40%" width="180%" height="190%"><feDropShadow dx="0" dy="6" stdDeviation="7" '
         f'flood-color="#000" flood-opacity="{T["sh"]}"/></filter></defs>',
         '<style>.tb{animation:tb 4s ease-in-out infinite alternate}@keyframes tb{to{transform:translateY(-8px)}}'
         '.tc{stroke-dasharray:420;animation:tc 6s ease-in-out infinite}@keyframes tc{0%{stroke-dashoffset:420}45%,100%{stroke-dashoffset:0}}</style>',
         f'<rect width="{W}" height="{H}" fill="url(#tbg)"/>']
    for i, (a, c, b) in enumerate(CURVES):
        o.append(f'<linearGradient id="tg{i}" gradientUnits="userSpaceOnUse" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}">'
                 f'<stop offset="0" stop-color="{T["line"]}" stop-opacity="1"/><stop offset="1" stop-color="{T["line"]}" stop-opacity="0"/></linearGradient>'
                 f'<path class="tc" style="animation-delay:{i * .8:.1f}s" d="M{a[0]} {a[1]}Q{c[0]} {c[1]} {b[0]} {b[1]}" fill="none" stroke="url(#tg{i})" stroke-width="1.6"/>')
    for i, (name, x, y, s, tilt, text, style) in enumerate(ICONS):
        data = base64.b64encode(open(os.path.join(ROOT, "assets", "tools", f"{name}.svg"), "rb").read()).decode()
        bx, by = (x + s - 4, y + 4) if style == "dot" else (x + s * .55, y - 2)
        o.append(f'<g class="tb" style="animation-delay:{-i * .7:.1f}s;animation-duration:{3.6 + (i % 3) * .6:.1f}s">'
                 f'<g transform="rotate({tilt} {x + s / 2} {y + s / 2})">'
                 f'<g filter="url(#tsh)"><image x="{x}" y="{y}" width="{s}" height="{s}" href="data:image/svg+xml;base64,{data}"/></g>'
                 f'{badge(bx, by, text, style, T) if text or style == "dot" else ""}</g></g>')
    o.append(f'<text x="500" y="282" style="font-family:{SANS};font-size:58px;'
             f'font-weight:400;letter-spacing:-2px;text-anchor:middle;dominant-baseline:auto" fill="{T["ink"]}">Many tools.</text>')
    o.append(f'<text x="500" y="348" style="font-family:{SANS};font-size:58px;'
             f'font-weight:400;letter-spacing:-2px;text-anchor:middle;dominant-baseline:auto" fill="{T["ink"]}">One calm workflow.</text>')
    cols = [("Read the problem before", "writing the code."), ("Ship small, test often,", "keep it simple."),
            ("Turn messy data into", "clear decisions.")]
    for i, (l1, l2) in enumerate(cols):
        x = 140 + i * 265
        for j, line in enumerate((l1, l2)):
            o.append(f'<text x="{x}" y="{430 + j * 24}" style="font-family:{MONO};font-size:15.5px;text-anchor:start;'
                     f'dominant-baseline:auto" fill="{T["muted"]}">{line}</text>')
    o.append('</svg>')
    return "".join(o), H
