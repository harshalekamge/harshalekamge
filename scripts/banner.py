"""Koi pond banner (light + dark)."""
import math, random
S=12  # cell
TH={'light':dict(bg1='#ffffff',bg2='#ffffff',grid='#e6e6e3',ink='#1c1c1c',muted='#8a8a8a',card='#ffffff',cardo='.86',cstroke='#e4e4e2',chip='#ffffff',chipo='.7',chipt='#6b6b6b',btn='#ececec',btnt='#333',
             cream='#f1efea',creamc='#9c9a94',pale='#e3e2de',palec='#b5b3ad',black='#2a2a2a',blackc='#9a9a9a',orange='#e2582a',orangec='#ffd6c4',yellow='#d6b21c',yellowc='#fff3b0'),
    'dark':dict(bg1='#0d1117',bg2='#0a0d12',grid='#161c25',ink='#e6edf3',muted='#7d8590',card='#161b22',cardo='.88',cstroke='#30363d',chip='#161b22',chipo='.8',chipt='#9da7b3',btn='#21262d',btnt='#c9d1d9',
             cream='#c9cfd6',creamc='#5d6570',pale='#2a313b',palec='#59626e',black='#05070a',blackc='#59626e',orange='#e2582a',orangec='#ffd6c4',yellow='#d6b21c',yellowc='#fff3b0')}
def fish_cells(seed,kind,L=20,H=7.5,tail=7):
    rnd=random.Random(seed); cells=[]
    spots=[(rnd.uniform(.15,.95),rnd.uniform(-.6,.6),rnd.uniform(.12,.22),rnd.choice(['orange','orange','black'] if kind=='kohaku' else (['black','orange','orange'] if kind=='showa' else ['yellow']))) for _ in range(5)]
    for i in range(0,L+1):
        t=i/L
        if i>=0:
            h=H*(max(t,0.001)**0.55)*((1-t)**0.3) if t<1 else 0.6
            h=max(h,1.2)
        else:
            u=-i/tail; h=1.0+2.8*u
        for j in range(-8,9):
            y=j
            if i<0 and abs(y)<1.2*(-i/tail)*2 and -i>tail*0.6: continue  # fork
            d=abs(y)/h
            if d>1.08: continue
            edge=d>0.82 or i<0
            col='cream'
            if i>=0 and not edge:
                for (sx,sy,r,c) in spots:
                    if (t-sx)**2/(r*r)+((y/H)-sy)**2/(r*r*3)<1: col=c
                if kind=='yamabuki': col='yellow' if col=='cream' else col
            if i<0 or edge:
                col='pale' if rnd.random()<.75 else ('orange' if kind!='yamabuki' and rnd.random()<.4 else ('yellow' if kind=='yamabuki' else 'cream'))
            if i<0 and rnd.random()<.25: continue
            cells.append((i,y,col,i<0))
    # shark-style crescent tail: two swept-back lobes, the upper one longer
    def tcol(k,n):
        if k>=n-1: return 'pale'
        r=rnd.random()
        if kind=='yamabuki': return 'yellow' if r<.6 else 'pale'
        return 'orange' if r<.45 else ('pale' if r<.8 else 'cream')
    for y in (-1,0,1): cells.append((-1,y,tcol(0,9),True))
    for k in range(1,8):
        for y in (-1-round(k*.85),-round(k*.85)): cells.append((-1-k,y,tcol(k,8),True))
    for k in range(1,6):
        for y in (1+round(k*.85),round(k*.85)): cells.append((-1-k,y,tcol(k,6),True))
    # pectoral fins: the top pair as before; the bottom pair sweeps back like a fin
    for (fx,fy) in [(13,-5),(14,-5),(14,-6),(13,-6)]:
        if fx<=L: cells.append((fx,fy,'pale',False))
    e=int(1.08*max(H*((13/L)**0.55)*((1-13/L)**0.3),1.2))
    for k,xs in ((1,range(11,15)),(2,range(10,13)),(3,range(9,11))):
        for fx in xs: cells.append((fx,e+k,'pale',False))
    return cells
CH={'cream':':.x:.:','pale':'..::','orange':'ZXZ%Z','black':'X#X','yellow':'ZXZ'}
def fish(T,cells,seed,cls,tid):
    rnd=random.Random(seed+7); body=[]; tail=[]
    for (i,y,col,ist) in cells:
        x=i*S; yy=y*S
        ch=rnd.choice(CH[col])
        s=f'<rect x="{x}" y="{yy}" width="{S-1}" height="{S-1}" rx="2" fill="{T[col]}"/><text x="{x+5.5}" y="{yy+8.5}" fill="{T[col+"c"]}">{ch}</text>'
        (tail if ist else body).append(s)
    return f'<g class="{cls}"><g class="tail">{"".join(tail)}</g>{"".join(body)}<rect x="{17*S+3}" y="{-2*S+3}" width="5" height="5" fill="{T["black"]}"/></g>'
def build(t, overlay=''):
    T=TH[t]; o=[]; a=o.append
    W,Hh=1000,460
    a(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" role="img" aria-label="Animated koi pond banner: Dive into my code.">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T['bg2']}"/><stop offset=".35" stop-color="{T['bg1']}"/><stop offset="1" stop-color="{T['bg2']}"/></linearGradient>
<pattern id="g" width="{S}" height="{S}" patternUnits="userSpaceOnUse"><path d="M{S} 0H0V{S}" fill="none" stroke="{T['grid']}" stroke-width="1"/></pattern>
<filter id="sh" x="-10%" y="-30%" width="120%" height="170%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000" flood-opacity="{'.10' if t=='light' else '.5'}"/></filter>

</defs>
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:8px;text-anchor:middle}}
.h{{font-family:Inter,"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:66px;letter-spacing:-2.5px;fill:{T['ink']};text-anchor:middle}}
.q{{font-family:Inter,"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;fill:{T['ink']};text-anchor:start}}
.hint{{font-size:12.5px;fill:{T['muted']};text-anchor:start}}
.chip{{font-family:Inter,"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:15px;fill:{T['chipt']};text-anchor:middle}}
.tail{{transform-box:fill-box;transform-origin:100% 50%;animation:wag 1.1s ease-in-out infinite alternate}}
@keyframes wag{{from{{transform:rotate(-9deg)}}to{{transform:rotate(9deg)}}}}
.sway{{transform-box:fill-box;transform-origin:50% 50%;animation:sway 3.2s ease-in-out infinite alternate}}
@keyframes sway{{from{{transform:translateY(-10px) rotate(-3deg)}}to{{transform:translateY(10px) rotate(3deg)}}}}
.swimR{{animation:swimR linear infinite}} @keyframes swimR{{from{{transform:translateX(-420px)}}to{{transform:translateX(1100px)}}}}
.swimL{{animation:swimL linear infinite}} @keyframes swimL{{from{{transform:translateX(1420px)}}to{{transform:translateX(-100px)}}}}
.typing{{transform-box:fill-box;transform-origin:0 0;animation:ty 9s steps(27) infinite}}
@keyframes ty{{0%{{transform:scaleX(0)}}30%,92%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
.cur{{animation:bl 1s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}
</style>
<rect width="{W}" height="{Hh}" fill="url(#bg)"/><rect width="{W}" height="{Hh}" fill="url(#g)"/>''')
    import koi
    a(koi.build(t))
    # headline + card
    a(f'<defs><radialGradient id="haze" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{T["bg1"]}" stop-opacity=".9"/><stop offset="1" stop-color="{T["bg1"]}" stop-opacity="0"/></radialGradient></defs>'
      '<ellipse cx="500" cy="250" rx="380" ry="190" fill="url(#haze)"/>')
    a(f'<text class="h" x="500" y="186">Dive into my code.</text>')
    a(f'<g filter="url(#sh)"><rect x="240" y="226" width="520" height="104" rx="18" fill="{T["card"]}" fill-opacity="{T["cardo"]}" stroke="{T["cstroke"]}"/></g>')
    a(f'<text class="q" x="266" y="272">What is Harsha building next?</text>')
    a(f'<rect class="cur" x="520" y="256" width="2" height="21" fill="{T["ink"]}"/>')
    a(f'<text class="hint" x="266" y="310">esc clear · ↵ ship</text>')
    a(f'<circle cx="726" cy="303" r="17" fill="{T["btn"]}"/><path d="M726 311v-15M719 302l7-7 7 7" fill="none" stroke="{T["btnt"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    chips=[('Web platforms',160),('Vision AI for accessibility',250),('AI agents',130)]
    gap=14; total=sum(w for _,w in chips)+gap*2; x=500-total/2
    for label,w in chips:
        a(f'<rect x="{x}" y="352" width="{w}" height="38" rx="19" fill="{T["chip"]}" fill-opacity="{T["chipo"]}" stroke="{T["cstroke"]}"/><text class="chip" x="{x+w/2}" y="376">{label}</text>')
        x+=w+gap
    a(overlay)
    a('</svg>')
    return '\n'.join(o)
