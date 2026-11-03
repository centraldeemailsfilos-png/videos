"""Autoavaliacao do video montado, antes de mostrar para alguem.

Passo 7 do processo no CLAUDE.md: olhar o RESULTADO RENDERIZADO em cada
borda de corte, nao a cena isolada. Procura:
  - salto visual na emenda entre cenas
  - pico de onda no audio (estalo que passou pelo fade)
  - quadro preto ou congelado onde nao devia
"""
import json, os, subprocess, sys
import numpy as np

VIDEO = sys.argv[1] if len(sys.argv) > 1 else 'edit/rede/final.mp4'
SAIDA = 'edit/rede/verify'
CENAS = json.load(open('edit/rede/align/alinhamento_final.json', encoding='utf-8'))['cenas']
os.makedirs(SAIDA, exist_ok=True)

bordas = [CENAS[str(n)]['a'] for n in range(2, 13)]

def quadro(t, alvo):
    subprocess.run(['ffmpeg','-v','error','-y','-ss','%.3f' % t,'-i',VIDEO,
                    '-frames:v','1','-vf','scale=480:-1', alvo], check=True)

# --- 1. emendas: um quadro antes e um depois de cada corte ---
from PIL import Image, ImageDraw, ImageFont
f = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 15)
tiras = []
for i, b in enumerate(bordas, start=2):
    ps = []
    for dt in (-0.50, -0.07, 0.07, 0.50):
        p = '%s/_b%02d_%+0.2f.png' % (SAIDA, i, dt)
        quadro(max(0, b + dt), p); ps.append((dt, p))
    ims = [Image.open(p) for _, p in ps]
    w, h = ims[0].size
    t = Image.new('RGB', (w*4 + 24, h + 26), (18, 18, 20))
    d = ImageDraw.Draw(t)
    d.text((4, 5), 'cena %d -> %d   corte em %.2fs' % (i-1, i, b), font=f, fill=(235, 200, 90))
    for k, im in enumerate(ims): t.paste(im, (k*(w+8), 24))
    tiras.append(t)
    for _, p in ps: os.remove(p)
lw = max(t.width for t in tiras); lh = sum(t.height + 6 for t in tiras)
folha = Image.new('RGB', (lw, lh), (10, 10, 12)); y = 0
for t in tiras: folha.paste(t, (0, y)); y += t.height + 6
folha.save('%s/emendas.jpg' % SAIDA, quality=88)

# --- 2. audio: pico curto onde nao ha fala e nem toque previsto ---
r = subprocess.run(['ffmpeg','-v','error','-i',VIDEO,'-f','f32le','-ac','1','-ar','48000','-'],
                   capture_output=True)
a = np.frombuffer(r.stdout, '<f4'); SR = 48000
j = 480                                    # janelas de 10 ms
rms = np.sqrt((a[:len(a)//j*j].reshape(-1, j)**2).mean(1))
db = 20*np.log10(np.maximum(rms, 1e-7))
salto = np.diff(db)
toques = set(round(t, 1) for t, _, _ in json.load(open('edit/rede/sons.json')))
susp = []
for i in np.where(salto > 17)[0]:
    t = (i + 1) * j / SR
    if any(abs(t - q) < 0.25 for q in toques): continue
    if any(abs(t - b) < 0.30 for b in bordas): susp.append(('emenda', round(t, 2), round(salto[i], 1)))
    elif db[i+1] > -30: susp.append(('?', round(t, 2), round(salto[i], 1)))

print('emendas conferidas: %d  ->  %s/emendas.jpg' % (len(bordas), SAIDA))
print('picos de audio sem toque previsto: %d' % len(susp))
for tipo, t, s in susp[:20]: print('   %-7s %7.2fs  +%.1f dB' % (tipo, t, s))

# --- 3. quadro preto ---
pr = subprocess.run(['ffmpeg','-v','error','-i',VIDEO,'-vf','blackdetect=d=0.08:pix_th=0.06',
                     '-f','null','-'], capture_output=True, text=True)
pretos = [l for l in pr.stderr.split('\n') if 'black_start' in l]
print('trechos pretos: %d' % len(pretos))
for l in pretos[:10]: print('   ' + l.strip())
