"""Draws today's banner: koi pond with a date card, then points the README at it."""
import base64, calendar, hashlib, datetime, glob, os, re, sys
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banner
import contact
import showcase
import tools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = ZoneInfo("Asia/Colombo")
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
CARD = {
    "light": dict(bg="#e8e6e1", line="#d6d3cc", ink="#141414", muted="#8c8a85", empty="#c9c6bf", today="#f26b0b", sh=".12"),
    "dark": dict(bg="#161b22", line="#30363d", ink="#e6edf3", muted="#7d8590", empty="#3a414b", today="#f26b0b", sh=".5"),
}


def date_card(today, t, x=26, y=26, w=176):
    T = CARD[t]
    first_wd, ndays = calendar.monthrange(today.year, today.month)  # Monday = 0
    rows = (first_wd + ndays + 6) // 7
    gap, r = 22, 7.5
    gx0, gy0 = x + 22, y + 156
    h = (gy0 - y) + (rows - 1) * gap + r + 18
    o = [f'<filter id="dsh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="{T["sh"]}"/></filter>',
         f'<style>.p{{transform-box:fill-box;transform-origin:center;animation:p 2.4s ease-in-out infinite}}@keyframes p{{50%{{transform:scale(.8)}}}}</style>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{T["bg"]}" stroke="{T["line"]}" filter="url(#dsh)"/>',
         f'<text x="{x + 18}" y="{y + 70}" style="font-family:{SANS};font-size:64px;font-weight:700;letter-spacing:-3px;text-anchor:start" fill="{T["ink"]}">{today.day}</text>',
         f'<text x="{x + 20}" y="{y + 96}" style="font-family:{SANS};font-size:12px;letter-spacing:1px;text-anchor:start" fill="{T["ink"]}">{today.strftime("%B").upper()}</text>',
         f'<text x="{x + 20}" y="{y + 113}" style="font-family:{SANS};font-size:12px;text-anchor:start" fill="{T["muted"]}">{today.year}</text>',
         f'<text x="{x + w - 18}" y="{y + 113}" style="font-family:{SANS};font-size:13px;text-anchor:end" fill="{T["ink"]}">{today:%a}</text>',
         f'<line x1="{x}" y1="{y + 128}" x2="{x + w}" y2="{y + 128}" stroke="{T["line"]}"/>']
    for i, d in enumerate("MTWTFSS"):
        o.append(f'<text x="{gx0 + i * gap}" y="{y + 143}" style="font-family:{SANS};font-size:7px;text-anchor:middle" fill="{T["muted"]}">{d}</text>')
    for day in range(1, ndays + 1):
        idx = first_wd + day - 1
        cx, cy = gx0 + (idx % 7) * gap, gy0 + (idx // 7) * gap
        if day < today.day:
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{T["ink"]}"/>')
        elif day == today.day:
            o.append(f'<circle class="p" cx="{cx}" cy="{cy}" r="{r}" fill="{T["today"]}"/>')
        else:
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{r - .7}" fill="none" stroke="{T["empty"]}" stroke-width="1.4"/>')
    return "".join(o)


def main():
    today = datetime.datetime.now(TZ).date()
    stamp = today.isoformat()
    for f in glob.glob(os.path.join(ROOT, "assets", "profile-*.svg")):
        os.remove(f)
    out = {}
    for t in banner.TH:
        top = banner.build(t, date_card(today, t))
        with open(os.path.join(ROOT, "assets", f"stack-{t}.svg"), "rb") as fh:
            bottom = base64.b64encode(fh.read()).decode()
        ph = 1000 * 1000 / 820  # poster is 820x1000, scaled to the banner's width
        tl, th = tools.build(t)
        tl = tl.replace("{Y}", f"{460 + ph - 1:.1f}")
        sc, sh = showcase.build(t)
        sc = sc.replace("{Y}", f"{460 + ph - 1 + th - 1:.1f}")
        cs, ch = contact.build(t)
        cs = cs.replace("{Y}", f"{460 + ph - 1 + th - 1 + sh - 1:.1f}")
        total = 460 + ph + th - 1 + sh - 1 + ch - 1
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {total:.1f}" width="1000" height="{total:.1f}" '
               f'role="img" aria-label="Dive into my code. Everything around you that you call life was made up by people that were no smarter than you.">'
               f'{top}'
               f'<image x="0" y="460" width="1000" height="{ph:.1f}" href="data:image/svg+xml;base64,{bottom}"/>{tl}{sc}{cs}</svg>')
        out[t] = svg
    tag = hashlib.sha1("".join(out.values()).encode()).hexdigest()[:6]
    name = f"profile-{stamp}-{tag}"
    for t, svg in out.items():
        with open(os.path.join(ROOT, "assets", f"{name}-{t}.svg"), "w") as fh:
            fh.write(svg)
    readme = os.path.join(ROOT, "README.md")
    s = open(readme, encoding="utf-8").read()
    s = re.sub(r"profile-\d{4}-\d{2}-\d{2}(?:-[0-9a-f]{6})?-(light|dark)\.svg", lambda m: f"{name}-{m.group(1)}.svg", s)
    open(readme, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main()
