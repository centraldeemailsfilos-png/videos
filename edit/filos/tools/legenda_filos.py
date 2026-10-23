"""Queima legendas no estilo Filos (placa escura + barra ambar).

O libass nao faz canto arredondado nem barra lateral, entao cada deixa vira
um PNG com alpha e e composta na janela de tempo dela.
"""
import re, os, subprocess
from PIL import Image, ImageDraw, ImageFont

BOLD = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
AMBAR = (253, 179, 4, 255)
CLARO = (246, 246, 246, 255)
PLACA = (14, 16, 19, 207)

def le_srt(p):
    blocos = []
    for b in re.split(r'\n\s*\n', open(p, encoding='utf-8').read().strip()):
        L = [x for x in b.strip().split('\n') if x.strip()]
        if len(L) < 3: continue
        m = re.match(r'(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)', L[1])
        if not m: continue
        g = [int(x) for x in m.groups()]
        a = g[0]*3600 + g[1]*60 + g[2] + g[3]/1000
        z = g[4]*3600 + g[5]*60 + g[6] + g[7]/1000
        blocos.append((a, z, ' '.join(L[2:])))
    return blocos

def quebra_equilibrada(texto, f, larg_max, med):
    """Quebra em 1-2 linhas tentando deixa-las do mesmo tamanho."""
    palavras = texto.split()
    if med(texto) <= larg_max:
        return [texto]
    melhor, custo = None, None
    for i in range(1, len(palavras)):
        a, b = ' '.join(palavras[:i]), ' '.join(palavras[i:])
        la, lb = med(a), med(b)
        if max(la, lb) > larg_max: continue
        c = abs(la - lb)
        if custo is None or c < custo: melhor, custo = (a, b), c
    if melhor: return list(melhor)
    # nao coube em duas: cai para quebra simples por largura
    linhas, atual = [], ''
    for w in palavras:
        t = (atual + ' ' + w).strip()
        if atual and med(t) > larg_max: linhas.append(atual); atual = w
        else: atual = t
    if atual: linhas.append(atual)
    return linhas

def desenha(texto, larg_video, tam=None, margem=None, barra=None, raio=None):
    # tudo proporcional a largura: o mesmo desenho em 464px ou em 1080px
    tam    = tam    if tam    else max(22, round(larg_video * 0.052))
    margem = margem if margem else round(larg_video * 0.030)
    barra  = barra  if barra  else max(4, round(larg_video * 0.0085))
    raio   = raio   if raio   else round(larg_video * 0.016)
    larg_max = int(larg_video * 0.86) - margem*2 - barra
    f = ImageFont.truetype(BOLD, tam)
    tmp = ImageDraw.Draw(Image.new('RGBA', (8, 8)))
    med = lambda t: tmp.textbbox((0, 0), t, font=f)[2]
    while tam > larg_video * 0.034:
        linhas = quebra_equilibrada(texto, f, larg_max, med)
        if len(linhas) <= 2 and max(med(L) for L in linhas) <= larg_max: break
        tam -= 3
        f = ImageFont.truetype(BOLD, tam)
        med = lambda t, f=f: tmp.textbbox((0, 0), t, font=f)[2]
    larguras = [med(L) for L in linhas]
    alt_l = int(tam * 1.30)
    w = max(larguras) + margem*2 + barra
    h = alt_l*len(linhas) + int(margem*0.95)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w-1, h-1], raio, fill=PLACA)
    d.rounded_rectangle([0, 0, barra+raio, h-1], raio, fill=AMBAR)
    d.rectangle([barra, 0, barra+raio, h-1], fill=PLACA)
    y = int(margem*0.42)
    for L, lw in zip(linhas, larguras):
        d.text(((w - lw + barra)//2, y), L, font=f, fill=CLARO)
        y += alt_l
    return im

def queima(video, srt, saida, altura_rel=0.74, tam=None, crf=21, larg_saida=None):
    blocos = le_srt(srt)
    info = subprocess.run(['ffprobe','-v','error','-select_streams','v:0',
        '-show_entries','stream=width,height','-of','csv=p=0:s=x',video],
        capture_output=True, text=True).stdout.strip()
    W, H = (int(x) for x in info.split('x'))
    pre = ''
    if larg_saida and larg_saida != W:
        H = round(H * larg_saida / W / 2) * 2; W = larg_saida
        pre = f'[0:v]scale={W}:{H}:flags=lanczos,setsar=1[base];'
    tmp = os.path.join(os.path.dirname(saida) or '.', '_leg_tmp'); os.makedirs(tmp, exist_ok=True)
    ent, filt, prev = ['-i', video], [], ('[base]' if pre else '[0:v]')
    for i, (a, z, t) in enumerate(blocos):
        png = f'{tmp}/c{i:03d}.png'
        im = desenha(t, W, tam=tam)
        im.save(png); ent += ['-i', png]
        y = int(H*altura_rel) - im.height//2
        nxt = f'[v{i}]'
        filt.append(f"{prev}[{i+1}:v]overlay=(W-w)/2:{y}:enable='between(t,{a:.3f},{z:.3f})'{nxt}")
        prev = nxt
    fc = pre + (';'.join(filt) if filt else f'{prev}null[vout]')
    if filt: fc = fc[:-len(prev)] + '[vout]'
    cmd = ['ffmpeg','-v','error','-y'] + ent + ['-filter_complex', fc, '-map','[vout]']
    cmd += ['-map','0:a?','-c:v','libx264','-crf',str(crf),'-preset','medium',
            '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart', saida]
    subprocess.run(cmd, check=True)
    return len(blocos)
