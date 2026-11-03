import { gravar } from './gravar.mjs';
import { TOMADAS } from './tomadas.mjs';
const pedido = process.argv.slice(2);
const fila = pedido.length ? TOMADAS.filter(t => pedido.includes(t.id)) : TOMADAS;
if (!fila.length) { console.error('nenhuma tomada casa com', pedido.join(' ')); process.exit(1); }
for (const t of fila) {
  const t0 = Date.now();
  try {
    const m = await gravar(t, `edit/rede/gravacoes/${t.id}.mp4`);
    const toques = m.eventos.filter(e => e.tipo === 'toque' || e.tipo === 'arrastar');
    console.log(`${t.id.padEnd(5)} ${String(m.quadros).padStart(4)}q  ${String(m.duracao).padStart(6)}s  ` +
                `${toques.length} toques  [${((Date.now()-t0)/1000).toFixed(0)}s]`);
    for (const e of toques) console.log(`        ${String(e.t).padStart(6)}s  ${e.rotulo || e.alvo}` +
                                        (e.x === undefined ? '   << ALVO NAO ENCONTRADO' : ''));
  } catch (err) { console.log(`${t.id.padEnd(5)} FALHOU: ${String(err).slice(0, 150)}`); }
}
