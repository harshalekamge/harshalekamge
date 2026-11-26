"""Poster section: the word CODE built from tool icons, with poster typography and a QR to the portfolio (light + dark)."""
import base64, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
TH = {"light": dict(bg="#ffffff", ink="#111111", muted="#555555", qr="#111111"),
      "dark": dict(bg="#0d1117", ink="#e6edf3", muted="#9da7b3", qr="#e6edf3")}
W, H = 1000, 1000
CELL, ICON = 37, 35
GLYPHS = {
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
}
PLACES = {"C": (70, 70), "O": (640, 240), "D": (330, 430), "E": (700, 640)}


def txt(x, y, s, size, fill, weight=400, anchor="start", extra="", rot=None):
    tr = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    return (f'<text x="{x}" y="{y}"{tr} style="font-family:{SANS};font-size:{size}px;font-weight:{weight};'
            f'text-anchor:{anchor};dominant-baseline:auto;{extra}" fill="{fill}">{s}</text>')


def build(t):
    T = TH[t]
    rnd = random.Random(26)
    names = sorted(f[:-4] for f in os.listdir(os.path.join(ROOT, "assets", "icons")) if f.endswith(".svg"))
    defs = "".join(
        f'<image id="ic-{n}" width="{ICON}" height="{ICON}" href="data:image/svg+xml;base64,'
        f'{base64.b64encode(open(os.path.join(ROOT, "assets", "icons", n + ".svg"), "rb").read()).decode()}"/>' for n in names)
    o = [f'<svg x="0" y="{{Y}}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<defs>{defs}<filter id="ish" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="3" stdDeviation="2.5" '
         f'flood-color="#000" flood-opacity="{".25" if t == "light" else ".6"}"/></filter></defs>',
         '<style>.ic{transform-box:fill-box;transform-origin:center;animation:wg 3.2s ease-in-out infinite alternate}'
         '@keyframes wg{from{transform:rotate(-5deg)}to{transform:rotate(5deg)}}</style>',
         f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>']
    # letters made of icons
    o.append('<g filter="url(#ish)">')
    pool = names[:]
    for ch, (lx, ly) in PLACES.items():
        for r, row in enumerate(GLYPHS[ch]):
            for c, on in enumerate(row):
                if on != "#":
                    continue
                if not pool:
                    pool = names[:]
                n = pool.pop(rnd.randrange(len(pool)))
                x = lx + c * CELL + rnd.uniform(-3, 3)
                y = ly + r * CELL + rnd.uniform(-3, 3)
                rot = rnd.uniform(-22, 22)
                o.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f} {ICON / 2} {ICON / 2})">'
                         f'<use class="ic" href="#ic-{n}" style="animation-delay:{-rnd.random() * 3:.2f}s"/></g>')
    o.append('</g>')
    # poster text
    o.append(txt(330, 96, "Vol.", 18, T["ink"], 400))
    o.append(txt(370, 96, "2026", 18, T["ink"], 700))
    o.append(txt(330, 150, "HARSHA", 56, T["ink"], 800, extra="letter-spacing:-2px"))
    blurb = ["Every letter on this page is built from the tools", "I use every day — React, Python, Spring, PyTorch,",
             "Docker and more. Code is how I build things,", "and these are my building blocks."]
    for i, line in enumerate(blurb):
        o.append(txt(332, 182 + i * 18, line, 12.5, T["muted"]))
    # QR code to the portfolio
    rows = open(os.path.join(ROOT, "assets", "icons", "qr.txt")).read().split("\n")
    qs = 110 / len(rows)
    qx, qy = 850, 70
    o.append(f'<rect x="{qx - 6}" y="{qy - 6}" width="122" height="122" fill="{T["bg"]}"/>')
    o.append('<g fill="{}">'.format(T["qr"]) + "".join(
        f'<rect x="{qx + c * qs:.2f}" y="{qy + r * qs:.2f}" width="{qs + .3:.2f}" height="{qs + .3:.2f}"/>'
        for r, row in enumerate(rows) for c, v in enumerate(row) if v == "1") + '</g>')
    o.append(txt(qx + 55, qy + 136, "scan → portfolio", 11.5, T["muted"], 500, "middle"))
    o.append(txt(52, 650, "Colombo, Sri Lanka", 26, T["ink"], 700, rot=-90))
    o.append(txt(92, 650, "SLIIT · BSc (Hons) IT · Data Science", 14, T["muted"], 500, rot=-90))
    o.append(txt(70, 728, "github.com/harshalekamge", 22, T["ink"], 800))
    o.append(txt(70, 980, "2026", 54, T["ink"], 800, rot=-90, extra="letter-spacing:-2px"))
    o.append(txt(150, 800, "YOUNG", 36, T["ink"], 300, extra="letter-spacing:-1px"))
    o.append(txt(150, 840, "DEVELOPER&#8217;S", 36, T["ink"], 300, extra="letter-spacing:-1px"))
    o.append(txt(150, 886, "PORTFOLIO", 44, T["ink"], 800, extra="letter-spacing:-1.5px"))
    o.append(txt(150, 950, "Web · AI · Data · Vision", 30, T["ink"], 800, extra="letter-spacing:-1px"))
    o.append(txt(560, 600, "IDEA", 22, T["ink"], 400))
    o.append(f'<path d="M581 616v52m-9-10 9 10 9-10" fill="none" stroke="{T["ink"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(txt(560, 700, "SHIPPED", 22, T["ink"], 400))
    o.append('</svg>')
    return "".join(o), H
