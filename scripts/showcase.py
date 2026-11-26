"""Project showcase: UI screenshots on the walls of a perspective tunnel (light + dark)."""
import base64, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
TH = {
    "light": dict(top="#e8e4da", edge="#cfcfcf", bg="#ffffff", line="#e3e3e3", ray="#ececec", ink="#141414", muted="#5c5c5c", accent="#e2582a",
                  btn="#141414", btnt="#ffffff", fade="#ffffff"),
    "dark": dict(top="#0d1117", edge="#30363d", bg="#0d1117", line="#262d37", ray="#1c232c", ink="#e6edf3", muted="#9da7b3", accent="#ff7a45",
                 btn="#e6edf3", btnt="#0d1117", fade="#0d1117"),
}
W, H = 1000, 780
CX, CY, HW, HH = 500, 390, 500, 390   # vanishing point and outer half-size
DEPTHS = [1, .8, .63, .5, .4]


def wall(side, s, t):
    """Point on a wall at depth s (1 = front) and position t (-1..1 along the wall)."""
    if side == "left":
        return CX - HW * s, CY + HH * s * t
    if side == "right":
        return CX + HW * s, CY + HH * s * t
    if side == "floor":
        return CX + HW * s * t, CY + HH * s
    return CX + HW * s * t, CY - HH * s  # ceiling


EDGE = ["#cfcfcf"]


def panel(side, near, far, t1, t2, img, idx, opacity=1):
    P = lambda s, t: wall(side, s, t)
    if side == "left":
        A, B, C = P(near, t1), P(far, t1), P(near, t2)
    elif side == "right":
        A, B, C = P(far, t1), P(near, t1), P(far, t2)
    elif side == "floor":
        A, B, C = P(far, t1), P(far, t2), P(near, t1)
    else:
        A, B, C = P(near, t1), P(near, t2), P(far, t1)
    quad = [P(near, t1), P(far, t1), P(far, t2), P(near, t2)]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in quad)
    m = f"matrix({B[0]-A[0]:.2f} {B[1]-A[1]:.2f} {C[0]-A[0]:.2f} {C[1]-A[1]:.2f} {A[0]:.2f} {A[1]:.2f})"
    data = base64.b64encode(open(os.path.join(ROOT, "assets", "showcase", img), "rb").read()).decode()
    return (f'<clipPath id="sc{idx}"><polygon points="{pts}"/></clipPath>'
            f'<g clip-path="url(#sc{idx})" opacity="{opacity}"><image width="1" height="1" preserveAspectRatio="xMidYMid slice" '
            f'transform="{m}" href="data:image/jpeg;base64,{data}"/></g>'
            f'<polygon points="{pts}" fill="none" stroke="{EDGE[0]}" stroke-width="1" opacity="{opacity}"/>')


def txt(x, y, s, size, fill, weight=400, anchor="middle", font=SANS, extra="", length=None):
    tl = f' textLength="{length}" lengthAdjust="spacingAndGlyphs"' if length else ""
    return (f'<text x="{x}" y="{y}"{tl} style="font-family:{font};font-size:{size}px;font-weight:{weight};'
            f'text-anchor:{anchor};dominant-baseline:auto;{extra}" fill="{fill}">{s}</text>')


def build(t):
    T = TH[t]
    EDGE[0] = T["edge"]
    o = [f'<svg x="0" y="{{Y}}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<style>.tun{transform-origin:500px 390px;animation:tz 9s ease-in-out infinite alternate}'
         '@keyframes tz{from{transform:scale(1)}to{transform:scale(1.035)}}</style>',
         f'<linearGradient id="shg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["top"]}"/><stop offset=".3" stop-color="{T["bg"]}"/></linearGradient>'
         f'<rect width="{W}" height="{H}" fill="url(#shg)"/><g class="tun">']
    # rays from the vanishing point
    for fx, fy in [(-1, -1), (1, -1), (1, 1), (-1, 1), (-.45, -1), (.45, -1), (-.45, 1), (.45, 1), (-1, -.3), (1, -.3), (-1, .35), (1, .35)]:
        o.append(f'<line x1="{CX + HW * .4 * fx:.1f}" y1="{CY + HH * .4 * fy:.1f}" x2="{CX + HW * 1.2 * fx:.1f}" y2="{CY + HH * 1.2 * fy:.1f}" stroke="{T["ray"]}"/>')
    for s in DEPTHS[1:]:
        o.append(f'<rect x="{CX - HW * s:.1f}" y="{CY - HH * s:.1f}" width="{2 * HW * s:.1f}" height="{2 * HH * s:.1f}" fill="none" stroke="{T["line"]}"/>')
    # screenshots on the walls
    o += [panel("left", 1, .8, -.78, -.08, "smart-campus.jpg", 1),
          panel("left", .8, .63, .1, .78, "greencycle.jpg", 2, .85),
          panel("left", .63, .5, -.75, -.1, "file-tracking-system.jpg", 3, .6),
          panel("right", 1, .8, .05, .78, "kola-vision.jpg", 4),
          panel("right", .8, .63, -.8, -.12, "cart-recovery-ai.jpg", 5, .85),
          panel("right", .63, .5, .15, .8, "offer-suggestor.jpg", 6, .6),
          panel("ceiling", 1, .8, -.62, -.06, "eroc-ccms.jpg", 7),
          panel("ceiling", .8, .63, .12, .72, "roc-it-inventory.jpg", 8, .85),
          panel("floor", 1, .8, .08, .66, "portfolio.jpg", 9),
          panel("floor", .8, .63, -.72, -.1, "restaurant-cancellations.jpg", 10, .85)]
    o.append('</g>')
    # soft centre so the headline reads cleanly
    o.append(f'<defs><radialGradient id="scf" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="{T["fade"]}" stop-opacity=".95"/>'
             f'<stop offset="1" stop-color="{T["fade"]}" stop-opacity="0"/></radialGradient></defs>'
             f'<ellipse cx="{CX}" cy="{CY + 10}" rx="330" ry="190" fill="url(#scf)"/>')
    o.append(txt(CX, CY - 22, "Things I&#8217;ve built.", 72, T["ink"], 700, extra="letter-spacing:-3px", length=640))
    o.append(txt(CX, CY + 28, "Real interfaces from real projects — designed, coded and shipped,", 19, T["muted"], length=560))
    o.append(txt(CX, CY + 54, f'one screen at a time. <tspan fill="{T["accent"]}">Infinitely.</tspan>', 19, T["muted"]))
    names = "WEB  ·  AI  ·  DATA  ·  VISION"
    o.append(f'<rect x="{CX - 155}" y="{CY + 82}" width="310" height="40" rx="20" fill="{T["btn"]}"/>')
    o.append(txt(CX, CY + 108, names, 13, T["btnt"], 700, font=MONO, extra="letter-spacing:1px", length=260))
    o.append('</svg>')
    return "".join(o), H
