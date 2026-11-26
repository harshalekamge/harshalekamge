"""Draws the daily date card (light + dark) and points the README at it."""
import calendar, datetime, glob, os, re
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = ZoneInfo("Asia/Colombo")

THEMES = {
    "light": dict(bg="#e8e6e1", ink="#141414", muted="#8c8a85", empty="#cfcdc7", today="#f26b0b"),
    "dark": dict(bg="#161b22", ink="#e6edf3", muted="#7d8590", empty="#30363d", today="#f26b0b"),
}
SANS = '"Helvetica Neue",Helvetica,Arial,sans-serif'


def card(today, t):
    T = THEMES[t]
    first_wd, ndays = calendar.monthrange(today.year, today.month)  # Monday = 0
    x0, y0, gap, r = 418, 74, 52, 18
    rows = (first_wd + ndays + 6) // 7
    W, H = 820, max(340, y0 + (rows - 1) * gap + r + 30)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="{today:%A, %d %B %Y}">',
         f'<style>.p{{transform-box:fill-box;transform-origin:center;animation:p 2.4s ease-in-out infinite}}'
         f'@keyframes p{{50%{{transform:scale(.86)}}}}@media (prefers-reduced-motion:reduce){{.p{{animation:none}}}}</style>',
         f'<rect width="{W}" height="{H}" rx="22" fill="{T["bg"]}"/>',
         f'<text x="36" y="168" font-family=\'{SANS}\' font-size="150" font-weight="700" letter-spacing="-6" fill="{T["ink"]}">{today.day}</text>',
         f'<text x="40" y="222" font-family=\'{SANS}\' font-size="22" letter-spacing="1.5" fill="{T["ink"]}">{today.strftime("%B").upper()}</text>',
         f'<text x="40" y="252" font-family=\'{SANS}\' font-size="22" fill="{T["muted"]}">{today.year}</text>',
         f'<text x="330" y="252" text-anchor="end" font-family=\'{SANS}\' font-size="24" fill="{T["ink"]}">{today:%a}</text>',
         f'<text x="40" y="{H - 28}" font-family=\'{SANS}\' font-size="11" letter-spacing="2.5" fill="{T["muted"]}">ONE COMMIT AT A TIME</text>']
    for i, d in enumerate("MTWTFSS"):
        o.append(f'<text x="{x0 + i * gap}" y="42" text-anchor="middle" font-family=\'{SANS}\' font-size="11" fill="{T["muted"]}">{d}</text>')
    for day in range(1, ndays + 1):
        idx = first_wd + day - 1
        cx, cy = x0 + (idx % 7) * gap, y0 + (idx // 7) * gap
        if day < today.day:
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{T["ink"]}"/>')
        elif day == today.day:
            o.append(f'<circle class="p" cx="{cx}" cy="{cy}" r="{r}" fill="{T["today"]}"/>')
        else:
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 1}" fill="none" stroke="{T["empty"]}" stroke-width="2"/>')
    o.append("</svg>")
    return "\n".join(o)


def main():
    today = datetime.datetime.now(TZ).date()
    stamp = today.isoformat()
    for f in glob.glob(os.path.join(ROOT, "assets", "date-*.svg")):
        os.remove(f)
    for t in THEMES:
        with open(os.path.join(ROOT, "assets", f"date-{stamp}-{t}.svg"), "w") as fh:
            fh.write(card(today, t))
    readme = os.path.join(ROOT, "README.md")
    s = open(readme, encoding="utf-8").read()
    s = re.sub(r"date-\d{4}-\d{2}-\d{2}-(light|dark)\.svg", lambda m: f"date-{stamp}-{m.group(1)}.svg", s)
    open(readme, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main()
