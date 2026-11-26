"""Keyboard section: c-r-e-a-t-e + Enter, with code and heart keys (light + dark)."""

FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif"
TH = {
    "light": dict(top="#e8e4da", bottom="#ffffff", base="#dfe2de", cap="#f8f9f7", capb="#eef0ec", ink="#1d2a33",
                  sh=".16", head="#111111", sub="#6b6b6b"),
    "dark": dict(top="#0d1117", bottom="#0d1117", base="#11161d", cap="#222a35", capb="#1a212b", ink="#e6edf3",
                 sh=".6", head="#e6edf3", sub="#8b949e"),
}
ORANGE = dict(base="#d93a0a", cap="#ff5a1f", capb="#f04812")
U, G = 100, 8            # key size, gap
CYCLE = 8                # seconds for one full typing loop


def key(x, y, w, h, c, label, delay, idx):
    lift = 9
    o = [f'<g class="k" style="animation-delay:{delay:.2f}s">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{c["base"]}" filter="url(#ksh)"/>',
         f'<rect x="{x + lift}" y="{y + lift - 3}" width="{w - 2 * lift}" height="{h - 2 * lift}" rx="12" fill="url(#kc{idx})"/>',
         label(x + w / 2, y + h / 2 - 3), '</g>']
    grad = (f'<linearGradient id="kc{idx}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["cap"]}"/>'
            f'<stop offset="1" stop-color="{c["capb"]}"/></linearGradient>')
    return "".join(o), grad


def build(t, width=1000):
    T = TH[t]
    light = dict(base=T["base"], cap=T["cap"], capb=T["capb"])
    H = 560
    ox, oy = 120, 70  # keyboard origin

    def letter(ch, size=38):
        return lambda cx, cy: (f'<text x="{cx}" y="{cy}" style="font-family:{FONT};font-size:{size}px;text-anchor:middle;'
                               f'dominant-baseline:central" fill="{T["ink"]}">{ch}</text>')

    def face(cx, cy):
        heart = lambda hx, hy: (f'<path d="M{hx} {hy + 3}c-3-2.6-5-4-5-6a2.6 2.6 0 0 1 5-1 2.6 2.6 0 0 1 5 1c0 2-2 3.4-5 6z" fill="#ff3b30"/>')
        return (f'<circle cx="{cx}" cy="{cy}" r="17" fill="#fff6ee"/>' + heart(cx - 6, cy - 4) + heart(cx + 6, cy - 4) +
                f'<path d="M{cx - 8} {cy + 5}q8 9 16 0z" fill="#7a2a12"/>')

    def heart(cx, cy):
        return (f'<path d="M{cx} {cy + 13}c-9-7.5-15-12-15-18a7.5 7.5 0 0 1 15-3 7.5 7.5 0 0 1 15 3c0 6-6 10.5-15 18z" fill="#ffffff"/>')

    def code(cx, cy):
        return (f'<g fill="none" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round">'
                f'<path d="M{cx - 10} {cy - 12}l-12 12 12 12" stroke="#ff5a1f"/><path d="M{cx + 10} {cy - 12}l12 12-12 12" stroke="#7f5af0"/>'
                f'<path d="M{cx + 5} {cy - 16}l-10 32" stroke="{T["ink"]}"/></g>')

    S = U + G
    layout = [  # x, y, w, h, colours, label, press order
        (0, 0, U, U, ORANGE, face, None),
        (0.45 * S, S, U, U, light, letter("c"), 0),
        (1.45 * S, S, U, U, light, letter("r"), 1),
        (0, 2 * S, U, U, light, letter("e"), 2),
        (S, 2 * S, U, U, light, letter("a"), 3),
        (2 * S, 2 * S, U, U, light, letter("t"), 4),
        (3 * S, 2 * S, U, U, light, letter("e"), 5),
        (2.45 * S, 0, 1.3 * U, 2 * U + G, light, letter("Enter", 30), 6),
        (1.45 * S, 3 * S, U, U, light, code, None),
        (2.45 * S, 3 * S, U, U, ORANGE, heart, 7),
    ]
    keys, grads = [], []
    step = 0.55
    for i, (x, y, w, h, c, lab, order) in enumerate(layout):
        delay = (order * step if order is not None else 99)
        k, g = key(ox + x, oy + y, w, h, c, lab, delay, i)
        if order is None:
            k = k.replace('class="k"', 'class="still"', 1)
        keys.append(k)
        grads.append(g)

    hx = 610
    head = [("Type the idea.", 0), ("Press Enter.", 1), ("Create it", 2), ("with love.", 3)]
    text = "".join(f'<text x="{hx}" y="{170 + i * 50}" style="font-family:{FONT};font-size:42px;font-weight:700;letter-spacing:-1px;'
                   f'text-anchor:start;dominant-baseline:auto" fill="{T["head"]}">{s}</text>' for s, i in head)
    text += (f'<text x="{hx + 2}" y="{410}" style="font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:17px;'
             f'letter-spacing:1px;text-anchor:start;dominant-baseline:auto" fill="{T["sub"]}">c r e a t e ⏎</text>')
    press = 100 / CYCLE * 0.35  # % of the cycle a key stays down
    return (f'<svg x="0" y="{{Y}}" width="{width}" height="{H}" viewBox="0 0 {width} {H}">'
            f'<defs><linearGradient id="kbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["top"]}"/>'
            f'<stop offset=".7" stop-color="{T["bottom"]}"/></linearGradient>{"".join(grads)}'
            f'<filter id="ksh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="8" stdDeviation="9" '
            f'flood-color="#000" flood-opacity="{T["sh"]}"/></filter></defs>'
            f'<style>.k{{animation:kp {CYCLE}s ease-in-out infinite}}'
            f'@keyframes kp{{0%,{press:.1f}%,100%{{transform:translateY(0)}}{press / 2:.1f}%{{transform:translateY(5px)}}}}</style>'
            f'<rect width="{width}" height="{H}" fill="url(#kbg)"/>{"".join(keys)}{text}</svg>'), H
