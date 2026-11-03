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
  // ---------- G00  mapa da rede  (cenas 2 e 12) ----------
  { id: 'G00', pagina: MAPA, endereco: E.mapa, passos: [
    { esperar: 2.0 },
    { rolar: '.mapa', folga: 150, dur: 2.6 },
    { esperar: 9.0 },                         // post acende um bloco por vez
    { rolar: '.cartao-link', folga: 90, dur: 2.8 },
    { esperar: 3.0 },
    { rolar: 2400, dur: 3.2 },
    { esperar: 3.0 },
  ]},

  // ---------- G01  Filos Editora, primeira tela  (cenas 1 e 3) ----------
  { id: 'G01', pagina: EDITORA, endereco: E.editora, passos: [
    { esperar: 7.0 },
  ]},

  // ---------- G02  Editora: menu -> Projetos sociais  (cena 3) ----------
  { id: 'G02', pagina: EDITORA, endereco: E.editora, passos: [
    { esperar: 1.6 },
    { tocar: '#hamburguer', rotulo: 'abrir o menu', dur: 1.4 },
    { esperar: 1.2 },
    { tocar: '#menuMovel > a:nth-of-type(3)', rotulo: 'Projetos sociais',
      semNavegar: true, dur: 2.2 },
  ]},

  // ---------- G03  Filos ABC: primeira tela e os tres projetos  (cena 4) ----------
  { id: 'G03', pagina: ABC, endereco: E.abc, passos: [
    { esperar: 2.4 },
    { rolar: '#projetos', folga: 70, dur: 2.6 },
    { esperar: 2.6 },
    { rolar: 1700, dur: 2.2 },
    { esperar: 2.4 },
    { rolar: '#frentes', folga: 70, dur: 2.4 },
    { esperar: 2.6 },
    { rolar: 3000, dur: 2.4 },
    { esperar: 2.0 },
  ]},

  // ---------- G04  Dando Asas: Brasil e Cuba, depois Como ajudar  (cena 4) ----------
  { id: 'G04', pagina: ABC, endereco: E.abc, passos: [
    { avaliar: () => window.scrollTo(0, 5300) },
    { esperar: 1.6 },
    { rolar: '#paises', folga: 230, dur: 1.6 },
    { esperar: 1.4 },
    { tocar: '#paises > button:nth-of-type(1)',  rotulo: 'Brasil', dur: 2.6 },
    { tocar: '#paises > button:nth-of-type(12)', rotulo: 'Cuba',   dur: 3.0 },
    { rolar: '#doar', folga: 70, dur: 3.0 },
    { esperar: 2.2 },
    { rolar: 8300, dur: 2.6 },
    { esperar: 2.4 },
  ]},

  // ---------- G05  Corrente 300, primeira tela parada  (cenas 1, 5 e 6) ----------
  { id: 'G05', pagina: CORRENTE, endereco: E.corrente, passos: [
    { esperar: 6.0 },
  ]},

  // ---------- G06  Corrente: + ate 3, atalho 5, arrastar ate 10  (cena 6) ----------
  { id: 'G06', pagina: CORRENTE, endereco: E.corrente, passos: [
    { esperar: 1.4 },
    { tocar: '#mais', rotulo: '+ (2)', dur: 0.75 },
    { tocar: '#mais', rotulo: '+ (3)', dur: 1.9 },
    { tocar: '#vals > button:nth-of-type(3)', rotulo: 'atalho 5', dur: 2.2 },
    { arrastar: { alvo: '#faixa', para: 10, dur: 1.8 }, rotulo: 'arrastar ate 10' },
    { esperar: 2.6 },
    { rolar: 760, dur: 2.0 },                 // a barra flutuante aparece
    { esperar: 2.4 },
    { rolar: 1400, dur: 2.0 },
    { esperar: 2.0 },
  ]},

  // ---------- G07  Metas e progresso  (cena 7) ----------
  { id: 'G07', pagina: CORRENTE, endereco: E.corrente, passos: [
    { avaliar: () => window.scrollTo(0, 1500) },
    { esperar: 1.2 },
    { rolar: '#metas', folga: 70, dur: 2.2 },
    { esperar: 3.4 },                         // a barra principal cresce
    { tocar: '#d-mais', rotulo: '+ na barra flutuante', dur: 1.0 },
    { tocar: '#d-mais', rotulo: '+ na barra flutuante', dur: 2.4 },
    { rolar: 2700, dur: 2.4 },                // metas da cozinha
    { esperar: 3.0 },
    { rolar: '#avulso', folga: 150, dur: 2.2 },
    { esperar: 1.6 },
    { tocar: '#avulso > a:nth-of-type(2)', rotulo: 'R$ 20', semNavegar: true, dur: 2.4 },
  ]},

  // ---------- G08  Confianca: transparencia, caminho, regras, empresas  (cena 8) ----------
  { id: 'G08', pagina: CORRENTE, endereco: E.corrente, passos: [
    { avaliar: () => window.scrollTo(0, 3900) },
    { esperar: 1.2 },
    { rolar: '#transparencia', folga: 70, dur: 1.8 },
    { esperar: 2.2 },
    { rolar: '#caminho', folga: 70, dur: 2.0 },
    { esperar: 2.0 },
    { rolar: '#regras', folga: 70, dur: 2.0 },
    { esperar: 1.2 },
    { tocar: '#regras details:first-of-type summary', rotulo: 'abrir uma regra', dur: 2.4 },
    { rolar: '#empresas', folga: 70, dur: 2.0 },
    { esperar: 2.0 },
  ]},

  // ---------- G09  Escolinha: Todo mes e R$ 20  (cenas 1 e 9) ----------
  { id: 'G09', pagina: ANGOLA, endereco: E.angola, passos: [
    { esperar: 2.6 },
    { rolar: 330, dur: 1.6 },
    { esperar: 1.2 },
    { tocar: '#tipo > button:nth-of-type(1)',    rotulo: 'Todo mês', dur: 2.2 },
    { tocar: '#valores > button:nth-of-type(2)', rotulo: 'R$ 20',    dur: 3.0 },
    { esperar: 2.4 },
  ]},

  // ---------- G10  Escolinha: o que faz e as fotos  (cena 9) ----------
  { id: 'G10', pagina: ANGOLA, endereco: E.angola, passos: [
    { avaliar: () => window.scrollTo(0, 900) },
    { esperar: 1.2 },
    { rolar: '#escola', folga: 70, dur: 2.2 },
    { esperar: 3.0 },
    { rolar: 1700, dur: 2.2 },
    { esperar: 2.0 },
    { rolar: '#fotos', folga: 70, dur: 2.4 },
    { esperar: 3.4 },
  ]},

  // ---------- G11a/b/c  trocar de pagina pelas marcas do topo  (cena 10) ----------
  { id: 'G11a', pagina: ABC, endereco: E.abc, passos: [
    { esperar: 1.6 },
    { tocar: '.rede-marcas li:nth-child(2) a', rotulo: 'Corrente 300', semNavegar: true, dur: 1.8 },
  ]},
  { id: 'G11b', pagina: CORRENTE, endereco: E.corrente, passos: [
    { esperar: 1.6 },
    { tocar: '.rede-marcas li:nth-child(3) a', rotulo: 'Escolinha em Angola', semNavegar: true, dur: 1.8 },
  ]},
  { id: 'G11c', pagina: ANGOLA, endereco: E.angola, passos: [
    { esperar: 1.6 },
    { tocar: '.rede-marcas li:nth-child(1) a', rotulo: 'Filos ABC', semNavegar: true, dur: 1.8 },
  ]},

  // ---------- G12  rodape "Conheca a rede inteira"  (cena 10) ----------
  { id: 'G12', pagina: ABC, endereco: E.abc, passos: [
    { avaliar: () => window.scrollTo(0, 8400) },
    { esperar: 1.2 },
    { rolar: '.rede-cartoes', folga: 120, dur: 2.6 },
    { esperar: 5.5 },
  ]},

  // ---------- G13  espalhar: WhatsApp e Compartilhar  (cena 11) ----------
  { id: 'G13', pagina: CORRENTE, endereco: E.corrente, passos: [
    { avaliar: () => window.scrollTo(0, 7300) },
    { esperar: 1.4 },
    { rolar: '#espalhe', folga: 70, dur: 1.8 },
    { esperar: 1.4 },
    { tocar: '#grupo', rotulo: 'Entrar no grupo', semNavegar: true, dur: 2.4 },
    { tocar: '#fab-enviar', rotulo: 'Compartilhar', dur: 3.4 },
  ]},
];
