"""Closing section: name, link columns and a giant 'harsha' rising out of green hills (light + dark)."""

SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
TH = {
    "light": dict(top="#ffffff", sky1="#f3f3f3", sky2="#9fd8f5", sky3="#4fb4ec", ink="#141414", muted="#5c5c5c",
                  word="#ffffff", wordo=".96", cloud="#ffffff", cloudo=".85", h1a="#7cc35a", h1b="#3f8f33", h2a="#5fb447",
                  h2b="#2e7d2a", h3a="#4ea83b", h3b="#1f6a22", stars="0"),
    "dark": dict(top="#0d1117", sky1="#0d1117", sky2="#14244a", sky3="#1d3770", ink="#e6edf3", muted="#9da7b3",
                 word="#e6edf3", wordo=".9", cloud="#8fa3c7", cloudo=".18", h1a="#24502a", h1b="#163a1c", h2a="#1d4523",
                 h2b="#112e16", h3a="#173b1d", h3b="#0b2210", stars="1"),
}
W, H = 1000, 640


def txt(x, y, s, size, fill, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" style="font-family:{SANS};font-size:{size}px;font-weight:{weight};'
            f'text-anchor:{anchor};dominant-baseline:auto;{extra}" fill="{fill}">{s}</text>')


ICONS = {
    "github": ('M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 '
               '1.8 1.2 1 1.8 2.8 1.3 3.5 1 0-.8.4-1.3.7-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.2.5-2.3 1.3-3.1-.2-.4-.6-1.6 0-3.2 0 0 1-.3 3.3 '
               '1.2a11.5 11.5 0 0 1 6 0C17.3 4.3 18.3 4.6 18.3 4.6c.6 1.6.2 2.8.1 3.2.8.8 1.3 1.9 1.3 3.1 0 4.6-2.8 5.6-5.5 5.9.4.4.8 '
               '1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3', "fill"),
    "whatsapp": ('M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z'
                 'm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4'
                 'l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.6 11.6 0 0 0 4.4 3.9c1.6.7 '
                 '2.3.8 3.1.6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .1-1.2c0-.1-.2-.2-.5-.3z', "fill"),
    "mail": ('M3 5h18v14H3zM3 6l9 7 9-7', "stroke"),
    "globe": ('M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM2 12h20M12 2c-3 3-3 17 0 20M12 2c3 3 3 17 0 20', "stroke"),
}


def icon(name, x, y, col):
    d, mode = ICONS[name]
    if mode == "fill":
        return f'<path transform="translate({x} {y}) scale(.8)" fill="{col}" d="{d}"/>'
    return f'<path transform="translate({x} {y}) scale(.8)" fill="none" stroke="{col}" stroke-width="1.9" stroke-linejoin="round" d="{d}"/>'


def build(t, year):
    T = TH[t]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="Harsha Lekamge — Software Engineer, Data Science at SLIIT. © {year} Harsha Lekamge.">',
         '<defs>'
         f'<linearGradient id="bsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["top"]}"/><stop offset=".3" stop-color="{T["sky1"]}"/>'
         f'<stop offset=".55" stop-color="{T["sky2"]}"/><stop offset=".85" stop-color="{T["sky3"]}"/></linearGradient>'
         f'<linearGradient id="bh1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["h1a"]}"/><stop offset="1" stop-color="{T["h1b"]}"/></linearGradient>'
         f'<linearGradient id="bh2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["h2a"]}"/><stop offset="1" stop-color="{T["h2b"]}"/></linearGradient>'
         f'<linearGradient id="bh3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["h3a"]}"/><stop offset="1" stop-color="{T["h3b"]}"/></linearGradient>'
         '<filter id="bcl" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>'
         '<filter id="bgr" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9 .35" numOctaves="2" seed="4"/>'
         '<feColorMatrix values="0 0 0 0 0  0 0 0 0 .25  0 0 0 0 0  0 0 0 -1.4 1.1"/><feComposite in2="SourceGraphic" operator="in"/></filter>'
         '</defs>'
         '<style>.cl{animation:cl 40s linear infinite alternate}.cl2{animation:cl 55s linear infinite alternate-reverse}'
         '@keyframes cl{from{transform:translateX(-40px)}to{transform:translateX(40px)}}'
         '.tw{animation:tw 3s ease-in-out infinite alternate}@keyframes tw{from{opacity:.25}to{opacity:1}}</style>',
         f'<rect width="{W}" height="{H}" fill="url(#bsky)"/>']
    if T["stars"] == "1":
        import random
        rnd = random.Random(7)
        o.append('<g fill="#ffffff">' + "".join(
            f'<circle class="tw" style="animation-delay:{-rnd.random() * 3:.1f}s" cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(250, 470):.0f}" r="{rnd.uniform(.6, 1.6):.1f}"/>'
            for _ in range(70)) + '</g>')
    # clouds
    for cls, blobs in (("cl", [(80, 360, 70, 26), (130, 345, 50, 30), (40, 380, 60, 18), (870, 330, 80, 24), (930, 350, 60, 22)]),
                       ("cl2", [(420, 300, 60, 16), (470, 292, 40, 18), (640, 380, 70, 20), (700, 370, 46, 22)])):
        o.append(f'<g class="{cls}" filter="url(#bcl)" fill="{T["cloud"]}" opacity="{T["cloudo"]}">' +
                 "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>' for x, y, rx, ry in blobs) + '</g>')
    # giant name, partly behind the hills
    o.append(f'<text x="{W / 2}" y="548" textLength="900" lengthAdjust="spacingAndGlyphs" style="font-family:{SANS};font-size:300px;'
             f'font-weight:600;letter-spacing:-10px;text-anchor:middle;dominant-baseline:auto" fill="{T["word"]}" opacity="{T["wordo"]}">harsha</text>')
    # hills, back to front, with a grass texture
    hills = [("bh1", "M0 545C150 505 300 505 430 528S720 505 860 518 1000 505 1000 505V640H0Z"),
             ("bh2", "M0 578C180 535 360 550 520 570S820 552 1000 566V640H0Z"),
             ("bh3", "M0 618C200 585 420 595 600 612S880 605 1000 595V640H0Z")]
    for g, d in hills:
        o.append(f'<path d="{d}" fill="url(#{g})"/><path d="{d}" fill="#000" filter="url(#bgr)" opacity=".5"/>')
    # top content
    o.append(f'<rect x="44" y="52" width="40" height="40" rx="10" fill="{T["ink"]}"/>')
    o.append(txt(64, 79, "HL", 16, T["top"], 700, "middle"))
    o.append(txt(96, 82, "Harsha Lekamge", 25, T["ink"], 500, extra="letter-spacing:-.5px"))
    o.append(txt(44, 126, "Software engineer and Data Science undergraduate", 14.5, T["muted"]))
    o.append(txt(44, 147, "at SLIIT — building software that ships.", 14.5, T["muted"]))
    for i, n in enumerate(["github", "whatsapp", "mail", "globe"]):
        o.append(icon(n, 44 + i * 32, 172, T["ink"]))
    cols = [("Work", ["Smart Campus", "Kola Vision", "GreenCycle.lk", "File Tracking"]),
            ("Skills", ["Web Apps", "AI &amp; Vision", "Data Science", "UI Design"]),
            ("Connect", ["Portfolio", "WhatsApp", "Email", "GitHub"]),
            ("Studying", ["SLIIT", "BSc (Hons) IT", "Data Science"])]
    for i, (head, items) in enumerate(cols):
        x = 470 + i * 135
        o.append(txt(x, 78, head, 15.5, T["ink"], 600))
        for j, it in enumerate(items):
            o.append(txt(x, 113 + j * 33, it, 14, T["muted"]))
    o.append(txt(470, 278, f"© {year} Harsha Lekamge.", 14, T["ink"], 500))
    o.append('</svg>')
    return "".join(o)
