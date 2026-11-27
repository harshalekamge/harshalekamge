"""Koi drawn frame by frame on the grid: bodies bend as they swim along looping paths (light + dark)."""
import math, random

S = 12            # grid cell
N = 48            # frames per loop
CYCLE = 14        # seconds per loop
W, H = 1000, 460

# tile palettes: (fill, character colour)
PAL = {
    "light": {"w": ("#ece9e3", "#8d887f"), "g": ("#cfcac1", "#5f5a50"), "d": ("#8e887d", "#ece8e0"),
              "k": ("#4a453d", "#d9d4cb"), "o": ("#6f6a52", "#e9e4cf"), "f": ("#f3f1ed", "#b9b4ab")},
    "dark": {"w": ("#c9ccd1", "#4b5058"), "g": ("#8f949c", "#1f242b"), "d": ("#5a6069", "#d0d5dc"),
             "k": ("#2b3038", "#9aa3ad"), "o": ("#6f6a52", "#e9e4cf"), "f": ("#262c34", "#6b7480")},
}
ACCENT = {"light": ["#3f8f86", "#7c6bb0"], "dark": ["#5fc0b3", "#a596de"]}
CHARS = "SX8%@tso:"

# each koi: centre, radii and phase of its looping path, length (spine steps), width scale, colour style
KOI = [
    dict(cx=260, cy=150, ax=210, ay=95, p=0.00, q=0.6, n=22, wid=1.0, style="spots"),
    dict(cx=700, cy=260, ax=240, ay=130, p=0.35, q=1.9, n=24, wid=1.05, style="pale"),
    dict(cx=520, cy=330, ax=330, ay=90, p=0.70, q=3.1, n=18, wid=.9, style="olive"),
]


def path(k, s):
    a = 2 * math.pi * (s + k["p"])
    return k["cx"] + k["ax"] * math.sin(a), k["cy"] + k["ay"] * math.sin(2 * a + k["q"])


def spine(k, s, step=6.0):
    """Points from the head backwards along the path, spaced ~step px apart."""
    pts, ds, cur = [path(k, s)], 1e-3, s
    need = k["n"] * 2
    while len(pts) < need:
        cur -= ds
        x, y = path(k, cur)
        if math.dist((x, y), pts[-1]) >= step:
            pts.append((x, y))
    return pts


def width(k, j):
    """Half-width (in cells) at spine point j (two points per cell)."""
    u = j / (k["n"] * 2)
    if u < .1:    w = 1.6 + u / .1 * 1.3
    elif u < .42: w = 2.9
    elif u < .8:  w = 2.9 - (u - .42) / .38 * 2.3
    else:         w = .6 + (u - .8) / .2 * 1.7      # tail fan
    return w * k["wid"]


def colour(k, j, lat, rnd):
    u = j / (k["n"] * 2)
    st = k["style"]
    if u > .82:
        return "f" if rnd.random() < .5 else "g"
    if st == "olive":
        return "o" if (j // 5 + (lat > 0)) % 3 else "k"
    if st == "pale":
        return "d" if ((j // 5) % 3 == 1 and lat > -0.5) else "w"
    return "k" if ((j // 4) % 3 == 1 and abs(lat) < 1.6) else ("d" if (j // 6) % 2 else "g")


def frame_cells(k, s, seed):
    pts = spine(k, s)
    cells = {}
    for j, (x, y) in enumerate(pts):
        w = width(k, j) * S
        # direction of the body here, for the side offset (lat)
        nx, ny = (pts[max(j - 1, 0)][0] - pts[min(j + 1, len(pts) - 1)][0],
                  pts[max(j - 1, 0)][1] - pts[min(j + 1, len(pts) - 1)][1])
        ln = math.hypot(nx, ny) or 1
        px, py = -ny / ln, nx / ln
        r = int(w // S) + 1
        ci, cj = int(x // S), int(y // S)
        for gi in range(ci - r - 1, ci + r + 2):
            for gj in range(cj - r - 1, cj + r + 2):
                cx, cy = gi * S + S / 2, gj * S + S / 2
                d = math.dist((cx, cy), (x, y))
                if d <= w + 1 and (gi, gj) not in cells:
                    lat = ((cx - x) * px + (cy - y) * py) / S
                    edge = d > w - S * .7
                    cells[(gi, gj)] = (j, lat, edge)
    # pectoral fins: a swept-back flap each side near the head
    for side in (-1, 1):
        j = int(k["n"] * 2 * .22)
        x, y = pts[j]
        nx, ny = pts[j - 1][0] - pts[j + 1][0], pts[j - 1][1] - pts[j + 1][1]
        ln = math.hypot(nx, ny) or 1
        ux, uy, px, py = nx / ln, ny / ln, -ny / ln, nx / ln
        for a in range(1, 4):
            for b in range(0, 4 - a + 1):
                fx = x + side * px * (width(k, j) * S + a * S * .9) - ux * b * S * .9 - ux * a * S * .5
                fy = y + side * py * (width(k, j) * S + a * S * .9) - uy * b * S * .9 - uy * a * S * .5
                cells.setdefault((int(fx // S), int(fy // S)), (j + 40, side * 9, True))
    # eyes
    x, y = pts[2]
    nx, ny = pts[0][0] - pts[4][0], pts[0][1] - pts[4][1]
    ln = math.hypot(nx, ny) or 1
    for side in (-1, 1):
        ex, ey = x + side * (-ny / ln) * S * .9, y + side * (nx / ln) * S * .9
        cells[(int(ex // S), int(ey // S))] = (-1, 0, False)
    return cells


def build(t):
    P, acc = PAL[t], ACCENT[t]
    rnd = random.Random(7)
    # tile symbols: every colour × character (+ an accent version)
    syms, sid = [], {}
    for key, (fill, ch_col) in P.items():
        for ch in CHARS:
            for a in (None, 0, 1):
                n = len(sid)
                sid[(key, ch, a)] = n
                syms.append(f'<symbol id="kt{n}" overflow="visible"><rect width="{S - 1}" height="{S - 1}" rx="2" fill="{fill}"/>'
                            f'<text x="5.5" y="8.5" fill="{acc[a] if a is not None else ch_col}">{ch}</text></symbol>')
    eye = len(sid)
    syms.append(f'<symbol id="kt{eye}" overflow="visible"><rect width="{S - 1}" height="{S - 1}" rx="2" fill="{"#1c1a17" if t == "light" else "#0b0e12"}"/></symbol>')
    o = [f'<defs>{"".join(syms)}</defs>',
         f'<style>.kf{{opacity:0;animation:kf {CYCLE}s steps(1,end) infinite}}'
         f'@keyframes kf{{0%{{opacity:1}}{100 / N:.3f}%{{opacity:0}}100%{{opacity:0}}}}</style>']
    # drifting dashes in the background
    o.append('<g fill="{}" opacity=".55">'.format("#b9b5ad" if t == "light" else "#3a414b") + "".join(
        f'<rect x="{rnd.uniform(0, W):.0f}" y="{rnd.uniform(0, H):.0f}" width="{rnd.choice((4, 6, 8))}" height="1.6"/>'
        for _ in range(140)) + '</g>')
    for f in range(N):
        s = f / N
        uses = []
        for ki, k in enumerate(KOI):
            fr = random.Random(ki * 1000 + 17)
            for (gi, gj), (j, lat, edge) in sorted(frame_cells(k, s, ki).items()):
                x, y = gi * S, gj * S
                if x < -S or x > W or y < -S or y > H:
                    continue
                if j < 0:
                    uses.append(f'<use href="#kt{eye}" x="{x}" y="{y}"/>')
                    continue
                cr = random.Random(ki * 7919 + j * 31 + int(lat * 3))
                key = "f" if edge and cr.random() < .3 else colour(k, j % 200, lat, cr)
                ch = CHARS[cr.randrange(len(CHARS))]
                a = (0 if cr.random() < .5 else 1) if cr.random() < .06 else None
                uses.append(f'<use href="#kt{sid[(key, ch, a)]}" x="{x}" y="{y}"/>')
        o.append(f'<g class="kf" style="animation-delay:{f * CYCLE / N - CYCLE:.3f}s">{"".join(uses)}</g>')
    return "".join(o)
