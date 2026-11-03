"""Monta o video final a partir das 12 cenas renderizadas.

Cada cena ocupa a fatia da linha do tempo que a sua parte da narracao
ocupa. Onde o render e mais curto que a fatia, o ultimo quadro segura o
resto; onde e mais longo, a sobra e cortada. As cenas ja sao desenhadas
para segurar no fim, entao segurar mais alguns quadros nao aparece.

Montagem por segmento e concat de demuxer, nunca filtergraph em passe
unico (Hard Rule 4 do video-use).

  python3 edit/rede/montar.py                 # final
  python3 edit/rede/montar.py --leve          # versao leve para aprovacao
  python3 edit/rede/montar.py --com-trilha    # com a trilha de fundo

Sem trilha por padrao: a pessoa ouviu a que eu compus e nao gostou. O
caminho da trilha continua no codigo para quando houver outra faixa —
basta pousar o WAV em edit/rede/trilha.wav e passar --com-trilha.
"""
import json, os, subprocess, sys, shutil

LEVE    = '--leve' in sys.argv
TRILHA  = '--com-trilha' in sys.argv
DUR   = 247.69
CENAS = json.load(open('edit/rede/align/alinhamento_final.json', encoding='utf-8'))['cenas']
TMP   = 'edit/rede/_montagem'
SAIDA = 'edit/rede/final_leve.mp4' if LEVE else 'edit/rede/final.mp4'

def dur(p):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
                                 '-of','csv=p=0', p], capture_output=True, text=True).stdout.strip())

def util(p, d):
    """Ate onde o render tem imagem de verdade.

    Quando o data-duration do <video> passa de um quadro o fim da midia,
    o elemento sai preto no ultimo quadro. Clonar esse quadro para
    preencher a fatia espalha o preto pela emenda, o que aconteceu com a
    cena 9. Aqui so recua se o quadro for mesmo escuro: a 30 fps um
    quadro dura 0,033s, entao a primeira amostra e em d-0,04.
    """
    import io
    import numpy as np
    from PIL import Image
    def claro(t):
        r = subprocess.run(['ffmpeg','-v','error','-ss','%.3f' % t, '-i', p,
                            '-frames:v','1','-f','image2pipe','-vcodec','png','-'],
                           capture_output=True)
        if not r.stdout: return None
        return np.asarray(Image.open(io.BytesIO(r.stdout)).convert('L'), float).mean()
    for dt in (0.04, 0.08, 0.12, 0.18, 0.25):
        m = claro(d - dt)
        if m is not None and m > 3.0:
            return d if dt <= 0.04 else d - dt
    return d


# --- fatias: cada cena vai do seu inicio ate o inicio da seguinte ---
ns = [str(i) for i in range(1, 13)]
ini = {n: CENAS[n]['a'] for n in ns}
fatia = {}
for i, n in enumerate(ns):
    a = 0.0 if n == '1' else ini[n]
    z = ini[ns[i+1]] if i + 1 < len(ns) else DUR
    fatia[n] = (a, z)

faltam = [n for n in ns if not os.path.exists('edit/rede/animations/cena_%02d/render.mp4' % int(n))]
if faltam:
    print('faltam renders das cenas: %s' % ', '.join(faltam)); sys.exit(1)

shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
lista = os.path.join(TMP, 'lista.txt')
CRF = '26' if LEVE else '18'
ESC = 'scale=1280:720:flags=lanczos' if LEVE else None

print(' #   fatia            render    ajuste')
with open(lista, 'w') as lf:
    for n in ns:
        src = 'edit/rede/animations/cena_%02d/render.mp4' % int(n)
        a, z = fatia[n]; alvo = z - a
        d0 = dur(src)
        bom = util(src, d0)
        if d0 - bom > 0.015:
            print('   cena %s: ultimo quadro sem imagem, cortando %.2fs' % (n, d0 - bom))
        d = bom
        # a cena 1 comeca 0,14s depois do zero: a narracao comeca ali
        pre = (ini[n] - a) if n == '1' else 0.0
        pos = alvo - pre - d
        f = []
        if bom < d0 - 0.015:
            f.append('trim=end=%.3f,setpts=PTS-STARTPTS' % bom)
        if pre > 0.004 or pos > 0.004:
            f.append('tpad=start_duration=%.3f:start_mode=clone:stop_duration=%.3f:stop_mode=clone'
                     % (max(0, pre), max(0, pos)))
        f.append('fps=30')
        if ESC: f.append(ESC)
        saida = os.path.join(TMP, 'c%02d.mp4' % int(n))
        cmd = ['ffmpeg','-v','error','-y','-i', src, '-vf', ','.join(f)]
        if pos < -0.004: cmd += ['-t', '%.3f' % alvo]
        cmd += ['-c:v','libx264','-crf',CRF,'-preset','medium','-pix_fmt','yuv420p',
                '-an','-r','30', saida]
        subprocess.run(cmd, check=True)
        print('%2s  %6.2f-%6.2f   %6.2fs   %+5.2fs  ->  %6.2fs'
              % (n, a, z, d, pos, dur(saida)))
        lf.write("file '%s'\n" % os.path.basename(saida))

mudo = os.path.join(TMP, 'mudo.mp4')
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i', lista,
                '-c','copy', mudo], check=True)
print('\nvideo mudo: %.2fs' % dur(mudo))

# --- som: narracao e os toques; a trilha so entra se pedida ---
entradas = ['-i', mudo, '-i', 'edit/rede/narracao_enxuta.wav', '-i', 'edit/rede/sons.wav']
if TRILHA:
    entradas += ['-i', 'edit/rede/trilha.wav']
    mistura = (
      '[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,asplit=2[voz][chave];'
      '[3:a]volume=0.65[mus];'
      # A trilha recua sozinha quando ha voz, em vez de curva desenhada a
      # mao. Aferido: 18,8 dB de voz sobre a trilha durante a fala e
      # 7,1 dB de recuo, com a trilha subindo a -24,5 dB nos intervalos.
      '[mus][chave]sidechaincompress=threshold=0.040:ratio=6:attack=24:release=420:makeup=1[musd];'
      '[2:a]volume=0.85[toq];'
      '[voz][musd][toq]amix=inputs=3:normalize=0:dropout_transition=0[som];'
    )
else:
    mistura = (
      '[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[voz];'
      '[2:a]volume=0.85[toq];'
      '[voz][toq]amix=inputs=2:normalize=0:dropout_transition=0[som];'
    )
mistura += ('[som]alimiter=limit=0.94,afade=t=in:st=0:d=0.5,'
            'afade=t=out:st=%.2f:d=1.4[saida]' % (DUR - 1.4))
subprocess.run(['ffmpeg','-v','error','-y'] + entradas +
               ['-filter_complex', mistura,
                '-map','0:v','-map','[saida]',
                '-c:v','copy','-c:a','aac','-b:a','192k',
                '-movflags','+faststart', SAIDA], check=True)
shutil.rmtree(TMP, ignore_errors=True)
print('\n%s  %.2fs  %.1f MB' % (SAIDA, dur(SAIDA), os.path.getsize(SAIDA) / 1e6))
