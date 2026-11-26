"""'HARSHA × The Stack.' — the tools and technologies as a shelf of book spines (light + dark)."""
import random

SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
TH = {"light": dict(bg="#ffffff", ink="#141414", shelf="#d9d9d9", shadow=".18"),
      "dark": dict(bg="#0d1117", ink="#e6edf3", shelf="#30363d", shadow=".6")}
W, H, FLOOR = 1000, 560, 515

# name, spine colour, text colour, style, width, height, accent
BOOKS = [
    ("Java", "#e76f00", "#ffffff", "serif-b", 38, 300, "#ffd2a6"),
    ("Python", "#3776ab", "#ffd43b", "sans-b", 44, 330, "#ffd43b"),
    ("JavaScript", "#f7df1e", "#1a1a1a", "mono", 36, 290, "#1a1a1a"),
    ("TypeScript", "#3178c6", "#ffffff", "sans", 34, 310, "#ffffff"),
    ("React", "#20232a", "#61dafb", "sans-b", 46, 345, "#61dafb"),
    ("Next.js", "#000000", "#ffffff", "sans-b", 36, 300, "#ffffff"),
    ("Tailwind", "#e0f2fe", "#0284c7", "serif-i", 32, 270, "#38bdf8"),
    ("Spring Boot", "#6db33f", "#ffffff", "cond", 40, 335, "#e8f5dc"),
    ("Node.js", "#215732", "#8cc84b", "mono", 34, 285, "#8cc84b"),
    ("MongoDB", "#00684a", "#00ed64", "sans-b", 36, 315, "#00ed64"),
    ("PostgreSQL", "#336791", "#ffffff", "serif", 38, 320, "#a7c4e0"),
    ("MySQL", "#f5f5f0", "#00758f", "mono", 30, 250, "#f29111"),
    ("Firebase", "#ffca28", "#3a2a00", "sans-b", 36, 280, "#f57c00"),
    ("PyTorch", "#ee4c2c", "#ffffff", "cond", 42, 330, "#ffd0c6"),
    ("YOLO", "#d7ff1e", "#111111", "lean", 56, 360, "#111111"),
    ("OpenCV", "#5c3ee8", "#ffffff", "sans", 34, 300, "#ff4d4d"),
    ("scikit-learn", "#f7931e", "#1f1f1f", "serif-i", 34, 295, "#3499cd"),
    ("Docker", "#2496ed", "#ffffff", "sans-b", 40, 320, "#d6ecfd"),
    ("Git", "#f05032", "#ffffff", "mono", 30, 240, "#ffffff"),
    ("GitHub", "#24292f", "#ffffff", "sans", 36, 330, "#8b949e"),
    ("Figma", "#ffffff", "#1e1e1e", "figma", 34, 275, None),
    ("Kotlin", "#7f52ff", "#ffffff", "cond", 32, 290, "#e44857"),
    ("Vite", "#1b1b3a", "#ffd62e", "serif-b", 32, 260, "#646cff"),
    ("FastAPI", "#009688", "#ffffff", "mono", 34, 300, "#b2dfdb"),
    ("Postman", "#ff6c37", "#ffffff", "sans", 32, 280, "#ffe0d3"),
    ("WordPress", "#21759b", "#ffffff", "serif", 36, 310, "#cfe5f0"),
]
FONTS = {"serif": (SERIF, 400, ""), "serif-b": (SERIF, 700, ""), "serif-i": (SERIF, 400, "font-style:italic;"),
         "sans": (SANS, 400, ""), "sans-b": (SANS, 800, ""), "mono": (MONO, 500, ""), "cond": (SANS, 800, "letter-spacing:-1px;"),
         "figma": (SANS, 600, ""), "lean": (SANS, 900, "letter-spacing:-1px;")}


def spine(x, b, i, T):
    name, col, tcol, style, w, h, acc = b
    w = round(w * .82)
    rnd = random.Random(i * 31 + 5)
    y = FLOOR - h
    font, weight, extra = FONTS[style]
    size = min(w * .58, 24) if style != "lean" else 28
    est = len(name) * size * (.62 if style != "mono" else .62)
    room = h - 70
    tl = f' textLength="{room}" lengthAdjust="spacingAndGlyphs"' if est > room else ""
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sgl)"/>']
    if style == "figma":
        for k, c in enumerate(["#f24e1e", "#ff7262", "#a259ff", "#1abcfe", "#0acf83"]):
            o.append(f'<rect x="{x}" y="{y + 10 + k * 9}" width="{w}" height="8" fill="{c}"/>')
    elif acc:
        kind = rnd.choice(["band", "top", "dots", "bar"])
        if kind == "band":
            o.append(f'<rect x="{x}" y="{y + h * .72:.0f}" width="{w}" height="10" fill="{acc}" opacity=".85"/>')
        elif kind == "top":
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="26" fill="{acc}" opacity=".9"/>')
        elif kind == "dots":
            o.append("".join(f'<circle cx="{x + w / 2}" cy="{y + h - 52 - k * 11}" r="3" fill="{acc}"/>' for k in range(3)))
        else:
            o.append(f'<rect x="{x + w / 2 - 6}" y="{y + h - 70}" width="12" height="3" fill="{acc}"/>')
    ty = y + (66 if style == "figma" else 60 if style == "lean" else 40)
    dx = -.36
    o.append(f'<text transform="translate({x + w / 2 + size * dx:.1f} {ty}) rotate(90)"{tl} style="font-family:{font};'
             f'font-size:{size:.1f}px;font-weight:{weight};{extra}text-anchor:start;dominant-baseline:auto" fill="{tcol}">{name}</text>')
    o.append(f'<rect x="{x + w / 2 - 5}" y="{FLOOR - 24}" width="10" height="10" rx="2" fill="none" stroke="{tcol}" stroke-width="1.2" opacity=".7"/>')
    body = "".join(o)
    if style == "lean":
        return f'<g transform="rotate(-11 {x} {FLOOR})">{body}</g>'
    return f'<g class="bk" style="animation-delay:{i * .25:.2f}s">{body}</g>'


def build(t):
    T = TH[t]
    total = sum(round(b[4] * .82) for b in BOOKS) + 3 * (len(BOOKS) - 1) + 60
    x = (W - total) / 2
    o = [f'<svg x="0" y="{{Y}}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<defs><linearGradient id="sgl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".18"/>'
         f'<stop offset=".18" stop-color="#fff" stop-opacity=".12"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>'
         f'<filter id="bsh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity="{T["shadow"]}"/></filter></defs>',
         f'<style>.bk{{animation:bk {len(BOOKS) * .25 + 4:.1f}s ease-in-out infinite}}@keyframes bk{{0%,8%,100%{{transform:translateY(0)}}4%{{transform:translateY(-12px)}}}}</style>',
         f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
         f'<text x="{W / 2}" y="78" style="font-family:{SANS};font-size:30px;text-anchor:middle;dominant-baseline:auto" fill="{T["ink"]}">'
         f'<tspan font-weight="400" letter-spacing="1">HARSHA</tspan><tspan font-weight="300"> × </tspan><tspan font-weight="800">The Stack.</tspan></text>',
         '<g filter="url(#bsh)">']
    for i, b in enumerate(BOOKS):
        if b[3] == "lean":
            x += 52   # room for the book to lean into
        o.append(spine(round(x, 1), b, i, T))
        x += round(b[4] * .82) + 3 + (8 if b[3] == "lean" else 0)
    o.append('</g>')
    o.append(f'<rect x="40" y="{FLOOR}" width="{W - 80}" height="3" fill="{T["shelf"]}"/>')
    o.append('</svg>')
    return "".join(o), H
