"""Footer: Lotus Tower line sketch, 'Let's build something lasting.' and contact cards (light + dark)."""

SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
TH = {
    "light": dict(bg="#ffffff", dot="#d9d9d9", ink="#141414", grey="#7a7a7a", muted="#5c5c5c", sketch="#8f8f8f",
                  blue="#5b6cff", bluefill="#e7e9ff", panel="#ffffff", line="#e6e6e6", card="#f3f3f3", btn="#141414", btnt="#ffffff"),
    "dark": dict(bg="#0d1117", dot="#232a33", ink="#e6edf3", grey="#7d8590", muted="#9da7b3", sketch="#5d6570",
                 blue="#7c8bff", bluefill="#1c2147", panel="#0d1117", line="#21262d", card="#161b22", btn="#e6edf3", btnt="#0d1117"),
}
W, H = 1000, 930


def txt(x, y, s, size, fill, weight=400, anchor="start", font=SANS, extra=""):
    return (f'<text x="{x}" y="{y}" style="font-family:{font};font-size:{size}px;font-weight:{weight};'
            f'text-anchor:{anchor};dominant-baseline:auto;{extra}" fill="{fill}">{s}</text>')


def tower(stroke, fill_bulb):
    cx = 150
    o = []
    # spire and rings
    o.append(f'<path d="M{cx} 36V128M{cx - 6} 70h12M{cx - 8} 92h16M{cx - 10} 112h20" stroke-width="1.6"/>')
    # lotus bud
    bud = f"M{cx} 312C{cx - 62} 282 {cx - 66} 196 {cx} 128C{cx + 66} 196 {cx + 62} 282 {cx} 312Z"
    o.append(f'<path d="{bud}" fill="{fill_bulb}" stroke-width="1.8"/>')
    o.append(f'<clipPath id="budc"><path d="{bud}"/></clipPath>')
    o.append(f'<g clip-path="url(#budc)" stroke-width=".9">' + "".join(
        f'<path d="M{cx - 70} {y}h140"/>' for y in range(150, 312, 9)) + '</g>')
    o.append(f'<path d="M{cx} 312C{cx - 30} 270 {cx - 30} 190 {cx} 150M{cx} 312C{cx + 30} 270 {cx + 30} 190 {cx} 150'
             f'M{cx} 312C{cx - 50} 280 {cx - 52} 220 {cx - 36} 180M{cx} 312C{cx + 50} 280 {cx + 52} 220 {cx + 36} 180" stroke-width="1.3"/>')
    # shaft
    o.append(f'<path d="M{cx - 18} 312L{cx - 30} 650M{cx + 18} 312L{cx + 30} 650" stroke-width="1.8"/>')
    for i in range(1, 6):
        f = i / 6
        o.append(f'<path d="M{cx - 18 + 36 * f} 312L{cx - 30 + 60 * f} 650" stroke-width=".8"/>')
    for y in range(330, 650, 16):
        t = (y - 312) / 338
        hw = 18 + 12 * t
        o.append(f'<path d="M{cx - hw:.1f} {y}h{2 * hw:.1f}" stroke-width=".7"/>')
    # podium
    o.append(f'<path d="M{cx - 70} 650h140v22h-140zM{cx - 100} 672h200v26h-200zM{cx - 130} 698h260v30h-260z" fill="none" stroke-width="1.5"/>')
    for x in range(cx - 120, cx + 130, 16):
        o.append(f'<path d="M{x} 702v22" stroke-width=".7"/>')
    for x in range(cx - 92, cx + 100, 14):
        o.append(f'<path d="M{x} 676v18" stroke-width=".7"/>')
    return f'<g fill="none" stroke="{stroke}" stroke-linecap="round">{"".join(o)}</g>'


def build(t):
    T = TH[t]
    o = [f'<svg x="0" y="{{Y}}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<defs><pattern id="fdot" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="9" cy="9" r="1" fill="{T["dot"]}"/></pattern>'
         f'<linearGradient id="ffade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg"]}"/><stop offset=".12" stop-color="{T["bg"]}" stop-opacity="0"/></linearGradient></defs>',
         '<style>.glow{animation:gw 3s ease-in-out infinite alternate}@keyframes gw{from{opacity:.65}to{opacity:1}}</style>',
         f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/><rect width="{W}" height="560" fill="url(#fdot)"/><rect width="{W}" height="560" fill="url(#ffade)"/>']
    # sketch: grey, then the blue band on top
    o.append(tower(T["sketch"], "none"))
    o.append(f'<clipPath id="fblue"><rect x="40" y="160" width="230" height="200"/></clipPath>')
    o.append(f'<g class="glow" clip-path="url(#fblue)">{tower(T["blue"], T["bluefill"])}</g>')
    # hero text
    o.append(f'<text x="600" y="132" style="font-family:{SANS};font-size:64px;letter-spacing:-2.5px;text-anchor:middle;dominant-baseline:auto">'
             f'<tspan fill="{T["grey"]}">Let&#8217;s build</tspan><tspan fill="{T["ink"]}"> something</tspan></text>')
    o.append(txt(600, 206, "lasting.", 64, T["ink"], anchor="middle", extra="letter-spacing:-2.5px"))
    o.append(txt(600, 258, "Software engineer and Data Science undergraduate at SLIIT —", 17, T["muted"], anchor="middle"))
    o.append(txt(600, 282, "open to projects, collaborations and good ideas.", 17, T["muted"], anchor="middle"))
    o.append(f'<rect x="510" y="318" width="180" height="46" rx="6" fill="{T["btn"]}"/>')
    o.append(txt(600, 347, "Visit Portfolio  →", 16, T["btnt"], 500, "middle"))
    # lower panel
    px = 270
    o.append(f'<rect x="{px}" y="560" width="{W - px}" height="{H - 560}" fill="{T["panel"]}"/>')
    o.append(f'<path d="M{px} 560H{W}M{px} 560V{H}M{px} 744H{W}M635 560V744" stroke="{T["line"]}"/>')
    o.append(f'<path d="M{px} 560L635 744" stroke="{T["line"]}" stroke-width=".8"/>')
    o.append(txt(px + 30, 622, "( GET IN TOUCH )", 11, T["muted"], 500, font=MONO, extra="letter-spacing:1px"))
    o.append(txt(px + 30, 676, "Let&#8217;s talk —", 40, T["ink"], extra="letter-spacing:-1.2px"))
    o.append(txt(px + 30, 722, "any way you like.", 40, T["ink"], extra="letter-spacing:-1.2px"))
    for i, line in enumerate(["Reach me on WhatsApp, by phone or by email.", "Everything is copyable right below this card,",
                              "and my work lives on my portfolio."]):
        o.append(txt(660, 664 + i * 22, line, 15, T["muted"]))
    cards = [("01 / WhatsApp &amp; Phone", "+94 77 875 3792"), ("02 / Email", "harshalekamge.official@gmail.com"),
             ("03 / Email", "lekamge.h2024@gmail.com"), ("04 / Portfolio", "portfolio.harshalekamge.com")]
    cw, ch, gap = (W - px - 44 - 10) / 2, 66, 10
    for i, (title, val) in enumerate(cards):
        x = px + 22 + (i % 2) * (cw + gap)
        y = 762 + (i // 2) * (ch + gap)
        o.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{ch}" rx="4" fill="{T["card"]}"/>')
        o.append(txt(f"{x + 16:.1f}", y + 25, title, 13, T["muted"]))
        o.append(txt(f"{x + 16:.1f}", y + 50, val, 15, T["ink"], 500, font=MONO))
    o.append('</svg>')
    return "".join(o), H
