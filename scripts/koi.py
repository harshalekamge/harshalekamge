"""Fine pixel-art koi (cross-stitch style) that bend and swim along looping paths.

Run `python3 scripts/koi.py` to regenerate assets/koi/koi-{light,dark}.frag (needs numpy).
The banner just reads those files, so the nightly job doesn't need numpy.
"""
import math, os
try:
    import numpy as np          # only needed to regenerate the frames
except ImportError:
    np = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "koi")
P = 5                 # pixel size
W_, H_ = 1000, 460    # banner size
N = 120               # frames per loop
CYCLE = 40            # seconds per loop
SWISH = 14            # tail swishes per loop

BG = {"light": (255, 255, 255), "dark": (13, 17, 23)}
SHADOW = {"light": ("#000000", ".07"), "dark": ("#000000", ".45")}
FIN_ALPHA = .8

def hx(c): return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def mix(a, b, t): return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))

# varieties: body base/edge/dorsal, fins base/rays, patches (u, v, ru, rv, colour)
KOI = [
    dict(name="sanke", path="top", cx=500, cy=-60, ax=640, ay=175, ph=0.00, q=0, L=265, Wd=34,
         base="#f4f3ef", edge="#cfd4da", dors="#e3e2dd", fin="#d3e0ec", ray="#b6c9da",
         patches=[(.11, 0, .075, .95, "#d6392b"), (.38, .35, .07, .6, "#d6392b"), (.53, -.32, .06, .5, "#d6392b"),
                  (.29, -.25, .08, .7, "#1c1d22"), (.46, .48, .06, .45, "#1c1d22"), (.63, .1, .06, .6, "#1c1d22")]),
    dict(name="kohaku", path="fig8v", cx=868, cy=235, ax=92, ay=158, ph=0.37, q=0.4, L=245, Wd=32,
         base="#f6f4f0", edge="#d3d6db", dors="#e5e3de", fin="#f2b2a3", ray="#e48b77",
         patches=[(.15, 0, .12, 1.25, "#d03a2d"), (.37, .12, .1, 1.1, "#d03a2d"), (.57, -.15, .08, .95, "#d03a2d")]),
    dict(name="karasu", path="bottom", cx=500, cy=578, ax=660, ay=165, ph=0.55, q=0, L=215, Wd=28,
         base="#4b4d53", edge="#2c2e33", dors="#3a3c41", fin="#8a8d94", ray="#6c6f76",
         patches=[(.3, 0, .25, .35, "#5f626a")]),
]


def half_width(u, Wd):
    """Body half-width (px) at u (0 nose → 1 tail tip)."""
    w = np.zeros_like(u)
    a = (u >= 0) & (u < .14)
    w[a] = Wd * .86 * np.sqrt(np.clip(1 - ((.14 - u[a]) / .14) ** 2, 0, 1))
    b = (u >= .14) & (u < .32)
    w[b] = Wd * (.86 + .14 * np.sin((u[b] - .14) / .18 * math.pi / 2))
    c = (u >= .32) & (u < .8)
    w[c] = Wd * (.17 + .83 * ((.8 - u[c]) / .48) ** 1.25)
    d = u >= .8
    w[d] = Wd * .17
    return w


def loop_polyline(k, n=6000):
    s = np.linspace(0, 1, n, endpoint=False)
    a = 2 * math.pi * (s + k["ph"])
    if k["path"] == "top":        # bottom arc of a big ellipse above the banner
        x, y = k["cx"] + k["ax"] * np.sin(a), k["cy"] + k["ay"] * np.cos(a)
    elif k["path"] == "bottom":   # top arc of a big ellipse below the banner, swimming the other way
        x, y = k["cx"] - k["ax"] * np.sin(a), k["cy"] - k["ay"] * np.cos(a)
    else:                         # upright figure-eight
        x, y = k["cx"] + k["ax"] * np.sin(2 * a + k["q"]), k["cy"] + k["ay"] * np.sin(a)
    pts = np.stack([x, y], 1)
    seg = np.linalg.norm(np.roll(pts, -1, 0) - pts, axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    return pts, cum


def spine(k, poly, f):
    pts, cum = poly
    total = cum[-1]
    head = f / N * total
    ls = np.arange(0, k["L"] + 1e-6, 2.0)
    arc = (head - ls) % total
    x = np.interp(arc, cum[:-1], pts[:, 0], period=total)
    y = np.interp(arc, cum[:-1], pts[:, 1], period=total)
    sp = np.stack([x, y], 1)
    tan = np.gradient(sp, axis=0) * -1          # pointing towards the head
    tan /= np.linalg.norm(tan, axis=1, keepdims=True)
    nor = np.stack([-tan[:, 1], tan[:, 0]], 1)
    u = ls / k["L"]
    sw = k["Wd"] * .55 * u ** 1.6 * np.sin(2 * math.pi * (u * 1.1 - f / N * SWISH))
    sp = sp + nor * sw[:, None]
    tan = np.gradient(sp, axis=0) * -1
    tan /= np.linalg.norm(tan, axis=1, keepdims=True)
    nor = np.stack([-tan[:, 1], tan[:, 0]], 1)
    return sp, tan, nor, u


def shade(k, U, V, D, inside_body, fin_mask, ray):
    """Colour (hex) per sample point."""
    out = np.full(U.shape, k["base"], dtype=object)
    for (uc, vc, ru, rv, col) in k["patches"]:
        wob = .22 * np.sin(23 * U + 7 * V + uc * 40)
        m = inside_body & (((U - uc) / ru) ** 2 + ((V - vc) / rv) ** 2 < 1 + wob)
        out[m] = col
    dors = inside_body & (np.abs(V) < .1) & (U > .33) & (U < .62)
    out[dors & (out == k["base"])] = k["dors"]
    edge = inside_body & (np.abs(V) > .8)
    for col in set(out[edge]):
        m = edge & (out == col)
        out[m] = hx(mix(rgb(col), rgb(k["edge"]) if col == k["base"] else (0, 0, 0), .35 if col == k["base"] else .22))
    eye = inside_body & (U > .035) & (U < .075) & (np.abs(V) > .42) & (np.abs(V) < .72)
    out[eye] = "#121215"
    out[fin_mask] = np.where(ray[fin_mask], k["ray"], k["fin"])
    return out


def sample_fish(k, poly, f):
    sp, tan, nor, u = spine(k, poly, f)
    Wd, L = k["Wd"], k["L"]
    lo = np.floor((sp.min(0) - 1.7 * Wd) / P).astype(int)
    hi = np.ceil((sp.max(0) + 1.7 * Wd) / P).astype(int)
    gx, gy = np.meshgrid(np.arange(lo[0], hi[0]), np.arange(lo[1], hi[1]), indexing="ij")
    gx, gy = gx.ravel(), gy.ravel()
    off = np.array([(.5, .5), (.17, .17), (.83, .17), (.17, .83), (.83, .83)])       # centre first
    px = (gx[:, None] + off[None, :, 0]) * P
    py = (gy[:, None] + off[None, :, 1]) * P
    pts = np.stack([px.ravel(), py.ravel()], 1)
    d2 = ((pts[:, None, :] - sp[None, :, :]) ** 2).sum(2)
    i = d2.argmin(1)
    rel = pts - sp[i]
    along = (rel * tan[i]).sum(1)
    lat = (rel * nor[i]).sum(1)
    U = u[i] - along / L
    w = half_width(np.clip(U, 0, 1), Wd)
    V = np.where(w > 0, lat / np.maximum(w, 1e-6), 9)
    body = (U >= 0) & (U <= .8) & (np.abs(lat) <= w)
    # tail fin: crescent with a forked notch
    tu = (U - .76) / .24
    tw = Wd * (.18 + 1.05 * np.clip(tu, 0, 1) ** .9)
    tail = (U > .76) & (np.abs(lat) <= tw) & (U <= .93 + .07 * np.clip(np.abs(lat) / np.maximum(tw, 1e-6), 0, 1))
    tail_ray = (np.floor(np.abs(lat) / np.maximum(tw, 1e-6) * 5 + tu * 2) % 2) == 0
    # pectoral (u .2) and pelvic (u .48) fins, swept back
    fins = np.zeros_like(body)
    fray = np.zeros_like(body)
    for u0, ln, wd in ((.2, 1.3 * Wd, .45 * Wd), (.47, .7 * Wd, .28 * Wd)):
        w0 = half_width(np.array([u0]), Wd)[0]
        a = (U - u0) * L
        o = np.abs(lat) - w0 * .82
        ang = math.radians(42)
        pp = o * math.cos(ang) + a * math.sin(ang)
        qq = -o * math.sin(ang) + a * math.cos(ang)
        prof = wd * np.sin(np.clip(pp / ln, 0, 1) * math.pi) ** .55
        m = (o > -3) & (pp > 0) & (pp < ln) & (np.abs(qq) < prof) & ~body
        fins |= m
        fray |= m & ((np.floor((qq / np.maximum(pp, 2)) * 5) % 2) == 0)
    finm = (fins | tail) & ~body
    ray = np.where(tail & ~body, tail_ray, fray)
    inside = body | finm
    col = shade(k, U, V, lat, body, finm, ray)
    return gx, gy, inside.reshape(-1, len(off)), col.reshape(-1, len(off)), finm.reshape(-1, len(off)), body.reshape(-1, len(off))


def frame_pixels(f, theme, polys):
    bg = BG[theme]
    pix, shadow = {}, set()
    for k, poly in zip(KOI, polys):
        gx, gy, ins, col, fin, body = sample_fish(k, poly, f)
        cov = ins.mean(1)
        for idx in np.nonzero(cov >= .2)[0]:
            j = 0 if ins[idx, 0] else int(np.argmax(ins[idx]))
            c = rgb(col[idx, j])
            if fin[idx, j]:
                c = mix(c, bg, 1 - FIN_ALPHA)
            if cov[idx] < .8:
                c = mix(c, bg, .35 if cov[idx] >= .45 else .65)
            pix[(int(gx[idx]), int(gy[idx]))] = hx(c)
            if body[idx].any():
                shadow.add((int(gx[idx]) + 2, int(gy[idx]) + 3))
    return pix, shadow


def runs(cells):
    """Merge horizontal runs into one stroked line each (stroke width = pixel size)."""
    rows = {}
    for (x, y) in cells:
        rows.setdefault(y, []).append(x)
    d = []
    for y, xs in rows.items():
        xs.sort()
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            d.append(f"M{start * P} {y * P + P / 2:g}h{(prev - start + 1) * P}")
            if x is not None:
                start = prev = x
    return "".join(d)


def generate(theme):
    polys = [loop_polyline(k) for k in KOI]
    sc, so = SHADOW[theme]
    out = [f'<style>.kf{{opacity:0;animation:kf {CYCLE}s steps(1,end) infinite}}'
           f'@keyframes kf{{0%{{opacity:1}}{100 / N:.4f}%{{opacity:0}}100%{{opacity:0}}}}</style>']
    for f in range(N):
        pix, shadow = frame_pixels(f, theme, polys)
        inb = lambda p: -1 <= p[0] <= W_ // P and -1 <= p[1] <= H_ // P
        g = [f'<path d="{runs([p for p in shadow if inb(p)])}" stroke="{sc}" stroke-opacity="{so}"/>']
        bycol = {}
        for p, c in pix.items():
            if inb(p):
                bycol.setdefault(c, []).append(p)
        for c, cells in bycol.items():
            g.append(f'<path d="{runs(cells)}" stroke="{c}"/>')
        out.append(f'<g class="kf" style="animation-delay:{f * CYCLE / N - CYCLE:.3f}s">{"".join(g)}</g>')
    out.insert(1, f'<g fill="none" stroke-width="{P}" stroke-linecap="butt">')
    out.append('</g>')
    return "".join(out)


def load(theme):
    return open(os.path.join(OUT, f"koi-{theme}.frag"), encoding="utf-8").read()


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for t in ("light", "dark"):
        s = generate(t)
        open(os.path.join(OUT, f"koi-{t}.frag"), "w", encoding="utf-8").write(s)
        print(t, len(s))
