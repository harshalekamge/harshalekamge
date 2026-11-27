"""Draws today's banner: koi pond with a date card, then points the README at it."""
import base64, calendar, hashlib, datetime, glob, os, re, sys
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banner
import contact
import showcase
import tools
import shelf
import codeposter
import footer
import bottom as closing

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


def gap_grids(t, y, h):
    """Banner's fine grid fades out while the poster's big squares fade in, inside the gap."""
    fine = banner.TH[t]["grid"]
    big = "#bdb8ad" if t == "light" else "#262c36"
    k = 1000 / 820                  # poster scale
    x0, cell = 20 * k, 60 * k       # poster grid origin and cell size
    y2 = y + h + x0 + 1              # down to the poster's top frame line
    cols = "".join(f'<line x1="{x0 + i * cell:.1f}" y1="{y}" x2="{x0 + i * cell:.1f}" y2="{y2:.1f}"/>' for i in range(14))
    return (f'<defs><pattern id="gfine" width="5" height="5" patternUnits="userSpaceOnUse">'
            f'<path d="M5 0H0V5" fill="none" stroke="{fine}" stroke-width=".6"/></pattern>'
            f'<linearGradient id="gfo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="gfi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>'
            f'<mask id="mfo" maskContentUnits="userSpaceOnUse"><rect x="0" y="{y}" width="1000" height="{h}" fill="url(#gfo)"/></mask>'
            f'<mask id="mfi" maskContentUnits="userSpaceOnUse"><rect x="0" y="{y}" width="1000" height="{y2 - y:.1f}" fill="url(#gfi)"/></mask></defs>'
            f'<rect x="0" y="{y}" width="1000" height="{h}" fill="url(#gfine)" mask="url(#mfo)"/>',
            f'<g stroke="{big}" stroke-width="{k:.2f}" mask="url(#mfi)">{cols}</g>')


def main():
    today = datetime.datetime.now(TZ).date()
    stamp = today.isoformat()
    for f in glob.glob(os.path.join(ROOT, "assets", "profile-*.svg")) + glob.glob(os.path.join(ROOT, "assets", "footer-*.svg")) + glob.glob(os.path.join(ROOT, "assets", "bottom-*.svg")):
        os.remove(f)
    out, feet, ends = {}, {}, {}
    for t in banner.TH:
        top = banner.build(t, date_card(today, t))
        with open(os.path.join(ROOT, "assets", f"stack-{t}.svg"), "rb") as fh:
            bottom = base64.b64encode(fh.read()).decode()
        ph = 1000 * 1000 / 820  # poster is 820x1000, scaled to the banner's width
        gap = 70
        fine_g, big_g = gap_grids(t, 459, 72)
        a, b = banner.TH[t]["bg2"], ("#ffffff" if t == "light" else "#0d1117")
        y = 460
        parts = [f'<linearGradient id="gapg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/>'
                 f'<stop offset="1" stop-color="{b}"/></linearGradient>'
                 f'<rect x="0" y="{y - 1}" width="1000" height="{gap + 2}" fill="url(#gapg)"/>'
                 + fine_g]
        y += gap
        tl, th = tools.build(t)
        parts.append(tl.replace("{Y}", f"{y:.1f}"))
        y += th - 1
        bs, bh = shelf.build(t)
        parts.append(bs.replace("{Y}", f"{y:.1f}"))
        y += bh - 1
        qs, qh = codeposter.build(t)
        parts.append(qs.replace("{Y}", f"{y:.1f}"))
        y += qh - 1
        parts.append(f'<rect x="0" y="{y:.1f}" width="1000" height="{gap + 2}" fill="{b}"/>')
        y += gap
        sc, sh = showcase.build(t)
        parts.append(sc.replace("{Y}", f"{y:.1f}"))
        y += sh - 1
        parts.append(f'<rect x="0" y="{y:.1f}" width="1000" height="{gap + 2}" fill="{b}"/>')
        y += gap
        cs, ch = contact.build(t)
        parts.append(cs.replace("{Y}", f"{y:.1f}"))
        total = y + ch
        ft, fh = footer.build(t)
        feet[t] = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {fh}" width="1000" height="{fh}" role="img" '
                   f'aria-label="Let\u2019s build something lasting. Visit portfolio.harshalekamge.com">{ft.replace("{Y}", "0")}</svg>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {total:.1f}" width="1000" height="{total:.1f}" '
               f'role="img" aria-label="Dive into my code. Many tools, one calm workflow. Things I have built.">'
               f'{top}{"".join(parts)}</svg>')
        out[t] = svg
        ends[t] = closing.build(t, today.year)
    tag = hashlib.sha1(("".join(out.values()) + "".join(feet.values()) + "".join(ends.values())).encode()).hexdigest()[:6]
    name = f"profile-{stamp}-{tag}"
    for t, svg in out.items():
        with open(os.path.join(ROOT, "assets", f"{name}-{t}.svg"), "w") as fh:
            fh.write(svg)
        with open(os.path.join(ROOT, "assets", f"footer-{stamp}-{tag}-{t}.svg"), "w") as fh:
            fh.write(feet[t])
        with open(os.path.join(ROOT, "assets", f"bottom-{stamp}-{tag}-{t}.svg"), "w") as fh:
            fh.write(ends[t])
    readme = os.path.join(ROOT, "README.md")
    s = open(readme, encoding="utf-8").read()
    s = re.sub(r"profile-\d{4}-\d{2}-\d{2}(?:-[0-9a-f]{6})?-(light|dark)\.svg", lambda m: f"{name}-{m.group(1)}.svg", s)
    s = re.sub(r"footer-\d{4}-\d{2}-\d{2}-[0-9a-f]{6}-(light|dark)\.svg", lambda m: f"footer-{stamp}-{tag}-{m.group(1)}.svg", s)
    s = re.sub(r"bottom-\d{4}-\d{2}-\d{2}-[0-9a-f]{6}-(light|dark)\.svg", lambda m: f"bottom-{stamp}-{tag}-{m.group(1)}.svg", s)
    open(readme, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main()
