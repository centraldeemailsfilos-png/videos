"""Gera, por cena, o dossie de tempo que a composicao precisa.

Junta: duracao medida no audio, a narracao com o tempo de cada palavra,
as palavras-chave onde o motion tem de bater, o texto na tela e as
gravacoes disponiveis. E a entrada dos briefings de construcao.
"""
import json, re, sys

FINAL = json.load(open('edit/rede/align/alinhamento_final.json', encoding='utf-8'))
ROT   = {c['n']: c for c in json.load(open('edit/rede/align/cenas_roteiro.json', encoding='utf-8'))}

# palavras em que o motion precisa bater, por cena (§6: "cada toque deve
# coincidir com a palavra correspondente na narracao")
CHAVES = {
 1: ['estrutura','tres','paginas','link','ligadas','editora'],
 2: ['Editora','casa','ABC','reune','Corrente','almocos','Escolinha','Angola'],
 3: ['primeiro','Editora','menu','toca','Projetos','sociais','ABC','toques'],
 4: ['conhecer','instituto','Dando','Asas','pais','ajudar','apadrinhar','escolinha','oficina','empresa'],
 5: ['segundo','direto','anuncio','Instagram','WhatsApp','campanha','Corrente','doacao'],
 6: ['Corrente','primeira','quantas','criancas','mais','menos','atalhos','arrastando','maozinha','valores','botao','dourado','acompanha'],
 7: ['metas','barra','padrinho','faltam','listrada','pessoa','cozinha','panelas','fogao','unica'],
 8: ['confianca','contas','passos','regras','empresas'],
 9: ['Escolinha','Angola','link','mes','vez','valor','apoiar','escola','fotos'],
10: ['importante','separado','isolado','topo','logo','projetos','fim','rede','toque'],
11: ['flutuantes','divulgar','WhatsApp','grupo','compartilha','link'],
12: ['Resumindo','conhecer','ABC','apadrinhar','Corrente','escola','Escolinha','links','casa','Editora'],
}

def normal(w): return re.sub(r'[^a-zà-ú0-9]', '', w.lower())

saida = {}
for n in range(1, 13):
    ws = [w for w in FINAL['palavras'] if w['cena'] == n]
    if not ws: continue
    c = ROT[n]
    chaves = []
    for alvo in CHAVES.get(n, []):
        na = normal(alvo)
        for w in ws:
            if normal(w['p']) == na and not any(k['palavra'] == w['p'] and abs(k['t'] - w['a']) < 0.3 for k in chaves):
                chaves.append({'palavra': w['p'], 't': w['a'], 'fim': w['z']}); break
    saida[n] = {
        'titulo': c['titulo'], 'ini': ws[0]['a'], 'fim': ws[-1]['z'],
        'dur': round(ws[-1]['z'] - ws[0]['a'], 2),
        'material': c['material'], 'texto_tela': c['texto_tela'],
        'narracao': c['narracao'],
        'chaves': sorted(chaves, key=lambda k: k['t']),
        'palavras': [{'p': w['p'], 'a': w['a'], 'z': w['z']} for w in ws],
    }
json.dump(saida, open('edit/rede/align/briefing.json','w'), ensure_ascii=False, indent=1)

alvo = int(sys.argv[1]) if len(sys.argv) > 1 else None
for n, d in saida.items():
    if alvo and n != alvo: continue
    print('\n===== Cena %d: %s =====' % (n, d['titulo']))
    print('  %.2fs -> %.2fs   (%.2fs)   material: %s' % (d['ini'], d['fim'], d['dur'], d['material']))
    print('  texto na tela: %s' % d['texto_tela'])
    print('  palavras-chave:')
    for k in d['chaves']: print('     %7.2fs  %s' % (k['t'], k['palavra']))
print('\nescrito edit/rede/align/briefing.json')
