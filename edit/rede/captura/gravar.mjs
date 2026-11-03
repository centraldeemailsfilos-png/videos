/* Motor de captura determinística das páginas reais.
 *
 * Tempo virtual do Chromium: o relógio da página só anda quando mandamos.
 * Assim 1 quadro = exatamente 33,333 ms de tempo de página, independente
 * de quanto o screenshot demora. O render é reproduzível.
 *
 * Cada tomada devolve um MP4 e um JSON de eventos (toque, destaque,
 * mudança de endereço) com o quadro exato em que cada um acontece, para
 * o motion da pós encaixar cursor e zoom na palavra certa da narração.
 */
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';

export const FPS = 30;
export const LARG = 390, ALT = 844, ESCALA = 2;

const cubico = t => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;

export async function gravar(tomada, destino) {
  const nav = await chromium.launch({ channel: 'chromium' });
  const ctx = await nav.newContext({ viewport: { width: LARG, height: ALT },
                                     deviceScaleFactor: ESCALA, reducedMotion: 'no-preference' });
  const pag = await ctx.newPage();
  await pag.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.abort());
  await pag.goto('file://' + path.join(process.cwd(), tomada.pagina), { waitUntil: 'load', timeout: 60000 });

  // nada de lazy: imagem que aparece no meio da rolagem estraga a tomada
  await pag.evaluate(async () => {
    document.documentElement.style.scrollBehavior = 'auto';
    const e = document.createElement('style');
    e.textContent = '::-webkit-scrollbar{display:none}html{scrollbar-width:none}';
    document.head.appendChild(e);
    for (const i of document.images) { i.loading = 'eager'; if (i.dataset.src && !i.src) i.src = i.dataset.src; }
    await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
    await document.fonts.ready;
  });
  await pag.waitForTimeout(900);

  const cdp = await ctx.newCDPSession(pag);
  let expirou;
  cdp.on('Emulation.virtualTimeBudgetExpired', () => { const f = expirou; expirou = null; f && f(); });
  const avancar = ms => new Promise(async res => {
    expirou = res;
    await cdp.send('Emulation.setVirtualTimePolicy',
      { policy: 'pauseIfNetworkFetchesPending', budget: ms, maxVirtualTimeTaskStarvationCount: 8000 });
  });
  await cdp.send('Emulation.setVirtualTimePolicy', { policy: 'pause' });

  fs.mkdirSync(path.dirname(destino), { recursive: true });
  const ff = spawn('ffmpeg', ['-v','error','-y','-f','image2pipe','-framerate',String(FPS),'-i','pipe:0',
    '-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-movflags','+faststart', destino],
    { stdio: ['pipe','inherit','inherit'] });
  let n = 0;
  const eventos = [];
  const escreve = async buf => {
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  };
  const quadro = async () => { await avancar(1000 / FPS); await escreve(await pag.screenshot()); n++; };
  const marcar = (tipo, extra = {}) => eventos.push({ q: n, t: +(n / FPS).toFixed(3), tipo, ...extra });
  const caixa = async sel => pag.evaluate(s => {
    const e = document.querySelector(s); if (!e) return null;
    const r = e.getBoundingClientRect();
    // 'topo', nao 't': 't' e o tempo do evento e seria sobrescrito
    return { x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2),
             esq: Math.round(r.left), topo: Math.round(r.top),
             larg: Math.round(r.width), alt: Math.round(r.height) };
  }, sel);

  for (const p of tomada.passos) {
    if (p.esperar) { for (let i = 0; i < Math.round(p.esperar * FPS); i++) await quadro(); }

    else if (p.rolar !== undefined) {
      const de = await pag.evaluate(() => window.scrollY);
      const para = typeof p.rolar === 'number' ? p.rolar : await pag.evaluate(([s, d]) => {
        const e = document.querySelector(s); if (!e) return window.scrollY;
        return Math.max(0, e.getBoundingClientRect().top + window.scrollY - (d || 0));
      }, [p.rolar, p.folga]);
      const total = Math.round((p.dur || 2) * FPS);
      marcar('rolar', { de: Math.round(de), para: Math.round(para) });
      for (let i = 1; i <= total; i++) {
        await pag.evaluate(y => window.scrollTo(0, y), de + (para - de) * cubico(i / total));
        await quadro();
      }
    }

    else if (p.tocar) {
      const c = await caixa(p.tocar);
      marcar('toque', { alvo: p.tocar, rotulo: p.rotulo || '', ...(c || {}) });
      await pag.evaluate(([s, sem]) => {
        const e = document.querySelector(s); if (!e) return;
        // tomada que so mostra o toque: a navegacao vira corte na edicao
        if (sem) e.addEventListener('click', ev => ev.preventDefault(), { capture: true, once: true });
        e.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
        e.click();
        e.dispatchEvent(new PointerEvent('pointerup', { bubbles: true }));
      }, [p.tocar, !!p.semNavegar]);
      for (let i = 0; i < Math.round((p.dur || 0.5) * FPS); i++) await quadro();
    }

    else if (p.arrastar) {
      const { alvo, para: valor, dur = 1.6 } = p.arrastar;
      const c = await caixa(alvo);
      marcar('arrastar', { alvo, rotulo: p.rotulo || '', para: valor, ...(c || {}) });
      const ini = await pag.evaluate(s => +document.querySelector(s).value, alvo);
      const total = Math.round(dur * FPS);
      for (let i = 1; i <= total; i++) {
        await pag.evaluate(([s, v]) => {
          const e = document.querySelector(s); e.value = v;
          e.dispatchEvent(new Event('input', { bubbles: true }));
          e.dispatchEvent(new Event('change', { bubbles: true }));
        }, [alvo, Math.round(ini + (valor - ini) * cubico(i / total))]);
        await quadro();
      }
    }

    else if (p.avaliar) { await pag.evaluate(p.avaliar); marcar('avaliar', { rotulo: p.rotulo || '' }); }
  }

  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await nav.close();
  const meta = { id: tomada.id, pagina: tomada.pagina, fps: FPS,
                 larg: LARG, alt: ALT, escala: ESCALA,
                 quadros: n, duracao: +(n / FPS).toFixed(3),
                 endereco: tomada.endereco || '', eventos };
  fs.writeFileSync(destino.replace(/\.mp4$/, '.json'), JSON.stringify(meta, null, 1));
  return meta;
}
