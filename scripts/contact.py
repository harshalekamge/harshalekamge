"""'Just search Harsha Lekamge' section with block art and contact strip (light + dark)."""

SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
TH = {
    "light": dict(bg="#ffffff", ink="#141414", muted="#6b6b6b", dot="#cfcfcf", block="#f1f1f1", wire="#dedede",
                  hl="#d9d0ff", bar="#ffffff", barline="#e2e2e2", btn="#111111", btnt="#ffffff", line="#ececec"),
    "dark": dict(bg="#0d1117", ink="#e6edf3", muted="#8b949e", dot="#2a313b", block="#161b22", wire="#262d37",
                 hl="#3b2f7a", bar="#161b22", barline="#30363d", btn="#e6edf3", btnt="#0d1117", line="#21262d"),
}
LIME, PURPLE = "#c6ff00", "#b6a4ff"


def txt(x, y, s, size, fill, weight=400, anchor="start", font=SANS, extra="", length=None):
    tl = f' textLength="{length}" lengthAdjust="spacingAndGlyphs"' if length else ""
    return (f'<text x="{x}" y="{y}"{tl} style="font-family:{font};font-size:{size}px;font-weight:{weight};'
            f'text-anchor:{anchor};dominant-baseline:auto;{extra}" fill="{fill}">{s}</text>')


def blob(cells, ox, oy, u, fill, r=16, cls=""):
    """Cells merged into one rounded shape: outer corners rounded, joints square."""
    cs = set(cells)
    o = []
    for (cx, cy) in cells:
        x, y = ox + cx * u, oy + cy * u
        n = lambda dx, dy: (cx + dx, cy + dy) in cs
        tl = r if not n(-1, 0) and not n(0, -1) else 0
        tr = r if not n(1, 0) and not n(0, -1) else 0
        br = r if not n(1, 0) and not n(0, 1) else 0
        bl = r if not n(-1, 0) and not n(0, 1) else 0
        e = u + 0.6
        o.append(f'<path d="M{x + tl} {y}H{x + e - tr}{f"a{tr} {tr} 0 0 1 {tr} {tr}" if tr else ""}V{y + e - br}'
                 f'{f"a{br} {br} 0 0 1 {-br} {br}" if br else ""}H{x + bl}{f"a{bl} {bl} 0 0 1 {-bl} {-bl}" if bl else ""}'
                 f'V{y + tl}{f"a{tl} {tl} 0 0 1 {tl} {-tl}" if tl else ""}Z"/>')
    return f'<g fill="{fill}" class="{cls}">{"".join(o)}</g>'


def build(t, width=1000):
    T = TH[t]
    H = 480
    o = [f'<svg x="0" y="{{Y}}" width="{width}" height="{H}" viewBox="0 0 {width} {H}">',
         '<style>.cb{animation:cb 1s steps(1) infinite}@keyframes cb{50%{fill-opacity:0}}'
         '.fl{animation:fl 5s ease-in-out infinite alternate}.fl2{animation:fl 6s ease-in-out infinite alternate-reverse}'
         '@keyframes fl{from{transform:translate(0,0)}to{transform:translate(0,-6px)}}</style>',
         f'<rect width="{width}" height="{H}" fill="{T["bg"]}"/>']
    # dot grid + block art on the right
    u, ox, oy = 50, 545, 40
    o.append('<g>' + "".join(f'<circle cx="{ox + 25 + i * 64}" cy="{oy + 25 + j * 64}" r="1.6" fill="{T["dot"]}"/>'
                             for i in range(7) for j in range(6)) + '</g>')
    grey = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 1), (6, 3), (6, 4), (5, 4), (4, 4), (4, 5), (4, 6), (3, 6),
            (0, 4), (1, 4), (1, 3), (2, 3), (7, 2), (7, 3)]
    o.append(blob([c for c in grey if c[1] < 7], ox, oy, u, T["block"]))
    o.append(f'<g fill="none" stroke="{T["wire"]}" stroke-width="1.2"><rect x="{ox + 0.5 * u}" y="{oy + 0.6 * u}" width="{2.6 * u}" height="{3.6 * u}" rx="18"/>'
             f'<rect x="{ox + 4.6 * u}" y="{oy + 4.4 * u}" width="{2.6 * u}" height="{3.3 * u}" rx="18"/>'
             f'<path d="M{ox + 0.5 * u} {oy + 2.2 * u}H{ox + 3.1 * u}M{ox + 1.8 * u} {oy + 0.6 * u}V{oy + 4.2 * u}'
             f'M{ox + 4.6 * u} {oy + 7.7 * u}L{ox + 7.2 * u} {oy + 5.6 * u}"/></g>')
    o.append(blob([(2, 0), (2, 1), (1, 1), (3, 1), (4, 1), (5, 1), (5, 0), (6, 0), (2, 2)], ox + 10, oy - 10, u, LIME, cls="fl"))
    o.append(blob([(3, 5), (4, 5), (4, 6)], ox, oy + 5, u, LIME, cls="fl2"))
    o.append(blob([(7, 3), (6, 4), (7, 4), (5, 4), (5, 5), (6, 5), (6, 6)], ox - 10, oy, u, PURPLE, cls="fl"))
    o.append(f'<g stroke="{T["bg"]}" stroke-width="1.5" opacity=".7"><path d="M{ox - 10 + 5.5 * u} {oy + 4 * u}V{oy + 6 * u}M{ox - 10 + 5 * u} {oy + 5.5 * u}H{ox - 10 + 7 * u}"/></g>')
    # headline with highlight pills
    o.append(txt(60, 120, "Just search", 52, T["ink"], extra="letter-spacing:-1.5px", length=268))
    o.append(f'<rect x="46" y="146" width="410" height="66" rx="20" fill="{T["hl"]}"/>')
    o.append(txt(64, 196, "Harsha Lekamge", 52, T["ink"], extra="letter-spacing:-1.5px", length=374))
    o.append(txt(60, 272, "on", 52, T["ink"], extra="letter-spacing:-1.5px", length=52))
    o.append(f'<rect x="124" y="222" width="200" height="66" rx="20" fill="{T["hl"]}"/>')
    o.append(txt(140, 272, "Google.", 52, T["ink"], extra="letter-spacing:-1.5px", length=166))
    # search bar
    o.append(f'<rect x="60" y="310" width="440" height="54" rx="27" fill="{T["bar"]}" stroke="{T["barline"]}"/>')
    o.append(f'<g fill="none" stroke="{T["muted"]}" stroke-width="2.2" stroke-linecap="round"><circle cx="90" cy="335" r="8"/><path d="M96 341l6 6"/></g>')
    o.append(txt(114, 343, 'harsha lekamge<tspan class="cb" dx="2">|</tspan>', 18, T["ink"]))
    o.append(f'<rect x="392" y="318" width="100" height="38" rx="19" fill="{T["btn"]}"/>')
    o.append(txt(442, 342, "SEARCH", 13, T["btnt"], 700, "middle", MONO, "letter-spacing:1px"))
    # degree
    o.append(txt(60, 404, "BSc (Hons) in Information Technology", 17, T["ink"], 600))
    o.append(txt(60, 428, "Specialised in Data Science — SLIIT", 16, T["muted"]))
    o.append('</svg>')
    return "".join(o), H
