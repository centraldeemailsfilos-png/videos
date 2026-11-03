# Como construir uma cena deste vídeo

Leia isto inteiro antes de escrever uma linha. O que está aqui foi
aprendido construindo as cenas 2 e 6, e cada regra custou um erro.

## O que você está fazendo

Um vídeo institucional de 4m07s que explica a estrutura dos projetos
sociais da Filos Editora. Doze cenas, cada uma um projeto HyperFrames
separado em `edit/rede/animations/cena_NN/`, renderizadas e montadas
depois. Você constrói **uma** cena.

**Nenhum tempo é inventado.** A narração real foi alinhada palavra a
palavra ao áudio, e o dossiê da sua cena
(`edit/rede/align/dossies/cena_NN.md`) tem o instante de cada palavra.
Quando o roteiro diz "cada toque deve coincidir com a palavra
correspondente na narração", é literal: use os números do dossiê.

## Leia antes

| Arquivo | Para quê |
|---|---|
| `edit/rede/align/dossies/cena_NN.md` | a sua cena: duração, narração, tempo de cada palavra |
| `edit/rede/animations/cena_06/index.html` | **a implementação de referência** — celular, câmera, cursor, pincel, painel |
| `edit/rede/animations/cena_02/index.html` | referência sem celular: diagrama nativo em HTML |
| `edit/rede/animations/_kit/LEIA.md` | o contrato do `check`, que morde |
| `footage/rede/roteiro.md` | o roteiro; ache a sua cena na seção 5 |

## Contrato que o `check` impõe

1. `<video>` **precisa** de `id`. Sem ele o vídeo sai **congelado** no
   MP4 e nada avisa.
2. `data-start` vai no `<video>` **ou** no invólucro, nunca nos dois.
   O celular é um `.clip`/div **sem** `data-start`; o vídeo dentro tem.
3. Filho direto da raiz com `data-start` vira caixa absoluta de tela
   cheia. Ponha tudo dentro de um `.clip` sem `data-start`.
4. **Um dono só para o `transform`.** Se o CSS tem `transform: scale()`
   e o GSAP anima `scale`, o GSAP sobrescreve e o elemento volta ao
   tamanho. Escala inicial vai em `gsap.set()` + `tl.set(..., 0)`.
5. Fontes: linke `assets/fontes/fontes.css` **no HTML**, não por
   `@import` — o linter não segue `@import`.
6. GSAP é local: `./node_modules/gsap/dist/gsap.min.js`. O CDN está
   bloqueado.
7. Texto de leitura não pode ficar abaixo de **28 px**.

## Composição

Canvas 1920×1080, 30 fps. Paleta e componentes em `assets/estilo.css`:
`--fundo #14110E`, `--fundo2 #1C1712`, `--ouro #C9A227`,
`--ouro-cl #DDBB6E`, `--creme #F1E8D9`, `--suave #A99C88`.
Títulos em Noto Serif com ênfase em itálico dourado (`.titulo em`),
apoio em Noto Sans, toque manuscrito em Caveat Brush (`.mao`).

Ajudantes em `assets/kit.js`: `toque()`, `pincel()`, `entra()`, `sai()`.

### O arranjo que as cenas 2 e 6 fixaram

- Celular à **esquerda**: caixa `left: 240px; top: 90px; 434×918`, borda
  9px, e o `<video>` com **416×900**. A caixa é conteúdo + 2×borda
  (`box-sizing: border-box`): se o vídeo tiver o tamanho da caixa ele
  transborda 18px e é cortado pelo `overflow`. Painel de texto à
  **direita** a partir de `left: 870px`.
- Barra de endereço no **canto superior direito** (`#barra.ender`), fora
  do caminho do celular quando a câmera aproxima.
- Painel: olho em Caveat Brush, título em Noto Serif, depois o conteúdo.
- Cena sem celular (diagrama): centralize e use a largura toda.

### Câmera

Aproxime **o celular inteiro, moldura junto** (`#fone`), nunca o
conteúdo dentro dele. Escalando só o conteúdo, a tela corta no meio da
palavra — telefone nenhum faz isso. O celular sangra para fora do
quadro, que é como um close funciona. Na cena 6: `scale 1.42,
x 43, y -261`. Uma aproximação por cena, não quatro: a cada movimento de
câmera o olho reassenta.

### Coordenadas de toque

O vídeo tem 390×844 CSS do site e entra escalado por **k = 416/390 =
1,0667**. O JSON da gravação (`edit/rede/gravacoes/GNN.json`) traz `x` e
`y` de cada toque em CSS do site; multiplique por `k`. O cursor e o
pincel moram **dentro** de `#fone`, para acompanharem a câmera.

## Regras de animação

- Easing **sempre cúbico** (`power2.inOut`, `power3.out`), nunca
  `linear`.
- Um elemento por vez. **Nunca revele dois independentes em paralelo** —
  o olho não acompanha.
- Entrada dura ~0,5s e começa 0,5s **antes** da palavra, para o quadro
  de chegada cair em cima dela.
- Segure o quadro final ≥ 1s antes do corte.
- Nada piscante. Este é um vídeo institucional.

## Antes de dizer que terminou

```bash
cd edit/rede/animations/cena_NN
npx --yes hyperframes check .          # tem de passar
npx --yes hyperframes snapshot --at <momentos que você mexeu>
```

Depois **olhe o contact-sheet** que o snapshot gera. Check passando não
diz como ficou. Corrija o que estiver feio e repita.

**Não renderize.** O render é centralizado depois, para as doze saírem
com o mesmo encode.

Avisos que podem ficar: `film_silent` (o áudio entra na montagem),
`container_overflow` do vídeo dentro do celular e `panel_out_of_canvas`
do celular quando a câmera aproxima — esses três são esperados.
