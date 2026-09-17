# videos — edição completa por conversa

Workspace de edição de vídeo guiada por agente: **corte baseado no que é falado**,
color grade, legendas e motion graphics. Fale em português; o material também
costuma estar em português.

Três ferramentas, um fluxo:

| Ferramenta | Papel | Origem |
|---|---|---|
| **video-use** | Orquestra tudo: transcreve, decide cortes, aplica grade, compõe, queima legendas | `browser-use/video-use` (MIT) |
| **HyperFrames** | Motor de motion em HTML/CSS/GSAP → MP4/WebM | `heygen-com/hyperframes` (Apache-2.0) |
| **Remotion** | Motor de motion em React, frame-driven | guia de referência do gist |

## Leia isto primeiro

O fluxo de trabalho completo está em **`.claude/skills/video-use/SKILL.md`**.
Ele é a fonte da verdade para o processo de edição. Este arquivo só adapta o
workflow a este repositório e define o roteamento entre os motores de motion.

As **12 Hard Rules** daquele SKILL.md não são opinião — são correção técnica.
Violar qualquer uma produz falha silenciosa ou saída quebrada. As que mais
pegam na prática:

- Legendas entram **por último** no filter chain, depois de todo overlay.
- Extração **por segmento** → concat `-c copy`. Nunca filtergraph em passe único.
- Fade de áudio de **30 ms** em toda borda de corte, senão estala.
- Overlay usa `setpts=PTS-STARTPTS+T/TB`, senão aparece o meio da animação.
- **Nunca corte no meio de uma palavra** — encoste toda borda num limite de palavra.
- **Confirme a estratégia em português com a pessoa antes de tocar no corte.**

## Layout deste repositório

```
videos/
├── CLAUDE.md                 ← este arquivo
├── footage/                  ← material bruto entra aqui (não versionado)
├── edit/                     ← toda saída sai aqui (não versionado)
│   ├── project.md            ← memória entre sessões
│   ├── takes_packed.md       ← transcrição por frase, a visão de leitura principal
│   ├── edl.json              ← decisões de corte
│   ├── transcripts/          ← JSON bruto do Scribe, em cache
│   ├── animations/slot_<id>/ ← um diretório por animação
│   ├── clips_graded/
│   ├── master.srt
│   ├── preview.mp4
│   └── final.mp4
├── scripts/setup.sh          ← prepara o ambiente numa máquina nova
└── .claude/skills/           ← as três ferramentas, vendorizadas
```

**Regra de ouro:** o material bruto em `footage/` é **imutável**. Nada é escrito
lá dentro e nada é escrito dentro de `.claude/skills/`. Toda saída vai para `edit/`.

Os helpers recebem caminhos explícitos, então neste repositório
`<videos_dir>` = `footage/` e o diretório de saída é `edit/` na raiz:

```bash
H=.claude/skills/video-use/helpers
python3 $H/transcribe_batch.py footage/ --language pt
python3 $H/pack_transcripts.py --edit-dir edit/
python3 $H/render.py edit/edl.json -o edit/preview.mp4 --preview
```

## Cold start

O container é efêmero. No início de cada sessão, verifique — não reinstale o que
já existe:

```bash
bash scripts/setup.sh --check
```

Precisa estar de pé: `ffmpeg` + `ffprobe`, Python com as deps do video-use,
Node.js **22+** (exigência do HyperFrames) e a `ELEVENLABS_API_KEY`.

A chave da ElevenLabs fica em `.env` na **raiz deste repositório** e nunca é
commitada. Sem ela nada transcreve — e sem transcrição não há corte guiado por
fala. Se faltar, peça uma vez e escreva no `.env`; nunca ecoe a chave na saída.

## Material em português

- Transcreva com `--language pt`. Sem isso o Scribe autodetecta e erra mais em
  material curto ou com ruído.
- Passe `--num-speakers N` quando souber quantas pessoas falam — melhora muito a
  diarização em entrevista e podcast.
- Fillers em português são `é`, `tipo`, `né`, `aí`, `então`, `hum` — o Scribe
  devolve verbatim, você decide o que cai. Nunca use modo normalizado.
- Legendas: 2 palavras em MAIÚSCULAS funciona para social; para narrativa e
  documentário use 4–7 palavras em caixa natural. Cuidado com acento cortado em
  fonte com outline fino.

## Roteamento dos motores de motion

Escolha **por slot de animação**, não uma vez para o projeto inteiro. Não caia no
default de Remotion só porque a animação parece web.

| Use | Quando |
|---|---|
| **HyperFrames** | UI de produto em movimento, site/mockup virando vídeo, tipografia cinética, promo de landing page, estados de dado, overlay WebM com alpha. Quando quiser autorar e validar como composição web (`lint`, `validate`, render determinístico). |
| **Remotion** | A pessoa pediu React/Remotion, já existe um design system em Remotion, ou uma árvore de componentes é o modelo mais simples. |
| **Manim** | Diagrama formal, máquina de estados, derivação de equação, morph de grafo. Leia `.claude/skills/video-use/skills/manim-video/SKILL.md`. |
| **PIL + sequência PNG + ffmpeg** | Card simples: contador, texto datilografado, revelação de barra. Rápido de iterar. |

Híbridos são válidos — fundo em PIL com camada HyperFrames por cima, por exemplo.

### HyperFrames num slot

Sempre dentro do diretório do slot, nunca na raiz:

```bash
cd edit/animations/slot_<id>/
npx --yes hyperframes init . --example blank --non-interactive --skip-skills
npm install gsap@3.14.2          # CDN é bloqueado aqui; veja as armadilhas abaixo
# construa a composição HTML aqui
npx --yes hyperframes check .    # lint + runtime + layout + motion + contraste
npx --yes hyperframes render . -o render.mp4
# alpha (overlay por cima do vídeo):
npx --yes hyperframes render . --format webm -o render.webm
```

As skills `hyperframes-core`, `hyperframes-cli`, `hyperframes-animation`,
`hyperframes-keyframes`, `hyperframes-registry` e `motion-graphics` estão
vendorizadas em `.claude/skills/` — leia-as antes de construir.

`talking-head-recut` também está disponível e é diretamente relevante para
recorte de vídeo falado.

### Remotion num slot

```bash
cd edit/animations/slot_<id>/
npx create-video@latest .
npx remotion render MyComp render.mp4
```

Guia completo em `.claude/skills/remotion/SKILL.md`.

### Armadilhas já verificadas neste ambiente

Estas custaram tempo na validação inicial. Leia antes de construir um slot.

**1. CDN bloqueado — use GSAP local.** O scaffold do HyperFrames carrega o GSAP
de `cdn.jsdelivr.net`, que o proxy de saída bloqueia
(`net::ERR_TUNNEL_CONNECTION_FAILED`). O registro do npm funciona normalmente,
então instale no slot e referencie por caminho relativo:

```bash
npm install gsap@3.14.2
```
```html
<script src="./node_modules/gsap/dist/gsap.min.js"></script>
```

O Google Fonts **não** é bloqueado — o compilador baixa e injeta `@font-face`
determinístico normalmente.

**2. Filho direto da raiz vira tela cheia.** Todo filho direto da composição que
tem `data-start` recebe `position: absolute; top:0; left:0` e 100% de tamanho.
Se você puser título, barra e subtítulo lado a lado na raiz, os três viram caixas
sobrepostas de tela inteira e o `check` acusa `content_overlap`. O padrão certo é
**uma cena como clip**, com o conteúdo dentro dela:

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="4" ...>
  <div id="cena" class="clip" data-start="0" data-duration="4" data-track-index="0">
    <h1>...</h1>
    <p>...</p>
  </div>
</div>
```

**3. Rode `check` antes de renderizar.** `npx --yes hyperframes check .` roda
lint, runtime, layout, motion e contraste de uma vez — pega sobreposição, texto
ilegível e conflito entre CSS `transform` e tween do GSAP antes de você gastar um
render.

### Regras de animação que valem para qualquer motor

- Easing **sempre cúbico**, nunca `linear` — linear parece robótico.
- Segure o frame final por **≥ 1 s** antes do corte.
- Sobre narração: duração total ≥ `tamanho_da_narração + 1s`.
- Sincronize o payoff: pegue o timestamp da palavra-chave e comece o overlay
  `reveal_duration` segundos antes, para o frame de chegada bater com a fala.
- Nunca revele dois elementos independentes em paralelo — o olho não acompanha.
- Múltiplas animações = **sub-agentes em paralelo** via a ferramenta `Agent`,
  nunca em sequência. Um sub-agente = um arquivo, nomes únicos.
- Sempre confirme a duração do render com `ffprobe` antes de apontar o EDL para ele.

## O processo, resumido

1. **Inventário** — `ffprobe` em tudo, `transcribe_batch.py`, `pack_transcripts.py`.
2. **Pré-varredura** — leia `takes_packed.md` e anote tropeços e frases a evitar.
3. **Converse** — descreva o que você viu em português e faça perguntas moldadas
   pelo material. Sem checklist fixo.
4. **Proponha a estratégia** em 4–8 frases e **espere a confirmação**.
5. **Execute** — `edl.json`, animações em paralelo, grade por segmento, `render.py`.
6. **Preview** — `render.py --preview` (720p, rápido).
7. **Autoavaliação antes de mostrar** — `timeline_view.py` no **resultado
   renderizado** em cada borda de corte (±1,5 s). Procure: salto visual, pico de
   waveform (estalo que passou pelo fade), legenda escondida atrás de overlay,
   overlay dessincronizado. Máximo de 3 passes; o que sobrar, relate.
8. **Itere e persista** — feedback em linguagem natural, re-render, e acrescente
   uma seção por sessão em `edit/project.md`. **Nunca re-transcreva** o que já
   está em cache.

## Antipadrões

Nunca: legenda queimada antes do overlay; filtergraph em passe único com
overlay; corte duro sem fade; easing linear; sub-agentes sequenciais para
animações; re-transcrever fonte em cache; editar antes de confirmar a estratégia;
assumir que tipo de vídeo é sem olhar o material.

## Créditos

Ferramentas de terceiros vendorizadas em `.claude/skills/`, licenças em `vendor/`.
Veja `vendor/UPSTREAM.md` para os commits exatos de origem.
