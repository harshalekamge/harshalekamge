"""Draws the contact pills (light + dark) used under the banner."""
import os
from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "pills")
VER = "v1"
FONT = "Inter,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
_F = {w: "/usr/share/fonts/opentype/inter/Inter-%s.otf" % ("SemiBold" if w == 600 else "Regular") for w in (400, 600)}
H, R, PAD = 60, 20, 14  # pill height, corner radius, room for the shadow

T = {
    "light": dict(card="#ffffff", soft="#ececec", ink="#141414", text="#4f4f4f", muted="#8a8a8a", line="#c4c4c4",
                  green="#c8f1d6", greent="#23944b", blue="#f3f7ff", bluet="#2f7fd8", sh=".09", av="#141414", avt="#ffffff"),
    "dark": dict(card="#161b22", soft="#21262d", ink="#e6edf3", text="#c9d1d9", muted="#7d8590", line="#3d444d",
                 green="#12361f", greent="#3fb950", blue="#0d2340", bluet="#58a6ff", sh=".5", av="#e6edf3", avt="#0d1117"),
}


def tw(s, size, weight=400):
    return ImageFont.truetype(_F[weight], size).getlength(s)


def svg(w, body, t, glow=False):
    c = T[t]
    W, Hh = w + 2 * PAD, H + 2 * PAD
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}">'
            f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb36b"/>'
            f'<stop offset=".45" stop-color="#ff7aa8"/><stop offset="1" stop-color="#5b6cff"/></linearGradient>'
            f'<radialGradient id="g2" cx=".9" cy=".05" r=".8"><stop offset="0" stop-color="#ffd9bd"/>'
            f'<stop offset="1" stop-color="#ff8a9e" stop-opacity="0"/></radialGradient>'
            f'<filter id="s" x="-20%" y="-40%" width="140%" height="190%"><feDropShadow dx="0" dy="4" stdDeviation="6" '
            f'flood-color="#000" flood-opacity="{c["sh"]}"/></filter>'
            f'<filter id="gl" x="-20%" y="-40%" width="140%" height="200%"><feDropShadow dx="0" dy="6" stdDeviation="8" '
            f'flood-color="#6b6bff" flood-opacity=".35"/></filter></defs>'
            f'<style>text{{font-family:{FONT};dominant-baseline:central}}'
            f'.spin{{transform-box:fill-box;transform-origin:center;animation:sp 6s linear infinite}}'
            f'@keyframes sp{{to{{transform:rotate(360deg)}}}}</style>'
            f'<g transform="translate({PAD} {PAD})">{body}</g></svg>')


def grad_rect(x, y, w, h, r, ring=True):
    ring_s = f' stroke="#ffffff" stroke-width="3"' if ring else ""
    return (f'<g filter="url(#gl)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#g)"{ring_s}/></g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#g2)"/>')


def card(w, fill, t, shadow=True, extra=""):
    f = ' filter="url(#s)"' if shadow else ""
    return f'<rect x="0" y="0" width="{w}" height="{H}" rx="{R}" fill="{fill}"{f}{extra}/>'


def mid(y=H / 2):
    return y + 1


PILLS = {}


def pill(name):
    def deco(fn):
        PILLS[name] = fn
        return fn
    return deco


@pill("name")
def _(t):
    label = "Harsha Lekamge"
    w = 64 + tw(label, 20, 600) + 26
    star = ('<path d="M30 20l3.6 9.4 9.4 3.6-9.4 3.6-3.6 9.4-3.6-9.4-9.4-3.6 9.4-3.6z'
            'M44 14l1.8 4.7 4.7 1.8-4.7 1.8-1.8 4.7-1.8-4.7-4.7-1.8 4.7-1.8z" fill="#fff"/>')
    return w, grad_rect(0, 0, w, H, R) + star + f'<text x="62" y="{mid()}" font-size="20" font-weight="600" fill="#fff">{label}</text>', True


@pill("degree")
def _(t):
    c = T[t]
    a, b = "BSc (Hons) in Information Technology", "Specialised in Data Science"
    w = 74 + max(tw(a, 16, 600), tw(b, 13.5)) + 26
    return w, (card(w, c["card"], t) + f'<circle cx="34" cy="30" r="19" fill="{c["av"]}"/>'
               f'<text x="34" y="{mid()}" font-size="13" font-weight="700" fill="{c["avt"]}" text-anchor="middle">HL</text>'
               f'<text x="66" y="21" font-size="16" font-weight="600" fill="{c["ink"]}">{a}</text>'
               f'<text x="66" y="42" font-size="13.5" fill="{c["muted"]}">{b}</text>'), False


@pill("portfolio")
def _(t):
    c = T[t]
    w = 60 + tw("Portfolio", 19) + 44
    globe = (f'<g fill="none" stroke="{c["text"]}" stroke-width="2" stroke-linecap="round"><circle cx="33" cy="30" r="11"/>'
             f'<path d="M22 30h22M33 19c-5 6-5 16 0 22M33 19c5 6 5 16 0 22"/></g>')
    arrow = f'<path d="M{w-34} 36l9-9M{w-32} 27h7v7" fill="none" stroke="{c["bluet"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    return w, (f'<rect x="1" y="1" width="{w-2}" height="{H-2}" rx="{R}" fill="none" stroke="{c["line"]}" stroke-width="2" stroke-dasharray="7 6"/>'
               + globe + f'<text x="54" y="{mid()}" font-size="19" fill="{c["text"]}">Portfolio</text>' + arrow), False


@pill("focus")
def _(t):
    c = T[t]
    labels = ["Web", "AI", "Data"]
    seg = [tw(s, 16, 600) + 32 for s in labels]
    w = sum(seg) + 12
    o = [card(w, c["soft"], t, shadow=False)]
    x = 6
    for i, (s, sw) in enumerate(zip(labels, seg)):
        if i == 0:
            o.append(f'<rect x="{x}" y="6" width="{sw}" height="{H-12}" rx="15" fill="{c["card"]}" filter="url(#s)"/>')
        o.append(f'<text x="{x + sw/2}" y="{mid()}" font-size="16" font-weight="{600 if i == 0 else 400}" '
                 f'fill="{c["ink"] if i == 0 else c["muted"]}" text-anchor="middle">{s}</text>')
        x += sw
    return w, "".join(o), False


@pill("whatsapp")
def _(t):
    c = T[t]
    num, btn = "+94 77 875 3792", "WhatsApp"
    bw = tw(btn, 15, 600) + 34
    w = 22 + tw(num, 17) + 18 + bw + 6
    bx = w - bw - 6
    return w, (card(w, c["card"], t) + f'<text x="22" y="{mid()}" font-size="17" fill="{c["ink"]}">{num}</text>'
               + grad_rect(bx, 7, bw, H - 14, 15, ring=False)
               + f'<text x="{bx + bw/2}" y="{mid()}" font-size="15" font-weight="600" fill="#fff" text-anchor="middle">{btn}</text>'), True


@pill("github")
def _(t):
    c = T[t]
    mark = ('M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 '
            '1 1.8 2.8 1.3 3.5 1 0-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.2.5-2.3 1.3-3.1-.2-.4-.6-1.6 0-3.2 0 0 1-.3 3.3 1.2a11.5 '
            '11.5 0 0 1 6 0C17.3 4.3 18.3 4.6 18.3 4.6c.6 1.6.2 2.8.1 3.2.8.8 1.3 1.9 1.3 3.1 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 '
            '.3.2.7.8.6A12 12 0 0 0 12 .3')
    return H, card(H, c["card"], t) + f'<path transform="translate(18 18)" fill="{c["text"]}" d="{mark}"/>', False


@pill("location")
def _(t):
    c = T[t]
    w = 46 + tw("Colombo", 18, 600) + 24
    return w, (card(w, c["green"], t, shadow=False) + f'<circle cx="27" cy="30" r="5" fill="{c["greent"]}"/>'
               f'<text x="42" y="{mid()}" font-size="18" font-weight="600" fill="{c["greent"]}">Colombo</text>'), False


@pill("kola")
def _(t):
    c = T[t]
    w = 60 + tw("Building Kola", 18, 600) + 24
    return w, (card(w, c["blue"], t) + f'<circle class="spin" cx="31" cy="30" r="12" fill="none" stroke="{c["bluet"]}" '
               f'stroke-width="3" stroke-dasharray="5 4.4" stroke-linecap="round"/>'
               f'<text x="54" y="{mid()}" font-size="18" font-weight="600" fill="{c["bluet"]}">Building Kola</text>'), False


def mail(label):
    def f(t):
        c = T[t]
        w = 22 + tw(label, 16) + 16 + 46 + 7
        cx = w - 30
        return w, (card(w, c["soft"], t, shadow=False) + f'<text x="22" y="{mid()}" font-size="16" fill="{c["text"]}">{label}</text>'
                   f'<circle cx="{cx}" cy="30" r="23" fill="{c["card"]}" filter="url(#s)"/>'
                   f'<g fill="none" stroke="{c["text"]}" stroke-width="2" stroke-linejoin="round"><rect x="{cx-10}" y="23" width="20" height="14" rx="2.5"/>'
                   f'<path d="M{cx-10} 25l10 7 10-7"/></g>'), False
    return f


PILLS["mail-official"] = mail("harshalekamge.official@gmail.com")
PILLS["mail-personal"] = mail("lekamge.h2024@gmail.com")


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    for name, fn in PILLS.items():
        for t in T:
            w, body, glow = fn(t)
            with open(os.path.join(OUT, f"{name}-{VER}-{t}.svg"), "w") as fh:
                fh.write(svg(round(w), body, t, glow))


if __name__ == "__main__":
    main()
