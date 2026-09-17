# Origem das ferramentas vendorizadas

As três ferramentas foram copiadas para `.claude/skills/` para que o repositório
funcione a partir de um clone limpo, sem depender de rede. Commits de origem:

| Ferramenta | Origem | Commit | Data | Licença |
|---|---|---|---|---|
| video-use | https://github.com/browser-use/video-use | `9575612f066aa517354790a645fd90f9f95a743b` | 2026-08-30 | MIT |
| HyperFrames | https://github.com/heygen-com/hyperframes | `a8a9fdb0fe88d97c99d7bd30da94e64dd0a96f3d` | 2026-09-17 | Apache-2.0 |
| Guia Remotion | https://gist.github.com/ThariqS/3d446e7c7aa9eb94f468194deb73028f | `a60f4c0e85422ee6304ceecaedf29f36dc894c4a` | 2025-07-22 | — (gist de referência) |

## O que foi copiado

**video-use** → `.claude/skills/video-use/`
Repositório inteiro, sem `tests/`, `static/` e `poster.html`. `SKILL.md`, `install.md`,
`helpers/` e `skills/manim-video/` preservados como estão — os helpers precisam
ficar ao lado do `SKILL.md` para os caminhos relativos funcionarem.

**HyperFrames** → `.claude/skills/`
Subconjunto de motion, 8 das 20 skills: `hyperframes`, `hyperframes-core`,
`hyperframes-cli`, `hyperframes-animation`, `hyperframes-keyframes`,
`hyperframes-registry`, `motion-graphics`, `talking-head-recut`.
As 12 restantes (`media-use`, `embedded-captions`, `music-to-video`,
`faceless-explainer`, `product-launch-video`, `pr-to-video`,
`remotion-to-hyperframes`, `slideshow`, `figma`, `general-video`,
`hyperframes-audio`, `hyperframes-creative`) ficaram de fora por tamanho
(19 MB no total) e por sobreposição com o que o video-use já faz.
Para puxar o conjunto completo: `npx skills add heygen-com/hyperframes`.

**Guia Remotion** → `.claude/skills/remotion/SKILL.md`
Conteúdo integral do gist, precedido de um cabeçalho de skill e de uma seção
curta explicando como isolar um projeto Remotion dentro de `edit/animations/slot_<id>/`.

## Atualizar

Estas cópias não se atualizam sozinhas. Para trazer o upstream mais novo,
clone o repositório de origem e recopie os diretórios acima, depois atualize os
commits desta tabela.
