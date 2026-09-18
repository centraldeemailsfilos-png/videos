# Projeto — FILOS · Histórias e Estórias

Vídeo vertical de apresentação do livro **Histórias e Estórias — Quilombos do Brasil
(Obra Coletiva)**, da FILOS · Projetando Pensamentos.

## Sessão 1 — 2026-09-18

**Material:** 5 clipes de WhatsApp, 464×832 @60fps, AAC estéreo, 95,31s no total.
Copiados para `footage/` como V1–V5 na ordem de envio
(15:24:11, 15:25:01, 15:25:02, 15:25:04, 15:25:08).

**Estratégia:** talking head único, apresentação de livro. Ordem narrativa por
escalada visual — fala sem livro → livro no colo → capa erguida → miolo aberto.
Corte guiado por energia de fala (não por conteúdo, ver limitação abaixo),
grade corretiva leve, três overlays de motion, saída vertical.

**Limitação que definiu tudo:** não há ASR alcançável neste container. O proxy de
saída nega `api.elevenlabs.io` (403 no CONNECT), Hugging Face, releases do GitHub
e `alphacephei.com`. Só PyPI, npm e `raw.githubusercontent.com` passam — as
bibliotecas de ASR são instaláveis, mas **os pesos dos modelos não**. A chave da
ElevenLabs, portanto, não resolveria. A pessoa optou por editar sem transcrição.

**Consequência:** sem legendas, sem corte de fillers por palavra e sem escolha de
melhor tomada por conteúdo. O corte removeu apenas tempo morto real, medido por
detecção de atividade de fala.

**Análise de fala** (librosa, RMS 10ms, limiar adaptativo piso+35% da faixa,
fusão de blocos com intervalo <0,18s) — em `edit/analysis/speech.json`:

| Clipe | Duração | Fala | Blocos | Pausas ≥0,3s |
|---|---|---|---|---|
| V1 | 3,46s | 2,67s | 2 | 1 |
| V2 | 38,27s | 32,04s | 13 | 10 |
| V3 | 41,70s | 32,38s | 14 | 11 |
| V4 | 2,25s | 1,83s | 1 | 0 |
| V5 | 9,66s | 6,40s | 3 | 2 |

**Decisões de corte** (`edit/edl.json`, 9 ranges, 87,96s):

- Ordem: **V1 → V4 → V5 → V2 → V3**. V5 subiu duas posições por ter a melhor
  tomada da capa completa; V4 virou ponte entre o gancho e a revelação.
- Cabeças e caudas mortas removidas: V5 (1,43s + 0,81s), V3 (0,15s + 0,70s),
  V4 (0,30s), V2 (0,17s).
- Quatro pausas internas >1,0s fechadas para ~0,25s: V2 em 25,43→26,48;
  V3 em 17,31→18,42, 33,36→34,39 e 36,17→37,50.
- **V1 mantido inteiro de propósito.** A pausa de 0,79s em 1,74→2,53 é ela
  alcançando o livro — cortar quebraria a continuidade do movimento do braço.
- Padding de 60ms antes e 120ms depois em cada borda (Hard Rule 7).
- Removidos 7,35s de tempo morto. Todo o resto do conteúdo preservado, porque
  sem transcrição não dá para julgar o que descartar.

**Grade:** `neutral_punch`. Testado contra o original — melhora contraste e deixa
o título da capa legível, sem estourar tom de pele. O material é interno, com uma
faixa de sol dura na parede; nada agressivo funcionaria aqui.

**Áudio:** fonte muito baixa (−27,17 LUFS). Loudnorm para −14 LUFS / −1 dBTP.

**Motion (HyperFrames, 1070×1920 @30fps, alpha):** três slots, construídos em
sub-agentes paralelos. Paleta compartilhada — âmbar `#F2A33C`, branco `#FFFFFF`,
secundário `#D8CFC2`, Inter. Easing `power3.out`/`power2.out`, nunca linear.

| Slot | Janela na saída | Conteúdo |
|---|---|---|
| slot_1 | 0,35 → 3,35s | Título do livro, terço inferior, com scrim |
| slot_2 | 7,00 → 10,50s | Selo de marca no topo esquerdo, durante a revelação da capa |
| slot_3 | 83,90 → 87,90s | Lockup de fecho, centralizado no terço inferior |

**Saída:** `edit/final.mp4` (1070×1920 @30, 88,20s, 79,9 MB) e
`edit/final_leve.mp4` (CRF 26, 29,8 MB) para compartilhar.

## Armadilhas resolvidas nesta sessão

1. **Alpha em VP9/WebM não chega no ffmpeg.** O HyperFrames renderiza WebM com
   alpha em `BlockAdditional` do Matroska, e o decoder `vp9` nativo do ffmpeg não
   lê esse canal — `ffprobe` reporta `yuv420p` e o overlay entraria como retângulo
   preto. O `render.py` abre overlays com `-i` simples, então **converta cada
   overlay para ProRes 4444 antes de compor**:
   ```bash
   ffmpeg -vcodec libvpx-vp9 -i render.webm -c:v prores_ks -profile:v 4444 \
          -pix_fmt yuva444p10le render.mov
   ```
   O `.mov` lê `yuva444p12le` nativamente e compõe certo. Aponte o EDL para o `.mov`.
2. **Nada de `<link>` do Google Fonts no HTML do slot.** O proxy quebra o TLS da
   folha de estilo e o `check` falha com `ERR_CERT_AUTHORITY_INVALID`. Declare só
   `font-family` — o compilador do HyperFrames busca a fonte server-side e injeta
   `@font-face` determinístico sozinho.
3. **`timeline_view.py` falha se `end` == duração exata** do arquivo (o último
   frame não existe). Use um valor um pouco menor.
4. **`timeline_view.py` escreve em `<pasta_do_video>/edit/` por padrão**, o que
   suja `footage/`. Sempre passe `-o`.

## Em aberto

- **Legendas** — dependem de transcrição, que este ambiente não alcança. Se a
  pessoa colar o roteiro, dá para alinhar aos blocos de fala já mapeados e gerar
  `master.srt`.
- **Corte por conteúdo** — idem. Hoje o vídeo tem 88s; com transcrição dá para
  cortar bem mais, escolhendo o que sai.
- **Ordem** — decidida por lógica visual, não pelo que é dito. Trocar a ordem é
  reordenar os ranges no `edl.json` e re-renderizar.
