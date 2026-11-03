"""Trilha original do video da Rede Filos.

Secao 7 do roteiro: "leve e sem letra, com licenca comercial e volume
baixo durante a fala". Composta aqui, entao nao ha o que licenciar.

Nada de percussao e nada de melodia que dispute com a narracao: um
colchao de acordes com um arpejo esparso por cima, filtrado no agudo
para sair de baixo da voz em vez de brigar com ela.
"""
import numpy as np, subprocess, sys

SR   = 48000
DUR  = 247.69
BPM  = 68
BAT  = 60 / BPM            # 0,882 s por batida
COMP = 4 * BAT             # compasso

def nota(n):               # midi -> hertz
    return 440.0 * 2 ** ((n - 69) / 12)

# Fa maior, progressao de quatro compassos. O baixo desce F - E - D - Bb,
# que e o que da o andar para a frente sem precisar de bateria.
ACORDES = [
    (53, [65, 69, 72]),    # F     (fa)
    (52, [64, 67, 72]),    # C/E   (do com baixo em mi)
    (50, [62, 65, 69]),    # Dm    (re menor)
    (46, [58, 62, 65]),    # Bb    (si bemol)
]

t = np.arange(int(SR * DUR)) / SR
esq = np.zeros_like(t); dir = np.zeros_like(t)

def env(ini, dur, ataque, solta):
    """Envelope com ataque e queda suaves, em cosseno — sem clique."""
    a, b = int(ini * SR), int((ini + dur) * SR)
    if a >= len(t): return None, None, None
    b = min(b, len(t)); n = b - a
    e = np.ones(n)
    na = min(int(ataque * SR), n // 2)
    ns = min(int(solta  * SR), n - na)
    if na: e[:na] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, na))
    if ns: e[-ns:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, ns))
    return a, b, e

def coloca(ini, dur, freq, amp, parciais, ataque, solta, pan=0.0, vib=0.0):
    a, b, e = env(ini, dur, ataque, solta)
    if a is None: return
    loc = np.arange(b - a) / SR
    f = freq * (1 + vib * np.sin(2 * np.pi * 4.6 * loc)) if vib else freq
    onda = np.zeros(b - a)
    for k, g in enumerate(parciais, 1):
        onda += g * np.sin(2 * np.pi * f * k * loc + k * 0.7)
    onda *= amp * e
    esq[a:b] += onda * (1 - max(0.0,  pan)) 
    dir[a:b] += onda * (1 - max(0.0, -pan))

# --- colchao: acorde longo por compasso, mais a fundamental uma oitava abaixo
PARC_PAD = [1.0, 0.34, 0.14, 0.055, 0.02]
PARC_ARP = [1.0, 0.42, 0.20, 0.09, 0.035, 0.015]

c = 0
while c * COMP < DUR:
    ini = c * COMP
    baixo, tons = ACORDES[c % 4]
    coloca(ini, COMP * 1.12, nota(baixo - 12), 0.055, [1.0, 0.22, 0.06], 0.55, 0.9)
    for j, m in enumerate(tons):
        coloca(ini, COMP * 1.12, nota(m), 0.030, PARC_PAD, 0.70, 1.0,
               pan=(j - 1) * 0.22, vib=0.0012)
    # arpejo: tres notas por compasso, nunca na cabeca da batida 1, para
    # a trilha nao marcar tempo por cima de quem esta falando
    for j, (passo, grau) in enumerate([(1.5, 2), (2.5, 0), (3.5, 1)]):
        m = tons[grau] + (12 if j == 1 else 0)
        coloca(ini + passo * BAT, BAT * 1.6, nota(m), 0.042, PARC_ARP,
               0.012, BAT * 1.5, pan=(j - 1) * 0.3)
    c += 1

# --- abertura e fecho ---
sobe = int(7.0 * SR); esq[:sobe] *= np.linspace(0, 1, sobe) ** 2
dir[:sobe] *= np.linspace(0, 1, sobe) ** 2
desce = int(6.5 * SR); esq[-desce:] *= np.linspace(1, 0, desce) ** 1.6
dir[-desce:] *= np.linspace(1, 0, desce) ** 1.6

# --- tira o agudo: o lugar da trilha e por baixo da voz ---
def passa_baixa(x, corte=2600.0):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1 + (f / corte) ** 2), n=len(x))
esq, dir = passa_baixa(esq), passa_baixa(dir)

est = np.stack([esq, dir], 1)
pico = np.abs(est).max()
est = est / pico * 0.62
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2',
                '-i','pipe:0','-c:a','pcm_s16le','edit/rede/trilha.wav'],
               input=est.astype('<f4').tobytes(), check=True)
print('trilha.wav  %.2fs  %d compassos  pico %.3f' % (DUR, c, pico))
