import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';

const paginas = [
  ['mapa',     'edit/rede/sites/rede/rede-filos.html'],
  ['abc',      'edit/rede/sites/rede/index.html'],
  ['corrente', 'edit/rede/sites/rede/corrente-300.html'],
  ['angola',   'edit/rede/sites/rede/escola-angola.html'],
  ['editora',  'edit/rede/sites/editora/index.html'],
];
const nav = await chromium.launch({ channel: 'chromium' });
const ctx = await nav.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
const tudo = {};
for (const [id, rel] of paginas) {
  const pag = await ctx.newPage();
  await pag.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
  await pag.goto('file://' + path.join(process.cwd(), rel), { waitUntil: 'load' });
  await pag.evaluate(() => document.fonts.ready);
  await pag.waitForTimeout(600);
  tudo[id] = await pag.evaluate(() => {
    const abs = e => Math.round(e.getBoundingClientRect().top + window.scrollY);
    const lim = s => (s || '').trim().replace(/\s+/g, ' ').slice(0, 46);
    return {
      altura: document.documentElement.scrollHeight,
      secoes: [...document.querySelectorAll('section[id],[id].sec,main>[id]')]
        .map(e => ({ id: e.id, y: abs(e), h: Math.round(e.getBoundingClientRect().height),
                     tit: lim((e.querySelector('h1,h2,h3') || {}).textContent) }))
        .filter(s => s.id),
      titulos: [...document.querySelectorAll('h1,h2')].map(e => ({ y: abs(e), t: lim(e.textContent) })),
      acoes: [...document.querySelectorAll('button[id],a[id],input[id],[role=tab],nav a')]
        .map(e => ({ sel: e.id ? '#' + e.id : null, tag: e.tagName.toLowerCase(),
                     txt: lim(e.textContent) || e.getAttribute('aria-label') || '',
                     href: (e.getAttribute('href') || '').slice(0, 34), y: abs(e) }))
        .filter(a => a.sel || a.href),
    };
  });
  await pag.close();
}
await nav.close();
fs.writeFileSync('edit/rede/captura/mapa_paginas.json', JSON.stringify(tudo, null, 1));
for (const [id, d] of Object.entries(tudo)) {
  console.log(`\n===== ${id}  (${d.altura}px) =====`);
  console.log('secoes:'); for (const s of d.secoes) console.log(`  ${String(s.y).padStart(6)}  #${s.id.padEnd(18)} h=${String(s.h).padStart(5)}  ${s.tit}`);
}
