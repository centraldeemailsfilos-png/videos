"""Limita cada pausa da narracao a TETO segundos e remapeia o alinhamento.

A locucao de IA pausa demais: 54,8s em 115 pausas. Corta-se o excedente
do MEIO de cada pausa, nunca das bordas, para nenhuma palavra encostar
no corte. Cada pedaco sai com fade de 15 ms nas duas pontas (Hard Rule 6
do video-use: borda de corte sem fade estala) e os pedacos sao
concatenados em WAV, que e sem perda.
"""
import json, os, subprocess, shutil

TETO  = 0.45
FADE  = 0.015
ENTRA = 'footage/rede/narracao/narracao_carla.mp3'
SAI   = 'edit/rede/narracao_enxuta.wav'
AL    = 'edit/rede/align/alinhamento.json'
FINAL = 'edit/rede/align/alinhamento_final.json'
TMP   = 'edit/rede/_pedacos'

d = json.load(open(AL)); blocos = d['blocos']; palavras = d['palavras']
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
       '-of','csv=p=0', ENTRA], capture_output=True, text=True).stdout.strip())

# --- intervalos a remover: o excedente do meio de cada pausa longa ---
remove = []
for i in range(len(blocos)-1):
    ga, gb = blocos[i][1], blocos[i+1][0]
    sobra = (gb - ga) - TETO
    if sobra > 0.02:
        meio = (ga + gb) / 2
        remove.append((meio - sobra/2, meio + sobra/2))
if dur - blocos[-1][1] > 0.90:          # cauda: deixa 0,90s de respiro
    remove.append((blocos[-1][1] + 0.90, dur))

# --- pedacos que ficam ---
fica, t = [], 0.0
for a, b in remove:
    if a - t > 0.01: fica.append((t, a))
    t = b
if dur - t > 0.01: fica.append((t, dur))

shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
lista = os.path.join(TMP, 'lista.txt')
with open(lista, 'w') as lf:
    for k, (a, b) in enumerate(fica):
        p = os.path.join(TMP, 'p%04d.wav' % k)
        n = b - a
        f = min(FADE, n/3)
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a:.4f}','-to',f'{b:.4f}','-i',ENTRA,
            '-af', f'afade=t=in:st=0:d={f:.4f},afade=t=out:st={n-f:.4f}:d={f:.4f}',
            '-ar','48000','-ac','1','-c:a','pcm_s16le', p], check=True)
        lf.write("file '%s'\n" % os.path.basename(p))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i', lista,
                '-c','copy', SAI], check=True)
nova = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
       '-of','csv=p=0', SAI], capture_output=True, text=True).stdout.strip())

# --- remapeia: tempo antigo -> tempo novo, linear por pedaco ---
base, mapa = 0.0, []
for a, b in fica:
    mapa.append((a, b, base)); base += b - a
def novo(t):
    for a, b, off in mapa:
        if a <= t <= b: return round(off + (t - a), 3)
    if t < mapa[0][0]: return 0.0
    for i in range(len(mapa)-1):          # caiu num buraco: encosta na borda
        if t > mapa[i][1] and t < mapa[i+1][0]:
            return round(mapa[i][2] + (mapa[i][1] - mapa[i][0]), 3)
    return round(base, 3)

for w in palavras: w['a'], w['z'] = novo(w['a']), novo(w['z'])
cenas = {}
for w in palavras:
    c = cenas.setdefault(w['cena'], {'a': w['a'], 'z': w['z']})
    c['a'] = min(c['a'], w['a']); c['z'] = max(c['z'], w['z'])

json.dump({'audio': SAI, 'duracao': round(nova,3), 'teto_pausa': TETO,
           'cenas': {str(k): v for k, v in sorted(cenas.items())},
           'palavras': palavras}, open(FINAL,'w'), ensure_ascii=False, indent=1)
shutil.rmtree(TMP, ignore_errors=True)

print('%d pedacos, %d pausas encurtadas' % (len(fica), len(remove)))
print('%.2fs -> %.2fs  (%d:%02d)   cortados %.1fs' % (dur, nova, int(nova//60), int(nova%60), dur-nova))
print()
print(' #   inicio    fim     dur   titulo')
rot = {c['n']: c['titulo'] for c in json.load(open('edit/rede/align/cenas_roteiro.json', encoding='utf-8'))}
for k, v in sorted(cenas.items()):
    print('%2d  %7.2f %7.2f  %6.2fs  %s' % (k, v['a'], v['z'], v['z']-v['a'], rot[k]))
