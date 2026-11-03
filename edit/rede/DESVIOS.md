# Desvios em relação ao roteiro

O que o vídeo entregue faz de diferente do que `roteiro-video-rede-filos.md`
pede, e por quê. Ordenado do que mais pesa para o que menos pesa.

## 1. Duração: 4m07s, não 3m34s

O roteiro estima 3 minutos e 34 segundos. A narração entregue tem
**261,25 s**, dos quais **207,5 s são fala** (4,7 sílabas/s, ritmo normal
de locução) e 54,8 s são pausas, distribuídas em 115 intervalos.

Enxugando cada pausa para no máximo 0,45 s — cortando sempre do meio da
pausa, nunca das bordas, para nenhuma palavra encostar no corte — o vídeo
fecha em **247,69 s (4m07s)**. Mesmo apertando toda pausa para 0,30 s o
resultado seria 3m57s. Os 3m34s só seriam alcançáveis regerando a
narração com ritmo mais rápido ou cortando texto; nenhuma das duas foi
feita sem autorização.

## 2. Tipografia: Noto Sans e Noto Serif, não Filos Sans e Filos Serif

A pasta `assets/fontes/` veio **vazia** no pacote `filos-site-para-hospedar`,
e o proxy deste ambiente bloqueia `filoseditora.com.br`, de onde os
arquivos poderiam ser baixados. A cadeia de fallback declarada pelo
próprio site é `"Filos Sans","Noto Sans",Roboto,…` e
`"Filos Serif","Noto Serif",Georgia,…`, então o vídeo usa o segundo item
de cada cadeia. Visualmente é muito próximo, mas **não é a fonte da
marca**. Para corrigir basta colocar os dois `.woff2` na pasta e regravar
as tomadas.

## 3. O mapa da rede foi reconstruído em HTML (cenas 2 e 12)

O roteiro pede, na cena 2, que *"cada bloco acende quando é citado"*. Não
é possível acender um bloco isolado dentro de um vídeo já gravado. O mapa
foi refeito em HTML com o mesmo desenho da página Rede Filos — pílulas
escuras de borda dourada, nomes em Caveat Brush, a Filos Editora em
dourado cheio — e cada bloco acende na palavra que o nomeia. O material
G00 foi gravado mas não entrou nessas duas cenas.

## 4. A barra de endereço fica no canto superior direito

O roteiro pede a barra *"sempre visível acima do site"*. Quando a câmera
aproxima, o celular cresce e sangra para fora do quadro pelo topo —
passaria por cima de uma barra ancorada acima dele. No canto superior
direito ela fica visível os quatro minutos inteiros, que atende melhor à
intenção ("mostrar o link de cada página") do que a posição literal.

## 5. O arrasto da barra quase não aparece (cena 6)

O roteiro pede *"arrasta até 10"*. Na faixa real do site, de 1 a 300, ir
de 5 para 10 move o polegar cerca de **6 pixels**. Quem conta a história
é o contador subindo e os valores indo a R$ 280,00 por mês; a barra em si
não lê. Foi mantido como o roteiro pede. Para o gesto aparecer seria
preciso arrastar até um número bem maior, o que mudaria os valores
mostrados.

## 6. Material que não existia e foi criado

- **Arte do anúncio (cena 5).** O roteiro (§8) manda criar uma *"arte
  ilustrativa, sem aparência de publicação real"*. Foi construída em HTML:
  cartão escuro com a marca, a manchete da campanha, botão "Apadrinhar" e
  assinatura "Corrente 300". **Sem** moldura de rede social, contador de
  curtidas, nome de perfil ou selo de patrocinado, e **com** a palavra
  "Exemplo" em pílula tracejada e a nota "arte ilustrativa" abaixo.
- **Trilha sonora.** Composta para este vídeo — fá maior, 68 bpm, sem
  percussão, agudo cortado em 2,6 kHz. Não há o que licenciar. Fica 18,8 dB
  abaixo da voz durante a fala e sobe nos intervalos.
- **Sons de toque.** Sintetizados; 18 ocorrências, posicionadas nos
  instantes exatos registrados pelas gravações de tela.

## 7. Item da checklist §8 aplicado na cópia de trabalho

*"Aponte o item e os botões para a Filos ABC antes de gravar a cena 3."*
O item **Projetos sociais** do menu da editora foi repontado de `#alcance`
para a página da Filos ABC na cópia de trabalho em `edit/rede/sites/`.
Os **botões de Doação** não foram repontados: nenhuma cena os mostra. No
site publicado os dois ainda precisam ser corrigidos.

## 8. Pendências do roteiro que continuam pendentes

Estas não foram resolvidas porque dependem de informação que não está no
material entregue:

- **Endereços.** `filosabc.filoseditora.com.br`, `corrente300.…` e
  `projetosocialangola.…` aparecem no vídeo como o roteiro define, mas
  continuam sendo sugestões. Se mudarem, as cenas 3, 5, 9 e 12 precisam
  ser refeitas.
- **Metas da Corrente 300.** Os números são exemplos. A etiqueta "Números
  de exemplo" está visível durante toda a cena 7, na página e no painel.
- **Grupo da Corrente 300.** Falta o link de convite; o botão gravado é o
  que existe hoje.
- **Fotos de crianças.** As que aparecem vêm das próprias páginas. A
  autorização de uso em vídeo precisa ser confirmada por vocês.
- **Pessoas citadas.** A seção "Quem está nessa corrente" não aparece em
  nenhuma cena.

## 9. Detalhes menores

- **Cena 9:** a gravação parte de "Uma vez / R$ 100" para que os toques em
  "Todo mês" e "R$ 20" produzam mudança visível. Partindo do padrão do
  site os dois toques não mudariam nada, contrariando a regra do §6
  ("mostre sempre o resultado depois do toque").
- **Cena 7:** o cartão "Mais panelas" já passou do topo quando a câmera
  chega, então a palavra "panelas" não tem a palavra na tela; o batimento
  é a chegada da câmera nos cartões de meta.
- **Cena 4:** o quadro final segura 0,39 s, abaixo do mínimo de 1 s, porque
  a última palavra ("empresa.") está a 0,59 s do fim da cena. Foi escolhida
  a sincronia com a palavra.
