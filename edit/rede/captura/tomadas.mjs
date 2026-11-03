/* As 16 tomadas de tela, na nomenclatura G00-G13 do roteiro (§4).
 *
 * As duracoes vem das cenas medidas no audio real
 * (edit/rede/align/alinhamento_final.json), com folga para a montagem.
 * Toque em link nao navega: a troca de pagina e corte na edicao, e a
 * barra de endereco muda no motion.
 */
const ABC      = 'edit/rede/sites/rede/index.html';
const CORRENTE = 'edit/rede/sites/rede/corrente-300.html';
const ANGOLA   = 'edit/rede/sites/rede/escola-angola.html';
const EDITORA  = 'edit/rede/sites/editora/index.html';
const MAPA     = 'edit/rede/sites/rede/rede-filos.html';

const E = {
  abc:      'filosabc.filoseditora.com.br',
  corrente: 'corrente300.filoseditora.com.br',
  angola:   'projetosocialangola.filoseditora.com.br',
  editora:  'filoseditora.com.br',
  mapa:     'rede interna',
};

export const TOMADAS = [
  /* As duracoes dos passos nao sao arbitrarias: cada toque e cada chegada
   * de rolagem cai na palavra da narracao que a nomeia. Os tempos abaixo
   * sao locais a cada cena e vem de edit/rede/align/briefing.json.       */

  // ---------- G00  mapa da rede  (cenas 2 e 12; a 2 refaz o mapa em HTML) ----------
  // cena 12 (21,80s): "ABC" 4.59 | "Corrente" 9.06 | "Escolinha" 14.09 | "casa" 20.30
  { id: 'G00', pagina: MAPA, endereco: E.mapa, passos: [
    { esperar: 2.6 },
    { rolar: '.cartao-link', folga: 90, dur: 2.0 },   // chega nas fichas em 4.6
    { esperar: 4.4 },
    { rolar: 2050, dur: 1.6 },                        // 9.0: ficha da Corrente
    { esperar: 3.4 },
    { rolar: 2700, dur: 1.6 },                        // 14.0: ficha da Escolinha
    { esperar: 4.6 },
    { rolar: 400,  dur: 2.0 },                        // 20.2: volta ao mapa, "casa"
    { esperar: 1.6 },
  ]},

  // ---------- S1a/b/c  primeiras telas paradas, lado a lado  (cena 1) ----------
  { id: 'S1a', pagina: ABC,      endereco: E.abc,      passos: [{ esperar: 15 }] },
  { id: 'S1b', pagina: CORRENTE, endereco: E.corrente, passos: [{ esperar: 15 }] },
  { id: 'S1c', pagina: ANGOLA,   endereco: E.angola,   passos: [{ esperar: 15 }] },

  // ---------- G01  Filos Editora, primeira tela  (cena 3, plano de apoio) ----------
  { id: 'G01', pagina: EDITORA, endereco: E.editora, passos: [{ esperar: 11 }] },

  /* ---------- G02  Editora: menu -> Projetos sociais  (cena 3) ----------
   * "menu," 4.94 | "toca" 5.95 | "Projetos" 6.50 | "sociais" 7.14 | "ABC." 10.21
   * Termina em 10,6s: dali a cena corta para a Filos ABC, e o resto vem da G03. */
  { id: 'G02', pagina: EDITORA, endereco: E.editora, passos: [
    { esperar: 4.94 },
    { tocar: '#hamburguer', rotulo: 'abrir o menu', dur: 1.56 },
    { tocar: '#menuMovel > a:nth-of-type(3)', rotulo: 'Projetos sociais',
      semNavegar: true, dur: 4.10 },
  ]},

  // ---------- G03  Filos ABC, primeira tela  (cena 3, segunda metade) ----------
  { id: 'G03', pagina: ABC, endereco: E.abc, passos: [{ esperar: 9.0 }] },

  /* ---------- G04  o tour inteiro da Filos ABC  (cena 4, 27,40s) ----------
   * "conhecer" 3.21 | "instituto" 6.50 | "Dando" 9.42 | "Asas" 9.87
   * "ajudar," 15.85 | depois os quatro cartoes sao citados um a um, e a
   * pagina fica parada numa altura em que os quatro cabem na tela.       */
  { id: 'G04', pagina: ABC, endereco: E.abc, passos: [
    { esperar: 4.10 },
    { rolar: '#frentes', folga: 70,  dur: 2.40 },     // 6.50 "instituto"
    { esperar: 2.12 },
    { rolar: '#asas',    folga: 70,  dur: 1.25 },     // 9.87 "Asas"
    { esperar: 0.80 },
    { rolar: '#paises',  folga: 230, dur: 1.00 },
    { esperar: 0.53 },
    { tocar: '#paises > button:nth-of-type(1)',  rotulo: 'Brasil', dur: 1.20 },
    { tocar: '#paises > button:nth-of-type(12)', rotulo: 'Cuba',   dur: 1.45 },
    { rolar: 7899, dur: 1.00 },                       // 15.85 "ajudar"
    { esperar: 11.55 },
  ]},

  // ---------- G05  Corrente 300, primeira tela parada  (cena 5) ----------
  { id: 'G05', pagina: CORRENTE, endereco: E.corrente, passos: [{ esperar: 7.0 }] },

  // ---------- G06  a calculadora inteira  (cena 6, 32,57s) ----------
  // "mais" 9.72 | "menos" 10.28 | "atalhos" 12.17 | "arrastando" 12.84
  // "acompanha" 28.31.  #atalhos e a fileira 1/2/5/10/30; #vals sao os
  // valores de doacao avulsa, bem mais abaixo na pagina.
  { id: 'G06', pagina: CORRENTE, endereco: E.corrente, passos: [
    { esperar: 9.72 },
    { tocar: '#mais', rotulo: '+ (2)', dur: 0.56 },
    { tocar: '#mais', rotulo: '+ (3)', dur: 1.89 },
    { tocar: '#atalhos > button:nth-of-type(3)', rotulo: 'atalho 5', dur: 0.67 },
    { arrastar: { alvo: '#faixa', para: 10, dur: 1.50 }, rotulo: 'arrastar ate 10' },
    { esperar: 13.56 },
    { rolar: 760, dur: 2.60 },
    { esperar: 2.07 },
  ]},

  /* ---------- G07  metas e progresso  (cena 7, 23,06s) ----------
   * "metas." 1.98 | "listrada" 8.08 | "pessoa:" 9.49 | "cozinha," 15.83  */
  { id: 'G07', pagina: CORRENTE, endereco: E.corrente, passos: [
    { avaliar: () => window.scrollTo(0, 1500) },
    { esperar: 0.50 },
    { rolar: '#metas', folga: 70, dur: 1.48 },        // 1.98 "metas"
    { esperar: 6.10 },
    { tocar: '#d-mais', rotulo: '+ na barra flutuante', dur: 0.70 },
    { tocar: '#d-mais', rotulo: '+ na barra flutuante', dur: 0.71 },   // 9.49 "pessoa"
    { esperar: 5.34 },
    { rolar: 2700, dur: 1.00 },                       // 15.83 "cozinha"
    { esperar: 4.17 },
    { rolar: '#avulso', folga: 150, dur: 1.40 },
    { esperar: 1.66 },
  ]},

  /* ---------- G08  confianca  (cena 8, 12,21s) ----------
   * "contas," 5.29 | "passos" 6.95 | "regras" 8.81 | "empresas" 10.94   */
  { id: 'G08', pagina: CORRENTE, endereco: E.corrente, passos: [
    { avaliar: () => window.scrollTo(0, 3900) },
    { esperar: 0.60 },
    { rolar: '#transparencia', folga: 70, dur: 1.40 },
    { esperar: 3.29 },
    { rolar: '#caminho', folga: 70, dur: 1.66 },      // 6.95 "passos"
    { esperar: 0.40 },
    { rolar: '#regras',  folga: 70, dur: 1.46 },      // 8.81 "regras"
    { tocar: '#regras details:first-of-type summary', rotulo: 'abrir uma regra', dur: 0.80 },
    { rolar: '#empresas', folga: 70, dur: 1.33 },     // 10.94 "empresas"
    { esperar: 1.27 },
  ]},

  /* ---------- G09  Escolinha em Angola  (cena 9, 22,46s) ----------
   * "vez," 10.25 | "valor" 11.77 | "apoiar" 13.57 | "escola" 19.55       */
  { id: 'G09', pagina: ANGOLA, endereco: E.angola, passos: [
    /* Parte de "Uma vez / R$ 100". Sem isto a gravacao comeca ja em
     * "Todo mes / R$ 20", que e o padrao do site, e os dois toques nao
     * mudam nada na tela — o roteiro (§6) exige que a resposta do site
     * apareca depois de cada toque.                                    */
    { avaliar: () => {
        document.querySelector('#tipo > button:nth-of-type(2)').click();
        document.querySelector('#valores > button:nth-of-type(4)').click();
      }, rotulo: 'estado inicial: uma vez / R$ 100' },
    { esperar: 2.60 },
    { rolar: 330, dur: 1.40 },
    { esperar: 5.40 },
    { tocar: '#tipo > button:nth-of-type(1)',    rotulo: 'Todo mês', dur: 2.37 },
    { tocar: '#valores > button:nth-of-type(2)', rotulo: 'R$ 20',    dur: 6.48 },
    { rolar: '#escola', folga: 70, dur: 1.30 },       // 19.55 "escola"
    { esperar: 0.60 },
    { rolar: '#fotos',  folga: 70, dur: 1.50 },
    { esperar: 0.81 },
  ]},

  // ---------- G11a/b/c  trocar de pagina pelas marcas do topo  (cena 10) ----------
  { id: 'G11a', pagina: ABC, endereco: E.abc, passos: [
    { esperar: 1.6 }, { tocar: '.rede-marcas li:nth-child(2) a', rotulo: 'Corrente 300', semNavegar: true, dur: 1.8 },
  ]},
  { id: 'G11b', pagina: CORRENTE, endereco: E.corrente, passos: [
    { esperar: 1.6 }, { tocar: '.rede-marcas li:nth-child(3) a', rotulo: 'Escolinha em Angola', semNavegar: true, dur: 1.8 },
  ]},
  { id: 'G11c', pagina: ANGOLA, endereco: E.angola, passos: [
    { esperar: 1.6 }, { tocar: '.rede-marcas li:nth-child(1) a', rotulo: 'Filos ABC', semNavegar: true, dur: 1.8 },
  ]},

  // ---------- G12  rodape "Conheca a rede inteira"  (cena 10) ----------
  // a cena precisa do rodape de 13,58s ("fim") ate o fim, 24,22s
  { id: 'G12', pagina: ABC, endereco: E.abc, passos: [
    { avaliar: () => window.scrollTo(0, 8400) },
    { esperar: 0.60 },
    { rolar: '.rede-cartoes', folga: 120, dur: 2.00 },
    { esperar: 8.40 },
  ]},

  /* ---------- G13  espalhar a corrente  (cena 11, 12,15s) ----------
   * "divulgar." 2.80 | "WhatsApp" 4.37 | "grupo." 6.69 | "compartilha" 8.22 */
  { id: 'G13', pagina: CORRENTE, endereco: E.corrente, passos: [
    { avaliar: () => window.scrollTo(0, 7300) },
    { esperar: 1.00 },
    { rolar: '#espalhe', folga: 70, dur: 1.80 },      // 2.80 "divulgar"
    { esperar: 3.89 },
    { tocar: '#grupo',      rotulo: 'Entrar no grupo', semNavegar: true, dur: 1.53 },
    { tocar: '#fab-enviar', rotulo: 'Compartilhar',    dur: 3.93 },
  ]},
];
