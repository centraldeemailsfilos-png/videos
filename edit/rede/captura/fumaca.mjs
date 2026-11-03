import { chromium } from 'playwright';
import path from 'node:path';

const RAIZ = process.cwd();
const paginas = [
  ['mapa',      'edit/rede/sites/rede/rede-filos.html'],
  ['abc',       'edit/rede/sites/rede/index.html'],
  ['corrente',  'edit/rede/sites/rede/corrente-300.html'],
  ['angola',    'edit/rede/sites/rede/escola-angola.html'],
  ['editora',   'edit/rede/sites/editora/index.html'],
];

const nav = await chromium.launch({ channel: 'chromium' });
const ctx = await nav.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });

for (const [id, rel] of paginas) {
  const pag = await ctx.newPage();
  const falhas = [], erros = [];
  pag.on('requestfailed', r => { if (!r.url().startsWith('file://')) falhas.push(r.url()); });
  pag.on('pageerror', e => erros.push(String(e).slice(0, 120)));
  // nada de rede: so arquivo local, para o render ser determinístico
  await pag.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
  await pag.goto('file://' + path.join(RAIZ, rel), { waitUntil: 'load', timeout: 45000 });
  await pag.evaluate(() => document.fonts.ready);
  await pag.waitForTimeout(1200);
  const info = await pag.evaluate(() => ({
    altura: document.documentElement.scrollHeight,
    titulo: document.title.slice(0, 48),
    fonte: getComputedStyle(document.body).fontFamily.split(',')[0],
    imgs: [...document.images].length,
    imgsQuebradas: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).length,
  }));
  await pag.screenshot({ path: `edit/rede/captura/fumaca_${id}.png` });
  console.log(`${id.padEnd(9)} ${String(info.altura).padStart(6)}px  fonte=${info.fonte.padEnd(14)} imgs=${info.imgs - info.imgsQuebradas}/${info.imgs}  erros=${erros.length}  req-bloq=${falhas.length}`);
  if (erros.length) console.log('           ', erros.slice(0, 3).join(' | '));
  await pag.close();
}
await nav.close();
