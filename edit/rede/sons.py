"""Sons discretos de toque, sintetizados aqui.

Secao 1 do roteiro: "narracao, musica leve e sons discretos de toque".
Discreto e a palavra: um clique curto e abafado, nao um bip de interface.
Dois corpos somados — um estalo de ruido filtrado, que da o "contato", e
um tom grave muito curto, que da o peso — com queda exponencial.

Os instantes saem dos JSON das gravacoes, nao de estimativa: cada toque
foi gravado no quadro exato em que acontece.
"""
import json, numpy as np, subprocess

SR  = 48000
DUR = 247.69

# inicio de cada cena na linha do tempo final (alinhamento_final.json)
CENA = json.load(open('edit/rede/align/alinhamento_final.json', encoding='utf-8'))['cenas']

# (cena, gravacao, deslocamento do video dentro da cena)
FONTES = [
    ('3',  'G02',  0.00), ('4',  'G04',  0.00), ('6',  'G06',  0.00),
    ('7',  'G07',  0.00), ('8',  'G08',  0.00), ('9',  'G09',  0.00),
    ('10', 'G11a', 8.94), ('10', 'G11b', 10.50), ('10', 'G11c', 12.06),
    ('11', 'G13',  0.00),
]

def clique(forca=1.0):
    n = int(0.075 * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(7)
    ruido = rng.standard_normal(n)
    # passa-baixa simples: media movel de 12 amostras tira o chiado agudo
    k = 12; ruido = np.convolve(ruido, np.ones(k) / k, mode='same')
    corpo = np.sin(2 * np.pi * 320 * t) * 0.55 + np.sin(2 * np.pi * 148 * t) * 0.35
    som = (ruido * 0.45 + corpo) * np.exp(-t * 52)
    som *= np.minimum(1.0, t / 0.0012)          # ataque de 1,2 ms, sem clique de borda
    return som / np.abs(som).max() * 0.17 * forca

base = clique()
pista = np.zeros(int(SR * DUR))
marcas = []
for cena, grav, desl in FONTES:
    d = json.load(open('edit/rede/gravacoes/%s.json' % grav))
    t0 = CENA[cena]['a'] + desl
    for e in d['eventos']:
        if e['tipo'] not in ('toque', 'arrastar'): continue
        q = t0 + e['t']
        if q >= DUR - 0.1: continue
        a = int(q * SR); b = min(a + len(base), len(pista))
        # o arrastar e mais surdo que o toque: nao e um contato novo
        pista[a:b] += base[:b - a] * (0.62 if e['tipo'] == 'arrastar' else 1.0)
        marcas.append((round(q, 3), grav, e.get('rotulo', '')))

est = np.stack([pista, pista], 1)
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2',
                '-i','pipe:0','-c:a','pcm_s16le','edit/rede/sons.wav'],
               input=est.astype('<f4').tobytes(), check=True)
json.dump(marcas, open('edit/rede/sons.json','w'), ensure_ascii=False, indent=1)
print('%d toques, pico %.3f' % (len(marcas), np.abs(pista).max()))
for q, g, r in marcas: print('  %7.2fs  %-5s %s' % (q, g, r))
