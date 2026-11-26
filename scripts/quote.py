"""'Talk is cheap. Show me the code.' — a book fanning open, its pages made of code and colour (light + dark)."""
import math, random

SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
TH = {"light": dict(bg="#ffffff", ink="#111111", muted="#555555", page="#ffffff", edge="#1a1a1a", code="#c9c9c9"),
      "dark": dict(bg="#0d1117", ink="#e6edf3", muted="#9da7b3", page="#e6edf3", edge="#0d1117", code="#8b949e")}
W, H = 1000, 760
PX, PY, R = 935, 610, 590            # spine (pivot) and page length
COLORS = ["#61dafb", "#ffd43b", "#3776ab", "#ee4c2c", "#6db33f", "#f7df1e", "#2496ed", "#00ed64", "#7f52ff",
          "#d7ff1e", "#f05032", "#ff6c37", "#e76f00", "#5c3ee8"]
LINES = ['git init', 'git commit -m "ship it"', 'git push origin main', 'Talk is cheap. Show me the code.']


def pt(a, r):
    return PX + r * math.cos(math.radians(a)), PY + r * math.sin(math.radians(a))


def build(t):
    T = TH[t]
    rnd = random.Random(11)
    o = [f'<svg x="0" y="{{Y}}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<defs><pattern id="qcode" width="60" height="9" patternUnits="userSpaceOnUse"><rect x="0" y="3" width="26" height="2.4" fill="{T["code"]}"/>'
         f'<rect x="31" y="3" width="14" height="2.4" fill="#5b6cff" opacity=".7"/></pattern>'
         f'<filter id="qsh" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#000" flood-opacity=".18"/></filter></defs>',
         f'<style>.fan{{transform-origin:{PX}px {PY}px;animation:fan 7s ease-in-out infinite alternate}}'
         '@keyframes fan{from{transform:rotate(-2deg)}to{transform:rotate(1.5deg)}}</style>',
         f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>']
    # the fan of pages
    a0, a1, n = 186, 282, 46
    pages = []
    for i in range(n):
        a = a0 + (a1 - a0) * i / (n - 1)
        da = (a1 - a0) / (n - 1) * (1.6 if i % 7 else 3.2)
        r = R * (0.86 + 0.14 * rnd.random())
        p1, p2 = pt(a, r), pt(a + da, r * (0.97 + 0.05 * rnd.random()))
        poly = f"{PX},{PY} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        kind = rnd.random()
        if i % 9 == 4:
            fill = f'url(#qcode)'
            base = f'<polygon points="{poly}" fill="{T["page"]}"/>'
        elif kind < .34:
            fill, base = rnd.choice(COLORS), ""
        else:
            fill, base = T["page"], ""
        pages.append(f'{base}<polygon points="{poly}" fill="{fill}" stroke="{T["edge"]}" stroke-width="1.3" stroke-linejoin="round"/>')
    # a few pages carry git commands, written along the page
    for j, (line, a) in enumerate(zip(LINES, [208, 228, 247, 266])):
        x, y = pt(a, 170)
        size = 17 if j < 3 else 21
        pages.append(f'<text transform="translate({x:.1f} {y:.1f}) rotate({a - 180:.1f})" style="font-family:{MONO if j < 3 else SANS};'
                     f'font-size:{size}px;font-weight:{500 if j < 3 else 800};text-anchor:end;dominant-baseline:central" '
                     f'fill="{T["ink"] if t == "light" else "#0d1117"}" opacity=".9">{line}</text>')
    o.append(f'<g class="fan" filter="url(#qsh)">{"".join(pages)}</g>')
    o.append(f'<circle cx="{PX}" cy="{PY}" r="5" fill="{T["ink"]}"/>')
    # the quote
    for k, line in enumerate(["TALK IS", "CHEAP.", "SHOW ME", "THE CODE."]):
        o.append(f'<text x="44" y="{108 + k * 66}" style="font-family:{SANS};font-size:68px;font-weight:700;letter-spacing:-2.5px;'
                 f'text-anchor:start;dominant-baseline:auto" fill="{T["ink"]}">{line}</text>')
    o.append(f'<text x="46" y="{108 + 3 * 66 + 42}" style="font-family:{SANS};font-size:16px;text-anchor:start;dominant-baseline:auto" '
             f'fill="{T["muted"]}">— Linus Torvalds, creator of Linux and Git</text>')
    # the timeline
    cols = [("2005", "Linus Torvalds creates Git."), ("2008", "GitHub launches: “social coding”."),
            ("Today", "Every repo here is a page of my story.")]
    for i, (yr, text) in enumerate(cols):
        x = 44 + i * 310
        o.append(f'<text x="{x}" y="{H - 64}" style="font-family:{SANS};font-size:30px;font-weight:700;letter-spacing:-1px;text-anchor:start;'
                 f'dominant-baseline:auto" fill="{T["ink"]}">{yr}</text>')
        o.append(f'<text x="{x}" y="{H - 36}" style="font-family:{SANS};font-size:15px;text-anchor:start;dominant-baseline:auto" '
                 f'fill="{T["muted"]}">{text}</text>')
    o.append('</svg>')
    return "".join(o), H
