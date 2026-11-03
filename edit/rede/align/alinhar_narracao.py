"""Alinha a narracao inteira (486 palavras, 261s) palavra a palavra.

Duas passadas, porque o ritmo nao e uniforme: a narracao tem 46 pausas
somando 54s, e um unico segundos-por-silaba global inflaria cada palavra
com o tempo das pausas.

  1. DP global sobre todos os onsets -> distribui as palavras no tempo
  2. cada palavra e atribuida ao bloco de fala que contem o seu meio
  3. cada bloco e re-alinhado sozinho, com o ritmo dele

A passada 1 so precisa acertar a qual bloco cada palavra pertence; a
passada 2 e quem da o tempo que vai para a legenda e para o motion.
"""
import sys, os, json, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'angola', 'align'))
import numpy as np
from alinhador2 import alinha

AUDIO = 'footage/rede/narracao/narracao_carla.mp3'
CENAS = 'edit/rede/align/cenas_roteiro.json'
SAIDA = 'edit/rede/align/alinhamento.json'

cenas = json.load(open(CENAS, encoding='utf-8'))
pal_cena = []            # (indice_da_cena, palavra)
for c in cenas:
    for w in re.findall(r'\S+', c['narracao']):
        if re.search(r'[A-Za-zÀ-ú0-9]', w): pal_cena.append((c['n'], w))
texto = ' '.join(w for _, w in pal_cena)
print('passada 1: %d palavras sobre o audio inteiro...' % len(pal_cena), flush=True)
p1, blocos = alinha(AUDIO, texto)
print('   %d palavras posicionadas, %d blocos de fala' % (len(p1), len(blocos)), flush=True)

# --- atribui cada palavra ao bloco que contem o seu meio ---
ini = np.array([b[0] for b in blocos]); fim = np.array([b[1] for b in blocos])
dono = []
for _, a, b in p1:
    m = (a + b) / 2
    dentro = np.where((ini <= m) & (m <= fim))[0]
    dono.append(int(dentro[0]) if len(dentro) else
                int(np.argmin(np.minimum(abs(ini - m), abs(fim - m)))))

# --- passada 2: re-alinha cada bloco com o ritmo dele ---
print('passada 2: re-alinhando %d blocos com ritmo local...' % len(set(dono)), flush=True)
final = []
for bi in sorted(set(dono)):
    idx = [i for i, d in enumerate(dono) if d == bi]
    sub = ' '.join(pal_cena[i][1] for i in idx)
    a, b = blocos[bi]
    folga = 0.06
    r, _ = alinha(AUDIO, sub, ini=max(0, a - folga), fim=b + folga)
    if len(r) != len(idx):           # bloco curto demais para re-alinhar
        passo = (b - a) / len(idx)
        r = [(pal_cena[i][1], a + k*passo, a + (k+1)*passo) for k, i in enumerate(idx)]
    for i, (w, ta, tb) in zip(idx, r):
        final.append({'cena': pal_cena[i][0], 'p': w,
                      'a': round(float(ta), 3), 'z': round(float(tb), 3)})

final.sort(key=lambda x: x['a'])
# nenhuma palavra pode terminar depois do inicio da seguinte
for i in range(len(final) - 1):
    if final[i]['z'] > final[i+1]['a']: final[i]['z'] = final[i+1]['a']

json.dump({'audio': AUDIO, 'blocos': blocos, 'palavras': final},
          open(SAIDA, 'w'), ensure_ascii=False, indent=1)

curtas = [w for w in final if w['z'] - w['a'] < 0.10]
print('\nescrito %s' % SAIDA)
print('palavras com menos de 0,10s: %d' % len(curtas))
print('\nfronteiras de cena medidas no audio:')
print(' #  inicio    fim    dur   roteiro previa   desvio')
for c in cenas:
    ws = [w for w in final if w['cena'] == c['n']]
    if not ws: continue
    a, z = ws[0]['a'], ws[-1]['z']
    prev = c['prev_fim'] - c['prev_ini']
    print('%2d  %6.2f  %6.2f  %5.1fs  %5.1fs        %+5.1fs' % (c['n'], a, z, z-a, prev, (z-a)-prev))
