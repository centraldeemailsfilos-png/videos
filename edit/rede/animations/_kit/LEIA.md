# Kit das cenas da Rede Filos

Cada cena é um projeto HyperFrames em `edit/rede/animations/cena_NN/`.
Os três arquivos deste diretório são copiados para dentro de cada cena
(`assets/`), porque o compilador do HyperFrames não resolve caminhos
para fora da raiz do projeto.

## Contrato que o `check` impõe (aprendido na marra)

1. `<video>` **precisa** de `id` — sem ele o renderizador não descobre a
   mídia e o vídeo sai **congelado** no MP4, sem avisar.
2. `data-start` vai no `<video>` **ou** no invólucro, nunca nos dois: o
   extrator de quadros lê o `data-start` do vídeo sem somar o do pai, e
   os dois discordam.
3. Filho direto da raiz com `data-start` vira caixa absoluta de tela
   cheia. O celular fica dentro de um `.clip` **sem** `data-start`.
4. Nada de `<link>` do Google Fonts: o compilador busca a fonte
   server-side e injeta `@font-face` determinístico. Basta declarar
   `font-family`.
5. GSAP é local (`./node_modules/gsap/dist/gsap.min.js`) — o CDN está
   bloqueado neste ambiente.

## Tempos

Nenhum tempo é inventado. Todos saem de
`edit/rede/align/briefing.json`, que tem, por cena, a duração medida no
áudio e o instante de cada palavra da narração. O campo `chaves` lista
as palavras em que o motion tem de bater.
