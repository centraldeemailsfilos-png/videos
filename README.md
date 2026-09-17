# videos

Workspace de edição de vídeo por conversa. Você coloca o material bruto em
`footage/`, abre o Claude Code aqui e diz o que quer — em português.

O corte é guiado **pelo que é falado**: o áudio é transcrito com timestamp por
palavra, e as decisões de corte saem dos limites de palavra e das pausas.

## O que ele faz

- Transcreve com diarização e timestamp por palavra (ElevenLabs Scribe)
- Corta fillers (`é`, `tipo`, `né`, `hum`) e o tempo morto entre as tomadas
- Escolhe a melhor tomada de cada trecho quando há várias
- Color grade por segmento
- Fade de 30 ms em cada corte, para não estalar
- Legendas queimadas, com estilo ajustável
- Motion graphics via HyperFrames, Remotion, Manim ou PIL
- Confere o próprio resultado antes de te mostrar
- Guarda a memória do projeto em `edit/project.md` entre sessões

## Começando

```bash
bash scripts/setup.sh          # instala/verifica ffmpeg, deps python, node
cp .env.example .env           # e cole sua chave da ElevenLabs
```

Coloque os arquivos em `footage/`, abra o Claude Code na raiz do repositório e
comece com algo como:

> faça um inventário desse material e me proponha uma estratégia

ou

> corta isso num vídeo de lançamento de 60 segundos, vertical, com legenda

O agente vai olhar o material, te fazer perguntas, propor um plano em português
e **esperar sua confirmação** antes de mexer no corte.

## Requisitos

| | |
|---|---|
| FFmpeg | obrigatório |
| Python 3.10+ | obrigatório (`requests`, `librosa`, `matplotlib`, `pillow`, `numpy`) |
| `ELEVENLABS_API_KEY` | obrigatório — sem transcrição não há corte guiado por fala |
| Node.js 22+ | só para slots HyperFrames/Remotion |
| yt-dlp | opcional, para baixar material de URL |

## Onde as coisas ficam

- `footage/` — material bruto, **imutável**, fora do git
- `edit/` — toda saída (preview, final, transcrições, EDL, animações), fora do git
- `CLAUDE.md` — instruções do agente e roteamento dos motores de motion
- `.claude/skills/` — as três ferramentas vendorizadas
- `vendor/` — licenças e commits de origem

## Créditos

- [video-use](https://github.com/browser-use/video-use) — MIT
- [HyperFrames](https://github.com/heygen-com/hyperframes) — Apache-2.0
- [Guia Remotion](https://gist.github.com/ThariqS/3d446e7c7aa9eb94f468194deb73028f)

Detalhes em `vendor/UPSTREAM.md`.
